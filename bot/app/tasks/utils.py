from datetime import datetime


async def check_time_form(datetime_message: str) -> datetime | None:
    try:
        return datetime.strptime(datetime_message, "%Y-%m-%d %H:%M")
    except ValueError:
        return None
