# Movie Synopsis Generator ETL Project
This project is a Python-based ETL (Extract, Transform, Load) application that retrieves data from an IMDb user list and generates new movie synopses using the OpenAI API. The generated synopses blend elements from existing synopses to create captivating and unique summaries for movies.
**Special Thanks:** This project is made possible thanks to the individual who created and shared the original IMDb user list titled "Kim Newman's Nightmare Movies," which is based on the book by Kim Newman. We also extend our gratitude to Kim Newman for his great work. You can find the original list [here](https://www.imdb.com/list/ls070229682/).

# Directory Structure
The project directory is structured as follows:
```bash
├── data/
│   └── Kim Newman's Nightmare Movies.csv   # IMDb user list data
├── src/
│   ├── __init__.py
│   ├── gpt.py          # Main script to generate new synopses
│   └── utils.py        # Utility functions for data retrieval and generation
├── tests/
│   ├── __init__.py
│   ├── conftest.py     # Configuration for test fixtures
│   └── test_utils.py   # Test functions for utility functions
├── .gitignore          # Specifies files/directories to ignore in version control
├── example.env         # Example environment variables
└── README.md           # Project documentation
```

Running Tests
To run the tests, navigate to the root directory of the project and execute the following command:
```bash
pytest
````

Loading OpenAI API Key
Create a file named .env in the root directory.

Add your OpenAI API key to the .env file in the following format:
```makefile
OPENAI_KEY=your_api_key_here
````
Replace your_api_key_here with your actual OpenAI API key.

Save the .env file and add it to the .gitignore before uploading it to the repository. In case you have doubts, just look at the example.env file.

Usage
The primary script for generating new synopses is gpt.py. It reads IMDb user list data, extracts information, and generates new synopses for movies based on the provided inspiration synopses. You can run the script as follows:

```bash
python src/gpt.py --num num_films --verbose True
```
Replace num_synopses with the number of films you want to generate. Use the --verbose flag to display existing synopses when generating new ones. Each film is generated from a combination of two existing synopses.

**Note**

This project was developed as part of a course on DIO.ME. It aims to demonstrate the ETL process using real-world data and the OpenAI API for creative text generation.

Feel free to modify the README to provide more details or customize it according to your project's requirements.

# License
[MIT](https://github.com/lombrosidade/dio-etl-project/blob/main/LICENSE)
