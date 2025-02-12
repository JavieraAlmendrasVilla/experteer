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
            }
            candidates.append(candidate)

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
     "7343715": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1TU0tjAyPDeEMTAwsTc0tDSwM2a7YQK86SzNzUTAYAqhEjwQ%7C%7C72c6f3c43e239c5d7573ab41de72285609f26f4e.career/profile_photo/5593021_1408479190"
  , "expertises":["Balanced Scorecard" , "Budgetierung" ,"MS-Office (insbesondere Excel)" , "Microsoft Visual Studio (C#)" , "Planung (GuV, Liquidität, Bilanz)" , "Reporting" , "SAP" , "SAP (CO & MM)" , "Vertriebscontrolling" ]},
   "962417": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH0LIyMjM0OgVlNzQ0sjQwsjNmu2ECvOkszc1EwGAIbKI4s%7Ca8ef03be4aedbe6058603838ca36f355e1c9333c.career/profile_photo/822261_1657192182"
, "expertises":["DATEV" , "EXCEL" , "SAP R/3 FI" , "Sage KHK" , "WORD"]},
 "10281198": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1zIDAyMYk3NDGwMDUxMLEwZ7NmC7HiLMnMTc1kAACrMiPM4cd5cbbe3264c63c6cc6881bf5ddb1c1bcb3e3b3.career/profile_photo/7777244_1408540487"
  , "expertises":["Automationssysteme (SCADA / HMI)" , "ERP (SAP, Navision etc.)" , "IT Infrastruktur Architectur und Aufbau" , "Logistikprozesse" ," Rechenzentrumsaufbau und -betrieb" , "Softwareentwicklung" , "Training" ," internationales Programm- und Changemanagement"]},
  "428704": {
      "expertises":["Real Estate Risk Manager (EBS)" , "Renewable Energies (esp. PV)"]
  },
   "2662228": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH0jIwMjCwPzeEMTAwtjUwtTSxM2a7YQK86SzNzUTAYAqaMjwQ%7C%7C05804500a218552ef864111ac528e33a245b3b60.career/profile_photo/2202807_1408358594"
   , "expertises":["Führungserfahrung", "Projektmanagement" , "Migrationsprojekte", "SOA", "Oracle", "Cognos" , "Optimierungsprojekte", "Costsaving Projekte", "technische Architektur", "Aufbau von Rechenzentren"]},
   "474298": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH0TIwsDc4t4Q3NjM0sTM3MjIzZrthArzpLM3NRMBgCH4COY05953c47ff5ac053ed1c0b518e308f2251e64a14.career/profile_photo/428078_1736946722"
   , "expertises":[
"Einsatzplanung" , "IT-Konsolidierung" , "Incident management" ," Itil v3 expert" , "Kunden Akquise", "Major Incident Management" , "Personalführung" , "Personalplanung" , "Prince2 Practitioner" , "Problemmanagement" , "Projekt Leitung" , "Releasemanagement" , "Scrum master" , "Scrum product owner" ]},
 "1281866": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH1DA0sjM1ODeENzYzNLY2MjQwM2a7YQK86SzNzUTAYAqWYjtw%7C%7C0c9c19fe02cfbf08d2e12c2830a9bd2a5f46a18f.career/profile_photo/1092650_1736933210"
  , "expertises":["Budgetplanung und Controlling" , "Change Management" , "Datenschutz" , "Gruppenkommunikation" , "ITIL Expert" , "ITIL Service Manager" , "ITSM" , "Mitarbeitergespräche" , "Prince 2" , "Projekt Management" , "Prozessoptimierung im Vertrieb und Support" , "Prozessoptimierung in der IT" ]},
"1995946": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw0ELgjAUAGAPMVrQnxCii9AW8pjr3MG79_GIt3ygbs4pUn--PvgOx6-0p5zQh7a8enzRMq-YyFWJFv7QiLvToPb_Kk5vJ6x4dvbMU6a04cCFlRFz35aXmILngVzsQw43DaZpoHa6VkaBuSsQD9FZmXkkLn6rSCPL3398221508e1ddd80064c8c65a6d1c618c7eb945.career/profile_photo/1689964_1408068206"
 , "expertises":["Java" , "MS Office" , "MS Visio" , "SAP R/3" , "Unternehmensentwicklung" , "VBA" , "Windows XP" ] },
 "105295": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXlgqL8tMyc1PiCjPySfH1LM2Mzw3hDU0NTM0tDY0tzNmu2ECvOkszc1EwGAGTGI2M%7C783b4e76488c47ab88437cc5ae48ca8880da55bd.career/profile_photo/96361_1515691397"
 , "expertises":[ "Data Warehousing and Data Modelling" , "Internal Project Management" , "PMP Certification (PMI)" , "Personalführung" , "Prince2" , "Scrum and Agile" ,"Software Entwicklung", "Systemintegration" ] },
 "587689": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1TQyMjY9N4QxMDCwMjcyNjCzZrthArzpLM3NRMBgCFzyOB302d23a4b8b1db8f9b36910e2a1afab24f160a8e.career/profile_photo/512235_1408027238"
  , "expertises":["Anforderungsmanagement und Projektvorbereitung" , "Datenschutz und Datensicherheit" , "IT-Projektleitung", "Projektumsetzung" , "Internet Präsentationen", "Websites und Datendienste" , "Java / .Net Application Development" , "Online Community Systeme und Foren" , "Onlineshopping und eCommercelösungen"]},
  "1108744": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyWVgqL8tMyc1PiCjPySfH1LEzNDQ_N4QxMDCwMTI0NDIzZrthArzpLM3NRMBgCGQCN_187b4d509a99a440d03761ee9cbe89e7f158793b.career/profile_photo/946117_1408042112"
   , "expertises":["Agile Project Management" ," Business Case Analysis" , "Business Process Optimisation" , "International Project Leadership", "PRINCE2" , "Team Leadership"]},
"757091":{
    "expertises":["BPMN und IT aligment", "Energieversorgung Konzepte", "Infrastrukture Anlagebau", "Kontinuierliche Prozessoptimierung", "Methode der Operativen Prozessgestaltung", "Prozessmanagement", "Schienenfahrzeugtechnik", "Stromrichter Theorie", "Elektronik/ Elektrik", "Bussysteme", "Gesamtfahrzeug"]
},
"17725093": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DEwMzI0tjQ6BmS2NLC1MDUwM2a7YQK86SzNzUTAYAzW4j9g%7C%7C019b77b426fa6722e89a52333f65c0d714adee04.career/profile_photo/14062931_1693985050"
 , "expertises":["Führung eines Teams", "Inbetriebnahme", "Inbetriebnahme von Anlagen", "Outsourcing", "Planungs", "Projektablaufs", "Projektleitung", "Richtfunk", "Service Desk", "Service Management", "Stakeholdern", "Technischer Leiter", "Telecom"]
 },
 "5633080": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH0TEwMDYzPDeENzY0MLU0NTI1M2a7YQK86SzNzUTAYAqPIjtQ%7C%7C66c00e15166aa3fd828a3ee1ffebc20739009abc.career/profile_photo/4400361_1731851525"
 , "expertises":["(Agiles) Projektmanagement", "Access DB", "Confluence", "DB", "Erstellung Berichte und Konzepte", "Jira", "Kaufmännisches", "LMS Bund", "MS-Office", "Microsoft SharePoint", "Office 365", "OpenOffice", "SAP", "Scrum", "SharePoint", "Terminüberwachung im Projektgeschäft", "öV-Karte 1.0"]
 },
  "18122343": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DE2NzM3NTg3hDcyNLAwtTC3NzNmu2ECvOkszc1EwGAM57JAU%7C3437add366e0cd9170f869b6c46da485f9b575b9.career/profile_photo/14376750_1729085877"
  , "expertises":["ABACUS", "Change management", "Einsatzplanung", "Excel", "Fakturierung", "Finanzbuchhaltung", "IT-KENNTNISSE", "Informatik", "Logistik", "Microsoft Office 365", "Möbel", "Outlook", "Produktentwicklung", "Projektmanagement", "Transport Management System", "Warehouse Management"]
},
"18147207": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw7EKwjAQANAOEhrBn-hQl4I9UwyJs0P37uGQiz1om5hGKfrz-uDtyq-0-5zQh746erzT-nxhItckWvlDM24OLu3238Tl4YQVt8EeeMmU3jhxYWXEPPZVHVPwPJGLY8jhBJ0yGs7gQCswWqnWiKsYrMw8Exc_zVkj9Q%7C%7Cab1c39effcc17c3298ca41393d46538df8bfc22c.career/profile_photo/14397121_1731973309"
  , "expertises":["CLM", "CRM", "Fintech", "Wealth management", "collaboration", "digital design", "digital technology", "initiative", "software solutions"]
},
"17411888": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyW1gqL8tMyc1PiCjPySfH1DYwtDSyMjc6BmUxMzc1NjE0M2a7YQK86SzNzUTAYAzdIj-Q%7C%7C97ae8f554650f24282a64e6720ca05b874a8c644.career/profile_photo/13819227_1654675341"
  , "expertises":["customer care", "customer service", "kommunikation", "kundenbetreuung", "kundenservice", "ms office", "projektmanagement", "vertrieb"]
},
"4756790": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw7EKwjAQANAOEozgTxTEpaChpCnn7NC9-3HIxR60TZpGKfrz-uDt9l8Nh5zIh648e3rwurwoMVaJV_nwRBua5rr9V3F-ogJ17-Eoc-b0plEK0JHy0JWnmIKXkTEOIYdL7WzrnEVjjatbYxunbqoHnWViKX6ruyPT38c79f52c4c51bd2695a7cf6affb5778f815034c.career/profile_photo/3758775_1517381567"
  , "expertises":["Anti-corruption compliance Management", "Architecture", "Ariba ACW", "BW", "Business process improvement", "Change control", "GTS (Global Trade Systems)", "Negotiations", "Packaging Artworks", "Process and Compliance Management", "Project Library", "SAP MDM", "SAP/R3; GTS P43 BW", "Sales and supply", "Supply and Logistics Management", "Supply chain management", "Sustainability", "Trackwise"]
},
"10460249": {
    "url": "https://blobs.experteer.com/blob/v1/eJwNw7EKwjAQANAOEozgTxTEpWBCwNQ4O3TvfhxysQdtE69Riv68Pnib7VeHXRGMqauPEe-0PF8oBI3Qwh-acAV7Nut_k-cHqKBufdjzXEjeOHIVdMYydPUhS4o8EuQhlXTyF-dd68B6561prTHqqvqgC0_E1Q-qxiPB465611aa9b15052583179d7b43cc8d3ac1f43757.career/profile_photo/7937383_1737108100"
 , "expertises":["Banking", "IT Finance Solutions Telemetry MS O365", "Recruitment Staffing HR Outsourcing", "Sales Sales Support Enablement", "Vending Operations Logistics"]
 },
 "10629004": {
    "url": "https://blobs.experteer.com/blob/v1/eJxj4ajmtOIqKUpMy_dUUk9LTE4tLixNLEqN1ylKLc6sSs1NrIg3NDOoAGKdgrz0eDYrNtcQK97MvJLUorLEnEwGK86CxJIMTyXVgqL8tMyc1PiCjPySfH0LAwsLY1OjeENzYzMjM3NzczM2a7YQK86SzNzUTAYAq4Ij0w%7C%7C8cb6b0655ce888e3300cd9a27161669d82e7e45c.career/profile_photo/8088352_1736267776"
  , "expertises":["Change management", "Consulting", "Management", "Process improvement", "Project management", "Strategic planning"]
}

    
}
    project_logos = {
        "Business Process Manager (m/w/d)": ["50240910","//blobs.experteer.com/blob/v1/eJwtjLEOgjAURRkMERN_gplowQjahtGBnbg2T6z1RWibthLQn7ckDnc55-Su1t-EbryFh27SqxUOP2KAiecFmcIyMXmhPF9w_WdMWhjRz3UXjLDsBt1LWv1W9zr8KGfABsEyoySPaXxp6RaXcIQeI5oY8M8m3Rnt0KNWvNODATXzXkvt9jmpSkIKnleH8nQ8nIsyZnFLE4-DwOgHLo05VQ%7C%7C215f070d17783c6e52d0e41660b3d4f465edbf2c.recruiting/position_company_logos/1076002_1736853926"],
        "Head of FP&A Operations (m/w/d)":["50395122",  "//blobs.experteer.com/blob/v1/eJwtjLEOgjAURR0MERN_gploARXShtGBnbg2T6z1RWibthLQn7ckDnc55-SuN9-Ybr2Fh26SqxUOP2KAiWc5mcJSMXmhPF9w_WdMWhjRz3UXjLDsBt1LWv1W9zr8KGfABsFSoySPaHRp6Q6XcIQeVzQ24J9NsjfaoUeteKcHA2rmvZbaHTJSnklBeFYWFTnlRXWMWNTS2OMgcPUDLg45TQ%7C%7C5006014454fd78431669de0361df85b548b65722.recruiting/position_company_logos/1076030_1738052384"],
        "Projektleiter Corporate Strategy (m/w/d)": ["50229955",""]
        }

    

    input_folder = "german_projects"  # Replace with the folder containing CSV files
    output_folder = "german_projects_finished"
    filter_eignung = False  # Only include "Sehr gut" and "Gut" candidates
    generate_german_emails(input_folder, output_folder, filter_eignung=filter_eignung, special_logos=candidates_info,
                           project_logos=project_logos)
    #clear_folder("german_projects")
