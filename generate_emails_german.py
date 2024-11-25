import csv
import os
import chardet

def detect_file_encoding(file_path):
    """
    Detect the encoding of the given file.
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']


def extract_projektname_from_csv(csv_file):
    """
    Extract a single project name ('Projektname') from the given CSV file.

    :param csv_file: Path to the CSV file
    :return: The first encountered project name
    """
    # Detect the file encoding
    encoding = detect_file_encoding(csv_file)

    with open(csv_file, 'r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file, delimiter="\t")  # Adjust delimiter if needed

        for row in csv_reader:
            projektname = row["Projektname"].strip()
            if projektname:  # Return the first non-empty project name
                return projektname

    return None  # Return None if no project name is found

def extract_candidates_from_csv(csv_file, filter_eignung=None, special_logos=None):
    """
    Extract candidate data from a CSV file and return a list of dictionaries.

    :param csv_file: Path to the CSV file
    :param filter_eignung: Filter for "Projekteignung". If None, all candidates are included.
                           Example: "Gut" to include only candidates with "Projekteignung" == "Gut".
    :return: List of dictionaries containing candidate data
    """
    special_logos = special_logos or {}
    # Detect file encoding
    encoding = detect_file_encoding(csv_file)

    candidates = []
    with open(csv_file, 'r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file, delimiter="\t")  # Adjust delimiter if needed

        for row in csv_reader:
            # Apply filter on "Projekteignung" if specified
            if filter_eignung and row["Projekteignung"] != filter_eignung:
                continue

            # Determine photo URL based on "Anrede"
            candidate_id = row["Mitglieds ID"]
            if candidate_id in special_logos and "url" in special_logos[candidate_id]:
                photo_url = special_logos[candidate_id]["url"]
            if row["Anrede"] == "Herr":
                photo_url = "https://www.experteer.de/images/default_photos/male.png"
            elif row["Anrede"] == "Frau":
                photo_url = "https://www.experteer.de/images/default_photos/female.png"
            else:
                photo_url = "https://www.experteer.de/images/default_photos/female.png"

            # Extract relevant fields
            candidate = {
                "name": f"{row['Vorname']} {row['Nachname']}".strip(),
                "id": row["Mitglieds ID"],
                "job_title": f"{row['Aktuelle Position']}\n        bei {row['Firma']}".strip(),
                "company": row["Firma"],
                "industry": row["Branche"],
                "email": row["E-Mail"],
                "phone": row["Telefonnummer"],
                "photo_url": photo_url,
                "profile_url": row["URL Kandidatenprofil"],
            }
            candidates.append(candidate)

    return candidates

def generate_html(title, logo_url, expertise_dict, number_candidates, candidates, output_file):
    """
    Generate an HTML file for the provided candidate data.

    :param title: The title of the HTML document.
    :param logo_url: The URL of the logo to be included in the HTML.
    :param number_candidates: Number of candidates included in the HTML.
    :param candidates: List of dictionaries containing candidate data.
    :param output_file: The file path where the HTML will be saved.
    """
    # Base HTML template
    html_template = """
<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml"
      xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
      <title>{title}</title>
      <!--[if !mso]><!-->
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <!--<![endif]-->
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style type="text/css">
        #outlook a {{
          padding: 0;
        }}

        body {{
          margin: 0;
          padding: 0;
          -webkit-text-size-adjust: 100%;
          -ms-text-size-adjust: 100%;
        }}

        table,
        td {{
          border-collapse: collapse;
          mso-table-lspace: 0pt;
          mso-table-rspace: 0pt;
        }}

        img {{
          border: 0;
          height: auto;
          line-height: 100%;
          outline: none;
          text-decoration: none;
          -ms-interpolation-mode: bicubic;
        }}

        p {{
          display: block;
          margin: 13px 0;
        }}
      </style>
      <!--[if mso]>
            <noscript>
            <xml>
            <o:OfficeDocumentSettings>
              <o:AllowPNG/>
              <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
            </xml>
            </noscript>
            <![endif]-->
      <!--[if lte mso 11]>
            <style type="text/css">
              .mj-outlook-group-fix {{ width:100% !important; }}
            </style>
            <![endif]-->
      <!--[if !mso]><!-->
      <link href="https://fonts.googleapis.com/css?family=Lato:300,400,500,700" rel="stylesheet" type="text/css">
      <style type="text/css">
        @import url(https://fonts.googleapis.com/css?family=Lato:300,400,500,700);
      </style>
      <!--<![endif]-->
      <style type="text/css">
        @media only screen and (min-width:480px) {{
          .mj-column-per-100 {{
            width: 100% !important;
            max-width: 100%;
          }}

          .mj-column-per-17 {{
            width: 17% !important;
            max-width: 17%;
          }}

          .mj-column-per-80 {{
            width: 80% !important;
            max-width: 80%;
          }}

          .mj-column-per-25 {{
            width: 25% !important;
            max-width: 25%;
          }}

          .mj-column-per-55 {{
            width: 55% !important;
            max-width: 55%;
          }}

          .mj-column-per-20 {{
            width: 20% !important;
            max-width: 20%;
          }}
        }}
      </style>
      <style media="screen and (min-width:480px)">
        .moz-text-html .mj-column-per-100 {{
          width: 100% !important;
          max-width: 100%;
        }}

        .moz-text-html .mj-column-per-17 {{
          width: 17% !important;
          max-width: 17%;
        }}

        .moz-text-html .mj-column-per-80 {{
          width: 80% !important;
          max-width: 80%;
        }}

        .moz-text-html .mj-column-per-25 {{
          width: 25% !important;
          max-width: 25%;
        }}

        .moz-text-html .mj-column-per-55 {{
          width: 55% !important;
          max-width: 55%;
        }}

        .moz-text-html .mj-column-per-20 {{
          width: 20% !important;
          max-width: 20%;
        }}
      </style>
      <style type="text/css">
        @media only screen and (max-width:480px) {{
          table.mj-full-width-mobile {{
            width: 100% !important;
          }}

          td.mj-full-width-mobile {{
            width: auto !important;
          }}
        }}
      </style>
      <style type="text/css">
        :root {{
          color-scheme: light dark;
          supported-color-schemes: light dark;
        }}

        body {{
          background-color: #f4f5f7;
          margin: 0 auto !important;
          padding: 0 auto !important;
          height: 100% !important;
          width: 100% !important;
          -ms-text-size-adjust: 100%;
          -webkit-text-size-adjust: 100%;
        }}

        a {{
          color: #2c88de;
          text-decoration: none;
          padding: 0;
          margin: 0;
        }}

        table {{
          border-spacing: 0;
          border-collapse: collapse;
          mso-table-lspace: 0pt;
          mso-table-rspace: 0pt;
        }}

        .dark-bg {{
          background-color: #f4f5f7;
        }}

        .white-bg {{
          background-color: white;
        }}
        </style>
  <meta name="color-scheme" content="light dark" />
  <meta name="supported-color-schemes" content="light dark" />
</head>

<body style="word-spacing:normal;">
  <div class="body" style="">
    <div style="margin:0px auto;max-width:610px;background-color: white">
      <!-- logo -->
      <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
      <div style="margin:0px auto;max-width:600px;background-color: white;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:0;padding-left:2px;text-align:left;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:598px;" ><![endif]-->
                <div class="mj-column-per-100 mj-outlook-group-fix"
                  style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                    <tbody>
                      <tr>
                        <td style="vertical-align:top;padding-left:2px;">
                          <div
                            style="font-family:Lato;font-size: 20px;font-style:normal;padding-top: 18px;padding-bottom: 5px;text-align:left;">
                            Premium Recruitment Assistant
                          </div>
                          <p style="border-top: solid 2px #B2CD0E;font-size:1px;margin: 0px;width: 15%;"></p>
                        </td>
                        <td style="vertical-align:top;padding-left:2px;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                            <tbody>
                              <tr>
                                <td align="right"
                                  style="font-size:0px;padding:10px 25px;padding-left:2px;word-break:break-word;">
                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                    style="border-collapse:collapse;border-spacing:0px;">
                                    <tbody>
                                      <tr>
                                        <td style="width:120px;">
                                          <img height="auto" class="logo"
                                            src="https://jca.experteer.com/feed_manager/api/public/bkoleva/public_experteer_huntLogo_unblurred.svg"
                                            style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:14px;"
                                            width="120px" />
                                        </td>
                                      </tr>
                                    </tbody>
                                  </table>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!--[if mso | IE]></td></tr></table><![endif]-->
      <!-- divider -->
      <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
      <div style="margin:0px auto;max-width:600px;background-color: white;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:0;padding-left:2px;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:598px;" ><![endif]-->
                <div class="mj-column-per-100 mj-outlook-group-fix"
                  style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                    <tbody>
                      <tr>
                        <td style="vertical-align:top;padding:0;padding-left:2px;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                            <tbody>
                              <tr>
                                <td align="center"
                                  style="font-size:0px;padding:10px 25px;padding-left:2px;word-break:break-word;">
                                  <p style="border-top:solid 2px #ecf0f3;font-size:1px;margin:0px auto;width:100%;">
                                  </p>
                                  <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" style="border-top:solid 2px #ecf0f3;font-size:1px;margin:0px auto;width:569px;" role="presentation" width="569px" ><tr><td style="height:0;line-height:0;"> &nbsp;
</td></tr></table><![endif]-->
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!--[if mso | IE]></td></tr></table><![endif]-->
      <!-- static text -->
      <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
      <div style="margin:0px auto;max-width:600px;background-color: white;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:0;padding-left:2px;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:598px;" ><![endif]-->
                <div class="mj-column-per-100 mj-outlook-group-fix"
                  style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                    <tbody>
                      <tr>
                        <td style="vertical-align:top;padding-left:2px;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                            <tbody>
                              <tr>
                                <td align="left"
                                  style="font-size:0px;padding:0;padding-left:2px;word-break:break-word;">
                                  <div
                                    style="font-family:Lato;font-size:14px;font-style:normal;line-height:24px;text-align:left;color:#3B414A;">
                                    <strong>{number_candidates} Kandidaten, die Sie lieben werden:</strong>
                                  </div>
                                </td>
                              </tr>
                              <tr>
                                <td align="center"
                                  style="font-size:0px;padding:0;padding-left:2px;word-break:break-word;">
                                  <table cellpadding="0" cellspacing="0" width="70%" border="0"
                                    style="color:#3B414A;font-family:Lato;font-size:14px;line-height:24px;table-layout:auto;width:70%;border:none;">
                                    <tr align="left" style="display: flex; display: flex; align-items: center;">
                                      <td align="left" style="padding-right:1px;width:18px">
                                        <img style="width:18px; height:18px;margin-top: 6px;" width="18"
                                          src="https://links.experteer.com/custloads/766432948/md_1457741.png" />
                                      </td>
                                      <td text-align="left"><strong>passend</strong> zu Ihrem Anforderungsprofil </td>
                                    </tr>
                                    <tr align="left" style="display: flex; display: flex; align-items: center;">
                                      <td align="left" style="padding-right:1px;width:18px">
                                        <img style="width:18px; height:18px;margin-top: 6px;" width="18"
                                          src="https://links.experteer.com/custloads/766432948/md_1457741.png" />
                                      </td>
                                      <td text-align="left"><strong>interessiert</strong> an Ihrer Position</td>
                                    </tr>
                                    <tr align="left" style="display: flex; display: flex; align-items: center;">
                                      <td align="left" style="padding-right:1px;width:18px">
                                        <img style="width:18px; height:18px;margin-top: 6px;" width="18"
                                          src="https://links.experteer.com/custloads/766432948/md_1457741.png" />
                                      </td>
                                      <td text-align="left"><strong>gesprächsbereit</strong> auf Ihre Ansprache </td>
                                    </tr>
                                  </table>
                                </td>
                              </tr>
                              <tr>
                                <td align="left" style="font-size:0px;padding-left:2px;word-break:break-word;">
                                  <div
                                    style="font-family:Lato;font-size:14px;font-style:normal;line-height:24px;text-align:left;color:#3B414A;">
                                    Die Kandidaten warten auf Ihre Rückmeldung!<strong> Nehmen Sie jetzt Kontakt
                                      auf!</strong>
                                  </div>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!--[if mso | IE]></td></tr></table><![endif]-->
      <!-- table plus button -->
      <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="dark-bg-outlook" style="width:600px;" width="600" ><tr><td style="background-color:#f4f5f7;line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
      <div class="dark-bg" style="background-color: #f4f5f7; margin:0px auto;max-width:600px;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
          style="width:100%;border-radius:5px 5px 0 0;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:5px 0 0 0;padding-left:2px;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="dark-bg-outlook" style="background-color:#f4f5f7;vertical-align:middle;width:101.66px;" ><![endif]-->
                <div class="mj-column-per-17 mj-outlook-group-fix dark-bg"
                  style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                    <tbody>
                      <tr>
                        <td style="vertical-align:middle;padding-left:2px;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                            <tbody>
                              <tr>
                                <td align="center" class="light-mode"
                                  style="font-size:0px;padding:10px 25px;padding-left:2px;word-break:break-word;">
                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                    style="border-collapse:collapse;border-spacing:0px;">
                                    <tbody>
                                      <tr>
                                        <td style="width:72px;">
                                          <img height="auto"
                                            src="https:{logo_url}"
                                            style="border:0;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:14px;"
                                            width="72" />
                                        </td>
                                      </tr>
                                    </tbody>
                                  </table>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!--[if mso | IE]></td><td class="" style="vertical-align:middle;width:478.4px;" ><![endif]-->
                <div class="mj-column-per-80 mj-outlook-group-fix"
                  style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                    <tbody>
                      <tr>
                        <td style="vertical-align:middle;padding-left:2px;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                            <tbody>
                              <tr>
                                <td style="font-size:0px;padding:10px 25px;padding-left:45px;word-break:break-word;">
                                  <div
                                    style="font-family:Lato;font-size:16px;font-style:normal;line-height:24px;color:#3B414A;">
                                     <strong>"{title}"</strong> 
                                  </div>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!--[if mso | IE]></td></tr></table><![endif]-->
    """

    candidate_template = """
    <!-- candidate section -->
    <div class="dark-bg" style="background-color: #f4f5f7; margin:0px auto;max-width:600px;">
        <div style="margin:0px auto;max-width:600px;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                <tbody>
                    <tr>
                        <td style="direction:ltr;font-size:0px;padding:5px 10px 5px 10px;padding-left:10px;text-align:center;">
                            <div class="white-bg" style="margin:0px auto;border-radius:5px;max-width:580px;background-color: white">
                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;border-radius:5px;">
                                    <tbody>
                                        <tr>
                                            <td style="direction:ltr;font-size:0px;padding:5px 0 5px 0;padding-left:2px;text-align:center;">
                                                <div style="font-size:0px;text-align:right;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                                        <tbody>
                                                            <tr>
                                                                <td style="vertical-align:middle;padding:0;padding-left:2px; text-align: right;">
                                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                                        style="color:#525B65;font-family:Lato;font-size:14px;line-height:24px;table-layout:auto;width:100%;border:none;"
                                                                        width="100%">
                                                                        <tbody>
                                                                            <tr style="display: flex;align-items: self-start;justify-content: flex-end;">
                                                                                <td style="color:#b2cd0e;padding-top:5px; padding-right: 5px;width: 18px;">
                                                                                    <img style="width:18px; height:18px" width="18"
                                                                                        src="https://jca.experteer.com/feed_manager/api/public/bkoleva/public_email.png" />
                                                                                </td>
                                                                                <td style="padding-top:2px">
                                                                                    <a style="text-decoration:none;color:#525B65;font-family:Lato;font-size:14px;line-height:24px;"
                                                                                        href="mailto:{email}"> {email}</a>
                                                                                </td>
                                                                                <td style="color:#b2cd0e;padding-top:5px;padding-right: 5px;width: 18px;padding-left: 15px;">
                                                                                    <img style="width:18px; height:18px" width="18"
                                                                                        src="https://jca.experteer.com/feed_manager/api/public/bkoleva/public_phone.png" />
                                                                                </td>
                                                                                <td style="padding-top:2px; padding-right:10px;">
                                                                                    <a style="text-decoration:none;color:#525B65;font-family:Lato;font-size:14px;line-height:24px;"
                                                                                        href="tel:{phone}">{phone}</a>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>

                                                <div class="mj-column-per-25 mj-outlook-group-fix"
                                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                                        <tbody>
                                                            <tr>
                                                                <td style="vertical-align:top;padding-left:5px;">
                                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" style=""
                                                                        width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td align="center"
                                                                                    style="font-size:0px;padding:10px 25px;padding-left:2px;word-break:break-word;">
                                                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                                                        style="border-collapse:collapse;border-spacing:0px;">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td style="width:112px;">
                                                                                                    <img height="auto" src="{photo_url}"
                                                                                                        style="border:0;border-radius:50%;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:14px;"
                                                                                                        width="112" />
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>

                                                <div class="mj-column-per-55 mj-outlook-group-fix"
                                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:middle;width:100%;">
                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                                        <tbody>
                                                            <tr>
                                                                <td style="vertical-align:middle;padding:0;padding-left:2px;">
                                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" style=""
                                                                        width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="font-size:0px;padding:0 0 0 5px;padding-left:2px;word-break:break-word;">
                                                                                    <div style="font-family:Lato;font-size:16px;font-style:normal;line-height:24px;text-align:left;color:#3B414A;">
                                                                                        <strong>{candidate_name}</strong>
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="font-size:0px;padding:0;padding-left:2px;word-break:break-word;">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%" border="0"
                                                                                        style="color:#7D8996;font-family:Lato;font-size:14px;line-height:24px;table-layout:auto;width:100%;border:none;">
                                                                                        <tr style="display: flex;align-items: self-start;">
                                                                                            <td style="padding-top:5px; padding-right: 5px;width: 18px;">
                                                                                                <img style="width:18px; height:18px" width="18"
                                                                                                    src="https://links.experteer.com/custloads/766432948/md_1457745.png" />
                                                                                            </td>
                                                                                            <td style="padding-top:2px">{job_title}</td>
                                                                                        </tr>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="font-size:0px;padding:0;padding-left:2px;word-break:break-word;">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%" border="0"
                                                                                        style="color:#7D8996;font-family:Lato;font-size:14px;line-height:24px;table-layout:auto;width:100%;border:none;">
                                                                                        <tr style="display: flex;align-items: self-start;">
                                                                                            <td style="padding-top:5px; padding-right: 5px;width: 18px;">
                                                                                                <img style="width:18px; height:18px" width="18"
                                                                                                    src="https://links.experteer.com/custloads/766432948/md_1457742.png" />
                                                                                            </td>
                                                                                            <td style="padding-top:2px">{company} ({industry})</td>
                                                                                        </tr>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                            <tr><td align="left"
                                                                                    style="font-size:0px;padding-top:5px;padding-left:2px;word-break:break-word;">
                                                                                    <table cellpadding="0" cellspacing="0" width="100%" border="0"
                                                                                      style="color:#525B65;font-family:Lato;font-size:14px;line-height:24px;table-layout:auto;width:100%;border:none;">
                                                                                        <tr style="display: flex;align-items: center;justify-content: flex-start;column-gap: 4px;">
                                                                                          {expertise_list}
                                                                                      </tr>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>

                                                <div class="mj-column-per-20 mj-outlook-group-fix"
                                                    style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:bottom;width:100%;">
                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                                        <tbody>
                                                            <tr>
                                                                <td style="vertical-align:bottom;padding:0;padding-left:2px;">
                                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" style=""
                                                                        width="100%">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td align="left"
                                                                                    style="font-size:0px;padding:0;padding-left:2px;word-break:break-word;">
                                                                                    <div style="font-family:Lato;font-size:14px;font-style:normal;line-height:24px;text-align:center;color:#3B414A;">
                                                                                        <a href="{profile_url}">Profil ansehen</a>
                                                                                    </div>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </td>
                                                            </tr>
                                                        </tbody>
                                                    </table>
                                                </div>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    """
    end = """
<!-- last text -->
      <!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="dark-bg-outlook" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;background-color:#f4f5f7;"><![endif]-->
      <div class="dark-bg"
        style="background-color: #f4f5f7; margin:0px auto;border-radius:0 0 5px 5px;max-width:600px;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation"
          style="width:100%;border-radius:0 0 5px 5px;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:5px 0;padding-left:2px;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!--[if mso | IE]></td></tr></table><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
      <div style="background-color: white;margin:0px auto;max-width:600px;">
        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td style="direction:ltr;font-size:0px;padding:0;padding-left:2px;text-align:center;">
                <!--[if mso | IE]><table role="presentation" border="0" cellpadding="0" cellspacing="0"><tr><td class="" style="vertical-align:top;width:598px;" ><![endif]-->
                <div class="mj-column-per-100 mj-outlook-group-fix"
                  style="font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%;">
                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                    <tbody>
                      <tr>
                        <td style="vertical-align:top;padding-left:2px;">
                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                            <tbody>
                              <tr>
                                <td align="left"
                                  style="font-size:0px;padding:10px 25px;padding-left:2px;word-break:break-word;">
                                  <div
                                    style="font-family:Lato;font-size:14px;font-style:normal;line-height:24px;text-align:left;color:#3B414A;">
                                    Sie erreichen Ihren Experteer Business Partner Manager <a
                                      style="text-decoration:none;"
                                      href="mailto:robert.stolpa@experteer.com">hier.</a>
                                  </div>
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <!--[if mso | IE]></td></tr></table><![endif]-->
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

</body>

</html>"""

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
        #else:
        #    expertise_list_html = generate_expertise_rows(["No expertise listed"])

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

def generate_german_emails(folder_path, filter_eignung, special_logos, project_logos):
    """
    Process all CSV files in a folder, extract candidate data, and generate an HTML file for each.

    :param folder_path: Path to the folder containing CSV files.
    :param filter_eignung: Filter for "Valutazione del progetto". If None, all candidates are included.
    :param special_logos: A dictionary mapping candidate IDs to special logo URLs.
    :param project_logos: A dictionary mapping project names to their company logo URLs.
    """
    special_logos = special_logos or {}
    project_logos = project_logos or {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            csv_file = os.path.join(folder_path, file_name)
            title = extract_projektname_from_csv(csv_file)

            if not title:
                print(f"Skipping file {csv_file}: No project name found.")
                continue

            candidates = extract_candidates_from_csv(
                csv_file, filter_eignung=filter_eignung, special_logos=special_logos
            )

            # Check if the title exists in project_logos
            if title in project_logos.keys():
                company_logo_url = project_logos[title]
            else:
                print(f"Warning: No logo found for project '{title}'.")
                company_logo_url = "https://default-logo-url.com/default-logo.png"  # Replace with your actual default URL

            output_file_path = os.path.join(
                folder_path, f"{title.replace(' ', '_').replace(':', '_').replace('-', '_')}.html"
            )

            generate_html(
                title=title,
                logo_url=company_logo_url,
                expertise_dict=special_logos,
                number_candidates=len(candidates),
                candidates=candidates,
                output_file=output_file_path
            )
            print(f"HTML file generated for project '{title}' at {output_file_path}")


if __name__ == "__main__":
    candidates_info = {
        "8586574": {
          "url":"https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1zAyMLYxPDeENTMyNzY0szQwM2a7YQK86SzNzUTAYAqecjvg%7C%7C09687101358c4398938549f20e2025174dd09fc5.career/profile_photo/7028341_1562739610",
          "expertises": ["CAD", "Personal"]
        }
    }
    project_logos = {
        "title": "url"
    }
    input_folder = "german_projects"  # Replace with the folder containing CSV files
    filter_eignung = "Gut"  # Change to None if you want all candidates
    generate_german_emails(input_folder, filter_eignung=filter_eignung, special_logos=candidates_info, project_logos=project_logos)