# note: tests may use https://jsonplaceholder.typicode.com for a testing REST API

import pytest
from aiohttp import ClientResponseError

from rest_requests import RequestMethod, request


@pytest.mark.asyncio
async def test_request_get_success():

    response = await request(
        method=RequestMethod.GET,
        url="https://jsonplaceholder.typicode.com/todos/1",
    )

    assert response == {
        "userId": 1,
        "id": 1,
        "title": "delectus aut autem",
        "completed": False,
    }


@pytest.mark.asyncio
async def test_request_post_success():

    response = await request(
        method=RequestMethod.POST,
        url="https://jsonplaceholder.typicode.com/posts",
        body={"title": "foo", "body": "bar", "userId": 1},
    )

    assert response == {
        "userId": 1,
        "id": 101,
        "title": "foo",
        "body": "bar",
    }


@pytest.mark.asyncio
async def test_request_error():

    with pytest.raises(ClientResponseError) as e:
        await request(
            method=RequestMethod.GET,
            url="https://jsonplaceholder.typicode.com/doesnotexist/1",
            body={"invalid": "data"},
        )


@pytest.mark.asyncio
async def test_request_text_response():

    with pytest.raises(RuntimeError) as e:
        await request(
            method=RequestMethod.GET,
            url="https://example.com",
        )