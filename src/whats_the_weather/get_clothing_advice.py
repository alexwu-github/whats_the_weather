from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_clothing_advice(csv_data: str) -> str:
    #with open("src/whats_the_weather/weather.csv", "r") as f:
        #csv_data = f.read()
    
    interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=f"""
    Väderdata: {csv_data}

    - Använd ENDAST Celsius för temperaturer, aldrig Fahrenheit
    - Använd 24-timmarsformat för tid (t.ex. "14:00", ALDRIG "2 PM")
    - Ange temperaturen tillsammans med "känns som"-temperaturen (feels_like) om den skiljer sig från den faktiska temperaturen
    - Svara på svenska

    Ge en sammanfattning av dagens väder, inklusive:
    - Temperatur (och "känns som"-temperatur om relevant) under dagen
    - Om det är kallt på morgonen men blir varmare senare, rekommendera lager-klädsel
    - Om det regnar, rekommendera paraply
    - Om det är soligt, rekommendera solglasögon och solskydd
    - Om det snöar, rekommendera varm jacka och stövlar
    """,
)   
    print(interaction.output_text)
    return interaction.output_text
    