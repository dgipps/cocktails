# Overview

Takes in a csv roughly in the form of https://docs.google.com/spreadsheets/d/1nJYYm_iHRjFBK8Qv5iwcAb1mP9t82YmXiffl8VnAEqY/edit?usp=sharing although cleaned up a bit

# Setup

`source env/bin/activate`

`poetry install`

# Load cocktails

`manage.py load_death_co_cocktails -i <path_to_csv>`

# Start

`manage.py runserver`

# Test

`manage.py test`