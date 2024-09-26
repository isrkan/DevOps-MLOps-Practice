#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expenses_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    args = sys.argv
    if 'runserver' in args:
        default_port = '8003'
        if len(args) == 2:
            args.append(default_port)
        elif len(args) == 3 and args[2].isdigit():
            args[2] = default_port
        else:
            args.insert(2, default_port)
    execute_from_command_line(args)


if __name__ == "__main__":
    main()
