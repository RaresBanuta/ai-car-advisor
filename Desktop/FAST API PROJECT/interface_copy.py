import streamlit as st
from mechanic import get_mechanic_advice
from mechanic import get_server_status
import time

if "answered" not in st.session_state:
    st.session_state.answered = False


def thank_user(feeling):
    if feeling == "good":
        st.toast("Feedback received! Thank you!", icon="🟢")
    else:
        st.toast("Feedback received! Thank you!", icon="🔴")
    st.session_state.answered = False


st.markdown(
    "<h1 style='text-align: center;'>👨‍🔧 Your AI Car Advisor 🚗</h1>",
    unsafe_allow_html=True
)

if get_server_status():
    st.markdown(
        "<h5 style='text-align: center; font-size: 18px;'>Online🟢<br></h5>",
        unsafe_allow_html=True
    )
else:
    st.error("System Offline", icon="🔴", width=130)

st.markdown(
    "<h4 style='text-align: center;'><strong>&quot;Your expert in automotive diagnostics and repair guidance&quot;</strong><br></h4>",
    unsafe_allow_html=True
)

st.subheader("Maker and Model:")
car_model = st.text_input(
    "Maker and Model: ", key="car_model", label_visibility="collapsed")
st.subheader("Car Part:")
car_part = st.text_input("Car Part: ", key="car_part",
                         label_visibility="collapsed")
st.subheader("Mechanical Experience Level:")
answer_dificulty = st.selectbox(
    "Mechanical Experience Level:", ("Beginner", "Medium", "Advanced"), key="answer_dificulty", label_visibility="collapsed")

if client_input := st.chat_input("Problem description: ", key="client_input"):

    st.session_state.answered = True
    if (car_model and car_part):
        st.subheader(
            f" **CAR: {car_model} -- PART: {car_part}**")
        st.toast(
            "Integrity of the information is OK", icon="🟢")

        with st.chat_message("ai"):
            st.markdown(f"""
        <div style="
            background-color: #2e3136; 
            padding: 14px; 
            margin: 5px 0;
            border-radius: 15px; 
            border-left: 5px solid #00d4ff;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        ">
            <strong style="color: #00d4ff;">🔧 Problem Reported:</strong><br>
            {client_input}
        </div>
    """, unsafe_allow_html=True)

        response = get_mechanic_advice(
            car_model, car_part, client_input, answer_dificulty)
        with st.container(border=True, height=700):
            st.write_stream(
                chunk.text for chunk in response)

    if st.session_state.answered:
        st.write("Was this advice helpful?")
        answer1, answer2 = st.columns([1, 5])
        with answer1:
            st.button("Yes", on_click=thank_user, args=["good"])
        with answer2:
            st.button("No", on_click=thank_user, args=["bad"])

    else:
        st.toast(
            "Car Model, Car Part, and Mechanical Experience Level must be filled", icon="🚨")
