"""
Public preview of the Power BI AI Toolkit workflow.

This module intentionally exposes only the safe outer logic:
- building example measure suggestions,
- parsing a user's numeric selection,
- adding required dependent measures,
- rendering a read-only TMDL preview.

The private repository keeps the production TMDL scanner, prompt templates,
local LLM client, validation rules, and write-to-file logic.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MeasureOperation:
    name: str
    expression: str
    format_string: str = "0"
    display_folder: str = "AI Suggestions"


@dataclass(frozen=True)
class Suggestion:
    title: str
    reason: str
    operation: MeasureOperation
    risk: str = "low"
    requires: tuple[str, ...] = field(default_factory=tuple)


def time_intelligence_suggestions():
    """Return a small public-safe sample of generated suggestions."""
    folder = "AI Suggestions\\Time Intelligence"

    return [
        Suggestion(
            title="Add Orders PY",
            reason="Orders in the same period of the previous year.",
            operation=MeasureOperation(
                name="Orders PY",
                expression="CALCULATE([Orders], SAMEPERIODLASTYEAR('dim_calendar'[Date]))",
                format_string="#,0",
                display_folder=folder,
            ),
        ),
        Suggestion(
            title="Add Orders YTD",
            reason="Cumulative orders from the beginning of the year.",
            operation=MeasureOperation(
                name="Orders YTD",
                expression="TOTALYTD([Orders], 'dim_calendar'[Date])",
                format_string="#,0",
                display_folder=folder,
            ),
        ),
        Suggestion(
            title="Add Orders YoY",
            reason="Difference between current orders and previous-year orders.",
            operation=MeasureOperation(
                name="Orders YoY",
                expression="[Orders] - [Orders PY]",
                format_string="#,0",
                display_folder=folder,
            ),
            requires=("Orders PY",),
        ),
        Suggestion(
            title="Add Orders YoY %",
            reason="Year-over-year order growth rate.",
            operation=MeasureOperation(
                name="Orders YoY %",
                expression="DIVIDE([Orders YoY], [Orders PY], 0)",
                format_string="0.0%;-0.0%;0.0%",
                display_folder=folder,
            ),
            requires=("Orders YoY", "Orders PY"),
        ),
    ]


def parse_selection(text, suggestion_count):
    """Parse input like '1,3', '2-4' or 'all' into suggestion numbers."""
    cleaned = text.strip().lower()

    if cleaned in {"", "no", "n", "nie"}:
        return []

    if cleaned in {"all", "wszystkie"}:
        return list(range(1, suggestion_count + 1))

    selected = []
    for part in cleaned.replace(";", ",").split(","):
        part = part.strip()

        if not part:
            continue

        if "-" in part:
            start, _, end = part.partition("-")
            if start.isdigit() and end.isdigit():
                for number in range(int(start), int(end) + 1):
                    if 1 <= number <= suggestion_count and number not in selected:
                        selected.append(number)
            continue

        if part.isdigit():
            number = int(part)
            if 1 <= number <= suggestion_count and number not in selected:
                selected.append(number)

    return selected


def expand_selection_with_dependencies(suggestions, selected_numbers):
    """
    Add required suggestions before applying a user's selection.

    Example:
    selecting only "Orders YoY %" also selects "Orders YoY" and "Orders PY",
    because the percentage measure references both of them.
    """
    selected = set(selected_numbers)
    added = []
    name_to_number = {
        suggestion.operation.name.lower(): index
        for index, suggestion in enumerate(suggestions, start=1)
    }

    changed = True
    while changed:
        changed = False

        for number in list(selected):
            suggestion = suggestions[number - 1]

            for required_name in suggestion.requires:
                required_number = name_to_number.get(required_name.lower())

                if not required_number or required_number in selected:
                    continue

                selected.add(required_number)
                added.append(required_number)
                changed = True

    expanded = [
        number
        for number in range(1, len(suggestions) + 1)
        if number in selected
    ]
    added = [number for number in expanded if number in set(added)]

    return expanded, added


def render_measure_preview(operation):
    """Render a TMDL measure block for preview only."""
    name = operation.name
    measure_name = name if name.replace("_", "").isalnum() and " " not in name else f"'{name}'"

    lines = [
        f"\tmeasure {measure_name} = {operation.expression}",
        f"\t\tformatString: {operation.format_string}",
        f"\t\tdisplayFolder: {operation.display_folder}",
    ]

    return "\n".join(lines)


def print_suggestions(suggestions):
    for index, suggestion in enumerate(suggestions, start=1):
        print(f"[{index}] {suggestion.title}")
        print(f"    Risk: {suggestion.risk}")
        print(f"    {suggestion.reason}")

        if suggestion.requires:
            print(f"    Requires: {', '.join(suggestion.requires)}")


def demo(selection_text="4"):
    suggestions = time_intelligence_suggestions()

    print("PUBLIC PREVIEW: Power BI AI Toolkit")
    print()
    print_suggestions(suggestions)

    selected = parse_selection(selection_text, len(suggestions))
    selected, added = expand_selection_with_dependencies(suggestions, selected)

    print()
    print(f"User selected: {selection_text}")

    if added:
        print("Automatically added dependencies:")
        for number in added:
            print(f"- [{number}] {suggestions[number - 1].title}")

    print()
    print("TMDL preview:")
    for number in selected:
        operation = suggestions[number - 1].operation
        print(render_measure_preview(operation))
        print()


if __name__ == "__main__":
    demo()
