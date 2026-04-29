# Package Management — Installing and Managing Software

One of the most pleasant surprises for Windows users moving to Linux is the package manager. On Windows, installing software means searching the web, downloading an installer, clicking through a wizard, and hoping for no surprises. On Ubuntu/Debian Linux, installing almost any software is a single command. The package manager handles downloading, installing, updating, and removing software — cleanly, safely, and consistently.

This guide covers **APT** (the primary package manager for Ubuntu and Debian), **dpkg** (the low-level tool beneath APT), and modern alternatives like **snap**.

---

## What Is a Package Manager?

A **package manager** is a system that:
1. Maintains a list of available software (**repository**)
2. Downloads, installs, and configures software automatically
3. Tracks all installed software and its version
4. Manages **dependencies** — software that other software requires to run
5. Updates all installed software in a single command
6. Removes software cleanly without leaving traces behind

On Ubuntu and Debian, the package format is `.deb` (Debian package) and the package manager is **APT** (Advanced Package Tool).

---

## APT — Advanced Package Tool
APT is the command-line package manager we'll use constantly on Ubuntu and Debian. It sits on top of the lower-level `dpkg` tool and adds automatic dependency resolution and repository management.

### Updating the Package List
Before installing anything, we should always refresh our local list of available packages. The package list tells APT what software is available and at which versions:

```bash
sudo apt update
```

This does **not** install or upgrade anything — it only refreshes the list of what's available in the repositories. Think of it like "syncing the catalog" before shopping.

We should run this:
- Before installing new software
- Before upgrading packages
- After adding a new repository

### Upgrading Installed Packages
Once we have an up-to-date package list, we can upgrade all installed packages to their latest versions:

```bash
sudo apt upgrade
```

APT will show us a list of packages to be upgraded and ask for confirmation. Press `Y` (or just `Enter`, since yes is the default) to proceed.

A combined workflow we'll use frequently:

```bash
sudo apt update && sudo apt upgrade
```

The `&&` ensures the upgrade only runs if the update succeeded.

There's also `full-upgrade` (previously `dist-upgrade`) which handles more complex upgrades that might require removing some packages:

```bash
sudo apt full-upgrade
```

### Installing Software
To install a package:

```bash
sudo apt install <package_name>
```

For example, to install the `tree` command-line tool:

```bash
sudo apt install tree
```

APT will show the packages to be installed (including any dependencies) and ask for confirmation.

To install multiple packages at once:

```bash
sudo apt install curl wget git vim htop
```

To install without being prompted for confirmation (useful in scripts):

```bash
sudo apt install -y nginx
```

The `-y` flag answers "yes" to all prompts automatically.

To install a specific version of a package:

```bash
sudo apt install python3=3.10.12-1
```

### Removing Software
To remove a package (keeps configuration files):

```bash
sudo apt remove nginx
```

To remove a package **and** its configuration files (cleaner):

```bash
sudo apt purge nginx
```

The difference:
- `remove` — uninstalls the program but leaves configuration files (in `/etc/`) in place
- `purge` — removes both the program and its configuration files

For most purposes, `purge` is the better choice when we're done with software and won't reinstall it.

### Removing Unused Dependencies
When we install a package, APT often installs additional packages that it depends on. When we remove the main package, those dependencies may no longer be needed. `autoremove` cleans them up:

```bash
sudo apt autoremove
```

It's good practice to run this after removing software. To combine with purge:

```bash
sudo apt purge nginx && sudo apt autoremove
```

### Searching for Packages
To search for packages by name or description:

```bash
apt search keyword
```

For example, to find all packages related to Python:

```bash
apt search python3
```

The output shows package names and descriptions. It can be long — pipe it through `less`:

```bash
apt search python3 | less
```

To search only in package names (faster, more focused):

```bash
apt search --names-only python3
```

### Getting Package Details
To see detailed information about a package before installing it — including its description, version, size, and dependencies:

```bash
apt show nginx
```

This is great for understanding what a package does before committing to the install.

### Listing Installed Packages
To see all installed packages:

```bash
apt list --installed
```

To check if a specific package is installed:

```bash
apt list --installed | grep nginx
```

Or more directly:

```bash
dpkg -l nginx
```

### Cleaning the Package Cache
APT caches downloaded `.deb` files in `/var/cache/apt/archives/`. Over time this can grow large. To clean it:

```bash
sudo apt clean
```

To remove only packages that are no longer available in the repositories (outdated cached files):

```bash
sudo apt autoclean
```

### apt-cache — The Old Way to Query
Before `apt` was unified, we used `apt-get` for installing and `apt-cache` for querying. These still work and are often seen in older documentation:

```bash
apt-cache search python3         # same as apt search
apt-cache show nginx             # same as apt show
apt-cache policy nginx           # show version details and repository sources
```

The `apt-cache policy` command is particularly useful for seeing which version of a package is installed vs. available, and from which repository.

### Summary of APT Commands

| Command | Purpose |
|---------|---------|
| `sudo apt update` | Refresh the package list |
| `sudo apt upgrade` | Upgrade all installed packages |
| `sudo apt install <pkg>` | Install a package |
| `sudo apt remove <pkg>` | Remove a package (keep config) |
| `sudo apt purge <pkg>` | Remove a package and config files |
| `sudo apt autoremove` | Remove unneeded dependencies |
| `apt search <keyword>` | Search for packages |
| `apt show <pkg>` | Show package details |
| `apt list --installed` | List installed packages |
| `sudo apt clean` | Clear download cache |

---

## dpkg — The Low-Level Package Tool

**dpkg** (Debian Package) is the underlying tool that APT uses. While APT handles repositories and dependencies automatically, dpkg works directly with `.deb` files. We use it when:
- Installing a `.deb` file we downloaded manually
- Querying installed packages at a low level
- Diagnosing package issues

#### Listing installed packages
To list all installed packages with their version and status:

```bash
dpkg -l
```

To filter for a specific package:

```bash
dpkg -l nginx
```

Output columns: status, name, version, architecture, description.

#### Installing a .deb file manually
When a vendor provides a `.deb` file directly (e.g., downloaded from their website), we install it with dpkg:

```bash
sudo dpkg -i package.deb
```

If dpkg reports dependency errors, fix them with:

```bash
sudo apt install -f
```

The `-f` (fix broken) option resolves missing dependencies.

#### Removing a package with dpkg
```bash
sudo dpkg -r package_name
```

To purge (remove including config):

```bash
sudo dpkg -P package_name
```

#### Finding which package owns a file
Very useful when we find a program and want to know what package installed it:

```bash
dpkg -S /usr/bin/python3
```

Output: `python3-minimal: /usr/bin/python3`

#### Listing files installed by a package
To see all files that belong to a package:

```bash
dpkg -L nginx
```

#### Checking package status
To see the installation status and details of a specific package:

```bash
dpkg -s nginx
```

---

## PPAs — Adding Third-Party Repositories
Sometimes the software we need isn't in Ubuntu's official repositories, or the official version is too old. **PPAs** (Personal Package Archives) are third-party repositories maintained by software developers or community members.

To add a PPA, we use `add-apt-repository`:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
```

After adding, we must update our package list so APT knows about the new packages:

```bash
sudo apt update
```

Then install from the PPA like any other package:

```bash
sudo apt install python3.12
```

**Be cautious with PPAs** — they're maintained by individuals, not the Ubuntu team. Only use PPAs from trusted sources. To remove a PPA:

```bash
sudo add-apt-repository --remove ppa:deadsnakes/ppa
```

### Adding a Repository Manually
Some software (like Docker or VS Code) provides its own repository. The process typically involves:

1. Adding the repository's signing key so apt can verify package integrity:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

2. Adding the repository URL:

```bash
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list
```

3. Updating and installing:

```bash
sudo apt update && sudo apt install docker-ce
```

Repository configuration files live in `/etc/apt/sources.list` (main file) and `/etc/apt/sources.list.d/` (additional files, one per repository). We can view them to understand what sources APT is pulling from.

---

## snap — Universal Packages
**snap** is a newer packaging format developed by Canonical (the company behind Ubuntu). Snap packages are self-contained with all their dependencies bundled inside, meaning they work across different Linux distributions and versions.

Snap is installed by default on Ubuntu 16.04 and later.

#### Installing a snap package

```bash
sudo snap install vlc
```

#### Listing installed snaps

```bash
snap list
```

#### Removing a snap

```bash
sudo snap remove vlc
```

#### Updating all snaps
Snaps update automatically in the background, but to update manually:

```bash
sudo snap refresh
```

**When to use snap vs apt:**
- Use `apt` as the default — it's faster, more integrated, and more efficient
- Use `snap` when the software is only available as a snap, or when we need a newer version than what apt provides
- Snap packages start slightly slower and use more disk space due to bundled dependencies

---

## flatpak — Another Universal Package Format

**Flatpak** is another self-contained package format, popular on desktop Linux distributions. While less common on servers, it's worth knowing:

```bash
# Install Flatpak support
sudo apt install flatpak

# Install a Flatpak application
flatpak install flathub org.gimp.GIMP

# Run a Flatpak application
flatpak run org.gimp.GIMP

# Update all Flatpak apps
flatpak update
```

---

## Practical Examples

Let's tie it all together with a real-world workflow — setting up a typical Python development environment:

```bash
# Step 1: Update the package list
sudo apt update

# Step 2: Install Python 3, pip, and a virtual environment tool
sudo apt install -y python3 python3-pip python3-venv

# Step 3: Install some useful development tools
sudo apt install -y git curl wget htop tree vim

# Step 4: Install Docker (via its official repository)
# (The actual Docker install process is documented at docs.docker.com)

# Step 5: Verify installations
python3 --version
git --version
curl --version
```