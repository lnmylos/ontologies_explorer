"""HAPI FHIR queries."""

from pathlib import Path
from typing import Any

import yaml

from utils import query_api

config_path = Path("..", "config", "settings.yml")


def load_config(config_file_path: Path) -> dict:
    """Load configuration file."""
    with Path(config_file_path).open(encoding="utf-8") as yaml_file:
        return yaml.safe_load(yaml_file)


def build_url(config_data: dict, endpoint: str, **kwargs: dict[str, Any]) -> str:
    """Dynamically build the search query URL.

    This function constructs a URL based on the provided configuration
    data, endpoint, and additional keyword arguments.
    It supports dynamic URL building by formatting the endpoint with
    optional parameters such as 'url', 'term', and 'code'.

    Args:
    ----
        config_data (dict): Loaded configuration containing the base URL & endpoint definitions.
        endpoint (str): The endpoint key from the configuration data to build the URL for.
        **kwargs (dict[str, Any]): Additional keyword arguments to customize the URL.
            - url (str, optional): The base URL to be used in formatting.
            - term (str, optional): A term to be included in the URL if specified.
            - code (str, optional): A code to be included in the URL if specified.

    Returns:
    -------
        url (str): The constructed URL based on the input parameters and configuration data.

    """
    url = kwargs.get("url", None)
    term = kwargs.get("term", None)
    code = kwargs.get("code", None)

    url_base = str(config_data["fhir_api_base"])

    if term:
        kwargs["term"] = url_endpoint = str(
            config_data["endpoints"].get(endpoint),
        ).format(url, term)

    elif code:
        kwargs["code"] = url_endpoint = str(
            config_data["endpoints"].get(endpoint),
        ).format(url, code)

    else:
        url_endpoint = str(config_data["endpoints"].get(endpoint))

    return f"{url_base}{url_endpoint}"


def get_value_sets(token: str, endpoint: str) -> dict | None:
    """Retrieve the available Value Sets or Code Systems from the SMT server.

    Args:
    ----
        token (str): Connection token obtained with get_access_token.
        endpoint (str): The endpoint key from the configuration data to build the URL for.

    Returns:
    -------
        Bundle (dict | None): FHIR Bundle resource containing the available Value Sets
        (https://build.fhir.org/bundle.html). Returns None if the request fails.

    """
    config_data = load_config(config_file_path=config_path)
    query_vs = build_url(config_data, endpoint=endpoint)
    headers = {"Authorization": f"{token}", "Content-Type": "application/json+fhir"}
    return query_api(url=query_vs, headers=headers)


def search_fhir_api(token: str, url: str, search_param: str, value: str) -> dict | None:
    """Search for a specified parameter (term or code) value in the given FHIR ValueSet.

    Args:
    ----
        token (str): Connection token obtained with get_access_token.
        url (str):  implicit value set to be searched
        search_param (str): Parameter to be searched: term or code.
        value (str): Value corresponding to the search parameter, the term or the code.

    Returns:
    -------
        dict | None: FHIR Bundle resource containing the result of the search
        (https://build.fhir.org/bundle.html) or None.

    """
    # Determine the endpoint based on the search parameter
    if search_param == "term":
        endpoint = "search_term"
    elif search_param == "code":
        endpoint = "search_code"
    else:
        msg = "Invalid search parameter. Supported parameters are 'term' and 'code'."
        raise ValueError(msg)

    # Load configuration data and build the query URL
    config_data = load_config(config_file_path=config_path)
    query_vs = build_url(config_data, endpoint, url=url, **{search_param: value})

    # Set headers and query the API
    headers = {"Authorization": f"{token}", "Content-Type": "application/json+fhir"}
    return query_api(url=query_vs, headers=headers)
