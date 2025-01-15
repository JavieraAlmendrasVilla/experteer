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

def read_html_template(country) -> str:
    
    path_html_files = Path(__file__).parent.resolve() / "html_files"

    if country == "DE":
        country_version = "german"
        file_name = f"template_{country_version}.html"
    elif country == "IT":
        country_version = "italian"
        file_name = f"template_{country_version}.html"
    else:
        return ""  # Ungültiger Ländercode


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
                if rate not in ["Hervorragend","Sehr gut","Gut","Buono", "Molto buono"]:
                    continue

            # Determine photo URL based on "Anrede"
            candidate_id = row[id_row]
            if candidate_id in profile_photo and "url" in profile_photo[candidate_id]:
                photo_url = profile_photo[candidate_id]["url"]
            # Handle gender-based default logic
            elif row[gender].strip().lower() in ["herr", "signor"]:
                photo_url = "https://www.experteer.de/images/default_photos/male.png"
            elif row[gender].strip().lower() in ["frau", "signora"]:
                photo_url = "https://www.experteer.de/images/default_photos/female.png"
            # Fallback for unexpected or missing gender values
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
    
    html_template = read_html_template(country)
    
    
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

def generate_emails(country, filter, profile_photo, project_logos):
    
    profile_photo = profile_photo or {}
    project_logos = project_logos or {}

    if country == "IT":
        project_country = "italian"
    elif country == "DE":
        project_country = "german"

    folder_path = f"{project_country}_projects"  # Replace with the folder containing CSV files
    output_folder= f"{project_country}_projects_finished"

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