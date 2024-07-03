# Git Commands Guide

This repository contains a list of essential Git and GitHub commands to help you get started and manage your repositories effectively.

### Git basics

##### Checking Git version
This command checks the currently installed version of Git.

```
git --version
```

##### Configuring Git
Set up your Git configuration with your username and email.

```
git config --global user.name "My Name"
git config --global user.email "my.email@example.com"
```

##### Initializing a repository
This command creates a new Git repository in the current directory.

```
git init
```

##### Cloning a repository
This command copies a Git repository from a remote server to our local machine.

```
git clone <repository_url>
```

To clone a repository into a specific directory, you can use the following syntax:

```
git clone <repository_url> <target_directory>
```

Options:

* `--branch <branch>` or `-b <branch>`: Clone a specific branch.
* `--depth <depth>`: Create a shallow clone with a history truncated to the specified number of commits.
* `--single-branch`: Clone only the history leading to the tip of a single branch.
* `--recurse-submodules`: Initialize and clone any submodules within the repository.
* `--no-checkout`: Clone the repository without checking out the files. This can be useful for creating a repository snapshot without consuming space for files. You can later check out files manually using git checkout.

##### Adding files
This command stages changes (new files, modified files, or deleted files) to be committed.

```
git add <file_name>
```

To add all changes in the current directory and subdirectories:

```
git add .
```

##### Committing changes
This command saves the staged changes to the repository with a descriptive message.

```
git commit -m "Commit message"
```

##### Viewing the commit history
This command shows the commit history for the current branch.

```
git log
```

- `-p` - This displays the differences (patches) introduced in each commit, showing what has been added or removed in the code.

##### Restoring changes
This command discards changes in the working directory and it is useful to undo changes to files. To discard changes to the specified file:

```
git restore <file_name>
```

To discard changes to all files in the working directory:

```
git restore .
```

### Sparse checkout

Sparse checkout allows us to check out only a portion of the files in a repository. This can be useful when dealing with large repositories where we do not need all the files.

##### Initializing sparse checkout
This command initializes sparse checkout in the current repository.

```
git sparse-checkout init
```

Options:
* `--cone`: Enable cone mode, which simplifies the sparse-checkout patterns to include only directories and files at the root level.
* `--no-cone`: Disable cone mode, using more complex sparse-checkout patterns.

##### Setting sparse checkout patterns
This command sets the sparse checkout patterns, specifying which files and directories to include in the working directory.

```
git sparse-checkout set <patterns>
```

For example, `git sparse-checkout set src/ docs/`. This includes only the `src/` and `docs/` directories in the working directory.

### Branching and merging

##### Creating a new branch
This command creates a new branch in the repository.

```
git branch <branch_name>
```

##### Switching branches
This command changes the current working branch.

```
git checkout <branch_name>
```

##### Creating and switching to a new branch
This command creates a new branch and immediately switches to it.

```
git checkout -b <branch_name>
```

##### Merging branches
This command merges the specified branch into the current branch.

```
git merge <branch_name>
```

##### Deleting a branch
This command deletes the specified branch.

```
git branch -d <branch_name>
```

### Remote repositories

##### Adding a remote repository
This command adds a remote repository to our local repository.

```
git remote add <remote_name> <repository_url>
```

##### Viewing remote repositories
This command lists all remote repositories associated with our local repository.

```
git remote -v
```

##### Fetching changes from a remote repository
This command fetches changes from the remote repository but does not merge them into our local branch.

```
git fetch <remote_name>
```

##### Pulling changes from a remote repository
This command fetches changes from the remote repository and merges them into our local branch.

```
git pull <remote_name> <branch_name>
```

Options:
* `--no-commit`: Merge changes but do not automatically create a new commit.
* `--all`: Fetch changes from all remotes.

##### Pushing changes to a remote repository
This command pushes our local changes to the remote repository.

```
git push <remote_name> <branch_name>
```

Options:
* `--set-upstream` or `-u`: Sets the remote branch as the upstream branch for the current local branch.
* `--tags`: Push all local tags to the remote repository.
* `--force` or `-f`: Force push the changes, overwriting changes on the remote repository. Use with caution.


### Stashing changes

##### Stashing changes
This command temporarily saves our local changes, allowing us to work on something else or switch branches without committing the changes.

```
git stash
```

##### Applying stashed changes
This command reapplies the most recently stashed changes to our working directory.

```
git stash apply
```

##### Listing stashes
This command shows a list of all stashed changes.

```
git stash list
```

##### Dropping a stash
This command deletes a specific stash from the list.

```
git stash drop <stash_id>
```

### Working with tags

##### Creating a tag
This command creates a new tag for a specific commit.

```
git tag -a <tag_name> -m "Tag message"
```

##### Listing tags
This command lists all tags in the repository.

```
git tag
```

##### Pushing tags to a remote repository
This command pushes all tags to the remote repository.

```
git push <remote_name> --tags
```

### GitHub collaboration

##### Forking a repository
Forking a repository creates a copy of a repository under our own GitHub account. This can be done through the GitHub website by clicking the "Fork" button on the repository page.

##### Creating a pull request
After making changes to our forked repository, we can create a pull request to propose our changes to the original repository. This can be done through the GitHub website by navigating to the "Pull requests" tab and clicking "New pull request".

##### Reviewing and merging pull requests
Repository maintainers can review pull requests, provide feedback, and merge the changes if they are satisfactory. This process is managed through the GitHub website.

### Additional commands

##### Viewing the status of our working directory
This command shows the status of our working directory, including staged, unstaged, and untracked files.

```
git status
```

##### Viewing changes
This command shows the changes made to files.

```
git diff
```

##### Viewing changes of a specific file
This command shows the changes made to a specific file.

```
git diff <file_name>
```

##### Discarding changes in a working directory
This command discards changes in the working directory.

```
git checkout -- <file_name>
```