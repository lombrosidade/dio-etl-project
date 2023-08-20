import os
from os import environ
from dotenv import load_dotenv
import pytest

REL_CSV_PATH = "data/Kim Newman's Nightmare Movies.csv"

def get_main_dir():
    main_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
    return main_dir

def get_csv_path():
    main_dir = get_main_dir()
    csv_path = os.path.abspath(
        os.path.join(main_dir, REL_CSV_PATH)
    )
    return csv_path