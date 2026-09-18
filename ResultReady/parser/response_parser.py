import json
import re
from typing import TypeVar

from pydantic import BaseModel, ValidationError


ModelType = TypeVar("ModelType", bound=BaseModel)


def remove_markdown_fences(text: str) -> str:
    cleaned = text.strip()

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\s*```$", "", cleaned)

    return cleaned.strip()


def extract_first_json_object(text: str) -> str:
    cleaned = remove_markdown_fences(text)

    start = cleaned.find("{")

    if start == -1:
        raise ValueError(
            "The model response did not contain a JSON object."
        )

    depth = 0
    inside_string = False
    escaped = False

    for index in range(start, len(cleaned)):
        character = cleaned[index]

        if escaped:
            escaped = False
            continue

        if character == "\\" and inside_string:
            escaped = True
            continue

        if character == '"':
            inside_string = not inside_string
            continue

        if inside_string:
            continue

        if character == "{":
            depth += 1
        elif character == "}":
            depth -= 1

            if depth == 0:
                return cleaned[start:index + 1]

    raise ValueError(
        "The model response contained incomplete JSON."
    )


def parse_model_response(
    text: str,
    model_class: type[ModelType],
) -> ModelType:
    json_text = extract_first_json_object(text)

    try:
        data = json.loads(json_text)
        return model_class.model_validate(data)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"The model returned invalid JSON: {exc}"
        ) from exc
    except ValidationError as exc:
        raise ValueError(
            f"The model response did not match the schema: {exc}"
        ) from exc