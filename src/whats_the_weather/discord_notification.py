import httpx

async def send_to_discord(discord_webhook_url: str, message: str):
    if not discord_webhook_url:
        raise ValueError("Webhook URL is not set")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(discord_webhook_url, json={"content": message})
            response.raise_for_status()
            return
        
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred while sending message to Discord: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"An error occurred while sending message to Discord: {e}")
