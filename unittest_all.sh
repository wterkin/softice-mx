#!/bin/sh
# /home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_babbler.py" -vv  >> unittest.log 2>> unittest2.log
# echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
# echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Barman %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% > unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Barman %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% > unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_barman.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%% Basis %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%% Basis %%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
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
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_majordomo.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
rem pluma unittest2.log &
