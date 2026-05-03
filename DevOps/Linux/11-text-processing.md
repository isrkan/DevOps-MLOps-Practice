# Text Processing and Advanced Shell Tools — The Real Power of Linux

This is where Linux truly shines. The tools in this guide — `grep`, `sed`, `awk`, `find`, and friends — plus the ability to chain them together with pipes and redirection — form the powerful text-processing environment. A handful of commands connected by pipes can analyze millions of log lines, transform data formats, extract information from files, and automate tasks that would take hours of manual work in other environments.

The Unix philosophy is: "write programs that do one thing and do it well, and that work well together." This guide is the payoff of that philosophy.

---

## I/O Redirection
Every Linux command has three standard data streams:
- **stdin** (standard input, file descriptor 0) — data going INTO the command
- **stdout** (standard output, file descriptor 1) — normal output from the command
- **stderr** (standard error, file descriptor 2) — error messages from the command

By default, stdin comes from the keyboard, stdout goes to the terminal, and stderr also goes to the terminal. **Redirection** changes where these streams go.

#### `>` — Redirect stdout (overwrite)
Send the output of a command to a file instead of the terminal:

```bash
ls -l > directory_listing.txt
```

The file is created if it doesn't exist, or **overwritten** if it does. Be careful with `>` — it silently replaces existing content.

#### `>>` — Redirect stdout (append)
Append output to a file without overwriting:

```bash
echo "New log entry: $(date)" >> app.log
```

This adds to the end of the file. If the file doesn't exist, it's created.

#### `2>` — Redirect stderr
Send error messages to a file:

```bash
ls /nonexistent_directory 2> errors.txt
```

Normal output goes to the terminal; error messages go to the file.

#### `2>&1` — Merge stderr into stdout
Redirect both stdout and stderr to the same place:

```bash
./script.sh > output.log 2>&1
```

Both regular output and error messages go to `output.log`. This is the standard pattern for capturing all output from a command.

A shorter modern syntax does the same:

```bash
./script.sh &> output.log
```

#### `/dev/null` — The black hole
`/dev/null` is a special file that discards everything written to it. It's useful when we want to suppress output:

```bash
# Suppress stdout (we only care if there are errors)
./script.sh > /dev/null

# Suppress all output (run silently)
./script.sh > /dev/null 2>&1

# Find files but suppress "permission denied" errors
find / -name "*.conf" 2>/dev/null
```

#### `<` — Redirect stdin
Feed a file as input to a command:

```bash
sort < unsorted.txt
```

This is equivalent to `sort unsorted.txt` for most commands, but some commands only read from stdin.

#### `<<` — Heredoc (inline stdin)
We covered heredoc in the scripting guide, but it's worth noting here: `<<` provides multi-line input to a command inline:

```bash
sort << EOF
banana
apple
cherry
EOF
```

Output:

```
apple
banana
cherry
```

---

## Pipes — Chaining Commands Together
The **pipe** (`|`) connects the stdout of one command to the stdin of the next. This lets us build processing pipelines where data flows from left to right.

```bash
command1 | command2 | command3
```

The output of `command1` becomes the input of `command2`, whose output becomes the input of `command3`.

**Simple example:** Count how many files are in a directory:

```bash
ls | wc -l
```

`ls` outputs one filename per line; `wc -l` counts the lines.

**Real-world example:** Find the most common IPs in a web server access log:

```bash
cat /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```

Breaking it down:
1. `cat` outputs the log file
2. `awk '{print $1}'` extracts the first field (IP address) from each line
3. `sort` sorts the IPs alphabetically
4. `uniq -c` counts consecutive duplicates (only works on sorted input!)
5. `sort -rn` sorts numerically in reverse (largest counts first)
6. `head -10` shows the top 10

This single pipeline extracts real intelligence from a log file in milliseconds.

---

## grep — Searching Text
`grep` (Global Regular Expression Print) searches for lines matching a pattern. It's arguably the most-used text command in Linux.

#### Basic usage
Search for lines containing a pattern in a file:

```bash
grep "error" /var/log/syslog
```

This prints every line in `/var/log/syslog` that contains the word "error".

#### Essential grep options
**Case-insensitive search** — match regardless of uppercase/lowercase:

```bash
grep -i "error" /var/log/syslog
```

**Recursive search** — search all files in a directory tree:

```bash
grep -r "TODO" ~/projects/
```

**Show line numbers** — prefix each match with its line number:

```bash
grep -n "def main" script.py
```

**Invert match** — show lines that do NOT match:

```bash
grep -v "^#" /etc/ssh/sshd_config    # Show lines that aren't comments
grep -v "^$" file.txt                  # Remove blank lines
```

**Count matching lines:**

```bash
grep -c "error" /var/log/syslog
```

**Show only filenames** (not the matching lines):

```bash
grep -l "password" ~/projects/**/*.py
```

**Show surrounding context:**

```bash
grep -A 3 "ERROR" app.log    # 3 lines After each match
grep -B 3 "ERROR" app.log    # 3 lines Before each match
grep -C 3 "ERROR" app.log    # 3 lines Context (before and after)
```

#### grep with regular expressions
grep supports regular expressions — patterns that describe text structure.

Common regex elements:
- `.` — any single character
- `*` — zero or more of the preceding character
- `+` — one or more of the preceding (use with `-E`)
- `^` — beginning of line
- `$` — end of line
- `[abc]` — any character in the set (a, b, or c)
- `[^abc]` — any character NOT in the set
- `\b` — word boundary

Examples:

```bash
grep "^alice" /etc/passwd             # Lines starting with "alice"
grep "bash$" /etc/passwd              # Lines ending with "bash"
grep "^[0-9]" data.txt                # Lines starting with a digit
grep -E "error|warning" app.log       # Lines with "error" OR "warning"
grep -E "\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b" access.log  # IP addresses
```

`-E` enables **Extended Regular Expressions** (ERE), which supports `+`, `?`, `|`, and `()` without escaping them.

#### Combining grep with other commands

```bash
ps aux | grep nginx                         # Find nginx processes
cat /etc/passwd | grep -v "nologin"         # Users with actual shells
dmesg | grep -i "error"                     # Kernel error messages
history | grep "git commit"                 # Find past git commit commands
```

---

## find — Finding Files
Imagine we need to find a file but we can't remember exactly where we saved it. Or we want to find every log file that hasn't been touched in 30 days and delete them. `find` is the tool for this.

`find` searches our filesystem in real time — it walks through directories and checks every file against the criteria we give it. This means results are always up to date, but it can be slow on large directories because it checks every single file.

The general structure of a `find` command is:
```
find [where to search] [what to look for] [what to do with results]
```

For example: `find ~ -name "*.txt"` means "search in my home directory (`~`) for anything with a name ending in `.txt`."

#### Basic find by name
Find all `.txt` files anywhere in the home directory:

```bash
find ~ -name "*.txt"
```

The `~` means "start searching from my home directory." We can replace it with any path — `/` to search the whole system, `/etc` to search only that folder, etc.

The `*` is a wildcard meaning "anything." So `"*.txt"` means "any name that ends in `.txt`."

Case-insensitive name search (matches `notes.txt`, `NOTES.TXT`, `Notes.Txt`, etc.):

```bash
find ~ -iname "*.txt"
```

Find a file by its exact name:

```bash
find /etc -name "sshd_config"
```

#### find by type
By default, `find` returns both files and directories. The `-type` option narrows it down.

Find only regular files (not directories):

```bash
find /home -type f -name "*.log"
```

Find only directories:

```bash
find /home -type d -name "projects"
```

Find symbolic links (shortcuts that point to another file):

```bash
find /usr/bin -type l
```

The most common types are `f` (file), `d` (directory), and `l` (symbolic link).

#### find by size
Find files larger than 100 MB — useful when our disk is filling up and we want to know what's taking space:

```bash
find / -type f -size +100M
```

The `+` means "more than." Use `-` for "less than":

```bash
find ~ -type f -size -10k
```

Find files between 1 MB and 5 MB (combine both):

```bash
find ~ -type f -size +1M -size -5M
```

Size units: `c` (bytes), `k` (kilobytes), `M` (megabytes), `G` (gigabytes).

#### find by modification time
"mtime" means "modification time" — the last time a file's content was changed.

Find files modified in the last 7 days (the `-` means "less than 7 days ago"):

```bash
find ~ -mtime -7
```

Find files not modified in over 30 days (useful for finding stale or forgotten files):

```bash
find ~ -mtime +30
```

Find files modified in the last 60 minutes:

```bash
find ~ -mmin -60
```

The unit for `-mtime` is days; for `-mmin` it's minutes.

#### find with -exec — Run a command on results
This is where `find` becomes truly powerful. Instead of just listing files, we can run a command on each one.

The syntax uses `{}` as a placeholder for the filename, and `\;` to end the command:

```bash
find ~ -name "*.tmp" -exec rm {} \;
```

This means: "find every `.tmp` file in my home directory, and for each one, run `rm` on it."

A more efficient version uses `+` instead of `\;` — it groups all the results and passes them to one `rm` call instead of running `rm` once per file:

```bash
find ~ -name "*.tmp" -exec rm {} +
```

Set permissions on all Python scripts found in a project:

```bash
find ~/projects -name "*.py" -exec chmod 644 {} +
```

Print just the filename without the full path:

```bash
find ~/projects -name "*.py" -exec basename {} \;
```

#### Suppressing "Permission denied" errors
When searching system directories like `/`, `find` will often print "Permission denied" for folders we can't read. Redirect those error messages away with `2>/dev/null`:

```bash
find / -name "*.conf" 2>/dev/null
```

The `2>/dev/null` sends error messages to `/dev/null` (a special "trash" destination that discards everything), so we only see the actual results.

#### Practical find examples

```bash
# Find large log files to clean up
find /var/log -type f -size +50M

# Find Python files modified today
find ~/projects -name "*.py" -mtime 0

# Find world-writable files (security check)
find /home -perm -o+w -type f

# Find SUID files (security audit)
find / -perm -4000 -type f 2>/dev/null
```

---

## locate — Fast File Search
`find` is powerful but slow on large systems because it scans every file in real time. `locate` takes a completely different approach: it searches a **pre-built database** of all filenames on the system. This makes it extremely fast — searching the entire filesystem takes less than a second.

The tradeoff is that the database is not updated instantly. New files won't appear in `locate` results until the database is refreshed. This makes `locate` best for finding established files, while `find` is better when we need up-to-the-second accuracy.

#### Installing locate
`locate` may not be installed by default. Install it with:

```bash
sudo apt install plocate
```

`plocate` is the modern, faster replacement for the older `mlocate` package. After installation, it automatically builds the initial database.

#### The database — updatedb
`locate` works by searching a database file (usually at `/var/lib/plocate/plocate.db`) that is rebuilt periodically by a background job. On most systems this runs automatically once a day.

To manually rebuild the database right now (for example, after creating new files we want to find immediately):

```bash
sudo updatedb
```

This scans the entire filesystem and updates the database. It takes a moment to run.

#### Basic usage
Find all files with "config" anywhere in their name or path:

```bash
locate config
```

`locate` matches any part of the full file path, so `locate config` would match `/etc/nginx/nginx.conf`, `/home/alice/.config/settings`, etc.

Find a file by exact name:

```bash
locate sshd_config
```

#### Case-insensitive search
By default, `locate` is case-sensitive. Use `-i` to ignore case:

```bash
locate -i readme
```

This matches `README.md`, `readme.txt`, `ReadMe`, etc.

#### Limit the number of results
If there are thousands of matches, use `-n` to show only the first few:

```bash
locate -n 20 ".log"
```

#### Count matches without listing them
```bash
locate -c ".py"
```

This prints just the number of matching files — useful to get a quick sense of how many files exist before listing them all.

#### Combining with grep
Since `locate` can return many results, we often pipe it through `grep` to filter further:

```bash
locate ".conf" | grep nginx
```

This finds all `.conf` files in the database, then filters to show only those with "nginx" in the path.

#### When locate won't find a new file
If we just created a file and `locate` can't find it, it's because the database hasn't been updated yet. Run `sudo updatedb` and then try again.

---

## find vs. locate — Which to use?

| | `find` | `locate` |
|---|---|---|
| **Speed** | Slow on large directories | Very fast (searches a database) |
| **Results** | Always up to date | May miss very recently created files |
| **Search by** | Name, size, type, date, permissions, and more | Name / path only |
| **Actions on results** | Yes (`-exec`) | No (just lists results) |
| **Needs root for some paths** | Yes | No (database is pre-built) |
| **Best for** | Precise, powerful searches; acting on results | Quickly finding established files by name |

A simple rule of thumb: use `locate` when we just want to find where a file lives and speed matters. Use `find` when we need to filter by size, date, type, or want to do something with the results.

---

## sed — Stream Editor
`sed` processes text line by line, applying editing commands. It's excellent for making consistent changes to files or transforming text in a pipeline.

#### Basic substitution
Replace the first occurrence of "old" with "new" on each line:

```bash
sed 's/old/new/' file.txt
```

Replace ALL occurrences on each line (add `g` flag):

```bash
sed 's/old/new/g' file.txt
```

Case-insensitive replacement:

```bash
sed 's/error/ERROR/gi' file.txt
```

By default, sed outputs to stdout — it doesn't modify the original file. To edit in place:

```bash
sed -i 's/old/new/g' file.txt
```

**Always make a backup before editing in place:**

```bash
sed -i.bak 's/old/new/g' file.txt    # Creates file.txt.bak before editing
```

#### Practical substitution examples
Remove leading whitespace from each line:

```bash
sed 's/^[[:space:]]*//' file.txt
```

Remove trailing whitespace:

```bash
sed 's/[[:space:]]*$//' file.txt
```

Remove blank lines:

```bash
sed '/^$/d' file.txt
```

Comment out lines containing "DEBUG":

```bash
sed 's/^.*DEBUG.*$/#&/' file.txt    # & is replaced by the matched text
```

Replace all occurrences in multiple files:

```bash
sed -i 's/localhost/production.server.com/g' config/*.conf
```

#### Printing specific lines
Print only lines 5 through 10:

```bash
sed -n '5,10p' file.txt
```

The `-n` suppresses default output; `p` explicitly prints the specified lines.

Print lines matching a pattern:

```bash
sed -n '/error/p' app.log
```

#### Deleting lines
Delete lines matching a pattern:

```bash
sed '/^#/d' config.txt              # Delete comment lines
sed '/^$/d' file.txt                # Delete blank lines
sed '1d' file.txt                   # Delete first line
sed '1,5d' file.txt                 # Delete lines 1 through 5
```

#### Inserting and appending text
Insert a line before a matching line:

```bash
sed '/^server/i # Server configuration section' config.conf
```

Append a line after a matching line:

```bash
sed '/^server/a     timeout = 30' config.conf
```

---

## awk — Text Processing Language
`awk` is a complete programming language designed for processing structured text, especially column-based data like CSV files, log files, and command output. It processes files line by line, automatically splitting each line into **fields** (columns).

#### Basic awk usage
Print the first field (column) of each line:

```bash
awk '{print $1}' file.txt
```

`$1` is the first field, `$2` is the second, `$NF` is the last field, `$0` is the entire line.

Print multiple fields:

```bash
awk '{print $1, $3}' file.txt
```

#### Field separators
By default, awk splits on whitespace. For other delimiters, use `-F`:

For CSV files (comma-separated):

```bash
awk -F',' '{print $1, $3}' data.csv
```

For `/etc/passwd` (colon-separated):

```bash
awk -F: '{print $1, $6}' /etc/passwd    # username and home directory
```

#### Filtering with conditions
Print lines where field 3 is greater than 100:

```bash
awk '$3 > 100 {print $0}' data.txt
```

Print lines where field 1 matches a pattern:

```bash
awk '$1 ~ /alice/ {print}' /etc/passwd    # ~ means "matches regex"
awk '$1 !~ /alice/ {print}' /etc/passwd   # !~ means "doesn't match"
```

Print lines where field 3 equals "active":

```bash
awk '$3 == "active" {print $1, $2}' users.csv
```

#### Calculations with awk
Sum a column of numbers:

```bash
awk '{sum += $1} END {print "Total:", sum}' numbers.txt
```

Calculate the average:

```bash
awk '{sum += $3; count++} END {print "Average:", sum/count}' data.txt
```

The `END` block runs after all lines have been processed. There's also a `BEGIN` block that runs before any lines:

```bash
awk 'BEGIN {print "Processing..."} {sum += $1} END {print "Total:", sum}' data.txt
```

#### Practical awk examples
Show only usernames and shells from `/etc/passwd`:

```bash
awk -F: '{print $1, $7}' /etc/passwd
```

Show username and home directory for users with UID >= 1000 (regular users):

```bash
awk -F: '$3 >= 1000 {print $1, $6}' /etc/passwd
```

Calculate total disk usage from `du` output:

```bash
du -s ~/projects/* | awk '{sum += $1} END {print sum/1024, "MB"}'
```

Count lines per HTTP response code in an access log:

```bash
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -rn
```

---

## Other Essential Text Utilities

#### cut — Extract specific columns
`cut` extracts specific columns or character ranges from each line.

By delimiter (extract the first field from a colon-separated file):

```bash
cut -d: -f1 /etc/passwd
```

Extract fields 1 and 3:

```bash
cut -d: -f1,3 /etc/passwd
```

Extract by character position (characters 1 through 10):

```bash
cut -c1-10 file.txt
```

#### sort — Sort text
Sort alphabetically:

```bash
sort names.txt
```

Sort numerically:

```bash
sort -n numbers.txt
```

Sort in reverse:

```bash
sort -r names.txt
sort -rn numbers.txt
```

Sort by a specific field (field 3, numeric):

```bash
sort -k3 -n data.txt
```

Sort a CSV by the second column:

```bash
sort -t',' -k2 data.csv
```

Remove duplicate lines while sorting:

```bash
sort -u names.txt
```

#### uniq — Remove or count duplicates
`uniq` removes consecutive duplicate lines. It must be used on sorted input (run `sort` first):

```bash
sort names.txt | uniq
```

Count occurrences of each line:

```bash
sort names.txt | uniq -c
```

Show only lines that appear more than once:

```bash
sort names.txt | uniq -d
```

Show only lines that appear exactly once:

```bash
sort names.txt | uniq -u
```

#### wc — Word, line, and character count

```bash
wc -l file.txt      # Count lines
wc -w file.txt      # Count words
wc -c file.txt      # Count bytes/characters
wc file.txt         # All three: lines, words, characters
```

Combined with pipes:

```bash
ps aux | wc -l                    # Count running processes
cat /etc/passwd | wc -l           # Count user accounts
find ~/projects -name "*.py" | wc -l   # Count Python files
```

#### tr — Translate or delete characters
`tr` translates (replaces) or deletes individual characters. It reads from stdin.

Convert lowercase to uppercase:

```bash
echo "hello world" | tr 'a-z' 'A-Z'
```

Delete specific characters:

```bash
echo "He-llo, Wor-ld!" | tr -d '-'    # Output: Hello, World!
```

Squeeze multiple spaces into one:

```bash
echo "too   many   spaces" | tr -s ' '
```

Remove newlines (join all lines into one):

```bash
cat file.txt | tr -d '\n'
```

#### tee — Split output to file and terminal
`tee` writes output to BOTH a file and stdout — useful when we want to see output in the terminal AND save it:

```bash
./script.sh | tee output.log
```

To append to the file:

```bash
./script.sh | tee -a output.log
```

#### xargs — Build commands from stdin
`xargs` takes lines from stdin and turns them into arguments for a command. It's essential for bridging find and other commands.

Delete all `.tmp` files found by find:

```bash
find ~ -name "*.tmp" | xargs rm
```

This is more efficient than `-exec rm {} +` for large numbers of files.

Count the lines in each Python file:

```bash
find ~/projects -name "*.py" | xargs wc -l
```

Pass stdin as an argument to a command that doesn't read stdin:

```bash
echo "/home/alice" | xargs ls
```

Handle filenames with spaces by using null-terminated strings:

```bash
find ~ -name "*.txt" -print0 | xargs -0 wc -l
```

---

## Powerful Pipeline Examples
The real magic happens when we chain these tools. Here are complete pipelines that solve real problems:

#### Find the 10 biggest files in our home directory:

```bash
find ~ -type f -printf '%s %p\n' 2>/dev/null | sort -rn | head -10 | awk '{printf "%s\t%s\n", $1, $2}'
```

#### Show the 10 most common words in a file:

```bash
cat essay.txt | tr '[:upper:]' '[:lower:]' | tr -s '[:punct:][:space:]' '\n' | sort | uniq -c | sort -rn | head -10
```

#### Find all failed SSH login attempts:

```bash
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn
```

#### Count HTTP status codes in nginx log:

```bash
awk '{print $9}' /var/log/nginx/access.log | grep -E '^[0-9]' | sort | uniq -c | sort -rn
```

#### Find which processes are using the most memory:

```bash
ps aux --sort=-%mem | head -11 | awk '{printf "%-20s %s%%\n", $11, $4}'
```

#### Extract all email addresses from a file:

```bash
grep -Eo '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' contacts.txt | sort -u
```