import streamlit as st
import requests

st.set_page_config(page_title="Enterprise AI Assistant", layout="centered")

st.title("🤖 Enterprise Knowledge & Operations Assistant")
st.write("اسأل عن سياسات الشركة، المستندات، أو استعلم عن بيانات الشكاوى والموظفين.")

# حفظ سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق إدخال رسالة المستخدم
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("الـ Agent يفكر ويستعلم عن الأدوات المناسبة..."):
            try:
                # إرسال الطلب لـ FastAPI Backend
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"question": prompt}
                )
                if response.status_code == 200:
                    answer = response.json().get("answer")
                else:
                    answer = "عذراً، حدث خطأ في الاتصال بالخادم."
            except Exception as e:
                answer = f"فشل الاتصال بالـ Backend: {str(e)}"
            
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})