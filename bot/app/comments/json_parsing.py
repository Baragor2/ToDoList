import textwrap

from httpx import Response


async def parse_get_comments_json(response: Response):
    try:
        comments_json = response.json()
        comments_message = ""
        for ind, comment in enumerate(comments_json[1]):
            comments_message += textwrap.dedent(
                f"""
                Комментарий {ind + 1}
                Текст: {comment.get("text")}
                Дата создания: {comment.get("creation_date")}
                ================""")
        return comments_message
    except KeyError:
        return response.json().get("detail")
