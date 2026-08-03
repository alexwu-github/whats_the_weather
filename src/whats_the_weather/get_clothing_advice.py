import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY saknas i miljövariablerna")

client = genai.Client(api_key=api_key)


def get_clothing_advice(csv_data: str) -> str:
    try:
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
            - Om det är blåsigt, rekommendera vindtät jacka
            """,
        )
    except errors.ClientError as e:
        raise RuntimeError(f"Request not allowed: {e}") from e
    except errors.ServerError as e:
        raise RuntimeError(
            f"No response from Gemini servern, try again later: {e}"
        ) from e
    except errors.APIError as e:
        raise RuntimeError(f"Error at request: {e}") from e

    if not interaction.output_text:
        raise RuntimeError("Gemini return empty response, try again later")

    return interaction.output_text
