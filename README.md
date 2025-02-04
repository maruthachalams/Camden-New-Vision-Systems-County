# Camden NewVision Systems Data Scraper

This Python script scrapes data from the Camden NewVision Systems website using POST requests and saves the extracted information in a text file. It also attempts to download PDFs related to the data.

## Features
- Scrapes data from Camden NewVision Systems.
- Extracts information such as doc_id, party_code, party_name, cross_party_name, rec_date, doc_type, town, book, and page.
- Saves the extracted information into a text file (`Output.txt`).
- Attempts to download and save PDFs related to the extracted data.

## Requirements
- Python 3.x
- `requests` library
- `re` library

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/maruthachalams/Camden-New-Vision-Systems-County.git
    cd camden-data-scraper
    ```
2. Install the required libraries:
    ```sh
    pip install requests
    ```

## Usage
1. Ensure the input data file `input_instrument_no.txt` contains the instrument numbers you want to scrape, with one instrument number per line.
2. Run the script:
    ```sh
    python scraper.py
    ```
3. The output will be saved in a file named `Output.txt`. PDFs, if successfully downloaded, will be saved in the same directory.

## Code Explanation
### `single_regex(pattern, target_string)`
This function uses regular expressions to find matches in a target string and returns the first match found.

### Main Script
1. Initializes an output string with headers and writes it to `Output.txt`.
2. Reads instrument numbers from the `input_instrument_no.txt` file and stores them in a list.
3. For each instrument number in the list:
    - Sends a POST request to the Camden NewVision Systems API.
    - Prints the response status code and writes the response content to `Search_Page.html`.
    - Extracts data blocks from the response content using regular expressions.
    - Extracts information such as `doc_id`, `party_code`, `party_name`, `cross_party_name`, `rec_date`, `doc_type`, `town`, `book`, and `page`.
    - Sends a POST request to the API to download the PDF related to the `doc_id`.
    - Checks if the response is a PDF and saves it to a file if it is. Logs an error if it is not.
    - Formats the extracted information and appends it to `Output.txt`.

