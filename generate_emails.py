from methods import detect_file_encoding, clear_folder, read_html_template, extract_project_name_from_csv, extract_candidates_from_csv, generate_html,generate_emails

def create_emails(country, filter_candidates):
    project_logos = {
        "Beauty": "//blobs.experteer.com/blob/v1/eJwtjEELwiAYhncIaUH_IXYeNMeCoXjssPvoKl_LnLSpqA1Xfz4HHd7L8zy8u_03J4fg4Gm64uaEVx8xQ-S4rmJaKWIQOvANsz-j0sGiwsqGZISjdxhe0pm3frD0o70FlwQtrZYcEXTtyVFt4QKTykhuIYxdcRrMbEGvfDLS-HN94bhpcY1x21SIop7kQc1CZT_4bjRmd7b039f72ba5ca67bc4a91616d5a2a22c500361c.recruiting/company_logos/25_1481211840" }
    
    candidates_info = {
        "106254" : {
            "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH1LcyMjs3hDUyMDUyNjEzNTNmu2ECvOkszc1EwGAGPyI1Y%7Cb2620e0586594bb457e00ccd130d39e17ed963f9.career/profile_photo/97226_1520523465"
            ,"expertises": ["Sales Promotion" , "Trade Marketing" , "Werbung"]
        }
      
    }
    
    generate_emails(country, filter=filter_candidates, profile_photo=candidates_info, project_logos=project_logos)
    

if __name__ == "__main__":
    country = "DE" # "DE" or "IT"
    filter_candidates = False # True: filter candidates / False: Include ALL candidates
    create_emails(country, filter_candidates)
    #clear_folder(input_folder)