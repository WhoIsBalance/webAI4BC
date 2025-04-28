import streamlit as st
from openai import OpenAI 
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import requests


# def chat_completion(messages):

#     client = OpenAI(
#     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
#     api_key="sk-3a5dfdb8e0124cb89346e6fac8e03c40",  # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

#     completion = client.chat.completions.create(
#         model="deepseek-r1",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
#         messages=[
#             {'role': 'user', 'content': messages}
#         ]
#     )

#     return completion.choices[0].message.content


def chat_completion(messages):
    llm = ChatOllama(model="deepseek-r1:8b")
    response = llm.invoke(["human", messages])
    return response.content


# def chat_completion(messages):

#     url = "https://api.siliconflow.cn/v1/chat/completions"
#     payload = {
#         "model": "THUDM/GLM-4-9B-0414",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": messages
#             }
#             ],
#             "stream": False,
#             "max_tokens": 512,
#             "stop": None,
#             "temperature": 0.7,
#             "top_p": 0.7,
#             "top_k": 50,
#             "frequency_penalty": 0.5,
#             "n": 1,
#             "response_format": {"type": "text"},
#             "tools": [
#                 {
#                     "type": "function",
#                     "function": {
#                         "description": "AIweb",
#                         "name": "AIweb",
#                         "parameters": {},
#                         "strict": False
#                     }
#                 }
#             ]
#     }

#     headers = {
#         "Authorization": "Bearer sk-soueimxfoqedbafbvgcrldkotibblsafjexxyqcxsgbcdmlx",
#         "Content-Type": "application/json"
#     }

#     response = requests.request("POST", url, json=payload, headers=headers)

#     return response.text



if "web_state" not in st.session_state:
    st.session_state.web_state = 0  # 问卷页面

    # 问卷结果
    st.session_state.questionnaire = {
        "gender": None,  # 性别
        "age": None,  # 年龄
        "weight": None,  # 体重
        "height": None,  # 身高
        "first_tide": None,  # 初潮年龄
        "menopause": None,  # 绝经
        "live_birth": None,  # 首次分娩
        "breastfeeding": None,  # 哺乳经历
        "biopsy": None,  # 活检史或乳腺良性疾病手术史
        "family_cancer": None,  # 一级亲属（母亲、姐妹、女儿）是否患有乳腺癌
        "brac12": None,  # 是否有已知的BRAC1/2基因突变
        "anxiety": None,  # 焦虑
        "high_calorie": None# 高卡路里
    }  

    # 评估结果
    st.session_state.evaluation = {
        "content": None  # 评估内容
    }

# 链接AI
# client = OpenAI(
#     # 如果没有配置环境变量，请用百炼API Key替换：api_key="sk-xxx"
#     api_key = "sk-W0rpStc95T7JVYVwDYc29IyirjtpPPby6SozFMQr17m8KWeo",
#     base_url="https://api.suanli.cn/v1/chat/completions"
# )


if st.session_state.web_state == 0:
    st.title("乳腺健康AI风险评估")
    with st.form("my_form"):
        
        # 问卷内容
        # 性别
        gender = st.radio("1、您的性别是", ["男", "女"], index=None) == "男"
        st.session_state.questionnaire["gender"] = gender
        # if st.radio("1、您的性别是", ["男", "女"], index=None) == "男": 
        #     st.session_state.questionnaire["gender"] = 0 
        # else: 
        #     st.session_state.questionnaire["gender"] = 1

        age = st.number_input("2、您的年龄是多少", 0, 120, None)
        st.session_state.questionnaire["age"] = age

        # 体重
        weight = st.number_input("3、请输入您的体重（kg）", 0.0, 200.0, None)
        st.session_state.questionnaire["weight"] = weight

        # 身高
        height = st.number_input("4、请输入您的身高（cm）", 0.0, 250.0, None)
        st.session_state.questionnaire["height"] = height

        # 初潮年龄
        first_tide = st.radio("5、您的初潮年龄", ["小于12周岁", "大于等于12周岁"], index=None)
        st.session_state.questionnaire["first_tide"] = first_tide

        # if first_tide: 
        #     st.session_state.questionnaire["first_tide"] = 0 
        # elif first_tide != None:
        #     st.session_state.questionnaire["first_tide"] = 1

        # 绝经
        menopause = st.radio("6、您的绝经年龄", ["小于55周岁", "大于等于55周岁", "不适用"], index=None)
        st.session_state.questionnaire["menopause"] = menopause
        # if menopause == "小于55周岁":
        #     st.session_state.questionnaire["menopause"] = 0
        # elif menopause == "大于等于55周岁":
        #     st.session_state.questionnaire["menopause"] = 1
        # elif menopause != None:
        #     st.session_state.questionnaire["menopause"] = 2

        # 首次分娩
        live_birth = st.radio("7、您初次生育的年龄是", ["大于等于30周岁", "小于30周岁", "未孕未育"], index=None)
        st.session_state.questionnaire["live_birth"] = live_birth
        # if live_birth == "大于等于30周岁":
        #     st.session_state.questionnaire["live_birth"] = 0
        # elif live_birth == "小于30周岁":
        #     st.session_state.questionnaire["live_birth"] = 1
        # elif live_birth != None:
        #     st.session_state.questionnaire["live_birth"] = 2

        # 您是否有哺乳经历
        breastfeeding = st.radio("8、您是否有哺乳经历", ["无", "有，大于4个月", "有，小于等于四个月"], index=None)
        st.session_state.questionnaire["breastfeeding"] = breastfeeding
        # if breastfeeding == "无":
        #     st.session_state.questionnaire["breastfeeding"] = 0
        # elif breastfeeding == "有，大于4个月":
        #     st.session_state.questionnaire["breastfeeding"] = 1
        # elif breastfeeding!= None:
        #     st.session_state.questionnaire["breastfeeding"] = 2

        # 您是否有活检史或乳腺良性疾病手术史
        biopsy = st.radio("9、您是否有活检史或乳腺良性疾病手术史", ["无", "有"], index=None)
        st.session_state.questionnaire["biopsy"] = biopsy
        # if biopsy == "是":
        #     st.session_state.questionnaire["biopsy"] = 1
        # elif biopsy!= None:
        #     st.session_state.questionnaire["biopsy"] = 0

        # 您的一级亲属（母亲、姐妹、女儿）是否患有乳腺癌
        family_cancer = st.radio("10、您的一级亲属（母亲、姐妹、女儿）是否患有乳腺癌", ["无", "有"], index=None)
        st.session_state.questionnaire["family_cancer"] = family_cancer
        # if family_cancer == "是":
        #     st.session_state.questionnaire["family_cancer"] = 1
        # elif family_cancer!= None:
        #     st.session_state.questionnaire["family_cancer"] = 0

        # 是否有已知的BRAC1/2基因突变
        brac12 = st.radio("11、是否有已知的BRAC1/2基因突变", ["无", "有", "未知"], index=None)
        st.session_state.questionnaire["brac12"] = brac12
        # if brac12 == "是":
        #     st.session_state.questionnaire["brac12"] = 1
        # elif brac12 == "否":
        #     st.session_state.questionnaire["brac12"] = 0
        # elif brac12!= None:
        #     st.session_state.questionnaire["brac12"] = 2

        # 您是否存在焦虑、作息不规律
        anxiety = st.radio("12、您是否存在焦虑、作息不规律", ["没有", "有"], index=None)
        st.session_state.questionnaire["anxiety"] = anxiety
        # if anxiety == "是":
        #     st.session_state.questionnaire["anxiety"] = 1
        # elif anxiety!= None:
        #     st.session_state.questionnaire["anxiety"] = 0

        # 您是否长期高热量饮食或吸烟、喝酒
        high_calorie = st.radio("13、您是否长期高热量饮食或吸烟、喝酒", ["没有", "有"], index=None)
        st.session_state.questionnaire["high_calorie"] = high_calorie
        # if high_calorie == "是":
        #     st.session_state.questionnaire["high_calorie"] = 1
        # elif high_calorie!= None:
        #     st.session_state.questionnaire["high_calorie"] = 0
        

        submit_button = st.form_submit_button(label="提交")
        b = 0
        if submit_button:
            for key in st.session_state.questionnaire.keys():
                if st.session_state.questionnaire[key] is None:
                    b = 1
                    st.toast('请填写所有问题')
                    break

            if b == 0:

                # 整合结果
                result = f"一位{age}岁，身高{height}cm、体重{weight}kg的{gender}，初潮年龄{first_tide}，绝经年龄{menopause},初次生育的年龄{live_birth}，哺乳经历{breastfeeding}、\
                    {biopsy}活检史或乳腺良性疾病手术史、一级亲属（母亲、姐妹、女儿）{family_cancer}乳腺癌，{brac12}BRCA1/2基因突变，{anxiety}焦虑、{high_calorie}作息不规律，长期高热量饮食或吸烟、喝酒，请判断该女性罹患乳腺癌的风险，确切回答属于高风险或中风险或低风险"

                # 输出结果
                st.session_state.evaluation["content"] = chat_completion(result)
                st.session_state.web_state = 1
                st.rerun()



else:
    st.title("乳腺健康AI风险评估结果")
    with st.container(border=True):
        
        st.write(st.session_state.evaluation["content"])

    if st.button("重新评估"):
        
        st.session_state.web_state = 0
        st.session_state.questionnaire = {
            "age": None,  # 年龄
            "weight": None,  # 体重
            "height": None,  # 身高
            "gender": None,  # 性别
            "first_tide": None,  # 初潮年龄
            "menopause": None,  # 绝经
            "live_birth": None,  # 首次分娩
            "breastfeeding": None,  # 哺乳经历
            "biopsy": None,  # 活检史或乳腺良性疾病手术史
            "family_cancer": None,  # 一级亲属（母亲、姐妹、女儿）是否患有乳腺癌
            "brac12": None,  # 是否有已知的BRAC1/2基因突变
            "anxiety": None,  # 焦虑
            "high_calorie": None,  # 高卡路里
        }  
        st.session_state.evaluation["content"] = None
        st.rerun()