import textwrap

from httpx import Response


async def parse_get_tasks_json(response: Response):
    tasks_json = response.json()
    tasks_message = ""
    for ind, task in enumerate(tasks_json):
        tasks_message += textwrap.dedent(
            f"""
            Задача {ind + 1}
            Название: {task.get("title")}
            Описание: {task.get("description")}
            Дата начала: {task.get("start_date")}
            Дата конца: {task.get("end_date")}
            Категория: {task.get("category_title")}
            ================""")
    return tasks_message
