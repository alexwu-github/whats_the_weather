from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone=ZoneInfo("Europe/Stockholm"))


async def scheduled_weather_job():
    from whats_the_weather.main import main

    await main()


def start_scheduler():
    scheduler.add_job(
        scheduled_weather_job, "cron", hour=7, minute=0
    )  # Schedule the job to run every day at 7:00 AM
    scheduler.start()
