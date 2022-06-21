#!/bin/bash

archive_url=$(curl \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/steryereo/weatherlights_frontend/releases/latest 2>&1 | \
  grep -o '"browser_download_url": "[^"]*' | grep -o '[^"]*$')

curl -L $archive_url -o frontend.zip

unzip -o frontend.zip -d webserver/public

rm frontend.zip
