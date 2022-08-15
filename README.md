# Script to extract search results from amazon Uk 

This script extracts search results from amazon.co.uk 
and stores result in csv file. 

reference: https://www.scrapehero.com/tutorial-how-to-scrape-amazon-product-details-using-python-and-selectorlib/

## To run the script follow below steps:

### Create python virtual environment in terminal
    python venv venv 

### activate python virtual environment
    source venv/bin/activate

### Install requirements
    python -m pip -r requirements.txt

### Finally, run the script
    python main.py 

## Limitations:
- Script has hardcoded url because we have only tested on amazon.co.uk
- Search terms are input in file to run as batch, Todo as run as command argument
- Uses async library but could hit performance issue if search terms 
  increases, TODO: need to add more reliable way to handle larger batch of 
  search terms.
