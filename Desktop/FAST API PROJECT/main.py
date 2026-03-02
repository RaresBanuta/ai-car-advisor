from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, RedirectResponse
from mechanic import get_mechanic_advice

app = FastAPI()


class Inquiry_Car(BaseModel):
    car_model: str
    car_part: str
    client_input: str
    dificulty: str


@app.get('/diagnosis')
def read_root():
    data = """
    <html>
        <body>
            <h1>Welcome to the Car Mechanic's Advice. The system is ONLINE</h1>
            <h2>To get information from the mechanic, POST a request to <code>/</code></h2>
        </body>
    </html>
    """
    return Response(content=data, media_type="text/html")


@app.get('/')
async def diagnosis():
    streamlit_url = "http://localhost:8501"
    return RedirectResponse(url=streamlit_url)
