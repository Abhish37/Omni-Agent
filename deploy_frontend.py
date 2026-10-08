import requests
import sys

API_KEY = "rnd_84DFYUhSjrkgvtaCqPDsEZ8KmOSg"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def main():
    print("Fetching owner ID...")
    resp = requests.get("https://api.render.com/v1/owners", headers=HEADERS)
    owners = resp.json()
    owner_id = owners[0]["owner"]["id"]
    
    print("Deploying Frontend as Static Site...")
    web_payload = {
        "type": "static_site",
        "name": "omni-agent-frontend",
        "ownerId": owner_id,
        "repo": "https://github.com/Abhish37/Omni-Agent",
        "branch": "master",
        "autoDeploy": "yes",
        "serviceDetails": {
            "publishPath": "./frontend",
            "pullRequestPreviewsEnabled": "no"
        }
    }

    resp = requests.post("https://api.render.com/v1/services", headers=HEADERS, json=web_payload)
    if not resp.ok:
        print("Error creating static site:", resp.text)
        sys.exit(1)

    service_data = resp.json()
    service_info = service_data if "service" not in service_data else service_data["service"]
    service_url = service_info.get("serviceDetails", {}).get("url", "URL pending")
    
    print("\n================================================")
    print("Frontend deployment triggered successfully!")
    print(f"Your public frontend URL is: {service_url}")
    print("================================================\n")

if __name__ == "__main__":
    main()
