#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

# Add upstream if it doesn't exist
git remote | grep -q 'upstream' || git remote add upstream https://github.com/policyengine/reweight

# Fetch tags from upstream
git fetch --tags upstream

# Try to get the last tag, if it fails, use the initial commit
last_tagged_commit=$(git describe --tags --abbrev=0 --first-parent 2>/dev/null || git rev-list --max-parents=0 HEAD)

# Show diff of CHANGELOG.md
git --no-pager diff $last_tagged_commit -- CHANGELOG.md