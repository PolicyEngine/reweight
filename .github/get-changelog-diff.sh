#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Add upstream if it doesn't exist
git remote | grep -q 'upstream' || git remote add upstream https://github.com/policyengine/reweight

# Fetch tags from upstream
git fetch --tags upstream

# Try to get the last tag, if it fails, use the initial commit
last_tagged_commit=$(git describe --tags --abbrev=0 --first-parent 2>/dev/null || git rev-list --max-parents=0 HEAD)

if [ -z "$last_tagged_commit" ]; then
    echo "No tags or initial commit found. Cannot compare changes."
    exit 1
fi

# Check if CHANGELOG.md exists
if [ ! -f CHANGELOG.md ]; then
    echo "CHANGELOG.md does not exist. Please create it and add your changes."
    exit 1
fi

# Show diff of CHANGELOG.md
git --no-pager diff $last_tagged_commit -- CHANGELOG.md

# Check if there are any changes in CHANGELOG.md
if [ -z "$(git diff $last_tagged_commit -- CHANGELOG.md)" ]; then
    echo "No changes detected in CHANGELOG.md since last tag ($last_tagged_commit)."
    echo "Please update CHANGELOG.md with your recent changes."
    exit 1
fi