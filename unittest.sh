#~/bin/env/bin/python3 test_softice.py -v
clear
touch flags/unittest.flg
#/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_babbler.py' -vv >unittest.log 2>unittest2.log
#/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_callbacks.py' -vv >unittest.log 2>unittest2.log
#/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_collector.py' -vv >unittest.log 2>unittest2.log
#/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_gambler.py' -vv >unittest.log 2>unittest2.log
#/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_haijin.py' -vv >unittest.log 2>unittest2.log
#/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_librarian.py' -vv >unittest.log 2>unittest2.log
#/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_majordomo.py' -vv >unittest.log 2>unittest2.log
#/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_moderator.py' -vv >unittest.log 2>unittest2.log
#/home/app/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_theolog.py' -vv >unittest.log 2>unittest2.log
#/home/app/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_meteorolog.py' -vv >unittest.log 2>unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_stargazer.py' -vv >unittest.log 2>unittest2.log
#/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_statistic.py' -vv >unittest.log 2>unittest2.log
echo ===================================================
cat unittest2.log
echo ---------------------------------------------------
cat unittest.log
