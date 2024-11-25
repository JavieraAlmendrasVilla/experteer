from generate_emails_italian import generate_italian_emails
from generate_emails_german import generate_german_emails



def main(language, candidates_info, project_logos):
    
    
    if language == "IT":
        filter_candidates = "Buono"
        folder = "italian_projects"
        generate_italian_emails(folder, filter_candidates,special_logos=candidates_info, project_logos=project_logos)
    elif language == "DE":
        filter_candidates = "Gut"
        folder = "german_projects"
        generate_german_emails(folder, filter_candidates,special_logos=candidates_info, project_logos=project_logos)
   


if __name__ == "__main__":

    # Languages "IT": italian, "DE": german

    language = "IT", 
    
    candidates_info = {
            "9321920": {
            "url":"https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1zAyMLYxPDeENTMyNzY0szQwM2a7YQK86SzNzUTAYAqecjvg%7C%7C09687101358c4398938549f20e2025174dd09fc5.career/profile_photo/7028341_1562739610",
            "expertises": ["Consulenza"]
            },
            "16461372": {
                "expertises":["AS400"]
            },
            "4699626": {
                "expertises": ["3D modelling"]
            },
            "7397497": {
                "expertises": ["plasturgia"]
            },
            "778278": {
                "expertises": ["creazione e gestione di DataBase Oracle"]
            },
            "7533174": {
                "expertises": [".net framework c#"]
            },
            "17912780": {
                "expertises": ["developer"]
            }

        }
        
    project_logos ={
            "Scada Engineer" : "//blobs.experteer.com/blob/v1/eJwtjLEOgjAURRkMERN_gpkoJSFAG0YHduLaPLHWF6Ft2kpAf96SONzlnJO7238TevAWHrpLr1Y4_IgJFk6KfAnLxOKF8nzD7Z8xaWFGv7ZDMMKyGwwvafVb3dvwo5wBGwTLjJI8pvGlp0fcwhlGjGhiwD-79GS0Q49a8UFPBtTKRy21O5O8Kqu65qQq6rIkTZPHLO5p4nESGP0AMFA5Zg%7C%7C4857cb02d009e02c75cdb39e59b40dab6cb0dae9.recruiting/position_company_logos/1075788_1728551990",
           # "Immobilienvermarktung": "//blobs.experteer.com/blob/v1/eJwtjLEOgjAURRkMERN_gpkoJSFAG0YHduLaPLHWF6Ft2kpAf96SONzlnJO7238TevAWHrpLr1Y4_IgJFk6KfAnLxOKF8nzD7Z8xaWFGv7ZDMMKyGwwvafVb3dvwo5wBGwTLjJI8pvGlp0fcwhlGjGhiwD-79GS0Q49a8UFPBtTKRy21O5O8Kqu65qQq6rIkTZPHLO5p4nESGP0AMFA5Zg%7C%7C4857cb02d009e02c75cdb39e59b40dab6cb0dae9.recruiting/position_company_logos/1075788_1728551990", 
        }
    
    main(
        language = language, 
        candidates_info= candidates_info,
        project_logos=project_logos,
        )
