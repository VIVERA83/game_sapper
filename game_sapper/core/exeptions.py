import json
import traceback
from typing import TYPE_CHECKING

from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity

from sqlalchemy.exc import IntegrityError

from core.utils import error_json_response

if TYPE_CHECKING:
    from core.componets import Request


async def error_handler(error: Exception, request: "Request"):
    # Наступает где-то при обращении к БД
    if isinstance(error, IntegrityError):
        error_response = error_json_response(
            http_status=HTTPUnprocessableEntity.status_code,
            message=HTTPUnprocessableEntity().reason,
            data=handler_integrity_error(error),
        )
    elif isinstance(error, HTTPUnprocessableEntity):
        error_response = error_json_response(
            http_status=error.status_code,
            message=error.reason,
            data=json.loads(error.body),
        )
    # Наступает если ошибка инициализирована где-то во views
    elif isinstance(error, HTTPException):
        error_response = error_json_response(
            http_status=error.status_code,
            status=error.reason,
            message=error.text,
        )
    # Возможно наступление если где-то
    else:
        error_response = error_json_response(
            http_status=500,
            message="Internal Server Error",
        )

    request.app.logger.warning(traceback.format_exc() if request.app.settings.traceback else error)
    return error_response


def handler_integrity_error(error: IntegrityError) -> dict:
    word_0, _, word_2 = error.args[0].partition("=")
    k1, k2, key = word_0.partition("Key")
    key = key[2:-1]
    value = word_2.partition(")")[0][1:]
    if error.orig.pgcode == "23503":  # noqa
        return {"message": error.args[0].partition("DETAIL: ")[-1]}
    else:
        return {
            key: [
                f"The parameter with the value `{value}` does not meet the uniqueness condition"
            ]
        }
