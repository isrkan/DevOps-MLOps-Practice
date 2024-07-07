# Git Tutorial for Change Restoring and Commit Tagging

This tutorial will guide you through the process of using Git commands such as restoring changes, viewing differences, and tagging commits. We will learn how to create and modify files, restore changes, view differences, and tag commits.

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
mkdir -p restoring-tagging
cd restoring-tagging
```

### Step 3: Create a new file
Create a new file called sample.txt with some content:

```
echo "This is a sample file." > sample.txt
```

### Step 4: Stage the file
Stage the new file for committing:

```
git add sample.txt
```

### Step 5: Commit the file
Commit the staged file with a descriptive message:

```
git commit -m "Initial commit with sample.txt"
```

### Step 6: Modify the file
Modify the file by adding another line of content:

```
echo "Adding second line to the sample file." >> sample.txt
```

### Step 7: View the differences
To see the changes made to the file since the last commit:

```
git diff sample.txt
```

This command will show the differences between the working directory and the last commit

### Step 8: Stage the file
Stage the modified file for committing:

```
git add sample.txt
```

### Step 9: Modify the file again
Modify the file by adding another line of content:

```
echo "Adding third line to the sample file." >> sample.txt
```

### Step 10: View the differences
To see the changes made to the file:

```
git diff sample.txt
```

This command will show the differences between the working directory and the staging area.

### Step 11: Restore changes
Let's say we want to undo the changes made to sample.txt. We can restore the file to its previous state using the `git restore` command:

```
git restore sample.txt
```

### Step 12: Verify the restoration
Verify that the file has been restored to its previous state by viewing its content:

```
cat sample.txt
```

### Step 13: Stage the modified file again
Stage the modified file for committing:

```
git add sample.txt
```

### Step 14: Commit the changes
Commit the staged changes with a descriptive message:

```
git commit -m "Modified sample.txt with additional content"
```

### Step 15: Tagging a commit
Tagging a commit allows us to mark a specific point in our repository's history. Create a new annotated tag for the last commit:

```
git tag -a v1.0 -m "Version 1.0 release"
```

### Step 16: View the tags
List all tags in the repository to verify that the tag was created:

```
git tag
```

### Step 17: View detailed tag information
View detailed information about the annotated tag:

```
git show v1.0
```

### Step 18: Connect to a remote repository
If we haven't already connected our local repository to a remote repository on GitHub, we can do so with the following command:

```
git remote add origin <remote_repository_url>
```

### Step 19: Push the changes and tags to the remote repository
Push the committed changes and tags to the remote repository:

```
git push origin main
git push origin --tags
```