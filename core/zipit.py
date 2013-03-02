#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:  rais --<CGE>
# Purpose: CGE system zip it
# Created: 2013/03/01

import os
from zipfile import ZipFile, ZIP_DEFLATED

from os.path import join
def zipfolder(foldername, filename, includeEmptyDIr=True):
	zip = ZipFile(filename, 'w', ZIP_DEFLATED)
	for root, dirs, files in os.walk(foldername):
		if '.git' in root:
			continue
		rel_path = os.path.relpath(root, os.path.dirname(foldername))
		for name in files:
			zip.write(join(root, name), join(rel_path,name))
	zip.close()


def extract(zip_file, output_dir):

	f_zip = ZipFile(zip_file, 'r')
	# 解压所有文件到指定目录
	f_zip.extractall(output_dir)
	# 逐个解压文件到指定目录
	#for f in f_zip.namelist():
	#	f_zip.extract(f, os.path.join(output_dir, 'bak'))
def extract2(zip_file, output_dir,first_dir):
	f_zip = ZipFile(zip_file, 'r')
	for f in f_zip.namelist():
		f_zip.extract(f, os.path.join(output_dir, first_dir))
if __name__ == '__main__':
	source_path = r'/home/rais/.nuke/user/7.0/'
	zipname = '/cifs/10.0.0.16/digitmovie_render/CGE_SYSTEM/nuke_system/nukePlugin/7.0.dat'
	zipfolder(source_path,zipname)
	#extract(zipname,'7.0_un')