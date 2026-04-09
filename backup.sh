#!/bin/sh
archive_name=softice-mx_`date "+%y%m%d_%H%M"`
7z a -t7z -m0=LZMA2 -mmt=on -mx7 -md=32m -mfb=64 -ms=8g -mqs=on -sccUTF-8 -bb0 -bse0 -bsp2 -w -mtc=on -mta=on ../$archive_name ../softice-mx 
cp ../$archive_name.7z /media/yandex/Private/Projects/softice-mx/
ls /media/yandex/Private/Projects/softice-mx/ | grep $archive_name.7z