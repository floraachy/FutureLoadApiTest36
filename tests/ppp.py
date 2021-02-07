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


# # . 只能匹配任意一个字符
# # 需要匹配的字符串
# target = "This is a test that generate by flora."
# # 匹配规则
# pattern = "that."
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result)
# print(result.group(0))


# # {m, n} 匹配m-n次，最少m次， 最多n次。贪婪模式：尽可能多的匹配。
# #  需要匹配的字符串
# target = "This is a test that generate by flora."
# # 匹配规则
# pattern = ".{2,3}"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result)
# print(result.group())
#
#
# # {m} 匹配m次
# #  需要匹配的字符串
# target = "This is a test that generate by flora."
# # 匹配规则
# pattern = ".{2}"
# # 根据规则，对指定字符串进行匹配
# result = re.search(pattern=pattern, string=target)
# # 得到的是一个匹配对象
# print(result)
# print(result.group())

# ? 表示非贪婪模式，尽可能少的匹配
#  需要匹配的字符串
target = '{"member_id": #member_id#, "loan_id": #loan_id#, "amount": 50000}'
# 匹配规则
pattern = "#??"
# 根据规则，对指定字符串进行匹配
result = re.search(pattern=pattern, string=target)
# 得到的是一个匹配对象
print(result)
print(result.group()) # 输出：#member_id#




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