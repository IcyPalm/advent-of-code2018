import os
from os.path import join, dirname
from pathlib import Path
import click
import logging
import requests
from bs4 import BeautifulSoup
from html2text import html2text
from dotenv import load_dotenv, set_key

# Small config
AOC_YEAR = 2018
AOC_DAY = 1

# Logging config
logging.basicConfig(level=logging.INFO)
# TODO: Logger formatting without user etc

# Environment settings for .env files
dotenv_path = Path(dirname(__file__)) / '.env'
load_dotenv(dotenv_path)
AOC_SESSION_TOKEN = os.getenv("AOC_SESSION_TOKEN")


# cookies = dict(session=session_token)


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


# TODO: If finished: download part two!
#
#
#     `7MN.   `7MF'                              .M"""bgd           mm
#       MMN.    M                               ,MI    "Y           MM
#       M YMb   M  .gP"Ya `7M'    ,A    `MF'    `MMb.      .gP"Ya mmMMmm `7MM  `7MM `7MMpdMAo.
#       M  `MN. M ,M'   Yb  VA   ,VAA   ,V        `YMMNq. ,M'   Yb  MM     MM    MM   MM   `Wb
#       M   `MM.M 8M""""""   VA ,V  VA ,V       .     `MM 8M""""""  MM     MM    MM   MM    M8
#       M     YMM YM.    ,    VVV    VVV        Mb     dM YM.    ,  MM     MM    MM   MM   ,AP
#     .JML.    YM  `Mbmmd'     W      W         P"Ybmmd"   `Mbmmd'  `Mbmo  `Mbod"YML. MMbmmd'
#                                                                                     MM
#                                                                                   .JMML.

def check_session_token(new_session_token=""):
    if new_session_token:
        set_aoc_session(new_session_token)
    if not AOC_SESSION_TOKEN:
        click.echo("It seems that you have not set your AOC session token!")
        session_token = click.prompt('Please enter your AOC session token', type=str)
        # TODO: Checking if session token is valid
        set_aoc_session(session_token)


def set_aoc_session(new_session_token):
    # Check if .env exists
    if not dotenv_path.is_file():
        open(dotenv_path, 'w+')
    set_key(dotenv_path, 'AOC_SESSION_TOKEN', new_session_token)
    global AOC_SESSION_TOKEN
    AOC_SESSION_TOKEN = new_session_token


def guess_day():
    directories = []
    for dir_or_file in os.listdir('.'):
        if os.path.isdir(dir_or_file) and dir_or_file.startswith('day'):
            directories.append(dir_or_file)
    if len(directories) > 0:
        directories.sort()
        day = directories.pop().strip('day_')
        day = int(day)
        return day
    return -1


@click.command()
@click.option('--session_token', help='Set (a new) AOC session token', metavar='<SESSIONTOKEN>')
@click.option('--year', '-y', 'year_input', type=int, help='Set the year', metavar='2018')
@click.option('--day', '-d', 'day_input', type=int, help='Set the day', metavar='19')
def main(session_token, year_input, day_input):
    check_session_token(session_token)
    if year_input:
        global AOC_YEAR
        AOC_YEAR = year_input
    if not day_input:
        day_input = guess_day()
    print(day_input)
    global AOC_DAY
    AOC_DAY = day_input


if __name__ == "__main__":
    main()
