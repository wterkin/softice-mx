#!/bin/sh
# /home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_babbler.py" -vv  >> unittest.log 2>> unittest2.log
# echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
# echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Barman %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% > unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Barman %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% > unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_barman.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Callbacks %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Callbacks %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_callbacks.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Config %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Config %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_config.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Gambler %%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Gambler %%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_gambler.py" -vv  > unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Haijin %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Haijin %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_haijin.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Librarian %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Librarian %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_librarian.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Majordomo %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Majordomo %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_majordomo.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Meteorolog %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Meteorolog %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_meteorolog.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Moderator %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Moderator %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_moderator.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Stargazer %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Stargazer %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_stargazer.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
# pluma unittest2.log &
