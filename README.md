# rest-requests

[![PyPI - Version](https://img.shields.io/pypi/v/rest-requests.svg)](https://pypi.org/project/rest-requests)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rest-requests.svg)](https://pypi.org/project/rest-requests)

-----

Asynchronous SLURM REST requests with proxy support.

## Installation

```console
pip install rest-requests
```

## Usage

```python
import asyncio

from rest_requests import request, RequestMethod


async def main():

    response = await request(
        method=RequestMethod.POST,
        url="https://jsonplaceholder.typicode.com/posts",
        # headers={"key": "value"},
        body={"title": "foo", "body": "bar", "userId": 1},
        # proxy_url="socks5://localhost:8080
    )

    assert response == {
        "userId": 1,
        "id": 101,
        "title": "foo",
        "body": "bar",
    }


if __name__ == "__main__":
    asyncio.run(main())

```

## Contributors

- [@AlexanderKlemps](https://github.com/AlexanderKlemps)
- [@Kwasniok](https://github.com/Kwasniok)

## License

`rest-requests` is distributed under the terms of the [CC-BY-SA-4.0](http://creativecommons.org/licenses/by-sa/4.0) license.
