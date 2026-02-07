#!/bin/bash
set -e
git config --global user.email 'reviewer@agent.bot'
git config --global user.name 'AI Reviewer'

if [ -d ".git" ]; then
    git remote set-url origin https://x-access-token:$GITHUB_TOKEN@github.com/bughouse-wizzard/service_alpha.git
    git fetch origin
else
    git clone https://x-access-token:$GITHUB_TOKEN@github.com/bughouse-wizzard/service_alpha.git .
fi

git checkout feat/mega-47a362e2-a8a4-4a43-9bb1-51f54c16e988
echo "Review Environment Ready"
