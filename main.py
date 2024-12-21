import csv
import os
import chardet
import re
from pathlib import Path

def detect_file_encoding(file_path):
    """
    Detect the encoding of the given file.
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

def clear_folder(folder_path):
    """
    Remove all files in the specified folder.

    :param folder_path: Path to the folder where files should be removed.
    """
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    if not os.path.isdir(folder_path):
        print(f"The path '{folder_path}' is not a folder.")
        return

    # Iterate through all items in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it is a file before attempting to delete
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            except Exception as e:
                print(f"Error removing file {file_path}: {e}")

    print(f"All files in the folder '{folder_path}' have been removed.")

def read_html_template(country, file_part) -> str:
    
    if country == "DE":
        country_version = "german"
    elif country == "IT":
        country_version = "italian"
    else:
        return ""  # Ungültiger Ländercode

    path_html_files = Path(__file__).parent.resolve() / "html_files"

    # Datei bestimmen
    if file_part in ["header", "candidates"]:
        file_name = f"{file_part}.txt"
    elif file_part in ["body", "end"]:
        file_name = f"{file_part}_{country_version}.txt"
    else:
        return ""  # Ungültiger Dateiteil

    # Dateiinhalt lesen
    try:
        path = path_html_files / file_name
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return ""  # Datei nicht gefunden
    except Exception as e:
        print(f"Error reading the text: {e}")
        return ""

def extract_project_name_from_csv(country, csv_file):
    """
    Extract a single project name ('Projektname') from the given CSV file.

    :param csv_file: Path to the CSV file
    :return: The first encountered project name
    """
    # Detect the file encoding
    encoding = detect_file_encoding(csv_file)
    projektname = ""
    with open(csv_file, 'r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file, delimiter="\t")  # Adjust delimiter if needed

        for row in csv_reader:
            if country == "IT":
                projektname = row["Nome del progetto"].strip()
            elif country == "DE":
                projektname = row["Projektname"].strip()
            if projektname:  # Return the first non-empty project name
                    
                return projektname
            
def extract_candidates_from_csv(country, csv_file, filter=None, profile_photo=None):
    
    profile_photo = profile_photo or {}
    # Detect file encoding
    encoding = detect_file_encoding(csv_file)

    candidates = []
    

    if country == "DE":
        rating_row = "Projekteignung"
        id_row = "Mitglieds ID"
        job_title = 'Aktuelle Position'
        company = "Firma"
        industry = "Branche"
        email = "E-Mail"
        phone = "Telefonnummer"
        profile_url = "URL Kandidatenprofil"
        gender = "Anrede"
        title = "Titel"
        first_name = "Vorname"
        last_name = "Nachname"

    if country == "IT":
        rating_row = "Valutazione del progetto"
        id_row = "ID utente"
        job_title = 'Posizione attuale'
        company = "Azienda"
        industry = "Settore"
        email = "Indirizzo email"
        phone = "Numero di telefono"
        profile_url = "URL del profilo del candidato"
        gender = "Titolo"
        title = "Posizione"
        first_name = "Nome"
        last_name = "Cognome"

    with open(csv_file, 'r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file, delimiter="\t")  # Adjust delimiter if needed

        for row in csv_reader:
            # Apply filter on "Projekteignung" if specified
            if filter:
                rate = row[rating_row].strip()
                if rate not in ["Sehr gut", "Gut","Buono", "Molto buono"]:
                    continue

            # Determine photo URL based on "Anrede"
            candidate_id = row[id_row]
            if candidate_id in profile_photo and "url" in profile_photo[candidate_id]:
                photo_url = profile_photo[candidate_id]["url"]
            elif row[gender] == "Herr" or "Signor":
                photo_url = "https://www.experteer.de/images/default_photos/male.png"
            elif row[gender] == "Frau" or "Signora":
                photo_url = "https://www.experteer.de/images/default_photos/female.png"
            else:
                photo_url = "https://www.experteer.de/images/default_photos/female.png"

            # Include the title in the candidate's name if present
            Title = row[title].strip()
            full_name = f"{Title} {row[first_name]} {row[last_name]}".strip() if Title else f"{row[first_name]} {row[last_name]}".strip()


            # Extract relevant fields
            candidate = {
                "name": full_name,
                "id": row[id_row],
                "job_title": row[job_title],
                "company": row[company],
                "industry": row[industry],
                "email": row[email],
                "phone": row[phone],
                "photo_url": photo_url,
                "profile_url": row[profile_url],
            }
            candidates.append(candidate)

    return candidates

def generate_html(country, title, logo_url, expertise_dict, number_candidates, candidates, output_file):
    """
    Generate an HTML file for the provided candidate data.

    :param title: The title of the HTML document.
    :param logo_url: The URL of the logo to be included in the HTML.
    :param number_candidates: Number of candidates included in the HTML.
    :param candidates: List of dictionaries containing candidate data.
    :param output_file: The file path where the HTML will be saved.
    """
    
    # Base HTML template
    header = read_html_template(country, "header")
    body = read_html_template(country, "body")
    candidate_template = read_html_template(country, "candidates")
    end = read_html_template(country, "end")
    html_template = header + body
    print(html_template)
    
    # Generate expertise table rows
    def generate_expertise_rows(expertise_list):
        return "".join(f"""
            <td style="border: solid 1px #525B65; border-radius: 50px;padding: 2px 6px 2px 6px;">
                {expertise}
            </td>
        """ for expertise in expertise_list)

    # Create the candidates' section content
    candidates_section = ""
    for candidate in candidates:
        candidate_id = candidate["id"]
        expertise_list_html = ""

        # Retrieve expertise for the candidate
        if candidate_id in expertise_dict:
            expertise_list_html = generate_expertise_rows(expertise_dict[candidate_id]["expertises"])
        
        candidates_section += candidate_template.format(
            candidate_name=candidate["name"],
            job_title=candidate["job_title"],
            company=candidate["company"],
            industry=candidate["industry"],
            email=candidate["email"],
            phone=candidate["phone"],
            photo_url=candidate["photo_url"],
            profile_url=candidate["profile_url"],
            expertise_list=expertise_list_html,
        )

    # Combine the template with the filled candidate sections

    candidates_complete = candidates_section.format(candidates_section=candidates_section)
    
    html_content = html_template.format(title=title, logo_url=logo_url, number_candidates=number_candidates)

    html_final = html_content + candidates_complete + end
    
    # Save the HTML to a file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_final)
    print(f"HTML file '{output_file}' has been generated successfully.")

def generate_emails(country, folder_path, output_folder, filter, profile_photo, project_logos):
    
    profile_photo = profile_photo or {}
    project_logos = project_logos or {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            csv_file = os.path.join(folder_path, file_name)
            title = extract_project_name_from_csv(country, csv_file)

            if not title:
                print(f"Skipping file {csv_file}: No project name found.")
                continue

            candidates = extract_candidates_from_csv(
                country, csv_file, filter=filter, profile_photo=profile_photo
            )

            # Check if the title exists in project_logos
            if title in project_logos.keys():
                company_logo_url = project_logos[title]
            else:
                print(f"Warning: No logo found for project '{title}'.")
                company_logo_url = "https://default-logo-url.com/default-logo.png"  # Replace with your actual default URL

            if not os.path.exists(output_folder):
                os.mkdir(output_folder)

            sanitized_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            output_file_path = os.path.join(output_folder, f"{sanitized_title}.html")
            

            generate_html(
                country=country,
                title=title,
                logo_url=company_logo_url,
                expertise_dict=profile_photo,
                number_candidates=len(candidates),
                candidates=candidates,
                output_file=output_file_path
            )
            print(f"HTML file generated for project '{title}' at {output_file_path}")

if __name__ == "__main__":
    candidates_info = {
        
        "106254" : {
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH1LcyMjs3hDUyMDUyNjEzNTNmu2ECvOkszc1EwGAGPyI1Y%7Cb2620e0586594bb457e00ccd130d39e17ed963f9.career/profile_photo/97226_1520523465"
            ,"expertises": ["Sales Promotion" , "Trade Marketing" , "Werbung"]
        },
        "401083":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1jMyNLU4N4Q1NLAxNLcyMzUzZrthArzpLM3NRMBgCHhCOV1fb071483233d76247a6a245d8c4437e29616354.career/profile_photo/362950_1590497265",
            "expertises":["SAP Gui & CRM", "Internationale Projekterfahrung"]   
        },
        "200189":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1DC0MzI9N4Q3NjY0tLIDZns2YLseIsycxNzWQAAIeeI5k%7Ccc26c3963949e3cffea0a8a9390c114fc70bd1e4.career/profile_photo/181625_1733993397",
            "expertises":["Lehrgang für junge Kaufleute" , "Rethorik Lehrgang"]
        },
        "89928":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH0LI1Nj03hDEwMLAwNLIzMLNmu2ECvOkszc1EwGAGPmI1g%7Cc2458736e77a3f0823633c97e59ac1ebacaeb2e7.career/profile_photo/82535_1408009268",
            "expertises":["Steuerung und Koordination internationaler Agenturen (Media, Kreation, PR)"]
        },
        "176288":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1DU0sLE-N4Q3NjEyNTE0NLQzZrthArzpLM3NRMBgCHTSOP69c7833046a0c58fc1e40ba1a71d234425a0d3e0.career/profile_photo/159843_1734254191",
            "expertises":["Budgetplanung" , "Umstruckturierung"]
        },
        "133677":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1DI0NjY4t4Q1MTIwtjC0NTMzZrthArzpLM3NRMBgCGVSOJ97869ef6916b13eae762beedc9335892879342f1.career/profile_photo/121338_1542838156",
            "expertises":["CRM" , "Key Account Management"]
        },
        "42325":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH1jSzNLy3hDUzNzM0tjI1MLNmu2ECvOkszc1EwGAGY4I3M%7C2d6f01de1a39b313f724e341b4ae5110b102be03.career/profile_photo/39699_1567693258",
            "expertises":["CRM", "Sales Management" , "Solution Selling"]
        },
        "715152":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH0zQxNjM6N4QxMDCwNjQyNzczZrthArzpLM3NRMBgCGGyODc1355005211fee7cab73983c844df8c82861eaed.career/profile_photo/614362_1408031277",
            "expertises":["Erstellung von Jahresplanungen Umsatz Kosten Liquidität"]
        },
        "201290":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1DCyMzE6N4QxNjIzMjYwNTMzZrthArzpLM3NRMBgCGMiOD043aabe362a582c33948103624a26b9016d183aa.career/profile_photo/182642_1432623056",
            "expertises":["Angebotserstellung", "Preisverhandlungen"]
        },
        "498810":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH0TE0tzc9N4QxMDCwMjEzNDSzZrthArzpLM3NRMBgCHpiOTd4a6c174e867d9c8339aee1e3b3a2a81c787ea4f.career/profile_photo/449775_1408024619",
            "expertises":["Einkauf", "Produkt-,Marketingmanagement"]
        },
        "145888":{
             "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1DYyNjY4N4Q1OgRksLIwMTNmu2ECvOkszc1EwGAIVhI3w%7C71bcb172b7162ca164d347871bfef99fe2837f0d.career/profile_photo/132330_1516098204",
             "expertises":["Excel" , "Grundlagen SAP","MS-Office"]
        },
        "123798": {
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1DQyMLS7N4QxMDCwNDA0tLQzZrthArzpLM3NRMBgCGhiOIbbfa6eaaae9950c6ea4cd1e5b2a466e7993a569b.career/profile_photo/112896_1408010991",
            "expertises":["Stratege im internationen, globalen automotive Markt"]
            
        },
        "103168":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH1LExND43hDEwMLAwNLSwtLNmu2ECvOkszc1EwGAGROI2A%7C6408f7aa8650652c6a8974ad6998b539db109194.career/profile_photo/94413_1408009989",
            "expertises":["CRM Anwendungen", "Sales Expert" , "Value based Leadership"]
        },
        "329352":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH0jSwszAyOgVhNjc0sDc1NTNmu2ECvOkszc1EwGAIevI5Y%7C6b5bc011e9af0af70878b4ad19414ff78de82b3b.career/profile_photo/298602_1643790755",
            "expertises":["ARS" , "Neukundengewinnung"]
            
        },
        "84950":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH1zCwNTi3hDUyMLcyMzc1NzNmu2ECvOkszc1EwGAGVBI2k%7C8865efb6cfc8f6f072abe56f8c51738c13c36ba1.career/profile_photo/78058_1528726757",
            "expertises":["über 10 Jahre mit div. Vertriebsschulungen gefördert"]
        },
        "88090":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH0LAwtLk3hDcwNjA0MjQ2NTNmu2ECvOkszc1EwGAGOdI08%7Cc18a1ecfcc0e9bc99d96fc1fde9379c34715b64a.career/profile_photo/80894_1703012135",
            "expertises":["After Sales", "Vertriebsstrategie", "Kundenbeziehungsmanagement"]
        },
        "70794":{
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH0zUxMjy3hDEwMLAwMLI1MjNmu2ECvOkszc1EwGAGPAI1M%7C5eb88cc9eaa598d0b8e5e9579e0526038a62d5ad.career/profile_photo/65429_1408008252",
            "expertises":["Acquisitions" , "Branding","CRM", "Sales" ]
        }
        
    }
    project_logos = {
        "Beauty": "//blobs.experteer.com/blob/v1/eJwtjEELwiAYhncIaUH_IXYeNMeCoXjssPvoKl_LnLSpqA1Xfz4HHd7L8zy8u_03J4fg4Gm64uaEVx8xQ-S4rmJaKWIQOvANsz-j0sGiwsqGZISjdxhe0pm3frD0o70FlwQtrZYcEXTtyVFt4QKTykhuIYxdcRrMbEGvfDLS-HN94bhpcY1x21SIop7kQc1CZT_4bjRmd7b039f72ba5ca67bc4a91616d5a2a22c500361c.recruiting/company_logos/25_1481211840" }
    country = "DE"
    input_folder = "german_projects"  # Replace with the folder containing CSV files
    output_folder= "german_projects_finished"
    filter = False  # Only include "Sehr gut" and "Gut" candidates
    generate_emails(country, input_folder, output_folder, filter=filter, profile_photo=candidates_info, project_logos=project_logos)
    #clear_folder(input_folder)