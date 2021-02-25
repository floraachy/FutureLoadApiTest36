技术要点：

- 正则表达式替换

- middlehandler 中间层 done

- 响应结果数据提取 extractor

- 多值断言
# 第一版多值断言
            # assert actual_result["code"] == expected["code"]
            # assert actual_result["msg"] == expected["msg"]

# 第二版多值断言
            for key, value in expected.items():
                assert actual_result["key"] == value

# 第三版断言
            """
            jsonpath的表达式作为key放置在预期结果的字典里面
            expected = {"$..code": 0, "$..msg": "OK"}
            for key, value in expected.items():
                # 实际结果：jsonpath(actual_result, key) 
                assert jsonpath(actual_result, key)[0] == value
            """

- 用例依赖

- 数据库操作

等等。