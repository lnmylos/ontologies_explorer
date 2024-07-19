"""treatment of the search ouputs results."""

from utils.fhir_api import search_fhir_api


def get_implicit_valueset(codesystem: dict) -> list | None:
    """Return the implicit ValueSets availables for CodeSystem.

    Args:
    ----
        codesystem (dict): Dictionary containing the information from each CodeSystem
        available in the SMT server.

    Returns:
    -------
        list|None: List of implicit valuesets

    """
    return [
        vs["resource"]["valueSet"] for vs in codesystem["entry"] if "valueSet" in vs["resource"]
    ]


def get_code_label(result: dict) -> dict | None:
    """Obtain the label and vocabulary for a searched code.

    Args:
    ----
        result (dict): result from search_code function

    Returns:
    -------
        dict | None: a dictionary containing the code, the label and the vocabulary
        for the searched code.

    """
    code = None
    label = None
    vocabulary = None

    for parameter in result["parameter"]:
        if parameter["name"] == "code":
            code = parameter["valueCode"]

        if parameter["name"] == "display":
            label = parameter["valueString"]

        if parameter["name"] == "name":
            vocabulary = parameter["valueString"]

    return {"code": code, "label": label, "vocabulary": vocabulary}


def get_relations(token: str, result: dict) -> dict | None:
    """Get the ontological relationships or the hierarchies of a searched code.

    Args:
    ----
        token (str): connection token obtained with get_access_token
        result (dict): result from search_code function

    Returns:
    -------
        dict | None: a dictionary containing the relationships (parent and children)
        of a given code.

    """
    parents = []
    children = []
    relations = {"parents": [], "children": []}

    for parameter in result["parameter"]:
        if parameter["name"] == "system":
            url = parameter["valueUri"]

        if parameter["name"] == "property":
            if parameter["part"][0]["valueCode"] == "parent":
                parent = parameter["part"][1]["valueCode"]
                parents.append(parent)

            if parameter["part"][0]["valueCode"] == "child":
                child = parameter["part"][1]["valueCode"]
                children.append(child)

    codes = {code: [] for code in set(parents + children)}

    for code in codes:
        code_result = search_fhir_api(
            token=token,
            url=url,
            search_param="code",
            value=code,
        )
        codes[code] = get_code_label(code_result)

    relations["parents"] = [codes[parent] for parent in parents]
    relations["children"] = [codes[child] for child in children]

    return relations
