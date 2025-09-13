import requests
import json
import time
from typing import List, Dict, Optional

def get_top_npm_packages(limit: int = 100) -> List[str]:
    """Get top npm packages from npmjs.org"""
    url = "https://registry.npmjs.org/-/v1/search"
    params = {
        "text": "keywords:popular",
        "size": limit,
        "quality": 1.0,
        "popularity": 1.0,
        "maintenance": 1.0
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return [pkg["package"]["name"] for pkg in data["objects"]]
    except Exception as e:
        print(f"Error fetching top packages: {e}")
        return []

def get_package_info(package_name: str) -> Optional[Dict]:
    """Get package information from npm registry"""
    url = f"https://registry.npmjs.org/{package_name}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {package_name}: {e}")
        return None

def extract_maintainer_emails(package_info: Dict) -> List[str]:
    """Extract maintainer emails from package info"""
    emails = []
    
    # Check maintainers field
    if "maintainers" in package_info:
        for maintainer in package_info["maintainers"]:
            if "email" in maintainer:
                emails.append(maintainer["email"])
    
    # Check author field
    if "author" in package_info:
        author = package_info["author"]
        if isinstance(author, dict) and "email" in author:
            emails.append(author["email"])
        elif isinstance(author, str) and "<" in author and ">" in author:
            # Parse "Name <email>" format
            email_start = author.find("<") + 1
            email_end = author.find(">")
            if email_start > 0 and email_end > email_start:
                emails.append(author[email_start:email_end])
    
    return list(set(emails))  # Remove duplicates

def main():
    print("Fetching top 100 npm packages...")
    packages = get_top_npm_packages(100)
    
    if not packages:
        print("Failed to fetch packages")
        return
    
    all_emails = []
    package_data = []
    
    for i, package_name in enumerate(packages, 1):
        print(f"Processing {i}/100: {package_name}")
        
        package_info = get_package_info(package_name)
        if package_info:
            emails = extract_maintainer_emails(package_info)
            all_emails.extend(emails)
            
            package_data.append({
                "package": package_name,
                "emails": emails,
                "description": package_info.get("description", ""),
                "downloads": package_info.get("downloads", {}).get("weekly", 0)
            })
        
        # Rate limiting
        time.sleep(0.1)
    
    # Save results
    unique_emails = list(set(all_emails))
    
    results = {
        "total_packages": len(packages),
        "total_emails": len(unique_emails),
        "unique_emails": unique_emails,
        "package_details": package_data
    }
    
    with open("npm_maintainer_emails.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to npm_maintainer_emails.json")
    print(f"Found {len(unique_emails)} unique maintainer emails")
    print(f"Processed {len(package_data)} packages")

if __name__ == "__main__":
    main()