# WSL Tips and Tricks — Getting the Most from Linux on Windows

WSL (Windows Subsystem for Linux) is a powerful environment, but it has quirks that aren't obvious from the standard documentation. This guide covers the configuration, workflow optimizations, and practical tips that make WSL feel like a first-class Linux environment rather than an afterthought.

---

## WSL Configuration with wsl.conf
The `/etc/wsl.conf` file inside our Linux distribution controls WSL-specific behavior. We create or edit it to customize how WSL starts and behaves.

```bash
sudo nano /etc/wsl.conf
```

### Automatic Startup Configuration

```ini
[boot]
# Run a command automatically when WSL starts (WSL 2 only)
command = service docker start
```

This is useful for starting services (Docker, databases) automatically when we open WSL.

### Filesystem Settings

```ini
[automount]
# Keep Windows drives mounted (default: true)
enabled = true

# Where Windows drives are mounted
root = /mnt/

# Mount options for Windows drives (improves performance and compatibility)
options = "metadata,umask=22,fmask=11"

# Mount /etc/fstab entries on startup
mountFsTab = true
```

The `metadata` option is important — it enables Linux-style permissions and attributes on Windows NTFS drives. Without it, all files on `/mnt/c/` show as executable by everyone, which can cause issues.

### Network Settings

```ini
[network]
# Set the hostname for our WSL distribution
hostname = mydevbox

# Automatically generate /etc/resolv.conf for DNS
generateResolvConf = true
```

### Interop Settings

```ini
[interop]
# Allow running Windows executables from Linux (default: true)
enabled = true

# Add Windows PATH to Linux PATH (default: true)
appendWindowsPath = true
```

Disabling `appendWindowsPath` can speed up tab completion significantly if we have many Windows programs installed, since Bash won't search through all Windows directories.

### Applying wsl.conf Changes
Changes to `wsl.conf` take effect after restarting the WSL distribution. From PowerShell:

```powershell
wsl --shutdown
```

Then reopen WSL.

---

## .wslconfig — Global WSL 2 Settings
`.wslconfig` lives in our **Windows** user directory (`C:\Users\Username\.wslconfig`) and controls WSL 2 resource limits globally (all distributions).

Create it with Notepad or from within WSL:

```bash
nano /mnt/c/Users/$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r')/.wslconfig
```

```ini
[wsl2]
# Limit WSL 2 memory usage (default: 50% of Windows RAM)
memory=4GB

# Limit CPU cores
processors=4

# Swap space
swap=2GB

# Disable page reporting (can improve performance)
pageReporting=false

# Enable localhost forwarding (forward localhost ports to Windows)
localhostForwarding=true

# Faster DNS lookup
dnsTunneling=true
```

By default, WSL 2 can consume up to half of Windows RAM. Setting `memory=4GB` prevents WSL from making Windows sluggish.

Apply by restarting WSL:

```powershell
wsl --shutdown
```

---

## Windows ↔ Linux Integration

### Running Windows Commands from Linux
We can execute Windows programs directly from the Linux terminal:

```bash
# Open File Explorer in the current directory
explorer.exe .

# Open a file with the default Windows application
cmd.exe /c start document.pdf

# Run PowerShell commands
powershell.exe -Command "Get-Process"

# Open VS Code in current directory (if installed on Windows)
code .

# Run Windows clipboard tools
echo "Hello" | clip.exe    # Copy to Windows clipboard
powershell.exe Get-Clipboard   # Paste from clipboard
```

### Running Linux Commands from Windows
From PowerShell or CMD:

```powershell
# Run a Linux command
wsl ls -la

# Run a specific distro
wsl -d Ubuntu ls /etc

# Pipe between Windows and Linux
dir | wsl grep ".txt"
wsl cat /etc/hosts | findstr localhost
```

### Accessing Linux Files from Windows
Our Linux home directory is accessible from Windows at:

```
\\wsl$\Ubuntu\home\username\
```

Or in File Explorer, type `\\wsl$` in the address bar to see all WSL distributions.

We can also open it directly:

```bash
# From Linux, open our home directory in Windows Explorer
explorer.exe ~
```

### Accessing Windows Files from Linux
Windows drives are mounted at `/mnt/`:

```bash
ls /mnt/c/Users/
cd /mnt/c/Users/Alice/Documents/

# Copy from Windows to Linux home
cp /mnt/c/Users/Alice/file.txt ~/

# Copy from Linux to Windows Desktop
cp ~/script.sh /mnt/c/Users/Alice/Desktop/
```

**Performance tip:** Work on project files inside the Linux filesystem (`~/projects/`), not on `/mnt/c/`. Cross-filesystem operations are 5-10x slower. Only use `/mnt/c/` for transferring files to/from Windows.

---

## VS Code + WSL — The Ideal Setup
VS Code with the WSL extension provides the best of both worlds: VS Code's graphical interface with true Linux execution.

### Setting Up
1. Install [VS Code](https://code.visualstudio.com/) on Windows
2. Install the "WSL" extension in VS Code
3. From WSL terminal, open any project:

```bash
code .
```

VS Code opens with:
- Files stored and executed on Linux
- Terminal running Linux bash
- Extensions running in Linux context
- No Windows/Linux path translation issues

### Working with VS Code from WSL

```bash
# Open a specific file
code ~/.bashrc

# Open the current directory as a project
code .

# Open in a new VS Code window
code -n ~/projects/myapp
```

### Useful VS Code WSL Features
- **Integrated terminal** is automatically a Linux bash shell
- **Extensions** install into the Linux context (Python interpreter, linters, etc. run on Linux)
- **Git** uses the Linux git, avoiding line ending issues
- **Port forwarding** — VS Code automatically forwards ports from WSL to Windows (access `localhost:8080` in Windows browser when running on WSL)

---

## Port Forwarding and Web Development
When we run a web server in WSL 2, its ports are automatically forwarded to Windows localhost. If we start a server on port 8080 in WSL:

```bash
python3 -m http.server 8080
```

We can access `http://localhost:8080` in any Windows browser.

### Accessing WSL from Other Devices on the Network
By default, WSL 2 services are NOT accessible from other machines on the network (only from localhost on Windows). To expose WSL services to the LAN, we need Windows port proxy:

From PowerShell (as Administrator):

```powershell
# Get WSL IP address
wsl hostname -I

# Forward Windows port 8080 to WSL port 8080
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=<WSL_IP>

# Also allow through Windows Firewall
netsh advfirewall firewall add rule name="WSL Port 8080" dir=in action=allow protocol=TCP localport=8080
```

To remove the proxy:

```powershell
netsh interface portproxy delete v4tov4 listenport=8080 listenaddress=0.0.0.0
```

---

## WSL-Specific Performance Tips

### Store Projects in Linux, Not Windows
The most impactful performance optimization:

```bash
# Do this (fast — native Linux filesystem):
cd ~/projects
git clone https://github.com/user/repo.git

# Not this (slow — cross-filesystem):
cd /mnt/c/Users/Alice/projects
git clone https://github.com/user/repo.git
```

File operations on `/mnt/c/` go through a translation layer that's significantly slower than native Linux operations.

### Disable Windows PATH in Linux (for faster tab completion)
If we have many Windows programs, tab completion can be slow because bash searches all Windows PATH directories. In `/etc/wsl.conf`:

```ini
[interop]
appendWindowsPath = false
```

Then manually add only the Windows tools we actually use from Linux:

```bash
# Add only specific Windows tools to Linux PATH
export PATH="$PATH:/mnt/c/Windows/System32:/mnt/c/Windows"
```

### Faster DNS Resolution
DNS can be slow in WSL 2. In `~/.wslconfig`:

```ini
[wsl2]
dnsTunneling=true
```

Or manually set a fast DNS server in `/etc/resolv.conf`:

```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

**Note:** WSL often overwrites `/etc/resolv.conf` on startup. To prevent this, add to `/etc/wsl.conf`:

```ini
[network]
generateResolvConf = false
```

---

## Managing Multiple WSL Distributions
We can install and run multiple Linux distributions simultaneously:

```powershell
# List available distributions
wsl --list --online

# Install a specific distribution
wsl --install -d Debian
wsl --install -d Ubuntu-22.04

# List installed distributions
wsl --list --verbose

# Set the default distribution
wsl --set-default Ubuntu

# Open a specific distribution
wsl -d Debian
```

### Backup and Restore WSL Distributions
To back up a distribution to a file:

```powershell
wsl --export Ubuntu ubuntu-backup.tar
```

To restore:

```powershell
wsl --import Ubuntu C:\WSL\Ubuntu ubuntu-backup.tar
```

This is useful for migrating to a new machine or creating a "clean" snapshot.

---

## Common WSL Issues and Fixes

### Clock Drift
WSL 2 sometimes has clock drift (the time inside WSL gets out of sync with Windows). Fix:

```bash
sudo hwclock -s
# Or:
sudo ntpdate pool.ntp.org
```

### /etc/resolv.conf Issues
If DNS stops working:

```bash
# Check current DNS server
cat /etc/resolv.conf

# If empty or wrong, fix temporarily:
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

### WSL Consuming Too Much Memory
WSL 2 uses a virtual machine that doesn't always release memory back to Windows. Set limits in `.wslconfig`:

```ini
[wsl2]
memory=4GB
```

To reclaim memory immediately:

```powershell
wsl --shutdown
```

Then reopen WSL.

### File Permissions on /mnt/c/ Are All 777
This is the default without metadata support. Fix in `/etc/wsl.conf`:

```ini
[automount]
options = "metadata,umask=22,fmask=11"
```

Restart WSL for this to take effect.