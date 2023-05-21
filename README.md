# GitHub Star - Alfred Workflow


This workflow is for [Alfred](https://www.alfredapp.com/), which is a launcher for MacOS. It allows you to search through your GitHub stared repositories from https://api.github.com/users/{username}/starred.

## Usage

- `ghs {query}`  will show you a stared repositories list in time order, with repo name, number of stars and descriptions.
   - `⏎`  on a selected result to directly open the repository in your browser
   - `⌘ + ⏎` to copy the URL to clipboard.
   - `⌃ + ⏎` to copy the `git clone` command to clipboard.

## Setup

- [Download the Workflow here](https://github.com/ychen-97/alfred-github-star/releases). Set the your Github username to `username`.
- Set cache time-to-live in seconds in `cache_ttl`, default is 86400 seconds before the old cache expires.
- You can also set a limit for pages retrieved from [GitHub's paginated API](https://docs.github.com/en/rest/guides/using-pagination-in-the-rest-api), your results will include `max_pages` * 30 recent starred repos. Recommended when you have a large database. Default (-1) fetches all starred repos.

Please note the GitHub API currently restricts anonymous requests to a maximum of 60 calls per hour. It is advised not to run the workflow too often when you set `cache_ttl` at a very small value.

## Thanks

- Jonathan Ströbele's [alfred-github-stars](https://github.com/stroebjo/alfred-github-stars). I took the inspiration from him, wrote the code in Python and removed the image caching. (Hopefully it will reduce the caching time if you have large database.)

