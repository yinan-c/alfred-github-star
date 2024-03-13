import os
import json
import requests
import time

username = os.getenv('username')
token = os.getenv('github_api_token')
cache_path = os.getenv('alfred_workflow_cache')
cache_response = os.path.join(cache_path, 'cache.json')
cache_ttl = float(os.getenv('cache_ttl'))  # in minutes
max_pages = os.getenv('max_pages')  # empty for no limit
search_repo_description = bool(os.getenv('search_repo_description'))

# Check first if caching directory exists.
if not os.path.isdir(cache_path):
    os.makedirs(cache_path)

http_status = 200  # default status code, so when using cache it doesn't run into error handling

# Check if there is cache
# If not load stars from github API
if os.path.exists(cache_response) and os.path.getmtime(cache_response) > (time.time() - cache_ttl * 60):
    with open(cache_response, 'r') as f:
        resp_json = json.load(f)
else:
    resp_json = []
    page = 1
    while True:
        if max_pages and page > int(max_pages):
            break

        starred_url = f'https://api.github.com/users/{username}/starred?page={page}'
        headers={'User-Agent': 'GitHub Stars Alfred workflow for: ' + username}
        if token:
            headers['Authorization'] = 'Bearer ' + token

        response = requests.get(starred_url, headers=headers)
        http_status = response.status_code
        page_data = response.json()

        if http_status != 200 or 'message' in page_data:
            print(json.dumps({
                'items': [{
                    "arg": page_data.get('documentation_url'),
                    "title": f"GitHub Response Error ({http_status})",
                    "subtitle": page_data.get('message'),
                }],
            }))
            exit(1)

        if not page_data:  # No more data, break the loop
            break

        resp_json.extend(page_data)
        page += 1

    # Cache response
    with open(cache_response, 'w') as f:
        json.dump(resp_json, f, indent=4)

items = []
# Search through the results.
for star in resp_json:
    match = (f"{star['full_name']}  {star['description']}" if search_repo_description else star['full_name']).replace('/', ' ').replace('-', ' ').replace('_', ' ')
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
