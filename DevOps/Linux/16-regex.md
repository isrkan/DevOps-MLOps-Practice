# Regular Expressions — Pattern Matching Mastery

Regular expressions (regex) are a language for describing patterns in text. Once learned, they apply everywhere: `grep`, `sed`, `awk`, `vim`, Python, JavaScript, databases, log analysis tools — the same patterns work in all of them. This is one of those skills that pays dividends for the entire rest of our career.

The goal of this guide is to build a complete mental model of regex — not just a list of symbols to memorize.

---

## The Core Idea
A regular expression is a **pattern** that either matches or doesn't match a piece of text. For example, the pattern `cat` matches the string "cat", "cats", "concatenate", and "tomcat" — anywhere the three letters c-a-t appear in sequence.

Regex is powerful because we can describe patterns that go far beyond literal strings:
- "a digit followed by two uppercase letters" 
- "a line that starts with ERROR"
- "an email address"
- "an IP address"

We'll build up from simple to complex.

---

## Literal Characters
The simplest regex is just a string of characters. `/error/` matches any line containing "error" anywhere.

```bash
grep "error" logfile.txt        # Matches: "An error occurred", "no errors found", etc.
```

Most characters match themselves literally. The special characters that don't are: `. * + ? ^ $ { } [ ] | ( ) \`

---

## Anchors — Matching Position
Anchors don't match characters — they match **positions** in the text.

#### `^` — Start of line
```bash
grep "^ERROR" logfile.txt       # Only lines that START with "ERROR"
grep "^$" file.txt              # Empty lines (nothing between start and end)
```

#### `$` — End of line
```bash
grep "\.py$" filelist.txt       # Lines ending with ".py"
grep "done$" output.txt         # Lines ending with "done"
```

#### `^...$` — Entire line
```bash
grep "^hello$" file.txt         # Lines containing ONLY "hello" (nothing else)
grep "^[0-9]*$" numbers.txt     # Lines containing only digits
```

#### `\b` — Word boundary
A word boundary matches between a word character (`[a-zA-Z0-9_]`) and a non-word character.

```bash
grep "\bcat\b" file.txt         # Matches "cat" but NOT "cats", "tomcat", "scatter"
grep "\berror\b" log.txt        # Matches standalone "error" but not "errors"
```

---

## The Dot — Any Single Character
`.` matches any single character except a newline.

```bash
grep "c.t" file.txt     # Matches "cat", "cut", "c1t", "c t" — any char between c and t
grep "^..$" file.txt    # Lines that contain exactly 2 characters
```

To match a literal dot (period), escape it with `\`:

```bash
grep "\." file.txt      # Lines containing a literal period
grep "192\.168" hosts   # IP address with literal dots
```

---

## Character Classes — [ ]
A character class matches **one character** from a defined set.

#### Simple character class
```bash
grep "[aeiou]" file.txt         # Any vowel
grep "[0-9]" file.txt           # Any digit
grep "[A-Z]" file.txt           # Any uppercase letter
grep "[a-zA-Z]" file.txt        # Any letter
grep "[a-zA-Z0-9]" file.txt     # Any alphanumeric character
```

#### Negated character class `[^...]`
The `^` inside `[]` means "NOT these characters":

```bash
grep "[^0-9]" file.txt          # Lines with any non-digit character
grep "^[^#]" config.txt         # Lines not starting with # (non-comment lines)
```

#### POSIX character classes (portable across tools)

| Class | Equivalent | Matches |
|-------|-----------|---------|
| `[:alpha:]` | `[a-zA-Z]` | Letters |
| `[:digit:]` | `[0-9]` | Digits |
| `[:alnum:]` | `[a-zA-Z0-9]` | Letters and digits |
| `[:space:]` | `[ \t\n\r]` | Whitespace |
| `[:upper:]` | `[A-Z]` | Uppercase letters |
| `[:lower:]` | `[a-z]` | Lowercase letters |
| `[:punct:]` | `[.,!?;:]` | Punctuation |

Used inside an outer `[]`:

```bash
grep "[[:digit:]]" file.txt     # Any digit
grep "[[:alpha:]_]" file.txt    # Any letter or underscore
```

---

## Quantifiers — How Many Times
Quantifiers apply to the preceding element (character, class, or group) and specify how many times it must appear.

#### `*` — Zero or more
```bash
grep "error*" file.txt          # "erro", "error", "errorr", "errorrrr"
grep "be*" file.txt             # "b", "be", "bee", "beee"
grep "[0-9]*" file.txt          # Zero or more digits (matches empty string too)
```

#### `+` — One or more (requires `-E` or `\+` in basic regex)
```bash
grep -E "error+" file.txt       # "error", "errorr" — at least one "r"
grep -E "[0-9]+" file.txt       # One or more digits (a number)
```

#### `?` — Zero or one (optional)
```bash
grep -E "colou?r" file.txt      # "color" or "colour" — u is optional
grep -E "https?" file.txt       # "http" or "https"
```

#### `{n}` — Exactly n times
```bash
grep -E "[0-9]{4}" file.txt     # Exactly 4 digits (year, PIN, etc.)
grep -E "[a-z]{3}" file.txt     # Exactly 3 lowercase letters
```

#### `{n,m}` — Between n and m times
```bash
grep -E "[0-9]{2,4}" file.txt   # 2 to 4 digits
grep -E "[a-z]{3,}" file.txt    # 3 or more lowercase letters
```

---

## Alternation — OR Patterns
`|` means "or" — match this OR that (requires `-E`):

```bash
grep -E "error|warning|critical" log.txt    # Any of these three words
grep -E "^(ERROR|WARN|INFO)" log.txt        # Lines starting with these log levels
grep -E "\.txt$|\.md$|\.csv$" filelist.txt  # Files with these extensions
```

---

## Groups — ( )
Parentheses group parts of a pattern together, allowing quantifiers and alternation to apply to the whole group (requires `-E`):

```bash
grep -E "(ab)+" file.txt        # "ab", "abab", "ababab" — repeat the group
grep -E "(cat|dog)s?" file.txt  # "cat", "cats", "dog", "dogs"
grep -E "^(GET|POST|PUT) " access.log   # HTTP method at line start
```

#### Backreferences — referring to captured groups
In `sed` and some grep patterns, we can refer to what a group matched using `\1`, `\2`, etc.:

```bash
# Find words that are repeated (like "the the")
grep -E "\b([a-z]+) \1\b" file.txt

# In sed, swap two words
echo "hello world" | sed -E 's/(\w+) (\w+)/\2 \1/'   # Output: "world hello"
```

---

## Basic Regex (BRE) vs Extended Regex (ERE)
grep has two modes:

- **Basic Regex (BRE)** — default; `+`, `?`, `|`, `{`, `(` are literal unless escaped: `\+`, `\?`
- **Extended Regex (ERE)** — enabled with `-E`; these characters are special without escaping

`grep -E` is equivalent to `egrep`. Always use `-E` for complex patterns.

```bash
# BRE (default) — must escape special chars
grep "error\+" file.txt
grep "\(cat\|dog\)" file.txt

# ERE (-E) — special chars are special by default
grep -E "error+" file.txt
grep -E "(cat|dog)" file.txt
```

In `sed`, use `-E` for extended regex:

```bash
sed -E 's/([0-9]+)/NUM/g' file.txt
```

---

## Practical Regex Patterns
These are real patterns used constantly in DevOps and development work.

#### Match an IP address (basic):
```bash
grep -E "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" file.txt
```

#### Match an email address (simple):
```bash
grep -E "\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b" file.txt
```

#### Match a URL:
```bash
grep -E "https?://[a-zA-Z0-9./_?=&%-]+" file.txt
```

#### Match a date (YYYY-MM-DD):
```bash
grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}" file.txt
```

#### Match a time (HH:MM:SS):
```bash
grep -E "[0-2][0-9]:[0-5][0-9]:[0-5][0-9]" file.txt
```

#### Extract log lines with ERROR or WARNING:
```bash
grep -E "^[0-9-]+ [0-9:]+ (ERROR|WARNING)" application.log
```

#### Find Python function definitions:
```bash
grep -E "^def [a-z_]+\(" *.py
```

#### Find lines with trailing whitespace:
```bash
grep -E " +$" file.txt
```

#### Match a valid port number (1-65535):
```bash
grep -E "\b([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\b"
```

---

## Regex in sed
`sed` uses regex for pattern matching and substitution:

```bash
# Replace all numbers with "NUM"
sed -E 's/[0-9]+/NUM/g' file.txt

# Remove HTML tags
sed -E 's/<[^>]+>//g' file.html

# Delete blank lines
sed '/^[[:space:]]*$/d' file.txt

# Extract only the IP address from each line (replace everything else)
sed -E 's/.*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*/\1/' file.txt

# Add a prefix to lines matching a pattern
sed -E '/ERROR/ s/^/>>> /' log.txt

# Remove comments (lines starting with #) and blank lines
sed -E '/^[[:space:]]*(#|$)/d' config.txt
```

---

## Regex in awk
`awk` uses regex for record matching and within conditions:

```bash
# Print lines matching a pattern
awk '/error/' file.txt

# Print lines NOT matching
awk '!/error/' file.txt

# Print lines where field 2 matches a pattern
awk '$2 ~ /[0-9]+/' file.txt

# Print lines where field 3 doesn't match
awk '$3 !~ /^admin/' users.txt

# Extract just the matched part using match()
awk 'match($0, /[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/, arr) { print arr[0] }' file.txt
```

---

## Regex in vim
In vim, regex is used for search (`/`) and substitution (`:%s`):

```vim
/[0-9]\+            " Find one or more digits (BRE in vim)
/\d\+               " Same using \d shorthand
/^\s*$              " Find blank lines

:%s/\bcolor\b/colour/g          " Whole-word replacement
:%s/\([0-9]\+\)/[\1]/g          " Wrap all numbers in brackets (BRE)
:%s/\v([0-9]+)/[\1]/g           " Same with \v (very magic - ERE-like mode)
```

Vim uses `\v` to enable "very magic" mode, which is similar to ERE:

```vim
:%s/\v(\d+)-(\d+)/\2-\1/g      " Swap two numbers separated by -
```

---

## Quick Reference Table

| Pattern | Meaning | Example |
|---------|---------|---------|
| `.` | Any single character | `c.t` → cat, cut, c1t |
| `^` | Start of line | `^Error` → line starts with Error |
| `$` | End of line | `\.log$` → ends with .log |
| `\b` | Word boundary | `\bcat\b` → cat but not cats |
| `[abc]` | One of a, b, c | `[aeiou]` → any vowel |
| `[^abc]` | Not a, b, or c | `[^0-9]` → not a digit |
| `[a-z]` | Range a to z | `[a-z]+` → lowercase word |
| `*` | Zero or more | `go*d` → gd, god, good |
| `+` | One or more (-E) | `go+d` → god, good |
| `?` | Zero or one (-E) | `colou?r` → color, colour |
| `{3}` | Exactly 3 (-E) | `[0-9]{4}` → 4 digits |
| `{2,5}` | 2 to 5 (-E) | `[a-z]{3,5}` → 3-5 letters |
| `\|` or `|` | Or (BRE `\|`, ERE `|`) | `cat\|dog` → cat or dog |
| `\(...\)` or `(...)` | Group | `(ab)+` → ab, abab |
| `\1` | Backreference | `\b(\w+) \1\b` → repeated word |