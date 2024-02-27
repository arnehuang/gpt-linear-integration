# Description
api to trigger linear tickets from customer support chat transcripts

# Setup
Python 3.11+ 

Install pipenv globally if you don't have

`pip3 install pipenv`

Use Pipenv to manage the environment

`pipenv install --dev`

To lint the code

`black .`

# Running
Make sure to set up `.env` file by using `.env_example`

run `pipenv run python application.py`

Bug 
```commandline
curl --location --request POST 'http://127.0.0.1:5000/classify' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_text":"I can not press submit because the page never validates my address"
}'
```

Feature
```commandline
curl --location --request POST 'http://127.0.0.1:5000/classify' \
--header 'Content-Type: application/json' \
--data-raw '{
    "input_text":"you should make the button red because its hard to see when I use dark mode"
}'
```