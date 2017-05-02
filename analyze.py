# -*- coding:utf-8 -*-
import re
from punctuation import is_punc
from keywords import is_keyword
from idn import is_idn
from digits import is_digits

# 读取目标文件
file = 'example.txt'
try:
    fin = open(file, 'r')
except:
    print "Input file does not exists: %s" % file
    quit(0)

lines = fin.readlines()  # 读取所有行并返回列表
if len(lines) <= 0:
    print "Input file %s is empty" % file
    quit(0)


def breakup_line(line):  # 分析列表中每个字符串
    words = line.split()  # 将字符串拆分为字符序列
    new_words = []
    for i in range(len(words)):  # 从0到words的长度-1
        if words[i][0] in ("'",'"') and words[i][-1] in ("'",'"'):  # 通过有无单双引号判断字符串
            new_words.append(words[i])
        else:
            t = re.findall(r"[1-9]\d*\.\d*|-*0.\d*|[\w]+|[^\s\w]", words[i])  # 通过正则表达式提取符合匹配的所有单词
            # 表达式：（任意浮点小数）或(任意英文字母一次)或（从行头开始匹配任意英文字母）
            new_words.extend(t)
    return new_words


def get_strings(words):
    new_words = []
    adding = False
    temp_string = ''
    skip = False
    for w in words:
        if ('"' in w or "'" in w) and (w.count('"') < 2 and w.count("'") < 2):
            adding = not adding
        if not adding:
            new_words.append(temp_string+w)
            temp_string = ''
            skip = True
        if adding:
            temp_string += w + ' '
        else:
            if skip:
                skip = False
            else:
                new_words.append(w)
    return new_words


skip = False
for line in lines:
    if '#' in line:
        line = line[:line.index('#')]
    tokens = breakup_line(line)
    final = get_strings(tokens)
    for c, item in enumerate(final):
        if not skip:
            if is_punc(item):
                try:
                    if is_punc(item + final[c+1]):
                        print '%s       _' % str(item + final[c+1])
                        skip = True
                    else:
                        print '%s       _' % item
                except:
                    print '%s       _' % item
            elif is_keyword(item):
                pass
            elif is_idn(item):
                pass
            else:
                is_digits(item)
        else:
            skip = False  
print "ENDMARKER"
