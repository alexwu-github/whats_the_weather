import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY saknas i miljövariablerna")

client = genai.Client(api_key=api_key)


async def get_clothing_advice(csv_data: str) -> str:
    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""
            Väderdata: {csv_data}

            - Max 10-15 meningar totalt
            - Skriv i punktform, för lättare läsning
            - Använd ENDAST Celsius för temperaturer, aldrig Fahrenheit
            - Använd 24-timmarsformat för tid (t.ex. "14:00", ALDRIG "2 PM")
            - Ange "känns som"-temperatur BARA om den skiljer sig från den faktiska temperaturen
            - Ignorera tidpunkter FÖRE kl 07:00 - de är ointressanta för dagens sammanfattning
            - "Morgon" avser tidpunkter från och med kl 07:00
            - Svara på svenska
            - Om det är risk för regn eller snö, skriv hur stort chans det är (t.ex. "50% chans för regn/snö")

            Sammanfatta dagens väder (temperatur under dagen, med morgon definierat som tidigast 07:00) och ge klädråd:
            - Lager om det är kallt på morgonen men blir varmare
            - Paraply om det regnar
            - Solglasögon/solskydd om det är soligt
            - Varm jacka/stövlar om det snöar   
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

    if not response.text:
        raise RuntimeError("Gemini return empty response, try again later")

    return response.text
