import json


def json_pretty(data: str) -> str:
    return json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)
