#!/usr/bin/env python3
"""
README.md Linter and Validator for Awesome Quantum Machine Learning.
Verifies section structure, entry formatting, alphabetical ordering, and sentence punctuation.
"""

import re
import sys
from pathlib import Path

EXPECTED_CATEGORIES = [
    "Frameworks",
    "Libraries",
    "Books",
    "Courses",
    "Tutorials",
    "Research Papers",
    "Tools",
    "Simulators",
    "Platforms",
    "Cloud Providers",
    "Datasets",
    "Communities",
]

METADATA_SECTIONS = [
    "Contents",
    "Contributing",
    "License",
]


def validate_readme(file_path: Path) -> bool:
    if not file_path.exists():
        print(f"Error: {file_path} does not exist.")
        return False

    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    errors = []
    current_category = None
    found_categories = []
    category_items = {}

    # Regular expression for matching standard entry format:
    # - [Item Name](https://url) - Description ending with a period.
    item_pattern = re.compile(r"^-\s+\[([^\]]+)\]\(([^)]+)\)\s+-\s+(.+)$")

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()

        if stripped.startswith("## "):
            category_title = stripped[3:].strip()
            # Ignore standard non-resource metadata sections
            if category_title not in METADATA_SECTIONS:
                if category_title not in EXPECTED_CATEGORIES:
                    errors.append(
                        f"Line {line_num}: Unexpected category '{category_title}'. Expected one of {EXPECTED_CATEGORIES}."
                    )
                current_category = category_title
                found_categories.append(current_category)
                category_items[current_category] = []
            else:
                current_category = None
            continue

        if stripped.startswith("### "):
            current_category = None
            continue

        if stripped.startswith("- ") and current_category:
            match = item_pattern.match(stripped)
            if not match:
                errors.append(
                    f"Line {line_num} in section '{current_category}': Does not follow format '- [Name](URL) - Description.'.\n  Got: {line}"
                )
                continue

            name, url, description = match.groups()

            # Check if URL starts with http:// or https:// or relative anchor
            if not (url.startswith("http://") or url.startswith("https://") or url.startswith("LICENSE") or url.startswith("#")):
                errors.append(
                    f"Line {line_num} in section '{current_category}': URL for '{name}' should be a valid URL (got '{url}')."
                )

            # Check if description ends with a period
            if not description.endswith("."):
                errors.append(
                    f"Line {line_num} in section '{current_category}': Description for '{name}' must end with a period ('.').\n  Got: '{description}'"
                )

            category_items[current_category].append((name, line_num))

    # Verify that all expected categories are present
    missing_categories = [cat for cat in EXPECTED_CATEGORIES if cat not in found_categories]
    if missing_categories:
        errors.append(f"Missing expected categories: {missing_categories}")

    # Check alphabetical ordering within each category
    for category, items in category_items.items():
        if not items:
            continue

        names = [item[0] for item in items]
        sorted_names = sorted(names, key=lambda s: s.casefold())

        for idx, (name, line_num) in enumerate(items):
            if names[idx] != sorted_names[idx]:
                expected = sorted_names[idx]
                errors.append(
                    f"Alphabetical Order Error in section '{category}' around line {line_num}:\n"
                    f"  Found '{name}', but expected '{expected}' when sorted alphabetically."
                )
                break

    if errors:
        print(f"[ERROR] Validation failed for {file_path.name} with {len(errors)} error(s):\n")
        for err in errors:
            print(f"- {err}")
        return False

    print(f"[OK] {file_path.name} validation passed successfully! All entries follow formatting and alphabetical order.")
    return True


if __name__ == "__main__":
    repo_root = Path(__file__).parent.parent
    readme_path = repo_root / "README.md"
    success = validate_readme(readme_path)
    if not success:
        sys.exit(1)
    sys.exit(0)
