# Creating systemd Service Units — Running Our Own Services

In the Processes guide we learned to use `systemctl` to manage existing services like nginx, ssh, and PostgreSQL. But what about our own applications? When we build a web server, a monitoring script, or a background data processor — how do we make it start automatically at boot, restart on failure, and integrate with the system logs?

The answer is: we write a **systemd service unit** file. This guide explains how. Once we understand unit files, we essentially understand how *every* service on a modern Linux system works — nginx, PostgreSQL, Docker, and our own apps all use the same mechanism.

---

## What Is a systemd Unit?
**systemd** is the service manager that runs as **PID 1** on modern Ubuntu/Debian systems — the very first process the kernel starts at boot, and the parent (directly or indirectly) of every other process. It manages all services and reads **unit files** — plain text configuration files in INI format — to know how to start, stop, and monitor each one. Before systemd, services were managed by older systems like SysVinit (using shell scripts in `/etc/init.d/`) or Upstart, but those have been largely retired. systemd unified all this into a consistent, declarative format.

Unit files live in two locations:
- `/lib/systemd/system/` — system-provided units (installed by packages). Don't edit these directly; updates will overwrite them.
- `/etc/systemd/system/` — our custom units (override system units too). systemd checks `/etc/systemd/system/` first, so a file with the same name here takes precedence over the version in `/lib/`.

We always create our own units in `/etc/systemd/system/`. The split exists for the same reason `/etc/` exists in general: package-provided defaults stay separate from local configuration, so system updates and our customizations don't fight.

Types of units (identified by file extension):
- `.service` — a process to manage (most common). Web servers, databases, custom apps.
- `.timer` — a scheduled task (like cron, but integrated with systemd). Triggers a service at specific times.
- `.socket` — socket-activated service. systemd opens the network port and only starts the actual service when a connection arrives — useful for rarely-used services.
- `.target` — a group of units (like a "runlevel"). For example, `multi-user.target` represents "system is fully booted, multi-user, no GUI."

This guide focuses on `.service` and `.timer` units, which cover 95% of real-world use cases.

---

> **What is an INI file?**
> INI is a simple, human-readable configuration file format that's been around since the early days of Windows (the name comes from the `.ini` extension, short for "initialization"). It organizes settings into named **sections** marked with square brackets, and inside each section, simple `Key=Value` pairs:
>
> ```ini
> [SectionName]
> Key1=Value1
> Key2=Value2
>
> [AnotherSection]
> Setting=Value
> ```
>
> INI's appeal is that it's trivial to read, edit by hand, and parse programmatically — no nested structures or quoting rules to fight with. It's used widely beyond systemd: Git's `~/.gitconfig`, Python's `configparser` module, PHP's `php.ini`, desktop entry files (`.desktop`), and many other tools all use INI or close variants. Lines starting with `#` are comments. systemd's unit files follow this format exactly, with sections like `[Unit]`, `[Service]`, and `[Install]` (which we'll see in a moment).

---

## Anatomy of a Service Unit File
A service unit file is a plain text file with three main sections, written in **INI format** (`[Section]` headers, `Key=Value` lines):

```ini
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/myapp --config /etc/myapp/config.yaml
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Each section answers a different question: `[Unit]` is metadata and dependencies (*who is this and what does it depend on?*), `[Service]` is the actual runtime configuration (*how do I run it?*), and `[Install]` controls what happens when we run `systemctl enable` (*when should it auto-start?*). Let's look at each one.

### [Unit] Section — Metadata and Dependencies

```ini
[Unit]
Description=My Application
Documentation=https://myapp.example.com/docs
After=network.target
After=postgresql.service
Requires=postgresql.service
```

Key directives:

| Directive | Meaning |
|-----------|---------|
| `Description=` | Human-readable name shown in `systemctl status` |
| `Documentation=` | URL or man page reference |
| `After=` | Start this unit only after the listed units are active |
| `Before=` | Start this unit before the listed units |
| `Requires=` | Hard dependency — if the required unit fails, this one fails too |
| `Wants=` | Soft dependency — start the listed units too, but continue even if they fail |
| `BindsTo=` | Like Requires, but also stop this unit when the required unit stops |

A subtle but important point: `After=`/`Before=` control **ordering** (the sequence in which things start), while `Requires=`/`Wants=` control **dependencies** (whether other things should start at all). These are independent! `Requires=postgresql.service` alone tells systemd "make sure postgres is running" but doesn't say *when* to start our service relative to it — we likely also want `After=postgresql.service` to make sure postgres is fully up before our app tries to connect. Forgetting one of them is one of the most common systemd bugs.

Common `After=` targets:
- `network.target` — after basic networking is up (interfaces are configured, but DNS may not work yet)
- `network-online.target` — after network is fully configured (more reliable). Use this if our service needs to make outbound connections at startup.
- `local-fs.target` — after local filesystems are mounted
- `multi-user.target` — after system is fully booted in multi-user mode

### [Service] Section — How to Run the Service

```ini
[Service]
Type=simple
User=appuser
Group=appgroup
WorkingDirectory=/opt/myapp
Environment="NODE_ENV=production" "PORT=3000"
EnvironmentFile=/etc/myapp/env
ExecStart=/usr/bin/python3 /opt/myapp/server.py
ExecStop=/bin/kill -SIGTERM $MAINPID
ExecReload=/bin/kill -SIGHUP $MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
```

This is the heart of the unit file — every line here directly affects how the process actually runs. A couple of notes about the directives that aren't always needed: `ExecStop` is usually unnecessary because systemd already sends SIGTERM by default when stopping. `ExecReload` defines what happens when we run `systemctl reload` — typically a signal that tells the app to re-read its config without restarting (useful for nginx, for example).

#### Service Types

| Type | Meaning |
|------|---------|
| `simple` | Process started with `ExecStart` is the main process (default) |
| `exec` | Like simple, but systemd waits until the executable is invoked |
| `forking` | Process forks itself; parent exits; child is the daemon |
| `oneshot` | Process exits after completing; systemd waits for it |
| `notify` | Process sends systemd a notification when ready |
| `idle` | Like simple, but delays start until other jobs are done |

Most applications use `simple` (anything that stays in the foreground) or `forking` (traditional daemons). The right choice depends on how the program behaves: if our app stays in the foreground and prints to stdout (most modern apps, especially containers and language runtimes like Python/Node.js), `simple` is correct. If the program "daemonizes" itself by forking into the background and the parent process exits (older Unix style), use `forking`. `oneshot` is perfect for setup or migration scripts that do their job once and exit — systemd considers them "active" while running and "inactive (dead)" afterwards, which is exactly the right semantics for a one-time job.

#### User and Security

```ini
User=appuser               # Run as this user (not root!)
Group=appgroup             # Run with this group
WorkingDirectory=/opt/app  # Start from this directory
```

**Always run services as a dedicated non-root user.** If the service is compromised, a non-root user limits the damage. A web server running as root that's exploited can do *anything* — read every file, install malware, pivot to other systems. The same web server running as `webappuser` can only touch files that user owns. This is the single most important security setting in a unit file.

By convention, we create a dedicated system user per service (e.g., `nginx`, `postgres`, `mywebappuser`) rather than running multiple services as the same user — that way, a compromise of one service can't easily affect another.

#### Environment Variables

```ini
# Set individual variables directly
Environment="KEY=value" "ANOTHER_KEY=value"

# Or load from a file (one KEY=value per line)
EnvironmentFile=/etc/myapp/env
EnvironmentFile=-/etc/myapp/optional.env   # Leading - means "ignore if missing"
```

`EnvironmentFile=` is the preferred way to handle secrets and configuration: it keeps sensitive data (database passwords, API keys) out of the unit file itself, which is often committed to version control. The unit file is safe to share; the env file stays on the server with restrictive permissions. The leading `-` is a useful pattern for optional config — for example, a `local-overrides.env` that exists only on developer machines.

#### Restart Behavior

| Directive | Meaning |
|-----------|---------|
| `Restart=no` | Never restart (default) |
| `Restart=on-failure` | Restart only if the process exited with non-zero code |
| `Restart=always` | Always restart (except if we stopped it manually) |
| `Restart=on-abnormal` | Restart on signals, watchdog, non-clean exit |
| `RestartSec=5` | Wait 5 seconds before restarting |
| `StartLimitIntervalSec=60` | Window for restart limit |
| `StartLimitBurst=3` | Max restarts within the window |

Auto-restart is one of systemd's most useful features — it turns "the process crashed in the middle of the night" into a self-healing event instead of a 3am page. The choice between `on-failure` and `always` matters: `on-failure` won't restart a service that exited cleanly with code 0 (which might be desired behavior — the service finished its job). `always` restarts no matter what, useful for things that should *never* be down.

The `StartLimitIntervalSec`/`StartLimitBurst` pair prevents restart loops. If our service crashes immediately on startup (say, due to a bad config), without limits systemd would restart it forever, burning CPU. With the defaults shown — 3 restarts per 60 seconds — systemd gives up after the burst and marks the service as failed, which is what we want: a noisy failure is better than a silent one.

#### Output Logging

```ini
StandardOutput=journal    # Send stdout to systemd journal (default)
StandardError=journal     # Send stderr to systemd journal (default)
StandardOutput=file:/var/log/myapp/stdout.log  # Or to a file
SyslogIdentifier=myapp    # Identifier shown in journal
```

The default — sending stdout/stderr to the systemd journal — is almost always what we want. The journal handles log rotation, indexing, and querying for us, and we can view our app's output with `journalctl -u myapp` from anywhere on the system. This is a major upgrade over the old "service writes to its own log file in /var/log/" pattern. `SyslogIdentifier=` is a small but nice touch that makes log entries easier to grep for.

### [Install] Section — When to Start

```ini
[Install]
WantedBy=multi-user.target
```

`WantedBy=multi-user.target` means "enable this service when the system reaches multi-user mode" (which is the normal booted state for servers without a GUI). This is the right value for almost all services.

Under the hood, this is what `systemctl enable` actually does: it creates a symlink from `/etc/systemd/system/multi-user.target.wants/myapp.service` pointing to our unit file. When systemd boots and reaches `multi-user.target`, it scans that `wants` directory and starts everything in it. So "enabling" a service is literally just creating that symlink, and "disabling" removes it. This is why the unit file *exists* on disk whether enabled or not — enabling just registers it for auto-start.

---

## Creating a Service: Step-by-Step Examples
The best way to internalize all this is to walk through a complete example. We'll build a real, working service from scratch.

### Example 1: A Simple Python Web Server
Let's make a Python script run as a permanent service.

**Step 1: Create the application and a dedicated user**

```bash
# Create application directory
sudo mkdir -p /opt/mywebapp

# Create the application file
sudo nano /opt/mywebapp/server.py
```

We're putting this under `/opt/` because that's the conventional Linux location for self-contained third-party or custom applications — separate from system binaries in `/usr/` and from package-managed software.

```python
#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

os.chdir('/opt/mywebapp/public')
server = HTTPServer(('0.0.0.0', 8080), SimpleHTTPRequestHandler)
print("Server running on port 8080")
server.serve_forever()
```

This is a deliberately tiny app that just serves files from a directory. Notice that it stays in the foreground (`serve_forever()` never returns) — this is what the `Type=simple` service type expects.

```bash
# Create a dedicated user (no login shell, no home directory)
sudo useradd -r -s /usr/sbin/nologin -d /opt/mywebapp webappuser

# Set ownership
sudo chown -R webappuser:webappuser /opt/mywebapp

# Create the public directory
sudo mkdir /opt/mywebapp/public
echo "<h1>Hello from systemd!</h1>" | sudo tee /opt/mywebapp/public/index.html
```

A few details about that `useradd` command:
- `-r` creates a **system user** with a UID below 1000 (the convention for non-human users) and no home directory in `/home/`.
- `-s /usr/sbin/nologin` sets the login shell to a special program that prints "This account is currently not available." and exits. If anyone (or any malware) tries to `su - webappuser` or SSH in as this user, they immediately get kicked out.
- `-d /opt/mywebapp` sets the user's home directory to the app directory, which is sometimes useful for processes that try to write config to `~`.

This pattern — *system user, no shell, no real home* — is the standard recipe for service accounts on Linux.

**Step 2: Create the service unit file**

```bash
sudo nano /etc/systemd/system/mywebapp.service
```

```ini
[Unit]
Description=My Python Web Application
After=network.target

[Service]
Type=simple
User=webappuser
WorkingDirectory=/opt/mywebapp
ExecStart=/usr/bin/python3 /opt/mywebapp/server.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mywebapp

[Install]
WantedBy=multi-user.target
```

Notice that `ExecStart` uses an **absolute path** to both the interpreter (`/usr/bin/python3`) and the script. systemd does *not* use our shell's `PATH` — every command must be specified as a full path. This catches a lot of beginners; if we just write `python3` here, systemd will report "executable not found." We can find the right path with `which python3`.

**Step 3: Reload systemd and start the service**

After creating or modifying a unit file, we must tell systemd to reload its configuration:

```bash
sudo systemctl daemon-reload
```

This is the most-forgotten step in working with systemd. systemd caches unit files in memory for performance; `daemon-reload` rescans the unit directories. Forgetting it leads to confusing situations where our edits seem to have no effect. Rule of thumb: any time we change a `.service` or `.timer` file, run `daemon-reload` before `restart`.

Now start and enable the service:

```bash
sudo systemctl start mywebapp
sudo systemctl enable mywebapp
```

Two distinct actions: `start` runs it *right now*, `enable` makes it run *automatically at boot*. They're independent — we can start without enabling (one-time test) or enable without starting (will start on next boot). Often we want both, which we can combine: `sudo systemctl enable --now mywebapp`.

**Step 4: Verify it's running**

```bash
sudo systemctl status mywebapp
```

Output shows active/running status and recent log lines. Look for `Active: active (running)` in green — that's the happy state. If we see `Active: failed`, the most useful next step is to look at the journal output that `status` shows underneath, which usually contains the actual error message. Test it:

```bash
curl http://localhost:8080
```

If we see our HTML, the service is working end-to-end: started by systemd, running as the dedicated user, listening on port 8080, serving files. View logs:

```bash
journalctl -u mywebapp -f
```

The `-u` filters to just our unit; `-f` follows new entries as they appear (like `tail -f`). This is one of the most useful commands when debugging a service.

### Example 2: A Service with Environment File
For services that need configuration (database credentials, API keys), use an environment file. This keeps secrets out of the unit file (which might end up in version control) and lets us change config without editing the unit.

**Create the environment file:**

```bash
sudo nano /etc/myapp/env
```

```
DATABASE_URL=postgresql://user:pass@localhost/mydb
API_KEY=secret_key_here
LOG_LEVEL=info
PORT=3000
```

The format is simple: one `KEY=value` per line, no `export`, no quotes (unless the value itself needs them — and even then, be careful, the rules differ from a shell).

Set strict permissions (sensitive data!):

```bash
sudo chmod 600 /etc/myapp/env
sudo chown appuser:appuser /etc/myapp/env
```

`600` means readable and writable only by the owner — *no one else* on the system can read this file. Combined with making the file owned by the service user, this is the minimal exposure we can manage. systemd reads the file as root before dropping to the service user, so we don't need to give it broader permissions.

**Reference in the unit file:**

```ini
[Unit]
Description=My Application
After=network.target postgresql.service

[Service]
Type=simple
User=appuser
EnvironmentFile=/etc/myapp/env
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/run.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Notice that we have both `After=postgresql.service` (start ordering) but no `Requires=postgresql.service` here — meaning the app will try to start whether or not postgres is running. For a real production app we'd usually add `Requires=` too, so a postgres failure prevents the app from starting (and from logging confusing connection errors).

### Example 3: Running a Script at Shutdown
To run a cleanup script when the system shuts down — useful for things like flushing caches, deregistering from a load balancer, or saving state:

```ini
[Unit]
Description=Cleanup on shutdown
DefaultDependencies=no
Before=shutdown.target reboot.target halt.target

[Service]
Type=oneshot
ExecStart=/opt/scripts/cleanup.sh
TimeoutStartSec=30

[Install]
WantedBy=halt.target reboot.target shutdown.target
```

Several unusual things here:
- `DefaultDependencies=no` opts out of the default ordering rules. Without it, systemd would try to start this *after* basic system services, which is exactly wrong for a shutdown script.
- `Before=shutdown.target ...` ensures the cleanup runs *before* the shutdown sequence completes.
- `Type=oneshot` because the script does its job and exits — there's no daemon to keep alive.
- `TimeoutStartSec=30` caps how long systemd will wait for the script. If our cleanup hangs forever, we don't want to block the shutdown indefinitely.
- `WantedBy=halt.target reboot.target shutdown.target` enables it for any kind of shutdown.

---

## systemd Timers — The Modern Cron
**systemd timers** are an alternative to cron for scheduling tasks. They integrate with the journal for logging, support sophisticated scheduling, and can be managed with `systemctl`. Compared to cron, timers offer a few real advantages:
- **Better logging** — output goes to the journal, viewable with `journalctl`. Cron silently emails output to `root` (which usually goes nowhere on modern systems).
- **Catch-up runs** — `Persistent=true` will run a missed job when the system comes back up.
- **Dependencies and ordering** — timers can `Requires=` other services and respect boot ordering.
- **Same management interface** — start/stop/enable/status work the same as for any other service.

Cron is still simpler for one-line scheduled jobs, but for anything beyond a single line, timers are usually worth the extra setup.

A timer requires two unit files:
1. A `.service` file describing what to run
2. A `.timer` file describing when to run it

This separation feels like extra work at first, but it pays off: the same service can be triggered by a timer, manually with `systemctl start`, by another service, or by a socket — all without changing the service definition.

### Creating a Timer
**Step 1: Create the service unit (what to run)**

```bash
sudo nano /etc/systemd/system/backup.service
```

```ini
[Unit]
Description=Daily Backup Job

[Service]
Type=oneshot
User=backup
ExecStart=/opt/scripts/backup.sh
StandardOutput=journal
StandardError=journal
```

Note: No `[Install]` section — the timer activates this service, not `systemctl enable`. This is a common pattern: the service is "passive," waiting to be triggered by something else. `Type=oneshot` is correct here because backup scripts run, finish, and exit.

**Step 2: Create the timer unit (when to run it)**

```bash
sudo nano /etc/systemd/system/backup.timer
```

```ini
[Unit]
Description=Run daily backup at 2 AM

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 02:00:00    # Specific time overrides "daily"
Persistent=true               # Run immediately if we missed the last run

[Install]
WantedBy=timers.target
```

Important convention: a timer named `backup.timer` automatically activates the service named `backup.service` — they need matching base names. (We can override this with a `Unit=` directive, but matching names is the standard.)

`Persistent=true` is one of the killer features over cron. With cron, if our laptop is asleep at 2 AM when the backup is supposed to run, the backup is just *missed* — it won't run again until tomorrow at 2 AM. With `Persistent=true`, systemd remembers the last successful run and triggers the missed job as soon as the system is available again. For laptop or sporadically-online machines, this is essential.

**Step 3: Enable and start the timer** (not the service!)

```bash
sudo systemctl daemon-reload
sudo systemctl enable backup.timer
sudo systemctl start backup.timer
```

We enable and start the *timer*, not the service. The timer's job is to start the service at the right moment. If we accidentally enabled the service, it would just run once at every boot — not what we want.

**Step 4: Verify**

```bash
systemctl list-timers
```

Shows all timers with their next and last execution times — incredibly useful for sanity-checking our schedule. The output includes columns for "NEXT" (when it'll run next), "LAST" (when it last ran), and "ACTIVATES" (which service it triggers).

#### Timer Schedule Examples

```ini
OnCalendar=daily             # Every day at midnight
OnCalendar=weekly            # Every Monday at midnight
OnCalendar=monthly           # First of each month at midnight
OnCalendar=hourly            # Every hour
OnCalendar=*-*-* 02:30:00   # Every day at 2:30 AM
OnCalendar=Mon-Fri *-*-* 09:00:00  # Weekdays at 9 AM
OnCalendar=*:0/15            # Every 15 minutes
```

The `OnCalendar=` syntax follows the format `DayOfWeek YYYY-MM-DD HH:MM:SS`, where each field accepts wildcards (`*`), ranges (`Mon-Fri`), comma-separated lists (`Mon,Wed,Fri`), and step values (`0/15` meaning "starting at 0, every 15 units"). To validate a timer expression before deploying, we can use `systemd-analyze calendar "Mon-Fri *-*-* 09:00:00"` — it'll tell us when the next match would occur, or report a syntax error.

#### Relative timers (after system boot or unit activation)

```ini
OnBootSec=5min       # 5 minutes after boot
OnUnitActiveSec=1h   # Every hour after the timer last activated
```

These are more useful than they look. `OnBootSec` is great for delaying jobs that shouldn't run during the boot rush. `OnUnitActiveSec` creates a "run every X after the last run" pattern that's more natural for periodic maintenance than absolute calendar times. We can combine them: `OnBootSec=10min` plus `OnUnitActiveSec=1h` means "first run 10 minutes after boot, then every hour."

---

## Managing Custom Services
After creating services, we manage them with the same `systemctl` commands we'd use for any system service:

```bash
# Control
sudo systemctl start mywebapp
sudo systemctl stop mywebapp
sudo systemctl restart mywebapp
sudo systemctl reload mywebapp      # Send SIGHUP (if supported)

# Enable/disable at boot
sudo systemctl enable mywebapp
sudo systemctl disable mywebapp

# Status and logs
sudo systemctl status mywebapp
journalctl -u mywebapp
journalctl -u mywebapp -f           # Follow live
journalctl -u mywebapp --since "1 hour ago"

# After editing the unit file, always reload first
sudo systemctl daemon-reload
sudo systemctl restart mywebapp
```

A few things worth highlighting from this list. `restart` is `stop` followed by `start` — a brief downtime. `reload` is gentler: it sends a signal (defined by `ExecReload=`) telling the running process to re-read config without restarting, which is great for tweaking nginx or postgres without dropping connections. `journalctl --since "1 hour ago"` accepts surprisingly natural date expressions: "yesterday", "2024-01-01", "30 minutes ago" all work. And the *daemon-reload then restart* pattern at the bottom is the typical edit-test cycle when iterating on a unit file.