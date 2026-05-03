# tmux — The Terminal Multiplexer

One of the most common frustrations when working on remote servers is losing work when the connection drops. We SSH into a server, start a long-running process, the network hiccups — and it's all gone. **tmux** solves this permanently.

**tmux** (terminal multiplexer) is a program that lets us:
- Run multiple terminal sessions inside a single window
- Keep sessions alive even after we disconnect from SSH
- Split our terminal into multiple panes (side by side or stacked)
- Switch between multiple projects in separate windows
- Share a terminal session with another user

Once we start using tmux, going back to a plain terminal feels limiting. It's one of the tools that professional Linux users run constantly.

---

## Installing tmux
On Ubuntu/Debian:

```bash
sudo apt install tmux
```

To verify the installation:

```bash
tmux -V
```

---

## The Core Concept: Sessions, Windows, and Panes
tmux has a three-level hierarchy:

```
Session
└── Window 1 (like a browser tab)
    ├── Pane 1 (left half)
    └── Pane 2 (right half)
└── Window 2
    └── Pane 1 (full screen)
```

- **Session** — a collection of windows, persists after detaching (even through SSH disconnects)
- **Window** — a full-screen terminal (like a tab in a browser)
- **Pane** — a subdivision of a window (split horizontally or vertically)

---

## The Prefix Key
Almost every tmux command starts with a **prefix key** — a special key combination that tells tmux "the next key is a tmux command, not regular terminal input."

The default prefix is `Ctrl+B`. So to split a window horizontally, we press:
1. `Ctrl+B` — activate tmux command mode
2. `"` — the command for horizontal split

Throughout this guide, we write this as `Ctrl+B "`.

---

## Starting and Managing Sessions

#### Starting a new session
Simply launch tmux with no arguments for a fresh unnamed session:

```bash
tmux
```

To start a named session (recommended — names help us remember what each session is for):

```bash
tmux new -s work
tmux new -s myproject
```

#### Detaching from a session — the killer feature
To detach (leave tmux running in the background while returning to our normal terminal):

```
Ctrl+B d
```

The session keeps running. All our processes inside it continue. We can close the terminal entirely, disconnect from SSH, even turn off our laptop — the tmux session waits for us on the server.

#### Listing running sessions

```bash
tmux ls
```

Output:

```
work: 3 windows (created Mon Apr  1 10:30:00 2024)
logs: 1 windows (created Mon Apr  1 09:15:00 2024)
```

#### Reattaching to a session
To reconnect to a detached session by name:

```bash
tmux attach -t work
```

Shorthand:

```bash
tmux a -t work
```

If we only have one session, just:

```bash
tmux attach
```

This is the fundamental workflow: `tmux new -s work` → do our work → `Ctrl+B d` to detach → `tmux a -t work` to come back.

#### Renaming a session
From inside tmux:

```
Ctrl+B $
```

This prompts us to enter a new name for the current session.

#### Killing a session
To kill a specific session from outside tmux:

```bash
tmux kill-session -t work
```

To kill all sessions:

```bash
tmux kill-server
```

---

## Windows — Multiple Terminals in One Session
Windows are like browser tabs inside a tmux session.

#### Creating a new window

```
Ctrl+B c
```

A new empty terminal opens. The status bar at the bottom shows our windows:

```
[work] 0:bash  1:bash* 2:bash
                      ↑ asterisk marks the current window
```

#### Switching between windows

```
Ctrl+B 0    # Switch to window 0
Ctrl+B 1    # Switch to window 1
Ctrl+B 2    # Switch to window 2
```

Navigate to the next/previous window:

```
Ctrl+B n    # Next window
Ctrl+B p    # Previous window
```

#### Renaming a window

```
Ctrl+B ,
```

Enter a descriptive name (e.g., "server", "logs", "editor"). Named windows make it much easier to find what we need.

#### Closing a window
Simply exit the shell inside it:

```bash
exit
```

Or force close:

```
Ctrl+B &
```

---

## Panes — Split Screen
Panes let us split a window into multiple terminals visible at the same time. This is invaluable for watching logs while editing code, or comparing two files side by side.

#### Splitting vertically (left and right)

```
Ctrl+B %
```

#### Splitting horizontally (top and bottom)

```
Ctrl+B "
```

#### Moving between panes

```
Ctrl+B ←    # Move to the pane on the left
Ctrl+B →    # Move to the pane on the right
Ctrl+B ↑    # Move to the pane above
Ctrl+B ↓    # Move to the pane below
```

Or cycle through panes with:

```
Ctrl+B o    # Move to the next pane
```

#### Resizing panes
Hold `Ctrl+B` and then keep pressing an arrow key to resize:

```
Ctrl+B Ctrl+←    # Make current pane wider (keep holding Ctrl)
Ctrl+B Ctrl+→
Ctrl+B Ctrl+↑
Ctrl+B Ctrl+↓
```

Or use `Ctrl+B Alt+←/→/↑/↓` for larger resize steps.

#### Zoom — maximize a pane temporarily

```
Ctrl+B z
```

This makes the current pane fill the entire window. Press `Ctrl+B z` again to restore the split view. Very useful when we need to focus on one pane but want to return to the split layout.

#### Closing a pane
Type `exit` or press `Ctrl+D`. If it's the last pane in a window, the window closes too.

---

## Copy Mode — Scrolling and Copying Text
By default, we can't scroll up in tmux with the mouse or Page Up key — those are captured by the application inside the pane. **Copy mode** lets us scroll and copy text.

#### Entering copy mode

```
Ctrl+B [
```

Now we can:
- Scroll up/down with arrow keys or `Page Up`/`Page Down`
- Navigate with vim-style keys (`h j k l`, `Ctrl+F/B`)
- Search with `/` (forward) or `?` (backward)

#### Selecting and copying text
While in copy mode:
1. Move to the start of the text we want
2. Press `Space` to start selection
3. Move to the end
4. Press `Enter` to copy and exit copy mode

#### Pasting

```
Ctrl+B ]
```

#### Exiting copy mode without copying

```
q
```

---

## Practical Workflows

#### Workflow 1: Long-running server task on remote machine
```bash
# SSH to server
ssh alice@myserver

# Create a named session
tmux new -s deployment

# Start the deployment script
./deploy.sh

# Detach (the deployment keeps running!)
# Ctrl+B d

# Log out of SSH
exit

# ... hours later, reconnect ...
ssh alice@myserver
tmux a -t deployment
```

#### Workflow 2: Multi-pane development setup
```bash
# Start a session for a project
tmux new -s webapp

# Rename window 0 to "editor"
# Ctrl+B ,  → type "editor"

# Split vertically: code on left, terminal on right
# Ctrl+B %

# In the right pane, create a second horizontal split for logs
# Ctrl+B "

# We now have: editor | terminal above / logs below
# Run our editor in the left pane, app server in top-right, logs in bottom-right
```

#### Workflow 3: Watching logs while working
```bash
# Split horizontally
# Ctrl+B "

# In the bottom pane, follow logs
tail -f /var/log/nginx/access.log

# Switch to top pane and do our work
# Ctrl+B ↑
```

---

## Quick Reference — Key Bindings

### Sessions

| Key | Action |
|-----|--------|
| `Ctrl+B d` | Detach from session |
| `Ctrl+B $` | Rename current session |
| `Ctrl+B s` | Show session list (interactive) |

### Windows

| Key | Action |
|-----|--------|
| `Ctrl+B c` | Create new window |
| `Ctrl+B ,` | Rename current window |
| `Ctrl+B n` | Next window |
| `Ctrl+B p` | Previous window |
| `Ctrl+B 0–9` | Switch to window by number |
| `Ctrl+B &` | Kill current window |
| `Ctrl+B w` | Interactive window list |

### Panes

| Key | Action |
|-----|--------|
| `Ctrl+B %` | Split vertically |
| `Ctrl+B "` | Split horizontally |
| `Ctrl+B ←→↑↓` | Navigate panes |
| `Ctrl+B o` | Cycle to next pane |
| `Ctrl+B z` | Zoom/unzoom pane |
| `Ctrl+B x` | Kill current pane |
| `Ctrl+B {` | Swap pane with previous |
| `Ctrl+B }` | Swap pane with next |

### Copy Mode

| Key | Action |
|-----|--------|
| `Ctrl+B [` | Enter copy mode |
| `Space` | Start selection |
| `Enter` | Copy and exit |
| `Ctrl+B ]` | Paste |
| `q` | Exit copy mode |

### Miscellaneous

| Key | Action |
|-----|--------|
| `Ctrl+B ?` | Show all key bindings |
| `Ctrl+B :` | Enter tmux command prompt |
| `Ctrl+B t` | Show clock |

---

## Customizing tmux (~/.tmux.conf)
tmux is highly configurable. We create `~/.tmux.conf` to customize it:

```bash
nano ~/.tmux.conf
```

A practical starter configuration:

```bash
# Change prefix from Ctrl+B to Ctrl+A (easier to type)
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# Enable mouse support (click to select panes/windows, scroll)
set -g mouse on

# Start window numbering from 1 (instead of 0)
set -g base-index 1
setw -g pane-base-index 1

# Increase scrollback buffer
set -g history-limit 10000

# Enable 256 colors
set -g default-terminal "screen-256color"

# Split panes with | and - (more intuitive than % and ")
bind | split-window -h
bind - split-window -v

# Reload config with Ctrl+A r
bind r source-file ~/.tmux.conf \; display "Config reloaded!"
```

To reload the config from inside tmux:

```
Ctrl+B :source-file ~/.tmux.conf
```

Or if we added the `bind r` shortcut above: `Ctrl+A r`.

---

## screen — The Older Alternative
**screen** is an older terminal multiplexer that predates tmux but is available on almost every Linux system (even minimal ones):

```bash
sudo apt install screen
```

Basic screen usage:

```bash
screen              # Start a new session
screen -S work      # Start named session
# Ctrl+A d          # Detach (note: Ctrl+A, not Ctrl+B)
screen -ls          # List sessions
screen -r work      # Reattach
```

Inside screen:
- `Ctrl+A c` — create new window
- `Ctrl+A n` / `Ctrl+A p` — next/previous window
- `Ctrl+A |` — split vertically
- `Ctrl+A S` — split horizontally
- `Ctrl+A Tab` — switch between panes

tmux is generally preferred for new setups, but knowing screen means we can work on any server even if tmux isn't installed.