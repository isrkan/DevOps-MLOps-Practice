# Linux Networking

Networking is at the heart of modern development work. Whether we're connecting to a remote server, testing an API, downloading a file, or deploying a web application, Linux networking tools are indispensable. This guide covers essential networking concepts and commands — from viewing our network configuration to mastering SSH for remote access.

---

## Networking Concepts
Before diving into commands, let's make sure we understand the key concepts.

#### IP addresses
An **IP address** is a unique identifier for a device on a network. There are two types:
- **IPv4** — 4 numbers 0–255 separated by dots: `192.168.1.100`
- **IPv6** — 8 groups of 4 hex digits: `2001:db8::1`

Special addresses:
- `127.0.0.1` (or `::1` in IPv6) — **loopback** address, refers to our own machine ("localhost"). When we send traffic here, it never actually leaves our computer — the kernel routes it right back to us. This is incredibly useful for testing local services.
- `0.0.0.0` — means "all network interfaces" when binding a service. If a web server "listens on `0.0.0.0:8080`," it accepts connections coming in on *any* of the machine's network interfaces. Listening on `127.0.0.1:8080` instead would only accept connections from the machine itself.
- Private IP ranges like `192.168.x.x`, `10.x.x.x`, and `172.16.x.x`–`172.31.x.x` — these are reserved for use inside private networks (like our home Wi-Fi) and are not routable on the public internet. That's why our home computer and our friend's home computer can both have the same `192.168.1.100` address without any conflict.

#### Ports
A **port** is a number (1–65535) that identifies a specific service on a machine. IP addresses get us to the machine; ports get us to the right service on that machine.

Ports are split into three ranges by convention:
- **0–1023** — *well-known ports* reserved for standard services. Binding to these typically requires root privileges on Linux, which prevents random user programs from impersonating system services like SSH or HTTP.
- **1024–49151** — *registered ports* assigned to specific applications (like `3306` for MySQL).
- **49152–65535** — *ephemeral ports* used temporarily by client connections.

Common ports to know:
- `22` — SSH
- `80` — HTTP (unencrypted web)
- `443` — HTTPS (encrypted web)
- `3306` — MySQL database
- `5432` — PostgreSQL database
- `6379` — Redis
- `8080`, `8000`, `8888` — common development server ports

#### TCP vs UDP
Most network traffic uses one of these two "transport" protocols. The choice depends on whether we value accuracy or speed.
- **TCP** (Transmission Control Protocol) — TCP ensures every single piece of data arrives correctly and in the right order. It starts with a "three-way handshake" to establish a connection. If a packet goes missing, TCP notices and asks the sender to send it again. Used for HTTP, email, SSH and databases. Has handshake and error correction. We wouldn't want a website to load with missing text or a database to skip a row.
- **UDP** (User Datagram Protocol) — UDP sends data as fast as possible without checking if it actually arrived or stayed in order. There is no connection setup and no error correction. It just "streams" the data. If a packet is lost, it’s gone forever. Used for DNS, live streaming, video calls, games. In a video call, it's better to have a tiny momentary glitch than to pause the entire live conversation to recover one lost frame.

---

## Viewing Network Information

#### ip addr — Show network interfaces and IP addresses
`ip addr` (or the shorthand `ip a`) shows all our network interfaces and their assigned IP addresses. A *network interface* is the software representation of a physical or virtual connection to a network — every Ethernet port, Wi-Fi adapter, or virtual network adapter shows up as an interface here.

```bash
ip addr
```

Output:

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536
    link/loopback 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 52:54:00:ab:cd:ef
    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
    inet6 fe80::5054:ff:feab:cdef/64 scope link
```

Key information:
- `lo` — loopback interface (always `127.0.0.1`)
- `eth0` — our main network interface (may also be `ens3`, `enp0s3`, `wlan0` depending on hardware)
- `inet 192.168.1.100/24` — our IPv4 address with subnet mask (`/24` = `255.255.255.0`)

#### ip route — Show the routing table
The routing table tells our system where to send network traffic. When our machine wants to send a packet, it consults this table to decide which interface to send it out of and which next-hop router (if any) should receive it.

```bash
ip route
```

Output:

```
default via 192.168.1.1 dev eth0
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100
```

The `default` line shows our **gateway** — the router that handles traffic going outside our local network.

#### hostname -I — Quick IP address lookup
For a quick summary of our IP addresses without all the extra output:

```bash
hostname -I
```

This prints just the IP addresses, one per line — useful in scripts.

#### ifconfig — The legacy interface command
`ifconfig` is the older tool (from `net-tools` package). We'll see it in older tutorials and some distributions:

```bash
ifconfig
```

It's not installed by default on modern Ubuntu. The modern replacement is `ip addr`. We can install it if needed:

```bash
sudo apt install net-tools
```

---

## Testing Connectivity
When something on the network isn't working, the first question is always: "where exactly is it broken?" The tools below help us systematically narrow that down.

#### ping — Test if a host is reachable
`ping` sends small test packets to a host and reports back. It's our first tool for testing network connectivity:

```bash
ping google.com
```

By default on Linux, `ping` runs forever — press `Ctrl+C` to stop. To send only 4 packets:

```bash
ping -c 4 google.com
```

Output shows the **round-trip time (RTT)** — how long each packet takes to go there and back. This helps us detect network latency.

```bash
ping -c 4 127.0.0.1      # Ping ourselves (should always work)
ping -c 4 192.168.1.1    # Ping our router
ping -c 4 8.8.8.8        # Ping Google's DNS server
```

If ping to `8.8.8.8` works but `google.com` doesn't, we have a DNS problem. If neither works, we have a connectivity problem. Latency is measured in milliseconds (ms); lower numbers indicate a faster, more responsive connection. High latency or packet loss (packets sent but not received) usually points to physical cable issues, interference, or network congestion.

#### traceroute — Trace the network path
`traceroute` shows the route packets take to reach a destination, hop by hop. This is enormously useful for figuring out *where* on the network path a problem lies — not just whether the destination is reachable, but at which intermediate router things start to break.

```bash
traceroute google.com
```

Install if needed:

```bash
sudo apt install traceroute
```

Each line shows one "hop" (router/gateway) along the path, with its IP and response time. Useful for diagnosing where a connection is failing or slowing down. If a hop shows asterisks (`* * *`), it means that specific router is not responding to the trace request, often due to security settings. In WSL, the first hop is typically the internal virtual gateway between the Linux environment and the Windows host.

#### DNS resolution — nslookup and dig
**DNS** (Domain Name System) translates domain names (like `google.com`) into IP addresses. When we type `google.com` into a browser, our machine first asks a DNS server "what's the IP for `google.com`?" before it can connect.

`nslookup` queries DNS:

```bash
nslookup google.com
```

`dig` provides more detailed DNS information:

```bash
dig google.com
```

```bash
dig google.com MX          # Look up mail server records
dig @8.8.8.8 google.com    # Query a specific DNS server
dig +short google.com      # Just the IP addresses
```

---

## Checking Ports and Connections
Once a service is running on our machine, we often need to verify it's actually listening on the expected port — or, conversely, find out what's already using a port we want.

#### ss — Socket statistics (modern tool)
`ss` shows network sockets and connections. A **socket** is the OS abstraction for a network endpoint — basically a combination of an IP address and a port number that a program is using to send or receive data. The most useful form is to see what ports are listening for incoming connections:

```bash
ss -tuln
```

Flags:
- `-t` — TCP sockets
- `-u` — UDP sockets
- `-l` — listening (waiting for connections)
- `-n` — show numeric port numbers (don't resolve service names)

Output:

```
Netid  State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port
tcp    LISTEN  0       128     0.0.0.0:22           0.0.0.0:*
tcp    LISTEN  0       80      0.0.0.0:80           0.0.0.0:*
```

This tells us SSH (port 22) and HTTP (port 80) are listening on all interfaces.

To see established connections too:

```bash
ss -tu
```

#### netstat — The legacy socket tool
`netstat` is the older equivalent of `ss`:

```bash
netstat -tuln
```

Install with `sudo apt install net-tools` if needed.

#### lsof — List open files and network connections
`lsof` (list open files) can show us what's using a specific port:

```bash
sudo lsof -i :80
```

This shows all processes listening on port 80. Very useful when a service fails to start because its port is already taken.

```bash
sudo lsof -i :8080
sudo lsof -i TCP:443
```

---

## Downloading Files
These tools fetch data from URLs from the command line. They're indispensable in scripts, server provisioning, API testing, and any situation where we don't want to (or can't) open a browser.

#### curl — Transfer data from URLs
`curl` is an extremely versatile tool for making HTTP requests and downloading files. It's one of the most-used tools in DevOps and scripting. Despite its name suggesting downloads, `curl` actually supports many protocols (HTTP, HTTPS, FTP, SFTP, and more) and can both fetch *and* send data, making it equally useful for testing APIs as for downloading files.

To fetch the content of a URL and print it:

```bash
curl https://example.com
```

By default, `curl` writes the response body to standard output, which is perfect for piping into other commands or viewing quickly.

To save the output to a file (lowercase `-o` with a custom filename):

```bash
curl -o mypage.html https://example.com
```

To save with the same filename as on the server (uppercase `-O`):

```bash
curl -O https://example.com/archive.tar.gz
```

To follow redirects (important for many URLs that redirect to the actual content):

```bash
curl -L https://short.url/link
```

To send HTTP headers (e.g., for API authentication):

```bash
curl -H "Authorization: Bearer mytoken" https://api.example.com/data
```

Headers carry metadata about the request — authentication tokens, content types, expected response formats, and so on. Most modern APIs require at least an `Authorization` header.

To make a POST request with JSON data:

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"name": "Alice", "age": 30}' \
     https://api.example.com/users
```

Here, `-X POST` sets the HTTP method (the default is `GET`), `-H` sets the content type so the server knows we're sending JSON, and `-d` provides the request body. This is the bread and butter of API testing from the command line.

To show only the HTTP response status code (handy for health checks):

```bash
curl -o /dev/null -s -w "%{http_code}\n" https://example.com
```

Breaking this down: `-o /dev/null` discards the body, `-s` silences the progress meter, and `-w` writes a custom output format — in this case, just the HTTP status code (200, 404, 500, etc.). This kind of one-liner is gold in monitoring scripts.

To include headers in the output (useful for debugging):

```bash
curl -i https://example.com
```

`curl` is indispensable for testing REST APIs, downloading files in scripts, and debugging web services.

#### wget — Download files
`wget` is designed specifically for downloading files, including large ones and recursive downloads:

```bash
wget https://example.com/file.tar.gz
```

By default, `wget` saves to the current directory using the filename from the URL and shows a nice progress bar.

To save to a specific filename:

```bash
wget -O archive.tar.gz https://example.com/file.tar.gz
```

To download in the background (good for huge files when we want to keep using the terminal):

```bash
wget -b https://example.com/large-file.iso
```

Output is logged to `wget-log` in the current directory so we can check progress later.

To resume an interrupted download:

```bash
wget -c https://example.com/large-file.iso
```

The `-c` (continue) flag picks up where a previous download left off, instead of starting from scratch.

To download a website recursively (mirror), useful for archiving documentation:

```bash
wget -r https://example.com/
```

This follows links and downloads every page on the site. Use with care — it can put significant load on the target server.

**curl vs wget:** `curl` is more powerful for API work and supports more protocols and HTTP methods. `wget` is simpler for straightforward file downloads and supports recursive downloading. Both are excellent tools.

---

## SSH — Secure Remote Access
**SSH** (Secure Shell) is the standard protocol for securely accessing remote Linux machines over a network. When we work with cloud servers, virtual machines, or remote systems, SSH is how we connect to them. SSH replaced older insecure protocols like Telnet and rsh by encrypting all traffic — including passwords and command output — using strong cryptography. It's so foundational that almost every Linux server comes with an SSH server installed and running by default.

### Basic SSH Connection
To connect to a remote server:

```bash
ssh username@server-ip-or-hostname
```

For example:

```bash
ssh alice@192.168.1.200
ssh alice@myserver.example.com
```

On first connection, SSH will ask us to verify the server's identity (fingerprint). Type `yes` to accept and remember it. After that, we'll be prompted for the user's password. The fingerprint gets stored in `~/.ssh/known_hosts`, and on subsequent connections, SSH silently checks that the server still presents the same key — protecting us from "man-in-the-middle" attacks where an attacker tries to impersonate the server. If the key ever changes unexpectedly, SSH will refuse to connect and warn us loudly. After accepting the fingerprint, we'll be prompted for the user's password.

Once connected, we're in a shell on the remote machine — every command we type runs there. The local terminal is just a window into a session that's actually executing on the remote server.

To disconnect, type `exit` or press `Ctrl+D`.

To connect on a non-standard port (default is 22):

```bash
ssh -p 2222 alice@myserver.example.com
```

Many sysadmins move SSH off port 22 to reduce the volume of automated brute-force login attempts (though this is more about reducing log noise than real security).

### SSH Key Authentication — The Secure and Convenient Way
Typing a password every time we SSH is inconvenient, and passwords are less secure than key pairs because they can be guessed, phished, or brute-forced. **SSH key authentication** uses cryptographic key pairs based on public-key cryptography:
- **Private key** — stays on our machine, never shared (keep it secret!). Anyone who has this can log in as us.
- **Public key** — installed on the server, can be freely distributed. Mathematically derived from the private key but cannot be used to reconstruct it.

The way it works: when we connect, the server sends a challenge that can only be answered correctly by someone with the private key. We never actually send the private key over the network — the math proves we have it without exposing it.

#### Step 1: Generate a key pair
Generate a new Ed25519 key pair (the modern, recommended algorithm — faster and more secure than older RSA keys):

```bash
ssh-keygen -t ed25519 -C "alice@myworkstation"
```

The `-t ed25519` flag specifies the key type (Ed25519 is currently the best general-purpose choice). The `-C` flag adds a comment to identify the key, which is helpful when we have multiple keys and need to tell them apart in a server's `authorized_keys` file. We'll be asked for a file location (press `Enter` to use the default `~/.ssh/id_ed25519`) and optionally a passphrase for extra security. A passphrase encrypts the private key on disk so that even if someone steals the file, they can't use it without knowing the passphrase — strongly recommended for important keys.

This creates:
- `~/.ssh/id_ed25519` — our private key (protect this! Permissions are auto-set to 600 so only we can read it.)
- `~/.ssh/id_ed25519.pub` — our public key (safe to share — this goes on every server we want to log into.)

#### Step 2: Copy the public key to the server
The easiest way is using `ssh-copy-id`:

```bash
ssh-copy-id alice@192.168.1.200
```

This securely copies our public key to `~/.ssh/authorized_keys` on the server and sets the correct permissions automatically (which matters — SSH will refuse to use the key if the permissions are too loose). We'll need to enter the password this one last time, after which key authentication takes over.

Alternatively, we can do it manually if `ssh-copy-id` isn't available:

```bash
cat ~/.ssh/id_ed25519.pub | ssh alice@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

This pipes the public key over an SSH connection, creates the `.ssh` directory if needed, and appends the key to `authorized_keys`. Note the `>>` (append) — using `>` would overwrite any existing keys, kicking out other devices.

#### Step 3: Connect without a password
Now we can SSH without a password:

```bash
ssh alice@192.168.1.200
```

If the connection still asks for a password, common issues include incorrect permissions on `~/.ssh` or `~/.ssh/authorized_keys` on the server (they should be `700` and `600` respectively), or the public key not being properly appended.

### The SSH Config File — Simplifying Connections
If we connect to multiple servers, typing the full connection details every time gets tedious. The `~/.ssh/config` file lets us define shortcuts. SSH automatically reads this file before every connection, so once configured, we can refer to servers by short, memorable names.

```bash
nano ~/.ssh/config
```

Add entries like this:

```
Host myserver
    HostName 192.168.1.200
    User alice
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host devserver
    HostName dev.example.com
    User deploy
    Port 2222
    IdentityFile ~/.ssh/deploy_key
```

Each block defines a "host alias." `Host myserver` is the nickname we'll use; `HostName` is the actual address; `User`, `Port`, and `IdentityFile` configure how to connect. We can have as many entries as we like, plus wildcards like `Host *.example.com` for groups of servers.

Now we can connect with just:

```bash
ssh myserver
ssh devserver
```

This same config is also used by `scp`, `sftp`, `rsync`, and Git when fetching from SSH URLs, so a single setup benefits all our tools.

Make sure the config file has the right permissions (otherwise SSH may ignore it for security reasons):

```bash
chmod 600 ~/.ssh/config
```

### Copying Files with SCP
**SCP** (Secure Copy Protocol) lets us copy files between our local machine and a remote server securely. It works over SSH, so it uses the same connection, the same port (22), and the same authentication (password or SSH key) — no extra setup needed if SSH already works. If we can `ssh` into a server, we can `scp` to and from it.

The general syntax follows the same pattern as the regular `cp` command, but with `user@server:` added to indicate the remote side:

```
scp [options] [source] [destination]
```

Either source or destination can be remote — the other is local. The colon after the server address is what tells `scp` "this is a remote path, not a local file with a weird name."

#### Copy a local file to a remote server
```bash
scp local_file.txt alice@server:/home/alice/
```

This copies `local_file.txt` from our machine into the `/home/alice/` directory on the server. The `:` separates the server address from the remote path.

#### Copy a file from the remote server to our machine
```bash
scp alice@server:/home/alice/report.txt ./
```

The `./` means "put it here, in my current local directory." We can also specify a full local path like `~/Downloads/` or `/tmp/`.

#### Copy a whole directory (use -r for recursive)
```bash
scp -r local_dir/ alice@server:/home/alice/
```

The `-r` flag means "recursive" — it copies the directory and everything inside it. Without `-r`, `scp` will refuse to copy a directory and print an error.

#### Copy between two remote servers
We can copy directly from one remote server to another without downloading the file first to our local machine:
```bash
scp alice@server1:/home/alice/file.txt bob@server2:/home/bob/
```

By default, the data flows through our local machine; add `-3` to force this behavior explicitly, or omit it and let `scp` try a direct server-to-server transfer if possible.

#### Use a non-standard SSH port
If the server's SSH runs on a port other than 22, use `-P` (capital P):
```bash
scp -P 2222 local_file.txt alice@server:/home/alice/
```

Note the inconsistency: `ssh` uses lowercase `-p` for port, but `scp` uses uppercase `-P`. This trips up almost everyone at some point.

#### Useful scp options
- `-r` — copy directories recursively
- `-P <port>` — connect on a specific port
- `-i <key>` — use a specific SSH private key file
- `-C` — compress data during transfer (useful on slow connections)
- `-q` — quiet mode, suppress progress output

### Transferring Files Interactively with SFTP
**SFTP** (SSH File Transfer Protocol) is an interactive file transfer tool that also works over SSH. While `scp` is a one-shot command (run it, it copies, it exits), `sftp` opens a session where we can browse the remote filesystem, navigate directories, and transfer multiple files — more like using a file manager over the command line.

Think of `sftp` as an interactive session where we issue commands on both sides (local and remote) without disconnecting between them.

#### Opening an SFTP session
```bash
sftp alice@server
```

After connecting, we get an `sftp>` prompt. We are now in the SFTP session — commands we type here run against the remote server until we exit.

#### Navigating inside an SFTP session
Remote side (the server) — these work like normal shell commands:
```bash
ls                        # List files on the remote server
pwd                       # Show current remote directory
cd /home/alice/projects   # Change remote directory
```

Local side (our machine) — prefix commands with `l` to operate locally:
```bash
lls                       # List files on our local machine
lpwd                      # Show current local directory
lcd ~/Downloads           # Change local directory
```

This dual-context system is what makes SFTP powerful: we can `cd` into the right remote directory, `lcd` into the right local directory, and then transfer files between them with simple `get`/`put` commands.

#### Downloading files from the server
```bash
get report.txt            # Download a single file to our current local directory
get report.txt ~/docs/    # Download and save to a specific local path
get -r projects/          # Download a whole directory (-r for recursive)
```

#### Uploading files to the server
```bash
put local_file.txt        # Upload a file to the current remote directory
put local_file.txt /home/alice/docs/   # Upload to a specific remote path
put -r local_dir/         # Upload a whole directory
```

#### Other useful SFTP commands
```bash
mkdir backup              # Create a directory on the remote server
rm old_file.txt           # Delete a file on the remote server
rename old.txt new.txt    # Rename a file on the remote server
exit                      # Close the SFTP session (also: quit or bye)
```

#### Exiting the session
```bash
exit
```

#### SCP vs. SFTP — which to use?
Both use SSH and are equally secure. The difference is in how we use them:

| | `scp` | `sftp` |
|---|---|---|
| **Style** | Single command, then done | Interactive session |
| **Best for** | Scripting, quick one-off transfers | Browsing and transferring multiple files |
| **Can browse remote files** | No | Yes |
| **Works in scripts** | Yes | Less convenient |

Use `scp` when we know exactly what to copy and want to do it in one command. Use `sftp` when we want to explore the remote filesystem first or transfer several files in one session.

### Efficient Syncing with rsync
**rsync** is more efficient than SCP for transferring files because it only transfers the changed parts of files. If we sync a 1 GB file and only a few bytes have changed since last time, `rsync` figures that out and transfers just the differences — saving enormous amounts of time and bandwidth on incremental backups or repeated deployments.

```bash
rsync -avz local_dir/ alice@server:/home/alice/remote_dir/
```

Flags:
- `-a` — archive mode: preserves permissions, timestamps, symlinks, etc.
- `-v` — verbose output, lists each file as it's transferred
- `-z` — compress data during transfer (great on slow connections, may not help much on fast LANs)

Note the trailing slash on `local_dir/` — this matters! With the trailing slash, rsync copies the contents of `local_dir` into `remote_dir`. Without it, it copies the directory itself, ending up with `remote_dir/local_dir/`. This is one of the most common rsync gotchas.

To sync from server to local (just swap source and destination):

```bash
rsync -avz alice@server:/home/alice/data/ ./local_data/
```

To preview what would be synced without doing it (dry run):

```bash
rsync -avz --dry-run local_dir/ alice@server:/path/
```

The `--dry-run` flag is invaluable for verifying our command before unleashing it on real data — especially when combined with `--delete` (which removes files at the destination that no longer exist at the source — powerful but dangerous).

---

## Firewall with ufw
**ufw** (Uncomplicated Firewall) is Ubuntu's user-friendly frontend for managing firewall rules. It sits on top of `iptables` (the underlying Linux kernel firewall), which is famously complex, and makes common firewall tasks simple. A firewall controls which network traffic is allowed in or out of our machine, and is essential for any server that's exposed to the internet.

#### Checking firewall status
To see if ufw is active and list current rules:

```bash
sudo ufw status
```

If ufw is inactive, no rules are being enforced — the firewall isn't blocking anything. Active means rules are being applied.

#### Enabling the firewall
Before enabling, make sure we allow SSH first (otherwise we'll lock ourselves out of a remote server!). This is the cardinal rule of remote firewall management — enabling a firewall that blocks SSH while we're connected over SSH will instantly disconnect us, and we won't be able to get back in:

```bash
sudo ufw allow 22
sudo ufw enable
```

By default, ufw denies all incoming connections and allows all outgoing connections — a sensible secure starting point. We then explicitly open the ports we want to expose.

#### Allowing services and ports
To allow a service by name (ufw knows common services from `/etc/services`):

```bash
sudo ufw allow ssh        # Same as allowing port 22
sudo ufw allow http       # Port 80
sudo ufw allow https      # Port 443
```

Using service names instead of port numbers makes our rule list more readable later.

To allow a specific port number:

```bash
sudo ufw allow 8080
```

To allow a port with a specific protocol (otherwise ufw allows both TCP and UDP):

```bash
sudo ufw allow 80/tcp
sudo ufw allow 53/udp
```

To allow a port range:

```bash
sudo ufw allow 8000:9000/tcp
```

To allow traffic only from a specific IP address — useful for restricting database access to a known application server, for instance:

```bash
sudo ufw allow from 192.168.1.100
```

#### Denying and deleting rules
To deny a port (explicitly block it, useful when our default policy is "allow"):

```bash
sudo ufw deny 23        # Block Telnet
```

To delete a rule:

```bash
sudo ufw delete allow 8080
```

Or by rule number (first run `sudo ufw status numbered` to see the numbers, then delete by number — easier when rules are complex):

```bash
sudo ufw delete 3
```

#### Disabling the firewall

```bash
sudo ufw disable
```

This stops ufw from enforcing rules — but the rules themselves are remembered, so re-enabling it restores them.

---

## /etc/hosts — Local DNS Overrides
The `/etc/hosts` file is a simple text file that maps hostnames to IP addresses locally, bypassing DNS. It's the original "DNS" — predating the actual DNS system — and it's still consulted before DNS by default, so entries here take precedence over anything DNS returns. The order in which Linux checks name-resolution sources is configured in `/etc/nsswitch.conf`, where `hosts: files dns` means "look at `/etc/hosts first`, then ask DNS."

```bash
cat /etc/hosts
```

Default contents:

```
127.0.0.1    localhost
::1          localhost ip6-localhost ip6-loopback
127.0.1.1    hostname
```

These default entries are why typing `localhost` in a browser always works — it's resolved here, not via DNS.

We can add our own entries for development:

```bash
sudo nano /etc/hosts
```

Add a line like:

```
192.168.1.200    myserver.local
127.0.0.1        myapp.dev
```

Now `ssh myserver.local` or `curl http://myapp.dev` resolves to the specified IP without needing a real DNS entry. This is great for local development environments.