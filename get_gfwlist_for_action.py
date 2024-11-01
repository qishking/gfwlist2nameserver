#! /usr/bin/python

import base64
import re


# openwrt直接存到/etc/smartdns/address.conf,记得备份原文件
OUTPUT_FILE_PATH = 'gfwlist.conf'

# 0. fetch origin gfwlist
# origin gfwlst path
ori_gfwlst = 'gfwlist.txt'

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


# 1. 直接使用github上原始版gfwlst
with open(ori_gfwlst, 'r') as ori_f:
    with open(file=TEMP_FILE_PATH, mode='w', encoding='utf-8') as f:
        d = base64.b64decode(ori_f.read())
        f.write(d.decode('utf-8'))


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
