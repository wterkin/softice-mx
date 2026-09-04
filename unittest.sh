#~/bin/env/bin/python3 test_softice.py -v
clear
touch flags/unittest.flg
#/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_moderator.py' -vv >unittest.log 2>unittest2.log
#/home/app/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_theolog.py' -vv >unittest.log 2>unittest2.log
#/home/app/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_meteorolog.py' -vv >unittest.log 2>unittest2.log
/home/app/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_database.py' -vv >unittest.log 2>unittest2.log