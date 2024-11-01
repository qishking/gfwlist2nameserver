#! /usr/bin/python

import base64
import re
import urllib.request

# 0.
# gfwlst国内下载地址
GFWLST_URL = "https://gitlab.com/gfwlist/gfwlist/raw/master/gfwlist.txt"
# GFWLST_URL = "https://github.com/gfwlist/gfwlist/raw/master/gfwlist.txt"

# openwrt直接存到/etc/smartdns/address.conf,记得备份原文件
OUTPUT_FILE_PATH = 'gfwlist.conf'


# 可以设置为/var/temp目录
TEMP_FILE_PATH = 'tmp_gfwlist.txt'

# 保存到set去掉重复数据
pure_dn_data = set()

# domain name only
dn_only = 'domain_name_only.txt'

# 匹配域名的正则表达式
# python 3.11以下版本用这个简化正则表达式
# pattern_dn = r'(\w+\.)+\w+'
# 以下正则表达式可以精确匹配规范域名，如：域名字段中开始和结尾不能为‘-’
pattern_dn = r'((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}'


# 1. 下载gfwlst
try:
    with urllib.request.urlopen(GFWLST_URL) as req:
        with open(file=TEMP_FILE_PATH, mode='w', encoding='utf-8') as f:
            d = base64.b64decode(req.read())
            f.write(d.decode('utf-8'))
except urllib.error.HTTPError as e:
    print(e.code)
    raise


# 2. 提取域名
with open(TEMP_FILE_PATH, 'r') as f:
    for line in f:
        if 'General List End' not in line:
            dn = re.search(pattern_dn, line)
            if dn:
                pure_dn_data.add(dn.group())
            else:
                continue
        else:
            break

# 3. 保存一份只有域名的文件
with open(file=dn_only, mode='w', encoding='utf-8') as f:
    f.write('\n'.join(pure_dn_data))

# 4. 写入配置文件
with open(file=OUTPUT_FILE_PATH, mode='w', encoding='utf-8') as f:
    ns_data = (f'nameserver /{dn}/GFW' for dn in pure_dn_data)
    f.write('\n'.join(ns_data))

# 5. smartdns reload配置文件
# import os
# os.system('service smartdns reload')