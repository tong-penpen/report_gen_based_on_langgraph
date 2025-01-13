def gen_human_message():
    res = ""
    street = ["娄葑街道", "金鸡湖街道", "唯亭街道", "胜浦街道", "斜塘街道"]
    ind = [
        "社会协同",
        "协商参与",
        "城市运行",
        "公共服务",
        "社会治安",
        "法制保障",
        "科技支撑",
    ]
    cnt = 1
    for i in range(len(street)):
        for j in range(len(ind)):
            res += f"{cnt}. "
            cnt += 1
            res += gen_task(street[i], ind[j])
            res += "\n"
    return res


def gen_task(street, ind):
    res = ""
    res += f"请生成{street}，{ind}指标的报告，你需要先绘制图像，然后进行详情分析，然后进行原因分析，然后进行建议，最后调整格式"
    return res


if __name__ == "__main__":
    print(gen_human_message())
