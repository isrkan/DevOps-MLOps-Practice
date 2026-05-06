# Troubleshooting — Diagnosing and Fixing Linux Problems

Linux is transparent about what's happening — everything is logged, every error has a reason, and every problem has a systematic solution. The key skill is knowing *where to look* and *how to read* what Linux is telling us. This guide teaches a systematic troubleshooting methodology and covers the most common categories of Linux problems.

---

## The Troubleshooting Mindset
Before running commands blindly, adopt this mindset:

1. **Read the error message carefully.** Linux error messages are usually specific and informative. Don't glance at them — read them word by word.
2. **When did it last work?** If it worked before, what changed? New package, config edit, reboot?
3. **Can we reproduce it?** Run the command again and capture the exact output.
4. **Narrow it down.** Is it a permission issue? A missing file? A network problem? A wrong configuration?
5. **Check the logs.** Most problems leave traces in system or application logs.
6. **Search the exact error message.** Copy the error verbatim and search for it — thousands of others have hit the same issue.

---

## Decoding Common Error Messages

### "Permission denied"
The operation was blocked by the permission system.

```
bash: ./script.sh: Permission denied
```

**Diagnosis:**
```bash
ls -l script.sh              # Check permissions
whoami                       # Check current user
```

**Fixes:**
```bash
chmod +x script.sh           # Add execute permission
sudo ./script.sh             # Run with root privileges (if appropriate)
```

### "No such file or directory"
The file or directory doesn't exist at the specified path.

```
bash: /opt/myapp/start.sh: No such file or directory
```

**Diagnosis:**
```bash
ls -la /opt/myapp/           # Does the directory exist?
which python3                # Is the interpreter in PATH?
file /opt/myapp/start.sh     # Is it actually a file?
```

Common causes:
- Typo in the path
- Relative vs absolute path confusion
- File was deleted or never created
- Symlink pointing to a non-existent target

### "Command not found"
The shell can't find the executable we're trying to run.

```
bash: pip: command not found
```

**Diagnosis:**
```bash
which pip                    # Is it in PATH?
which pip3                   # Maybe it's named differently?
find /usr -name "pip*" 2>/dev/null   # Find it on disk
echo $PATH                   # Check what directories are searched
```

**Fixes:**
```bash
sudo apt install python3-pip          # Install the missing package
export PATH="$PATH:$HOME/.local/bin"  # Add directory to PATH
pip3 install ...                      # Use pip3 instead of pip
```

### "Address already in use"
A service is trying to bind to a port that's already occupied.

```
Error: listen EADDRINUSE: address already in use 0.0.0.0:8080
```

**Diagnosis:**
```bash
sudo ss -tulnp | grep :8080   # What process is using port 8080?
sudo lsof -i :8080            # Same information, different format
```

**Fix:**
```bash
sudo kill <PID>               # Kill the occupying process
# Or change our application to use a different port
```

### "Disk quota exceeded" / "No space left on device"
The filesystem is full.

```
cp: error writing 'file.txt': No space left on device
```

**Diagnosis:**
```bash
df -h                         # Check filesystem usage
du -sh /var/log/*             # Find large directories
du -sh ~/*                    # Check our home directory
```

**Fixes:**
```bash
sudo apt clean                # Clean package cache
sudo journalctl --vacuum-size=100M   # Shrink journal logs
sudo find /tmp -mtime +7 -delete     # Clean old temp files
sudo du -sh /var/log/* | sort -h     # Find and delete large logs
```

### "Too many open files"
A process has hit the system limit for open file descriptors.

```
OSError: [Errno 24] Too many open files
```

**Diagnosis:**
```bash
ulimit -n                     # Current limit for our session
cat /proc/sys/fs/file-max     # System-wide maximum
```

**Fix (temporary):**
```bash
ulimit -n 65536               # Increase limit for current session
```

**Fix (permanent, for a service):**
Add to the service's systemd unit file:
```ini
[Service]
LimitNOFILE=65536
```

---

## Systematic Log Investigation
Logs are the most reliable source of truth. Here's how to efficiently search them.

### The Most Important Log Locations

```bash
journalctl                    # systemd journal (all system logs)
/var/log/syslog               # General system messages
/var/log/auth.log             # Authentication events
/var/log/kern.log             # Kernel messages
/var/log/dpkg.log             # Package installation history
/var/log/apt/history.log      # APT operation history
/var/log/nginx/error.log      # Nginx errors
/var/log/nginx/access.log     # Nginx access log
/var/log/postgresql/          # PostgreSQL logs
```

### Efficient Log Searching

```bash
# Find recent errors in the system journal
journalctl -p err --since "1 hour ago"

# Follow a service log live
journalctl -u nginx -f

# Show logs for a crashed service (includes previous failures)
journalctl -u myservice -b -1    # -b -1 = previous boot

# Find authentication failures
grep "Failed" /var/log/auth.log | tail -20

# Find errors across multiple log files
grep -r "error" /var/log/ 2>/dev/null | grep -v "Binary"

# Find what happened at a specific time
journalctl --since "2024-04-01 10:00" --until "2024-04-01 10:30"
```

### A Service Won't Start
This is one of the most common troubleshooting scenarios:

```bash
# Step 1: Check status and get error summary
sudo systemctl status myservice

# Step 2: Get the full logs since last attempt
journalctl -u myservice -n 50 --no-pager

# Step 3: Check the service configuration
sudo systemctl cat myservice      # View the unit file

# Step 4: Test the command manually
# Run the exact command from ExecStart= as the service's User=
sudo -u serviceuser /opt/myapp/start.sh

# Step 5: Check file permissions
ls -la /opt/myapp/
ls -la /etc/myapp/config.yaml
```

---

## Diagnosing Process and Performance Issues

### System Is Slow

```bash
# Check load average (is CPU maxed out?)
uptime

# Find what's consuming CPU
top       # Press P to sort by CPU
htop      # More visual version

# Check memory
free -h
vmstat 2 5   # Memory/CPU/IO stats, 5 times every 2 seconds

# Check disk I/O (install if needed: sudo apt install iotop)
sudo iotop

# Check network usage (sudo apt install nethogs)
sudo nethogs
```

### A Process Is Stuck

```bash
# Find the process
ps aux | grep processname
pgrep -a processname

# Check what files it has open
sudo lsof -p <PID>

# Check what system calls it's making (strace)
sudo strace -p <PID>       # Shows every system call in real time
sudo strace -p <PID> -e trace=network  # Only network calls
```

`strace` is invaluable for understanding why a process is hanging — it shows exactly what it's waiting for (a file lock, a network connection, etc.).

### Zombie Processes
A **zombie process** is one that has finished but hasn't been reaped by its parent. It shows as `Z` in `ps`:

```bash
ps aux | grep Z              # Find zombies
```

Zombies can't be killed (they're already dead) — only their parent process can reap them. If the parent is still running, send it SIGCHLD:

```bash
kill -SIGCHLD <parent_PID>
```

If the parent won't reap them, we need to kill the parent.

---

## Network Troubleshooting

### Is the Network Interface Up?

```bash
ip link show              # Shows interfaces and their state (UP/DOWN)
ip addr show              # Shows assigned IP addresses
```

If an interface is DOWN:

```bash
sudo ip link set eth0 up   # Bring it up
```

### Can We Reach the Gateway?

```bash
ip route show             # Find gateway IP (default via X.X.X.X)
ping -c 3 <gateway_ip>    # Can we reach the router?
```

### Can We Reach the Internet?

```bash
ping -c 3 8.8.8.8         # Reach Google's DNS (no DNS needed)
ping -c 3 google.com      # Reach by hostname (tests DNS)
```

If `8.8.8.8` works but `google.com` doesn't, the problem is **DNS**, not connectivity.

### DNS Problems

```bash
cat /etc/resolv.conf       # What DNS servers are we using?
nslookup google.com        # Query DNS directly
dig google.com @8.8.8.8    # Query a specific DNS server

# Temporary fix for broken DNS:
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

### Connection Refused

```
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

This means nothing is listening on that port. Check:

```bash
sudo ss -tulnp | grep :8080    # Is anything listening on 8080?
sudo systemctl status myservice   # Is the service running?
```

### Connection Timed Out
This usually means a firewall is blocking the connection:

```bash
sudo ufw status               # Check local firewall
sudo iptables -L -n           # Check iptables directly
```

Or the host is unreachable:

```bash
ping -c 3 <host>
traceroute <host>             # Where does the path break?
```

---

## File Permission Troubleshooting

### Can't Read a File

```bash
ls -la filename             # Check permissions
whoami                      # Who are we?
id                          # What groups are we in?
stat filename               # Full file metadata
```

Check the permission chain — we need execute permission on every directory in the path:

```bash
namei -l /path/to/file      # Shows permissions for every component of the path
```

### Script Won't Run

```bash
ls -l script.sh             # Check: does it have +x?
head -1 script.sh           # Check: does it have a proper shebang?
file script.sh              # Check: is it actually a text file?
cat -A script.sh | head     # Check for Windows line endings (shows ^M at end of lines)
```

Windows line endings (`\r\n`) in a script cause the `#!/bin/bash` shebang to not be recognized. Fix:

```bash
sed -i 's/\r//' script.sh   # Remove carriage returns
# Or:
dos2unix script.sh           # Install with: sudo apt install dos2unix
```

---

## Package Management Troubleshooting

### apt Won't Install (Dependency Errors)

```bash
# Fix broken dependencies
sudo apt install -f

# Clear the package cache and try again
sudo apt clean
sudo apt update
sudo apt install <package>

# If a specific package is broken
sudo dpkg --configure -a   # Reconfigure unconfigured packages
```

### "Package not found" or "Unable to locate package"

```bash
# Refresh the package list first
sudo apt update

# Check if universe/multiverse repos are enabled
cat /etc/apt/sources.list

# Enable additional repositories
sudo add-apt-repository universe
sudo apt update
```

### GPG Key Error When Adding Repository

```
W: GPG error: ... The following signatures couldn't be verified because the public key is not available
```

```bash
# Import the missing key (the error message usually includes the key ID)
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <KEY_ID>
# Or use the newer approach:
curl -fsSL https://example.com/gpg.key | sudo gpg --dearmor -o /usr/share/keyrings/example-archive-keyring.gpg
```

---

## Useful Diagnostic Commands Quick Reference

| Scenario | Command |
|----------|---------|
| What's using disk space? | `du -sh /* 2>/dev/null | sort -h` |
| What process uses a port? | `sudo ss -tulnp | grep :<port>` |
| What's causing high CPU? | `top` then `P`, or `ps aux --sort=-%cpu | head` |
| What's consuming memory? | `ps aux --sort=-%mem | head` |
| Why did a service fail? | `journalctl -u <service> -n 50` |
| What changed recently? | `find /etc -mtime -1` |
| Who logged in? | `last -20` |
| What files does PID have open? | `sudo lsof -p <PID>` |
| What system calls is a process making? | `sudo strace -p <PID>` |
| What's in the kernel log? | `dmesg | tail -20` |
| Why can't I write to a file? | `namei -l /path/to/file` |
| Why is DNS broken? | `cat /etc/resolv.conf`, then `dig google.com` |