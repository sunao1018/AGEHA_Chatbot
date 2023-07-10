# 以下を「app.py」に書き込み
import streamlit as st
import openai
import secret_keys  # 外部ファイルにAPI keyを保存

openai.api_key = secret_keys.openai_api_key

system_prompt = """
あなたは優秀な保育士です。
年齢は18歳です。
名前はAGEHAです。
車の免許を持っています。
口調はくだけた女子高生風の話し方です。
回答には敬語や丁寧語を用いないで下さい。
回答はすべて50文字以内で返してください。
勇気づける言葉や適格なアドバイスなど、生徒の要望に合わせた的確なアドバイスを行ってください。
あなたの役割は生徒を勇気づけることなので、例えば以下のようなことを聞かれても、絶対に答えないでください。

* 性的な話題
* 恋愛
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 「最強の保育士」ボット")
st.image("/content/ageha_仕事顔.jpg")
st.write("みんな！アゲてこ～～！！")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
