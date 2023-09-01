# CryptoDataScience
Fun Data Science project to experiment with Crypto Tokens. 

# Start postgres container
docker-compose up

# Install dependencies
poetry install

# Run in Single Mode

Collects data from a single date

poetry run python app.py single --id bitcoin --date 28-08-2023

# Run in Batch Mode

Collects data from a date range

poetry run python app.py batch --id bitcoin --start 28-08-2023 --end 29-06-2023

