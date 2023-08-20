from os import environ
import argparse
from typing import Dict, Tuple
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import pandas as pd
import openai
import utils

# Load the API key
load_dotenv()
OPENAI_KEY = environ.get('OPENAI_KEY')
openai.api_key = OPENAI_KEY

# Load the data
df = pd.read_csv("../data/Kim Newman's Nightmare Movies.csv")

def generate_new_synopsis(synopses: Dict[int, Tuple[str, str]], show_old_synopses: bool = False) -> str:
    """
    Generate new synopses for a series of movies based on provided inspiration synopses.

    Args:
        synopses (Dict[int, Tuple[str, str]]): A dictionary mapping movie numbers to a pair of existing synopses.
        show_old_synopses (bool, optional): Whether to print the old synopses when generating new ones. Default is False.

    Returns:
        str: A string containing the newly generated synopses for the movies.
    """
    system_prompt = """
    You are a movie connoisseur tasked with generating a new synopsis for a film.
    You have been given several synopses as inspiration. Your task is to create a
    creative and captivating synopsis that follows the same format as the provided
    synopses. The goal is to come up with a synopsis that entices the audience
    while maintaining the essence of the original synopses.
    """

    user_prompt = "Synopses for Inspiration:\n"
    for movie_id, syn_tuple in synopses.items():
        syn1, syn2 = syn_tuple
        synopsis_preview = f"Movie {movie_id}:\nSynopsis 1 for Movie {movie_id}: {syn1}\nSynopsis 2 for Movie {movie_id}: {syn2}\n"
        user_prompt += synopsis_preview
        if show_old_synopses:
            print("*" * 40)
            print("Here are the actual movies from the database:")
            print(synopsis_preview)
            print("*" * 40)

    user_prompt += """
    You are a talented writer with the task of crafting new synopses for a series of movies. Each movie consists of a movie ID followed by a pair of existing synopses that are provided as inspiration. Your objective is to generate a unique and captivating synopsis for each movie, following a specific format.
    For each movie ID:
    - Blend elements from the two given synopses to create a SINGLE and NEW synopsis.
    - Retain the core essence of the original synopses, but DO NOT COPY THEM.
    - Adhere to this structure: "[Invent a movie title here]: Directed by [Invent a director here]. With [Invent a cast here]. [Your new synopsis details here]."
    Your focus should be on producing a single new synopsis for each movie ID.
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    new_synopses = completion.choices[0].message["content"].strip()
    return new_synopses

def main(args: argparse.Namespace) -> str:
    """
    Generate new synopses for a specified number of movies.

    Args:
        args: Command-line arguments.

    Returns:
        str: A string containing the newly generated synopses for the movies.
    """
    num_films = args.num
    is_verbose = args.verbose
    movies_dict = utils.get_films_dict(df, num_films)
    new_synopses = generate_new_synopsis(movies_dict, is_verbose)
    print("*" * 20)
    print(new_synopses)
    print("*" * 20)
if __name__ == "__main__":

    ARG_DESC = """
    Pick random movies from a user-generated IMDb list and create a new synopsis
    using OpenAI API.
    """
    parser = argparse.ArgumentParser(description=ARG_DESC)
    parser.add_argument("--num", type=utils.limited_movies, 
                        default=1, 
                        help="Number of fake synopses and movies to generate."
    )
    parser.add_argument("--verbose", 
                        type=bool, 
                        default=False, 
                        help="Whether to show the synopses from the existing movies when generating the new ones"
                        )
    params = parser.parse_args()  # Parse the command-line arguments
    main(params)  # Call the main function with the parsed arguments