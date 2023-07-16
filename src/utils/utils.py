"""Module to provide add-ons for main server and cli modules"""

import re


def get_section_info(content, start_tag, end_tag):
    """Function extracting data between 2 resume sections"""
    if end_tag:
        pattern = re.escape(start_tag) + r"(.*?)" + re.escape(end_tag)
    else:
        pattern = re.escape(start_tag) + r"(.*$)" + ""

    match = re.search(pattern, content, re.DOTALL)
    if match:
        extracted_text = match.group(1).strip()
        return extracted_text

    return ""


def get_about_info(content):
    """Function extracting personal data"""
    return {
        "Full Name": get_section_info(content, "Full Name", "Title"),
        "Title": get_section_info(content, "Title", "About Me"),
        "About Me": get_section_info(content, "About Me", "Contact"),
    }


def get_contact_info(content):
    """Function extracting contact data from file"""
    result = {}

    contact_data = get_section_info(content, "Contact", "Education")

    for line in contact_data.splitlines():
        line_data = line.strip().split(":")
        if len(line_data) < 2:
            pass

        result[line.split(":", 1)[0].strip()] = line.split(":", 1)[1].strip()

    return result


def get_raw_array(content, start_tag, end_tag):
    """Function extracting data presented as array in the original input file"""
    data = get_section_info(content, start_tag, end_tag)

    return data.splitlines()


def get_raw_data(content, start_tag, end_tag, lines_number=0, keys=None, grouped=False):
    """Function extracting data and structuring data from experience,
    education and projects sections"""
    result = []

    if not keys or (grouped and not lines_number):
        return result

    data = get_section_info(content, start_tag, end_tag)

    if grouped:
        for line in data.strip().split("\n\n"):
            lines_split = line.strip().split("\n")
            if len(lines_split) < lines_number:
                pass

            entry = {key: lines_split[index] for index, key in enumerate(keys)}
            result.append(entry)
    else:
        pattern = r"^(.*?) - (.*?) \((.*?)\)$"
        for line in data.strip().splitlines():
            match = re.match(pattern, line.strip())

            if match:
                entry = {key: match.group(index + 1) for index, key in enumerate(keys)}
                result.append(entry)

    return result


def get_section_data(section, content):
    """Function combining the section data"""
    match section:
        case "About":
            result = get_about_info(content)
        case "Contact":
            result = get_contact_info(content)
        case "Education":
            result = get_raw_data(
                content,
                "Education",
                "Experience",
                lines_number=3,
                keys=["Duration", "Degree", "Institution"],
                grouped=True,
            )
        case "Experience":
            result = get_raw_data(
                content,
                "Experience",
                "Tech Skills",
                lines_number=4,
                keys=["Duration", "Company", "Position", "Description"],
                grouped=True,
            )
        case "Skills":
            result = get_raw_array(content, "Tech Skills", "Languages")
        case "Languages":
            result = get_raw_array(content, "Languages", "Some Personal Projects")
        case "Projects":
            result = get_raw_data(
                content,
                "Some Personal Projects",
                "",
                lines_number=0,
                keys=["Name", "Description", "Stack"],
            )
        case _:
            result = {}

    return result


def get_all_sections(content):
    try:
        result = {
            "About": get_about_info(content),
            "Contact": get_contact_info(content),
            "Education": get_raw_data(
                content,
                "Education",
                "Experience",
                lines_number=3,
                keys=["Duration", "Degree", "Institution"],
                grouped=True,
            ),
            "Experience": get_raw_data(
                content,
                "Experience",
                "Tech Skills",
                lines_number=4,
                keys=["Duration", "Company", "Position", "Description"],
                grouped=True,
            ),
            "Tech Skills": get_raw_array(content, "Tech Skills", "Languages"),
            "Languages": get_raw_array(content, "Languages", "Some Personal Projects"),
            "Projects": get_raw_data(
                content,
                "Some Personal Projects",
                "",
                lines_number=0,
                keys=["Name", "Description", "Stack"],
            ),
        }
    except Exception as error:
        print(error)
        return {}

    return result
