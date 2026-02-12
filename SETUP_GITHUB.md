# GitHub Setup Instructions

This guide explains how to push your local repository to GitHub with proper commit history.

## Prerequisites

- GitHub account (create one at https://github.com if you don't have)
- Git installed on your system
- Access to the remote repository URL

## Step-by-Step Instructions

### Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Fill in the repository name: `Uninformed-Search-in-a-Grid-Environment`
3. Add description: "AI Pathfinder implementing 6 uninformed search algorithms with dynamic obstacles"
4. Choose visibility: **Public** (so evaluators can see it)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### Step 2: Add Remote Repository

After creating the repository on GitHub, you'll see commands. Run:

```bash
cd "/home/muhammad-imtinan-ul-haq/Desktop/Uninformed Search in a Grid Environment"

# Add the remote reference (replace YOUR_USERNAME)
git remote add origin https://github.com/ImtinanulHaq/Uninformed-Search-in-a-Grid-Environment.git

# Verify it was added
git remote -v
```

**Output should show:**
```
origin  https://github.com/ImtinanulHaq/Uninformed-Search-in-a-Grid-Environment.git (fetch)
origin  https://github.com/ImtinanulHaq/Uninformed-Search-in-a-Grid-Environment.git (push)
```

### Step 3: Push to GitHub

```bash
cd "/home/muhammad-imtinan-ul-haq/Desktop/Uninformed Search in a Grid Environment"

# Rename branch from 'master' to 'main' (GitHub standard)
git branch -M main

# Push all commits to GitHub
git push -u origin main
```

You may be prompted to authenticate:
- **If using HTTPS:** Enter your GitHub username and personal access token (not your password)
  - Create token at: https://github.com/settings/tokens
  - Select scopes: `repo` (full control of private repositories)

- **If using SSH:** Make sure you've set up SSH keys
  - Guide: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Step 4: Verify on GitHub

1. Visit your repository: `https://github.com/ImtinanulHaq/Uninformed-Search-in-a-Grid-Environment`
2. Check the "Commits" tab - you should see 5 commits:
   - feat: Implement grid management module with obstacle handling
   - feat: Implement all six uninformed search algorithms
   - feat: Implement professional GUI visualization using Pygame
   - feat: Implement main application with interactive interface
   - docs: Add comprehensive documentation and project configuration

## Viewing Commit History

To see detailed commit information:

```bash
# View commit log with full messages
git log

# View commit log in one line (like GitHub)
git log --oneline

# View specific commit details
git show <commit-hash>

# View changes in a specific commit
git diff <commit-hash>^..<commit-hash>
```

## If You Made a Mistake

### Reset to Previous Commit
```bash
# CAUTION: This will undo changes
git reset --hard <commit-hash>

# Then force push (only if not shared with others)
git push -f origin main
```

### Add Forgotten Changes
```bash
# Make the changes
git add <files>
git commit -m "fix: Additional fixes"
git push origin main
```

## After Pushing to GitHub

The repository is now public and ready for evaluators to view:

✅ Complete code with all 6 algorithms
✅ Professional GUI visualization
✅ Comprehensive README.md
✅ Clean commit history showing development progress
✅ requirements.txt for easy setup
✅ .gitignore for best practices

## Sharing Your Repository

You can share the link:
```
https://github.com/ImtinanulHaq/Uninformed-Search-in-a-Grid-Environment
```

## Troubleshooting

### Authentication Failed
```bash
# Update remote URL to use SSH instead of HTTPS
git remote set-url origin git@github.com:ImtinanulHaq/Uninformed-Search-in-a-Grid-Environment.git

# Or use personal access token for HTTPS
```

### Branch Already Exists
```bash
# Check existing branches
git branch -a

# Delete local branch if needed
git branch -d master

# Continue with push
git push -u origin main
```

### Large Binary Files Error
```bash
# This repository doesn't have large files, so this shouldn't be an issue
# But if it occurs, check .gitignore
cat .gitignore
```

## Important Notes

✅ **Your repository looks professional because:**
- Multiple meaningful commits showing development progression
- Detailed commit messages explaining what and why
- Comprehensive README with usage instructions
- All code is well-documented with comments
- .gitignore properly configured
- requirements.txt for dependencies

✅ **Make sure your evaluator can easily:**
- Understand the project structure
- Install dependencies: `pip install -r requirements.txt`
- Run the application: `python app.py`
- View code quality and documentation
- See commit history showing development

## Next Steps

1. Push your code to GitHub
2. Test the GitHub page looks good
3. Verify README renders properly
4. Check code is readable and well-commented
5. Confirm commit history shows progression
6. Share the repository link with evaluators

---

**All set!** Your project is now ready for submission with a professional GitHub repository.
