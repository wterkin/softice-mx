#!/bin/sh
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_gambler.py" -vv  > unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_gambler.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_haijin.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
# /home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_babbler.py" -vv  >> unittest.log 2>> unittest2.log
# echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
# echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
/home/user/bin/env/matrix/bin/python -m unittest discover tests/ -p "test_barman.py" -vv  >> unittest.log 2>> unittest2.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest.log
echo %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% >> unittest2.log
pluma unittest2.log &
