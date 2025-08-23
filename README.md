## Text Extraction Tool

This is a Pyhton-based tool that extracts text from an URL and save the results to structured files.

## Features
- Crawls websites starting from a given URL.
- Extracts and saves text from web pages.
- Supports filtering of links (e.g., exclude PDFs, images).
- Exports data into`.xlsx` file based on the language used, with each tab corresponding to each webpage.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/text-extraction-tool.git
   cd text-extraction-tool

2. Create and activate a virtual environment:
    ```bash
    python -m venv .venv

3. Install dependencies:
    pip install -r requirements.txt

4. Run the tool with
    ```bash
    python main.py

### Output Format
One Excel file per language detected. File name pattern:

```
<domain>_<lang>.xlsx  # e.g., example.com_en.xlsx, example.com_it.xlsx
```

If language is not specified in the URL path, file name is **default** as follows:

```
example.com_default.xlsx
```

Each workbook contains one sheet per page (tab name is the relative URL of the page, trimmed to Excel’s 31‑char limit). Data on each page is formatted in columns. Expected types of output is displayed as below:

| **Title** | **Description** | **CTA** |
| --------- | --------------- | ------- |
| H1, H2 Text | Paragraphs/spans/div text under that section | List of CTA texts |
| Empty Header| Text without a header | List of CTA texts |