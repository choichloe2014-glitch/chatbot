import streamlit as st
import random
import time

st.set_page_config(page_title="ChatBot")

st.title("Chat")

def get_reply(messege):
    messege = messege.lower()

    if "안녕" in messege or "hello" in messege:
        return ("text", "안녕")
    elif "오늘 뭐 먹지" in messege:
        return ("text", get_random_food())
    elif messege.startswith("메모:"):
        memo = messege[3:].strip()
        return ("text", save_memo(memo))
    elif "메모 보여줘" in messege:
        return ("text", get_memo())
    elif "메모 삭제해" in messege:
        return ("text", delete_all_memo())
    elif "고양이 사진 보내줘" in messege:
        return ("image", get_cat_image_url())
    else:
        return ("text", "아직 무슨 말인지 모르겠어.")
    
def get_random_food():
    foods = ["떡볶이", "돈까스", "칼국수", "비빔밥", "탕수육", "닭갈비", "초밥", "라면", "불고기", "파스타", "김치찌개"]   
    return random.choice(foods)

def save_memo(message):
    st.session_state.memo.append(message)
    return f"메모 저장해둘게: {message}"

def get_memo():
    if len(st.session_state.memo) == 0:
        return "아직 저장된 메모가 없어."
    else:
        return "저장된 메모:" + ",".join(st.session_state.memo) 
    
def delete_all_memo():
    st.session_state.memo = []
    return "전체 메모를 삭제했어."

def get_cat_image_url():
    return f"https://cataas.com/cat?time={time.time()}"  

#세션 메시지 저장공간
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "memo" not in st.session_state:
    st.session_state.memo = []

for msg in st.session_state.chat_log:
    with st.chat_message(msg["role"]):
        if msg.get("image"):
            st.image(msg["image"])
        else:
            st.write(msg["content"])

#chat_input
user_msg = st.chat_input("메시지를 입력하세요.")   

if user_msg:
    with st.chat_message("user"):
        st.write(user_msg)
    st.session_state.chat_log.append({"role":"user","type":"text","content": user_msg})

    #bot reply
    reply_type, reply_msg = get_reply(user_msg)

    if reply_type == "image":
        with st.chat_message("assistant"):
            st.image(reply_msg)
        st.session_state.chat_log.append({"role":"assistant", "type": "image", "image": reply_msg})
    else:
        with st.chat_message("assistant"):
            st.write(reply_msg)
        st.session_state.chat_log.append({"role": "assistant", "type": "text", "content": reply_msg})            


