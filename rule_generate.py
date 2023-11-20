import requests
import json

def generate_rules(website_list):
    rules = []
    for idx, website in enumerate(website_list, start=1):
        if len(website) == 0:
            continue
        rule = {
            "id": idx,
            "priority": 1,
            "action": {
                "type": "block"
            },
            "condition": {
                "urlFilter": f"*://*{website}/*"
            }
        }
        rules.append(rule)
    return rules

def read_websites_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Skipping lines that start with #
        lines = response.text.splitlines()
        websites = [line.strip('[] \n').split(' ')[1] for line in lines if (line.startswith('#') is False and len(line) > 0)]
        return websites
    else:
        print(f"Failed to fetch data from {url}")
        return []

def main():
    hosts_url = 'https://adaway.org/hosts.txt'
    output_json_file = 'rules1.json'  # Replace with your desired output JSON file

    websites = read_websites_from_url(hosts_url)
    rules = generate_rules(websites)

    with open(output_json_file, 'w') as json_file:
        json.dump(rules, json_file, indent=2)

if __name__ == "__main__":
    main()
