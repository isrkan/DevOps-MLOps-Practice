# Linux for windows users

For many developers who are primarily Windows users, integrating Linux into their workflow can be highly beneficial. Linux environments offer powerful tools, stability, and seamless compatibility with many development and machine learning tools. We will provides an overview of two popular ways to run Linux on a Windows machine: **Windows subsystem for Linux (WSL)** and **Oracle VM VirtualBox**.

As a Windows user, we might want to run Linux for its many advantages in development workflows, especially if we are dealing with tasks like server-side programming, AI systems or containerized environments. There are two primary ways to achieve this: WSL or Oracle VM VirtualBox. Both methods allow us to use Linux tools and commands, but each has its specific use cases, strengths, and drawbacks.

## Windows subsystem for Linux (WSL)
WSL is a compatibility layer developed by Microsoft that enables us to run a native Linux kernel directly on Windows. WSL allows us to use Linux distributions (such as Ubuntu, Debian, or Fedora) side-by-side with our Windows environment, without the need for dual-booting or virtualization. **WSL 2**, the latest version, introduces a full Linux kernel, providing better system compatibility and performance compared to WSL 1.

### Installation
1. **Enable WSL on Windows**: Open **PowerShell** as administrator and run:
     ```bash
     wsl --install
     ```

    This command installs the WSL feature and downloads the default Linux distribution (usually Ubuntu).
2. **Install a specific Linux distribution**: After installing WSL, we can install other Linux distributions via the Microsoft Store (e.g., Ubuntu, Debian, Kali Linux).
3. **Set WSL 2 as the default version**: To ensure we are using the improved WSL 2, run:
     ```bash
     wsl --set-default-version 2
     ```
4. **Check for WSL version**: To check if **WSL** is installed and enabled on our Windows machine, type the following command:
     ```bash
     wsl --list --verbose
     ```

     If WSL is installed, it will list the installed distributions along with their state and version. If WSL is not installed, we may receive an error message or an empty list. If Ubuntu or Debian appears in the list, it means we have it installed under WSL.

### Key features
- **Native Linux on Windows**: WSL runs a full Linux kernel, offering system compatibility. With **WSL 2**, GPU acceleration support (via CUDA on NVIDIA cards) makes it viable for ML tasks.
- **Lightweight**: WSL doesn't require the overhead of a full virtual machine. We only install the necessary components to run Linux distributions.
- **Windows/Linux integration**: We can access our Windows files from within Linux and vice versa (`/mnt/c/` for Windows files inside WSL), making file transfers between systems fast and straightforward. We can switch between Windows and Linux terminals without needing to reboot or run a virtual machine. We can also execute Windows programs from the Linux terminal and Linux programs from Windows, providing a hybrid environment for mixed workflows.
- **Low resource consumption**: Minimal CPU and memory usage compared to a full virtual machine.
- **Fast start-up**: WSL launches instantly, unlike a virtual machine that requires time to boot.

### Disadvantages of WSL
- **Limited system control**: WSL runs a managed Linux environment. We don't have full control over the system, unlike a standalone Linux installation or virtual machine.
- **No full GUI support** (WSL 1): Earlier versions of WSL had no support for GUI applications. WSL 2 supports GUI apps but still requires configuration.
- **Hardware limitations**: Some system-level tasks, like kernel module management, are restricted in WSL since the environment is virtualized. Tasks that rely on hardware (e.g., direct access to GPUs without specific support) are harder to configure.


## Oracle VM VirtualBox
Oracle VM VirtualBox is a free, open-source virtualization tool that allows users to run multiple operating systems on a single physical machine. It enables us to create virtual machines (VMs) that simulate entire hardware environments, including processor, memory, storage, and network devices. VirtualBox allows Windows users to run full Linux distributions as guest operating systems.

### Installation
1. **Download and install VirtualBox**:  Download VirtualBox from the official site and follow the installation steps for Windows.   
2. **Download a Linux ISO**: Choose a Linux distribution (e.g., Ubuntu) and download its ISO image from the official website.
3. **Create a virtual machine**: Open VirtualBox and create a new VM, specifying Linux as the OS and configuring system resources (RAM, CPU, disk space). Install the Linux distribution using the ISO image.
4. **Install guest additions**: To improve integration between Windows and Linux, install **VirtualBox Guest Additions**, which enhances performance, file sharing, and screen resolution.

### Key features
- **Complete virtualization**: VirtualBox runs a fully virtualized Linux environment with full hardware support, including kernel access, allowing us to perform system-level operations.
- **Snapshot feature**: We can take "snapshots" of the VM’s state and restore it later, making it easy to revert to a previous configuration if something breaks during development.
- **Linux distribution**: We can install any Linux distribution, whether it’s Ubuntu, CentOS, Fedora, or even experimental systems.
- **GUI support**: We can run Linux desktop environments like GNOME or KDE and Linux GUI applications easily.
- **Cross-platform**: VirtualBox can run Linux, Windows, macOS, and other operating systems, making it versatile for testing and development.
- **Isolation**: VMs are isolated from the host system, which is great for testing, running servers, or sandboxing risky tasks. With full control over the Linux environment, VirtualBox allows backend developers to run production-like servers.

### Disadvantages of VirtualBox
1. **Resource intensive**: Running a virtual machine consumes significant CPU, RAM, and disk space since we are running two operating systems simultaneously. This can be challenging for systems with limited resources.
2. **Slower performance**: VM performance tends to be slower than running Linux natively or in WSL due to the overhead of virtualization.
3. **More setup time**: Setting up VirtualBox, installing a Linux distribution, and configuring shared resources (files, network) take more time compared to WSL.

---

## WSL vs. VirtualBox: Which to Choose?

| Feature | WSL | VirtualBox |
| ------- | --- | ---------- |
| **Resource usage** | Low | High |
| **Performance** | Faster | Slower due to VM overhead |
| **Ease of installation** | Simple | More setup required |
| **Hardware access** | Limited (depends on WSL 2 features) | Full hardware access |
| **GUI support** | Limited (WSL 2 supports GUI apps) | Full GUI (runs full desktop environment) |
| **Data science/ML tools** | Easy setup | More flexible but resource-intensive |
| **System control** | Limited system control | Full system control |
| **Snapshot support** | No | Yes (useful for backups) |

### When to Choose WSL
- If we need **quick and easy access** to Linux tools while working on a primarily Windows-based system.
- If we are looking for **low overhead** and **fast startup**, especially for running command-line tools, servers, and development environments.

### When to Choose VirtualBox
- If we need **full control** over a Linux environment, including kernel access and hardware features.
- If we are working on projects that require **isolated environments** or if we are experimenting with multiple Linux distributions.
- If we need to run a **complete Linux desktop** for development and GUI-based applications.