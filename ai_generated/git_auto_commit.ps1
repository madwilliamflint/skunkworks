param (
    [string]$RepoPath
)

if (-not $RepoPath) {
    Write-Host "Usage: git_auto_commit.ps1 -RepoPath <path to repository>"
    exit 1
}

# Navigate to your repository directory
Set-Location -Path $RepoPath

# Get the current branch name
$currentBranch = git symbolic-ref --short HEAD

# Add any new or modified files
git add .

# Add removed files
git ls-files --deleted -z | ForEach-Object { git rm $_ }

# Commit the changes with a boilerplate message
git commit -m "Automated commit of changes."

# Check the most recent tag
$latestTag = git tag --list --sort=-creatordate | Select-Object -First 1

# Get today's date
$today = Get-Date -Format "yyyy-MM-dd"

# Create a new tag if the most recent tag is not today's date and push all changes
if ($latestTag -ne "daily-$today") {
    git tag "daily-$today"
    git push origin "daily-$today"
    # Push the changes to the remote repository
    #git push origin $currentBranch
}

# Push the changes to the remote repository (but commented out as it's now handled above)
git push origin $currentBranch
