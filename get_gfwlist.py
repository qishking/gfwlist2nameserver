#! /usr/bin/python

import base64
import re
import urllib.request

# 0.
# gfwlst国内下载地址
# GFWLST_URL = "https://gitlab.com/gfwlist/gfwlist/raw/master/gfwlist.txt"
GFWLST_URL = "https://github.com/gfwlist/gfwlist/raw/master/gfwlist.txt"

# openwrt直接存到/etc/smartdns/address.conf,记得备份原文件
OUTPUT_FILE_PATH = 'gfwlist.conf'


# 临时字符串
ORIG_GFW_STR = ''

# 保存到set去掉重复数据
PURE_DN_DATA = set()

# domain name only
DN_ONLY = 'domain_name_only.txt'

# 匹配域名的正则表达式
# python 3.11以下版本用这个简化正则表达式
# PATTERN_DN = r'(\w+\.)+\w+'
# 以下正则表达式可以精确匹配规范域名，如：域名字段中开始和结尾不能为‘-’
PATTERN_DN = r'((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}'


# 1. 下载gfwlst
try:
    with urllib.request.urlopen(GFWLST_URL) as req:
        d = base64.b64decode(req.read())
        ORIG_GFW_STR = d.decode('utf-8')
except urllib.error.HTTPError as e:
    print(e.code)
    raise


# 2. 提取域名
for line in (ORIG_GFW_STR.split(sep='\n')):
    if 'General List End' not in line:
        dn = re.search(PATTERN_DN, line)
        if dn:
            PURE_DN_DATA.add(dn.group())
        else:
            continue
    else:
        break

# 3. 保存一份只有域名的文件
with open(file=DN_ONLY, mode='w', encoding='utf-8') as f:
    f.write('\n'.join(PURE_DN_DATA))

# 4. 写入配置文件
with open(file=OUTPUT_FILE_PATH, mode='w', encoding='utf-8') as f:
    ns_data = (f'nameserver /{dn}/GFW' for dn in PURE_DN_DATA)
    f.write('\n'.join(ns_data))

# 5. smartdns reload配置文件
# import os
# os.system('service smartdns reload')
