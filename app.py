import streamlit as st
# from openai import OpenAI 
# from langchain_ollama import ChatOllama
# from langchain_core.output_parsers import StrOutputParser
import requests
import json
import base64


        # div[data-testid="stHeading"] div[data-testid="stHeadingWithActionElements"] h1{
        #     font-size: 30 /*字体大小 */
        #     font-weight: bold; /* 字体加粗 */ 
        #     text-align: center;
        # }

        # div[data-testid="stElementContainer"] div[data-testid="stMarkdown"] div[data-testid="stMarkdownContainer"] p{
        #     font-size: 30px; /* 字体大小 */
        #     font-weight: bold; /* 字体加粗 */
        #     text-align: center;
        # }


# 注入自定义 CSS 样式
main_bg = "background3.jpg"
main_bg_ext = "jpg"
st.markdown(
    """
    <style>
        /* 调整单选按钮的字体样式 */
        div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] div[data-testid="stMarkdownContainer"] p{
            font-size: 15px; /* 字体大小 */
            font-weight: bold; /* 字体加粗 */
        }



        div[data-testid="stNumberInput"] label[data-testid="stWidgetLabel"] div[data-testid="stMarkdownContainer"] p{
            font-size: 15px; /* 字体大小 */
            font-weight: bold; /* 字体加粗 */
        }

    </style>
    """,
    unsafe_allow_html=True
)


with open(main_bg, "rb") as img_file:
    encoded_string = base64.b64encode(img_file.read()).decode()


def extract_risk(content):
    # 定义风险等级和对应的匹配字符串
    risk_levels = {
        "低风险": "低风险",
        "中风险": "中风险",
        "高风险": "高风险",
        "非常高风险": "非常高风险",
        "无风险": "无风险",
        "中等风险": "中等风险",
        "中低风险": "中低风险",
        "中高风险": "中高风险",
        "风险偏高":"高风险",
        "风险偏低":"低风险",
        "风险适中":"中风险",
        "风险较低":"低风险",
        "风险较高":"高风险",
        "风险极高":"高风险",
        "风险较低":"低风险",
        "风险一般":"中风险",
        "一般风险":"中风险",
    }

    conclusion = content.split("\n")[-1]
    for level, match_str in risk_levels.items():
        if level in conclusion:
            return match_str
    return -1



# def chat_completion(messages):
#     llm = ChatOllama(model="deepseek-r1:8b")
#     response = llm.invoke(["human", messages])
#     result = response.content.split("</think>")
#     print(result)
#     return result[-1]


def chat_completion(messages):

    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {
        "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "messages": [
            {
                "role": "user",
                "content": messages
            }
            ],
            "stream": False,
            "max_tokens": 512,
            "stop": None,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"},
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "description": "AIweb",
                        "name": "AIweb",
                        "parameters": {},
                        "strict": False
                    }
                }
            ]
    }

    headers = {
        "Authorization": "Bearer sk-soueimxfoqedbafbvgcrldkotibblsafjexxyqcxsgbcdmlx",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers).text
    response = json.loads(response)
    result = response["choices"][0]["message"]["reasoning_content"]
    result = result.replace("她", "您")


    return result



# 弹窗提醒
@st.dialog("提交成功")
def mention():
    st.write("AI分析过程可能需要1分钟左右，请勿关闭页面，耐心等待！")


if "web_state" not in st.session_state:
    st.session_state.web_state = 0  # 问卷页面

    # 问卷结果
    st.session_state.questionnaire = {
        # "gender": None,  # 性别
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
    st.session_state.evaluation["risk"] = -1  # 评估风险

# 链接AI
# client = OpenAI(
#     # 如果没有配置环境变量，请用百炼API Key替换：api_key="sk-xxx"
#     api_key = "sk-W0rpStc95T7JVYVwDYc29IyirjtpPPby6SozFMQr17m8KWeo",
#     base_url="https://api.suanli.cn/v1/chat/completions"
# )


if st.session_state.web_state == 0:
    # st.write("乳腺健康AI风险评估")
    st.markdown('<h2 style="font-size: 30px; font-weight: bold; text-align: center;">乳腺健康AI风险评估</h2>', unsafe_allow_html=True)
    
    # st.markdown(
    #     f"""
    #     <style>
    #     [data-testid="stForm"] {{
    #         background: url(data:image/{main_bg_ext};base64,{encoded_string});
    #         background-size: cover;
    #         background-position: center;
    #     }}
    #     </style
    #     """,
    #     unsafe_allow_html=True
    # )
        
    with st.form("my_form"):
        
        # 问卷内容

        age = st.number_input("1、请输入您的年龄", 0, 120, None)
        st.session_state.questionnaire["age"] = age

        # 体重
        weight = st.number_input("2、请输入您的体重（kg）", 0.0, 200.0, None)
        st.session_state.questionnaire["weight"] = weight

        # 身高
        height = st.number_input("3、请输入您的身高（cm）", 0.0, 250.0, None)
        st.session_state.questionnaire["height"] = height

        # 初潮年龄
        first_tide = st.radio("4、您的初潮年龄", ["小于12周岁", "大于等于12周岁"], index=None)
        st.session_state.questionnaire["first_tide"] = first_tide


        # 绝经
        menopause = st.radio("5、您的绝经年龄", ["小于55周岁", "大于等于55周岁", "不适用"], index=None)
        st.session_state.questionnaire["menopause"] = menopause


        # 首次分娩
        live_birth = st.radio("6、您初次生育的年龄是", ["小于30周岁", "大于等于30周岁", "不适用"], index=None)
        st.session_state.questionnaire["live_birth"] = live_birth


        # 您是否有哺乳经历
        breastfeeding = st.radio("7、您是否有哺乳经历", ["无", "有，小于等于4个月", "有，大于4个月"], index=None)
        st.session_state.questionnaire["breastfeeding"] = breastfeeding


        # 您是否有活检史或乳腺良性疾病手术史
        biopsy = st.radio("8、您是否有活检史或乳腺良性疾病手术史", ["无", "有"], index=None)
        st.session_state.questionnaire["biopsy"] = biopsy


        # 您的一级亲属（母亲、姐妹、女儿）是否患有乳腺癌
        family_cancer = st.radio("9、您的一级亲属（母亲、姐妹、女儿）是否患有乳腺癌", ["无", "有"], index=None)
        st.session_state.questionnaire["family_cancer"] = family_cancer


        # 是否有已知的BRAC1/2基因突变
        brac12 = st.radio("10、是否有已知的BRAC1/2基因突变", ["无", "有", "未知"], index=None)
        st.session_state.questionnaire["brac12"] = brac12


        # 您是否存在焦虑、作息不规律
        anxiety = st.radio("11、您是否存在焦虑、作息不规律", ["没有", "有"], index=None)
        st.session_state.questionnaire["anxiety"] = anxiety


        # 您是否长期高热量饮食或吸烟、喝酒
        high_calorie = st.radio("12、您是否长期高热量饮食或吸烟、喝酒", ["没有", "有"], index=None)
        st.session_state.questionnaire["high_calorie"] = high_calorie

        
        st.divider()
        col1, col2, col3 = st.columns([2, 3, 2])  # 调整列的宽度比例
        with col2:
            submit_button = st.form_submit_button(label="开始评估", use_container_width=True)
        b = 0
        if submit_button:
            for key in st.session_state.questionnaire.keys():
                if st.session_state.questionnaire[key] is None:
                    b = 1
                    st.toast('请填写所有问题')
                    break

            if b == 0:

                # 整合结果
                mention()
                # result = f"我是一位{age}岁，身高{height}cm、体重{weight}kg的女性，初潮年龄{first_tide}，绝经年龄{menopause},初次生育的年龄{live_birth}，哺乳经历{breastfeeding}、\
                #     {biopsy}活检史或乳腺良性疾病手术史、一级亲属（母亲、姐妹、女儿）{family_cancer}乳腺癌，{brac12}BRCA1/2基因突变，{anxiety}焦虑、{high_calorie}作息不规律，长期高热量饮食或吸烟、喝酒，请判断该女性罹患乳腺癌的风险，确切回答属于高风险或中风险或低风险。"
                result = f"我是一位{age}岁的女性，初潮年龄{first_tide},初次生育的年龄{live_birth}，\
                    {biopsy}活检史或乳腺良性疾病手术史、一级亲属（母亲、姐妹、女儿）{family_cancer}乳腺癌，请判断该女性罹患乳腺癌的风险，回答属于高风险或中风险或低风险。"

                # 输出结果
                try:
                    st.session_state.evaluation["content"] = chat_completion(result)
                except:
                    st.session_state.evaluation["content"] = "AI评估出错，请尝试重新提交"

                st.session_state.web_state = 1
                st.rerun()

    st.write("注：本乳腺健康评估问卷依据《中国女性乳腺癌筛查指南（2022年版）》针对中国女性制定，有助于您提前发现风险，可能会耽误您约1分钟的时间，最后结果由AI评估，仅供参考。")

else:
    # st.title("乳腺健康AI风险评估结果")
    st.markdown('<h2 style="font-size: 30px; font-weight: bold; text-align: center;">乳腺健康AI风险评估结果</h2>', unsafe_allow_html=True)
    with st.container(border=True):
        
        st.write(st.session_state.evaluation["content"])
        # data = dict(st.session_state.questionnaire)
        # data["result"] = st.session_state.evaluation["content"]

        # t = time.localtime()
        # current_time = time.strftime("%Y-%m-%d %H-%M-%S", t)
        # f = open(f".\\data\\{current_time}.json", "w", encoding="utf-8")
        # json.dump(data, f, ensure_ascii=False, indent=4)
        # f.close()

    col1, col2, col3 = st.columns([2, 3, 2])  # 调整列的宽度比例
    with col2:
        resubmit_button = st.button("重新评估", use_container_width=True)

    if resubmit_button:
        
        st.session_state.web_state = 0
        st.session_state.questionnaire = {
            "age": None,  # 年龄
            "weight": None,  # 体重
            "height": None,  # 身高
            # "gender": None,  # 性别
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