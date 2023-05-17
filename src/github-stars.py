import os
import json
import requests
import time

# Check for username
username = os.getenv('username')
if not username:
    print(json.dumps({
        'items': [{
            "arg": "https://www.alfredapp.com/help/workflows/advanced/variables/",
            "title": "Please set your GitHub username first",
            "subtitle": "Hit enter to open an introduction to variables."
        }]
    }))
    exit(1)

cache_path = os.getenv('alfred_workflow_cache')
cache_response = os.path.join(cache_path, 'cache.json')
cache_ttl = int(os.getenv('cache_ttl'))  # in seconds

# Check first if caching directory exists.
if not os.path.isdir(cache_path):
    os.makedirs(cache_path)

starred_url = f'https://api.github.com/users/{username}/starred'
http_status = 200  # default status code, so when using cache it doesn't run into error handling

# Check if there is cache
# If not load stars from github API
if os.path.exists(cache_response) and os.path.getmtime(cache_response) > (time.time() - cache_ttl):
    with open(cache_response, 'r') as f:
        resp_json = json.load(f)
else:
    response = requests.get(starred_url, headers={'User-Agent': 'GitHub Stars Alfred workflow for: ' + username})
    http_status = response.status_code
    resp_json = response.json()

    # Cache response
    if http_status == 200:
        with open(cache_response, 'w') as f:
            json.dump(resp_json, f, indent=4)

items = []
# Github API returned some sort of error.
# Also check for presence of `message` key, if HTTP Status
# code was not set to an error.
if http_status != 200 or 'message' in resp_json:
    print(json.dumps({
        'items': [{
            "arg": resp_json.get('documentation_url'),
            "title": f"GitHub Response Error ({http_status})",
            "subtitle": resp_json.get('message'),
        }],
    }))
    exit(1)
# Search through the results.
for star in resp_json:
    match = star['full_name'].replace('/', ' ').replace('-', ' ').replace('_', ' ')
    items.append({
        'type': 'default',
        'title': star['full_name'],
        'subtitle': f" ⭐ {star['stargazers_count']},  {star['description']}",
        'arg': f"https://www.github.com/{star['full_name']}",
        'autocomplete': star['full_name'],
        'icon': {
            'path': "./icon.png"
        },
        'match': match,
        'quicklookurl': f"https://www.github.com/{star['full_name']}"
    })

print(json.dumps({"items": items}, indent=4))
