# Git Tutorial for Branching and Merging

This tutorial will guide you through the process of creating branches, switching between branches, merging changes, and resolving conflicts in a Git repository. We will learn how to manage different features or versions of our project using branches and how to integrate changes from different branches.

## Prerequisites

- Ensure you have Git installed on your machine.
- Make sure you have access to the repository on GitHub.

## Steps

### Step 1: Navigate to the relevant folder
First, navigate to the relevant folder in our local repository:

```sh
cd /path/to/DevOps-MLOps-Practice/DevOps/Git
```

### Step 2: Create a new directory for this tutorial
Create a new directory for this tutorial and navigate into it:

```sh
mkdir -p branching-merging
cd branching-merging
```

### Step 3: Create a new file
Create a new file called `sample.txt` with some content:

```sh
echo "This is the main branch file." > sample.txt
```

### Step 4: Stage and commit the file
Stage the new file for committing:

```sh
git add sample.txt
```

Commit the staged file with a descriptive message:

```sh
git commit -m "Initial commit with sample.txt"
```

### Step 5: Create a new branch
Create a new branch named `feature-branch`:

```sh
git branch feature-branch
```

Branches in Git are like parallel working space. Changes in one branch do not affect other branches until we merge them.

### Step 6: Switch to the new branch
Switch to the newly created `feature-branch`:

```sh
git checkout feature-branch
```

### Step 7: Modify the file in the feature branch
Modify the file by adding another line of content:

```sh
echo "This is a feature branch addition." >> sample.txt
```

### Step 8: Stage and commit the changes in the feature branch
Stage the modified file for committing:

```sh
git add sample.txt
```

Commit the staged changes with a descriptive message:

```sh
git commit -m "Added a line in the feature branch"
```

### Step 9: Switch back to the main branch
Switch back to the `main` branch:

```sh
git checkout main
```

### Step 10: Modify the file in the main branch
Modify the file by adding another line of content:

```sh
echo "This is a main branch addition." >> sample.txt
```

### Step 11: Stage and commit the changes in the main branch
Stage the modified file for committing:

```sh
git add sample.txt
```

Commit the staged changes with a descriptive message:

```sh
git commit -m "Added a line in the main branch"
```

### Step 12: Merge the feature branch into the main branch
Merge the changes from `feature-branch` into the `main` branch:

```sh
git merge feature-branch
```

At this point, we will encounter a merge conflict because both the `main` branch and the `feature-branch` have modified the same part of the file (`sample.txt`).

File content in `main` branch:
```css
This is the main branch file.
This is a main branch addition.
```
File content in `feature-branch`:
```css
This is the main branch file.
This is a feature branch addition.
```

* The first line (`This is the main branch file.`) is the same in both branches, so Git can merge this line without any issue.
* The second line is different in both branches (`This is a main branch addition.` vs. `This is a feature branch addition.`). Git cannot automatically determine which change to keep, resulting in a merge conflict and we will need to resolve this conflict manually.

### Step 13: Resolve merge conflicts
If there are conflicts, we will see a message from Git indicating the files that have conflicts. Open the conflicting file(s) to resolve the conflicts manually. In this example, let's resolve the conflict in `sample.txt`.
First, let's see the conflict markers in sample.txt:

```sh
cat sample.txt
```

The file will look something like this:

```css
This is the main branch file.
<<<<<<< HEAD
This is a main branch addition.
=======
This is a feature branch addition.
>>>>>>> feature-branch
```

The `<<<<<<< HEAD` marker indicates the beginning of the conflicting changes from the current branch (main). The `=======` marker separates the conflicting changes, and the `>>>>>>> feature-branch` marker indicates the end of the conflicting changes from the feature branch.

To resolve the conflict, we need to choose which changes to keep or merge them manually. For example, we can merge both changes and we modify the file directly in the main branch:

```sh
echo "This is the main branch file.
This is a main branch addition.
This is a feature branch addition." > sample.txt
```

This merged version now includes both the main branch and feature branch additions. Now, stage the resolved file:

```sh
git add sample.txt
```

Complete the merge with a commit:

```sh
git commit -m "Resolved merge conflict between main and feature-branch"
```

### Step 14: Verify the merge
Verify that the file contains changes from both branches:

```sh
cat sample.txt
```

### Step 15: Push the changes to the remote repository
Connect to a remote repository if not already connected:

```sh
git remote add origin <remote_repository_url>
```

Push the committed changes to the remote repository:

```sh
git push origin main
```

### Step 16: Delete the feature branch
Once the feature branch has been successfully merged and pushed, we can delete it:

```sh
git branch -d feature-branch
```

Deleting a branch does not delete the commits on that branch; they are still part of the repository's history.

### Step 17: Create and switch to a new branch for another feature
Create and switch to a new branch named `another-feature-branch`:

```sh
git checkout -b another-feature-branch
```

### Step 18: Modify the file in the new feature branch
Modify the file by adding another line of content:

```sh
echo "This is another feature branch addition." >> sample.txt
```

### Step 19: Stage and commit the changes in the new feature branch
Stage the modified file for committing:

```sh
git add sample.txt
```

Commit the staged changes with a descriptive message:

```sh
git commit -m "Added a line in another feature branch"
```

### Step 20: Switch back to the main branch and merge the new feature branch
Switch back to the `main` branch:

```sh
git checkout main
```

Merge the changes from `another-feature-branch` into the `main` branch:

```sh
git merge another-feature-branch
``` 

In this case, we will not encounter a merge conflict because the changes in `another-feature-branch` do not overlap with the changes already in the `main` branch. The changes are in different parts of the file.

File content in `main` branch before merging:
```css
This is the main branch file.
This is a main branch addition.
This is a feature branch addition.
```
File content in `another-feature-branch`:
```css
This is the main branch file.
This is a main branch addition.
This is a feature branch addition.
This is another feature branch addition.
```

* The changes made in `another-feature-branch` are simply an addition to the file, rather than modifying an existing line that was also modified in the `main` branch.
* Since there is no overlap or conflicting modification, Git can automatically merge the changes.

### Step 21: Push the changes to the remote repository
Push the committed changes to the remote repository:

```sh
git push origin main
```

### Step 22: Delete the new feature branch
Once the new feature branch has been successfully merged and pushed, we can delete it:

```sh
git branch -d another-feature-branch
```