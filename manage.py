#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import pkg_resources

DEFAULT_COLOR = "#a4a61d"
COLORS = {
    "brightgreen": "#4c1",
    "green": "#97CA00",
    "yellowgreen": "#a4a61d",
    "yellow": "#dfb317",
    "orange": "#fe7d37",
    "red": "#e05d44",
    "lightgrey": "#9f9f9f",
}

COLOR_RANGES = [
    (95, "brightgreen"),
    (90, "green"),
    (75, "yellowgreen"),
    (60, "yellow"),
    (40, "orange"),
    (0, "red"),
]


def get_color(total):
    """
    Return color for current coverage precent
    """
    try:
        xtotal = int(total)
    except ValueError:
        return COLORS["lightgrey"]
    for range_, color in COLOR_RANGES:
        if xtotal >= range_:
            return COLORS[color]


def get_badge(total, color=DEFAULT_COLOR):
    """
    Read the SVG template from the package, update total, return SVG as a
    string.
    """
    template_path = "flat.svg"
    template = pkg_resources.resource_string(__name__, template_path).decode("utf8")
    return template.replace("{{ total }}", str(int(total))).replace("{{ color }}", color)


def save_badge(badge, filepath):
    """
    Save badge to the specified path.
    """
    path = os.path.abspath(filepath)

    # Write file
    with open(path, "w", encoding="utf-8") as f:
        f.write(badge)

    return path


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fifa_manager.settings")
    try:
        command = sys.argv[1]
    except IndexError:
        command = "help"
    running_tests = command == "test"
    if running_tests:
        from coverage import Coverage

        cov = Coverage(source=["manager"], omit=["manage.py"])
        cov.erase()
        cov.start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    if running_tests:
        cov.stop()
        cov.save()
        covered = cov.report(show_missing=True)
        percentage = 95
        color = get_color(covered)
        badge = get_badge(covered, color)
        filepath = "coverage.svg"
        path = save_badge(badge, filepath)
        print(f"Saved badge to {path}")

        if covered < percentage:
            print(f"Coverage < {percentage}")
            sys.exit(1)


if __name__ == "__main__":
    main()
