# Shell Customization — Making the Terminal Our Own

A default Bash shell works, but a customized shell works *for us*. After a few hours of setup, our terminal becomes faster, more informative, and genuinely enjoyable to use. This guide covers the configuration files that control our shell, how to create aliases and functions, how to customize the prompt, and how to set up a productive daily workflow.

---

## Shell Configuration Files
When Bash starts, it reads configuration files to set up the environment. Understanding which file is read when prevents the common frustration of "why isn't my change taking effect?"

#### ~/.bashrc — Interactive non-login shells
Loaded every time we open a new terminal window or tab. This is where most of our customizations belong:
- Aliases
- Functions
- Custom prompt (PS1)
- Environment variables for interactive use

#### ~/.bash_profile — Login shells
Loaded once when we log in (SSH sessions, the first terminal at system startup). On Ubuntu, this file typically sources `~/.bashrc` so both are applied.

#### ~/.profile — POSIX-compatible login configuration
Used when `~/.bash_profile` doesn't exist. Works with multiple shells (not just Bash).

#### ~/.bash_aliases — Dedicated aliases file (optional but clean)
Ubuntu's default `~/.bashrc` includes these lines that load a separate aliases file if it exists:

```bash
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
```

Keeping aliases in a separate `~/.bash_aliases` file keeps `~/.bashrc` clean. We can do the same.

#### ~/.bash_logout — Run on logout
Executed when a login shell exits. Useful for cleanup tasks (clearing the screen, logging, etc.).

### Applying Changes
After editing any of these files, the changes apply to **new** shell sessions. To apply them to the current session:

```bash
source ~/.bashrc
# or equivalently:
. ~/.bashrc
```

---

## Aliases — Shorter Commands for What We Type Most
An **alias** replaces a long command with a short one. The syntax is:

```bash
alias shortname='full command here'
```

### Creating Aliases
Open `~/.bashrc` (or `~/.bash_aliases`):

```bash
nano ~/.bashrc
```

Add aliases at the end. Here are essential ones to start with:

```bash
# --- Navigation ---
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias ~='cd ~'

# --- ls improvements ---
alias ls='ls --color=auto'
alias ll='ls -lah'          # Long list, all files, human-readable sizes
alias la='ls -A'            # All files except . and ..
alias l='ls -CF'

# --- Safety nets ---
alias rm='rm -i'            # Always ask before deleting
alias cp='cp -i'            # Always ask before overwriting
alias mv='mv -i'            # Always ask before overwriting

# --- grep with color ---
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# --- System shortcuts ---
alias update='sudo apt update && sudo apt upgrade'
alias install='sudo apt install'
alias ports='ss -tuln'
alias myip='hostname -I'
alias diskspace='df -h'
alias meminfo='free -h'

# --- Git shortcuts ---
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline --graph'

# --- Python virtual environments ---
alias venv='python3 -m venv .venv && source .venv/bin/activate'
alias activate='source .venv/bin/activate'
```

Apply the changes:

```bash
source ~/.bashrc
```

### Viewing and Removing Aliases
To see all active aliases:

```bash
alias
```

To see a specific alias:

```bash
alias ll
```

To temporarily remove an alias for the current session:

```bash
unalias ll
```

### Bypassing an Alias
Sometimes we want the original command, not our alias. Prefix with `\`:

```bash
\rm file.txt    # Runs original rm without -i prompt
```

Or use the full path:

```bash
/bin/rm file.txt
```

---

## Functions — Aliases with Arguments
Aliases can't take arguments. When we need something more flexible, we write a **function**. Functions go in `~/.bashrc` (or a separate `~/.bash_functions` file).

```bash
# Create a directory and immediately cd into it
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Extract any archive with a single command
extract() {
    if [ -f "$1" ]; then
        case "$1" in
            *.tar.bz2)  tar -xjf "$1"  ;;
            *.tar.gz)   tar -xzf "$1"  ;;
            *.tar.xz)   tar -xJf "$1"  ;;
            *.bz2)      bunzip2 "$1"   ;;
            *.gz)       gunzip "$1"    ;;
            *.zip)      unzip "$1"     ;;
            *.7z)       7z x "$1"      ;;
            *)          echo "Unknown archive format: $1" ;;
        esac
    else
        echo "'$1' is not a file"
    fi
}

# Quick backup of a file (adds .bak extension)
bak() {
    cp "$1" "${1}.bak" && echo "Backed up: ${1}.bak"
}

# Search process list
psg() {
    ps aux | grep -i "$1" | grep -v grep
}

# Find a file by name in the current directory tree
ff() {
    find . -name "*$1*" 2>/dev/null
}

# Go up N directories: "up 3" goes up 3 levels
up() {
    local d=""
    for (( i=0; i<${1:-1}; i++ )); do
        d="../$d"
    done
    cd "$d"
}
```

Usage:

```bash
mkcd new_project         # Creates and enters new_project/
extract archive.tar.gz   # Extracts any archive
bak important.conf       # Creates important.conf.bak
psg nginx                # Find nginx processes
ff config                # Find files containing "config" in name
up 3                     # Go up 3 directories
```

---

## Customizing the Prompt (PS1)
The **PS1** variable controls what our shell prompt looks like. A well-designed prompt shows us exactly what we need to know at a glance: current directory, git branch, user, hostname.

### Understanding the Default Prompt
The default Ubuntu PS1 looks like:

```
\u@\h:\w\$
```

Which renders as: `alice@hostname:~$`

Common escape sequences:

| Escape | Meaning |
|--------|---------|
| `\u` | Current username |
| `\h` | Hostname (up to first `.`) |
| `\H` | Full hostname |
| `\w` | Current directory (full path) |
| `\W` | Current directory (basename only) |
| `\$` | `$` for regular user, `#` for root |
| `\n` | Newline |
| `\t` | Current time (HH:MM:SS) |
| `\d` | Current date |

### Adding Color to the Prompt
Colors use ANSI escape codes wrapped in `\[...\]` (the brackets tell Bash the enclosed characters have zero display width):

```bash
# Color codes
RED='\[\033[0;31m\]'
GREEN='\[\033[0;32m\]'
YELLOW='\[\033[0;33m\]'
BLUE='\[\033[0;34m\]'
CYAN='\[\033[0;36m\]'
WHITE='\[\033[0;37m\]'
BOLD='\[\033[1m\]'
RESET='\[\033[0m\]'     # Reset all colors

# A colorful prompt: green user@host, blue directory, white $
PS1="${GREEN}\u@\h${RESET}:${BLUE}\w${RESET}\$ "
```

Add this to `~/.bashrc` and `source ~/.bashrc` to see it.

### Showing the Git Branch in the Prompt
This is one of the most useful prompt customizations for developers:

```bash
# Function to get current git branch
git_branch() {
    local branch
    branch=$(git symbolic-ref --short HEAD 2>/dev/null) && echo " ($branch)"
}

# Prompt with git branch
GREEN='\[\033[0;32m\]'
YELLOW='\[\033[0;33m\]'
BLUE='\[\033[0;34m\]'
CYAN='\[\033[0;36m\]'
RESET='\[\033[0m\]'

PS1="${GREEN}\u@\h${RESET}:${BLUE}\w${CYAN}\$(git_branch)${RESET}\$ "
```

This renders as: `alice@hostname:~/projects/webapp (main)$`

The `\$(git_branch)` runs the function every time the prompt is displayed (the backslash prevents early evaluation).

### A Two-Line Prompt
For long paths, a two-line prompt gives more room to type:

```bash
PS1="${GREEN}\u@\h${RESET}:${BLUE}\w${CYAN}\$(git_branch)${RESET}\n\$ "
```

The `\n` creates a new line, so the `$` prompt is always at the start of a fresh line regardless of how long the path is.

---

## Environment Variables
Environment variables configure both our shell session and programs we run. We covered the basics in `05-users-and-groups.md` — here we go deeper.

### Setting a Persistent Variable
To make a variable available in every new terminal session, add it to `~/.bashrc`:

```bash
# API keys and tokens (keep sensitive values here, not in code)
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
export AWS_REGION="us-east-1"

# Application settings
export EDITOR="nano"         # Default editor for git, cron, etc.
export PAGER="less"          # Default pager
export HISTSIZE=10000        # Remember 10000 commands in history
export HISTFILESIZE=20000    # Store 20000 commands in history file
export HISTCONTROL=ignoredups:erasedups  # Don't store duplicate commands
```

### Extending the PATH
To add a directory to PATH so executables there are found automatically:

```bash
# Add local bin directory to PATH
export PATH="$HOME/.local/bin:$PATH"

# Add custom scripts directory
export PATH="$PATH:$HOME/scripts"

# Add Go binaries (example)
export PATH="$PATH:/usr/local/go/bin"
```

Always include `$PATH` to preserve the existing directories — never replace it entirely.

### Useful History Settings

```bash
# Append to history file instead of overwriting
shopt -s histappend

# Save multi-line commands as single entry
shopt -s cmdhist

# Ignore commands starting with space (useful for sensitive commands)
HISTCONTROL=ignorespace

# Record timestamp with each history entry
HISTTIMEFORMAT="%F %T "
```

With `HISTCONTROL=ignorespace`, any command we prefix with a space won't be saved to history — useful when typing passwords or sensitive API calls we don't want stored.

---

## Useful Shell Options (shopt)
`shopt` (shell options) enables or disables various Bash behaviors:

```bash
# Correct minor typos in cd commands (e.g., "cd Documens" → "cd Documents")
shopt -s cdspell

# Include hidden files in glob patterns
shopt -s dotglob

# Case-insensitive globbing
shopt -s nocaseglob

# Resize terminal output when window size changes
shopt -s checkwinsize
```

Add these to `~/.bashrc`.

---

## A Complete ~/.bashrc Template
Here's a well-organized starting `~/.bashrc` we can adapt:

```bash
# ~/.bashrc — Bash configuration for interactive shells

# ── Environment ──────────────────────────────────────────────
export EDITOR="nano"
export PAGER="less"
export HISTSIZE=10000
export HISTFILESIZE=20000
export HISTCONTROL=ignoredups:erasedups
export PATH="$HOME/.local/bin:$PATH"

# ── Shell Options ─────────────────────────────────────────────
shopt -s histappend
shopt -s checkwinsize
shopt -s cdspell

# ── Prompt ────────────────────────────────────────────────────
git_branch() {
    git symbolic-ref --short HEAD 2>/dev/null | sed 's/.*/ (&)/'
}

GREEN='\[\033[0;32m\]'
BLUE='\[\033[0;34m\]'
CYAN='\[\033[0;36m\]'
RESET='\[\033[0m\]'
PS1="${GREEN}\u@\h${RESET}:${BLUE}\w${CYAN}\$(git_branch)${RESET}\$ "

# ── Aliases ───────────────────────────────────────────────────
alias ls='ls --color=auto'
alias ll='ls -lah'
alias la='ls -A'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias update='sudo apt update && sudo apt upgrade'
alias ports='ss -tuln'
alias myip='hostname -I'

# ── Functions ─────────────────────────────────────────────────
mkcd() { mkdir -p "$1" && cd "$1"; }

extract() {
    [ -f "$1" ] || { echo "'$1' is not a file"; return 1; }
    case "$1" in
        *.tar.gz)  tar -xzf "$1" ;;
        *.tar.bz2) tar -xjf "$1" ;;
        *.zip)     unzip "$1"    ;;
        *.gz)      gunzip "$1"   ;;
        *)         echo "Unknown format: $1" ;;
    esac
}

ff() { find . -name "*$1*" 2>/dev/null; }
psg() { ps aux | grep -i "$1" | grep -v grep; }
```