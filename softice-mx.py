#!/home/app/bin/python/matrix/bin/python
import asyncio

try:
    from softice import main

    # Run the main function of the bot
    asyncio.get_event_loop().run_until_complete(main.main())
except ImportError as e:
    print("Unable to import softice.main:", e)


