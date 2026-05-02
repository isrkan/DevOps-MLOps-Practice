# Shell Scripting — Automating Tasks with Bash

One of Linux's greatest strengths is **automation**. Instead of typing the same sequence of commands every day, we can write them once in a script and run it whenever needed — or even schedule it to run automatically. Shell scripting turns us from someone who *uses* Linux into someone who *harnesses* its full power.

This guide covers Bash scripting from the ground up — variables, conditionals, loops, functions, and practical script examples. By the end, we'll be writing scripts that save hours of manual work.

---

## What Is Shell Scripting?
A **shell script** is a text file containing a sequence of Bash commands. When we run the script, the shell executes each command in order, just as if we'd typed them one by one in the terminal.

Why write scripts?
- **Automation** — Run a 20-step deployment process with a single command
- **Consistency** — The same script runs the same way every time, eliminating human error
- **Scheduling** — Scripts can be scheduled with cron to run automatically
- **Repeatability** — Share scripts with teammates so everyone follows the same process
- **Documentation** — A script is self-documenting — it shows exactly what steps were taken

---

## Creating and Running Our First Script

#### Creating a script file
Let's create our first script. By convention, shell scripts end in `.sh`, though this is purely a human-readable convention — Linux doesn't actually care about the file extension. What matters is the content and the file's permissions. Open a text editor and create a file called `hello.sh`:

```bash
nano hello.sh
```

Add this content:

```bash
#!/bin/bash

# This is a comment. Lines starting with # are ignored by bash.
echo "Hello, World!"
echo "Today is: $(date)"
echo "We are logged in as: $(whoami)"
```

Comments are essential — even small scripts benefit from a few lines explaining *why* something is done, not just *what* it does. Future-us will be grateful.

In `nano`, saving and exiting takes two key combinations:
1. **Press `Ctrl+O`** — this is "WriteOut" (nano's term for save). At the bottom of the screen, nano will show `File Name to Write: hello.sh`.
2. **Press `Enter`** to confirm the filename. Nano writes the file to disk and shows something like `[ Wrote 5 lines ]` at the bottom.
3. **Press `Ctrl+X`** to exit nano and return to the shell prompt.

#### The shebang line
The very first line `#!/bin/bash` is called the **shebang** (or hashbang). It tells the operating system which interpreter to use for this script. `#!` followed by `/bin/bash` means "run this file with Bash." When we execute the script directly, the kernel reads this first line and uses the specified program to interpret the rest of the file. Without it, the kernel doesn't know what to do with our text file and may fall back to whatever default shell is configured — which might not be Bash at all.

Common shebangs:
- `#!/bin/bash` — explicit Bash. Simple and direct, but assumes Bash lives at exactly `/bin/bash`.
- `#!/usr/bin/env bash` — finds bash using PATH (more portable, works on different Linux systems)
- `#!/bin/sh` — POSIX shell (more portable but fewer features)

**Always include the shebang line.** Without it, the script might run with a different shell that doesn't support all Bash features.

#### Making a script executable
Before we can run a script by its name, we need to give it the execute permission. Linux distinguishes between files we can *read* and files we can *run*; by default, a newly created text file is readable but not executable, so we have to explicitly grant execute permission:

```bash
chmod +x hello.sh
```

The `+x` adds the execute bit for everyone (owner, group, and others). For more restrictive permissions, we could use `chmod u+x` to give execute access only to the owner.

#### Running the script
There are two ways to run a script:

**Method 1: Execute directly** (requires execute permission):

```bash
./hello.sh
```

The `./` is important — it means "in the current directory." Without it, Linux looks for `hello.sh` in the directories listed in our `PATH` environment variable, not in the current directory. This behavior is a security feature: it prevents accidentally running a malicious `ls` script that someone planted in our current directory when we meant to run the real `ls` command.

**Method 2: Pass to bash explicitly** (doesn't require execute permission):

```bash
bash hello.sh
```

Here we're telling Bash to read and execute the file directly, bypassing the executable-permission check entirely. This is useful for quickly testing a script we just downloaded or for running a script we don't want to mark executable. Note that with this method, the shebang line is technically ignored — the file is executed by *whichever* shell we name (`bash`, `sh`, etc.).

---

## Variables
Variables store data that we can use throughout our script. They make scripts flexible — instead of hardcoding values everywhere, we set them once at the top and reference them throughout, so changes only need to be made in one place.

#### Defining variables
To assign a value to a variable:

```bash
NAME="Alice"
AGE=30
GREETING="Hello"
```

By convention, shell variables are written in `UPPERCASE`, especially when they're constants or environment variables. Lowercase names are also valid and are often used for local variables inside functions.

**Important:** There must be **no spaces** around the `=` sign. `NAME = "Alice"` would cause an error.

#### Using variables
To use a variable's value, prefix its name with `$`:

```bash
echo $NAME
echo "My name is $NAME and I am $AGE years old."
```

Using curly braces `${NAME}` is more explicit and avoids ambiguity, especially when the variable name is adjacent to other text:

```bash
FILE="report"
echo "Creating ${FILE}_backup.txt"  # Correct: creates "report_backup.txt"
echo "Creating $FILE_backup.txt"    # Wrong: looks for variable $FILE_backup
```

Get into the habit of always using `${VAR}` for clarity.

#### Command substitution
We can capture the output of a command into a variable using `$()`. This is incredibly powerful — it lets us build dynamic values based on the current state of the system:

```bash
CURRENT_DATE=$(date +"%Y-%m-%d")
HOSTNAME=$(hostname)
FILE_COUNT=$(ls ~/Documents | wc -l)

echo "Today: $CURRENT_DATE"
echo "Machine: $HOSTNAME"
echo "Documents: $FILE_COUNT files"
```

The `$()` syntax runs the command inside, captures its standard output, and substitutes it in. Trailing newlines are stripped, so the result is clean and ready to use.

The backtick syntax `` `command` `` is an older equivalent, but `$()` is preferred because it's cleaner and can be nested.

#### Special variables
Bash provides built-in variables that contain useful information:

| Variable | Meaning |
|----------|---------|
| `$0` | The name of the script itself |
| `$1`, `$2`, ... | Command-line arguments (first, second, ...) |
| `$@` | All arguments as separate words |
| `$#` | Number of arguments passed |
| `$?` | Exit code of the last command (0=success, non-zero=error) |
| `$$` | PID of the current script/shell |
| `$USER` | Current username |
| `$HOME` | Home directory path |
| `$PWD` | Current working directory |

These special variables are how scripts interact with their environment. `$1`, `$2`, etc. let us pass data into a script when we invoke it. `$?` lets us check whether a command succeeded. `$$` is useful for creating unique temporary filenames (e.g., `/tmp/myscript_$$.tmp`) that won't collide with other instances of the script.

Example using arguments:

```bash
#!/usr/bin/env bash
echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "All arguments: $@"
echo "Number of arguments: $#"
```

Running it: `./args.sh hello world` outputs:

```
Script name: ./args.sh
First argument: hello
Second argument: world
All arguments: hello world
Number of arguments: 2
```

---

## User Input
To interactively ask the user for input during script execution:

```bash
read -p "Enter your name: " USERNAME
echo "Welcome, $USERNAME!"
```

The `-p` flag displays a prompt before waiting for input. The value typed is stored in `USERNAME`. The script pauses on this line until the user presses Enter, making it easy to build interactive tools. Note that `read` is most useful for genuinely interactive scripts — for scripts that run in cron jobs or CI pipelines, command-line arguments (`$1`, `$2`) are preferable since there's no human around to type input.

To read a password without showing characters on screen:

```bash
read -s -p "Enter password: " PASSWORD
echo ""  # New line after the silent input
echo "Password received (not shown for security)"
```

This is the same mechanism `sudo` uses when prompting for our password. The extra `echo ""` is needed because pressing Enter doesn't produce a visible newline in silent mode, so without it, the next output would appear right next to the prompt.

Other useful `read` flags include `-t SECONDS` (timeout if no input given), `-n N` (read only N characters), and `-r` (don't interpret backslashes — almost always what we want).

---

## Arithmetic

Bash can perform integer arithmetic using `$(( ))`. Inside the double parentheses, Bash evaluates the expression mathematically rather than as text — and unusually, we can refer to variables without the `$` prefix:

```bash
A=10
B=3

SUM=$(( A + B ))
DIFF=$(( A - B ))
PRODUCT=$(( A * B ))
QUOTIENT=$(( A / B ))   # Integer division (no decimals)
REMAINDER=$(( A % B ))  # Modulo (remainder)

echo "Sum: $SUM"
echo "Product: $PRODUCT"
echo "Remainder: $REMAINDER"
```

We can also increment a variable:

```bash
COUNT=0
COUNT=$(( COUNT + 1 ))
# or equivalently:
(( COUNT++ ))
```

The `(( ))` form (without the `$`) is used when we want the arithmetic side effect (incrementing) without capturing the result. It's the same syntax used in C-style for loops.

For floating-point arithmetic, we use `bc` (basic calculator), an external command-line calculator that supports arbitrary precision:

```bash
RESULT=$(echo "scale=2; 10 / 3" | bc)
echo "10 / 3 = $RESULT"   # Output: 10 / 3 = 3.33
```

The `scale=2` directive tells `bc` to keep 2 decimal places. We pipe the expression into `bc` because `bc` reads from standard input. For more complex math, `awk` or Python (`python3 -c "print(10/3)"`) are also good options.

---

## Conditionals — Making Decisions
Conditionals let our scripts make decisions based on the data they encounter — checking whether a file exists, whether a variable has a certain value, whether a command succeeded, and so on. This is what turns a linear sequence of commands into actual logic.

#### if / elif / else / fi
The basic conditional structure:

```bash
if [ condition ]; then
    # commands if condition is true
elif [ other_condition ]; then
    # commands if other_condition is true
else
    # commands if no condition was true
fi
```

Notice that the block ends with `fi` — that's `if` spelled backwards, a Bash convention also used for `case`/`esac`. The `then` keyword is required after the condition, and the semicolon `;` is what lets us put `then` on the same line as `if`.

**Important:** Spaces inside the brackets are required. `[ condition ]` works; `[condition]` does not. This is because `[` is actually a *command* (a built-in alias for `test`), not a syntax element — Bash needs whitespace to separate the command from its arguments.

#### Test conditions with [ ] and [[ ]]
The `[[ ]]` double brackets are the modern, preferred way to test conditions. They support more features (regex matching, glob patterns, no word splitting on variables) and are less error-prone than single brackets. The single `[ ]` form is older and POSIX-portable, but it has subtle pitfalls — for example, an unquoted empty variable inside `[ ]` causes a syntax error, while `[[ ]]` handles it gracefully.

**String comparisons:**

```bash
NAME="Alice"

if [[ "$NAME" == "Alice" ]]; then
    echo "Hello Alice!"
fi

if [[ "$NAME" != "Bob" ]]; then
    echo "You are not Bob."
fi

if [[ -z "$NAME" ]]; then
    echo "Name is empty"    # -z = zero length (empty string)
fi

if [[ -n "$NAME" ]]; then
    echo "Name is set"      # -n = non-zero length (not empty)
fi
```

Note that string comparison uses `==` (or `=` in older syntax), unlike numeric comparison which uses `-eq` — Bash distinguishes between the two. The `-z` and `-n` checks are particularly useful for validating that arguments or environment variables are set before using them.

**Numeric comparisons:**

```bash
AGE=25

if [[ $AGE -eq 25 ]]; then echo "Exactly 25"; fi       # equal
if [[ $AGE -ne 30 ]]; then echo "Not 30"; fi            # not equal
if [[ $AGE -lt 30 ]]; then echo "Less than 30"; fi      # less than
if [[ $AGE -le 25 ]]; then echo "25 or younger"; fi     # less than or equal
if [[ $AGE -gt 18 ]]; then echo "Over 18"; fi           # greater than
if [[ $AGE -ge 21 ]]; then echo "21 or older"; fi       # greater than or equal
```

The mnemonic for these is "**eq**ual, **n**ot **e**qual, **l**ess **t**han, **l**ess or **e**qual, **g**reater **t**han, **g**reater or **e**qual." Don't be tempted to use `<` and `>` here — inside `[[ ]]` they perform *string* comparison, not numeric (so `"10" < "9"` would be true because "1" comes before "9" alphabetically).

**File and directory tests:**

```bash
FILE="/etc/hosts"
DIR="/home/alice"

if [[ -f "$FILE" ]]; then
    echo "$FILE exists and is a regular file"
fi

if [[ -d "$DIR" ]]; then
    echo "$DIR is a directory"
fi

if [[ -r "$FILE" ]]; then
    echo "$FILE is readable"
fi

if [[ -w "$FILE" ]]; then
    echo "$FILE is writable"
fi

if [[ -x "/usr/bin/python3" ]]; then
    echo "Python 3 is executable"
fi

if [[ -e "$FILE" ]]; then
    echo "$FILE exists (file or directory)"
fi
```

These are invaluable for writing robust scripts. Before reading a config file, check `-r`. Before writing a log, check `-w` (or that the parent directory exists). Before assuming a tool is installed, check that its binary is `-x`. Defensive checks like these prevent confusing errors deep in a script and let us provide clear error messages instead.

**Combining conditions:**

```bash
AGE=25
NAME="Alice"

# AND — both must be true
if [[ $AGE -gt 18 && "$NAME" == "Alice" ]]; then
    echo "Alice is over 18"
fi

# OR — at least one must be true
if [[ $AGE -lt 13 || $AGE -gt 65 ]]; then
    echo "Youth or senior discount applies"
fi

# NOT
if [[ ! -f "/tmp/lockfile" ]]; then
    echo "No lock file found, safe to proceed"
fi
```

The `&&` and `||` operators short-circuit, just like in most languages: with `&&`, if the first condition is false, the second isn't evaluated; with `||`, if the first is true, the second isn't evaluated. The "lock file" pattern shown with `!` is a common idiom for preventing two copies of a script from running at the same time.

#### Case statement
When we need to match a value against multiple patterns, `case` is cleaner than many `elif` chains. It's especially useful for scripts that take a "command" or "subcommand" argument (like `git pull`, `git push`, etc.):

```bash
read -p "Enter a fruit name: " FRUIT

case "$FRUIT" in
    apple)
        echo "Apples are red or green."
        ;;
    banana)
        echo "Bananas are yellow."
        ;;
    orange|tangerine)
        echo "Citrus fruit!"
        ;;
    *)
        echo "Unknown fruit: $FRUIT"
        ;;
esac
```

Each pattern ends with `)`, commands end with `;;`, and the whole block ends with `esac` ("case" backwards). The `|` lets us match multiple patterns against the same block, and `*` is a wildcard that catches anything not matched above — like the `default` clause in other languages. Patterns can also use shell glob syntax like `*.txt` or `[0-9]*` for more flexible matching.

---

## Loops
Loops let us repeat actions — process every file in a directory, retry a network call until it succeeds, or count from 1 to 100. They're where shell scripting starts to feel genuinely powerful.

#### for loop — Iterate over a list
The most common loop. Iterate over a list of values:

```bash
for color in red green blue; do
    echo "Color: $color"
done
```

The variable (`color` here) takes each value in turn. The list can be hardcoded as above, or generated dynamically from a command, glob pattern, or variable.

Iterate over files:

```bash
for file in *.txt; do
    echo "Processing: $file"
    wc -l "$file"
done
```

Bash expands `*.txt` into a list of matching filenames before the loop starts — this is called **globbing**. If no files match, by default Bash leaves the pattern as the literal string `*.txt`, which can cause unexpected behavior; `shopt -s nullglob` makes the pattern expand to nothing instead. Always quote `"$file"` inside the loop to handle filenames with spaces correctly.

Iterate over numbers with a range using `seq` or brace expansion:

```bash
for i in {1..5}; do
    echo "Count: $i"
done
```

Brace expansion `{1..5}` is evaluated by Bash itself — fast and clean. We can also do `{1..10..2}` for "1 to 10, step 2" (giving 1, 3, 5, 7, 9), or `{a..z}` for letters.

C-style for loop (numeric iteration):

```bash
for (( i=0; i<10; i++ )); do
    echo "i = $i"
done
```

This will look familiar from C, Java, JavaScript, and many other languages. It's more flexible than brace expansion when the range depends on variables, like `for (( i=0; i<$COUNT; i++ ))`.

#### while loop — Run while a condition is true
```bash
COUNT=1

while [[ $COUNT -le 5 ]]; do
    echo "Count: $COUNT"
    (( COUNT++ ))
done
```

The condition is checked *before* each iteration, so if it starts false, the loop body never runs. `while` is the right choice when we don't know in advance how many iterations we'll need — such as polling for an event or processing input until it ends.

Reading lines from a file with a while loop:

```bash
while IFS= read -r line; do
    echo "Line: $line"
done < /etc/hosts
```

This is the canonical pattern for processing a file line-by-line in Bash. The `< /etc/hosts` redirects the file into the loop's standard input, which `read` consumes one line at a time.

`IFS=` prevents leading/trailing whitespace from being stripped (`IFS` is the "Internal Field Separator" Bash uses to split words). `-r` prevents backslash interpretation, so a line like `path\to\file` is read literally instead of treating `\t` as a tab. Together, `IFS= read -r` is the safe way to read arbitrary text — without these flags, files with unusual whitespace or backslashes can produce surprising results.

#### until loop — Run until a condition becomes true
`until` is the opposite of `while` — it runs until the condition becomes true:

```bash
COUNT=1

until [[ $COUNT -gt 5 ]]; do
    echo "Count: $COUNT"
    (( COUNT++ ))
done
```

`until` is rarely used in practice — most logic reads more naturally as `while`. It's occasionally clearer when expressing "keep retrying *until* this thing succeeds," like waiting for a service to come up.

#### break and continue
- `break` — exit the loop immediately
- `continue` — skip to the next iteration

```bash
for i in {1..10}; do
    if [[ $i -eq 5 ]]; then
        continue    # Skip 5
    fi
    if [[ $i -eq 8 ]]; then
        break       # Stop at 8
    fi
    echo "$i"
done
```

Output: `1 2 3 4 6 7`

Walking through it: when `i` reaches 5, `continue` jumps back to the top of the loop without running the `echo`, so `5` is never printed. When `i` reaches 8, `break` exits the loop entirely, so neither `8` nor anything after it is printed. These two keywords are essential for early termination and selective skipping in real-world loops.

---

## Functions
Functions let us reuse blocks of code and keep scripts organized. As scripts grow longer, factoring repeated logic into well-named functions makes them dramatically more readable and maintainable — the same reasoning that applies in any programming language.

#### Defining and calling functions

```bash
# Define the function
greet() {
    echo "Hello, $1!"    # $1 is the first argument passed to the function
}

# Call the function
greet "Alice"
greet "Bob"
```

Notice that we **don't** put parentheses or commas when calling the function — we call it just like any other command, with arguments space-separated. Inside the function, `$1`, `$2`, etc. refer to the function's arguments, not the script's. (If we need the script's arguments inside a function, we'd save them to a variable before calling the function.)

Functions must be defined before they are called (placed earlier in the script). Bash reads the script top-to-bottom, so it has to see the function definition before it encounters a call to it. A common pattern is to put all function definitions at the top of the script, then have the actual logic at the bottom.

#### Return values
Bash functions don't return values like in other languages. Instead, they use either:
- `echo` to output a value (captured with command substitution)
- `return` to set an exit code (0=success, non-zero=error)

This is one of the more confusing aspects of Bash for newcomers from other languages. `return` does *not* return a value the way `return` does in Python or JavaScript — it sets the function's *exit status*, which is a number from 0 to 255 indicating success or failure. To "return" actual data, we print it with `echo` and capture it from the caller.

```bash
add() {
    local RESULT=$(( $1 + $2 ))
    echo $RESULT    # "return" via echo
}

SUM=$(add 10 20)
echo "10 + 20 = $SUM"
```

Here, `$(add 10 20)` runs the function and captures whatever it printed to stdout — that captured text becomes the value of `SUM`.

Using `return` for success/failure:

```bash
is_even() {
    if (( $1 % 2 == 0 )); then
        return 0    # Success (true)
    else
        return 1    # Failure (false)
    fi
}

if is_even 4; then
    echo "4 is even"
fi
```

Note the inversion: `0` means success/true and non-zero means failure/false. This matches the convention used throughout Unix — most commands return 0 on success, and `if` treats a 0 exit code as "true." It's the opposite of Boolean conventions in most programming languages, so it takes some getting used to.

#### Local variables
Variables inside functions are **global** by default. Use `local` to keep them scoped to the function:

```bash
calculate() {
    local A=$1
    local B=$2
    local RESULT=$(( A * B ))
    echo $RESULT
}

calculate 5 6    # 30
```

Without `local`, `A`, `B`, and `RESULT` would persist in the script's global scope after the function returns — and worse, they'd silently overwrite any variables of the same name in the calling code. Always use `local` for variables that are internal to a function. This is a small habit that prevents a whole class of debugging headaches.

---

## Heredoc — Multi-line Text
A **heredoc** (here document) lets us write multi-line text without escaping every line. It's perfect for embedding blocks of text — config files, SQL queries, email bodies, help messages — directly into a script:

```bash
cat << EOF
This is line 1.
This is line 2.
Current user: $USER
Current date: $(date)
EOF
```

The text between `<< EOF` and `EOF` is passed as standard input to `cat`. Variable substitution happens inside the heredoc, just like in double-quoted strings — so we can mix static text with dynamic values from the script.

`EOF` is just a convention for the delimiter — we can use any unique word (`END`, `STOP`, `EOM`, etc.). What matters is that the same word appears at the start (after `<<`) and at the end (alone on its own line, with no leading whitespace by default).

To prevent variable substitution, quote the delimiter:

```bash
cat << 'EOF'
This $variable will NOT be expanded.
$(date) will also NOT be executed.
EOF
```

This is the heredoc equivalent of single-quoted strings — useful when we genuinely want to print a `$` or write a literal command-substitution syntax (e.g., when generating a script that will be run later).

Heredocs are useful for creating configuration files within scripts:

```bash
cat << EOF > /etc/myapp/config.conf
server_name = production
port = 8080
debug = false
EOF
```

Here we redirect the heredoc's output to a file with `>`, generating the config file in one clean step — no need for multiple `echo` statements or temporary files.

---

## Exit Codes and Error Handling
Every command in Linux returns an **exit code** when it finishes:
- `0` — success
- Any non-zero value — failure (different numbers indicate different types of failure)

This is the universal language commands use to signal success or failure. It's how `if some_command; then ...` works — under the hood, `if` is checking whether the command's exit code was zero. Specific exit codes vary by program: `127` means "command not found," `1` is generic failure, `2` often means misuse, and so on.

We check the last command's exit code with `$?`:

```bash
ls /nonexistent_directory
echo "Exit code: $?"    # Will print a non-zero value (error)

ls /home
echo "Exit code: $?"    # Will print 0 (success)
```

`$?` only contains the exit code of the *immediately previous* command, so if we want to use it, we have to capture it right away — by the next command, it's been overwritten.

#### set -e — Exit on error
By default, scripts continue running even when a command fails. This is dangerous: imagine a deployment script that fails to download a new version of an app, but then proceeds to delete the old version anyway. Adding `set -e` at the top causes the script to **exit immediately** on any error:

```bash
#!/usr/bin/env bash
set -e    # Exit on first error

cd /some/directory      # If this fails, script stops here
cp important_file.txt backup/
process_file.sh
```

This is highly recommended for deployment and maintenance scripts where we never want to continue if something goes wrong. There are some edge cases (commands inside `if` conditions are exempt, for example, since the whole point is to test their exit code), but in general, `set -e` makes scripts dramatically safer.

#### set -u — Error on undefined variables
`set -u` causes the script to exit with an error if we use an undefined variable (prevents bugs from typos):

```bash
set -u

echo $UNDERFINED_VAR    # Script exits with error instead of silently using ""
```

Without `set -u`, undefined variables silently expand to an empty string. This can lead to dangerous bugs like `rm -rf "$BASE_DIR/$SUBDIR"` becoming `rm -rf "/"` if `$BASE_DIR` was misspelled. Catching the typo early is far better than discovering it after a disaster.

#### Combining safety options
A common best practice for robust scripts:

```bash
#!/usr/bin/env bash
set -euo pipefail

# -e: exit on error
# -u: error on undefined variable
# -o pipefail: exit if any command in a pipeline fails
```

`pipefail` makes pipelines like `cmd1 | cmd2` fail if any command in the pipeline fails (not just the last one). By default, the exit code of `cmd1 | cmd2` is just the exit code of `cmd2`, which means `failing_command | grep something` would appear to succeed if `grep` worked — even though the real command failed. `pipefail` fixes this by propagating any failure in the pipeline.

#### trap — Run cleanup on exit
`trap` lets us run commands when the script exits (whether normally, on error, or on Ctrl+C). It's the Bash equivalent of a `finally` block in other languages — a way to guarantee cleanup happens no matter how the script ends:

```bash
#!/usr/bin/env bash
set -e

TEMPFILE=$(mktemp)

# This runs on any exit, ensuring cleanup
trap "rm -f $TEMPFILE" EXIT

echo "Working with $TEMPFILE..."
# ... script work ...
echo "Done. Cleaning up."
# TEMPFILE will be deleted automatically when script exits
```

The `EXIT` signal fires for any kind of exit — clean exit, error exit (with `set -e`), or interruption. We can also trap specific signals: `trap "..." INT` runs on Ctrl+C, `trap "..." TERM` runs on `kill`, and so on. This pattern is essential for scripts that create temporary files, lock files, or other resources that need to be cleaned up reliably.

---

## Practical Script Examples
These examples show how the building blocks above come together into useful, real-world scripts. Reading and understanding them is one of the best ways to internalize Bash patterns.

#### Example 1: Backup script
This script creates a timestamped backup of a directory:

```bash
#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$HOME/Documents"
BACKUP_DIR="$HOME/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/documents_$TIMESTAMP.tar.gz"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

echo "Starting backup of $SOURCE_DIR..."
tar -czf "$BACKUP_FILE" "$SOURCE_DIR"
echo "Backup completed: $BACKUP_FILE"
echo "Backup size: $(du -sh "$BACKUP_FILE" | cut -f1)"
```

What's happening here: we define configuration variables at the top so they're easy to find and change. The timestamp uses a sortable format (`YYYYMMDD_HHMMSS`) so backup files naturally sort chronologically. `mkdir -p` creates the backup directory and silently does nothing if it already exists — a useful idempotent pattern. `tar -czf` creates a gzip-compressed archive (`c`=create, `z`=gzip, `f`=filename). Finally, `du -sh` reports the human-readable size, and we pipe it through `cut -f1` to keep only the size (dropping the trailing path).

#### Example 2: System health check script
This script checks key system metrics and reports their status:

```bash
#!/usr/bin/env bash

echo "===== System Health Check ====="
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo ""

echo "--- Disk Usage ---"
df -h | grep -v tmpfs

echo ""
echo "--- Memory Usage ---"
free -h

echo ""
echo "--- CPU Load ---"
uptime

echo ""
echo "--- Top 5 Processes by CPU ---"
ps aux --sort=-%cpu | head -6

echo ""
echo "===== Check Complete ====="
```

This is a classic "snapshot the system state" script — useful for diagnostics or as a daily cron report. `df -h` shows human-readable disk usage; `grep -v tmpfs` filters out temporary in-memory filesystems we don't usually care about. `free -h` shows memory usage. `uptime` shows the load averages (1, 5, and 15 minute averages). `ps aux --sort=-%cpu | head -6` shows the top CPU consumers (`head -6` because the first line is a header, leaving 5 actual processes). Notice we don't use `set -e` here — for a reporting script, we want it to keep going even if one section fails.

#### Example 3: User creation script with validation
A script that creates a user only if they don't already exist:

```bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <username>"
    exit 1
fi

USERNAME="$1"

# Validate username: only lowercase letters, numbers, hyphens
if [[ ! "$USERNAME" =~ ^[a-z][a-z0-9-]*$ ]]; then
    echo "Error: Invalid username. Use lowercase letters, numbers, and hyphens only."
    exit 1
fi

# Check if user already exists
if id "$USERNAME" &>/dev/null; then
    echo "User '$USERNAME' already exists."
    exit 0
fi

# Create the user
sudo adduser --disabled-password --gecos "" "$USERNAME"
echo "User '$USERNAME' created successfully."
```

This script is a great showcase of defensive scripting practices. First, it checks `$#` to make sure exactly one argument was given — otherwise it prints a usage message and exits with code 1. Second, it uses `[[ ... =~ regex ]]` (a Bash-specific regex match) to validate the username matches a safe pattern: starts with a lowercase letter, followed by lowercase letters, digits, or hyphens. This prevents shell-injection attacks and enforces standard Linux username conventions. Third, it uses `id` (which exits 0 if the user exists, non-zero otherwise) to check for existence; `&>/dev/null` discards both stdout and stderr so we just care about the exit code. Notably, this case exits with code 0 — "user already exists" is treated as a success because the desired state is achieved (idempotency!). Finally, `adduser` actually creates the user; `--disabled-password` means no password login (force key-based auth), and `--gecos ""` skips the interactive prompts for full name, room number, etc.