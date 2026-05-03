# Disk Management — Partitioning, Formatting, and Mounting

Every Linux system admin eventually needs to add a new disk, resize a partition, or set up persistent storage. Whether we're adding a data drive to a server, setting up a VM's extra disk, or preparing storage for a database — these skills are essential. This guide covers partitioning with `fdisk`, formatting filesystems, and making mounts permanent via `/etc/fstab`.

> **WSL Note:** In WSL 2, the Linux filesystem runs inside a virtual hard disk (`.vhdx` file), so we can't partition the WSL disk itself. The concepts in this guide apply to real Linux machines, VMs, and cloud servers. We can still experiment in WSL by creating **loop devices** from files, which we'll show at the end.

---

## Understanding Disk Terminology
Before we touch any commands, let's get the vocabulary right.

#### Block devices
A **block device** is a storage device (hard drive, SSD, USB drive, virtual disk) that Linux interacts with in fixed-size blocks. They appear as files in `/dev/`:
- `/dev/sda` — first SATA/SCSI/virtual disk
- `/dev/sdb` — second disk
- `/dev/nvme0n1` — first NVMe (modern SSD) disk
- `/dev/vda` — virtual disk (in cloud VMs)

Partitions are numbered: `/dev/sda1`, `/dev/sda2`, `/dev/sdb1`, etc.

#### Partitions
A **partition** is a defined region of a disk. A disk can have multiple partitions, each acting as an independent storage unit. We partition disks to separate the OS, data, swap, etc.

#### Filesystem
A **filesystem** is the structure that organizes data on a partition — how files are stored, named, and retrieved. Common Linux filesystems:
- **ext4** — the default on Ubuntu/Debian, reliable and well-supported
- **xfs** — high performance, good for large files
- **btrfs** — advanced features (snapshots, compression)
- **swap** — special type used as virtual memory (not for files)
- **vfat/FAT32** — Windows-compatible (USB drives)

#### Mount point
A **mount point** is a directory where a filesystem is attached to the directory tree. When we mount `/dev/sdb1` at `/data`, everything in `/data` lives on that partition.

---

## Viewing Disk Layout
Before we change anything, let's understand what we have.

#### lsblk — Tree view of all block devices

```bash
lsblk
```

Output:

```
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0   50G  0 disk
├─sda1   8:1    0    1G  0 part /boot
├─sda2   8:2    0   47G  0 part /
└─sda3   8:3    0    2G  0 part [SWAP]
sdb      8:16   0  100G  0 disk
```

`sdb` has no partitions yet — it's a fresh disk.

To show filesystems:

```bash
lsblk -f
```

Output includes filesystem type, UUID, and mount point.

#### fdisk -l — List partition tables

```bash
sudo fdisk -l
```

Shows all disks and their partition tables with sizes and types.

#### blkid — Show block device UUIDs and types

```bash
sudo blkid
```

UUIDs (universally unique identifiers) are used in `/etc/fstab` to identify partitions reliably (device names like `/dev/sdb1` can change after reboot).

---

## Partitioning with fdisk
`fdisk` is the interactive partition editor. Let's walk through partitioning a fresh disk (`/dev/sdb`).

> **Warning:** Partitioning the wrong disk destroys data. Always double-check device names with `lsblk` first.

#### Launching fdisk

```bash
sudo fdisk /dev/sdb
```

We enter an interactive prompt. Type `m` for the menu of available commands:

```
Command (m for help): m

Help:
  g   create a new empty GPT partition table
  n   add a new partition
  p   print the partition table
  d   delete a partition
  w   write table to disk and exit
  q   quit without saving changes
```

#### Creating a partition table
Modern disks should use GPT (GUID Partition Table). Type `g` then Enter:

```
Command (m for help): g
Created a new GPT disklabel (GUID: ...)
```

#### Adding a partition
Type `n` to create a new partition:

```
Command (m for help): n
Partition number (1-128, default 1): 1
First sector (2048-..., default 2048): [Enter]    ← accept default
Last sector (+sectors or +size{K,M,G,T,P}): +50G  ← take first 50G
```

To use the entire disk for one partition, just press Enter for all defaults.

#### Reviewing the layout
Type `p` to print the current partition table before writing:

```
Command (m for help): p
Device       Start       End   Sectors  Size Type
/dev/sdb1     2048 104859647 104857600   50G Linux filesystem
```

#### Writing the changes
Type `w` to write the partition table and exit:

```
Command (m for help): w
The partition table has been altered.
Syncing disks.
```

**Nothing is written to disk until `w` is pressed.** If we make a mistake, `q` quits without saving.

#### parted — Alternative partitioning tool
`parted` is another partitioner with both interactive and non-interactive modes:

```bash
sudo parted /dev/sdb
```

Or in one command (useful in scripts):

```bash
sudo parted /dev/sdb mklabel gpt
sudo parted /dev/sdb mkpart primary ext4 0% 100%
```

---

## Formatting (Creating a Filesystem)
After partitioning, we must create a filesystem on the partition. This is called **formatting**. It erases any existing data.

#### mkfs.ext4 — Create an ext4 filesystem (recommended for Linux data)

```bash
sudo mkfs.ext4 /dev/sdb1
```

Output shows block size, inode count, and UUID. To add a label (a human-readable name):

```bash
sudo mkfs.ext4 -L mydata /dev/sdb1
```

Labels make it easier to identify partitions in `lsblk -f` and `/etc/fstab`.

#### Other filesystem types

```bash
sudo mkfs.xfs /dev/sdb1           # XFS filesystem
sudo mkfs.btrfs /dev/sdb1         # Btrfs filesystem
sudo mkfs.vfat /dev/sdb1          # FAT32 (Windows compatible)
sudo mkfs.ntfs /dev/sdb1          # NTFS (Windows compatible, needs ntfsprogs)
```

#### Creating swap

```bash
sudo mkswap /dev/sdb3             # Format as swap
sudo swapon /dev/sdb3             # Enable the swap
```

To see current swap usage:

```bash
swapon --show
free -h
```

---

## Mounting Filesystems
After formatting, we **mount** the filesystem at a directory to make it accessible.

#### Creating a mount point
The mount point is just a directory. It should be empty:

```bash
sudo mkdir -p /data
```

#### Mounting manually

```bash
sudo mount /dev/sdb1 /data
```

Now everything we write to `/data/` is stored on `/dev/sdb1`.

To verify:

```bash
df -h /data
lsblk
```

#### Mounting with options

```bash
sudo mount -o ro /dev/sdb1 /data          # Mount read-only
sudo mount -o remount,rw /dev/sdb1 /data  # Remount as read-write
```

Common mount options:
- `ro` — read-only
- `rw` — read-write (default)
- `noexec` — prevent executing files (security measure for `/tmp`)
- `nosuid` — ignore setuid bits (security)
- `noatime` — don't update file access time (performance improvement)

#### Unmounting
Always unmount before physically removing a drive or before modifying the filesystem:

```bash
sudo umount /data
# or by device:
sudo umount /dev/sdb1
```

If it says "device is busy," a process has a file open on that filesystem:

```bash
lsof /data           # Find which process has files open there
fuser -mv /data      # Another way to find processes
```

---

## Making Mounts Permanent with /etc/fstab
Manual mounts don't survive reboots. To mount a filesystem automatically at boot, we add it to `/etc/fstab` (filesystem table).

#### Understanding /etc/fstab

```bash
cat /etc/fstab
```

Each non-comment line has 6 fields:

```
<device>  <mount_point>  <type>  <options>  <dump>  <pass>
```

- **device** — device path (`/dev/sdb1`) or UUID (`UUID=...`) or label (`LABEL=mydata`)
- **mount_point** — where to mount it
- **type** — filesystem type (`ext4`, `xfs`, `swap`, `auto`)
- **options** — mount options (use `defaults` for standard)
- **dump** — backup flag (0=no backup, almost always 0)
- **pass** — filesystem check order at boot (0=skip, 1=root, 2=other)

#### Finding the UUID (preferred over device names)
Device names can change after adding/removing disks. UUIDs are stable:

```bash
sudo blkid /dev/sdb1
```

Output: `/dev/sdb1: UUID="a1b2c3d4-..." TYPE="ext4" LABEL="mydata"`

#### Adding an entry to /etc/fstab
Open with sudo (use `nano` or `vim`):

```bash
sudo nano /etc/fstab
```

Add a line at the bottom:

```
UUID=a1b2c3d4-e5f6-7890-abcd-ef1234567890  /data  ext4  defaults  0  2
```

For swap:

```
UUID=b2c3d4e5-...  none  swap  sw  0  0
```

#### Testing before rebooting
**Always test the fstab entry before rebooting** — a bad fstab can prevent the system from booting:

```bash
sudo mount -a
```

`mount -a` mounts all filesystems listed in `/etc/fstab` that aren't currently mounted. If it succeeds without error, our entry is correct.

To check:

```bash
df -h /data
```

#### fstab options reference

| Option | Meaning |
|--------|---------|
| `defaults` | rw, suid, dev, exec, auto, nouser, async |
| `ro` | Read-only |
| `noexec` | Don't allow program execution |
| `noatime` | Don't update access timestamps (faster) |
| `nofail` | Don't fail to boot if device isn't present |
| `auto` | Mount automatically at boot |
| `noauto` | Don't mount at boot (manual only) |
| `user` | Allow any user to mount |

The `nofail` option is very useful for external drives or network storage — it prevents a missing device from causing boot failure.

---

## Practical Example: Adding a Data Disk to a Server
Here's a complete walkthrough of adding a second disk to a Linux server:

```bash
# Step 1: Check what's there
lsblk

# Step 2: Partition the new disk (say it's /dev/sdb)
sudo fdisk /dev/sdb
# Inside fdisk: g (new GPT table) → n (new partition) → Enter Enter Enter → w (write)

# Step 3: Format it
sudo mkfs.ext4 -L appdata /dev/sdb1

# Step 4: Create mount point
sudo mkdir /appdata

# Step 5: Get the UUID
sudo blkid /dev/sdb1

# Step 6: Add to fstab
echo 'UUID=<paste-uuid-here>  /appdata  ext4  defaults,nofail  0  2' | sudo tee -a /etc/fstab

# Step 7: Test the mount
sudo mount -a

# Step 8: Verify
df -h /appdata

# Step 9: Set ownership so our app user can write to it
sudo chown -R appuser:appuser /appdata
```

---

## Loop Devices — Experimenting in WSL
In WSL, we can simulate disk management using **loop devices** — regular files used as if they were block devices:

```bash
# Create a 100MB file to act as our "disk"
dd if=/dev/zero of=~/disk.img bs=1M count=100

# Associate it with a loop device
sudo losetup /dev/loop0 ~/disk.img

# Now we can use it like a real disk
sudo mkfs.ext4 /dev/loop0
sudo mkdir /mnt/testdisk
sudo mount /dev/loop0 /mnt/testdisk

# Use it
echo "Hello from the loop device!" > /mnt/testdisk/test.txt

# Clean up
sudo umount /mnt/testdisk
sudo losetup -d /dev/loop0
rm ~/disk.img
```

This lets us practice partitioning and filesystem commands safely without risking real data.