# CryptoDataScience
Fun Data Science project to experiment with Crypto Tokens. 

# Start postgres container
docker-compose up

# Install dependencies
poetry install

# Run in Single Mode

Collects data from a single date

poetry run python app.py single --id (e.g. bitcoin) --date YYYY-MM-DD

# Run in Batch Mode

Collects data from a date range

poetry run python app.py batch --id (e.g. bitcoin) --start YYYY-MM-DD --end YYYY-MM-DD

