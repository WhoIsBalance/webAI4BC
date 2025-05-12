import streamlit as st
from openai import OpenAI 
# from langchain_ollama import ChatOllama
# from langchain_core.output_parsers import StrOutputParser
# import requests
import json
import base64
import time
from streamlit_lottie import st_lottie
import re


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


# 设置页面配置
main_bg = "background3.jpg"
main_bg_ext = "jpg"

with open(main_bg, "rb") as img_file:
    encoded_string = base64.b64encode(img_file.read()).decode()


container_bg = "pink_flower.jpg"  # 替换为你的图片文件名
container_bg_ext = "jpg"
with open(container_bg, "rb") as img_file:
    container_encoded_string = base64.b64encode(img_file.read()).decode()


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

        .low-risk {
            color: green; /* 低风险为绿色 */
            font-size: 25px; 
            font-weight: bold;
        }
        .medium-risk {
            color: orange; /* 中低风险和中风险为橙色 */
            font-size: 25px; 
            font-weight: bold;
        }
        .high-risk {
            color: red; /* 中高风险和高风险为红色 */
            font-size: 25px; 
            font-weight: bold;
        }





    </style>
    """,
    unsafe_allow_html=True
)


        # .stMainBlockContainer {
        #     max-width:100rem;
        # }
        # div[data-testid="stBottomBlockContainer"] {
        #     max-width:100rem;
        # }


        # div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        #     padding-bottom: 200px;
        #     padding-top: 200px;
        #     padding-left: 100px;
        #     padding-right: 100px;
        #     margin: 0 auto;
        # }

        # div[data-testid="stVerticalBlock"] {
        #     height: 80%;
        #     width: 75%;
        #     margin: 0 auto;
        # }


        # .stMainBlockContainer {
        #     max-width:200rem;
        # }
        # div[data-testid="stBottomBlockContainer"] {
        #     max-width:200rem;
        # }



def extract_risk(content):
    # 定义风险等级和对应的匹配字符串
    risk_levels = {
        "低风险": "低风险",
        "中风险": "中风险",
        "高风险": "高风险",
        "非常高风险": "高风险",
        "无风险": "低风险",
        "中等风险": "中风险",
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
    conclusion = content.strip()
    print("\n\n\n")
    print(conclusion)

    # 定义正则表达式，匹配可能的风险等级表述
    # 排除“降低风险”“降低风险”等干扰项
    pattern = r"(?:综合风险|符合|风险等级|风险分层|风险为|属于|为|是|风险|:|：|\*\*|乳腺癌)\s*(低风险|中风险|高风险|非常高风险|无风险|中等风险|中高风险|风险偏高|风险偏低|风险适中|风险较低|风险较高|风险极高|风险较低|风险一般|一般风险)|\b(低风险|中风险|高风险|非常高风险|无风险|中等风险|中高风险|风险偏高|风险偏低|风险适中|风险较低|风险较高|风险极高|风险较低|风险一般|一般风险)\b"
    
    # 使用正则表达式查找匹配项
    matches = re.findall(pattern, conclusion)
    
    # 合并匹配结果
    risk_level_ = [match[0] or match[1] for match in matches]
    result = list(set(risk_level_))
    print(result)
    
    if len(result) == 0:
        return -1
    # 去重并返回结果
    else:
        return risk_levels[result[0]]
    

def load_lottiefile(filepath: str):
    """
    从指定文件路径加载 Lottie 动画文件。

    Lottie 是一种 JSON 格式的动画文件，常用于在网页上展示矢量动画。
    此函数会读取指定路径的 JSON 文件，并将其解析为 Python 字典。

    Args:
        filepath (str): Lottie 动画文件的路径。

    Returns:
        dict: 包含 Lottie 动画数据的 Python 字典。
    """
    with open(filepath, 'r') as f:
        return json.load(f)

lottie_rabbit = load_lottiefile(r"./image/animations/6793c5a5-0795-4193-92a3-5f3f6dd10316.json")
# def chat_completion(messages):
#     llm = ChatOllama(model="deepseek-r1:8b")
#     response = llm.invoke(["human", messages])
#     result = response.content.split("</think>")
#     print(result)
#     return result[-1]


# def chat_completion(messages):

#     url = "https://api.siliconflow.cn/v1/chat/completions"
#     payload = {
#         "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",    # deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
#         "messages": [
#             {
#                 "role": "user",
#                 "content": messages
#             }
#             ],
#             "stream": False,
#             "max_tokens": 300,
#             "stop": None,
#             "temperature": 0.3,
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

#     responses = []
#     for i in range(3):
#         response = requests.request("POST", url, json=payload, headers=headers).text
#         response = json.loads(response)
#         responses.append(response)
#         time.sleep(0.5)

#     # 遍历responses，综合投票得到最优结果，返回风险评估
#     risk_results = []
#     for response in responses:
#         reasoning_content = response["choices"][0]["message"]["reasoning_content"]
#         risk = extract_risk(reasoning_content)
#         risk_results.append(risk)
#     # 对risk_results进行投票
#     risk_counts = {}
#     for risk in risk_results:
#         if risk != -1:
#             risk_counts.update({risk: risk_counts.get(risk, 0) + 1})
        
#     # 找到出现次数最多的风险
#     if len(risk_counts) == 0:
#         return -1
#     else:
#         max_risk = max(risk_counts, key=risk_counts.get)
#         result = responses[risk_results.index(max_risk)]["choices"][0]["message"]["reasoning_content"]

#     result = result.replace("她", "您")

#     return max_risk, result



def chat_completion(messages):

    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="sk-3a5dfdb8e0124cb89346e6fac8e03c40",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )



    responses = []
    risk_results = []
    for i in range(1):

        completion = client.chat.completions.create(
            # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            model="deepseek-r1",
            messages=[
                {"role": "system", "content": "你是一名专业的乳腺外科医生。"},
                {"role": "user", "content": f"{messages}"},
            ],
            # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
            # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
            # extra_body={"enable_thinking": False},
            temperature=0.4,
            max_tokens=500,
            n=1
        )
        response = completion.choices[0].message.content

        # print(response + '\n\n\n')
        risk = extract_risk(completion.choices[0].message.content)
        responses.append(response)
        risk_results.append(risk)
        time.sleep(0.5)

        
        
    # 对risk_results进行投票
    risk_counts = {}
    for risk in risk_results:
        if risk != -1:
            risk_counts.update({risk: risk_counts.get(risk, 0) + 1})
        
    # 找到出现次数最多的风险
    if len(risk_counts) == 0:
        return -1
    else:
        max_risk = max(risk_counts, key=risk_counts.get)
        result = responses[risk_results.index(max_risk)]

    result = result.replace("她", "您")

    return max_risk, result

# 弹窗提醒
@st.dialog("提交成功")
def mention():
    st.write("AI分析过程可能需要1分钟左右，请勿关闭页面，耐心等待！")
    st_lottie(lottie_rabbit, height=70, key="rabbit")

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




with st.container(border=False):

    # 背景图片
    # st.markdown(
    #     f"""
    #     <style>

    #         div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]{{
    #             background: url(data:image/{container_bg_ext};base64,{container_encoded_string});
    #             background-size: cover;
    #             background-position: center;
    #         }}

    #     </style
    #     """,
    #     unsafe_allow_html=True
    # )


        # .stApp {{
        #     background: url(data:image/{main_bg_ext};base64,{encoded_string});
        #     background-size: cover;
        #     background-position: center;
        # }}

        # div[data-testid="{custom_container.id}"] {{
        #     background: url(data:image/{container_bg_ext};base64,{container_encoded_string});
        #     background-size: cover;
        #     background-position: center;
        # }}

    if st.session_state.web_state == 0:

        st.markdown('<h2 style="font-size: 30px; font-weight: bold; text-align: center;">乳腺健康AI风险评估</h2>', unsafe_allow_html=True)
        
            
        with st.form("my_form"):
            
            # 问卷内容
            age = st.number_input("1、请输入您的年龄（岁）", 0, 120, None)
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
                if "button_disabled" not in st.session_state:
                    st.session_state.button_disabled = False
                submit_button = st.form_submit_button(label="开始评估", use_container_width=True, type="primary", disabled=st.session_state.button_disabled)
            b = 0
            if submit_button:
                for key in st.session_state.questionnaire.keys():
                    if st.session_state.questionnaire[key] is None:
                        b = 1
                        st.session_state.button_disabled = False
                        st.toast('请填写所有问题')
                        break

                if b == 0:

                    # 点击后禁用按钮
                    st.session_state.button_disabled = True
                    st.rerun()

            if st.session_state.button_disabled:

                mention()
                result = f"我是一位{age}岁，身高{height}cm、体重{weight}kg的女性，初潮年龄{first_tide}，绝经年龄{menopause},初次生育的年龄{live_birth}，哺乳经历{breastfeeding}、\
                    {biopsy}活检史或乳腺良性疾病手术史、一级亲属（母亲、姐妹、女儿）{family_cancer}乳腺癌，{brac12}BRCA1/2基因突变，{anxiety}焦虑、作息不规律，{high_calorie}长期高热量饮食或吸烟、喝酒，请根据她的情况在最后判断该女性乳腺癌风险等级，只能回答高风险或中风险或低风险，并给出相应建议。内容精简且控制在500字以内，排版样式优美"
                # result = f"我是一位{age}岁的女性，初潮年龄{first_tide},初次生育的年龄{live_birth}，\
                #     {biopsy}活检史或乳腺良性疾病手术史、一级亲属（母亲、姐妹、女儿）{family_cancer}乳腺癌，请判断该女性罹患乳腺癌的风险，回答属于高风险或中风险或低风险。"

                # 输出结果
                try:
                    result = st.session_state.evaluation["content"] = chat_completion(result)
                    if result == -1:
                        st.session_state.evaluation["content"] = "AI小助手开小差啦，请尝试重新提交"
                    else:
                        st.session_state.evaluation["risk"] = result[0]
                        st.session_state.evaluation["content"] = result[1]
                except:
                    st.session_state.evaluation["content"] = "AI小助手开小差啦，请尝试重新提交"

                st.session_state.web_state = 1
                st.rerun()

        st.write("注：本乳腺健康评估问卷依据《中国女性乳腺癌筛查指南（2022年版）》针对中国女性制定，有助于您提前发现风险，可能会耽误您约1分钟的时间，最后结果由AI评估，仅供参考。")

    else:

        st.markdown('<h2 style="font-size: 30px; font-weight: bold; text-align: center;">乳腺健康AI风险评估</h2>', unsafe_allow_html=True)
        with st.container(border=True):
            if st.session_state.evaluation["risk"] == "高风险" or st.session_state.evaluation["risk"] == "中高风险":
                risk_context = f'<span class="high-risk">{st.session_state.evaluation["risk"]}</span>'
                st.markdown(f'<p style="font-size: 25px; font-weight: bold; height: 45px;line-height: 45px;">评估结果：您属于{risk_context}人群</p><div style="border:1px solid #CCC"></div><br>', unsafe_allow_html=True)
                st.write(st.session_state.evaluation["content"])
            elif st.session_state.evaluation["risk"] == "中风险" or st.session_state.evaluation["risk"] == "中低风险":
                risk_context = f'<span class="medium-risk">{st.session_state.evaluation["risk"]}</span>'
                st.markdown(f'<p style="font-size: 25px; font-weight: bold; height: 45px;line-height: 45px;">评估结果：您属于{risk_context}人群</p><div style="border:1px solid #CCC"></div><br>', unsafe_allow_html=True)
                st.write(st.session_state.evaluation["content"])
            elif st.session_state.evaluation["risk"] == "低风险":
                risk_context = f'<span class="low-risk">{st.session_state.evaluation["risk"]}</span>'
                st.markdown(f'<p style="font-size: 25px; font-weight: bold; height: 45px;line-height: 45px;">评估结果：您属于{risk_context}人群</p><div style="border:1px solid #CCC"></div><br>', unsafe_allow_html=True)
                st.write(st.session_state.evaluation["content"])
            else:
                st.markdown(f'<p style="font-size: 25px; font-weight: bold; height: 45px;line-height: 45px;">AI小助手开小差啦，请尝试重新提交</p><br>', unsafe_allow_html=True)
            
            

        col1, col2, col3 = st.columns([2, 3, 2])  # 调整列的宽度比例
        with col2:
            resubmit_button = st.button("重新评估", use_container_width=True, type="primary")

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
            st.session_state.evaluation["risk"] = -1
            st.session_state.button_disabled = False
            st.rerun()