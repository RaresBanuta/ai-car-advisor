import streamlit as st
import datetime
import requests
from datetime import datetime
from mechanic import get_mechanic_advice

if "answered" not in st.session_state:
    st.session_state.answered = False

if "start" not in st.session_state:
    st.session_state.start = datetime.now()


def set_background_image(image_url):
    image_background = f"""
    <style>
        .stApp{{
        background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        [data-testid="stBottom"] {{
        background-color: transparent !important;
    }}
        [data-testid="stBottom"] > div{{
        background-color: transparent !important;
    }}
        [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    </style>
    """
    st.markdown(image_background, unsafe_allow_html=True)


set_background_image("https://wallpapercave.com/wp/wp3006091.jpg")


def thank_user(feeling):
    if feeling == "good":
        st.toast("Feedback received! Thank you!", icon="🟢", duration="short")
    else:
        st.toast("Feedback received! Thank you!", icon="🔴", duration="short")
    st.session_state.answered = False


def check_api_connection():
    try:
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            return True
        return False
    except requests.ConnectionError:
        return False


def check_vin(vin):
    endpoint = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json"
    answer = requests.get(endpoint)
    data = answer.json()
    return data["Results"]


@st.fragment(run_every=1)
def catch_time():
    now = datetime.now()
    elapsed_time = datetime.now() - st.session_state.start
    current_time = datetime.now().strftime("%H:%M:%S")
    delta = str(elapsed_time).split(".")[0]
    st.markdown(
        f"""
        <div style='text-align: center'>
            <h5>{current_time}</h5>
            <p style='font-size: 0.8em; opacity: 0.7;'>Session Duration: {delta}</p>
        </div>
        """, unsafe_allow_html=True
    )


st.markdown(
    "<h1 style='text-align: center;'>👨‍🔧 Your AI Car Advisor 🚗</h1>",
    unsafe_allow_html=True
)
if check_api_connection():
    catch_time()
    st.markdown(
        "<h5 style='text-align: center; font-size: 18px;'>Online🟢<br></h5>",
        unsafe_allow_html=True
    )

else:
    st.markdown(
        "<h5 style='text-align: center; font-size: 18px;'>Offline🔴<br></h5>",
        unsafe_allow_html=True
    )

st.markdown(
    "<h4 style='text-align: center; font-size: 27px;'><strong>&quot;Your expert in automotive diagnostics and repair guidance&quot;</strong><br></h4>",
    unsafe_allow_html=True
)

st.markdown(
    "<h5 style='text-align: left; font-size: 15px; opacity: 0.3;'>You can use this VIN for testing WA114BGF0SA023736<br></h5>",
    unsafe_allow_html=True
)

with st.popover("📄Check your VIN here!📄", type="secondary"):
    limit = 20
    VIN = st.text_input("VIN: ", label_visibility="collapsed", key="VIN")
    if st.button("CHECK", key="vin_button"):
        if VIN:
            result = check_vin(VIN)
            with st.container(border=True, height=700):
                for item in result:
                    if item["Value"] and item["Value"] != "Not Applicable":
                        st.write(
                            f"{item['Variable']} --- {item['Value']}")
                        limit -= 1
                        if limit <= 0:
                            break


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
        st.toast("Sending your inquiry to the mechanic...",
                 icon="⏳", duration="long")
        st.header(
            f" **Car: {car_model} -- Part: {car_part}**")
        st.toast(
            "INFO OK", icon="🟢", duration="short")

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

        payload = {
            "car_model": car_model,
            "car_part": car_part,
            "client_input": client_input,
            "dificulty": answer_dificulty
        }
        if not payload:
            st.toast(
                "Car Model, Car Part, and Mechanical Experience Level must be filled", icon="🚨")

        print("🔍 STREAMLIT IS SENDING THIS:", payload)

        response = get_mechanic_advice(
            car_model, car_part, client_input, answer_dificulty)
        with st.container(border=True, height="content"):
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

        def fetch_from_API():
            try:
                api_url = "http://127.0.0.1:8000/diagnosis"
                response = requests.post(
                    api_url, json=payload, stream=True, timeout=30)
                if (response.status_code == 200):
                    for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                        if chunk:
                            yield chunk
                else:
                    yield f"API Error CODE: {response.status_code}"
            except requests.exceptions.ConnectionError:
                yield "🚨 API connection Failed. Check your server connection."

        with st.chat_message("ai"):
            with st.container(border=True, height=700):
                st.write_stream(fetch_from_API())
