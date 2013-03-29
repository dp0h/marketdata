Market Data
==========
Library for working with Market Data


# ToDo
- Module to find working days for stock exchange
- db create tool
- module to retrieve market data and put to db
- module to load market data to pandas objects

# DB creation
import table_def
table_def.create_all()

# virtualenv setup
virtualenv --distribute .
source bin/activate
pip install -r requirements.txt

