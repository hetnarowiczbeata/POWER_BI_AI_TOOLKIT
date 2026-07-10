"""
Public preview only.

This file shows the outer shape of the Power BI AI Toolkit workflow
without exposing the private parser, prompt logic, or TMDL editor.
"""


def scan_model(model_path):
    """Return a minimal public-safe summary placeholder."""
    return {
        "model_path": model_path,
        "tables": ["<hidden>"],
        "relationships": "<hidden>",
        "measures": "<hidden>",
    }


def suggest_next_steps(model_summary):
    """Illustrative suggestions only, not the private rule engine."""
    return [
        "Review visible fact and dimension tables.",
        "Check relationship directions and inactive relationships.",
        "Identify candidate KPI measures.",
        "Ask the user before writing any model changes.",
    ]


if __name__ == "__main__":
    summary = scan_model("<path-to-semantic-model>")
    for index, suggestion in enumerate(suggest_next_steps(summary), start=1):
        print(f"{index}. {suggestion}")
