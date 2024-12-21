from methods import detect_file_encoding, clear_folder, read_html_template, extract_project_name_from_csv, extract_candidates_from_csv, generate_html,generate_emails

def create_emails(country, filter_candidates):
    project_logos = {
        "Beauty": "//blobs.experteer.com/blob/v1/eJwtjEELwiAYhncIaUH_IXYeNMeCoXjssPvoKl_LnLSpqA1Xfz4HHd7L8zy8u_03J4fg4Gm64uaEVx8xQ-S4rmJaKWIQOvANsz-j0sGiwsqGZISjdxhe0pm3frD0o70FlwQtrZYcEXTtyVFt4QKTykhuIYxdcRrMbEGvfDLS-HN94bhpcY1x21SIop7kQc1CZT_4bjRmd7b039f72ba5ca67bc4a91616d5a2a22c500361c.recruiting/company_logos/25_1481211840" }
    
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
    
    generate_emails(country, filter=filter_candidates, profile_photo=candidates_info, project_logos=project_logos)
    

if __name__ == "__main__":
    country = "IT" # "DE" or "IT"
    filter_candidates = True # True: filter candidates / False: Include ALL candidates
    create_emails(country, filter_candidates)
    #clear_folder(input_folder)