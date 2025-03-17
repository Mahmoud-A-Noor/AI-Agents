import re
from dataclasses import dataclass


@dataclass
class TagContentResult:
    content: list[str]
    found: bool


def extract_tag_content(text: str, tag: str) -> TagContentResult:
    # Build the regex pattern dynamically to find multiple occurrences of the tag
    tag_pattern = rf"<{tag}>(.*?)</{tag}>"

    # Use findall to capture all content between the specified tag
    matched_contents = re.findall(tag_pattern, text, re.DOTALL)

    # Return the dataclass instance with the result
    return TagContentResult(
        content=[content.strip() for content in matched_contents],
        found=bool(matched_contents),
    )