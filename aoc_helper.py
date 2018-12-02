import importlib
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
# AOC_YEAR = 2017  # testing
AOC_DAY = 1

# Logging config
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Environment settings for .env files
dotenv_path = Path(dirname(__file__)) / '.env'
load_dotenv(dotenv_path)
AOC_SESSION_TOKEN = os.getenv('AOC_SESSION_TOKEN')


class AocExercise:
    title = None
    part_one = None
    part_one_answer = None
    part_two = None
    part_two_answer = None

    def get_html(self):
        return '\n'.join((filter(None, (self.part_one, self.part_one_answer, self.part_two, self.part_two_answer))))


def download_exercise(exercise_file):
    url = f'https://adventofcode.com/{AOC_YEAR}/day/{AOC_DAY}'
    logging.debug(f'Downloading exercise from:{url}')
    r = requests.get(url=url, cookies=dict(session=AOC_SESSION_TOKEN))
    page_content = BeautifulSoup(r.content, 'html.parser').findAll('article')
    parts_count = len(page_content)
    exercise = AocExercise()
    exercise.title = BeautifulSoup(r.content, 'html.parser').find('article').find('h2').contents[0].strip('-').strip()
    exercise.part_one = str(page_content[0])
    if parts_count > 1:
        answerstring = str(page_content[0].find_next_sibling('p'))
        exercise.part_one_answer = answerstring if 'Your puzzle answer was' in answerstring else None
        exercise.part_two = str(page_content[1])
        answerstring = str(page_content[1].find_next_sibling('p'))
        exercise.part_two_answer = answerstring if 'Your puzzle answer was' in answerstring else None

    markdown = html2text(exercise.get_html())
    with open(exercise_file, 'w') as markdownfile:
        markdownfile.write(markdown)


def download_input(input_file):
    url = f'https://adventofcode.com/{AOC_YEAR}/day/{AOC_DAY}/input'
    logging.debug(f'Downloading input file from:{url}')
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
        logging.info('Directory exists, skip creating')
        # TODO: Ask for override

    exercise_file = day_dir / 'README.md'
    logging.debug(f'Exercise file: {exercise_file}')
    if not exercise_file.is_file():
        logging.info('Create Exercise file')
        download_exercise(exercise_file)
    else:
        logging.info('Exercise file exists, skip creating')
        # TODO: Ask for override

    input_file = day_dir / 'input'
    logging.debug(f'Input file: {input_file}')
    if not input_file.is_file():
        logging.info('Downloading and creating input file')
        download_input(input_file)
    else:
        logging.info('Input file exists, skip creating')
        # TODO: Ask for override

    day_template = day_dir / f'day_{AOC_DAY:02}.py'
    logging.debug(f'Template file: {day_template}')
    if not day_template.is_file():
        logging.info('Copying Template')
        with open('template.py', 'r') as template:
            with open(day_template, 'w') as f:
                f.write(template.read())
    else:
        logging.info('Template file exists, skip creating')
        # TODO: Ask for override


def check_session_token(new_session_token=''):
    # If a new session token is set, take that one
    if new_session_token:
        logging.debug('New session token given, setting that')
        session_token = new_session_token
    # If not a new token is given and there is no environment variable set with the token, ask for one
    elif not AOC_SESSION_TOKEN:
        logging.debug('No new and no environment varible with Token, asking user for new token')
        click.echo('It seems that you have not set your AOC session token!')
        session_token = click.prompt('Please enter your AOC session token', type=str)
    else:
        logging.debug('We have a token, setting that')
        session_token = AOC_SESSION_TOKEN
    url = 'https://adventofcode.com/'
    token_valid = False
    while not token_valid:
        logging.debug('testing if session token is valid')
        r = requests.get(url=url, cookies=dict(session=session_token))
        user_div = BeautifulSoup(r.content, 'html.parser').find('div', class_='user')
        if not user_div:
            logging.debug('Token is invalid, asking user for a new one')
            click.echo('It seems that the session token is invalid')
            session_token = click.prompt('Please enter your AOC session token', type=str)
        else:
            logging.debug('User div is found, session is valid')
            username = str(user_div.string)
            click.echo('It seems that the token is valid')
            click.echo(f'Hello {username}')
            token_valid = True
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
            if click.confirm(f'Looks like the day you want to get is: {day}, correct?'):
                return day
    return click.prompt('Please fill in the day(1-25)', type=click.IntRange(1, 25))


def submit_exercise():
    day_template = f'day_{AOC_DAY:02}'
    exercise_file = importlib.import_module(f'{day_template}.{day_template}')
    # TODO: Actually submit


@click.command()
@click.option('--session_token', help='Set (a new) AOC session token', metavar='<SESSIONTOKEN>')
@click.option('--year', '-y', 'year_input', type=int, help='Set the year', metavar='2018')
@click.option('--day', '-d', 'day_input', type=click.IntRange(1, 25), help='Set the day', metavar='19')
@click.option('--loglevel', default='WARNING', type=click.Choice(logging._levelToName.values()),
              help='Set the loglevel', metavar='INFO')
@click.option('--submit', '-s', is_flag=True)
def main(session_token, day_input, loglevel, submit, year_input=AOC_DAY):
    logging.getLogger().setLevel(getattr(logging, loglevel))
    check_session_token(session_token)
    if year_input:
        global AOC_YEAR
        AOC_YEAR = year_input
    global AOC_DAY
    AOC_DAY = get_day(day_input)
    if submit:
        submit_exercise()
    else:
        create_day_setup()
    # TODO: commandline handler asking what user wants to do, get day, submit, other things?
    # TODO: Figure out how to handle part one and part two
    # TODO: Download part two of a day(does the input differ?)
    # TODO: Build a README in main dir
    # TODO: Maybe even submit an answer?


if __name__ == '__main__':
    main()
