import requests as requests_orig
import sys

from requests import Response
from requests import exceptions as requests_exceptions
from typing import Any


class Requests:
    # Expose the exceptions module from requests
    exceptions = requests_exceptions

    def __init__(self) -> None:
        pass

    @classmethod
    def _generate_curl_command(
            cls,
            method: str,
            url: str,
            headers: dict[str, str] | None = None,
            data: dict[str, Any] | str | None = None,
            params: dict[str, str] | None = None
    ) -> str:
        curl_cmd = f"curl -X {method.upper()} '{url}'"

        # Add headers to the curl command
        if headers:
            for key, value in headers.items():
                curl_cmd += f" -H '{key}: {value}'"

        # Add params to the curl command (for GET requests)
        if params:
            param_str = '&'.join([f"{k}={v}" for k, v in params.items()])
            curl_cmd += f" -G --data '{param_str}'"

        # Add payload/body to the curl command (for POST/PUT requests)
        if data:
            curl_cmd += f" --data '{data}'"

        return curl_cmd

    @classmethod
    def request(
            cls,
            method: str,
            url: str,
            *,
            headers: dict[str, str] | None = None,
            data: dict[str, Any] | str | None = None,
            params: dict[str, str] | None = None,
            debug: bool = False,
            **kwargs: Any
    ) -> Response:
        if debug:
            curl_cmd = cls._generate_curl_command(method, url, headers, data, params)
            print("Equivalent curl command:")
            print(curl_cmd)
            sys.exit(1)  # Exit without making the request

        # Make the actual request
        return requests_orig.request(method, url, headers=headers, data=data, params=params, **kwargs)

    @classmethod
    def get(
            cls,
            url: str,
            *,
            headers: dict[str, str] | None = None,
            params: dict[str, str] | None = None,
            debug: bool = False,
            **kwargs: Any
    ) -> Response:
        return cls.request("GET", url, headers=headers, params=params, debug=debug, **kwargs)

    @classmethod
    def post(
            cls,
            url: str,
            *,
            headers: dict[str, str] | None = None,
            data: dict[str, Any] | str | None = None,
            debug: bool = False,
            **kwargs: Any
    ) -> Response:
        return cls.request("POST", url, headers=headers, data=data, debug=debug, **kwargs)

    @classmethod
    def put(
            cls,
            url: str,
            *,
            headers: dict[str, str] | None = None,
            data: dict[str, Any] | str | None = None,
            debug: bool = False,
            **kwargs: Any
    ) -> Response:
        return cls.request("PUT", url, headers=headers, data=data, debug=debug, **kwargs)

    @classmethod
    def delete(
            cls,
            url: str,
            *,
            headers: dict[str, str] | None = None,
            data: dict[str, Any] | str | None = None,
            debug: bool = False,
            **kwargs: Any
    ) -> Response:
        return cls.request("DELETE", url, headers=headers, data=data, debug=debug, **kwargs)
