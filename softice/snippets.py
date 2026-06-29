from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Создаём асинхронный движок
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/mydb"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,              # Логировать SQL-запросы (для отладки)
    pool_size=10,           # Размер пула соединений
    max_overflow=20,        # Дополнительные соединения при пиковой нагрузке
    pool_pre_ping=True,     # Проверять соединение перед использованием
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # Важно! Не инвалидировать объекты после commit
)


from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


async def create_user(username: str, email: str) -> User:
    async with AsyncSessionLocal() as session:
        async with session.begin():  # Автоматический commit/rollback
            new_user = User(username=username, email=email)
            session.add(new_user)
            await session.flush()  # Получаем ID без commit
            return new_user



from sqlalchemy import select

async def get_user_by_id(user_id: int) -> User | None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

async def get_all_users() -> list[User]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

async def search_users(pattern: str) -> list[User]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.username.ilike(f"%{pattern}%"))
        )
        return result.scalars().all()


async def update_user_email(user_id: int, new_email: str) -> bool:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                return False
            user.email = new_email
            return True


async def delete_user(user_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                return False
            await session.delete(user)
            return True


# Вариант 1: Автоматический begin/commit/rollback
async with AsyncSessionLocal() as session:
    async with session.begin():
        user = User(username="alice", email="alice@example.com")
        session.add(user)
        # Если здесь возникнет исключение — автоматический rollback
        # Если всё хорошо — автоматический commit

# Вариант 2: Ручное управление
async with AsyncSessionLocal() as session:
    try:
        user = User(username="bob", email="bob@example.com")
        session.add(user)
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username}



class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, username: str, email: str) -> User:
        user = User(username=username, email=email)
        self.session.add(user)
        await self.session.flush()
        return user

# Использование
async with AsyncSessionLocal() as session:
    repo = UserRepository(session)
    user = await repo.create("charlie", "charlie@example.com")
    await session.commit()

# ❌ ПЛОХО: заблокирует event loop
session.execute(select(User))

# ✅ ХОРОШО
await session.execute(select(User))



# ❌ ПЛОХО: гонка состояний
session = AsyncSessionLocal()
asyncio.create_task(task1(session))
asyncio.create_task(task2(session))

# ✅ ХОРОШО: каждая корутина со своей сессией
async def task1():
    async with AsyncSessionLocal() as session:
        # ...

async def task2():
    async with AsyncSessionLocal() as session:
        # ...


# ❌ ПЛОХО: изменения не сохранятся
async with AsyncSessionLocal() as session:
    user = User(username="test")
    session.add(user)
    # Забыл commit!

# ✅ ХОРОШО
async with AsyncSessionLocal() as session:
    async with session.begin():
        user = User(username="test")
        session.add(user)


async def init_db():
    async with engine.begin() as conn:
        # Создать все таблицы
        await conn.run_sync(Base.metadata.create_all)
        
        # Или удалить и создать заново (для разработки)
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)

# Запуск
asyncio.run(init_db())



