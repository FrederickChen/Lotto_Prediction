# coding=utf-8
from __future__ import unicode_literals

import logging
import os
import re
import time

try:
    from urllib.parse import urlparse  # py3
except:
    from urlparse import urlparse  # py2

import requests
from bs4 import BeautifulSoup

# url='https://www.ozlotteries.com/oz-lotto/results/december-2017'
def parse_page(url,filepath):
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    tags = soup.find_all(class_="results-number-set__number--ns1 number")
    numbers = [0,0,0,0,0,0,0]
    i = 0
    j = 1
    with open(filepath,'a') as f:
        for tag in tags:
            numbers[i] = int(tag.get_text())
            i = i+1
            if i == 7:
                i = 0
                if j == 1:
                    numbers.sort()
                    k=0
                    for number in numbers:
                        f.write(str(number))
                        k=k+1
                        if(k<7):
                            f.write(',')
                    f.write('\n')
                j = (j+1)% 2

pre_url='https://www.ozlotteries.com/oz-lotto/results/'
months = ['january','february','march','april','may','june','july','august','september','october','november','december']
years = [2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
filepath = 'lotto_result.txt'

# 2005
for month in ['october','november','december']:
    url = pre_url+month+'-'+str(2005)
#print(url)
    parse_page(url,filepath)

# 2006 - 2018
for year in years:
    for month in months:
        url = pre_url + month + '-' + str(year)
#        print(url+'\n')
        parse_page(url,filepath)
        
# 2019
url = 'https://www.ozlotteries.com/oz-lotto/results/january-2018'
parse_page(url,filepath)


