import numpy as np
import pandas as pd


# "weight": None,  # 体重
# "height": None,  # 身高
# "gender": None,  # 性别
# "first_tide": None,  # 初潮年龄
# "menopause": None,  # 绝经
# "live_birth": None,  # 首次分娩
# "breastfeeding": None,  # 哺乳经历
# "biopsy": None,  # 活检史或乳腺良性疾病手术史
# "family_cancer": None,  # 一级亲属（母亲、姐妹、女儿）是否患有乳腺癌
# "brac12": None,  # 是否有已知的BRAC1/2基因突变
# "anxiety": None,  # 焦虑
# "high_calorie": None,  # 高卡路里


def generate_data(n=50):

    data = {"age":[], "weight": [], "height": [], "first_tide": [], "menopause": [], "live_birth": [], "breastfeeding": [], "biopsy": [], "family_cancer": [], "brac12": [], "anxiety": [], "high_calorie": [], "no_typical": []}

    for i in range(n):
        age = np.random.randint(35, 80)  # 年龄
        weight = np.random.randint(40, 80)  # 体重
        height = np.random.randint(140, 190)  # 身高
        first_tide = np.random.randint(7, 17)  # 初潮年龄
        if age < 55:
            menopause = np.random.choice(["小于55周岁", "不适用"])  # 绝经
        else:
            menopause = np.random.choice(["大于等于55周岁", "不适用"])  # 绝经
        if age < 30:
            live_birth = np.random.choice(["小于20周岁", "20-24", "25-29","不适用"])  # 首次分娩
        else:
            live_birth = np.random.choice(["小于20周岁", "20-24", "25-29", "大于等于30周岁", "不适用"])  # 首次分娩

        if live_birth == "不适用":
            breastfeeding = "无"  # 哺乳经历
        else:
            breastfeeding = np.random.choice(["无", "有，小于等于四个月", "有，大于4个月"])  # 哺乳经历
        
        biopsy = np.random.choice(["无", "有1次", "有多次"])  # 活检史或乳腺良性疾病手术史

        if biopsy != "无":
            no_typical = "无"  # 无典型
        else:
            no_typical = np.random.choice(["无", "有", "未知"])  # 无典型

        family_cancer = np.random.choice(["无", "有", "多个", "未知"])  # 一级亲属（母亲、姐妹、女儿）是否患有乳腺癌
        brac12 = np.random.choice(["无", "有"])  # 是否有已知的BRAC1/2基因突变
        anxiety = np.random.choice(["无", "有"])  # 焦虑
        high_calorie = np.random.choice(["无", "有"])  # 高卡路里

        data["weight"].append(weight)
        data["height"].append(height)
        data["first_tide"].append(first_tide)
        data["menopause"].append(menopause)
        data["live_birth"].append(live_birth)
        data["breastfeeding"].append(breastfeeding)
        data["biopsy"].append(biopsy)
        data["family_cancer"].append(family_cancer)
        data["brac12"].append(brac12)
        data["anxiety"].append(anxiety)
        data["high_calorie"].append(high_calorie)
        data["no_typical"].append(no_typical)
        data["age"].append(age)

    df = pd.DataFrame(data)
    df.to_excel("data.xlsx", index=False)

if __name__ == "__main__":
    generate_data()