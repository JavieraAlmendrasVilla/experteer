# Premium Recruitment Assistant – CSV-to-HTML Pipeline

This repository provides a Python pipeline that converts candidate export CSV files into fully-styled HTML email templates for Experteer’s Premium Recruitment Assistant.
The script reads CSV data, extracts and filters candidate information, enriches it with optional expertise and logo data, and finally generates polished HTML files ready for use in outreach emails.

## Features

* Automatic detection of file encoding using **chardet**
* Extraction of:

  * Project name 
  * Candidate details and ranking 
  * Expertise tags per candidate
* Automatic assignment of default or custom profile photos
* Sorting candidates by suitability ("Hervorragend" → "Sehr gut" → "Gut")
* Support for custom project logos
* Safe folder-cleaning function for output directories
* Generation of complete HTML email documents with Experteer branding

## Input CSV Requirements

The script expects the following columns (tab-delimited by default):

* `Projektname`
* `Mitglieds ID`
* `Anrede`
* `Vorname`
* `Nachname`
* `Titel`
* `Aktuelle Position`
* `Firma`
* `Branche`
* `E-Mail`
* `Telefonnummer`
* `URL Kandidatenprofil`
* `Projekteignung` (`Hervorragend`, `Sehr gut`, or `Gut`)

## Core Functions

### `extract_projektname_from_csv(path)`

Reads a CSV file and returns the first non-empty `Projektname`.

### `extract_candidates_from_csv(path, filter_eignung=None, special_logos=None)`

Parses all candidates, applies ranking and filters, injects special logos or default photos, and returns a clean list of candidate dictionaries.

### `generate_html(title, logo_url, job_id, expertise_dict, number_candidates, candidates, output_file)`

Renders a complete branded HTML email containing all candidate profiles.

### `clear_folder(path)`

Removes all files from a given directory.

### `generate_german_emails(folder_path, output_folder, filter_eignung, special_logos, project_logos)`

Processes all CSVs in a folder and generates an HTML file for each project.

## Usage Example

```python
from pipeline import generate_german_emails, clear_folder

input_folder = "input/"
output_folder = "output/"

special_logos = {
    "12345": {"url": "https://example.com/custom.png"}
}

project_logos = {
    "Finance Director München": ["FinanceCo", "cdn.financeco.com/logo.png"]
}

clear_folder(output_folder)

generate_german_emails(
    folder_path=input_folder,
    output_folder=output_folder,
    filter_eignung="Gut",
    special_logos=special_logos,
    project_logos=project_logos
)
```

## Output

Each processed CSV produces one HTML file containing:

* Client greeting text
* Job title & project logo
* Candidate cards with:

  * Name and title
  * Current role, company, industry
  * Email & phone links
  * Profile image
  * Expertise tags (if provided)
  * Link to Experteer profile

