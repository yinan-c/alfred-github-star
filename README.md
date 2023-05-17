# GitHub Star - Alfred Workflow


This workflow is for [Alfred](https://www.alfredapp.com/), which is a launcher for MacOS. It allows you to search through your GitHub stared repositories.

## Usage

- `ghs {query}`  will show you a stared repositories list in time order, with repo name, number of stars and descriptions.
   - `⏎`  on a selected result to directly open the repository in your browser
   - `⌘ + ⏎` to modifier key ⌘ to copy the URL to the clipboard.
   - `⌃ + ⏎` to copy the `git clone` command to the clipboard.

## Setup

- [Download the Workflow here](https://github.com/ychen-97/alfred-github-star/releases). Go the variables inside Alfred variable panel {x} and set your username.
- You can set cache duration in seconds, default is 600 seconds before the old cache expires.

## Thanks

- Jonathan Ströbele's [alfred-github-stars](https://github.com/stroebjo/alfred-github-stars). I took the inspiration from him, wrote the code in Python and removed the image caching. (Hopefully it will reduce the caching time if you have large database.)

