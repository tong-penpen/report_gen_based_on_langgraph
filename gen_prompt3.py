import os
import pandas as pd


def excel_to_prompt(excel_path2, excel_path3, street, fileName):
    df2 = pd.read_excel(excel_path2, engine="openpyxl")
    df3 = pd.read_excel(excel_path3, engine="openpyxl")
    with open(fileName, "w", encoding="utf-8") as f:
        pass  # 不需要写入任何内容，只是为了清空文件
    str1 = ""
    str2 = ""
    str3 = ""
    curPrompt = (
        "你是一个政府工作者，你擅长数据分析和写政府工作报告，请你根据以下内容，\n"
    )
    for idx, row2 in df2.iterrows():
        # if idx == 0:
        #     continue
        row3 = df3.iloc[idx]
        if row2[1] != str1 and str1 != "":
            curPrompt += f"-代表一级指标，--代表二级指标，---代表三级指标，\n"
            curPrompt += f"帮我写一份{street}的相关指标数据的详情分析，主要分析数据的变化波动，注意不需要原因分析和相关建议\n"
            curPrompt += f"输出格式：标题：{street}指标{row2[1]}详情分析\n"
            with open(fileName, "a", encoding="utf-8") as f:
                f.write("*" * 50 + "\n" + curPrompt + "\n" + "*" * 50)
            curPrompt = "你是一个政府工作者，你擅长数据分析和写政府工作报告，请你根据以下内容，\n"
        if str1 != row2[1]:
            curPrompt += f"-{row2[1]}\n"
            curPrompt += f" 指标定义: {row2[2]}\n"
            curPrompt += f" {row2[0]}指标得分: {row2[3]}\n"
            curPrompt += f" {row3[0]}指标得分: {row3[3]}\n"
        if str2 != row2[4]:
            curPrompt += f"--{row2[4]}\n"
            curPrompt += f"  指标定义: {row2[5]}\n"
            curPrompt += f"  {row2[0]}指标得分: {row2[6]}\n"
            curPrompt += f"  {row3[0]}指标得分: {row3[6]}\n"
        if str3 != row3[7]:
            curPrompt += f"---{row2[7]}\n"
            curPrompt += f"   指标定义: {row2[8]}\n"
            curPrompt += f"   {row2[0]}指标得分: {row2[9]}\n"
            curPrompt += f"   {row3[0]}指标得分: {row3[9]}\n"
            curPrompt += f"   中间变量: {row2[10]}\n"
            curPrompt += f"   变量定义: {row2[11]}\n"
            curPrompt += f"   未经归一化的量化公式: {row2[12]}\n"
            curPrompt += f"   量化公式(已归一至90~100): {row2[13]}\n"
        str1 = row2[1]
        str2 = row2[4]
        str3 = row2[7]


def get_score(data, street):
    score = str(data).split(",")
    return str(score[ord(street) - ord("A")])


def main():
    excel_path2 = os.path.join(
        os.path.dirname(__file__), "../assets/2024年2季度圆融指数指标定义与数值.xlsx"
    )
    excel_path3 = os.path.join(
        os.path.dirname(__file__), "../assets/2024年3季度圆融指数指标定义与数值.xlsx"
    )
    street1 = "娄葑街道"
    street2 = "斜塘街道"
    street3 = "唯亭街道"
    street4 = "胜浦街道"
    street5 = "金鸡湖街道"
    excel_to_prompt(excel_path2, excel_path3, street5, street5 + "prompt.txt")


if __name__ == "__main__":
    main()
