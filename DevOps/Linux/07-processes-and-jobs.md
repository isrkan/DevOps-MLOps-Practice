# Processes and Jobs — Managing Running Programs

Every program that runs on Linux is a **process**. When we type a command, open a web server, or run a script, Linux creates a process to execute it. Understanding how to view, monitor, control, and terminate processes is essential for diagnosing problems, managing system resources, and keeping our system running smoothly.

This guide covers process management — from viewing what's running to controlling processes in the foreground and background, to managing system services with systemd.

---

## What Is a Process?
A **process** is an instance of a running program. Every process has:

- **PID** (Process ID) — a unique number identifying this specific process
- **PPID** (Parent Process ID) — the PID of the process that created this one
- **Owner** — the user account this process is running as
- **State** — running, sleeping, stopped, zombie, etc.
- **Resources** — CPU and memory being used

When we open a terminal, a `bash` process starts. When we run `ls`, bash creates a child process (the `ls` process). When `ls` finishes, the child process exits, and bash continues.

The process with PID 1 is special — it's the **init** process (on modern Ubuntu/Debian, this is **systemd**). It's the first process the kernel starts and the ancestor of all other processes.

---

## Viewing Processes

#### ps — Process snapshot
`ps` shows a snapshot of currently running processes. By default it shows only processes in our current terminal session:

```bash
ps
```

Output:

```
  PID TTY          TIME CMD
 1234 pts/0    00:00:00 bash
 5678 pts/0    00:00:00 ps
```

To see **all** processes from all users in a comprehensive format, use:

```bash
ps aux
```

The flags mean:
- `a` — show processes from all users
- `u` — show in user-oriented format (includes owner, CPU/memory %)
- `x` — show processes without a terminal (background daemons)

Output columns:

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0 168420 13340 ?        Ss   08:00   0:01 /sbin/init
alice     1234  0.0  0.1  10312  5120 pts/0    Ss   09:15   0:00 bash
alice     5678  0.0  0.0   8316  2048 pts/0    R+   09:16   0:00 ps aux
```

Key columns:
- `USER` — the user who owns this process
- `PID` — process ID
- `%CPU` — CPU usage percentage
- `%MEM` — memory usage percentage
- `STAT` — process state (`S`=sleeping, `R`=running, `Z`=zombie, `T`=stopped)
- `COMMAND` — the command that started the process

To see processes in a tree view showing parent-child relationships:

```bash
ps axjf
```

Or install and use `pstree`:

```bash
pstree
```

#### pgrep — Find a process by name
`pgrep` searches for processes by name and returns their PIDs:

```bash
pgrep nginx
```

Output: the PID(s) of running nginx processes.

To see the process name alongside the PID:

```bash
pgrep -l nginx
```

#### top — Real-time process monitor
`top` shows a live, continuously-updating display of running processes sorted by CPU usage:

```bash
top
```

The screen updates every few seconds. The top section shows overall system statistics (uptime, load average, CPU usage, memory usage). Below that is the process list.

Useful keyboard shortcuts inside `top`:
- `q` — quit
- `k` — kill a process (prompts for PID)
- `M` — sort by memory usage
- `P` — sort by CPU usage (default)
- `1` — toggle showing individual CPU cores
- `h` — help
- `u <username>` — filter by user

**Load average** shown by top is one of the most important metrics. It shows system load over 1, 5, and 15 minutes. A load average equal to the number of CPU cores means the system is fully loaded; higher means processes are waiting.

#### htop — An Improved top
`htop` is an enhanced, color-coded version of `top` with a friendlier interface. We need to install it first:

```bash
sudo apt install htop
```

Then:

```bash
htop
```

`htop` shows CPU and memory bars visually, supports mouse interaction, and makes it easy to kill processes with `F9`.

---

## Killing Processes
Sometimes a process stops responding, uses too many resources, or needs to be stopped for other reasons. We can terminate processes by sending them **signals**.

#### kill — Send a signal to a process by PID
The most common signal is SIGTERM (signal 15), which politely asks a process to stop:

```bash
kill <PID>
```

For example, to kill process 5678:

```bash
kill 5678
```

SIGTERM gives the process a chance to clean up — close files, save state, release resources. Most well-written programs respond to SIGTERM gracefully.

If a process ignores SIGTERM, we can send SIGKILL (signal 9), which **forcibly** terminates the process with no cleanup:

```bash
kill -9 <PID>
```

SIGKILL cannot be caught or ignored by the process — the kernel terminates it immediately. Use it as a last resort, as the process won't have a chance to clean up.

#### pkill — Kill by process name
Instead of finding the PID first with `pgrep`, we can kill by name directly:

```bash
pkill nginx
```

This sends SIGTERM to all processes named `nginx`. To force kill:

```bash
pkill -9 nginx
```

#### killall — Kill all processes with a name
`killall` terminates all processes with the exact specified name:

```bash
killall firefox
```

#### Common signals table

| Signal | Number | Name | Meaning |
|--------|--------|------|---------|
| `SIGTERM` | 15 | Terminate | Polite request to stop (default `kill`) |
| `SIGKILL` | 9 | Kill | Force termination (cannot be ignored) |
| `SIGHUP` | 1 | Hangup | Reload configuration (for daemons) |
| `SIGINT` | 2 | Interrupt | Same as `Ctrl+C` |
| `SIGSTOP` | 19 | Stop | Pause process (like `Ctrl+Z`) |
| `SIGCONT` | 18 | Continue | Resume a stopped process |

Daemons (background services) often respond to SIGHUP by reloading their configuration file without restarting:

```bash
kill -HUP <PID>
# or equivalently:
kill -1 <PID>
```

---

## Foreground and Background Jobs
When we run a command, it normally runs in the **foreground** — it takes over our terminal until it finishes. **Background** jobs run independently, freeing up our terminal for other commands.

#### Running a command in the background with `&`
Add `&` at the end of a command to start it in the background immediately:

```bash
python3 server.py &
```

Output: `[1] 12345` — the `[1]` is the **job number** and `12345` is the PID.

Our terminal is immediately free to use. The background process continues running.

#### jobs — List background jobs
To see all background jobs in our current terminal session:

```bash
jobs
```

Output:

```
[1]+  Running    python3 server.py &
[2]-  Stopped    vim notes.txt
```

Job numbers (in brackets) are session-local — different from PIDs.

#### Ctrl+Z — Pause a foreground process
To pause (suspend) the currently running foreground process, press `Ctrl+Z`:

```
^Z
[1]+  Stopped    vim notes.txt
```

The process is paused (not killed) and sent to the background in a stopped state.

#### bg — Resume a stopped job in the background
After pressing `Ctrl+Z`, we can resume the paused process in the background:

```bash
bg %1
```

The `%1` refers to job number 1. Without a number, `bg` resumes the most recently stopped job.

#### fg — Bring a background job to the foreground
To bring a background job back to the foreground (making it interactive again):

```bash
fg %1
```

This is useful when we backgrounded a text editor or interactive program and want to return to it.

#### nohup — Run a command immune to hangups
When we log out (or close a terminal), all processes in that session receive SIGHUP and typically terminate. `nohup` makes a command immune to this signal, so it continues running even after we log out:

```bash
nohup python3 long_script.py &
```

Output is redirected to `nohup.out` by default (unless we redirect it ourselves):

```bash
nohup python3 long_script.py > output.log 2>&1 &
```

`nohup` is useful for long-running jobs on remote servers where we might disconnect.

---

## Process Priority — nice and renice
Linux assigns each process a **priority** that affects how much CPU time it gets relative to other processes. The priority is expressed as a "niceness" value from **-20** (highest priority) to **19** (lowest priority). The default is 0.

The name "nice" comes from the idea that a "nice" process voluntarily gives up CPU time for others.

#### Running a command with a specific niceness
To start a CPU-intensive job with low priority (so it doesn't slow down other processes):

```bash
nice -n 10 python3 heavy_computation.py
```

A positive nice value = lower priority (be "nicer" to other processes).
Only root can set negative values (higher priority).

#### renice — Change priority of a running process
To change the priority of an already-running process:

```bash
sudo renice -n 5 -p <PID>
```

To lower the priority of all processes owned by a user:

```bash
sudo renice -n 10 -u alice
```

---

## systemd and Services
Modern Ubuntu and Debian use **systemd** as their init system and service manager. systemd manages background services (called **units**) — things like web servers, databases, SSH, and network services that start automatically at boot and run continuously.

#### Understanding systemd units
In systemd, "services" are a type of "unit." Unit configuration files typically live in `/etc/systemd/system/` or `/lib/systemd/system/` with a `.service` extension.

#### systemctl — Control the systemd service manager
To start a service:

```bash
sudo systemctl start nginx
```

To stop a service:

```bash
sudo systemctl stop nginx
```

To restart a service (stop then start):

```bash
sudo systemctl restart nginx
```

To reload a service's configuration without fully restarting (if supported by the service):

```bash
sudo systemctl reload nginx
```

To check the status of a service (shows if it's running, recent log output, errors):

```bash
sudo systemctl status nginx
```

Output includes whether the service is active/running, when it started, and the most recent log lines — very useful for quick diagnostics.

To enable a service to start automatically at boot:

```bash
sudo systemctl enable nginx
```

To disable autostart:

```bash
sudo systemctl disable nginx
```

To enable and start immediately in one command:

```bash
sudo systemctl enable --now nginx
```

To list all running services:

```bash
systemctl list-units --type=service --state=running
```

To list all services (running and stopped):

```bash
systemctl list-units --type=service
```

#### journalctl — View systemd logs
systemd logs everything to the **journal**. To view logs for a specific service:

```bash
journalctl -u nginx
```

To follow logs in real time (like `tail -f`):

```bash
journalctl -u nginx -f
```

To see only the last 50 lines:

```bash
journalctl -u nginx -n 50
```

To see logs from the last hour:

```bash
journalctl -u nginx --since "1 hour ago"
```

To see all system logs (can be very long):

```bash
journalctl
```