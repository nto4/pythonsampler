"""
This script fetches data from a CSV file at the given url,
and returns the data in the columns given as parameters in a "data" envelope.
Author: https://github.com/nto4
Date: 12/28/2023
"""
import argparse
import json
from io import StringIO
import requests
import pandas as pd

# Constants
CSV_FILE_URL = "https://drive.google.com/uc?id=1zLdEcpzCp357s3Rse112Lch9EMUWzMLE"

def read_csv_from_url(fields):
    """
    This function fetches data from a CSV file at the given URL,
    and returns the data in the columns specified by the 'fields' parameter.
    """
    try:
        headers = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
        response = requests.get(CSV_FILE_URL, headers=headers, timeout=10)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            data = pd.read_csv(StringIO(content))
            if fields:
                data = data[fields]
            return {"data": data.to_dict(orient='records')}
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
    except requests.RequestException as req_err:
        return {"error": f"Request Exception: {req_err}"}
    except pd.errors.ParserError as parse_err:
        return {"error": f"Error parsing CSV file: {parse_err}"}
    except Exception as ex:
        return {"error": f"Exception occurred: {ex}"}
def main():
    """
    argument wrapper and runner for read_csv_from_url fuction
    """
    parser = argparse.ArgumentParser(
        description='Fetch data from a CSV file hosted on Google Drive.')
    parser.add_argument('--fields', type=str,
        help='Specify fields to return from the CSV file separated by commas')
    args = parser.parse_args()
    if args.fields:
        result = read_csv_from_url(args.fields.split(','))
        print(json.dumps(result, separators=(',', ':')))
    else:
        print("Please specify fields using --fields argument.")
if __name__ == "__main__":
    main()
