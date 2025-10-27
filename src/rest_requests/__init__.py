"""
Asynchronous REST compatible requests module.

Supports basic HTTP methods with JSON payloads and has proxy support.
"""

from typing import Any
from enum import Enum
import logging
import aiohttp
from aiohttp_socks import ProxyConnector

_logger = logging.getLogger(__name__)

_JSONNode = str | int | float | bool | None | dict[str, "_JSONNode"] | list["_JSONNode"]
JSON = dict[str, "_JSONNode"] | list["_JSONNode"]


class RequestMethod(Enum):
    """
    HTTP request methods.
    """

    GET = "get"
    HEAD = "head"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    OPTIONS = "options"
    PATCH = "patch"


async def _request(
    method: RequestMethod,
    url: str,
    headers: dict[str, str] | None,
    body: JSON,
    session: aiohttp.ClientSession,
    dry_run: bool = False,
) -> str | dict[str, Any]:
    """
    Raises:
        aiohttp.client_exceptions.ClientResponseError: If the response status is not successful.
    """
    headers = (headers or {}) | {
        "Content-Type": "application/json",
    }
    request_func = _resolve_method(method, session)

    _logger.debug(
        f"Sending {method.name} request to SLURM server at '{url}' with headers={headers} and body={body}."
    )

    if dry_run:
        _logger.info(
            f"Dry run enabled - not sending {method.name} request to '{url}'.\n"
            f"Request headers: {headers}\n"
            f"Request body: {body}\n"
        )
        return {}

    async with request_func(url=url, headers=headers, json=body) as response:
        if response.content_type == "application/json":
            response_body = await response.json()
        elif response.content_type.startswith("text/plain"):
            response_body = await response.text()
        else:
            raise RuntimeError(
                f"Unsupported response content type: {response.content_type}"
            )
        response.raise_for_status()
        return response_body


def _resolve_method(
        method: RequestMethod,
        session: aiohttp.ClientSession,
    ):
    match method:
        case RequestMethod.GET:
            request_func = session.get
        case RequestMethod.HEAD:
            request_func = session.head
        case RequestMethod.POST:
            request_func = session.post
        case RequestMethod.PUT:
            request_func = session.put
        case RequestMethod.DELETE:
            request_func = session.delete
        case RequestMethod.OPTIONS:
            request_func = session.options
        case RequestMethod.PATCH:
            request_func = session.patch
    return request_func


async def request(
    method: RequestMethod,
    url: str,
    headers: dict[str, str] | None = None,
    body: JSON = {},
    timeout: int = 600,
    proxy_url: str | None = None,
    dry_run: bool = False,
) -> str | JSON:
    """
    Makes an asynchronous request.

    Raises:
        aiohttp.client_exceptions.ClientResponseError: If the response status is not successful.
    """

    session_timeout = aiohttp.ClientTimeout(
        total=None, sock_connect=timeout, sock_read=timeout
    )

    optional_args = {}
    if proxy_url is not None:
        optional_args["connector"] = ProxyConnector.from_url(proxy_url)

    async with aiohttp.ClientSession(
        timeout=session_timeout, **optional_args
    ) as session:
        return await _request(
            method,
            url,
            headers,
            body,
            session,
            dry_run,
        )
