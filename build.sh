#!/bin/bash

if [ "$CF_PAGES_BRANCH" == "master" ]; then
  # Run the "production" script in package.json on the "production" branch
  hugo --minify -b $CF_PAGES_URL

else
  # Else run the dev script
  hugo --minify -D -b $CF_PAGES_URL
fi