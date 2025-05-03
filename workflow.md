# Team Collaboration Workflow

This document outlines our team's GitHub workflow and collaboration practices.

**API URLS:**

*OpenF1:* https://openf1.org/

*FastF1:* https://docs.fastf1.dev/index.html

*Ergast:* https://ergast.com/mrd/db/

## 1. Branch Strategy
- Maintain a protected `main` branch that always contains stable, working code
- Create feature branches for different components using the format:
  ```
  data-collection
  data-visualization
  web-dev
  ```

## 2. Working Process

### Starting each work session
```bash
# First time only: Check out your assigned branch
# Choose ONE of:
git checkout data-collection
git checkout data-visualization
git checkout web-dev
```

### Starting Each Work Session
```bash
# 1. Always start by updating main
git checkout main
git pull origin main

# 2. Switch to your branch
git checkout your-branch-name  # (data-collection, data-visualization, or web-dev)

# 3. Merge main into your branch to stay up-to-date
git merge main

# 4. Activate the virtual environment (if needed)
# On Windows:
5200-project\Scripts\activate
# On Mac/Linux:
source 5200-project/bin/activate

# 5. Install/update any new requirements
pip install -r requirements.txt
```

### During Your Work Session
```bash
# Commit your changes frequently with descriptive messages
git add .
git commit -m "descriptive message about what you did"

# If you added new Python packages:
pip freeze > requirements.txt
git add requirements.txt
git commit -m "update requirements.txt with new packages"
```

### Ending Your Work Session
```bash
# 1. Ensure all changes are committed
git status  # Check for any uncommitted changes
git add .
git commit -m "your final commit message for the session"

# 2. Push your changes to remote
git push origin your-branch-name

# 3. Deactivate virtual environment
deactivate

# Optional but recommended: Create a pull request if your feature is complete
# Go to GitHub > Pull Requests > New Pull Request
# Select: base: main <- compare: your-branch-name
```

## 3. Code Review Process
- Create Pull Requests (PRs) for feature branches into `main`
- Require at least one other team member to review before merging
- Use PR templates to ensure consistency in review process
- After PR approval, use "Squash and merge" to keep history clean

## 4. Project Organization
```
code/
├── data_processing/      # Scripts for data cleaning and preparation
├── visualization/        # Visualization code
├── analysis/            # Analysis scripts
└── utils/               # Shared utility functions

data/
├── raw/                 # Original unmodified data
├── processed/           # Cleaned and transformed data
└── final/              # Final datasets for visualizations

website/
├── assets/             # CSS, JS, and other assets
├── pages/              # Individual page content
└── index.html          # Main entry point
```


## 5. Documentation
Maintain a clear README.md with:
- Project title and team information
- Setup instructions
- Directory structure explanation
- Contribution guidelines

## 6. Communication
- Use GitHub Issues for task tracking
- Create project boards for milestone planning
- Use PR comments for code-specific discussions

## 7. Best Practices
- Write descriptive commit messages
- Keep PRs focused and reasonably sized
- Document code with comments
- Use consistent code formatting (with linters)
- Regular commits and pushes to avoid conflicts

## 8. Conflict Resolution
- Regular team sync-ups to discuss overlapping work
- Clear communication about who is working on what
- Use GitHub's conflict resolution tools when needed

## Example Commit Message Format
```
feat: add data processing script for census data

- Added script to clean and transform census data
- Implemented data validation checks
- Created processed data output in CSV format

Related to #42
```

## Pull Request Template
```markdown
## Description
[Describe the changes you're proposing]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
[Describe how you tested these changes]

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation has been updated
- [ ] All tests pass
- [ ] No merge conflicts with main branch
```