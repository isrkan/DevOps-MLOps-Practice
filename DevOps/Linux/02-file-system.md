# The Linux Filesystem 

One of the biggest mental shifts when moving from Windows to Linux is how files and directories are organized. In Windows, we have multiple drives (`C:\`, `D:\`) each with their own tree of folders. In Linux, everything lives under a single root — literally a single `/` from which the entire filesystem branches out. Once this concept clicks, navigating Linux becomes natural and intuitive.

This guide covers the Linux filesystem hierarchy, how to navigate it, and all the essential commands for working with files and directories.

---

## The Single-Root Filesystem
In Linux, there are no drive letters. There is one root, written as `/`, and everything — every file, directory, device, and even running process information — exists somewhere under that root.

```
/
├── home/
│   └── username/       ← our personal directory
├── etc/                ← configuration files
├── var/                ← variable data (logs, databases)
├── tmp/                ← temporary files
├── bin/                ← essential system commands
├── sbin/               ← system administration commands
├── lib/                ← system libraries
├── usr/                ← user-installed software
├── opt/                ← optional third-party software
├── boot/               ← kernel and boot files
├── proc/               ← virtual filesystem (process info)
├── dev/                ← device files
├── mnt/                ← mount points for external drives
└── media/              ← auto-mounted removable media
```

When we connect to a remote Linux server, access a Docker container, or look at a cloud VM — they all share this same structure. Learning it once means we know it everywhere.

---

## Key Directories Explained
Understanding what lives in each directory helps us know where to look when we need something.

#### / — The root directory
The very top of the filesystem tree. Everything is inside `/`. We never store our personal files here — it belongs to the system.

#### /home — User home directories
Each regular user gets a directory here: `/home/alice`, `/home/bob`. This is where personal files, downloads, and user-specific configuration files live. When we open a terminal in WSL, we start in our home directory.

#### /root — The root user's home
The **root** user (the superuser / administrator) has its own home directory at `/root`, not `/home/root`. This is intentional — separating the root user's files from regular users.

#### /boot — Boot files
Contains the Linux kernel and the files needed to start the system (the bootloader, initial RAM disk, etc.). We rarely touch this directly — it's managed by the system and the package manager when the kernel is updated. On WSL, this directory may be empty or minimal since WSL uses a kernel provided by Windows.

#### /etc — System-wide configuration files
This is one of the most important directories. Almost every program that runs on Linux reads its configuration from somewhere in `/etc`. For example:
- `/etc/hostname` — the machine's hostname
- `/etc/hosts` — local DNS mappings
- `/etc/apt/sources.list` — APT package repositories
- `/etc/passwd` — user account information
- `/etc/ssh/sshd_config` — SSH server configuration

The name "etc" comes from old Unix conventions meaning "et cetera" (everything else), but in practice it's the configuration directory.

#### /var — Variable data
Files that change frequently at runtime live here:
- `/var/log/` — system and application log files
- `/var/lib/` — persistent data for applications (e.g., databases)
- `/var/cache/` — cached data from programs
- `/var/spool/` — queued data like print jobs or mail

When debugging problems, `/var/log/` is one of the first places we look.

#### /tmp — Temporary files
Programs use `/tmp` to store temporary files. The contents of `/tmp` are usually cleared on every reboot. We can use it freely for temporary work, but we should never store anything important here.

#### /bin and /usr/bin — Executable programs (commands)
Both directories hold **binaries** — compiled programs and executable scripts that we run as commands in the terminal. The difference is which binaries go where:

- `/bin` holds the **essential** commands needed for the system to function at a basic level, even before other filesystems are mounted or in recovery mode. These are tools like `ls`, `cp`, `mv`, `cat`, `bash`, `mkdir`, and `rm`.
- `/usr/bin` holds the **rest** — the majority of user-facing programs like `python3`, `git`, `vim`, `curl`, and `gcc`. This is where most software installed via `apt` ends up.

The split is historical: on older Unix systems, `/usr` could live on a separate disk that mounted *after* boot, so `/bin` had to contain everything needed to bring the system up. On modern Ubuntu/Debian, `/bin` is actually a symbolic link to `/usr/bin`, so they're effectively the same directory — but the conceptual distinction still appears in documentation and other distributions.

#### /lib and /lib64 — System libraries
These contain shared libraries that programs in `/bin` and `/sbin` depend on. `/lib64` holds 64-bit libraries on 64-bit systems. We don't edit these manually — the package manager keeps them in sync with the programs that need them. On modern Ubuntu, `/lib` is a symbolic link to `/usr/lib`, just like `/bin` points to `/usr/bin`.

#### /sbin and /usr/sbin — System administration commands
While `/bin` and `/usr/bin` hold everyday commands any user runs (`ls`, `cp`, `cat`), `/sbin` and `/usr/sbin` hold commands meant for system administration — things like `fdisk` (partition disks), `iptables` (firewall), or `useradd` (create users). These typically require `sudo` to run because they affect the whole system.

#### /usr — User programs and data
`/usr` is a large directory containing most of the software installed on the system:
- `/usr/bin/` — programs
- `/usr/lib/` — libraries
- `/usr/share/` — shared data (documentation, icons, locales)
- `/usr/local/` — software we compile and install ourselves (not via apt)

#### /opt — Optional third-party software
Large software packages that want to install themselves in one place (like Google Chrome, JetBrains IDEs, or some ML frameworks) often use `/opt`. Each package gets its own subdirectory: `/opt/google/`, `/opt/jetbrains/`, etc.

#### /proc — Virtual process filesystem
This is not a real directory on disk — it's a virtual filesystem created by the kernel at runtime. It exposes information about running processes and system hardware as files:
- `/proc/cpuinfo` — CPU details
- `/proc/meminfo` — memory details
- `/proc/<PID>/` — information about a specific running process

We can read these files with `cat` to inspect the system at a very low level.

#### /dev — Device files
Linux represents hardware devices as files. Our hard drive might be `/dev/sda`, our first partition `/dev/sda1`, USB drives `/dev/sdb`, and so on. There are also special devices like `/dev/null` (discards everything written to it) and `/dev/random` (generates random bytes).

#### /mnt and /media — Mount points
When we plug in a USB drive or mount a network share, it appears under one of these directories. In WSL, our Windows drives are accessible under `/mnt/`:
- `/mnt/c/` — our Windows C: drive
- `/mnt/d/` — our Windows D: drive (if it exists)

#### How applications organize their own files
Many applications follow the same `bin` / `etc` / `lib` convention as the system itself. For example, an application installed under `/opt/myapp/` typically organizes itself like this:
- `/opt/myapp/bin/` — the application's programs
- `/opt/myapp/etc/` — its configuration files
- `/opt/myapp/lib/` — its libraries
- `/opt/myapp/logs/` — its log files

The same pattern shows up under `/usr/local/` for software we compile and install ourselves. Once we recognize this layout, exploring an unfamiliar application on the system becomes much easier — we know where to look for its commands, its config, and its logs.

---

## Absolute vs Relative Paths
Before we learn to navigate, we need to understand the difference between **absolute** and **relative** paths.

#### Absolute paths
An absolute path starts from the root `/` and specifies the full location of a file:

```bash
/home/username/Documents/notes.txt
/etc/hosts
/var/log/syslog
```

Absolute paths work from anywhere in the filesystem. They always mean the same thing regardless of where we currently are.

#### Relative paths
A relative path is specified *relative to our current location*. If we're currently in `/home/username/`, then:

```bash
Documents/notes.txt      # means /home/username/Documents/notes.txt
../alice/                # means /home/alice/ (go up one level, then into alice/)
./script.sh              # means /home/username/script.sh (. means current dir)
```

Special relative path symbols:
- `.` — The current directory
- `..` — The parent directory (one level up)
- `~` — Our home directory (absolute shorthand)

---

## Navigating the Filesystem

#### pwd — Where are we?
Before we go anywhere, let's confirm our current location:

```bash
pwd
```

The output shows our current absolute path, e.g., `/home/username`.

#### ls — List directory contents
`ls` shows us what's inside a directory. By default, it lists the current directory:

```bash
ls
```

To list a specific directory:

```bash
ls /etc
```

`ls` becomes far more useful with options:

```bash
ls -l
```

The `-l` flag shows a **long listing** with one item per line, including permissions, owner name, group name, size, modification date and file name. Example output:

```
drwxr-xr-x 2 alice alice 4096 Apr  1 10:30 Documents
-rw-r--r-- 1 alice alice  220 Mar 15 08:00 .bash_logout
```

More useful options:

```bash
ls -a
```

The `-a` flag shows **all** files, including hidden ones (files starting with `.`).

```bash
ls -lh
```

`-h` makes file sizes **human-readable** (shows KB, MB, GB instead of raw bytes).

```bash
ls -lt
```

`-t` sorts by **modification time**, newest first — useful for finding recently changed files.

```bash
ls -lR
```

`-R` lists **recursively** — shows all contents of all subdirectories.

We can combine options freely. Our most common usage will likely be:

```bash
ls -lah
```

This shows all files (including hidden), in long format, with human-readable sizes.

```bash
ls -F
```

The `-F` flag appends a **classifier symbol** to each entry, telling us at a glance what kind of file it is — without needing the full detail of `-l`. The symbols are:
- `/` — a directory
- `*` — an executable file (a program or script with execute permission)
- `@` — a symbolic link (symlink)
- `|` — a named pipe (FIFO)
- `=` — a socket
- `>` — a door (rare, mostly on Solaris)
- *(no symbol)* — a regular file

#### cd — Change directory
`cd` moves us to a different directory:

```bash
cd /etc
```

Now our prompt shows `/etc`. To go back to our home directory:

```bash
cd ~
```

Or simply:

```bash
cd
```

Running `cd` without any argument always takes us home. To go up one directory level:

```bash
cd ..
```

To go up two levels:

```bash
cd ../..
```

To go back to the previous directory we were in (very useful!):

```bash
cd -
```

This toggles between our current and previous locations, like the "back" button in a browser.

#### tree — Visual directory structure
`tree` displays directories and their contents in a visual tree format. We may need to install it first:

```bash
sudo apt install tree
```

Then:

```bash
tree /home/username
```

Output:

```
/home/username
├── Documents
│   ├── notes.txt
│   └── report.pdf
├── Downloads
└── projects
    └── webapp
        ├── app.py
        └── requirements.txt
```

Useful options:
- `tree -L 2` — limit to 2 levels deep
- `tree -a` — show hidden files
- `tree -d` — show directories only

---

## Creating Files and Directories

#### mkdir — Make a new directory
To create a new directory:

```bash
mkdir projects
```

To create nested directories in one command (very useful!), we use `-p` which creates parent directories as needed:

```bash
mkdir -p projects/webapp/templates
```

Without `-p`, this would fail if `projects/` or `webapp/` didn't already exist.

To create multiple directories at once:

```bash
mkdir docs logs backups
```

#### touch — Create an empty file (or update timestamps)
`touch` creates a new, empty file if it doesn't exist. If the file already exists, it just updates its last-modified timestamp without changing the contents.

```bash
touch notes.txt
```

Create multiple files at once:

```bash
touch index.html style.css app.js
```

`touch` is commonly used to create placeholder files or to trigger file-watcher tools.

---

## Copying, Moving, and Deleting

#### cp — Copy files and directories
To copy a file:

```bash
cp notes.txt notes_backup.txt
```

To copy a file to a different directory:

```bash
cp notes.txt ~/Documents/
```

To copy a file and rename it in the destination:

```bash
cp notes.txt ~/Documents/important_notes.txt
```

To copy an entire directory and its contents, we must use `-r` (recursive):

```bash
cp -r projects/ projects_backup/
```

Useful options:
- `-i` — **interactive**: ask before overwriting an existing file
- `-v` — **verbose**: print what's being copied
- `-u` — only copy if the source is newer than the destination (useful for syncing)

```bash
cp -rv projects/ projects_backup/
```

#### mv — Move or rename files and directories
`mv` both moves files to a new location and renames them. Linux doesn't have a separate "rename" command — moving and renaming are the same operation.

To rename a file:

```bash
mv notes.txt important_notes.txt
```

To move a file to a different directory:

```bash
mv notes.txt ~/Documents/
```

To move and rename at the same time:

```bash
mv notes.txt ~/Documents/important_notes.txt
```

To move a directory:

```bash
mv old_project/ ~/projects/new_project/
```

Unlike `cp`, `mv` doesn't need `-r` for directories.

#### rm — Remove (delete) files and directories
`rm` deletes files. **Unlike Windows, Linux does not have a Recycle Bin. Deletion is permanent.**

To delete a file:

```bash
rm notes.txt
```

To delete multiple files:

```bash
rm file1.txt file2.txt file3.txt
```

To delete a directory and all its contents (be careful!):

```bash
rm -r old_project/
```

Useful options:
- `-i` — **interactive**: ask before deleting each file (great for safety)
- `-v` — **verbose**: print what's being deleted
- `-f` — **force**: skip prompts and delete without confirmation (use with caution!)

**Safety tip:** When deleting directories with `rm -r`, it's good practice to use `-i` to confirm what's being deleted, especially if using wildcards. A habit of `rm -ri <directory>` can save us from accidental data loss.

**Never run** `rm -rf /` or `rm -rf /*` — these would delete the entire filesystem.

---

## Viewing File Contents
We often need to read the contents of files without opening a text editor.

#### cat — Display entire file contents
`cat` (concatenate) prints the entire contents of a file to the terminal:

```bash
cat notes.txt
```

For multiple files, it prints them one after another:

```bash
cat file1.txt file2.txt
```

`cat` is great for short files. For long files, the output will scroll past too quickly — use `less` instead.

#### less — Read files page by page
`less` opens a file for reading with pagination. We can scroll through it and search within it:

```bash
less /var/log/syslog
```

Inside `less`:
- `Space` or `f` — scroll down one page
- `b` — scroll up one page
- Arrow keys — scroll line by line
- `/pattern` — search forward for a pattern
- `n` — next search match
- `N` — previous search match
- `g` — jump to beginning
- `G` — jump to end
- `q` — quit

`less` is our go-to tool for reading long log files or configuration files.

#### head — Show the beginning of a file
`head` prints the first 10 lines of a file by default:

```bash
head /var/log/syslog
```

To show a different number of lines, use `-n`:

```bash
head -n 20 /var/log/syslog
```

#### tail — Show the end of a file
`tail` prints the last 10 lines by default — very useful for checking the most recent log entries:

```bash
tail /var/log/syslog
```

The `-f` flag is extremely useful: it **follows** the file in real time, printing new lines as they're added. This is how we watch logs live:

```bash
tail -f /var/log/syslog
```

Press `Ctrl+C` to stop following.

Combined:

```bash
tail -n 50 -f /var/log/syslog
```

This shows the last 50 lines and then follows new output.

---

## Getting File Information

#### file — Determine file type
Linux doesn't rely on file extensions to know what a file is. The `file` command inspects the actual file contents and reports its type:

```bash
file image.png
file script.sh
file archive.tar.gz
```

Output might be:

```
image.png: PNG image data, 1920 x 1080, 8-bit/color RGBA
script.sh: Bourne-Again shell script, ASCII text executable
archive.tar.gz: gzip compressed data
```

This is useful when we have files with no or wrong extensions.

#### stat — Detailed file metadata
`stat` shows detailed metadata about a file: size, permissions, owner, timestamps:

```bash
stat notes.txt
```

Output:

```
  File: notes.txt
  Size: 1024       Blocks: 8          IO Block: 4096   regular file
Device: 8,1        Inode: 1234567     Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/  alice)   Gid: ( 1000/  alice)
Access: 2024-04-01 10:30:00
Modify: 2024-03-28 15:20:00
Change: 2024-03-28 15:20:00
```

#### wc — Count lines, words, and characters
`wc` (word count) counts the number of lines, words, and characters in a file:

```bash
wc notes.txt
```

Output: `42 156 987 notes.txt` (lines, words, characters)

Useful options:
- `wc -l` — count lines only (great for counting log entries, CSV rows, etc.)
- `wc -w` — count words only
- `wc -c` — count characters/bytes only

```bash
wc -l /var/log/syslog
```

---

## Hidden Files

In Linux, any file or directory whose name starts with a `.` (dot) is **hidden**. It won't appear in normal `ls` output — we need `ls -a` to see it.

```bash
ls -a ~
```

It lists all files (including hidden ones) located in the home directory. Output might include:

```
.  ..  .bash_history  .bashrc  .profile  .ssh  Documents  Downloads
```

Hidden files are typically configuration files for applications. Common ones in our home directory:
- `.bashrc` — shell configuration (run when we open a terminal)
- `.bash_history` — our command history
- `.profile` — environment setup for login shells
- `.ssh/` — SSH keys and configuration
- `.gitconfig` — Git configuration

These aren't "hidden" for security — they're hidden to keep directory listings clean. Anyone with access to our home directory can see them with `ls -a`.

---

## Working with Spaces in Filenames
In Linux, spaces in filenames cause a specific kind of trouble because the shell uses whitespace to separate arguments. When we type `cp my file.txt backup/`, the shell sees *three* arguments — `my`, `file.txt`, and `backup/` — not two. The result is a confusing error like `cp: cannot stat 'my': No such file or directory`.

Linux conventions favor filenames without spaces (using `_` or `-` instead), but we'll still run into spaces constantly when working with files copied from Windows, downloaded from the web, or shared by non-technical users. Here are the ways to handle them.

#### Quoting with double quotes
Wrapping the path in `"..."` tells the shell to treat everything inside as a single argument:

```bash
cd "My Documents"
cp "vacation photo.jpg" ~/Pictures/
rm "old report (final).pdf"
```

#### Quoting with single quotes
Single quotes work the same way for spaces, with one important difference: single quotes also disable variable expansion, so `$HOME` stays literal instead of being replaced with the home directory path.

```bash
cat 'meeting notes.txt'
```

For paths with plain spaces, either quote style works fine.

#### Escaping with a backslash
We can also "escape" each space by putting a `\` directly before it. The backslash tells the shell that the next character is literal, not a separator:

```bash
cd My\ Documents
cp vacation\ photo.jpg ~/Pictures/
```

This style is shorter for one-off use but harder to read when there are multiple spaces. Quoting is usually clearer.

#### Let tab completion do it for us
Here's the easy way: **just use tab completion**. If we type `cd My` and press `Tab`, the shell automatically inserts the backslashes for us, producing `cd My\ Documents/`. We never have to think about quoting at all when we let `Tab` do the work — yet another reason to make tab completion a habit.

#### Other tricky characters
Spaces aren't the only characters the shell treats specially. Parentheses `( )`, ampersands `&`, dollar signs `$`, asterisks `*`, and quotes themselves can all cause similar issues. The same solutions apply — quote the whole path or escape the offending character with `\`. When in doubt, wrap the whole path in single quotes:

```bash
ls 'report (draft) & notes.txt'
```

---

## Wildcards and Globbing

**Wildcards** (also called **glob patterns**) let us match multiple files by pattern instead of typing each name individually.

#### `*` — Match any number of characters
To list all `.txt` files in the current directory:

```bash
ls *.txt
```

To delete all log files:

```bash
rm *.log
```

To copy all Python files to a backup directory:

```bash
cp *.py backup/
```

`*` matches zero or more of any character. `*.txt` matches `notes.txt`, `report.txt`, `a.txt`, but not `notes.md`.

#### `?` — Match exactly one character
`?` matches exactly one character. `file?.txt` matches `file1.txt`, `fileA.txt`, but not `file10.txt`:

```bash
ls file?.txt
```

#### `[abc]` — Match one character from a set
To match files starting with `a`, `b`, or `c`:

```bash
ls [abc]*.txt
```

To match files with a digit at a specific position:

```bash
ls report[0-9].txt
```

#### `{a,b}` — Match one of the listed patterns (brace expansion)
To create multiple directories at once:

```bash
mkdir {images,videos,docs}
```

To copy two specific files:

```bash
cp {report.txt,summary.txt} ~/Documents/
```

**Caution with wildcards:** Before running a destructive command like `rm` with wildcards, run `ls` with the same pattern first to confirm what we're about to delete:

```bash
ls *.log        # check what would be deleted
rm *.log        # now delete
```

---

## Hard Links and Symbolic Links
Linux supports two types of links — ways to have a filename point to the same file content.

#### Hard links
A **hard link** is an additional name for an existing file. Both the original file and the hard link point to the same data on disk. If we delete the original filename, the data is still accessible through the hard link.

```bash
ln original.txt hardlink.txt
```

Hard links have limitations: they can't span different filesystems and can't be used for directories.

#### Symbolic links (symlinks)
A **symbolic link** (or symlink) is like a shortcut — it's a special file that points to another file or directory by path. If the original is deleted, the symlink becomes a "broken link."

```bash
ln -s /path/to/original.txt shortcut.txt
```

To create a symlink to a directory:

```bash
ln -s /usr/share/myapp myapp
```

Symlinks are very common in Linux system configuration. To see where a symlink points:

```bash
ls -l myapp
```

Output: `lrwxrwxrwx 1 alice alice 18 Apr 1 10:00 myapp -> /usr/share/myapp`

---

## Accessing Windows Files from WSL
One of the most useful WSL features is that our Windows filesystem is accessible from inside Linux. Our Windows drives are mounted under `/mnt/`:

- `/mnt/c/` — Windows C: drive
- `/mnt/d/` — Windows D: drive (if present)

So our Windows user files are at:

```bash
ls /mnt/c/Users/<WindowsUsername>/
```

We can copy files between Windows and Linux:

```bash
# Copy from Windows to our Linux home directory
cp /mnt/c/Users/Alice/Documents/report.txt ~/Documents/

# Copy from Linux to Windows Desktop
cp ~/script.sh /mnt/c/Users/Alice/Desktop/
```

**Performance note:** File operations on `/mnt/c/` are slower than operations on native Linux files (inside `~/`). For development work, we should keep project files inside our Linux home directory (`~/`) and only use `/mnt/c/` for copying files to/from Windows.