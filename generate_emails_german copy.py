import csv
import os
import chardet
import re


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
    encoding = detect_file_encoding(csv_file)
    candidates = []
    
    with open(csv_file, 'r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file, delimiter="\t")  # Adjust delimiter if needed

        for row in csv_reader:
            eignung = row["Projekteignung"].strip()
            
            # Handle missing or false eignung cases
            if not eignung or eignung not in ["Sehr gut", "Gut", "Hervorragend"]:
                continue

            # Determine photo URL based on "Anrede"
            candidate_id = row["Mitglieds ID"]
            if candidate_id in special_logos and "url" in special_logos[candidate_id]:
                photo_url = special_logos[candidate_id]["url"]
            elif row["Anrede"] == "Herr":
                photo_url = "https://www.experteer.de/images/default_photos/male.png"
            elif row["Anrede"] == "Frau":
                photo_url = "https://www.experteer.de/images/default_photos/female.png"
            else:
                photo_url = "https://www.experteer.de/images/default_photos/female.png"

            # Include title in the candidate's name if present
            title = row["Titel"].strip()
            full_name = f"{title} {row['Vorname']} {row['Nachname']}".strip() if title else f"{row['Vorname']} {row['Nachname']}".strip()

            candidate = {
                "name": full_name,
                "id": row["Mitglieds ID"],
                "job_title": row['Aktuelle Position'],
                "company": row["Firma"],
                "industry": row["Branche"],
                "email": row["E-Mail"],
                "phone": row["Telefonnummer"],
                "photo_url": photo_url,
                "profile_url": row["URL Kandidatenprofil"],
                "eignung": eignung  # Can be None
            }
            candidates.append(candidate)
    
    eignung_ranking = {"Hervorragend": 1, "Sehr gut": 2, "Gut": 3}
    candidates.sort(key=lambda c: eignung_ranking.get(c["eignung"], float('inf')))


    
    return candidates



def generate_html(title, logo_url, job_id, expertise_dict, number_candidates, candidates, output_file):
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
    <title></title><!--[if !mso]><!-->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"><!--<![endif]-->
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
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
    </style><!--[if mso]>
<noscript>
<xml>
<o:OfficeDocumentSettings>
  <o:AllowPNG/>
  <o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings>
</xml>
</noscript>
<![endif]--><!--[if lte mso 11]>
<style type="text/css">
  .mj-outlook-group-fix {{ width:100% !important; }}
</style>
<![endif]--><!--[if !mso]><!-->
    <link href="https://fonts.googleapis.com/css?family=Lato:300,400,500,700" rel="stylesheet" type="text/css">
    <style type="text/css">
        @import url(https://fonts.googleapis.com/css?family=Lato:300,400,500,700);
    </style><!--<![endif]-->
    <style type="text/css">
        @media only screen and (min-width:480px) {{
            .mj-column-per-70 {{
                width: 70% !important;
                max-width: 70%;
            }}

            .mj-column-per-30 {{
                width: 30% !important;
                max-width: 30%;
            }}

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

            .mj-column-per-20 {{
                width: 20% !important;
                max-width: 20%;
            }}

            .mj-column-per-55 {{
                width: 55% !important;
                max-width: 55%;
            }}
        }}
    </style>
    <style media="screen and (min-width:480px)">
        .moz-text-html .mj-column-per-70 {{
            width: 70% !important;
            max-width: 70%;
        }}

        .moz-text-html .mj-column-per-30 {{
            width: 30% !important;
            max-width: 30%;
        }}

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

        .moz-text-html .mj-column-per-20 {{
            width: 20% !important;
            max-width: 20%;
        }}

        .moz-text-html .mj-column-per-55 {{
            width: 55% !important;
            max-width: 55%;
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
            background-color: white;
            margin: 0 auto !important;
            padding: 0 auto !important;
            height: 100% !important;
            width: 100% !important;
            -ms-text-size-adjust: 100%;
            -webkit-text-size-adjust: 100%;
        }}

        a {{
            color:
                #2c88de;
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

        table {{
            border-spacing: 0;
            border-collapse:
                collapse;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }}

        @media (prefers-color-scheme: dark) {{
            body {{
                background-color: #272623;
                color:
                    #f4f5f7;
                background-position: top center;
                background-repeat: no-repeat;
            }}

            .blue-bg {{
                background-color: #ecf3f9;
            }}

            .dark-bg {{
                background-color:
                    #484f59;
                color: #f4f5f7;
            }}

            .dark-img-wrapper,
            .dark-img {{
                display: block !important;
                width: auto !important;
                overflow: visible !important;
                float:
                    none !important;
                max-height: inherit !important;
                max-width: inherit !important;
                line-height: auto !important;
                margin-top: 0px !important;
                visibility: inherit !important;
            }}

            .white-bg {{
                background-color: #272623;
                color: #f4f5f7;
            }}

            p,
            ul,
            ol,
            li,
            div,
            span,
            b,
            td,
            .headline,
            .textcolor {{
                color: #f4f5f7;
            }}

            a,
            .link {{
                color: #91add4;
            }}
        }}
    </style>
    <meta name="color-scheme" content="light dark">
    <meta name="supported-color-schemes" content="light dark">
</head>

<body style="word-spacing:normal;">
    <div class="body">
        <!-- logo --><!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
        <div style="max-width:600px;margin:0 auto;">
            <table align="center" border="0" cellpadding="0" cellspacing="0"
                style="width:100%;border-collapse:collapse;">
                <tr>
                    <td style="padding:0;">
                        <table align="left" style="width:70%;border-collapse:collapse;">
                            <tr>
                                <td style="padding:18px 25px 5px 2px;">
                                    <div style="font-family:Lato;font-size:20px;line-height:24px;color:#3B414A;">
                                        Premium Recruitment Assistant
                                    </div>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding:5px 2px 0;">
                                    <div style="border-top:4px solid #B2CD0E;width:15%;"></div>
                                </td>
                            </tr>
                        </table>
                        <table align="right" style="width:30%;border-collapse:collapse;">
                            <tr>
                                <td style="padding:10px 25px 0;text-align:right;">
                                    <img src="https://jca.experteer.com/feed_manager/api/public/bkoleva/public_experteer_huntLogo_unblurred.svg"
                                        alt="Logo" style="width:120px;height:auto;border:0;display:block;" />
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </div>

        <!--[if mso | IE]></td></tr></table><![endif]--><!-- divider --><!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
        <div style="max-width:600px;margin:0 auto;">
            <table align="center" border="0" cellpadding="0" cellspacing="0"
                style="width:100%;border-collapse:collapse;">
                <tr>
                    <td align="center" style="padding:10px 25px;">
                        <table width="100%" border="0" cellpadding="0" cellspacing="0"
                            style="border-collapse:collapse;">
                            <tr>
                                <td style="border-top:2px solid #ecf0f3;line-height:0;font-size:0;">
                                    &nbsp;
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </div>

        <!--[if mso | IE]></td></tr></table><![endif]--><!-- static text --><!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
        <div style="margin: 0 auto; max-width: 600px; font-family: Lato, sans-serif; color: #3B414A;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                    <td style="padding: 10px 2px;">
                        <p>Sehr geehrte/r Herr/Frau xx,</p>
                        <p>Ihre Stellenanzeige <a href="https://www.experteer.de/career/positions/{job_id}"
                                style="font-weight: bold;">„{title}“</a> ist live auf Experteer.de – dem Karriereservice für Executives und
                            Senior Professionals.</p>
                        <p>Dazu liefert Ihnen unser Experteer Premium Recruitment Assistant heute <strong>als
                                Inklusivleistung zu Ihrer Stellenanzeige und ohne weitere verdeckte Kosten:</strong></p>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 2px;">
                        <strong>{number_candidates} ausgewählte Top-Kandidaten-Profile</strong>
                    </td>
                </tr>
                <tr>
                    <td align="center">
                        <table cellpadding="0" cellspacing="0" width="70%" style="border: none;">
                            <tr>
                                <td>
                                    <img src="https://links.experteer.com/custloads/766432948/md_1457741.png" width="18"
                                        height="18" style="vertical-align: middle;" />
                                    <strong>passend</strong> zu Ihrem Anforderungsprofil
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <img src="https://links.experteer.com/custloads/766432948/md_1457741.png" width="18"
                                        height="18" style="vertical-align: middle;" />
                                    <strong>interessiert</strong> an Ihrer Position
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <img src="https://links.experteer.com/custloads/766432948/md_1457741.png" width="18"
                                        height="18" style="vertical-align: middle;" />
                                    <strong>gesprächsbereit</strong> auf Ihre Ansprache
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 2px;">
                        Die Kandidaten warten auf Ihre Rückmeldung! <strong>Nehmen Sie jetzt Kontakt auf!</strong> –
                        direkt und kostenfrei mit den hier bereits angegebenen Kontaktdaten.
                    </td>
                </tr>
                <tr>
                    <td style="padding: 10px 2px;">
                        Für weitere Informationen zu unserem Service besuchen Sie <a
                            href="https://www.experteer.de/recruiting/page/products_premium_recruitment_assistant">www.experteer.de/Premium-Recruitment-Assistant</a>
                        oder nehmen Sie direkt <a style="text-decoration: none"
                            href="mailto:steven.franke@experteer.com">Kontakt zu uns</a> auf.
                    </td>
                </tr>

            </table>
        </div>


        <div style="margin:0 auto; max-width:600px; background-color:#f5f5f5; border-radius:5px 5px 0 0;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%"
                style="border-radius:5px 5px 0 0;">
                <tr>
                    <!-- Logo Section -->
                    <td align="center" width="20%" style="padding:10px;">
                        <img src="https://{logo_url}"
                            alt="Logo" style="display:block; width:72px; height:auto; border:0;" width="72">
                    </td>

                    <!-- Title Section -->
                    <td align="center" width="80%" style="padding:10px;">
                        <div
                            style="font-family:Lato, Arial, sans-serif; font-size:16px; line-height:24px; color:#3B414A; text-align:center;">
                            <strong>"{title}"</strong>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
    """
    candidate_template = """
           
        <!--[if mso | IE]><![endif]--><!--candidate 1 --><!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="dark-bg-outlook" style="width:600px;  background-color:#f5f5f5" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
        <div style="margin: 0 auto; max-width: 600px; background-color:#f5f5f5">
            <table align="center" border="0" cellpadding="0" cellspacing="0"
                style="width: 97%; background-color: white; border-radius: 4px;">
                <tr>
                    <!-- Contact Data-->
                <tr>
                    <td style="text-align: right; padding-top: 5px; padding-right: 5px;">
                        <table role="presentation" border="0" cellpadding="0" cellspacing="0"
                            style="width: auto; display: inline-block; font-family: Lato, sans-serif; font-size: 14px; color: #3B414A; line-height: 24px; white-space: nowrap;">
                            <tr>
                                <td style="padding-right: 15px; vertical-align: middle; white-space: nowrap;">
                                    <img src="https://jca.experteer.com/feed_manager/api/public/bkoleva/public_email.png"
                                        style="width: 18px; height: 18px; vertical-align: middle;" />
                                    <a href="mailto:{email}"
                                        style="text-decoration: none; color: #525b65; vertical-align: middle; padding-left: 5px;">{email}</a>
                                </td>
                                <td style="vertical-align: middle; white-space: nowrap;">
                                    <img src="https://jca.experteer.com/feed_manager/api/public/bkoleva/public_phone.png"
                                        style="width: 18px; height: 18px; vertical-align: middle;" />
                                    <a href="tel:{phone}"
                                        style="text-decoration: none; color: #525b65; vertical-align: middle; padding-left: 5px;">{phone}</a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>


                <!-- Profile Picture and View Profile -->
                <tr>
                    <td style="padding: 0px 5px 0px 5px">
                        <table width="97%" cellspacing="0" cellpadding="0">
                            <tr>
                                <!-- Profile Image -->
                                <td style="width: 25%; text-align: center; padding-right: 15px;">
                                    <img src={photo_url}
                                        alt="Profile Image" style="border-radius: 50%; width: 100%; height: auto;" />
                                </td>
                                <!-- User Details and View Profile -->
                                <td style="width: 70%; vertical-align: top;">
                                    <div
                                        style="font-family: Lato, Arial, sans-serif; font-size: 16px; color: #3B414A; margin-bottom: 5px;">
                                        <strong>{candidate_name}</strong>
                                    </div>
                                    <div
                                        style="font-family: Lato; font-size: 14px; color: #7D8996; margin-bottom: 5px;">
                                        <img src="https://links.experteer.com/custloads/766432948/md_1457745.png"
                                            style="width: 18px; height: 18px;" />
                                        {job_title}
                                    </div>
                                    <div
                                        style="font-family: Lato; font-size: 14px; color: #7D8996; margin-bottom: 5px;">
                                        <img src="https://links.experteer.com/custloads/766432948/md_1457742.png"
                                            style="width: 18px; height: 18px;" />
                                        {company} - {industry}
                                    </div>

                                    {expertise_list}

                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>

                <!-- View Profile Link -->
                <tr>
                    <td style="text-align: right; font-family: Lato; font-size: 14px; padding:0px 5px 10px 0px">
                        <a href={profile_url}
                            style="text-decoration: none;">Profil
                            ansehen</a>
                    </td>
                </tr>
            </table>
            <div style="margin:0px auto;border-radius:0 0 5px 5px;max-width:600px; background-color:#f5f5f5">
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
        </div>
    """
    end = """
 <!--[if mso | IE]></td></tr></table><![endif]--><!-- last text --><!--[if mso | IE]><table align="center" border="0" cellpadding="0" cellspacing="0" class="dark-bg-outlook" style="width:600px;" width="600" ><tr><td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;"><![endif]-->
        <div style="margin:0px auto;border-radius:0 0 5px 5px;max-width:600px; background-color:#f5f5f5">
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
        <div style="margin:0px auto;max-width:600px;">
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
                                                <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                                    width="100%">
                                                    <tbody>
                                                        <tr>
                                                            <td align="left"
                                                                style="font-size:0px;padding:10px 25px;padding-left:2px;word-break:break-word;">
                                                                <div
                                                                    style="font-family:Lato;font-size:14px;font-style:normal;line-height:24px;text-align:left;color:#3B414A;">
                                                                    Sie erreichen Ihren Experteer Business Partner
                                                                    Manager
                                                                    <a style="text-decoration: none"
                                                                        href="mailto:steven.franke@experteer.com">hier.</a>
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div><!--[if mso | IE]></td></tr></table><![endif]-->
                        </td>
                    </tr>
                </tbody>
            </table>
        </div><!--[if mso | IE]></td></tr></table><![endif]-->
    </div>
</body>

</html>"""

    # Generate expertise table rows
    def generate_expertise_rows(expertise_list):
        return "".join(f"""
            <div style="font-family: Lato; font-size: 14px; color: #525b65; border: 1px solid #525b65; border-radius: 50px; display: inline-block; padding: 2px 6px;">
                {expertise}
            </div>
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
    html_content = html_template.format(title=title,logo_url=logo_url,number_candidates=number_candidates, job_id=job_id)
    

    html_final = html_content + candidates_complete + end

    # Save the HTML to a file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_final)
    print(f"HTML file '{output_file}' has been generated successfully.")


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


def generate_german_emails(folder_path, output_folder, filter_eignung, special_logos, project_logos):
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
                company_logo_url = project_logos[title][1]
            else:
                print(f"Warning: No logo found for project '{title}'.")
                company_logo_url = "" # Replace with your actual default URL https://default-logo-url.com/default-logo.png

            if not os.path.exists(output_folder):
                os.mkdir(output_folder)

            sanitized_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            output_file_path = os.path.join(output_folder, f"{sanitized_title}.html")

            

            generate_html(
                title=title,
                logo_url=company_logo_url,
                expertise_dict=special_logos,
                number_candidates=len(candidates),
                candidates=candidates,
                output_file=output_file_path,
                job_id=project_logos[title][0],  
            )
            print(f"HTML file generated for project '{title}' at {output_file_path}")


if __name__ == "__main__":
    candidates_info = {
"194762": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1DczMzM8N4Q1MzExMjcwtDSzZrthArzpLM3NRMBgCHliOW476c81f13c0d429d4f00f2d7f34efedc53e6feb7.career/profile_photo/176661_1564427819"
  ,"expertises": ["DATEV", "MS-Office", "Rechnungslegung US-GAAP und HGB", "SAP R/3 FI", "CO", "MM", "PP", "SD"]
  },
"18203196": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DExMTYyMDw3hDc2MLU3NLA1NDNmu2ECvOkszc1EwGAMy0I-8%7Ce7312415148dec375cbe22d7823a8dbce7203697.career/profile_photo/14443201_1738579051"
  ,"expertises":["B2B Sales", "B2C Sales", "Budgetverantwortung", "CAD", "CRM", "Cross- und Upselling", "Einarbeitung neuer Mitarbeiter", "Gebietsführung", "Kundenbetreuung", "Orthopädie", "Produktschulungen", "Projektkoordination", "Projektmanagement", "Projektplanung"]
},
"17415496": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DYwsjI0MjQ6BmUxNDS2Mgl82aLcSKsyQzNzWTAQDMdCPs44e9eee996b095dd1461cbb05e8b65f1f450dab4.career/profile_photo/13822121_1654193382"
  ,"expertises":["CRM (Capsule)", "Excel", "MDG", "MS Office", "Microsoft 365", "Oracle", "PPT", "SAP", "Symbol", "Word"]

  },
  "17864214": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw7EKwjAQANAOEozgT3TQpWCPxgbj7NC9ezjkYg_aJl6jFP15ffA22692uywYYlceA95peb5QyFdCC39owtVDW6__VZofXjl1692e50zyxpELpxPmoSsPSWLgkXwaYo4nMGDPtm492ObSWGMA1FX1TmeeiIsfzYQj9Q%7C%7C62b07b9b2a88d102f9b50859af6776c2bdceb771.career/profile_photo/14175706_1739374411"
  ,"expertises":["CMS", "CRM", "Change Management", "Citrix", "Compliance Management", "Computer Science", "Confluence", "Consultancy", "Customer feedback", "CyberArk", "DB2", "Data recovery", "Debugging", "Desktop support", "Docker", "ERP", "EXCEL", "Engineering", "File system", "Finances", "Firewalls"]
  },
   "17748267": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DEwMLQ0NDS6BmSyNLUwNjUyM2a7YQK86SzNzUTAYAzPoj8Q%7C%7C67e2b92ea752d5d5d07941e555620c93e062c25f.career/profile_photo/14081119_1692950352"
  ,"expertises":["Automatisierung", "BMC Remedy", "Cisco", "Consulting", "DHCP", "DNS", "Dokumentationen", "Erneuerung", "Firewall", "Gas", "HP Server", "Hardware", "Hyper-V", "IPTV", "IT System", "IT-Infrastruktur", "KPI", "MS Active Directory", "McAfee", "Microsoft Windows Server", "Outsourcing", "Pflegen", "Projektmanagement", "Projektunterstützung", "Release Management", "SCCM", "SCOM", "Server Administrator"]

  },
  "12853407": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DAwMLA1MzQ6Bmc0NLcwtLC1M2a7YQK86SzNzUTAYAzZ4kAA%7C%7Ce0be8e1d7a2d6dc1507b86ab29d7e09e188e25c3.career/profile_photo/10080561_1671978985"
   ,"expertises":["Architect", "BIM", "Data Analyst", "Data Mining", "Data Visualization", "Microsoft Excel", "OLUWAROTIMI", "Programming", "R", "REVIT", "SQL", "Statistics", "Tableau", "Building Construction", "Design Patterns"]

   },
   "17836632":{
       "expertises":["Computer Services", "Data Visualisation", "ETL", "Economic", "Excel", "Geoscience", "Geosciences", "Investigation", "Machine Learning", "Microsoft Access", "Microsoft Excel", "Microsoft Office", "Modelling", "Operational Efficiency", "Power BI"]
   },
   "7941489": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH0zA0MDI0sjoF5DcwtDEzMzUzZrthArzpLM3NRMBgCphyO-723b2401d7d9a7d0673aac3f5f88698455d4e878.career/profile_photo/6010292_1617814665"
  ,"expertises":["BaFin", "Beschwerdemanagement", "Car sharing", "Car2go", "Claim Management", "Claims", "Claims Management", "Corporate Insurance", "Einkauf", "Englisch", "Fleet Insurance", "Fleet Management", "Flottenmanagement", "Flottenversicherung", "Free float car sharing", "Führungserfahrung", "Haftpflicht underwriter", "Handlungsvollmacht"]

  },
  "2874089": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH0jY1NLQ3PjeCA2N7KwtDQwYrNmC7HiLMnMTc1kAACq3yPL467f8620d9e221a59f0150efc094e5607d351861.career/profile_photo/2359173_1737289902"
   ,"expertises":["Bank/Investment", "Change management", "Coaching", "Entrepreneurism", "Insurance", "Leadership", "Motivation", "Operations management", "Process improvement", "Process optimizations", "Sales"]

  },
  "1939953": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1DMxNjQ0uTeEMTAwsDMzMjEws2a7YQK86SzNzUTAYAqeMjwA%7C%7Ca34dfe1cabac8151d9cbb80772607bbe73673d12.career/profile_photo/1643194_1408066248"
  ,"expertises":["Bewerbergespräche", "Vertriebsprozesse", "Führung", "Analysen und Massnahmenplanung", "Coaching", "Schulung", "Workshops"]

  },
  "12021667": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1LYxNDA0vDeENzYwszA2MzUwM2a7YQK86SzNzUTAYAqhcjvw%7C%7C63e31cc578166ca46957c340b6045b2618b39eef.career/profile_photo/9341091_1738603650"
  ,"expertises":["Haftpflichtrecht", "Schadenspezialist Industriehaftpflichtversicherung"]
},
"6082635":{
    "expertises": ["Capital Markets", "Company and Tax Law", "Compliance", "Leadership", "Management", "Private equity", "Project management", "Real estate"]

},
"11151231":{
    "expertises": ["Erfahrungen in Projektarbeit", "Mitarbeiterführung", "Mitarbeitercoaching", "Mitarbeitereinsatzplanung", "Mitarbeiterausbildung", "Organisation und Durchführung von Schulungen", "Personengroßschäden", "Referentin in Stabsfunktion", "Schadenbearbeitung", "Regulierungsaußendienst", "Gruppenleitung", "Schadenjuristin", "Schadensregulierung", "Versicherungsrecht", "Langjährige Erfahrung in der Versicherungsbranche"]

},
 "10939012": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH0LY3MDS2PTeEMTI1NDQwtjIxM2a7YQK86SzNzUTAYAqj4jvw%7C%7Ca26d001cca08e32dfa6141efc28dbda97ac88777.career/profile_photo/8370935_1425118324"
  ,"expertises": ["Controlling", "Einkauf", "Projektmanagement", "Prozessoptimierung"]
},
 "5324502": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH0TQ3NTExPzeENTcwsjYwNDYwM2a7YQK86SzNzUTAYAqfwjuw%7C%7C01b7e9abc19549e4c045b30cb1695a3555f1b527.career/profile_photo/4175447_1578230130"
  ,"expertises": ["Aufbau von zwei Sachversicherungszweigen", "Produktentwicklung", "Schaden", "Vertrieb"]
},
"14649309": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DQ3MTAyNLw3hDUxNzS0tTA2MDNmu2ECvOkszc1EwGAM0ZI_I%7Cc667cd8b9ad66d893bb985a072a0c69f19a9e302.career/profile_photo/11740291_1547995030"
  ,"expertises": ["Beratung", "Consulting", "Fachliche Leitung", "Gewerbliche Versicherungen", "Prozessoptimierung", "Underwriting", "Vergleichsrechnerentwicklung", "Vertrieb", "Liability Insurance"]
}



  
  
}
    project_logos = {
        "Berater Projektfinanzierung (m/w/d)": ["50150171", "//blobs.experteer.com/blob/v1/eJwtjL0OgjAYRRlMIya-BDNRfgLVNowO7MS1-cRaG6Ft2kpAX96SONzlnJO72X5jsvMWHrpNrpY7-eEjzCwvsjks5bPnyrMVN39GhYVJ-qXpg-GW3qB_Cavf6t6EH-UM2CBoapRgiKBLR_ZyDScYZERiA_7ZJgejnfRSK9br0YBa2KCFdsc8w9X5VLMcl3VZYFyViKKOxF6OXEY_MBw5Yw%7C%7C7b41fb60190bf1a2ffc9b2d8bd937bdd70afbbe1.recruiting/position_company_logos/1075986_1736327753"],
       "Bereichsleitung Schaden Außenregulierung (m/w/d)":["50457753","//blobs.experteer.com/blob/v1/eJwtjLEOgjAURRlMIyb-BK4kyhOJtmF0YCeuzRNqbYS2KZWA_rwlcbjLOSd3tf7GdOMdPkyV3JwY1Ef0OPEMDlNYKiYvtOcLLv-MSYej8nPZBCMcu2Pzks68dVuGHz1YdEGw1GrJCSXXmm7VEo7YqYjGFv2zSnaN6S3qmXdGmmF_BMiBZ0UOpzNcoCCM1DT2qhcq-gGVxTUOb555e4c737694225dbf9383506f6f76aaeaba075.recruiting/company_logos/32242_1642582926"],
       "IT-Spezialist für Server- und Rechenzentrumsinfrastruktur (m/w/d)":["50431109", "//blobs.experteer.com/blob/v1/eJwtjLEOgjAURRlMIyb-BDPRFiNoG0YHduLaPLHWRmibthLQn7ckDnc55-Su1t-UboKDh2myqxNefcQAEycFnuJyMQWhA19w_WdMOhhVmOsuGuHYDbqXdOat73X80d6Ci4LlVkuOKLq0dKuWcIReJTS1EJ5NtrPGq6CM5p0ZLOiZ90Yavye4KvGh5KQ6nIojweUZMdTSNKhBqOQHLqo5VA%7C%7Cd366cd84cd2ce568e63a5a123ca7ded7c256a557.recruiting/position_company_logos/1076036_1738251069"]
       }

    

    input_folder = "german_projects"  # Replace with the folder containing CSV files
    output_folder = "german_projects_finished"
    filter_eignung = True  # Only include "Sehr gut" and "Gut" candidates
    generate_german_emails(input_folder, output_folder, filter_eignung=filter_eignung, special_logos=candidates_info,
                           project_logos=project_logos)
    #clear_folder("german_projects_finished")
