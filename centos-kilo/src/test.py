#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from config import *
from func import *

def exportTest():
  os.putenv('OS_TOKEN','123456'); 
  os.system("export")
  #os.system('bash')

def main():
  exportTest()

if __name__ == '__main__':
  main()