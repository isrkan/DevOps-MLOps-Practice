# Security Hardening — Protecting Our Linux System

A default Linux installation is reasonably secure, but a production server exposed to the internet needs additional hardening. This guide covers the essential steps for securing an Ubuntu/Debian server: hardening SSH, blocking brute-force attacks with fail2ban, configuring AppArmor, auditing users and permissions, and establishing good security habits.

Security is not a one-time task — it's an ongoing practice of reducing attack surface, monitoring for threats, and responding to incidents.

---

## SSH Hardening
SSH is the primary way we access remote Linux servers, and it's also the most frequently attacked service. Hardening SSH is the first priority on any server.

### Disable Password Authentication
The most impactful SSH security improvement is switching to key-only authentication. With password auth enabled, attackers can try thousands of passwords per minute.

**Step 1: Ensure we have our SSH key set up first** (see the Networking guide). Never disable password auth before confirming key-based login works.

**Step 2: Edit the SSH server configuration:**

```bash
sudo nano /etc/ssh/sshd_config
```

Change or add these settings:

```
# Disable password authentication
PasswordAuthentication no

# Disable empty passwords
PermitEmptyPasswords no

# Disable root login
PermitRootLogin no

# Use only modern, secure algorithms
Protocol 2

# Limit SSH to specific users (replace with actual usernames)
AllowUsers alice bob

# Change from the default port (optional, reduces noise in logs)
Port 2222

# Disconnect idle sessions after 10 minutes
ClientAliveInterval 300
ClientAliveCountMax 2
```

**Step 3: Test the configuration before restarting:**

```bash
sudo sshd -t
```

If there are no errors, restart SSH:

```bash
sudo systemctl restart ssh
```

> **Critical:** Open a second terminal and verify we can still log in before closing the current session. If something is wrong, we can fix it while still connected.

### Restrict SSH Access by User
Only allow specific users to SSH in:

```bash
AllowUsers alice deploy
```

Or restrict to a group:

```bash
AllowGroups sshusers
```

### Disable Unused Authentication Methods

```
ChallengeResponseAuthentication no
KerberosAuthentication no
GSSAPIAuthentication no
```

---

## fail2ban — Blocking Brute-Force Attacks
Even with password auth disabled, attackers constantly scan for open SSH ports. **fail2ban** monitors log files and automatically bans IPs that show malicious behavior (too many failed login attempts).

### Installing fail2ban

```bash
sudo apt install fail2ban
```

### Basic Configuration
fail2ban reads from `/etc/fail2ban/jail.conf`, but we should never edit this file directly — it gets overwritten on updates. Instead, we create a local override:

```bash
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

Key settings in `[DEFAULT]`:

```ini
[DEFAULT]
# Ban duration (in seconds, or use "1h", "1d")
bantime  = 1h

# Time window to count failures
findtime  = 10m

# Number of failures before banning
maxretry = 5

# Email notifications (configure if needed)
# destemail = admin@example.com

# Ignore these IPs (whitelist - add our own IP!)
ignoreip = 127.0.0.1/8 ::1 192.168.1.100
```

For SSH protection, ensure the `[sshd]` jail is enabled:

```ini
[sshd]
enabled = true
port    = ssh
logpath = /var/log/auth.log
maxretry = 3
```

If we changed the SSH port, update the `port` value:

```ini
[sshd]
enabled = true
port    = 2222
```

### Starting and Enabling fail2ban

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Managing fail2ban
Check the status of all jails:

```bash
sudo fail2ban-client status
```

Check a specific jail:

```bash
sudo fail2ban-client status sshd
```

Manually ban an IP:

```bash
sudo fail2ban-client set sshd banip 192.168.1.50
```

Unban an IP:

```bash
sudo fail2ban-client set sshd unbanip 192.168.1.50
```

View recent bans in the log:

```bash
sudo tail -f /var/log/fail2ban.log
```

---

## Firewall Configuration (ufw — revisited)
We covered ufw basics in the Networking guide. Here's the security-focused hardening approach:

```bash
# Start with a clean slate
sudo ufw default deny incoming    # Block all incoming by default
sudo ufw default allow outgoing   # Allow all outgoing by default

# Allow SSH (do this BEFORE enabling, or we'll lock ourselves out)
sudo ufw allow ssh

# Allow only what we need
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS

# If we're running a database, restrict to specific IP only
sudo ufw allow from 192.168.1.0/24 to any port 5432   # PostgreSQL from LAN only

# Enable
sudo ufw enable

# Verify
sudo ufw status verbose
```

**Rate limiting with ufw** — limit SSH connections to prevent brute-force:

```bash
sudo ufw limit ssh    # Allows max 6 connections per 30 seconds from a single IP
```

---

## User and Privilege Hardening

### Audit Users with Login Access
Review which users can log in:

```bash
# Users with real shells (can log in)
grep -vE "^#|nologin|false" /etc/passwd | cut -d: -f1,7

# Check for users with no password (dangerous!)
sudo passwd -S -a | grep " NP "

# Check sudo privileges
sudo cat /etc/sudoers
sudo ls /etc/sudoers.d/
```

### Disable Unnecessary System Accounts
System accounts used by services should have a no-login shell:

```bash
# Check current shell for a system user
grep www-data /etc/passwd

# Should look like: www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
# If not, fix it:
sudo usermod -s /usr/sbin/nologin www-data
```

### Restrict sudo Access
Principle of least privilege: users should only be able to sudo specific commands they need, not everything.

Edit with `visudo`:

```bash
sudo visudo -f /etc/sudoers.d/deploy
```

Add granular sudo rules:

```
# deploy user can only restart nginx and read logs
deploy ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx, /usr/bin/tail /var/log/nginx/*
```

### Lock Unused User Accounts

```bash
sudo passwd -l inactiveuser    # Lock account
sudo usermod -e 1 inactiveuser # Set account to expire immediately (1 = Jan 1, 1970)
```

---

## AppArmor — Mandatory Access Control
**AppArmor** is a Linux Security Module (LSM) that confines programs to a defined set of resources. Even if a program is compromised, AppArmor limits what it can do (read only certain files, access only certain network ports, etc.).

AppArmor is installed and enabled by default on Ubuntu.

### Checking AppArmor Status

```bash
sudo aa-status
```

Output shows: loaded profiles, enforced profiles, and which processes are confined.

### AppArmor Modes
- **enforce** — blocks violations and logs them
- **complain** — logs violations but doesn't block (useful for developing profiles)
- **disabled** — no enforcement

### Managing Profiles
Install the utilities:

```bash
sudo apt install apparmor-utils
```

To see which profiles are in enforce vs complain mode:

```bash
sudo aa-status | grep -A5 "profiles are in enforce"
```

To put a profile in complain mode (for testing):

```bash
sudo aa-complain /usr/sbin/nginx
```

To enforce a profile:

```bash
sudo aa-enforce /usr/sbin/nginx
```

### Checking Violations
AppArmor logs violations to syslog:

```bash
sudo dmesg | grep apparmor
sudo grep apparmor /var/log/syslog | tail -20
```

---

## System Auditing

### Check Recently Modified Files
After a potential intrusion, we want to know what changed:

```bash
# Files modified in the last 24 hours in /etc
find /etc -mtime -1 -type f

# Files modified in the last 7 days system-wide (excluding /proc, /sys)
find / -mtime -7 -type f -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null
```

### Check for SUID/SGID Files
SUID/SGID files run with elevated privileges — unexpected ones could indicate compromise:

```bash
# Find all SUID files
find / -perm -4000 -type f 2>/dev/null

# Find all SGID files  
find / -perm -2000 -type f 2>/dev/null

# Find world-writable files (anyone can modify these)
find / -perm -o+w -type f -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null
```

Compare this list against a known-good baseline. Any unexpected SUID binary is suspicious.

### Checking Login History

```bash
last              # All login history
last -20          # Last 20 logins
lastb             # Failed login attempts
lastb | head -20  # Most recent failed attempts
who               # Who is currently logged in
w                 # Who is logged in and what they're doing
```

Look for logins from unexpected locations or at unusual hours.

### Checking for Listening Services
Periodically audit what's listening on our network:

```bash
sudo ss -tulnp          # All listening sockets with process names
sudo netstat -tulnp     # Same with netstat (if installed)
```

Any unexpected listening service is a security concern.

---

## Keeping the System Updated
The single most effective security measure is keeping software updated. Unpatched vulnerabilities are the primary attack vector.

```bash
# Update everything
sudo apt update && sudo apt upgrade

# Apply only security updates
sudo apt-get --only-upgrade install $(apt-get --simulate upgrade | grep "^Inst" | grep -i security | awk '{print $2}')
```

### Enabling Automatic Security Updates
Ubuntu/Debian can apply security updates automatically:

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades
```

The configuration in `/etc/apt/apt.conf.d/50unattended-upgrades` controls what gets auto-updated. By default, only security updates are applied automatically.

---

## Security Checklist
Use this as a quick reference when hardening a new server:

| Task | Command/File | Status |
|------|-------------|--------|
| SSH: Disable password auth | `/etc/ssh/sshd_config`: `PasswordAuthentication no` | ☐ |
| SSH: Disable root login | `/etc/ssh/sshd_config`: `PermitRootLogin no` | ☐ |
| SSH: Restrict to specific users | `/etc/ssh/sshd_config`: `AllowUsers` | ☐ |
| Firewall: Default deny incoming | `sudo ufw default deny incoming` | ☐ |
| Firewall: Allow only needed ports | `sudo ufw allow ...` | ☐ |
| fail2ban: Installed and configured | `sudo systemctl status fail2ban` | ☐ |
| Users: No unnecessary accounts | `cat /etc/passwd` review | ☐ |
| Users: Service accounts use nologin | `grep nologin /etc/passwd` | ☐ |
| Updates: System is current | `sudo apt update && apt upgrade` | ☐ |
| Auto-updates: Security updates enabled | `unattended-upgrades` | ☐ |
| AppArmor: Active and enforcing | `sudo aa-status` | ☐ |
| Audit: No unexpected SUID files | `find / -perm -4000` reviewed | ☐ |
| Audit: No unexpected open ports | `ss -tulnp` reviewed | ☐ |