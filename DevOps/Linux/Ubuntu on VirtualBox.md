# Installing Ubuntu on VirtualBox — Full Desktop GUI

This guide walks through installing Ubuntu as a virtual machine using Oracle VM VirtualBox, so we end up with a complete Ubuntu desktop — full graphical interface, taskbar, application menu, and all — running inside a window on our Windows machine.

This is different from WSL, which only gives a terminal. With VirtualBox, Ubuntu runs as an entirely separate computer simulated inside our Windows machine, with its own screen, its own desktop, and full hardware emulation.

---

## What We Need Before Starting
- A Windows PC with at least **8 GB of RAM** (4 GB will be reserved for Ubuntu, 4 GB stays for Windows)
- At least **30 GB of free disk space**
- A reliable internet connection to download the software

---

## Step 1 — Download and Install VirtualBox
1. Go to [https://www.virtualbox.org](https://www.virtualbox.org) and click **Downloads**.
2. Under "VirtualBox platform packages", click **Windows hosts** to download the installer.
3. Run the downloaded `.exe` file and follow the installer steps. The defaults are fine — just keep clicking **Next** and then **Install**.
4. When prompted about network interfaces being reset briefly, click **Yes**.
5. Once installed, also download the **VirtualBox Extension Pack** from the same Downloads page (it adds USB 2.0/3.0 support and better display drivers). Open VirtualBox, go to **File → Tools → Extension Pack Manager**, click **Install**, and select the downloaded `.vbox-extpack` file.

---

## Step 2 — Download the Ubuntu ISO
An ISO file is a complete disk image — it's the same as a physical Ubuntu installation disc, just in file form. VirtualBox will use it to boot and install Ubuntu.

1. Go to [https://ubuntu.com/download/desktop](https://ubuntu.com/download/desktop).
2. Download the latest **Ubuntu LTS** release (LTS stands for Long-Term Support — it receives security updates for 5 years, making it the stable, recommended choice).
3. Save the `.iso` file somewhere easy to find (e.g., our Downloads folder). It is around 5 GB.

---

## Step 3 — Create a New Virtual Machine
Open VirtualBox and click **New** (the blue star-like icon in the toolbar).

### Name and operating system
- **Name**: Type anything, e.g. `Ubuntu`
- **Folder**: Leave as default (where VMs are stored on our disk)
- **ISO Image**: Click the dropdown, choose **Other**, and browse to the Ubuntu `.iso` file we downloaded
- VirtualBox should automatically detect **Type: Linux** and **Version: Ubuntu (64-bit)** — if not, set them manually
- Check **Skip Unattended Installation** — this lets us go through the Ubuntu installer ourselves, which is more educational and gives us more control
- Click **Next**

### Hardware (memory and CPU)
- **Base Memory (RAM)**: Set to **4096 MB** (4 GB). This gives Ubuntu enough room to run smoothly. Do not set it higher than half our total system RAM.
- **Processors**: Set to **2** CPUs. This lets Ubuntu use two of our processor cores.
- Click **Next**

### Virtual hard disk
- Select **Create a Virtual Hard Disk Now**
- Set the size to at least **25 GB** — **30 GB** is more comfortable if we plan to install software inside Ubuntu
- Leave the type as **VDI (VirtualBox Disk Image)**
- Click **Next**, then **Finish**

The VM now appears in the left panel of VirtualBox. We haven't installed Ubuntu yet — we've just set up the virtual hardware. The next steps boot from the ISO and install Ubuntu onto the virtual disk.

---

## Step 4 — Adjust Display Settings Before First Boot
Before starting the VM, let's give it more video memory so the desktop runs at a good resolution.

1. Select the VM in the left panel and click **Settings** (the orange gear icon).
2. Go to **Display**.
3. Set **Video Memory** to **128 MB** (drag the slider all the way to the right).
4. Under **Graphics Controller**, select **VMSVGA**.
5. Click **OK**.

---

## Step 5 — Install Ubuntu
Click the green **Start** arrow to boot the VM. A window opens — this is Ubuntu booting from the ISO.

### Going through the Ubuntu installer

1. **Welcome screen**: Select our language and click **Install Ubuntu**.

2. **Keyboard layout**: Choose our keyboard layout and click **Continue**.

3. **Updates and other software**:
   - Select **Normal installation** (includes a web browser, utilities, and basic apps).
   - Check **Download updates while installing Ubuntu** if our internet is fast.
   - Click **Continue**.

4. **Installation type**: Select **Erase disk and install Ubuntu**.
   > Don't worry — this only erases the **virtual disk** we created in Step 3. It cannot touch our real Windows files or drives. Click **Install Now**, then **Continue** to confirm.

5. **Where are we?**: Click our region on the map or type our city to set the timezone. Click **Continue**.

6. **Who are we?**:
   - Enter our name, a computer name (e.g. `ubuntu-vm`), and a username.
   - Set a password — we'll need this to log in and run `sudo` commands.
   - Leave **Require my password to log in** selected.
   - Click **Continue**.

7. Ubuntu will now install. This takes **5–15 minutes** depending on our machine. We'll see a slideshow while it works.

8. When installation finishes, click **Restart Now**. When prompted to "remove the installation medium", just press **Enter** — VirtualBox handles this automatically.

9. Ubuntu will boot and show a login screen. Enter our password.

**We now have a full Ubuntu desktop running in VirtualBox.**

---

## Step 6 — Install VirtualBox Guest Additions (Important)
Right now the desktop is functional but limited — the screen resolution may be low, copy-paste between Windows and Ubuntu won't work, and resizing the VM window won't resize the Ubuntu desktop. **Guest Additions** fixes all of this.

Guest Additions is a small package installed inside Ubuntu that lets it communicate better with VirtualBox.

1. With the Ubuntu VM running, go to the VirtualBox menu bar at the top and click **Devices → Insert Guest Additions CD image...**

   This mounts a virtual CD inside Ubuntu.

2. Ubuntu will likely show a notification asking if we want to run the software on the CD. Click **Run** and enter our password when prompted.

   If no notification appears:
   - Open the **Files** app (file manager) in Ubuntu.
   - Click on **VBox_GAs_...** in the left panel (the mounted CD).
   - Right-click in the folder and select **Open Terminal Here**.
   - Run:
     ```bash
     sudo bash VBoxLinuxAdditions.run
     ```

3. Wait for the installation to finish. When done, **reboot Ubuntu**:
   ```bash
   sudo reboot
   ```

4. After rebooting, we can now:
   - **Resize the VM window** — Ubuntu's desktop resolution follows automatically.
   - **Use full screen** — Press `Right Ctrl + F` (or go to **View → Full Screen Mode**) to make Ubuntu fill our entire monitor.
   - **Shared clipboard** — Go to **Devices → Shared Clipboard → Bidirectional** to copy and paste between Windows and Ubuntu.
   - **Drag and drop** — Go to **Devices → Drag and Drop → Bidirectional** to drag files between Windows and Ubuntu.

---

## Step 7 — Set Up a Shared Folder (Optional)
A shared folder lets us access files from our Windows machine directly inside Ubuntu, without needing to copy them.

1. Shut down Ubuntu (click the top-right corner of the desktop → Power → Shut Down).
2. In VirtualBox, select the VM and click **Settings → Shared Folders**.
3. Click the **+** icon on the right to add a folder.
4. Under **Folder Path**, browse to a Windows folder (e.g. `C:\Users\YourName\Documents`).
5. Check **Auto-mount** and **Make Permanent**.
6. Click **OK**, then start Ubuntu again.

The shared folder will appear in Ubuntu's file manager under `/media/sf_<foldername>`. If we can't access it, run:
```bash
sudo adduser $USER vboxsf
```
Then log out and log back in.

---

## Taking Snapshots — Saving Our VM State
One of VirtualBox's best features is **snapshots** — they save the entire current state of our VM so we can restore it later if something goes wrong (e.g., after a bad software install or a broken configuration).

**Take a snapshot:**
1. With the VM running or shut down, go to **Machine → Take Snapshot**.
2. Give it a name like `Fresh Ubuntu install` and click **OK**.

**Restore a snapshot:**
1. Shut down the VM.
2. In VirtualBox, click the hamburger menu (≡) next to the VM name → **Snapshots**.
3. Select the snapshot and click **Restore**.

A good habit is to take a snapshot right after getting Ubuntu set up the way we like it, before installing anything major.

---

## Common Issues
**The VM window is tiny and resolution is stuck low**
Install Guest Additions (Step 6) and make sure the Graphics Controller is set to VMSVGA (Step 4).

**Ubuntu is very slow**
- Make sure we  allocated enough RAM (at least 4 GB) and 2 CPUs in the VM settings.
- In VirtualBox Settings → Display, enable **3D Acceleration**.
- Close other applications on our Windows machine to free up resources.

**"VT-x/AMD-V hardware acceleration is not available" error**
This means hardware virtualization is disabled in our PC's BIOS. Restart our PC, enter the BIOS setup (usually by pressing `F2`, `F10`, `Del`, or `Esc` during startup), and enable **Intel VT-x** or **AMD-V** (also called **SVM Mode**). The exact location varies by motherboard.

**Shared clipboard not working**
Make sure Guest Additions is installed and set Devices → Shared Clipboard → Bidirectional while the VM is running.

**Black screen after reboot**
Try pressing `Right Ctrl + F` to toggle full screen, or go to **View → Virtual Screen 1 → Resize** to trigger a redraw.