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

user_input = st.text_input("대화를 시작하세요")

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "memo" not in st.session_state:
    st.session_state.memo = []    

for role, msg, msg_type in st.session_state.chat_log:
    if msg_type == "text":
        st.write(f"{role}: {msg}")
    elif msg_type == 'image':
        st.image(msg, width=300)       

user_input = st.text_input("대화를 시작하세요",key="chat_input")


if st.button("SEND"):
    if user_input.strip():
    #USER messege
        st.session_state.chat_log.append(("You",user_input, "text"))
    #bot_messege
    reply_type, bot_reply = get_reply(user_input)
    st.session_state.chat_log.append(("Bot", bot_reply, reply_type))
    #clear the input
    st.session_state.chat_input =""


