import json
import os
import sys

import click
from flask import Flask
from flask.cli import AppGroup

from definitions import ROOT_DIR
from utils.utils import get_section_data, get_all_sections

app = Flask(__name__)
user_cli = AppGroup("resume")

file_path = os.environ.get("RELATIVE_FILE_PATH", None)
if file_path is None:
    raise EnvironmentError("Missing RELATIVE_FILE_PATH in .env file.")


@user_cli.command("read")
@click.argument(
    "section",
    type=click.Choice(
        [
            "All",
            "About",
            "Contact",
            "Education",
            "Experience",
            "Skills",
            "Projects",
            "Languages",
        ]
    ),
)
def read_resume(section):
    cv_path = os.path.join(str(ROOT_DIR), file_path)
    if not os.path.exists(cv_path):
        raise click.ClickException(
            "File path does not exist. Please fix the path in the .env file"
        )

    try:
        with open(cv_path, "r", encoding="utf-8") as file:
            content = file.read()
    except EnvironmentError as error:
        click.echo(error, err=True)
        sys.exit(1)

    if section == "All":
        result = get_all_sections(content)
    else:
        result = get_section_data(section, content)

    print(json.dumps(result, indent=4))


app.cli.add_command(user_cli)

if __name__ == "__main__":
    try:
        app.run()
    except click.ClickException as error:
        click.echo(str(error), err=True)
        sys.exit(1)
