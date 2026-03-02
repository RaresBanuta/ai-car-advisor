import sys
import os
from urllib import response
from google import genai
from datetime import datetime

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY NOT SET. SET IN THE ENVIRONMENT VARIABLES")

client = genai.Client(api_key=api_key)

# car_model = input("What car and model you need advice for: ")
# car_part = input("What car part needs to be fixed: ")
# client_input = input("A more detailed description of the problem: ")
# final_prompt = f"Provide your opinion or repair advice on {car_part} for a {car_model}. Take into consideration that you are a fanstastic mechanic with over 20 years of experience and the inquiry of the customer is:{client_input}"


def get_server_status():
    if api_key:
        return True
    else:
        return False


def get_mechanic_advice(car_model: str, car_part: str, client_input: str, dificulty: str):

    final_prompt = f"Provide your clear opinion or repair advice on {car_part} for a {car_model}, with answer dificulty as {dificulty}. Take into consideration that you are a fanstastic mechanic with over 20 years of experience and the inquiry of the customer is:{client_input}"
    return client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=final_prompt,
        config={
            "system_instruction":
            """ Choose random the mechanic's name, introduce yourself, and be aware of the instructions in the final prompt, and also add slightly a note of originality. 
                Be clear and concise with maximum 300 words.
                Take into consideration that the customer is not a car expert, so avoid technical jargon and be as clear as possible.
                maximum 300 words, fixed length, no more, no less.Make the text well structured, with a clear introduction, body and conclusion. Avoid unnecessary details and focus on the most important information.
                You are EXCLUSIVELY a car mechanic. If you encounter non-automotive questions or problems, refuse to answer politely and encourage the user to type again.
                Also, if you need further information to provide a more accurate answer, ask the user for more details in a clear and concise manner.
            """,
            "temperature": 0.1,
            # "max_output_tokens": 300
        })


# start = datetime.now()
# response = get_mechanic_advice(car_model, car_part, client_input)
# for chunk in response:
   # print(chunk.text, end="", flush=True)
# print(end='\n')
# print(round((datetime.now()-start).total_seconds(), 2), " s")
