# Install OpenTabletDriver on Linux


## Overview

This guide walks you through installing and setting up OpenTabletDriver on selected x86-64 Linux distributions. It links to separate instructions for advanced options and other setups.

- Debian 13 (Trixie)
- Pop!_OS 24.04 LTS
- Fedora 45
- EndeavourOS
- CachyOS

## Notes

- All the commands shown in this installation guide use the Bash shell.
- See the [official OpenTabletDriver installation guide for Linux](https://opentabletdriver.net/Wiki/Install/Linux).

## Installation methods by distro

This guide uses your distro’s package manager.

- **Debian** installs the official DEB package downloaded from GitHub.
- **Pop!_OS** uses APT to install the official DEB package downloaded from GitHub.
- **Fedora** uses DNF to install the official RPM package downloaded from GitHub. Fedora Atomic desktops such as Silverblue and Kinoite are outside this guide’s scope.
- **EndeavourOS** builds and installs the AUR package with `yay`.
- **CachyOS** installs the package from its own repository.

See [Advanced installation options](linux-otd-advanced.md) to choose a different official release, build directly from upstream source, or manually install the official tarball on EndeavourOS or CachyOS.

## Other distros and install methods

| Setup or install method | Official instructions |
| --- | --- |
| Ubuntu | [Ubuntu / Debian](https://opentabletdriver.net/Wiki/Install/Linux#debian) |
| Arch Linux | [Arch Linux](https://opentabletdriver.net/Wiki/Install/Linux#arch) |
| openSUSE | [openSUSE](https://opentabletdriver.net/Wiki/Install/Linux#opensuse) |
| Gentoo | [Gentoo](https://opentabletdriver.net/Wiki/Install/Linux#gentoo) |
| NixOS | [NixOS](https://opentabletdriver.net/Wiki/Install/Linux#nixos) |
| Bazzite | [Bazzite](https://opentabletdriver.net/Wiki/Install/Linux#bazzite) |
| Flatpak | [Flatpak and its prerequisites](https://opentabletdriver.net/Wiki/Install/Linux#flatpak) |
| Manually building the AUR package with `makepkg` | [Arch Linux `makepkg` method](https://opentabletdriver.net/Wiki/Install/Linux#manual-makepkg-method) |

## 1. Prepare your system

### Verify your tablet is supported
Look up your  tablet model in the supported tablets list and check any notes for Linux. [OpenTabletDriver supported tablets](https://opentabletdriver.net/Tablets)

### Check your architecture

This guide covers 64-bit x86 systems. To check your architecture, open a terminal and run the following command.

```bash
uname -m
```

Example output from a Fedora 45 Workstation VM:

```text
x86_64
```

If the command prints `x86_64`, your system matches the architecture covered here. If it prints something else, such as `aarch64`, skip these install steps and check the official documentation for your architecture.

### Remove manufacturer tablet drivers
If you previously installed a manufacturer driver, quit it and use the manufacturer's uninstaller or your package manager before proceeding.

### How OpenTabletDriver affects built-in tablet support

Linux distributions come with built-in drivers for many drawing tablets. If your tablet already works without a separate driver installed, Linux may be using one of these drivers.

OpenTabletDriver disables built-in drivers such as `wacom` and `hid_uclogic` so they do not compete for the same tablet. **If your tablet relies on one of those drivers, expect its input to stop working during the switch.** On Debian, this can happen as soon as the package is installed. Tablet input through OpenTabletDriver becomes available once you finish setup and the driver detects your tablet. [Upstream Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux)

## 2. Install OpenTabletDriver

Follow the instructions for your distro shown below.
Those instructions include restarting your computer before you start the OTD daemon.

| Your system | Where to start |
| --- | --- |
| Debian 13 | [Install the official DEB](linux-otd-install-debian.md) |
| Pop!_OS 24.04 LTS | [Install the official DEB on Pop!_OS](linux-otd-install-popos.md) |
| Fedora 45 | [Install the official RPM](linux-otd-install-fedora.md) |
| EndeavourOS | [Install the AUR package](linux-otd-install-endeavouros.md) |
| CachyOS | [Install the CachyOS repository package](linux-otd-install-cachyos.md) |

## 3. Start the OTD daemon and check tablet detection

As a reminder, restart your computer after installing OpenTabletDriver. If you haven’t restarted yet, do so now.

### Start the daemon

```bash
systemctl --user start opentabletdriver.service
```

### Verify the daemon is running

```bash
systemctl --user status opentabletdriver.service --no-pager
```

Look for **active (running)** on the `Active:` line.

```text
Active: active (running)
```

### Launching the OTD app

You can launch the OTD app in two ways.

- Open **OpenTabletDriver** from your desktop’s app menu.
- Run `otd-gui` in a terminal.

The first time you launch the OTD app, it opens the OpenTabletDriver Guide. You can read it or close it right away to see the main window. To reopen it, choose **Help → Show guide...**.

### Closing the OTD app

You can close the app and keep using your tablet. The OTD daemon continues running in the background. [Upstream daemon guidance](https://opentabletdriver.net/Wiki/FAQ/General#gui-is-almost-always-the-driver)

### Installation checkpoint

- OpenTabletDriver is installed.
- The OTD daemon is running. The service status shows **active (running)**.
- The OTD app connects to the daemon and opens its main window.
- If no tablet is connected, the **Info** tab can show **No tablets detected** while the app is working normally.

### Check tablet detection

If you haven’t connected your tablet to your computer with a USB cable, do that now. As a reminder, OpenTabletDriver has no support for Bluetooth tablet connections and only partial support for wireless USB dongles.

Confirm that OpenTabletDriver identifies the expected model. Use **Tablets → Detect tablet** to rescan, and check the **Console** tab for the result. Move the pen to check pointer movement once the tablet is detected.

If the app cannot connect to the daemon or the tablet is missing, see the [troubleshooting guide](linux-otd-troubleshooting.md).

## Start automatically at desktop login

To have OpenTabletDriver start when you sign in, follow the [automatic startup instructions](linux-otd-autostart.md).

## 4. Configure the tablet for drawing

1. In **Output**, choose the display you want to map and lock the tablet area's aspect ratio.
2. In the output mode selector at the bottom left, choose **Artist Mode**.
3. In **Pen Settings**, open the tip binding's advanced editor with **…**, then choose **Clear**. Use **Artist Mode** pen bindings if you configure pen buttons.
4. Click **Apply** to try the settings in your current session and **Save** to keep them for future sessions. [OpenTabletDriver Linux FAQ on pressure](https://opentabletdriver.net/Wiki/FAQ/Linux#artist-mode)

Open a drawing app with a pressure-sensitive brush. Check that the pointer stays on the mapped display, a circle stays round, and light and heavy strokes look different. Check tilt separately if your tablet, pen, and brush support it.

## Troubleshooting

See the [troubleshooting guide](linux-otd-troubleshooting.md) for daemon startup, tablet detection, permissions, and display mapping.

## Update OpenTabletDriver

For package and tarball updates or rollbacks, see [Update OpenTabletDriver on Linux](linux-otd-update.md).

## Preventing built-in Linux drivers from interfering with OTD

### Why this is needed

Linux can load a built-in tablet driver at startup that prevents OpenTabletDriver from accessing your tablet. To prevent this problem, you need to rebuild the boot image.

The rebuild updates the boot image (also called the initramfs) so Linux uses OpenTabletDriver’s settings the next time you start your computer.

After uninstalling OpenTabletDriver, the same rebuild lets Linux use its built-in tablet drivers again.

### Rebuild the boot image

Use the rebuild command for your setup. If you use EndeavourOS and are unsure which command applies, see [Choosing the rebuild command on EndeavourOS](#choosing-the-rebuild-command-on-endeavouros).

| Setup | Rebuild command |
| --- | --- |
| Debian with initramfs-tools | `sudo update-initramfs -u -k all` |
| Pop!_OS 24.04 LTS with initramfs-tools | `sudo update-initramfs -u -k all` |
| Fedora with dracut | `sudo dracut --regenerate-all --force` |
| EndeavourOS with GRUB and dracut | `sudo dracut-rebuild` |
| EndeavourOS with systemd-boot and dracut | `sudo reinstall-kernels` |
| CachyOS with Limine and mkinitcpio | `sudo limine-mkinitcpio` |

### Choosing the rebuild command on EndeavourOS

On EndeavourOS, check which dracut helper your system has installed:

```bash
pacman -Q eos-dracut
pacman -Q kernel-install-for-dracut
```

If only `eos-dracut` reports a version, use the GRUB command. If only `kernel-install-for-dracut` reports a version, use the systemd-boot command. Pacman reports a package as missing when it is absent. If both or neither are installed, check your bootloader and initramfs setup against the EndeavourOS documentation before proceeding. On UEFI systems, `sudo bootctl status` can show the **Current Boot Loader**. We verified the helper package check on both lab configurations. [EndeavourOS dracut helpers](https://discovery.endeavouros.com/dracut/) · [bootctl manual](https://www.freedesktop.org/software/systemd/man/latest/bootctl.html)

### Reboot your computer

After the rebuild succeeds, restart your computer.

```bash
sudo reboot
```

## Appendix: Identify or switch an existing OpenTabletDriver installation

If OpenTabletDriver is already installed and you are unsure how it was installed, check which commands Bash finds and where systemd loaded the daemon service from.

```bash
type -a otd otd-gui otd-daemon
systemctl --user show opentabletdriver.service -p FragmentPath
```

If Bash shows a file path, ask your package manager whether it owns that file. Substitute the path you found for `/usr/bin/otd` in the example below.

| Distribution | Ownership check |
| --- | --- |
| Debian | `dpkg-query -S /usr/bin/otd` |
| Fedora | `rpm -qf /usr/bin/otd` |
| EndeavourOS or CachyOS | `pacman -Qo /usr/bin/otd` |

An unowned file under `/usr/local` may come from a manual tarball installation. If you use Flatpak, check separately with `flatpak list --app | grep -i opentabletdriver`. Package ownership identifies the installed package. Its exact download source may still be unknown.

Once you know the existing install method, follow [Uninstall OpenTabletDriver on Linux](linux-otd-uninstall.md) before switching methods. [Upstream guidance on conflicting drivers](https://opentabletdriver.net/Wiki/FAQ/General#two-cursors)
