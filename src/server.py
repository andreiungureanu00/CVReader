"""Main server module to provide the JSON REST API"""

import os

from dotenv import load_dotenv
from flask import Flask, abort
from flask_restx import Api, Resource

from definitions import ROOT_DIR
from utils.utils import get_section_data, get_all_sections

load_dotenv()

app = Flask(__name__)
api = Api(app)

file_path = os.environ.get("RELATIVE_FILE_PATH", None)
if file_path is None:
    raise EnvironmentError("Missing RELATIVE_FILE_PATH in .env file.")


@api.route("/resume", defaults={"section": None})
@api.route("/resume[/<string:section>]")
class CVData(Resource):
    """Endpoint to read data from CV file. It may take a parameter called section to extract
    data of one section. By default it will read the file and structure the data in a JSON format
    """

    @api.response(200, "Success")
    @api.response(400, "Bad Request")
    @api.response(500, "Internal Server Error")
    @api.doc(
        description="""Returns Resume data all together or you can choose a specific section
        from the following: About, Contact, Education, Experience, Skills, 
        Languages, Projects."""
    )
    def get(self, section):
        """GET Logic of the endpoint"""
        cv_path = os.path.join(str(ROOT_DIR), file_path)
        if not os.path.exists(cv_path):
            abort(500, "File path does not exist")

        try:
            with open(cv_path, "r", encoding="utf-8") as file:
                content = file.read()

            if section is not None:
                section = section.capitalize()
                if section not in [
                    "About",
                    "Contact",
                    "Education",
                    "Experience",
                    "Skills",
                    "Languages",
                    "Projects",
                ]:
                    abort(
                        400,
                        """The section provided does not exist. Please choose from the following:
                        About, Contact, Education, Experience, Skills, Languages, Projects.""",
                    )

                result = get_section_data(section, content)

            else:
                result = get_all_sections(content)

            return result

        except EnvironmentError as error:
            print(error)
            abort(500, "Internal Server Error. Please contact an administrator")


if __name__ == "__main__":
    app.run()
