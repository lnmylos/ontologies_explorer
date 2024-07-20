"""utils functions."""

import json
import os
from pathlib import Path
from typing import Any

import requests


def load_json_file(path: str | os.PathLike) -> dict[str, Any]:
    """Load and parse a JSON file from the specified path."""
    with Path(path).open(encoding="utf-8") as file_:
        return json.load(file_)


def query_api(url: str, headers: dict, timeout: int = 20) -> dict | None:
    """Query API function.

    This function sends a GET request to the specified URL with the provided headers and timeout.
    It returns the result as a dictionary if successful or None if an error occurs.

    Args:
    ----
        url (str): The query endpoint.
        headers (dict): Headers including the authorization token and content type specification.
        timeout (int, optional): The request timeout in seconds. Defaults to 20 seconds.

    Returns:
    -------
        dict | None: The result of the query as a dictionary if successful, or None if error occurs.

    """
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error_:
        print("Error:", error_)
        return None
