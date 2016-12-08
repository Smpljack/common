#!/bin/bash
export GIT_COMMITTER_NAME="page update bot"
export GIT_COMMITTER_EMAIL="none@none"
export GIT_AUTHOR_NAME=`git --no-pager show -s --format='%an'`
export GIT_AUTHOR_EMAIL=`git --no-pager show -s --format='%ae'`

git commit -m "Update by page update bot" > /dev/null
