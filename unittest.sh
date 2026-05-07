#~/bin/env/bin/python3 test_softice.py -v
clear
touch flags/unittest.flg
/home/user/bin/env/matrix/bin/python -m unittest discover -s tests/ -p 'test_haijin.py' -vv >unittest.log 2>unittest2.log
