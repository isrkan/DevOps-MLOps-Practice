# Git Tutorial for File Staging and Committing

This tutorial will guide you through the process of staging and committing a file to a Git repository step-by-step. We will learn how to navigate directories, create and stage files, commit changes, and push them to a remote repository.

## Prerequisites

- Ensure you have Git installed on your machine.
- Make sure you have access to the repository on GitHub.

## Steps

### Step 1: Navigate to the relevant folder
First, navigate to the relevant folder in our local repository:

```
cd /path/to/DevOps-MLOps-Practice/DevOps/Git
```

### Step 2: Create a new directory for this tutorial
Create a new directory for this tutorial and navigate into it:

```
mkdir -p staging-and-committing
cd staging-and-committing
```

### Step 3: Create a new file
Create a new file called sample.txt with some content:

```
echo "This is a sample file." > sample.txt
```

### Step 4: Stage the file
Staging the file means preparing it for the next commit. We need to add the file to the staging area:

```
git add sample.txt
```

To verify that the file has been staged, we can use:

```
git status
```

### Step 5: Commit the file
Committing the file means saving the staged changes to the repository with a descriptive message:

```
git commit -m "Initial commit with sample.txt"
```

### Step 6: Connect to a remote repository
If we haven't already connected our local repository to a remote repository on GitHub, we can do so with the following command:

```
git remote add origin <remote_repository_url>
```

`origin` is the name or alias given to the remote repository. We can choose a different name, but 'origin' is conventional and widely used as the default.

### Step 7: Push the changes to the remote repository
Push the committed changes to the remote repository. This updates the remote repository with our local changes:

```
git push origin main
```

If this is the first push to a new repository or branch, we may need to set the upstream branch:

```
git push -u origin main
```