import streamlit as st
import uuid

st.title("ChatBot")

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"

# チャットログを保存したセッション情報を初期化
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.chats[st.session_state.current_chat_id] = []

def create_new_chat():
    new_chat_id = str(uuid.uuid4())
    st.session_state.chats[new_chat_id] = []
    st.session_state.current_chat_id = new_chat_id

# サイドバー
with st.sidebar:
    if st.button("新しいチャット"):
        create_new_chat()
    st.write("チャット履歴:")
    for chat_id, messages in st.session_state.chats.items():
        if messages:
            button_label = "チャット"
        else:
            button_label = "空のチャット"
        if st.button(button_label, key=f"chat_button_{chat_id}"):
            st.session_state.current_chat_id = chat_id
            st.rerun()

# メインチャット領域
current_chat = st.session_state.chats[st.session_state.current_chat_id]

for message in current_chat:
    with st.chat_message(message["name"]):
        st.markdown(message["msg"])

user_msg = st.chat_input("ここにメッセージを入力")
if user_msg:
    # ユーザーメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # アシスタントの応答（ここではエコーバック）
    assistant_msg = user_msg
    with st.chat_message(ASSISTANT_NAME):
        st.write(assistant_msg)

    # 現在のチャットにメッセージを追加
    current_chat.append({"name": USER_NAME, "msg": user_msg})
    current_chat.append({"name": ASSISTANT_NAME, "msg": assistant_msg})

    # セッション状態を更新
    st.session_state.chats[st.session_state.current_chat_id] = current_chat

    # 再描画
    st.rerun()
