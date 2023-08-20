import os
import requests
import argparse
import pandas as pd
from bs4 import BeautifulSoup
from typing import Dict, List, Tuple, Optional, Union

# Retrieve absolute path for CSV file
MAIN_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
)
REL_CSV_PATH = "data/Kim Newman's Nightmare Movies.csv"
DF_PATH = os.path.join(MAIN_DIR, REL_CSV_PATH)
ABS_CSV_PATH = os.path.abspath(DF_PATH)
assert os.path.isfile(ABS_CSV_PATH) is True, ".CSV file couldn't be found in directory: {ABS_CSV_PATH}"
df = pd.read_csv(ABS_CSV_PATH)

# Default values for argparse
MIN_FILMS = 1 # Minimum number of films
MAX_FILMS = 10 # Maximum number of films

# Default IMDB URL
IMDB_URL = 'https://www.imdb.com/title'

# User-agent headers is needed for the request to go through
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

def get_synopsis(movie_id: str = '') -> str:
    """
    Retrieve the synopsis of a movie using its IMDb URL.

    Args:
        imdb_url (str): IMDb base URL.
        movie_id (str): IMDb movie ID.

    Returns:
        Optional[str]: The movie's synopsis or None if not found.
    """
    movie_url = f'{IMDB_URL + movie_id}'
    try:
        movie_request = requests.get(movie_url, headers=HEADERS, timeout=10)
        movie_request.raise_for_status()
        movie_soup = BeautifulSoup(movie_request.content, 'html.parser')
        meta_tag = movie_soup.find('meta', {'data-id': 'main', 'name': 'description'})
        if meta_tag:
            synopsis = meta_tag.get('content', '').strip()
            return synopsis
    except requests.exceptions.HTTPError as exc:
        raise requests.exceptions.HTTPError from exc

def get_random_movie_id(movie_df: pd.DataFrame = df) -> str:
    """
    Get a random movie ID from the DataFrame.

    Args:
        movie_df (pd.DataFrame): DataFrame containing movie data.

    Returns:
        str: Random movie ID.
    """
    random_id = movie_df.sample()['URL'].to_string().partition('title')[2]
    return random_id

def get_films_dict(movie_df: pd.DataFrame = df, num_films: int = 1) -> Dict[int, Tuple[str, str]]:
    """
    Generate a dictionary of movie synopses for a given number of films.

    Args:
        movie_df (pd.DataFrame): DataFrame containing movie data.
        num_films (int): Number of films for which to generate synopses.

    Returns:
        Dict[int, Tuple[Optional[str], Optional[str]]]: Dictionary mapping movie numbers to synopses.
    """
    movie_ids = [(get_random_movie_id(movie_df), get_random_movie_id(movie_df))
                 for _ in range(num_films)]
    movie_synopses = {movie_num: (get_synopsis(id1), get_synopsis(id2))
                      for movie_num, (id1, id2)
                      in enumerate(movie_ids, start=1)
    }
    return movie_synopses

def limited_movies(arg: str) -> int:
    """
    Type function for argparse - an integer within predefined bounds.

    Args:
        arg (str): The argument to be converted to an integer.

    Returns:
        int: The integer value if within bounds.

    Raises:
        argparse.ArgumentTypeError: If the argument is not a valid integer or not within bounds.
    """
    try:
        num_int = int(arg)
    except ValueError as exc:
        raise argparse.ArgumentTypeError('Must be an integer') from exc
    if num_int < MIN_FILMS or num_int > MAX_FILMS:
        raise argparse.ArgumentTypeError(f"Argument must be < {MIN_FILMS} and > {MAX_FILMS}")
    return num_int