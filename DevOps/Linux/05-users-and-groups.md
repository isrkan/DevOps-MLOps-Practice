# Users and Groups — Managing Identities on Linux

Linux is built around the concept of **users** and **groups**. Every process runs as a user, every file is owned by a user, and every user belongs to one or more groups. Understanding how to create, manage, and switch between users is essential for both daily use and system administration.

This guide covers the root user, `sudo`, user management commands, and group management — everything we need to confidently administer users on an Ubuntu or Debian system.

---

## Root vs Regular Users

#### The root user
The **root** user is the superuser — the all-powerful administrator account on every Linux system. Root can:
- Read, write, and delete any file on the system
- Change ownership of any file
- Kill any process
- Install or remove any software
- Add or delete any user

Root's home directory is `/root`, and root's prompt ends with `#` instead of `$`.

#### Why we don't use root for daily work
Using root for everyday tasks is dangerous because:
- A typo in a command can delete critical system files
- A malicious program running as root can compromise the entire system
- There's no safety net — no "are you sure?" prompts

Best practice is to use a **regular user account** for daily work and only escalate to root privileges when specifically needed — and that's exactly what `sudo` is for.

---

## sudo — Running Commands as Root
**`sudo`** (Super User Do) allows an authorized regular user to run a specific command with root privileges. It's the safe, auditable way to perform administrative tasks without staying logged in as root.

#### Running a single command as root
Simply prefix the command with `sudo`:

```bash
sudo apt install nginx
```

This command uses the package manager (`apt`) to install a web server called `nginx`. Because installing software changes system files, it requires `sudo`.

Linux will ask for our **own password** (not root's password). After authenticating, the command runs with root privileges. The session is usually cached for a few minutes so we don't have to re-enter our password for every subsequent `sudo` command.

#### Why sudo is safer than logging in as root
- **Auditing:** Every `sudo` command is logged in `/var/log/auth.log`, creating an audit trail
- **Limited exposure:** We're root only for that one command, not for the entire session
- **Intentional:** Having to type `sudo` makes us think twice before doing something destructive

#### Checking if we have sudo access
To see what sudo privileges we have:

```bash
sudo -l
```

On a freshly installed Ubuntu system with WSL, our default user already has full sudo access.

#### Opening a root shell (use sparingly)
If we need to run many commands as root in sequence, we can start a root shell:

```bash
sudo -i
```

This logs us in as root (the prompt changes to `#`). To return to our regular user:

```bash
exit
```

Alternatively:

```bash
sudo su
```

Both are equivalent. Use root shells sparingly and exit promptly when done.

#### The sudoers file
The `/etc/sudoers` file controls which users can use `sudo` and what they can run. **Never edit this file directly with a text editor** — always use `visudo`, which validates the syntax before saving:

```bash
sudo visudo
```

If we make a syntax error in sudoers, we could lock ourselves out of sudo entirely. `visudo` prevents this.

A typical sudoers entry that gives a user full sudo access:

```
alice   ALL=(ALL:ALL) ALL
```

This means: user `alice` on `ALL` hosts can run commands as `ALL` users/groups for `ALL` commands.

---

## User Management

#### adduser — Create a new user (recommended on Debian/Ubuntu)
`adduser` is a friendly, interactive command that creates a new user, sets up their home directory, and prompts us for a password:

```bash
sudo adduser bob
```

It will ask for:
- Full name
- Room number (can skip)
- Phone numbers (can skip)
- A password

This command:
1. Creates the user account
2. Creates `/home/bob/` with proper ownership
3. Copies default configuration files (`.bashrc`, `.profile`) from `/etc/skel/`
4. Sets the password

#### useradd — Low-level user creation command
`useradd` is the lower-level command that adds a user but doesn't do all the friendly setup automatically:

```bash
sudo useradd -m -s /bin/bash bob
```

Options:
- `-m` — create the home directory
- `-s /bin/bash` — set the default shell to bash
- `-d /custom/home` — specify a custom home directory
- `-G sudo,devs` — add to supplementary groups immediately

After `useradd`, we must set the password manually:

```bash
sudo passwd bob
```

**On Ubuntu/Debian, `adduser` is preferred** because it handles all the setup automatically and is more user-friendly. `useradd` is more common in scripts and on Red Hat-based systems (like CentOS/RHEL).

#### passwd — Set or change a password
To change our own password:

```bash
passwd
```

To change another user's password (requires root):

```bash
sudo passwd bob
```

To expire a user's password (force them to change it at next login):

```bash
sudo passwd -e bob
```

To lock a user account (prevent login):

```bash
sudo passwd -l bob
```

To unlock:

```bash
sudo passwd -u bob
```

#### usermod — Modify an existing user
`usermod` changes the properties of an existing user account.

To add a user to a supplementary group (without removing them from other groups, use `-aG`):

```bash
sudo usermod -aG docker alice
```

The `-aG` is critically important — using just `-G` without `-a` would **replace** all the user's groups with only the ones specified. Always use `-aG` to add to groups.

To change the user's home directory:

```bash
sudo usermod -d /new/home alice
```

To change the user's default shell:

```bash
sudo usermod -s /bin/zsh alice
```

To rename a user:

```bash
sudo usermod -l newname oldname
```

#### deluser / userdel — Delete a user
On Ubuntu/Debian:

```bash
sudo deluser bob
```

To also remove their home directory and mail spool:

```bash
sudo deluser --remove-home bob
```

The lower-level command is `userdel`:

```bash
sudo userdel -r bob
```

The `-r` flag removes the home directory.

---

## Inspecting User Information

#### id — Show user and group IDs
`id` shows the numeric and symbolic user ID (UID) and group ID (GID) for a user:

```bash
id
```

Output:

```
uid=1000(alice) gid=1000(alice) groups=1000(alice),27(sudo),998(docker)
```

To check another user:

```bash
id bob
```

Every user has a unique **UID** (User ID number). Root always has UID 0. Regular users on Ubuntu/Debian start at UID 1000.

#### whoami — Show current username
A quick way to confirm which user we're currently operating as:

```bash
whoami
```

#### who and w — Who is logged in
`who` shows who is currently logged in to the system:

```bash
who
```

`w` shows who is logged in and what they're currently doing:

```bash
w
```

#### last — Login history
`last` shows a history of recent logins:

```bash
last
```

To see only the last 10 entries:

```bash
last -n 10
```

---

## Understanding /etc/passwd and /etc/shadow

#### /etc/passwd — User account database
Every user account on the system is listed in `/etc/passwd`. Despite the name, it doesn't store passwords anymore (that's `/etc/shadow`). Let's look at it:

```bash
cat /etc/passwd
```

Each line represents one user account and has 7 fields separated by colons:

```
alice:x:1000:1000:Alice Smith,,,:/home/alice:/bin/bash
  ↑   ↑  ↑    ↑        ↑            ↑           ↑
  1   2  3    4         5            6           7
```

1. **Username** — the login name (`alice`)
2. **Password** — always `x` now (means "look in /etc/shadow")
3. **UID** — unique numeric user ID (`1000`)
4. **GID** — primary group ID (`1000`)
5. **GECOS** — full name and other info (optional, comma-separated)
6. **Home directory** — the user's home directory path
7. **Shell** — the user's default shell

System accounts (for services) have UIDs below 1000 and often have `/usr/sbin/nologin` as their shell, preventing interactive login.

#### /etc/shadow — Password storage
`/etc/shadow` stores the actual (hashed) passwords and password policy information. It's only readable by root:

```bash
sudo cat /etc/shadow
```

Each line has the format:

```
alice:$6$salt$hashedpassword:18000:0:99999:7:::
```

Fields include: username, hashed password (`$6$` means SHA-512), days since epoch of last password change, minimum days before change allowed, maximum days password is valid, etc.

The password field starts with `!` if the account is locked, or `*` if it has no password (service accounts).

---

## Group Management
Groups let us apply permissions to multiple users at once. Instead of granting a file permission to 20 individual users, we put them all in a group and grant the group permission.

#### groups — Show a user's groups
To see which groups a user belongs to:

```bash
groups alice
```

Output: `alice : alice sudo docker`

This shows: primary group is `alice`, plus supplementary groups `sudo` and `docker`.

#### groupadd — Create a new group

```bash
sudo groupadd developers
```

To create a group with a specific GID:

```bash
sudo groupadd -g 2000 developers
```

#### Adding a user to a group
After creating a group, we add users to it with `usermod -aG`:

```bash
sudo usermod -aG developers alice
```

Or using `gpasswd`:

```bash
sudo gpasswd -a alice developers
```

**Important:** Changes to group membership take effect the next time the user logs in. For WSL, we might need to close and reopen the terminal, or run:

```bash
newgrp developers
```

This starts a new shell with the updated group membership without logging out.

#### groupmod — Modify a group
To rename a group:

```bash
sudo groupmod -n newname oldname
```

#### groupdel — Delete a group
To delete a group (make sure no important files are owned by it first):

```bash
sudo groupdel developers
```

#### /etc/group — Group database
Similar to `/etc/passwd`, `/etc/group` lists all groups:

```bash
cat /etc/group
```

Format: `groupname:password:GID:member1,member2,...`

Example:

```
sudo:x:27:alice,bob
docker:x:998:alice
developers:x:1001:alice,carol,dave
```

---

## Switching Users

#### su — Switch user
`su` (substitute user) switches to another user account. We need that user's password:

```bash
su - bob
```

The `-` (or `-l` or `--login`) makes it a **login shell** — it loads bob's environment (`.bashrc`, environment variables, home directory). Without `-`, we keep our current environment.

To switch to root (requires root's password, not recommended — use `sudo` instead):

```bash
su -
```

To return to our original user:

```bash
exit
```

#### Running a single command as another user
`sudo -u` runs one command as a specific user:

```bash
sudo -u bob ls /home/bob/
```

This is useful for testing what a user can do without actually switching to them.

---

## The sudo Group
On Ubuntu/Debian, users in the **`sudo` group** can use `sudo` to run commands as root. This is the standard way to grant administrative access.

To check if a user is in the sudo group:

```bash
groups alice
```

If `sudo` appears in the output, they have sudo access.

To grant a user sudo access, add them to the sudo group:

```bash
sudo usermod -aG sudo newadmin
```

On Red Hat-based systems (CentOS, Fedora, RHEL), the equivalent group is called **`wheel`** instead of `sudo`. On Ubuntu/Debian, `sudo` is the group name.