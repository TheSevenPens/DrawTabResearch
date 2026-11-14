# Install OpenTabletDriver on Linux


## Overview

This guide covers x86-64 desktop installs of OpenTabletDriver on **Debian 13 (Trixie)**, **Fedora 45**, **EndeavourOS**, and **CachyOS**.

## Notes

- The commands use Bash.
- Also see [OpenTabletDriver Linux installation guide](https://opentabletdriver.net/Wiki/Install/Linux)

### Installation sources

| Your system | Where to start |
| --- | --- |
| Debian 13 | [Install the official DEB](#debian-13) |
| Fedora 45 | [Install the official RPM](#fedora-45) |
| EndeavourOS | [Install the AUR package](#endeavouros) |
| CachyOS | [Install the CachyOS repository package](#cachyos) |

For a specific release, source build, or manual tarball install, see [Advanced installation options](linux-otd-advanced.md). See [Lab verification](linux-otd-install-verification.md) for what was tested.

## Instructions outside this guide

### OpenTabletDriver’s official instructions for additional cases.

| Setup or install method | Official instructions |
| --- | --- |
| Ubuntu | [Ubuntu / Debian](https://opentabletdriver.net/Wiki/Install/Linux#debian) |
| Arch Linux | [Arch Linux](https://opentabletdriver.net/Wiki/Install/Linux#arch) |
| openSUSE | [openSUSE](https://opentabletdriver.net/Wiki/Install/Linux#opensuse) |
| Gentoo | [Gentoo](https://opentabletdriver.net/Wiki/Install/Linux#gentoo) |
| NixOS | [NixOS](https://opentabletdriver.net/Wiki/Install/Linux#nixos) |
| Bazzite | [Bazzite](https://opentabletdriver.net/Wiki/Install/Linux#bazzite) |
| Flatpak, including on the four distros above | [Flatpak and its prerequisites](https://opentabletdriver.net/Wiki/Install/Linux#flatpak) |
| Manually building the AUR package with `makepkg` | [Arch Linux `makepkg` method](https://opentabletdriver.net/Wiki/Install/Linux#manual-makepkg-method) |

### legacy udev rules
For legacy udev rules, kernel module conflicts, and permissions troubleshooting, see OpenTabletDriver’s [Linux permissions guide](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux) and [Linux FAQ](https://opentabletdriver.net/Wiki/FAQ/Linux).

### Notes on Fedora
The Fedora RPM steps cover DNF-based Fedora. Fedora Atomic desktops such as Silverblue and Kinoite are outside this guide’s scope.

## 1. Prepare your system

### Verify your tablet is supported
Look up your  tablet model in the supported tablets list and check any notes for Linux. [OpenTabletDriver supported tablets](https://opentabletdriver.net/Tablets)

### Check your distribution and architecture.

```bash
cat /etc/os-release
uname -m
```

### Remove manufacturer tablet drivers
If you previously installed a manufacturer driver, quit it and use the manufacturer's uninstaller or your package manager before proceeding.

### Switching OTD Install methods
If you already have OpenTabletDriver from another source, follow [Uninstall OpenTabletDriver on Linux](linux-otd-uninstall.md) before switching install methods. [Upstream guidance on conflicting drivers](https://opentabletdriver.net/Wiki/FAQ/General#two-cursors)

### OTD impact on built-in tablet support on Linux

**Built-in tablet support can stop working during installation.** OpenTabletDriver installs kernel-module overrides to prevent drivers such as `wacom` and `hid_uclogic` from competing for the same tablet. The Debian package also attempts to unload those modules during installation. The [uninstall steps](linux-otd-uninstall.md) clear OpenTabletDriver’s overrides and rebuild the boot image. Recovery of built-in tablet input after removal still needs a hardware test. [Upstream Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux)

### Verify your tablet is detected

For the first detection test, connect the tablet using a USB data cable. Upstream documents partial support for wireless dongles and no support for Bluetooth tablet connections. [Upstream connection guidance](https://opentabletdriver.net/Wiki/FAQ/General#tablet-not-detected)


## 2. Install OpenTabletDriver

Choose the section for your distro. Run its blocks in order in the same Bash terminal so variables such as `deb` and `rpm_file` are available for later commands. Run `sudo -v` first to confirm your account can install packages. Once you have rebuilt the boot image and restarted, continue to [Start the driver](#3-start-the-driver-and-check-tablet-detection).

### Debian 13

```bash
sudo apt update
sudo apt install curl ca-certificates
```

Download the tested release package and inspect its version and dependencies. If you already have the DEB, set `deb` to its filename and skip the `curl` line.

```bash
deb=opentabletdriver_0.6.8.1-1_x64.deb
curl -fLO "https://github.com/OpenTabletDriver/OpenTabletDriver/releases/download/v0.6.8.1/$deb"
dpkg-deb -f "$deb" Version Architecture Depends
```

This build requires `dotnet-runtime-10.0`. Check whether your configured repositories provide it.

```bash
apt-cache policy dotnet-runtime-10.0
```

If APT reports `Candidate: (none)` or returns no entry for the package, add Microsoft's Debian 13 feed as shown below. The lab's clean Debian VM needed this feed. Keep the .NET packages on a single provider to avoid mismatched runtime components. [Microsoft's Debian .NET instructions](https://learn.microsoft.com/en-us/dotnet/core/install/linux-debian) · [OpenTabletDriver Debian instructions](https://opentabletdriver.net/Wiki/Install/Linux#debian)

```bash
curl -fLO https://packages.microsoft.com/config/debian/13/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update
```

If you already have .NET installed and see a `libhostfxr` error, check which repositories provide the runtime and host packages before changing them. [Microsoft's package mix-up troubleshooting](https://learn.microsoft.com/en-us/dotnet/core/install/linux-package-mixup)

Install the local DEB. APT pulls in the declared dependencies. On Debian with **initramfs-tools**, rebuild the boot images before restarting so they contain the same OpenTabletDriver module overrides as the installed system. [OpenTabletDriver Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux)

```bash
sudo apt install "./$deb"
dpkg-query -W opentabletdriver
dotnet --list-runtimes
sudo update-initramfs -u -k all
sudo reboot
```

For the tested release, look for a `Microsoft.NETCore.App 10.0.x` entry, where `x` is the installed patch version.

The tested DEB leaves existing boot images unchanged. The rebuild adds the OpenTabletDriver module configuration to the boot image. Repeat the rebuild when [uninstalling](linux-otd-uninstall.md#verify-removal) to remove that configuration from the image. [Debian update-initramfs manual](https://manpages.debian.org/trixie/initramfs-tools/update-initramfs.8.en.html)

For a DEB downloaded from GitHub, get new OpenTabletDriver releases manually. See [Update OpenTabletDriver](#update-opentabletdriver).

### Fedora 45

Install the tested RPM with DNF. If you already have the RPM, set `rpm_file` to its filename and skip the `curl` line. Fedora 45 provides the required .NET 10 runtime in its own repositories. After installing the RPM, rebuild the initramfs, then restart. [Upstream Fedora instructions](https://opentabletdriver.net/Wiki/Install/Linux#fedora)

If `curl` is unavailable, install it with `sudo dnf install curl` or download the RPM from the [official release assets](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/tag/v0.6.8.1).

```bash
rpm_file=opentabletdriver-0.6.8.1-1.x86_64.rpm
curl -fLO "https://github.com/OpenTabletDriver/OpenTabletDriver/releases/download/v0.6.8.1/$rpm_file"
sudo dnf install "./$rpm_file"
rpm -q opentabletdriver
dotnet --list-runtimes
sudo dracut --regenerate-all --force
sudo reboot
```

For an RPM downloaded from GitHub, get new OpenTabletDriver releases manually. See [Update OpenTabletDriver](#update-opentabletdriver).

### EndeavourOS

Install the `opentabletdriver` AUR package as your regular desktop user. The AUR package version can differ from the upstream DEB and RPM versions.

```bash
sudo pacman -Syu
```

On an older EndeavourOS Plasma installation, the Plasma 6.8 upgrade may ask whether to remove `plasma-x11-session`. If you plan to use Plasma on Wayland, accept the prompt to continue. This removes the Plasma X11 login option. If you depend on that session, review the migration notes before proceeding. [EndeavourOS Plasma 6.8 migration notes](https://forum.endeavouros.com/t/kde-plasma-x11-session-removed-from-archrepos-plasma-moved-to-wayland-only/81977)

```bash
sudo pacman -S --needed base-devel
yay -S opentabletdriver
pacman -Q opentabletdriver
```

Run `yay` in an interactive terminal so it can prompt when it needs sudo. If your setup lacks `yay`, see [the official AUR installation options](https://opentabletdriver.net/Wiki/Install/Linux#arch). The AUR recipe builds from source using the .NET 10 SDK and declares the .NET 10 runtime. Both came from the configured package repositories in the test.

Follow [Rebuild the boot image and restart](#rebuild-the-boot-image-and-restart). That section shows how to choose the EndeavourOS command for your bootloader. [OpenTabletDriver EndeavourOS instructions](https://opentabletdriver.net/Wiki/Install/Linux#endeavouros)

### CachyOS

CachyOS provides a prebuilt `opentabletdriver` package in its own repository. Use Pacman to update the system and install the package. [CachyOS package listing](https://packages.cachyos.org/package/cachyos/x86_64/opentabletdriver)

```bash
sudo pacman -Syu opentabletdriver
pacman -Q opentabletdriver
dotnet --list-runtimes
```

Rebuild the boot image before rebooting. These commands cover CachyOS with **Limine** and mkinitcpio. If you use a different bootloader, follow the CachyOS instructions for that bootloader. [CachyOS boot manager documentation](https://wiki.cachyos.org/configuration/boot_manager_configuration/)

```bash
sudo limine-mkinitcpio
sudo reboot
```

## 3. Start the driver and check tablet detection

After restarting, sign in to your desktop as the user who will use the tablet. Run these commands in your desktop terminal. The first command starts the daemon now and enables it for desktops that activate systemd’s `graphical-session.target`. The last command checks whether your current desktop activates that target. [OpenTabletDriver Linux FAQ](https://opentabletdriver.net/Wiki/FAQ/Linux)

```bash
systemctl --user enable --now opentabletdriver.service
systemctl --user status opentabletdriver.service --no-pager
systemctl --user is-active graphical-session.target
```

Look for **active (running)** in the service status. If the target check prints `inactive` on Xfce, follow [the Xfce login steps](#start-automatically-at-desktop-login) to make startup persistent. On other desktops with an inactive target, see the [upstream autostart guidance](https://opentabletdriver.net/Wiki/FAQ/Linux#autostart).

Open **OpenTabletDriver** from the desktop app menu or run `otd-gui` in a terminal. Use a second terminal for diagnostics if you launched the GUI from the first one. The Linux GUI connects to the daemon running under your desktop account. Closing the GUI leaves the service running. [Upstream daemon guidance](https://opentabletdriver.net/Wiki/FAQ/General#gui-is-almost-always-the-driver)

The packaged service checks for `WAYLAND_DISPLAY` or `DISPLAY` in the systemd user environment. If you run the start command over plain SSH, it can enable the service while skipping startup. Check the status from the desktop session where you plan to use the tablet.

**Installation checkpoint.** The daemon reports **active (running)** and the GUI reaches the main window without a connection timeout. On first launch, close the OpenTabletDriver Guide window to see the main window. With no tablet attached, the **Info** tab can report **No tablets detected** even when the GUI is connected.

Connect the tablet and confirm that OpenTabletDriver identifies the expected model. Use **Tablets → Detect tablet** to rescan, and check the **Console** tab for the result. Move the pen to check pointer movement once the tablet is detected.

If the app cannot connect to the daemon or the tablet is missing, inspect the user service log. Look for messages about `/dev/uinput`, `/dev/hidraw*`, or a conflicting driver. [OpenTabletDriver Linux troubleshooting](https://opentabletdriver.net/Wiki/FAQ/Linux)

```bash
journalctl --user -u opentabletdriver.service -b --no-pager
```

| What you see | What to check |
| --- | --- |
| Nothing changes in `lsusb` when you plug in the tablet | Try another USB port or a known data cable. If the command is missing, install the `usbutils` package with your distro's package manager. [Upstream USB checks](https://opentabletdriver.net/Wiki/FAQ/General#tablet-not-detected) |
| The log reports another tablet driver or denied access to `/dev/hidraw*` | Check for a running vendor driver, then verify the installed udev rules and kernel module configuration. [Upstream Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux) |
| Virtual tablet initialization fails with `ENODEV`, `ENOENT`, or `EACCES` | Upstream maps those errors to a missing device, missing kernel support, and denied access respectively. Check the matching fix. [Upstream Linux troubleshooting](https://opentabletdriver.net/Wiki/FAQ/Linux#fail-virtual-device) |
| Mapping is wrong with multiple monitors | Have either the desktop tablet settings or OpenTabletDriver map to all screens, then set your target area in the other. [Upstream multi-monitor steps](https://opentabletdriver.net/Wiki/FAQ/Linux#multi-monitor-mapping-issues) |

### Start automatically at desktop login

On **Fedora Workstation with GNOME Wayland**, **EndeavourOS with Plasma Wayland**, and **CachyOS with Plasma Wayland**, the standard `systemctl --user enable --now opentabletdriver.service` command is sufficient. These desktops activate the graphical session target after you sign in.

On the tested **Debian and Fedora Xfce** desktops, enabling the packaged service alone left it inactive after login because Xfce left `graphical-session.target` inactive. Keep the user service enabled and add an Xfce login entry to start it. Run this once from your regular desktop account:

```bash
systemctl --user enable opentabletdriver.service
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/opentabletdriver-xfce.desktop <<'DESKTOP'
[Desktop Entry]
Type=Application
Name=OpenTabletDriver Daemon
Exec=systemctl --user start opentabletdriver.service
OnlyShowIn=XFCE;
DESKTOP
```

Restart and sign in. After the desktop finishes loading, run `systemctl --user is-active opentabletdriver.service` and `systemctl --user is-enabled opentabletdriver.service`. Expect `active` and `enabled`, respectively. [OpenTabletDriver guidance on desktop autostart](https://opentabletdriver.net/Wiki/FAQ/Linux#autostart)

## 4. Configure the tablet for drawing

1. In **Output**, choose the display you want to map and lock the tablet area's aspect ratio.
2. In the output mode selector at the bottom left, choose **Artist Mode**.
3. In **Pen Settings**, open the tip binding's advanced editor with **…**, then choose **Clear**. Use **Artist Mode** pen bindings if you configure pen buttons.
4. Click **Apply** to try the settings in your current session and **Save** to keep them for future sessions. [OpenTabletDriver Linux FAQ on pressure](https://opentabletdriver.net/Wiki/FAQ/Linux#artist-mode)

Open a drawing app with a pressure-sensitive brush. Check that the pointer stays on the mapped display, a circle stays round, and light and heavy strokes look different. Check tilt separately if your tablet, pen, and brush support it.

## Update OpenTabletDriver

GitHub downloads are updated manually. Check the official releases page for a new DEB, RPM, or tarball. Before replacing one of those builds, back up your settings, quit the GUI, and run `systemctl --user stop opentabletdriver.service` from your regular desktop account. AUR and CachyOS repository packages update through normal system updates. [Official OpenTabletDriver releases](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/latest)

| Current install | How to update |
| --- | --- |
| Debian DEB | Download the new official x86-64 DEB into your current directory and set `deb` to its actual filename. Check the new release's runtime requirements, then run `sudo apt install "./$deb"`. |
| Fedora RPM | Download the new official x86-64 RPM into your current directory and set `rpm_file` to its actual filename. Run `sudo dnf install "./$rpm_file"`. |
| EndeavourOS AUR package | Run `yay -Syu` in a regular user's terminal. Confirm that the transaction includes OpenTabletDriver if an AUR update is available. |
| CachyOS repository package | Run `sudo pacman -Syu`. Pacman updates OpenTabletDriver when a newer build is available from your configured repositories. |
| Manual GitHub tarball | Follow the [tarball removal steps](linux-otd-uninstall.md#official-github-tarball-installs) for the old release, then [install the new archive](linux-otd-advanced.md#official-github-tarball-on-endeavouros-or-cachyos). Use the filenames, checksum, layout, and dependencies for the new release. Keep your user settings if you want to reuse them. |

After installing the new version, run the [boot-image rebuild for your setup](#rebuild-the-boot-image-and-restart) and restart. If you removed a tarball before installing its replacement, rebuild once after the new archive and its configuration are in place. After signing in, check `otd --version` and `systemctl --user is-active opentabletdriver.service`, then open the GUI. [Official releases](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/latest) · [Pacman manual](https://man.archlinux.org/man/pacman.8)

If you need to roll back, keep a copy of the previous package or archive. Install an older DEB with `sudo apt install --allow-downgrades "./$old_deb"` or an older RPM with `sudo dnf downgrade "./$old_rpm"`, setting the variable to the downloaded filename. For an AUR or CachyOS package, use `sudo pacman -U` with the saved older package if its dependencies are still compatible. For a tarball, remove the current archive's files and reinstall the previous archive. Restore your pre-update settings if the older version cannot read the newer settings, then rebuild the boot image and restart. [APT manual](https://manpages.debian.org/trixie/apt/apt.8.en.html) · [DNF5 downgrade manual](https://dnf5.readthedocs.io/en/stable/commands/downgrade.8.html) · [Pacman manual](https://man.archlinux.org/man/pacman.8)

The lab verified both the in-place upgrade from `v0.6.8` to `v0.6.8.1` and the rollback to `v0.6.8` using the official DEB on Debian 13.7 and the official RPM on Fedora 45. The package transactions left the settings file byte-for-byte unchanged. The daemon started automatically after reboot and Xfce login and loaded the global setting changed for each test. Other version pairs and the AUR, CachyOS repository, and tarball update and rollback paths remain unverified. See [VM upgrade and rollback results](linux-otd-install-verification.md#vm-upgrade-and-rollback-results).

## Rebuild the boot image and restart

Rebuilding the initramfs synchronizes its module configuration with the installed system. Use the command for your setup, then run `sudo reboot` after the rebuild succeeds. [OpenTabletDriver Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux) · [EndeavourOS dracut guide](https://discovery.endeavouros.com/dracut/) · [CachyOS boot manager guide](https://wiki.cachyos.org/configuration/boot_manager_configuration/)

| Setup | Rebuild command |
| --- | --- |
| Debian with initramfs-tools | `sudo update-initramfs -u -k all` |
| Fedora with dracut | `sudo dracut --regenerate-all --force` |
| EndeavourOS with GRUB and dracut | `sudo dracut-rebuild` |
| EndeavourOS with systemd-boot and dracut | `sudo reinstall-kernels` |
| CachyOS with Limine and mkinitcpio | `sudo limine-mkinitcpio` |

On EndeavourOS, check which dracut helper your system has installed:

```bash
pacman -Q eos-dracut
pacman -Q kernel-install-for-dracut
```

If only `eos-dracut` reports a version, use the GRUB command. If only `kernel-install-for-dracut` reports a version, use the systemd-boot command. Pacman reports a package as missing when it is absent. If both or neither are installed, check your bootloader and initramfs setup against the EndeavourOS documentation before proceeding. On UEFI systems, `sudo bootctl status` can show the **Current Boot Loader**. We verified the helper package check on both lab configurations. [EndeavourOS dracut helpers](https://discovery.endeavouros.com/dracut/) · [bootctl manual](https://www.freedesktop.org/software/systemd/man/latest/bootctl.html)
