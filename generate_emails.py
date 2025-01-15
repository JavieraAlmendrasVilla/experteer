from methods import generate_emails

def create_emails(country, filter_candidates):
    project_logos = {
        "Abteilungsleiter Elektro-/MSR-Technik (m/w/d)": "//blobs.experteer.com/blob/v1/eJwtjLEKwjAURR0kWMGf6Fy0qWggoaND9-IanjXGh20Sklha_XlTcLhwOedy15tvxrfRw8M2-dWrgB81wCRpVU4phZqiMlEuuP4zoT2MGOe6S0Z5cYPupb19m3udfkxw4JMQhTNaEk4uLd_hMhyhxxXPHMRnk--dDRjRGtnZwYGZZW-1DQdaMspYJen5xFJn1ZEI0vIs4qBw9QMuuTlT469416f975e73a42aafe2e3fadcf737fa38c86fe.recruiting/position_company_logos/1071772_1657107723",
       }
    
    candidates_info = {
    "13611564": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw0ELgjAUAGAPMVzQn_BQF6ENcZPXuYN37-MRb_lA3ZozpP58ffAdyq-EY07oQ19dPD5ofW2YyNWJVv7QjLvTRu3_dVyeToC4D3DiJVN648QFyIh57KtzTMHzRC6OIYerVtbarmmdtsqoplPGiJsYQGaeiYsfzdkj-Q%7C%7C97a75c282379b0e912d9902e3521a9c28eafe9be.career/profile_photo/10777835_1706038066"
  , "expertises":["Electric Drive Train" , " SMPS Design"]},
  "306709":{
      "expertises":["Gehaltverhandlungen"]
  },
  "4493396":{
      "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1jUzNjU2OTeEMTAwsTA0tjEwM2a7YQK86SzNzUTAYAqcUjuw%7C%7Cdd0fed2c30e9024b205e005e9fceedab692cb2c9.career/profile_photo/3563534_1408409340",
      "expertises":["Produktlebenszyklusmanagement "]
  },
  "2056442": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1DcxMDY0uTeEMTcyMjA0MDI1M2a7YQK86SzNzUTAYAqQojsQ%7C%7C7e6694c25f4ed2baaa524cd23da04d532e0cba02.career/profile_photo/1740394_1472201025",
    "expertises":["Lean Management"]
  },
  "1303717": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw7EKwjAQANAOEozgTxTEpWAOQo1xdujePRxysQdtE69Riv68Pnib7Vf7XRGMqauPEe-0PF8oFBqhhT804RqgNet_k-dHUF7der_nuZC8ceTK64xl6OpDlhR5pJCHVNIJAMzF2QDWOGNbdzbqqnqvC0_E1Q-pXiO721f18d929ced60e5da5fb319d009fcefcd470069.career/profile_photo/1110984_1408046870"
  , "expertises":["Qualitätsmanagement "]},
  "1447673": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1DI2NDY0uLeEMTAwsDUwMzE0s2a7YQK86SzNzUTAYAqYkjvQ%7C%7Ca58cfbfb1ed00744e293004102b79ee89dcff548.career/profile_photo/1231398_1408050649"
  , "expertises":[" Automatisierungstechnik" , "Änderungsmanagement "]},
  "17966046":{
      "expertises":["Lean management" , "Mitarbeiterführung"]
  },
  "16516752": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DYyNzM2MDE6BmQwNLU0szA1M2a7YQK86SzNzUTAYAzPwj8g%7C%7C100438c09ee2eddafee919be12b78e723a143470.career/profile_photo/13276304_1610959605"
  , "expertises":["Diesel engines maintenance"]}
  
}

    
    generate_emails(country, filter=filter_candidates, profile_photo=candidates_info, project_logos=project_logos)
    

if __name__ == "__main__":
    country = "DE" # "DE" or "IT"
    filter_candidates = True # True: filter candidates / False: Include ALL candidates
    create_emails(country, filter_candidates)
    #clear_folder(input_folder)