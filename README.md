# Experteer - Instructions to Generate Emails

## Folder Setup
1. Save the `.csv` files for the relevant projects in the folder named after the nationality. For example:
   - If the project belongs to the German market, name the folder `german_projects`.
   - For the Italian market, name the folder `italian_projects`, and so on.

## File Setup
2. Go to the file `generate_emails.py`.

3. Complete the dictionary called `project_logos`. The key should be the project's name, and the value should correspond to the URL of the company's logo:
   ```python
   project_logos = {
       "Beauty": "//blobs.experteer.com/blob/v1/eJwtjEELwiAYhncIaUH_IXYeNMeCoXjssPvoKl_LnLSpqA1Xfz4HHd7L8zy8u_03J4fg4Gm64uaEVx8xQ-S4rmJaKWIQOvANsz-j0sGiwsqGZISjdxhe0pm3frD0o70FlwQtrZYcEXTtyVFt4QKTykhuIYxdcRrMbEGvfDLS-HN94bhpcY1x21SIop7kQc1CZT_4bjRmd7b039f72ba5ca67bc4a91616d5a2a22c500361c.recruiting/company_logos/25_1481211840"
   }
   ´´´

    

4. Complete the dictionary of dictionaries called candidates_info with the info of the candidates.
The key of each dictionary is the candidates' ID, "url" is the url of the candidate profile picture (only add it if the candidate added a profile photo), "expertises" is a list with the selected expertises of the candidate.

´´´python
candidates_info = {
    # Candidate with profile picture
        "106254" : {
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH1LcyMjs3hDUyMDUyNjEzNTNmu2ECvOkszc1EwGAGPyI1Y%7Cb2620e0586594bb457e00ccd130d39e17ed963f9.career/profile_photo/97226_1520523465"
            ,"expertises": ["Sales Promotion" , "Trade Marketing" , "Werbung"]
        },

    # Candidate without profile picture
        "401083":{
            "expertises":["SAP Gui & CRM", "Internationale Projekterfahrung"]   
        }
}´´´´

5. Select the country version:

German projects: country = "DE",
Italian projects: country = "IT"

6. Select the candidates filter:
filter = True # to select only the best candidates
filter = False # to select ALL candidates

7. Run main


In case of having to add countries modify the file methods.py

1. Add the country version in the method "read_html_template"


def read_html_template(country, file_part) -> str:
    
    if country == "DE":
        country_version = "german"
    elif country == "IT":
        country_version = "italian"
    else:
        return ""  

2. Add the name of the row for "project names" in the corresponding language in the method extract_project_name_from_csv

    for row in csv_reader:
                if country == "IT":
                    projektname = row["Nome del progetto"].strip()
                elif country == "DE":
                    projektname = row["Projektname"].strip()
                if projektname:  # Return the first non-empty project name
                        
                    
3. Changes in extract_candidates_from_csv
3.1 Redefine the rows' names in the corresponding language to extract the candidates data

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

3.2 Add the rating words in the corresponding language to the list "rate":

    with open(csv_file, 'r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file, delimiter="\t")  # Adjust delimiter if needed

        for row in csv_reader:
            # Apply filter on "Projekteignung" if specified
            if filter:
                rate = row[rating_row].strip()
                if rate not in ["Sehr gut","Gut","Buono", "Molto buono", "New rating word"]:
                    continue

3.3 Add the words for genders in the corresponding language:

            candidate_id = row[id_row]
            if candidate_id in profile_photo and "url" in profile_photo[candidate_id]:
                photo_url = profile_photo[candidate_id]["url"]
            elif row[gender] == "Herr" or "Signor" or "New word":
                photo_url = "https://www.experteer.de/images/default_photos/male.png"
            elif row[gender] == "Frau" or "Signora" or "New word":
                photo_url = "https://www.experteer.de/images/default_photos/female.png"
            else:
                photo_url = "https://www.experteer.de/images/default_photos/female.png"

4. Add the new country version to the method generate_emails

    if country == "IT":
            project_country = "italian"
        elif country == "DE":
            project_country = "german"