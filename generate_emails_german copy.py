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
    # Detect file encoding
    encoding = detect_file_encoding(csv_file)

    candidates = []
    with open(csv_file, 'r', encoding=encoding) as file:
        csv_reader = csv.DictReader(file, delimiter="\t")  # Adjust delimiter if needed

        for row in csv_reader:
            # Apply filter on "Projekteignung" if specified
            if filter_eignung:
                eignung = row["Projekteignung"].strip()
                if eignung not in ["Sehr gut", "Gut", "Hervorragend"]:
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

            # Include the title in the candidate's name if present
            title = row["Titel"].strip()
            full_name = f"{title} {row['Vorname']} {row['Nachname']}".strip() if title else f"{row['Vorname']} {row['Nachname']}".strip()

            # Extract relevant fields
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
                "eignung": eignung
            }
            candidates.append(candidate)
    eignung_ranking = {"Hervorragend": 1, "Sehr gut": 2, "Gut": 3}
    candidates.sort(key=lambda c: eignung_ranking[c["eignung"]])
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
"2365080": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1DSwtjY2PTeEMTSwNDI2NDUzM2a7YQK86SzNzUTAYAqf8jvQ%7C%7C51bf1be381ca1133776ccfbf60f5a5a0eebfc9ac.career/profile_photo/1983335_1490123156"
  ,"expertises":["CANADIAN GAAP", "IPSAS/ UNSAS", "MICROSOFT OFFICE SUITE", "ORACLE ERP", "SAP ERP ECC 6.0", "US GAAP"]
},
"18088047": {
    "expertises":["Total Quality Management", "US GAAP", "USGAAP", "IFRS", "Import-Export"]
},
"18148330":{
    "expertises":[
     "Caseware", "Customer Centricity", 
    "Data Classification", "Economic", "Entrepreneurial mindset", "Financials", 
    "Food & Beverage", "HACCP", "International Financial Reporting Standards (IFRS)", 
    "Legislation", "Management Accounting"
]

},
"14182188": {
 "expertises":["Accounting", "Finance"]
},
"18003606":{
    "expertises":["Front Office", "Operations"]

},
"6978295": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1TYxMjEwuDeENzYwsLCwMLM0M2a7YQK86SzNzUTAYAqqYjyQ%7C%7C5028c3807eb95fc03b5f9767ab01d4092960ff0e.career/profile_photo/5342480_1738880861"
 , "expertises":[
    "Business Management", "Business Administration", "Computer Science", 
    "Excel", "Fidelio", "Front Office", "Hospitality Management", 
    "Information Technology", "Leadership", "MS Office", "Mirus", 
    "Operations Management", "Sales", "Workflow", "Planning"
]
 },
 "6377928":{
     "expertises":[
    "Konzernsteuerrecht", "Leitung Steuerabteilung", "Personalführung", 
    "Tax Compliance", "Transfer Pricing"
]
 },
 "11071585": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH0LE0tjQ2OLeENTYzNzUzMLUxM2a7YQK86SzNzUTAYAq50j0w%7C%7Cc856af71b2bda694dbd95f3fa21634f2ac2a4380.career/profile_photo/8493138_1536756854"
  , "expertises":[
    "Addison", "Concur", "DATEV", "Datenbanken", "Excel", "IFRS", 
    "Lexware", "Office", "Outlook", "SAP FI/CO", "Word"
]
},
"15385492": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DI2NLI0NL03hDU3MzA1NzCwNTNmu2ECvOkszc1EwGAM29I_o%7C65b8998f804dedc55ce1eca6475bf4a733cb895e.career/profile_photo/12392195_1576057805"
  , "expertises":[
    "Projektleitung", "Projektmanagement"
]

  },
  "4713016": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1jcyMzI1OzeEMTAwsTQ1MLIyM2a7YQK86SzNzUTAYAqg4jvw%7C%7Cbf534b06466a73b007595871068d5ff838d71473.career/profile_photo/3726256_1408415822"
 , "expertises":[
    "Corporate Tax", "Wealth Management"
]
   },
   "14514906": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw7EKwjAQANAOEozgT3TQpWCOQKPn7NC9ezjkYg_aJqZRiv68Pnib7VfjrmQKsauPge68PF-U2TeZF_nwRKuH1qz_TZofXqG69biXuXB-0ygV6kRl6OpDyjHIyD4NscQTQGsNXIwHZ8_GWQdGXVWPusjEUv0AzEAj6A%7C%7C412dfeeabef710dddab30eced54cba0fd8300bb5.career/profile_photo/11630190_1738073710"
  , "expertises":[
    "Active Sourcing", "Business Development", "Führungserfahrung", 
    "Key Account Management", "Personalverantwortung", "Transaktionsanalyse"
]
},
"1401302": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw7EKwjAQANAOEozgTxTEpaBJIGKcHbp3Pw652IO2idcoRX_ePnib7U-HXRGMqa2PER80v94oBI3QzF8acQHjz8u6ydMTVFD3Lux5KiQfHLgKOmPp2_qQJUUeCHKfSjoZc7XeWTAX593aOnVTXdCFR-LqD6nKI74%7C08741fe34da2a7138dcef998c52d808f6b161d60.career/profile_photo/1192632_1736373623"
  , "expertises":[
    "Berichtswesen", "Bilanzierung nach HGB, IFRS und US GAAP", 
    "Business Model unter verschiedenen Szenarien", "Business Planung einschließlich Top-down / Bottom-up Planung", 
    "Financial Due Diligence", "Financial und Business Analysis", "Forecasting und rollierendes Forecasting", 
    "Prozessbeschreibungen/Prozessoptimierung", "fachliche und disziplinarische Führung"
]

  },
   "114427": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1DAxMzS8t4Q3NjSyMDczMLAzZrthArzpLM3NRMBgCHfSOU20e0ffa6aca535f4ee6a6626d63b285bde38d23c.career/profile_photo/104699_1739207680"
   , "expertises":[
    "Anlagebuchhaltung", "BaFin", "Bankbuchhaltung", "Business Development", 
    "Change Management", "Controlling", "Debitoren- und Kreditorenbuchhaltung", 
    "Finanzbuchhaltung", "Geldwäscheprävention", "HGB & IFRS - abschlusssicher"
]

   },
   "10377868": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1zCzNjC3PTeEMTAwtTEyNjYxM2a7YQK86SzNzUTAYAq2ojyw%7C%7C85673d477173291a7541be8f778a9e4593a07cae.career/profile_photo/7863875_1408542334"
 , "expertises": [
    "Kaufmännische Leitung", "SAP R/3 (FI und CO)", "Vertriebscontrolling"
]
},
"18749":{
    "expertises":[
    "Treasury", "Systeme", "Organisation", "Führung"
]
},
"95438": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH0LcxMT03hDUyMzE1Nzc3MjNmu2ECvOkszc1EwGAGULI2U%7Ce6f6f65a0ffbcd36d45bec9c5d069c40a6834ec6.career/profile_photo/87445_1526457772"
   , "expertises":[
    "Einführung bzw. Aufbau eines Berichtswesens (mehrfach)", 
    "Erstellung eines Sanierungskonzeptes mit PeWeCo", 
    "Neugestaltung der Kalkulation", 
    "Weiterentwicklung des Projektcontrollings", 
    "Zur Zeit Optimierung der vorhandenen SAP-Systeme"
]

   },
   "18168647":{
        "expertises":[
    "Engineering Management", "Enterprise Resource Planning", "Excel", "Excel-VBA", 
    "Export", "FMEA", "Financial Management", "Finite Element", "Geschäftsabläufe", 
    "Gesetze", "IFRS", "ISO 13485", "ISO 9000", "ISO 9001", "IT-Kenntnisse", 
    "International Financial Reporting Standards", "International Sales", "Internationales Management"
]

   },
    "12958943": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DA0MLA1Mz43hDE3Njc0MzIzNLNmu2ECvOkszc1EwGAMzsI_Q%7Cc7682937355bbb005656e996bf377da1f93e895e.career/profile_photo/10180563_1473716269"
  , "expertises":[
    "Controlling", "Data Modeling", "MaRisk", "Projektleitung", 
    "Prozessentwicklung", "Regulatorik & Recht", "Restrukturierung von Abteilungen/Bereichen", 
    "Risikomanagement", "Sehr gute Kenntnisse im Bereich Finanzierungen (Konsumentenkredite, Baufinanzierungen, Autokredite)"
]

  },
  "6446429": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH0TS3MTS0sDoF5zEzMDAwtTCzZrthArzpLM3NRMBgCr6yPUcaabfd9e12191ff0eaa53e69cd72110dc2b2241c.career/profile_photo/4974990_1674600858"
  , "expertises":[
    "(Inter-)Nationale Bankenaufsicht", "Kredit- und Handelsgeschäft", 
    "MaRisk", "Risikocontrolling"
]

  },
  "16680685":{
      "expertises":[
    "Absolute Zahlenaffinität", "Pricing & Revenuemanagement"
]

  },
  "6057": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWlgqL8tMyc1PiCjPySfH1TM0vzeENzY0tDSyNLc2M2a7YQK86SzNzUTAYAQtYjOA%7C%7Cc529b20f75ec0b407c482a998df2663167fb0266.career/profile_photo/5697_1739192973"
  ,"expertises":[
    "Fernstudium 'Masterconsultant in Finance®' (MFC®) Internationaler Abschluss im Finanzdienstleistungsbereich", 
    "Depot A bei Eigenanlage Bank - Treasury - DZ-Bank", 
    "Wertpapieranalyse bei ADG Montabaur", 
    "Steuerseminar bei ADG Rendsburg", 
    "Qualifizierte Vermögensberatung bei ADG Rendsburg"
]

  },
  "17052865": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DY1MLcxNTA6BmIxNTQwtzQwM2a7YQK86SzNzUTAYAzWEj8g%7C%7Cd901f3a61ea997fe0a45a357c6cd9583e89f14ee.career/profile_photo/13587450_1624518710"
   ,"expertises":[
    "Aktienhandel", "Asset Allocation", "Bloomberg", "Derivatehandel", 
    "Eurex GUI", "FrontArena", "Kryptowährungen", "Microsoft Office", 
    "Murex", "Portfoliomanagement", "Private Equity", "Real Estate", 
    "Relationship Management", "Reuters", "SSEOMS", "Technische Analyse", 
    "Vermögensberatung", "Vermögensverwaltung", "Xetra GUI"
]

   },
    "327128": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH0jSzMzQ6N4Q3MDcwtDM2NjIzZrthArzpLM3NRMBgCHDiOM02315d2dc7f155fb752b2b4cd7beb2f0fc358dd3.career/profile_photo/296612_1707816332"
  ,"expertises":[
    "Berufsexamen zum Internen Revisor (DIIR)", "Interne/externe Revision", 
    "HGB/IFRS-Kenntnisse", "Kreditanalyse", "NPL-Workout", "Kreditrisikomanagement"
]

  },
  "15267725": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DIyMLc0sLS6BmE3MzQ0sTC2M2a7YQK86SzNzUTAYAz3AkDQ%7C%7Cbdf3969dd20914f2d9a186dd1fdaf3abde874d74.career/profile_photo/12287989_1647619483"
  ,"expertises":[
    "Banking & Financial Services", "Budgetplanung und -controlling", 
    "Budgets and Forecasts", "Business Process Analysis", "Business Strategy", 
    "Business Development", "Customer Relationship Management", "Financial Analysis", 
    "Finanzdienstleitung Financial Services", "Intercorporate Relationships", 
    "Interkulturelle Erfahrung und Kompetenz"
]

  },
   "10336918": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1zCyMzC3ODeEMTA0tTIDAwYLNmC7HiLMnMTc1kAACq5yPFfe39238696a4379eb260a29ec994b0bdfac9fef1.career/profile_photo/7826870_1409555500"
  ,"expertises":[
    "Accounting", "Außenhandel", "Beteiligungscontrolling", "Beteiligungsmanagement", 
    "Betriebswirtschaftliche Beratung", "Buchhaltung", "Budget", "Budgets", 
    "Controlling", "Controlling-Instrumente", "DATEV", "Due Diligences", 
    "Due-Diligence", "ERP-Software", "Einführung von ERP-Systemen", "Erstellung von Jahresabschlüssen", 
    "Excel", "Financial Management"
]

  },
  "110679": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1DA0MjC_N4QxMzc0MTQ3MjSzZrthArzpLM3NRMBgCGVCOJa0dc9fd42c6d18ae4b35575833fc579f72921c3d.career/profile_photo/101287_1467141729"
   ,"expertises":[
    "MaRisk", "Steuerung und Führung von Vertriebsteams"
]
},
"17934660": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw70KwjAQAOAOEozgS3TQpWDOnwTi7NC9-3HIxR60TUyjFH15_eBbrb_ab0qmENt6H-jO8_NFmbHJPMuHR1oQrFn-mzQ9UHl16_xWpsL5TYNUXicqfVvvUo5BBsbUxxIPcD6ewBlAcGCssxcAdVWd10VGluoHy98j5A%7C%7Cc49ef72fbcc9ee8e147f545bf4d3ee6b3c3517da.career/profile_photo/14231701_1710676511"
  ,"expertises":[
    "Asset Management", "Due Diligence", "Facility Services", "Fondsmanagement", 
    "Immobilien", "Microsoft Office", "Monte-Carlo", "Real Estate", "Risikoanalyse", 
    "Risikoberichterstattung", "Risikocontrolling", "Risikomanagement", "Simulation", 
    "Unternehmensbewertung", "Visual Basic", "Wirtschaftswissenschaften", "Wirtschaftlicher"
]

  },
  "17563504":{
    "expertises":  [
    "Beratung", "Change Management", "Compliance", "CRM", 
    "Key Account Management", "Know Your Customer (KYC)", "Projektmanagement", "SAP"
]

  },
  "13284497": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw0ELgjAUAGAPMVzQn_BQF6E9UJfr3MG79_GIt3ygbs4ZUn--PvgO-VeaY4rofFdcHD5pXTaMZMtIK39owt1Co_b_MswvK4x49ObEc6L4xpEzIwOmoSvOIXrHI9kw-OSvoCpdtxos1FWjWgB9E3fRG5l4Is5-zb0j-g%7C%7Ce3b1c4f6b07ba67eb01d18ac32a0a733136d9557.career/profile_photo/10475971_1546091178"
  , "expertises":[
    "Accounting", "Arbeitssicherheit", "Banking", "Beratung", "Betriebswirtschaft", 
    "Buchhaltung", "Budgetierung", "Business Analyse", "Business Development", 
    "Business Process Management", "Controlling", "Darlehensbuchhaltung", 
    "Datenanalyse", "Datenbanken", "Debitorenbuchhaltung", "Financial Reporting", 
    "Finanzen", "Finanzierung"
]

  },
  "13144985": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DA2NTYyMD43hDcyMjIMPI1JTNmi3EirMkMzc1kwEAyy4j3A%7C%7C23f9e90747e8f1cb8dd575e7005f13f4cdfd12c5.career/profile_photo/10353203_1722320255"
   , "expertises":[
    "Change Management im Team", "Digitalisierung von Workflowprozessen", "Docuware", 
    "Englisch verhandlungssicher", "HGB / IFRS", "Intercompany-Prozesse; Lösungen und Abstimmung", 
    "Konzernrechnungswesen", "Personalführung", "Projektleitung Implementierung eines DMS", 
    "Projektleitung S4Hana Migration", "Prozessoptimierung", "Qualitätsmanagement"
]

   },
    "17946578": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DEyMTA1NL83hDc2NLQyA0sWCzZgux4izJzE3NZAAAzikkAg%7C%7C513c4ab3ae97ed251e63cca395ad0e7364f06c0f.career/profile_photo/14240597_1739191948"
  , "expertises":["Versicherung" , "Vertrieb"]
  },
  "16652520": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DY2MzQ3NTk3hDc2NLYxMTI0MLNmu2ECvOkszc1EwGAM1vI_Y%7C10ee32cc81fbce7f55410829c850c5ad04a68ace.career/profile_photo/13361754_1739344218"
   , "expertises":[
    "Experte Baufinanzierung", "Kreditgeschäft"
]
   },
"18124485":{
   "expertises": [
    "Artificial Intelligence", "Cloud Infrastructure", "Data Analytics", 
    "Deep Learning", "IT Infrastructure", "Machine Learning", "Python", "System Integration"
]

},
"18208123":{
"expertises":[
    "Agile", "Communication", "Confluence", "DORA", "GDPR", "ISO 27001", "Jira", 
    "Microsoft Office", "Multitasking", "NIS2", "Prince2", "Problem Solving", 
    "Project Management", "Risk Management", "Scrum", "Waterfall"
]

},
"15542488":{
    "expertises":[
    "Consulting", "IT-Security"
]

},
"18174079":{
    "expertises":[
    "Arbeitsplatzgestaltung", "Arbeitsrecht", "Audit", "Audits", "Automotive", 
    "Cyber Security", "Kooperatives", "Produktion und Verkauf", "Rhetorik", "Überzeugend"
]

},
"714519": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH0zQ2MLU2OgVkMzCxNTS3MjNmu2ECvOkszc1EwGAIeiI5c%7Ce46ad01023e89bcd7e9d390f3a97ec70c7bc66b6.career/profile_photo/613853_1616845972"
    ,"expertises":[
    "Active Directory", "Altiris", "Azure", "Backup", "Beratung", "Citrix", "Client", 
    "Client Management", "Cloud", "Cyber Security", "DHCP", "DNS", "Domänenaufbau", 
    "Exchange", "Failover Cluster", "File Server", "Firewall", "Hyper-V", "IDS", "IT Security", 
    "Server 2012", "ITIL", "JIRA", "Java Web Anwendung", "LAN", "LANDesk", "MDM Support", 
    "MS", "MS 2016"
]

    },
    "16756370": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DYxMjI3MLI6BmQzMzC2MLAyM2a7YQK86SzNzUTAYAzUQj9A%7C%7C92e5531ba41175665857b16718c55bb6554cb646.career/profile_photo/13422782_1616683802"
  ,"expertises":[
    "Apple", "ISO 9001 certification level", "Miller Heiman sales methodology", 
    "Quality Total Quality Method (TQM)", "Data Security", "Data Security Responsibility", "Tablet PC"
]

  },
   "18100548": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DE2NTC3NT03hDcyNzS3NLC0sTNmu2ECvOkszc1EwGAM-RJBM%7Ce036279e0564e82b2d896272c9263fb2c0c54ccc.career/profile_photo/14358755_1727979894"
 ,"expertises":[
    "Banking", "Business IT", "Computer Science", "Credit Union", "Economics", "HTML", 
    "ISO 27000", "IT Implementation", "Java", "Management System", "Markup Languages", 
    "Process Management", "Python", "SQL", "UML", "Business Continuity", "Cyber Security"
]

   },
   "17889391": {
       "expertises":[
    "Analyse und Anwendung von Kundenfeedback", "Aufbau und Pflege von Kundenbeziehungen", 
    "ISO 13485", "ISO 14971", "Kennzeichnungsregeln", "Klassifizierung von Medizinprodukten", 
    "Klassifizierungskriterien (IVD)", "Kundenberatung und -schulung", "MATLAB", 
    "MDR-Anforderungen", "Medizinische Bildgebung und Sensortechnik"
]
   },
    "13175791": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DA2MLQyNz43hDc2NLIwNjc0sDNmu2ECvOkszc1EwGAMzSI_A%7Ccfcc802390a6e866eaaa76968f607841492ddadf.career/profile_photo/10381273_1739203790"
  ,"expertises":[
    "Aviatik", "Customer Care", "Demand Management", "Einkauf", "Beschaffung", "Food", 
    "Industrie", "IT Service Management", "Kundenbetreuung", "Lizenzen", "Lizenzmanagement", 
    "Logistik", "Procurement", "Purchasing", "Software", "Supply Chain Management", "Verkauf", 
    "Gelernter Hotelfachmann"
]

  },
  "17833985":{
      "expertises":[
    "Crowdstrike", "Cyber Security", "E-Mail Security", "IBMQradar", "ISO 27001", 
    "Phishing Analysis", "SIEM", "Schwachstellen Management", "SentinelOne", "Splunk"
]

  },
  "17420990": {
      "expertises":[
    "Business Development", "Controlling", "Cyber Security", "Digitalisierung", 
    "Führungserfahrung", "MS Office", "Mitarbeiterführung", "Personalführung", 
    "Projektleitung", "Projektmanagement", "Prozessmanagement", "Prozessoptimierung", 
    "SAP", "Strategie", "Strategieentwicklung", "Supply Chain Management", "Teamleitung"
]

  },
  "18043438": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DE2NDExNDy3hDc2MLSxMDI1NLNmu2ECvOkszc1EwGAM12I_k%7Cdcc1e7afbca291e06c72665648c4bde25a53e227.career/profile_photo/14314419_1738940259"
  ,"expertises":[
    "API", "Antenna", "C/C++", "Cryptographic Algorithms", "Electrical Engineering", 
    "Electronics", "GitHub", "Latex", "Linux", "MATLAB", "Microsoft Office Suite", 
    "NIST", "PCB Assembly", "Presentation", "Project Scope", "Python", "Quality Control", 
    "Quantum", "Quantum Computing", "Radar", "Rapid Learning", "Signal Analysis", 
    "Software Development Life Cycle"
]

  },
  "18143067":{
      "expertises":[
    "Data Collection", "Data Integration", "Emergency Handling", "Field Operations", 
    "First Aid Training", "Hardware Integration", "Innovation", "Innovative", "Inventor", 
    "Manual Handling", "Manufacturing", "Offshore", "Product Development", "Prototype", 
    "R&D", "Research & Development", "Risk Management", "Safety"
]

  },
  "13243287":{
      "expertises":[
    "Cyber Security", "Mechatronik", "SMT", "SPS", "Siplace Pro", "Siplace SX", "Siplace TX", 
    "Siplace XS", "Softwaretest", "Technischer Prüfer"
]
  },
  "18079539": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DE2MTI1Mjy3hDcyMzQ2MjY0tzNmu2ECvOkszc1EwGAM05I_U%7Cc9c46873485a70e7cdfec268e4ec10894d4b6d91.career/profile_photo/14342529_1726132397"
 ,"expertises":[
    "Information Security", "Network Security", "SOC Analyst", "Cyber Security"
]

 },
 "18146358":{
     "expertises":[
    "Audits", "Automation", "Automobiltechnik", "Automotive", "Beratung von Kunden", 
    "Cyber Security", "Cybersecurity", "Dokumentationen", "Durchführung von Schulungen", 
    "Elektrische Antriebe", "Excel", "Fahren", "Funktionale Sicherheit", "IEC 61508", 
    "ISO 26262", "ISO 9001", "Landmaschinen", "MATLAB Simulink", "Managementsysteme"
]

 },
 

"130257":{
    "expertises":[
    "Abteilungsleiter", "Diplom Bankbetriebswirt (BA)", "Quantitativer Investment Analyst"
]

},
"14493085":{
     "url":"https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DoAZLUyPDeENTC1MLI2NLM0M2a7YQK86SzNzUTAYAzV0j9w%7C%7C1871d80618d9b5adde788237ba2afe234f961c4d.career/profile_photo/11609521_1585823961"
     , "expertises": ["Lean Thinking - Geübt", "Research - Geübt"]
 },
"442103":{
    "url":"https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1jS0sTU7N4Q1MjY2NTCyNzEzZrthArzpLM3NRMBgCICyOY3c6c2d0aedfe272ecb862f6d37b5e2633fa73bba.career/profile_photo/399456_1523358274",
    "expertises":[
    "Consulting", "Controlling", "Corporate Finance", "Transaktionsberatung", 
    "M&A-Beratung", "Due Diligence", "Geschäftsfeldsteuerung", "Businessplan-Erstellung", 
    "Geschäftsprozesse (BPM)", "Operational Risk Management", 
    "Organisations- und Prozessmanagement in Banken und Sparkassen", 
    "Outsourcing", "Projektleitung"
]

}



  
  
}
    project_logos = {
        "Leitung Geschäftsbereich Finanzen und Controlling (m/w/d)": ["50515702","//blobs.experteer.com/blob/v1/eJwtjLEOgjAURRkMERN_gpkoCAJpw-jATlybJ9b6IrRNWwnoz1sSh7ucc3I3229Eds7AQ7Xx1XCLHz7CzLJTOvslfHZcOrbi5s-oMDChW5reG27oDfqXMOot743_kVaD8YImWgoWkvDSkT2u4QQDBiTS4J5tfNDKokMlWa9GDXJhgxLKHrO0KtPizLIqr-u8qPMypGFHIocjx-AHL0w5XQ%7C%7Cc176aae9538f5df19b6490e25ab8817d9f7ea381.recruiting/position_company_logos/1076045_1738834836"],
        "Experte für Cybersicherheit und Schadenmanagement (m/w/d)":["50457750",  "//blobs.experteer.com/blob/v1/eJwtjEELgjAYhj3EyKA_IXQTcluQbXjs4F26ji-ba6TbmEu0_nwTOryX53l4N9tvynbBQ2fr7OblqD9ygFlgUsxxuZyDNEGsuPozrjxMOixVG430_A7tS3n7No8q_pjRgY-C584ogRi6Nmyv13CCXicsdRCedXZo7eDALKK3yo5HTAklFyzwmdKSnHBZII4algY9SJ38AP74NXA%7C8072c7c2306d3953f34cd732102499d897e58898.recruiting/company_logos/1323291_1733824180"],
        "Steuerberater – Manager (m/w/d)": ["50488415","//blobs.experteer.com/blob/v1/eJwtjL0OgjAURhkMERNfgpkoPwawDaMDO3FtrljrjdA2bSWgL29JHL7lnJNvs_1GZOcMPFQbXw23-OEjzCzL09kv4bPj0rEVN39GhYEJ3dL03nBDb9C_hFFveW_8j7QajBc00VKwkISXjuxxDScYMCCRBvds44NWFh0qyXo1apALG5RQ9pilVZmeCpZVRV1WdZ2fQxp2JHI4cgx-L5U5Yw%7C%7C9afec7b6d38a47f6a9266587d473150b956ce63d.recruiting/position_company_logos/1076043_1738678829"],
        "Finanzspezialist/in":["50457723", "//blobs.experteer.com/blob/v1/eJwtjLEOgjAURR0MERN_gploUQTShtGBnbg2T6z1RWibthLQn7ckDnc55-SuN9-Ybr2Fh26SqxUOP2KAiWdHMoWlYvJCeb7g-s-YtDCin-suGGHZDbqXtPqt7nX4Uc6ADYKlRkke0ejS0h0u4Qg9rmhswD-bZG-0Q49a8U4PBtTMey21O2SkLEhOeFaeqnNRVUUesailscdB4OoHLyE5XQ%7C%7C0cddcf2ef50b6eef60969cf5f1e4484dd5d09f7d.recruiting/position_company_logos/1076040_1738568864"]
        }

    

    input_folder = "german_projects"  # Replace with the folder containing CSV files
    output_folder = "german_projects_finished"
    filter_eignung = True  # Only include "Sehr gut" and "Gut" candidates
    generate_german_emails(input_folder, output_folder, filter_eignung=filter_eignung, special_logos=candidates_info,
                           project_logos=project_logos)
    #clear_folder("german_projects")
