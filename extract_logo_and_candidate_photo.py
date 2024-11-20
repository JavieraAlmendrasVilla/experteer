import requests
import json

def fetch_urls_from_json(session, url):
    """
    Fetch and extract URLs from the JSON response at the given URL.

    :param session: An authenticated requests.Session object.
    :param url: The URL to fetch the JSON data from.
    :return: A dictionary containing the extracted URLs.
    """
    try:
        # Send a GET request to the URL using the authenticated session
        response = session.get(url)
        
        # Check the response status
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract URLs from the JSON data
            extracted_urls = {key: value.get("url") for key, value in data.items()}
            
            # Display the URLs
            for key, url in extracted_urls.items():
                print(f"ID: {key}, URL: {url}")
            
            return extracted_urls
        else:
            print(f"Failed to fetch JSON. HTTP Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # The URL to fetch the JSON data from
    json_url = "https://intern.experteer.com/admin/account_photo_json?jid=49147175&id=1955208"

    # Create a session (assuming you are already logged in)
    session = requests.Session()
    # You might need to add session cookies or headers if required for authentication
    # Example: session.cookies.set("sessionid", "your_session_id")

    # Fetch and extract the URLs
    urls = fetch_urls_from_json(session, json_url)
    if urls:
        print("Extracted URLs:")
        print(json.dumps(urls, indent=2))
