# Git Tutorial for Stashing and Applying Changes

This tutorial will guide you through the process of using Git commands to stash and apply changes. Stashing is useful for saving incomplete work temporarily so we can switch branches or work on something else without committing the changes. We will learn how to create stashes, list them, apply or pop them, and clear the stash.

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
mkdir -p stashing-and-applying-changes
cd stashing-and-applying-changes
```

### Step 3: Create a new file
Create a new file called `sample.txt` with some content:

```sh
echo "This is a sample file for stashing tutorial." > sample.txt
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

### Step 5: Connect to a remote repository and push the initial commit
If we haven't already connected our local repository to a remote repository on GitHub, we can do so with the following command:

```sh
git remote add origin <remote_repository_url>
```

Push the committed changes to the remote repository:

```sh
git push -u origin main
```

### Step 6: Modify the file with some changes
Modify the file by adding another line of content:

```sh
echo "This is an uncommitted change." >> sample.txt
```

### Step 7: Stash the changes
Save the uncommitted changes to a stash:

```sh
git stash
```

Stashing is useful when we want to save our work temporarily and come back to it later. The working directory is now clean, and we can switch branches or work on something else.

### Step 8: Verify the stash
List all the stashes to verify that the changes have been stashed:

```sh
git stash list
```

We should see our stash listed with an identifier like `stash@{0}`.

### Step 9: Make another modification and stash it
Modify the file by adding another line of content:

```sh
echo "This is another uncommitted change." >> sample.txt
```

Stash this new change with a descriptive message:

```sh
git stash push -m "Stashing another uncommitted change"
```

### Step 10: Verify the stash again
List all the stashes to verify that the new changes have been stashed:

```sh
git stash list
```

We should now see both stashes listed.

### Step 11: Apply the most recent stash
Apply the most recent stash to your working directory without removing it from the stash list:

```sh
git stash apply
```

This command applies the changes from the most recent stash (`stash@{0}`) to our working directory.

### Step 12: Verify the applied changes
Check the contents of `sample.txt` to ensure that the changes have been applied:

```sh
cat sample.txt
```

### Step 13: Clear the working directory
Clear the working directory by resetting the changes:

```sh
git reset --hard
```

### Step 14: Apply a specific stash
Apply a specific stash by its identifier. First, verify the list of stashes:

```sh
git stash list
```

Then apply the specific stash (e.g., `stash@{1}`):

```sh
git stash apply stash@{1}
```

### Step 15: Pop a stash
Pop the most recent stash and remove it from the stash list:

```sh
git stash pop
```

This command applies the changes from the most recent stash (`stash@{0}`) and then removes it from the stash list.

### Step 16: Verify the stashes again
List all the stashes to verify that the stash has been popped:

```sh
git stash list
```

We should see that the stash we popped is no longer listed.

### Step 17: Clear all stashes
Clear all stashes from the stash list:

```sh
git stash clear
```

### Step 18: Verify that all stashes are cleared
List all the stashes to ensure that they have been cleared:

```sh
git stash list
```

We should see no stashes listed.

### Step 19: Stash only certain files
Sometimes we may want to stash only certain files and leave others untouched. Let's modify `sample.txt` again and create a new file `example.txt`:

```sh
echo "This is another uncommitted change in sample.txt." >> sample.txt
echo "This is an uncommitted change in example.txt." > example.txt
```

Now, stash only the changes in `sample.txt`:

```sh
git stash push -m "Stashing only sample.txt" sample.txt
```

Verify the stash:

```sh
git stash list
```

### Step 20: Stash with untracked files
By default, git stash does not include untracked files. To include them, use the `-u` option:

```sh
git stash push -u -m "Stashing with untracked files"
```

Verify the stash:

```sh
git stash list
```

### Step 21: Create a branch from a stash
Sometimes we may want to create a new branch from a stash. First, apply the stash:

```sh
git stash apply stash@{0}
```

Then create a new branch and commit the changes:

```sh
git checkout -b new-feature
git add .
git commit -m "Committing stashed changes to new-feature branch"
```

Push the new branch to the remote repository:

```sh
git push origin new-feature
```

### Step 22: Stash and switch branches
Let's modify `sample.txt` again:

```sh
echo "This is a temporary change before switching branches." >> sample.txt
```

Stash the changes and switch to a new branch:

```sh
git stash
git checkout -b another-branch
```

Apply the stash in the new branch:

```sh
git stash apply
```

Commit and push the changes:

```sh
git add sample.txt
git commit -m "Applied stashed changes in another-branch"
git push origin another-branch
```

### Step 23: Merging branches:

##### Merging new-feature into main
Checkout the `main`  branch:

```sh
git checkout main
```

Merge the `new-feature` branch into main:

```sh
git merge new-feature
```

Push the merged `main` branch:

```sh
git push origin main
```

After merging or if a branch is no longer needed, you can delete it locally:

```sh
git branch -d new-feature
```

And also delete it from GitHub:

```sh
git push origin --delete new-feature
```

##### Merging new-feature into main
Now, merge the `another-branch` branch into main:

```sh
git merge another-branch
```

Push the merged `main` branch:

```sh
git push origin main
```

After merging or if a branch is no longer needed, you can delete it locally:

```sh
git branch -d another-branch
```

And also delete it from GitHub:

```sh
git push origin --delete another-branch
```