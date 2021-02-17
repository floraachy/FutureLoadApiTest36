"""
=================================
Author: Flora Chen
Time: 2021/2/1 20:28
-_- -_- -_- -_- -_- -_- -_- -_-
=================================
"""
import re

# # 需要匹配的字符串
# target = "This is a test that generate by flora."
# # 匹配规则
# pattern = "flora"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result)  # 输出：<re.Match object; span=(32, 37), match='flora'>
# # 得到最终的结果，默认值为0  result.group() = result.group(0)
# print(result.group(0)) # 输出：flora

# # [bco] 表示中括号当中任选其一
# # 需要匹配的字符串
# target = "This is a test that generate by flora."
# # 匹配规则
# pattern = "fl[bco]ra"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result)  # 输出：<re.Match object; span=(32, 37), match='flora'>
# print(result.group(0)) # 输出：flora


# # . 只能匹配任意一个字符，除了\n
# # 需要匹配的字符串
# target = "This is a test that generate by flora."
# # 匹配规则
# pattern = "that."
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result) # 输出： <_sre.SRE_Match object; span=(15, 20), match='that '>
# print(result.group(0)) # 输出：that


# # {m, n} 匹配m-n次，最少m次， 最多n次。贪婪模式：尽可能多的匹配。
# #  需要匹配的字符串
# target = "This is a test that generate by flora."
# # 匹配规则
# pattern = ".{2,3}"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result) # 输出：<_sre.SRE_Match object; span=(0, 3), match='Thi'>
# print(result.group()) # 输出：Thi


# # {m} 匹配m次
# #  需要匹配的字符串
# target = "This is a test that generate by flora."
# # 匹配规则
# pattern = ".{2}"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result) # 输出：<_sre.SRE_Match object; span=(0, 2), match='Th'>
# print(result.group()) # 输出：Th

# {,} 如果不写数字就是无穷
# target = '{"member_id": #member_id#, "loan_id": #loan_id#, "amount": 50000}'
# # 匹配规则
# pattern = "#.{,}#"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result) # 输出：<_sre.SRE_Match object; span=(14, 47), match='#member_id#, "loan_id": #loan_id#'>
# print(result.group()) # 输出：#member_id#, "loan_id": #loan_id#

# * 表示匹配0次或多次
# ? 表示非贪婪模式，尽可能少的匹配
#  需要匹配的字符串
# target = '{"member_id": #member_id#, "loan_id": #loan_id#, "amount": 50000}'
# # 匹配规则
# pattern = "#.*?#"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result) # 输出：<_sre.SRE_Match object; span=(14, 25), match='#member_id#'>
# print(result.group()) # 输出：#member_id#


# # * 表示匹配0次或多次
# # ? 表示非贪婪模式，尽可能少的匹配
# #  需要匹配的字符串
# target = '{"member_id": #member_id#, "loan_id": #loan_id#, "amount": 50000}'
# # 匹配规则
# pattern = "#.*?#"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result)
# print(result.group()) # 输出：#member_id#

# # \w：匹配字母
# target = '{"member_id": #member_id#, "loan_id": #loan_id#, "amount": 50000}'
# # 匹配规则
# pattern = "\w"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result)  # 输出：<_sre.SRE_Match object; span=(2, 3), match='m'>
# print(result.group())  # 输出：m

# # \d：匹配数字
# target = '{"member_id": #member_id#, "loan_id": #loan_id#, "amount": 50000}'
# # 匹配规则
# pattern = "\d"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result)  # 输出：<_sre.SRE_Match object; span=(59, 60), match='5'>
# print(result.group())  # 输出：5

# # +：匹配任意字符一次或任意次
# target = '{"member_id": #member_id#, "loan_id": #loan_id#, "amount": 50000}'
# # 匹配规则
# pattern = "\d+"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result)  # 输出：<_sre.SRE_Match object; span=(59, 60), match='50000'>
# print(result.group())  # 输出：50000

# ()分组: 不加括号默认只有1个组，可以多个括号分多个组
target = '{"member_id": #member_id#, "loan_id": #loan_id#, "amount": 50000}'
pattern = "#(.*?)#"
result = re.search(pattern=pattern, string=target)
print(result.group())  # 输出：#member_id#
print(result.group(0))  # 输出：#member_id#
print(result.group(1))  # 输出：member_id

# class Data:
#     """
#     finditer会多次去寻找匹配的数据
#     search只会寻找一次
#     """
#     member_id = "1234444"
#     loan_id = "15555"
#
#
# # ()分组: 不加括号默认只有1个组，可以多个括号分多个组
# target = '{"member_id": #member_id#, "loan_id": #loan_id#, "amount": 50000}'
# pattern = "#(.*?)#"
# results = re.finditer(pattern=pattern, string=target)
# for result in results:
#     old = result.group()
#     key = result.group(1) # 序号默认是从0开始
#     new = getattr(Data, key, "")
#     target = target.replace(old, new)
#
# print(target)  # 输出：{"member_id": 1234444, "loan_id": 15555, "amount": 50000}
