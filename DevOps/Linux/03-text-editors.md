# Editing Files in the Terminal — nano and vim

One of the first things that surprises new Linux users is the need to edit files directly in the terminal. On Windows, we'd just double-click a file and it opens in Notepad or VS Code. On a remote Linux server, there's no desktop to double-click on — we need to edit configuration files, scripts, and code entirely from the command line.

This guide covers two terminal text editors: **nano** (beginner-friendly and approachable) and **vim** (powerful, efficient, and ubiquitous). We'll learn nano first because it's easier, then explore vim because knowing it will serve us for life — it's available on virtually every Linux/Unix system, including Docker containers, embedded systems, and cloud servers where nothing else is installed.

---

## Why Terminal Editors Matter
Before we dive in, let's understand why this skill is important:

- **Remote servers** have no graphical interface. When we SSH into a cloud server to change a configuration file, a terminal editor is our only option.
- **Speed** — experienced Linux users make quick edits to files in seconds without ever leaving the terminal.
- **Availability** — vim (or its predecessor vi) is installed on essentially every Unix-like system on the planet. Docker containers, Kubernetes pods, minimal VMs — vim is always there.
- **Automation** — terminal editors work over SSH, in scripts, and in automated workflows.

For everyday development on our local machine or WSL, we can absolutely use VS Code or any GUI editor. But the moment we work with remote systems or containers, terminal editing skills become essential.

---

## nano — The Beginner-Friendly Editor
**nano** is a simple, straightforward terminal editor with a helpful hint bar at the bottom showing available commands. It works like a basic text editor with a few keyboard shortcuts.

### Opening a File with nano
To open a file for editing:

```bash
nano notes.txt
```

If the file doesn't exist, nano will create it when we save. The interface looks like this:

```
  GNU nano 6.2               notes.txt

Hello, this is my first file in Linux.
I can type freely here.

                                              [ New File ]
^G Help      ^O Write Out  ^W Where Is   ^K Cut       ^T Execute
^X Exit      ^R Read File  ^\ Replace    ^U Paste     ^J Justify
```

The bottom two lines show available commands. The `^` symbol means `Ctrl`. So `^X` means `Ctrl+X`.

### Basic nano Operations

#### Typing and editing
Once nano is open, we can simply type. There's no special mode — we're always in editing mode.

#### Saving a file
When we're done editing and want to save, we press `Ctrl+O` (Write Out):

```
^O (Ctrl+O)
```

nano will ask us to confirm the filename. Press `Enter` to save with the same name, or type a new name.

#### Exiting nano
To close nano, press `Ctrl+X`:

```
^X (Ctrl+X)
```

If we have unsaved changes, nano will ask: "Save modified buffer?" Press `Y` for yes, `N` for no, or `Ctrl+C` to cancel and go back to editing.

The most common workflow is: make changes → `Ctrl+O` to save → `Ctrl+X` to exit.

#### Searching for text
To search within a file, press `Ctrl+W` (Where Is):

```
^W (Ctrl+W)
```

Type the search term and press `Enter`. nano highlights the first match and moves the cursor there. Press `Ctrl+W` then `Enter` again to find the next match.

#### Cutting and pasting lines
To cut (delete) the current line:

```
^K (Ctrl+K)
```

The line is removed and stored in a clipboard. To paste it elsewhere, move the cursor to the desired location and press:

```
^U (Ctrl+U)
```

We can cut multiple consecutive lines by pressing `Ctrl+K` multiple times before pasting.

#### Navigating
We can use the arrow keys to move around. For larger files:
- `Ctrl+Y` — scroll up one page
- `Ctrl+V` — scroll down one page
- `Ctrl+_` — go to a specific line number (enter the line number when prompted)

### Practical Example: Editing a Configuration File
Let's try a real-world example. We'll edit the `/etc/hosts` file to add a custom hostname mapping. (In WSL this requires sudo):

```bash
sudo nano /etc/hosts
```

We'll see existing entries like:

```
127.0.0.1    localhost
::1          localhost
```

We can add our own entry at the bottom, then save with `Ctrl+O` and exit with `Ctrl+X`.

### nano Summary Table

| Action | Shortcut |
|--------|----------|
| Save file | `Ctrl+O` then `Enter` |
| Exit | `Ctrl+X` |
| Search | `Ctrl+W` |
| Replace | `Ctrl+\` |
| Cut line | `Ctrl+K` |
| Paste | `Ctrl+U` |
| Go to line | `Ctrl+_` |
| Page up | `Ctrl+Y` |
| Page down | `Ctrl+V` |
| Show cursor position | `Ctrl+C` |

---

## vim — The Powerful Editor
**vim** (Vi IMproved) is the most widely used terminal text editor in the professional Linux world. It's available on every Linux/Unix system and is the default editor on many servers. Learning vim feels strange at first — nothing works the way we expect — but that's because vim uses a **modal** approach that makes editing extremely fast once mastered.

Vim is famous for being hard to quit. The first time most people open vim, they don't know how to exit. Let's fix that right now:

**To quit vim without saving: press `Esc`, then type `:q!` and press `Enter`.**

Now let's learn the rest.

### The Modal Concept
The core idea of vim that makes it different from every other editor is **modes**. In vim, the same keys do different things depending on which mode we're in.

- **Normal mode** — The default mode. Keys are commands (navigation, deletion, copying). We are NOT typing text.
- **Insert mode** — We can type text like a normal editor.
- **Visual mode** — We can select text.
- **Command mode** — We type commands (save, quit, search-and-replace).

We start in Normal mode. We must switch to Insert mode to type. We return to Normal mode with `Esc`.

This feels weird at first, but there's a reason: in Normal mode, every key is a command. `w` jumps forward a word, `d` deletes, `y` copies, `p` pastes. We can navigate and edit files with zero mouse clicks, moving at the speed of thought.

### Opening a File with vim

```bash
vim notes.txt
```

The file opens in **Normal mode**. We'll see the file contents (or tildes `~` for empty lines if it's a new file).

### Switching Between Modes

#### Entering Insert mode (to type text)
From Normal mode, press `i` to enter Insert mode at the current cursor position. We'll see `-- INSERT --` at the bottom of the screen.

```
i    — insert before the cursor
a    — append after the cursor
I    — insert at the beginning of the current line
A    — append at the end of the current line
o    — open a new line below and enter Insert mode
O    — open a new line above and enter Insert mode
```

#### Returning to Normal mode
Press `Esc` at any time to return to Normal mode. This is the most important key to remember.

### Saving and Quitting
These are typed in Normal mode after pressing `:` (colon), which enters Command mode:

```bash
:w          # Save the file (write)
:q          # Quit (only works if no unsaved changes)
:wq         # Save and quit
:q!         # Quit without saving (force quit — discards changes)
:w filename # Save as a new filename
```

The `:wq` combination is the standard way to save and exit vim. We'll use it constantly.

### Navigation in Normal Mode
In Normal mode, we navigate with the keyboard. We can use arrow keys, but the traditional vim keys are faster once learned because our fingers never leave the home row:

| Key | Movement |
|-----|----------|
| `h` | Move left |
| `j` | Move down |
| `k` | Move up |
| `l` | Move right |
| `w` | Jump forward one **word** |
| `b` | Jump **backward** one word |
| `e` | Jump to the **end** of the current word |
| `0` | Jump to the **beginning** of the line |
| `$` | Jump to the **end** of the line |
| `gg` | Jump to the **first** line of the file |
| `G` | Jump to the **last** line of the file |
| `:<n>` | Jump to line number n (e.g., `:42` goes to line 42) |
| `Ctrl+F` | Scroll down (Forward) one page |
| `Ctrl+B` | Scroll up (Backward) one page |

Numbers can be combined with movements: `5j` moves down 5 lines, `3w` jumps forward 3 words.

### Editing in Normal Mode
In Normal mode, these keys perform editing operations without entering Insert mode:

| Key | Action |
|-----|--------|
| `x` | Delete the character under the cursor |
| `dd` | Delete (cut) the current line |
| `5dd` | Delete 5 lines starting from the current line |
| `D` | Delete from cursor to end of line |
| `yy` | Yank (copy) the current line |
| `5yy` | Yank 5 lines |
| `p` | Paste after the cursor |
| `P` | Paste before the cursor |
| `u` | Undo the last action |
| `Ctrl+R` | Redo (undo the undo) |
| `r<char>` | Replace the character under cursor with `<char>` |
| `.` | Repeat the last command (extremely powerful!) |

`dd` followed by `p` in a new location is how we cut and paste a line. `yy` followed by `p` is copy-paste.

### Searching in vim
To search forward through the file, press `/` followed by the pattern:

```
/pattern
```

Then press `Enter`. vim highlights all matches and jumps to the first one.

- Press `n` to jump to the **next** match
- Press `N` to jump to the **previous** match

To search backward, use `?` instead of `/`:

```
?pattern
```

To clear the search highlighting after we're done:

```bash
:noh
```

### Find and Replace
To replace all occurrences of "old" with "new" in the entire file:

```bash
:%s/old/new/g
```

Breaking this down:
- `%` — apply to the entire file (without this, it only applies to the current line)
- `s` — substitute command
- `/old/` — the pattern to find
- `/new/` — the replacement
- `g` — global (replace all occurrences on each line, not just the first)

To confirm each replacement one by one, add `c` (confirm):

```bash
:%s/old/new/gc
```

To make the search case-insensitive, add `i`:

```bash
:%s/old/new/gi
```

To replace only on lines 5 through 10:

```bash
:5,10s/old/new/g
```

### Visual Mode — Selecting Text
Press `v` in Normal mode to enter Visual mode, then move the cursor to select text. Selected text is highlighted.

Once text is selected:
- `y` — yank (copy) the selection
- `d` — delete the selection
- `>` — indent the selection
- `<` — un-indent the selection

Press `V` (capital V) to select entire lines at a time. Press `Ctrl+V` to select a rectangular block (very useful for editing columns).

### vim Quick-Reference Cheat Sheet

| Category | Key | Action |
|----------|-----|--------|
| **Modes** | `i` | Enter Insert mode |
| | `Esc` | Return to Normal mode |
| | `v` | Enter Visual mode |
| | `:` | Enter Command mode |
| **Save/Quit** | `:w` | Save |
| | `:q` | Quit |
| | `:wq` | Save and quit |
| | `:q!` | Force quit (discard changes) |
| **Navigation** | `gg` | Go to first line |
| | `G` | Go to last line |
| | `0` | Start of line |
| | `$` | End of line |
| | `w` / `b` | Word forward / back |
| **Edit** | `dd` | Delete line |
| | `yy` | Copy line |
| | `p` | Paste |
| | `u` | Undo |
| | `Ctrl+R` | Redo |
| **Search** | `/pattern` | Search forward |
| | `n` / `N` | Next / previous match |
| | `:%s/old/new/g` | Replace all |

### Getting Comfortable with vim
The best way to learn vim is to run the built-in tutorial:

```bash
vimtutor
```

This is an interactive lesson that takes about 30 minutes and covers the most important vim commands through practice. We highly recommend spending that time — it's the best possible investment for learning vim.

---

## Other Editors

#### gedit — GUI text editor
On Ubuntu/Debian with a desktop environment (or with WSLg in WSL2), `gedit` provides a full graphical text editor similar to Notepad++:

```bash
gedit notes.txt
```

#### VS Code in WSL
If we have VS Code installed on Windows, we can open files from WSL and they'll open in VS Code (via the WSL Remote extension). From inside the WSL terminal:

```bash
code notes.txt
code .         # open the current directory as a VS Code project
```

This is a great workflow: use the Linux terminal for commands, but VS Code's familiar interface for editing code. VS Code handles the file system bridging automatically.

---

## Choosing the Right Editor

| Situation | Best Choice |
|-----------|------------|
| Quick edit on local WSL | nano or VS Code |
| Editing on a remote server via SSH | vim (always available) |
| Editing inside a Docker container | vim or vi (use `docker exec -it`) |
| Large code project locally | VS Code |
| Fast power-user editing | vim |

**Our recommendation:** Learn nano for quick edits, then invest time in vim. Even if we mostly use VS Code, knowing vim well means we're never stuck when there's no GUI available.