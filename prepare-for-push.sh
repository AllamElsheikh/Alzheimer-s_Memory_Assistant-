#!/bin/bash

# Prepare for Push Script
# This script prepares the project for pushing to GitHub by:
# 1. Adding all new files
# 2. Committing changes
# 3. Running pre-push checks

echo "🚀 Preparing فاكر؟ (Faker?) project for push..."

# Add all new files
echo "📂 Adding new files and changes..."
git add .

# Show status
echo "📊 Current git status:"
git status

# Prompt for commit message
echo "📝 Enter commit message:"
read commit_message

if [ -z "$commit_message" ]; then
  commit_message="Update project with React Native mobile app and environment configuration"
  echo "Using default commit message: $commit_message"
fi

# Commit changes
echo "💾 Committing changes..."
git commit -m "$commit_message"

# Run pre-push checks
echo "🔍 Running pre-push checks..."
cd mobile && npm run lint && npm run check-env
push_check_status=$?

if [ $push_check_status -eq 0 ]; then
  echo "✅ Pre-push checks passed!"
  echo "🚀 Ready to push! Run 'git push' to push to GitHub."
else
  echo "❌ Pre-push checks failed. Please fix the issues before pushing."
fi

cd ..
echo "Done! 🎉" 