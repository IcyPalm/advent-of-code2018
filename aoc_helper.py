import os
from os.path import dirname
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
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Environment settings for .env files
dotenv_path = Path(dirname(__file__)) / '.env'
load_dotenv(dotenv_path)
AOC_SESSION_TOKEN = os.getenv('AOC_SESSION_TOKEN')


def download_exercise(exercise_file):
    url = f'https://adventofcode.com/{AOC_YEAR}/day/{AOC_DAY}'
    r = requests.get(url=url, cookies=dict(session=AOC_SESSION_TOKEN))
    page_content = str(BeautifulSoup(r.content, 'html.parser').find('article'))

    markdown = html2text(page_content)
    with open(exercise_file, 'w') as markdownfile:
        markdownfile.write(markdown)


def download_input(input_file):
    url = f'https://adventofcode.com/{AOC_YEAR}/day/{AOC_DAY}/input'
    r = requests.get(url=url, cookies=dict(session=AOC_SESSION_TOKEN))
    page_content = r.content
    with open(input_file, 'wb') as write_file:
        write_file.write(page_content)


def create_day_setup():
    # Create daily folder:
    day_dir = Path(f'day_{AOC_DAY:02}')
    logging.debug(f'Directory name: {day_dir}')
    if not os.path.exists(day_dir):
        logging.info(f'Creating Directory {day_dir}')
        os.makedirs(day_dir)
    else:
        logging.debug('Directory exists, skip creating')
        # TODO: Ask for override
    exercise_file = day_dir / 'README.md'
    logging.debug(f'')
    if not exercise_file.is_file():
        logging.info('Create Exercise file')
        download_exercise(exercise_file)
    input_file = day_dir / 'input'
    if not input_file.is_file():
        logging.info('Downloading and creating input file')
        download_input(input_file)


def check_session_token(new_session_token=''):
    if new_session_token:
        set_aoc_session(new_session_token)
    if not AOC_SESSION_TOKEN:
        click.echo('It seems that you have not set your AOC session token!')
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
    # TODO: Check if exercise is finished(and part two), if not suggest last day
    return -1


def get_day(day_input):
    if day_input:
        return day_input
    else:
        day = guess_day()
        if day > 0:
            if click.confirm(f'Looks like the day you want is: {day}, correct?'):
                return day
    return click.prompt('Please fill in the day(1-31)', type=click.IntRange(1, 31))


@click.command()
@click.option('--session_token', help='Set (a new) AOC session token', metavar='<SESSIONTOKEN>')
@click.option('--year', '-y', 'year_input', type=int, help='Set the year', metavar='2018')
@click.option('--day', '-d', 'day_input', type=click.IntRange(1, 31), help='Set the day', metavar='19')
def main(session_token, day_input, year_input=AOC_DAY):
    check_session_token(session_token)
    global AOC_YEAR
    AOC_YEAR = year_input
    global AOC_DAY
    AOC_DAY = get_day(day_input)
    create_day_setup()
    # TODO: Create stub exercise file for specific day
    # TODO: Download part two of a day(does the input differ?)
    # TODO: Build a README in main dir
    # TODO: Maybe even submit an answer?


if __name__ == '__main__':
    main()
