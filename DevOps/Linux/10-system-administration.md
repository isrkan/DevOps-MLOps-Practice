# System Administration — Managing Our Linux System

System administration is the practice of keeping a Linux system healthy, organized, and running efficiently. Whether we're managing a personal WSL environment or a production server, these skills are essential: monitoring disk space, understanding memory usage, reading logs, automating tasks with cron, and managing archives and environment configuration.

---

## Disk and Storage
Running out of disk space silently causes mysterious failures — applications crash, databases corrupt, logs stop recording. Monitoring and managing disk space is a fundamental sysadmin habit.

#### df — Disk filesystem usage
`df` (disk free) shows how much space is used and available on each mounted filesystem:

```bash
df -h
```

The `-h` flag makes sizes **human-readable** (KB, MB, GB instead of raw bytes).

Output:

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        50G   18G   30G  38% /
tmpfs           2.0G  2.1M  2.0G   1% /run
/dev/sdb1       100G   55G   45G  55% /data
```

Key columns:
- `Size` — total filesystem size
- `Used` — space consumed
- `Avail` — free space remaining
- `Use%` — percentage used (watch this — above 90% is a warning sign)
- `Mounted on` — the directory where this filesystem is mounted

To see disk usage for a specific path:

```bash
df -h /home
```

To show only local filesystems (exclude virtual/network ones):

```bash
df -h -x tmpfs -x devtmpfs
```

#### du — Directory/file size
`df` shows filesystem-level space; `du` (disk usage) shows how much space a specific file or directory occupies:

```bash
du -sh ~/Documents
```

Output: `45M    /home/alice/Documents`

The `-s` flag shows a **summary** (total only), and `-h` makes it human-readable.

To see the size of everything in the current directory:

```bash
du -sh *
```

This is one of the most useful commands for finding where disk space went. Sort by size to find the largest items:

```bash
du -sh * | sort -h
```

To find the largest directories under `/var` (sorted):

```bash
du -h /var/* | sort -h | tail -20
```

To show sizes at specific depth levels:

```bash
du -h --max-depth=2 /home/alice
```

#### lsblk — List block devices
`lsblk` shows all block devices (disks, partitions, LVM volumes) in a tree format:

```bash
lsblk
```

Output:

```
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   50G  0 disk
├─sda1   8:1    0   49G  0 part /
└─sda2   8:2    0    1G  0 part [SWAP]
sdb      8:16   0  100G  0 disk
└─sdb1   8:17   0  100G  0 part /data
```

This shows us how disks are partitioned and where each partition is mounted.

#### mount and umount — Mounting filesystems
To manually mount a filesystem (e.g., a USB drive or disk partition):

```bash
sudo mount /dev/sdb1 /mnt/usb
```

The device `/dev/sdb1` is now accessible at `/mnt/usb`.

To unmount (always unmount before physically removing a drive!):

```bash
sudo umount /mnt/usb
```

To see all currently mounted filesystems:

```bash
mount | grep -v "cgroup\|proc\|sys"
```

---

## Memory and CPU

#### free — Memory usage
`free` shows how much RAM and swap space is being used:

```bash
free -h
```

Output:

```
              total        used        free      shared  buff/cache   available
Mem:          7.8Gi       2.1Gi       3.2Gi       234Mi       2.5Gi       5.2Gi
Swap:         2.0Gi          0B       2.0Gi
```

Key columns:
- `total` — total installed RAM
- `used` — RAM currently used by programs
- `free` — completely unused RAM
- `buff/cache` — RAM used for disk caching (Linux reclaims this when programs need it)
- `available` — RAM effectively available for new programs (free + reclaimable cache)

**Important:** The `available` column is the one that actually matters. `free` RAM alone can be misleadingly low because Linux aggressively uses free RAM for disk caching (which is a feature, not a problem).

Swap space is disk space used as overflow when RAM is full. Heavy swap usage indicates we need more RAM.

#### vmstat — Virtual memory statistics
`vmstat` gives a quick overview of memory, CPU, and I/O activity:

```bash
vmstat 2 5
```

This reports every 2 seconds, 5 times. Useful columns:
- `si`/`so` — swap in/out (non-zero means we're swapping)
- `us`/`sy`/`id` — CPU time: user/system/idle

#### uptime — System uptime and load average
`uptime` shows how long the system has been running and the **load average**:

```bash
uptime
```

Output:

```
 10:30:15 up 5 days,  3:22,  2 users,  load average: 0.52, 0.48, 0.51
```

The three numbers are CPU load averages over 1, 5, and 15 minutes. A load average equal to our number of CPU cores means the system is fully utilized; higher means processes are waiting for CPU time.

To see how many CPU cores we have:

```bash
nproc
```

A load of 1.0 on a 4-core machine means 25% utilization — that's fine. A load of 4.0 means all cores are fully busy.

#### uname — System and kernel information
`uname -a` shows comprehensive system information including the kernel version and architecture:

```bash
uname -a
```

Output:

```
Linux myhostname 5.15.0-91-generic #101-Ubuntu SMP Thu Nov 9 10:24:08 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

Fields: kernel name, hostname, kernel release, kernel version, machine hardware, OS.

To see just the kernel version:

```bash
uname -r
```

#### lscpu — CPU details
`lscpu` shows detailed CPU information:

```bash
lscpu
```

Useful for understanding our hardware: number of cores, threads, CPU model, cache sizes, and architecture.

---

## Archives and Compression
Linux has powerful tools for creating archives (combining multiple files into one) and compressing them to save space. The most common combination is `tar` + `gzip`.

#### tar — Tape archive
`tar` is the primary archiving tool. It combines multiple files and directories into a single archive file (`.tar`).

**Creating a compressed archive:**

```bash
tar -czf archive.tar.gz directory/
```

Breaking down the flags:
- `-c` — **create** a new archive
- `-z` — compress with **gzip** (adds the `.gz` compression)
- `-f archive.tar.gz` — **file** name of the archive
- `directory/` — what to archive

To archive multiple items:

```bash
tar -czf backup.tar.gz ~/Documents ~/projects config.txt
```

**Extracting an archive:**

```bash
tar -xzf archive.tar.gz
```

- `-x` — **extract** files
- `-z` — decompress with gzip
- `-f archive.tar.gz` — the archive file to extract

To extract to a specific directory:

```bash
tar -xzf archive.tar.gz -C /tmp/extracted/
```

**Listing archive contents without extracting:**

```bash
tar -tzf archive.tar.gz
```

**Verbose output** (shows each file as it's archived/extracted):

```bash
tar -czvf archive.tar.gz directory/
tar -xzvf archive.tar.gz
```

#### Other compression formats
**bzip2** (`.tar.bz2`) — slower but better compression than gzip:

```bash
tar -cjf archive.tar.bz2 directory/    # Create (j = bzip2)
tar -xjf archive.tar.bz2               # Extract
```

**xz** (`.tar.xz`) — best compression ratio but slowest:

```bash
tar -cJf archive.tar.xz directory/    # Create (J = xz)
tar -xJf archive.tar.xz               # Extract
```

**gzip/gunzip** for single files:

```bash
gzip large_file.log          # Creates large_file.log.gz, removes original
gunzip large_file.log.gz     # Decompresses, removes .gz
```

**zip/unzip** (Windows-compatible format):

```bash
zip -r archive.zip directory/    # Create (r = recursive)
unzip archive.zip                # Extract
unzip -l archive.zip             # List contents
```

#### Compression format quick reference

| Format | Extension | Create | Extract | Notes |
|--------|-----------|--------|---------|-------|
| gzip | `.tar.gz` | `tar -czf` | `tar -xzf` | Fast, good ratio, default choice |
| bzip2 | `.tar.bz2` | `tar -cjf` | `tar -xjf` | Better ratio, slower |
| xz | `.tar.xz` | `tar -cJf` | `tar -xJf` | Best ratio, slowest |
| zip | `.zip` | `zip -r` | `unzip` | Windows compatible |

---

## Environment Variables
**Environment variables** are key-value pairs that programs read to configure their behavior. They're how Linux communicates settings to running processes.

#### Viewing environment variables
To see all current environment variables:

```bash
printenv
```

Or:

```bash
env
```

To see a specific variable:

```bash
printenv HOME
printenv PATH
echo $HOME
echo $PATH
```

Important environment variables:
- `PATH` — colon-separated list of directories where Linux looks for executables
- `HOME` — our home directory path
- `USER` — our username
- `SHELL` — path to our current shell
- `LANG` — language/locale setting
- `EDITOR` — default text editor (used by git, cron, etc.)

#### Setting environment variables
To set a variable for the current session only:

```bash
export MY_VAR="hello"
```

After `export`, child processes (programs we run) can also see this variable.

Without `export`, the variable is only visible to the current shell:

```bash
MY_VAR="hello"          # Only visible in current shell
export MY_VAR="hello"   # Visible to current shell and child processes
```

#### Making variables permanent
Variables set with `export` in the terminal are lost when we close the terminal. To make them permanent, we add them to our shell's configuration file.

For Bash, the relevant files are:
- **`~/.bashrc`** — loaded every time we open a new interactive terminal
- **`~/.bash_profile`** or **`~/.profile`** — loaded once at login (SSH sessions, terminal on login)

For most purposes, `~/.bashrc` is the right place:

```bash
nano ~/.bashrc
```

Add at the end:

```bash
export MY_API_KEY="abc123"
export JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
```

To apply changes without restarting the terminal:

```bash
source ~/.bashrc
# or equivalently:
. ~/.bashrc
```

#### Adding to PATH
A very common need is adding a new directory to `PATH` so Linux can find executables there:

```bash
export PATH="$PATH:/opt/myapp/bin"
```

The `$PATH:` at the beginning preserves the existing PATH and appends our new directory. Never overwrite `PATH` without including the original — it would break most commands.

Add to `~/.bashrc` to make it permanent:

```bash
echo 'export PATH="$PATH:/opt/myapp/bin"' >> ~/.bashrc
source ~/.bashrc
```

---

## System Logs
Logs are the first place to look when something goes wrong. Linux logs everything: service starts/stops, authentication attempts, hardware errors, application messages.

#### journalctl — systemd's journal
On modern Ubuntu/Debian, systemd collects all logs in the **journal**:

View all logs (very long — pipe through `less`):

```bash
journalctl | less
```

View logs for a specific service:

```bash
journalctl -u nginx
journalctl -u ssh
```

Follow a service's logs in real time:

```bash
journalctl -u nginx -f
```

Show only the last N lines:

```bash
journalctl -u nginx -n 50
```

Filter by time:

```bash
journalctl --since "2024-04-01 10:00:00" --until "2024-04-01 11:00:00"
journalctl --since "1 hour ago"
journalctl --since today
```

Show only error messages and above:

```bash
journalctl -p err
```

Priority levels: `emerg`, `alert`, `crit`, `err`, `warning`, `notice`, `info`, `debug`

#### Log files in /var/log/
Traditional log files are still written to `/var/log/`. Key files on Ubuntu/Debian:

- `/var/log/syslog` — general system log (most important catch-all)
- `/var/log/auth.log` — authentication events (logins, sudo use, SSH)
- `/var/log/kern.log` — kernel messages
- `/var/log/dpkg.log` — package installation/removal history
- `/var/log/apt/history.log` — APT operations history
- `/var/log/nginx/access.log` — nginx web server access log
- `/var/log/nginx/error.log` — nginx error log

To watch a log file in real time:

```bash
tail -f /var/log/syslog
tail -f /var/log/auth.log
```

To search for specific errors:

```bash
grep -i "error" /var/log/syslog | tail -20
grep "Failed password" /var/log/auth.log
```

---

## Scheduled Tasks with cron
**cron** is the standard Linux scheduler. It runs commands at specified times — every minute, every hour, every day, on specific days — automatically, without any manual intervention. Cron is how we automate backups, reports, cleanup tasks, and more.

#### crontab — Edit scheduled jobs
Each user has their own crontab (cron table) listing their scheduled jobs. To edit it:

```bash
crontab -e
```

This opens our crontab in our default editor (usually nano or vim). The first time, it might ask which editor to use.

To view our current crontab:

```bash
crontab -l
```

To remove all crontab entries:

```bash
crontab -r
```

#### Cron syntax
Each crontab line has 6 fields:

```
┌───────── minute (0-59)
│ ┌─────── hour (0-23)
│ │ ┌───── day of month (1-31)
│ │ │ ┌─── month (1-12 or jan-dec)
│ │ │ │ ┌─ day of week (0-7, where 0 and 7 = Sunday, or sun-sat)
│ │ │ │ │
* * * * *  command to execute
```

Special values:
- `*` — every value (any)
- `5` — exactly at 5
- `1-5` — range (1 through 5)
- `*/15` — every 15 (step value)
- `1,3,5` — specific values

#### Example cron jobs

```bash
# Run backup every day at 2:30 AM
30 2 * * * /home/alice/scripts/backup.sh

# Run script every 15 minutes
*/15 * * * * /home/alice/scripts/monitor.sh

# Run cleanup every Sunday at midnight
0 0 * * 0 /home/alice/scripts/cleanup.sh

# Run a script at 9 AM on weekdays (Monday-Friday)
0 9 * * 1-5 /home/alice/scripts/workday_report.sh

# Run on the first day of every month
0 6 1 * * /home/alice/scripts/monthly_report.sh
```

**Redirect cron output to a log file** — by default, cron emails output. Redirect it to a file instead:

```bash
30 2 * * * /home/alice/scripts/backup.sh >> /var/log/backup.log 2>&1
```

The `>> /var/log/backup.log` appends stdout to the log file. `2>&1` redirects stderr to stdout (so errors are also logged).

**Common mistake:** Cron runs in a minimal environment — the `PATH` is much shorter than our interactive shell. Specify full paths to commands in crontab:

```bash
# Instead of:
30 2 * * * backup.sh

# Use full paths:
30 2 * * * /home/alice/scripts/backup.sh
```

Or set PATH at the top of the crontab:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

---

## Hostname and Time

#### Managing the hostname
To view the current hostname:

```bash
hostname
```

To see full hostname details:

```bash
hostnamectl
```

To change the hostname:

```bash
sudo hostnamectl set-hostname newname
```

After changing, update `/etc/hosts` to map the new hostname to `127.0.1.1`.

#### Managing time and timezone
Servers must have the correct time — logs, cron jobs, SSL certificates, and distributed systems all depend on accurate time.

To view current time and timezone settings:

```bash
timedatectl
```

To list available timezones:

```bash
timedatectl list-timezones | grep Europe
timedatectl list-timezones | grep America
```

To set our timezone:

```bash
sudo timedatectl set-timezone America/New_York
sudo timedatectl set-timezone Europe/London
```

To enable automatic time synchronization (NTP):

```bash
sudo timedatectl set-ntp true
```