from datetime import datetime
import time
import pandas as pd


class Test:
    def __init__(self) -> None:
        pass

    def compute(self, dataframe_dict:dict, current_time) -> pd.DataFrame:
        input1 = dataframe_dict.get("it_ck_test_2.input1")
        input2 = dataframe_dict.get("it_ck_test_2.input2")

        # 取第 0 行的值
        value1 = input1.iloc[0]["value"] if not input1.empty else 0
        value2 = input2.iloc[0]["value"] if not input2.empty else 0

        # 求和和求积
        sum_value = value1 + value2
        product_value = value1 * value2

        # 创建两个结果 DataFrame
        sum_result = pd.DataFrame([{"time": current_time, "value": sum_value}])
        product_result = pd.DataFrame([{"time": current_time, "value": product_value}])

        result = {}
        result["output1"] = sum_result
        result["output2"] = product_result

        return result
    
    def compute_history(self, dataframe_dict:dict) -> dict:
        input1 = dataframe_dict.get("it_ck_test_2.input1")
        input2 = dataframe_dict.get("it_ck_test_2.input2")
        
        # 确保时间列为 datetime 类型
        input1["time"] = pd.to_datetime(input1["time"])
        input2["time"] = pd.to_datetime(input2["time"])

        # 合并两个 DataFrame，按 time 对齐
        merged = pd.merge(input1, input2, on="time", how="outer", suffixes=("_1", "_2"))

        # 计算时间相同的求和，时间不同的保留
        merged["sum_value"] = merged["value_1"].fillna(0) + merged["value_2"].fillna(0)

        # 计算时间相同的求乘积，时间不同的保留
        merged["product_value"] = merged["value_1"].fillna(1) * merged["value_2"].fillna(1)

        # 分别生成两个结果表
        sum_result = merged[["time", "sum_value"]].rename(columns={"sum_value": "value"}).sort_values(by="time").reset_index(drop=True)
        product_result = merged[["time", "product_value"]].rename(columns={"product_value": "value"}).sort_values(by="time").reset_index(drop=True)

        result = {}
        result["output1"] = sum_result
        result["output2"] = product_result

        return result