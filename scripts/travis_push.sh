#!/bin/bash
if [ -z "${GH_TOKEN}" ]; then
    echo "GH_TOKEN not set! git remote will not be changed!"
    exit
fi
git remote set-url --push origin https://${GH_TOKEN}@github.com/d70-t/narval-ii.git > /dev/null
git push
