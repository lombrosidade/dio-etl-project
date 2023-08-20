from src.utils import (
    get_synopsis,
    get_random_movie_id,
    get_films_dict,
    limited_movies,
)
import os
import random
import pandas as pd
from .conftest import get_csv_path
import pytest
from requests.exceptions import HTTPError

df_path = get_csv_path()
df = pd.read_csv(df_path)

def test_get_random_movie_id():
    movie_id = get_random_movie_id(df)
    assert isinstance(movie_id, str)
    assert movie_id in 

def test_get_synopsis():
    movie_id = get_random_movie_id(df)
    synopsis = get_synopsis(movie_id)
    # Test with valid ID
    assert isinstance(synopsis, str)
    # Test with invalid movie ID (should raise HTTPError)
    with pytest.raises(HTTPError):
        get_synopsis("3affcDDE")

def test_get_films_dict():
    # Pick a random number of films between 1 and 10 (if larger, it'll take too long)
    num_films = random.choice(range(1, 10))
    movie_synopses = get_films_dict(df, num_films)
    assert isinstance(movie_synopses, dict)
    assert len(movie_synopses) == num_films