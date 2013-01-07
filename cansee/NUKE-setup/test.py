#!/usr/bin/env python
#-*-coding:utf-8-*-'
#Filename:download_file.py
import sys,os
import urllib
def urlcallback(a,b,c):
    """
        call back function
        a,已下载的数据块
        b,数据块的大小
        c,远程文件的大小
    """
    print "callback"
    prec=100.0*a*b/c
    if 100 < prec:
        prec=100
    print "%.2f%%"%(prec,)
    
def main(argv):
    """
        main
    """
    print "start..."
    urllib.urlretrieve("http://huangxf.sunupcg.cn:8000/Moses.pyc","Moses.pyc",urlcallback)
    print "end..."
    
if __name__=="__main__":
    main(sys.argv[1:])

