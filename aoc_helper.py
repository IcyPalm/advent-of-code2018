import os
from pathlib import Path
import logging
import requests
from bs4 import BeautifulSoup
from html2text import html2text

logging.basicConfig(level=logging.INFO)
# TODO: Move session token to env file or something like it
session_token = "123456789123456789123456789"

cookies = dict(session=session_token)
# TODO: Make some sort of terminal day selector
year = 2017
day = 12


def download_exercise(exercise_file):
    url = f"https://adventofcode.com/{year}/day/{day}"
    r = requests.get(url=url, cookies=cookies)
    page_content = str(BeautifulSoup(r.content, "html.parser").find("article"))

    markdown = html2text(page_content)
    with open(exercise_file, "w") as markdownfile:
        markdownfile.write(markdown)


def download_input(input_file):
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    r = requests.get(url=url, cookies=cookies)
    page_content = r.content
    with open(input_file, "wb") as write_file:
        write_file.write(page_content)


def create_day_setup():
    # Create daily folder:
    day_dir = Path(f"day_{day:02}")
    if not os.path.exists(day_dir):
        logging.info("Creating Directory")
        os.makedirs(day_dir)
    exercise_file = day_dir / 'README.md'
    if not exercise_file.is_file():
        logging.info("Create Excercise file")
        download_exercise(exercise_file)
    input_file = day_dir / 'input'
    if not input_file.is_file():
        logging.info("Downloading and creating input file")
        download_input(input_file)


create_day_setup()

# TODO: If finished: download part two!
