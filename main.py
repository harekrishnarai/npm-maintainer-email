import requests
import sys

def get_maintainer_info(package_name):
    """
    Attempts to fetch maintainer information for a given npm package.

    This script demonstrates a method that was historically used by attackers
    to easily collect maintainer emails for phishing campaigns.

    NOTE: As of recent security updates by npm/GitHub, the 'maintainers' field
    containing email addresses has been removed from the public API response
    to protect developers. This script now serves as an educational tool to
    show what was once possible.
    """
    # The public API endpoint for an npm package
    url = f"https://registry.npmjs.org/{package_name}"
    
    print(f"[*] Fetching package data for '{package_name}' from {url}...")
    
    try:
        # Make the GET request to the npm registry
        response = requests.get(url, timeout=10)
        
        # Check for a successful response (HTTP 200 OK)
        response.raise_for_status()
        
        # Parse the JSON response into a Python dictionary
        data = response.json()
        
        # --- THE HISTORICAL VULNERABILITY ---
        # Attackers would simply parse this 'maintainers' key.
        if 'maintainers' in data and data['maintainers']:
            print("\n[SUCCESS] Found maintainer data (this is now rare):\n")
            for maintainer in data['maintainers']:
                name = maintainer.get('name', 'N/A')
                email = maintainer.get('email', 'N/A')
                print(f"  - Name: {name}, Email: {email}")
        else:
            # This is the expected outcome today
            print("\n[INFO] The 'maintainers' field with public emails is no longer exposed by the npm registry API.")
            print("This is a positive security change to protect developers from mass-harvesting and phishing attacks.")

            # We can still show other non-sensitive data to prove the API call worked
            if 'author' in data and data.get('author'):
                 author_name = data['author'].get('name', 'Not specified')
                 print(f"[*] The package author is listed as: {author_name}")
            
            latest_version = data.get('dist-tags', {}).get('latest', 'N/A')
            print(f"[*] The latest version of the package is: {latest_version}")

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            print(f"\n[ERROR] Package '{package_name}' not found. Please check the name.")
        else:
            print(f"\n[ERROR] HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"\n[ERROR] A network error occurred: {req_err}")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Check if a package name was provided as a command-line argument
    if len(sys.argv) > 1:
        package_to_check = sys.argv[1]
    else:
        # Use a well-known package as a default example
        package_to_check = "chalk"
        print(f"[INFO] No package name provided. Using '{package_to_check}' as an example.")
        print("Usage: python main.py <package-name>\n")
    
    get_maintainer_info(package_to_check)