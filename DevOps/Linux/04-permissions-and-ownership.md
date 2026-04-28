# File Permissions and Ownership

Linux was designed from the ground up as a **multi-user system**. Multiple users can be logged in at the same time, running their own programs, accessing their own files. To prevent users from reading each other's private data, breaking system files, or running dangerous programs, Linux implements a detailed **permissions system** that controls exactly what each user can do with every file.

Understanding permissions is not just an administrative task — it's a fundamental Linux skill. We'll encounter permission errors constantly, and knowing how to read and fix them makes us far more productive.

---

## Why Permissions Exist
Imagine a shared server with a hundred users. Without permissions:
- Any user could read everyone else's private files
- Any user could delete or modify system configuration files
- Any user could replace system executables with malicious programs

The permission system prevents all of this. Every file and directory has:
1. An **owner** (a specific user)
2. A **group** (a group of users)
3. **Permission bits** specifying what the owner, the group, and everyone else can do

---

## Reading Permission Strings
When we run `ls -l`, each file is displayed with a 10-character permission string on the left:

```bash
ls -l
```

Output:

```
drwxr-xr-x 2 alice devs 4096 Apr  1 10:30 Documents
-rw-r--r-- 1 alice devs  220 Mar 15 08:00 notes.txt
-rwxr-xr-- 1 alice devs 8192 Apr  2 09:15 script.sh
lrwxrwxrwx 1 alice devs   12 Apr  3 11:00 link -> /etc/hosts
```

Let's dissect the string `drwxr-xr-x`:

#### Position 1 — File type
The first character tells us what type of file this is:

| Character | Type |
|-----------|------|
| `-` | Regular file |
| `d` | Directory |
| `l` | Symbolic link |
| `c` | Character device (e.g., terminal) |
| `b` | Block device (e.g., hard disk) |
| `p` | Named pipe |
| `s` | Socket |

#### Positions 2–10 — Permission triplets
The remaining 9 characters are three groups of three, representing permissions for three different parties:

```
d     rwx    r-x    r-x
↑     ↑      ↑      ↑
type  owner  group  others
```

Each triplet has three positions: **r** (read), **w** (write), **x** (execute). A `-` means that permission is not granted.

| Permission | File | Directory |
|------------|------|-----------|
| `r` (read) | Can read the file contents | Can list the directory (`ls`) |
| `w` (write) | Can modify the file contents | Can create, rename, delete files inside |
| `x` (execute) | Can run the file as a program | Can enter the directory (`cd`) and access its contents |

**Important:** For a directory, the `x` (execute) bit means "can enter and access." Without it, even if we can read the directory listing, we can't actually access any files inside it.

#### Example breakdown

```
-rw-r--r--  alice  devs  notes.txt
```

- `-` — regular file
- `rw-` — owner (alice) can read and write, but NOT execute
- `r--` — group (devs) can only read
- `r--` — others can only read

```
drwxr-x---  alice  devs  private/
```

- `d` — directory
- `rwx` — owner (alice) can read, write (create/delete files), and enter
- `r-x` — group (devs) can list and enter, but NOT create/delete files
- `---` — others have NO permissions at all

---

## Understanding Octal (Numeric) Permissions
Each permission is a bit that is either on (1) or off (0). The three bits in each triplet can be represented as a number from 0 to 7:

| Permission | Bits | Octal Value |
|------------|------|-------------|
| `---` | 000 | 0 |
| `--x` | 001 | 1 |
| `-w-` | 010 | 2 |
| `-wx` | 011 | 3 |
| `r--` | 100 | 4 |
| `r-x` | 101 | 5 |
| `rw-` | 110 | 6 |
| `rwx` | 111 | 7 |

So a full permission set like `rwxr-xr--` becomes: owner=7, group=5, others=4 → **`754`**

The most common permission patterns:
- **`755`** (`rwxr-xr-x`) — Standard for directories and executable scripts: owner has full control, everyone else can read and execute
- **`644`** (`rw-r--r--`) — Standard for regular files: owner can read/write, everyone else can only read
- **`700`** (`rwx------`) — Private: only the owner has any access
- **`600`** (`rw-------`) — Private file: only owner can read/write (used for SSH private keys!)
- **`777`** (`rwxrwxrwx`) — Full access for everyone (avoid this for security reasons)

---

## chmod — Changing Permissions
`chmod` (change mode) changes the permission bits of a file or directory.

### Symbolic mode (human-readable)
Symbolic mode uses letters and operators:
- **Who:** `u` (user/owner), `g` (group), `o` (others), `a` (all three)
- **Operator:** `+` (add permission), `-` (remove permission), `=` (set exactly)
- **Permission:** `r`, `w`, `x`

To make a script executable by the owner:

```bash
chmod u+x script.sh
```

To make a file readable by everyone:

```bash
chmod a+r notes.txt
```

To remove write permission from group and others:

```bash
chmod go-w config.txt
```

To set the group permission to read-only exactly (removes any existing write/execute):

```bash
chmod g=r config.txt
```

To add execute permission for everyone:

```bash
chmod a+x deploy.sh
```

### Octal mode (numeric)
Octal mode sets all permissions at once with a 3-digit number:

```bash
chmod 755 script.sh
```

This sets: owner=`rwx`, group=`r-x`, others=`r-x`

```bash
chmod 644 notes.txt
```

This sets: owner=`rw-`, group=`r--`, others=`r--`

```bash
chmod 600 ~/.ssh/id_rsa
```

SSH private keys must be `600` — readable only by the owner. SSH will refuse to use them if permissions are too open.

### Applying to directories recursively
To change permissions for a directory and everything inside it:

```bash
chmod -R 755 projects/
```

Be careful with `-R` — think about whether all files inside should really have the same permissions as the directory.

---

## chown — Changing Ownership
`chown` (change owner) changes who owns a file or directory.

To change just the owner:

```bash
sudo chown alice notes.txt
```

To change both owner and group (separated by `:`):

```bash
sudo chown alice:devs notes.txt
```

To change just the group (note the leading colon):

```bash
sudo chown :devs notes.txt
```

To change ownership recursively for a directory:

```bash
sudo chown -R alice:devs projects/
```

We need `sudo` to change ownership because only root (or the current owner, in some cases) can transfer ownership.

#### When chown is useful
- After creating a file as root, we need to transfer it to a regular user
- After moving files between users' home directories
- Setting up web server directories so the web server process (e.g., user `www-data`) can access them

---

## chgrp — Changing Group Ownership
`chgrp` changes only the group ownership without affecting the owner:

```bash
chgrp developers project.py
```

To change recursively:

```bash
chgrp -R developers projects/
```

This is equivalent to `chown :developers` — just a dedicated command for changing only the group.

---

## Special Permissions
The standard `rwx` model handles most situations, but a few common scenarios reveal its limits. A regular user needs to change their own password, yet only root can write to `/etc/shadow`. A team needs to collaborate in a shared directory, but every new file ends up tagged with the creator's personal group. A directory like `/tmp` needs to accept files from everyone, yet must stop users from deleting one another's work.

Linux solves all three problems with a second layer of permissions: the **setuid**, **setgid**, and **sticky** bits. They sit alongside the regular `rwx` bits and unlock behaviors that the basic model can't express on its own.

#### A hidden 4th octal digit
Every octal permission value is technically four digits, not three. We've simply been omitting the leading zero:

```bash
chmod 0755 file        # identical to chmod 755 file
```

That fourth digit holds the special permission bits:

| Value | Special bit |
|-------|-------------|
| `4` | setuid |
| `2` | setgid |
| `1` | sticky |

We add these together to combine them. So `chmod 4755` means "setuid + 755", `chmod 2775` means "setgid + 775", and `chmod 1777` means "sticky + 777". This is what's happening whenever we see a 4-digit `chmod`.

#### How special bits appear in `ls -l`
Special bits don't get their own column in the permission string — they **replace** the `x` character in one of the existing triplets:

| Bit | Position | Shown as |
|-----|----------|----------|
| setuid | owner's execute | `s` (lowercase) or `S` (uppercase) |
| setgid | group's execute | `s` (lowercase) or `S` (uppercase) |
| sticky | others' execute | `t` (lowercase) or `T` (uppercase) |

The case of the letter carries information. **Lowercase** (`s`, `t`) means the special bit *and* the underlying execute bit are both set — the normal, working configuration. **Uppercase** (`S`, `T`) means the special bit is set but execute is not, which almost always indicates a misconfiguration, since these bits depend on the file being executable in the first place.

#### Setuid (Set User ID) — `s` on owner execute
Consider a regular user changing their password. The new password must be written to `/etc/shadow`, a file readable only by root. Granting every user write access to `/etc/shadow` would defeat the purpose of having password security at all. What we need instead is a way for a user to gain root privileges *temporarily*, *narrowly*, and only while running one specific, trusted program.

The setuid bit provides exactly that. When set on an executable, the program runs with the **owner's** privileges instead of the launcher's. If the owner is root, then any user who runs the program does so with root authority — but only inside that program, and only for the duration of that single execution.

The `passwd` command is the textbook example:

```bash
ls -l /usr/bin/passwd
```

Output: `-rwsr-xr-x 1 root root 68208 ... /usr/bin/passwd`

The `s` in the owner's execute position is the setuid bit. When alice runs `passwd`, the program elevates to root just long enough to update `/etc/shadow`, then exits. Alice's own privileges never change — only the program briefly inherits root's powers.

Setting it:

```bash
chmod u+s program        # symbolic
chmod 4755 program       # octal (4 = setuid, then 755)
```

**Security warning:** Setuid is a powerful feature and a frequent target for attacks. Never set it on a program we don't fully trust. Linux ignores setuid on shell scripts entirely for safety reasons — it only works on compiled programs.

#### Setgid (Set Group ID) — `s` on group execute
Setgid has two distinct behaviors depending on whether it's applied to a file or a directory. The directory behavior is the one we'll meet most often.

**On an executable file**, setgid mirrors setuid for the group: the program runs with the file's group privileges rather than the launcher's. This is uncommon in practice.

**On a directory**, setgid changes how new files are tagged. By default, every file we create takes our **primary group** as its group. In a shared workspace this causes constant friction. Suppose `/srv/teamwork/` is owned by group `devs`, and alice and bob both belong to `devs`. When alice creates a file there, the file's group is `alice`, not `devs` — so bob, despite being a member of the team, can't access it.

Setgid on the directory fixes this. New files inside the directory automatically inherit the directory's group, regardless of who creates them, and the same rule applies to subdirectories created beneath it. The team's group ownership stays consistent without anyone having to remember to fix it manually.

Setting it on a shared directory:

```bash
chmod g+s shared_dir/
```

Now everyone in the group who creates files in `shared_dir/` will have those files belong to the shared group.

To set in octal: add `2` to the front: `chmod 2775 shared_dir/`

#### Sticky bit — `t` on others execute
Newcomers are often surprised to learn that **the right to delete a file is controlled by the directory containing it, not by the file itself.** That's because deletion is, mechanically, an edit to the directory's list of entries — and any user with write permission on a directory can edit that list. In a world-writable directory like `/tmp`, this would be untenable: alice could delete bob's session files on a whim, and applications using `/tmp` for temporary storage would be at the mercy of every other user on the system.

The sticky bit closes this loophole. When set on a directory, it restricts deletion and renaming to the **owner of each file** (plus root and the directory's own owner). Users can still create their own files freely; they just can't touch anyone else's.

The system uses this on `/tmp` itself:

```bash
ls -ld /tmp
```

Output: `drwxrwxrwt 1 root root 4096 ... /tmp`

The `t` at the end means sticky bit is set. Anyone can create files in `/tmp`, but only the file's owner (or root) can delete it. The `rwxrwxrwx` portion grants everyone full directory access, while the `t` ensures each user is fenced off from the others' files.

To set sticky bit:

```bash
chmod +t shared_dir/
```

Or in octal: add `1` to the front: `chmod 1777 /tmp`. The sticky bit is the right tool whenever a directory needs to be open for writing by many users but closed against cross-user interference.

---

## Default Permissions and umask
When we create a new file or directory, what permissions does it get by default? This is controlled by **umask** (user file creation mask).

The default maximum permissions are:
- Files: `666` (`rw-rw-rw-`)
- Directories: `777` (`rwxrwxrwx`)

The umask value is **subtracted** from these maximums. To see our current umask:

```bash
umask
```

A typical value is `0022`. Subtracting `022` from `666` gives `644` for files, and from `777` gives `755` for directories. This is why newly created files typically have `644` permissions and directories have `755`.

To temporarily change the umask for a session:

```bash
umask 027
```

This would give files `640` permissions and directories `750` — restricting access from "others" entirely.

---

## Practical Permission Scenarios
Understanding permissions is easier with real-world examples:

| File Type | Recommended Permissions | Octal | Reason |
|-----------|------------------------|-------|--------|
| Regular text file | `rw-r--r--` | `644` | Owner edits, others only read |
| Shell script | `rwxr-xr-x` | `755` | Owner and others can execute |
| Private config (passwords) | `rw-------` | `600` | Only owner can read/write |
| SSH private key | `rw-------` | `600` | SSH requires this; refuses if more open |
| SSH public key | `rw-r--r--` | `644` | Can be public, but only owner edits |
| Web server directory | `rwxr-xr-x` | `755` | Web server (different user) can read |
| Shared team directory | `rwxrwxr-x` | `775` | Owner and group can write |
| Shared scripts | `rwxr-xr-x` | `755` | Everyone can run, only owner edits |

---

## Viewing and Understanding ls -l Output
Let's read a real `ls -l` output completely:

```
-rw-r--r-- 1 alice devs  4096 Apr  1 10:30 report.txt
drwxr-xr-x 3 alice devs  4096 Mar 28 15:20 projects/
-rwxr-xr-- 1 alice devs  8192 Apr  2 09:15 deploy.sh
lrwxrwxrwx 1 alice devs    12 Apr  3 11:00 link -> /etc/hosts
```

Column by column:
1. `-rw-r--r--` — permission string (file type + owner/group/others permissions)
2. `1` — number of hard links
3. `alice` — owner
4. `devs` — group
5. `4096` — file size in bytes
6. `Apr  1 10:30` — last modification time
7. `report.txt` — filename