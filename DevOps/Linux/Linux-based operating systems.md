# Linux-based operating systems

Linux-based operating systems are open-source, flexible, and customizable platforms widely used in various fields such as software development and data science. These systems are popular in enterprise and academic environments due to their stability, security, and ability to work on different hardware.

#### Unix-like
The term Unix-like refers to operating systems that behave and function similarly to the original Unix system. Unix is a very old operating system that influenced many modern operating systems, including Linux. Linux is considered "Unix-like" because it shares many features, commands, and structure with Unix, but it's not exactly the same. Most commands and tools we would find in Unix systems can also be found in Linux, making Linux familiar to users who have worked with Unix.


## Linux distributions
A Linux distribution (or Linux distro) is an operating system that’s built around the Linux kernel. It comes with the necessary software, utilities, and tools to help users interact with their computer and run applications. Different distributions customize this core with different user interfaces, package management systems, and software choices to serve various needs.

#### Popular Linux distributions
1. **Ubuntu**: Ubuntu is one of the most user-friendly and widely used Linux distributions, based on Debian, offering a smooth user experience with an intuitive graphical user interface. It is known for its strong community support, frequent updates, and vast library of available software. It’s especially popular in cloud environments, enterprise servers, and as a development platform for web applications, data science, and ML projects.
   - **Software and package management**: Ubuntu has access to a vast repository of software through its package management system, **APT**. Installing and managing software (e.g., Python, R, TensorFlow, Docker) is straightforward with commands like `apt install`. It supports a wide range of development tools and libraries essential for modern tech professionals.
   - **Compatibility with tools for data science and backend development**: Ubuntu is known for its strong compatibility with the tools and frameworks commonly used in these fields.
      - Ubuntu makes it easy to install and manage multiple versions of Python, R, and their associated libraries using `pip`, `conda`, and `apt`.
      - Tools like Hadoop, Spark, and Dask run smoothly on Ubuntu, enabling large-scale data processing.
      - Ubuntu provides robust support for ML frameworks like TensorFlow, PyTorch, Keras, and more. Installing GPU-accelerated versions of these libraries is straightforward with tools like NVIDIA’s CUDA and cuDNN, making Ubuntu ideal for training complex models.
      - Ubuntu integrates seamlessly with modern containerization tools like Docker and orchestration systems like Kubernetes.
      - Ubuntu is widely used in both cloud and on-premise servers. Cloud providers like AWS, GCP and Azure offer Ubuntu as a preferred image for deploying services. It’s highly compatible with popular web servers like Apache and NGINX.

   The frequent updates and large community support ensure that Ubuntu is always up-to-date with the latest technologies.
2. **Debian**: Debian is one of the oldest Linux distributions and serves as the foundation for many other distros, including Ubuntu. Debian is known for its stability and conservative approach to new software versions, making it ideal for systems that prioritize reliability.
3. **CentOS/AlmaLinux**: CentOS (now succeeded by AlmaLinux) is a community-driven distribution based on Red Hat Enterprise Linux (RHEL). It is often used in enterprise settings for hosting and running web servers due to its stability and long-term support.

Each distribution may look and feel different, but they all share one thing in common: they use the **Linux kernel**.

### Linux kernel

The Linux kernel is the core component of the operating system. We can think of it as the "brain" that manages communication between the hardware (like our computer’s CPU, memory, and devices) and the software applications we run. When an application needs to perform a task, like reading from the disk or sending data to a printer, it sends requests to the kernel, which handles it with the hardware. Essentially, the kernel is the middleman that helps our applications work with our computer’s hardware.

---

### How to log into Linux
Logging into a Linux system is straightforward, especially if we are already using it locally (like with a WSL terminal on Windows or directly on a Linux machine). But often, especially when working with remote servers (for example, in cloud environments), we will log in **remotely** using a tool called **SSH**. If we are logging into our Linux machine:
1. Open the terminal.
2. Enter the **username** and **password**.

For example, in WSL (Windows Subsystem for Linux), we can just open a terminal and we are logged into our local Linux system directly.

#### SSH
**SSH** stands for Secure Shell, and it's a protocol used to securely log into another computer over a network. This is especially common when accessing remote servers, such as cloud servers or hosting environments. With SSH, we can:
- Securely log in to a remote Linux machine.
- Run commands on that remote machine just as if we were using it directly.
- Transfer files securely between our local computer and the remote server.

SSH is popular because it encrypts the data being transferred, keeping it secure from eavesdropping or attacks. For example, to log into a remote server, we would use this command in a terminal:
```bash
ssh username@server-ip-address
```

After entering our password, we will have remote access to that server.

---

## Getting started with Ubuntu on WSL

- **Launch Ubuntu:** After installation, open the **Ubuntu app** from the start menu.

### Launching Xfce applications
Xfce4 is a lightweight desktop environment for Linux and Unix-like operating systems. Xfce4 provides a graphical interface that allows users to interact with their computer using windows, icons, menus, and panels, making it easy to navigate files and applications. It is designed to be fast and use fewer system resources compared to other desktop environments like GNOME or KDE. Xfce4 is modular, meaning we can install only the components we need without requiring the entire desktop environment. Here are three essential Xfce applications we can launch:
1. **Xfce4 Terminal:** A terminal emulator that provides a command-line interface within a GUI. It allows us to run shell commands and interact with the Linux system using a terminal.
   ```bash
   xfce4-terminal &
   ```

2. **Thunar:** A lightweight file manager for Xfce. Thunar allows us to browse and manage files and directories graphically, making it easier to work with your files in a GUI environment.
   ```bash
   thunar &
   ```

3. **Xfce4 AppFinder:** A graphical application launcher for Xfce. It helps us find and launch installed applications quickly, similar to the Windows Start menu.
   ```bash
   xfce4-appfinder &
   ```