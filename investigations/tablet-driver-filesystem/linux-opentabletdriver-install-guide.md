# Install OpenTabletDriver on Linux

This guide covers OpenTabletDriver on **Debian 13 (Trixie)**, **Fedora 45**, **EndeavourOS**, and **CachyOS**, all x86-64. Debian, Fedora, and CachyOS used OpenTabletDriver **0.6.8.1**. EndeavourOS used the AUR package **0.6.8-1**. Start with a clean desktop installation and a regular user with sudo access for package installation. The commands use Bash. Use the install section for your distribution, then follow the shared desktop steps. These Fedora steps apply to DNF-based installations. [OpenTabletDriver Linux installation guide](https://opentabletdriver.net/Wiki/Install/Linux)

| Your system | Where to start |
| --- | --- |
| Debian 13 | [Install the official DEB](#debian-13) |
| Fedora 45 | [Install the official RPM](#fedora-45) |
| EndeavourOS | [Install the AUR package](#endeavouros) |
| CachyOS | [Install the CachyOS repository package](#cachyos) |

For release selection and source builds, see [Choose how to get a version](#choose-how-to-get-a-version).

## Setups covered by the official guide

This guide is scoped to the four x86-64 desktop setups above. Use OpenTabletDriver’s official instructions for these additional cases.

| Setup or install method | Official instructions |
| --- | --- |
| Ubuntu | [Ubuntu / Debian](https://opentabletdriver.net/Wiki/Install/Linux#ubuntu--debian) |
| Arch Linux | [Arch Linux](https://opentabletdriver.net/Wiki/Install/Linux#arch-linux) |
| openSUSE | [openSUSE](https://opentabletdriver.net/Wiki/Install/Linux#opensuse) |
| Gentoo | [Gentoo](https://opentabletdriver.net/Wiki/Install/Linux#gentoo) |
| NixOS | [NixOS](https://opentabletdriver.net/Wiki/Install/Linux#nixos) |
| Bazzite | [Bazzite](https://opentabletdriver.net/Wiki/Install/Linux#bazzite) |
| Flatpak, including on the four distros above | [Flatpak and its prerequisites](https://opentabletdriver.net/Wiki/Install/Linux#flatpak) |
| Manually building the AUR package with `makepkg` | [Arch Linux `makepkg` method](https://opentabletdriver.net/Wiki/Install/Linux#makepkg-method) |

For legacy udev rules, kernel module conflicts, and permissions troubleshooting, see OpenTabletDriver’s [Linux permissions guide](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux) and [Linux FAQ](https://opentabletdriver.net/Wiki/FAQ/Linux).

## 1. Prepare your system

Look up your exact tablet model in the supported tablets list and check any notes for Linux. Check your distribution and architecture. [OpenTabletDriver supported tablets](https://opentabletdriver.net/Tablets)

```bash
cat /etc/os-release
uname -m
```

If you previously installed a manufacturer driver, quit it and use the manufacturer's uninstaller or your package manager before proceeding. Back up any tablet settings you want to keep. If you already have OpenTabletDriver from another source, follow [Remove OpenTabletDriver](#5-remove-opentabletdriver) before switching install methods. The install packages and boot-image steps below handle kernel integration. [Upstream guidance on conflicting drivers](https://opentabletdriver.net/Wiki/FAQ/General#i-see-two-moving-cursors-when-hovering-my-pen)

For the first detection test, connect the tablet using a USB data cable. Upstream documents partial support for wireless dongles and no support for Bluetooth tablet connections. [Upstream connection guidance](https://opentabletdriver.net/Wiki/FAQ/General#my-tablet-is-supported-but-not-detected)

## 2. Install OpenTabletDriver

### Choose how to get a version

Use the **latest official release** for the current upstream build. Use an **exact GitHub tag** to reproduce a particular release. AUR and distribution repositories select their own package versions. For example, the test on EndeavourOS built `0.6.8` from the AUR while the official GitHub release was `0.6.8.1`. The CachyOS repository build `0.6.8.1-2` is upstream version `0.6.8.1` with CachyOS package revision `2`.

#### Download the latest or an exact official release

With the GitHub CLI (`gh`) installed and authenticated, set the asset pattern for your distro. Then run **one** of the download commands in a fresh directory. Each command retrieves a prebuilt x86-64 artifact from OpenTabletDriver's GitHub releases. [GitHub CLI download reference](https://cli.github.com/manual/gh_release_download)

```bash
repo=OpenTabletDriver/OpenTabletDriver

asset='opentabletdriver_*_x64.deb'                 # Debian
# asset='opentabletdriver-*.x86_64.rpm'             # Fedora
# asset='opentabletdriver-*_linux-x64_binary.tar.gz' # EndeavourOS or CachyOS

# Latest official stable release
gh release download --repo "$repo" --pattern "$asset"

# Exact official release, for example v0.6.8.1
gh release download v0.6.8.1 --repo "$repo" --pattern "$asset"
```

Without `gh`, use the release page and download the asset from **Assets**. The generic `_binary.tar.gz` contains the binaries and system files for a manual install. It requires the runtime and distro-specific device permissions and initramfs setup. Use the generic binary archive for a fresh install. Upstream describes the `_simple.tar.gz` archive as a way to test binaries on an existing installation. [Latest official release](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/latest) · [Release v0.6.8.1](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/tag/v0.6.8.1) · [Upstream Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux) · [Upstream archive formats](https://github.com/OpenTabletDriver/OpenTabletDriver/blob/v0.6.8.1/README.md#linux)

#### Build an exact version locally

Check out the release tag you want. Install Git, the .NET SDK required by that tag (.NET 10 for `v0.6.8.1`), and the Linux dependencies in the tag's README. The upstream script below builds and packages the generic Linux x86-64 tarball. Review the checkout's README for the packaging options and prerequisites if you choose a different tag. For an exact commit, substitute its full hash for the tag in the checkout command. [Upstream build instructions for v0.6.8.1](https://github.com/OpenTabletDriver/OpenTabletDriver/blob/v0.6.8.1/README.md#building-opentabletdriver-from-source)

```bash
tag=v0.6.8.1
git clone https://github.com/OpenTabletDriver/OpenTabletDriver.git
cd OpenTabletDriver
git checkout --detach "$tag"
git rev-parse HEAD
dotnet --list-sdks
./eng/bash/package.sh --runtime linux-x64 --configuration Release --package BinaryTarBall
```

#### Verification by distro

| Distro | Latest official GitHub download | Exact official GitHub release install | Build locally from source |
| --- | --- | --- | --- |
| Debian 13.7 | `.deb` download verified | `v0.6.8.1` DEB installed and GUI tested in the VM | Upstream tag build available. Untested. |
| Fedora 45 | `.rpm` download verified | `v0.6.8.1` RPM installed and GUI tested in the VM | Upstream tag build available. Untested. |
| EndeavourOS | Generic x64 archive download verified | Official `v0.6.8.1` tarball installed and GUI tested in Plasma Wayland with GRUB and dracut. | AUR build of `v0.6.8` installed and GUI tested in the VM. The direct upstream tag-build command above remains untested. |
| CachyOS | Generic x64 archive download verified | Official `v0.6.8.1` tarball installed and GUI tested in Plasma Wayland with Limine and mkinitcpio. | Upstream tag build available. Untested. We also verified the prebuilt CachyOS repository package. |

The latest-release download checks ran on the workstation. GitHub resolved them to `v0.6.8.1`, and the DEB and RPM hashes matched the pinned packages tested in the VMs.

### Debian 13

```bash
sudo apt update
sudo apt install curl ca-certificates
```

Download the release package and inspect its version and dependencies. The example pins the tested release. If you already downloaded a DEB above, set `deb` to its filename and skip the `curl` line. Run the dependency setup below for the tested release or another build that also requires .NET 10.

```bash
deb=opentabletdriver_0.6.8.1-1_x64.deb
curl -fLO "https://github.com/OpenTabletDriver/OpenTabletDriver/releases/download/v0.6.8.1/$deb"
dpkg-deb -f "$deb" Version Architecture Depends
```

This build requires `dotnet-runtime-10.0`. On the clean Debian VM, the default feeds did not provide it. If `apt-cache policy dotnet-runtime-10.0` shows no candidate, add Microsoft's Debian 13 feed. This feed is specific to Debian 13. Keep the .NET packages on a single provider to avoid mismatched runtime components. [Microsoft's Debian .NET instructions](https://learn.microsoft.com/en-us/dotnet/core/install/linux-debian) · [OpenTabletDriver Debian instructions](https://opentabletdriver.net/Wiki/Install/Linux#ubuntu--debian)

```bash
curl -fLO https://packages.microsoft.com/config/debian/13/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update
```

If you already have .NET installed and see a `libhostfxr` error, check which repositories provide the runtime and host packages before changing them. [Microsoft's package mix-up troubleshooting](https://learn.microsoft.com/en-us/dotnet/core/install/linux-package-mixup)

Install the local DEB. APT pulls in the runtime and the other declared dependencies. Complete the restart before testing tablet input. The Linux package supplies udev and kernel module configuration that affect device access. [OpenTabletDriver Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux)

```bash
sudo apt install "./$deb"
dpkg-query -W opentabletdriver
dotnet --list-runtimes
sudo reboot
```

### Fedora 45

Install the RPM with DNF. The example pins the tested release. If you already downloaded an RPM above, set `rpm_file` to its filename and skip the `curl` line. Fedora 45 provides the .NET 10 runtime required by the tested release in its own repositories. After installing the RPM, rebuild the initramfs as directed by the OpenTabletDriver team, then restart. [Upstream Fedora instructions](https://opentabletdriver.net/Wiki/Install/Linux#fedora)

```bash
rpm_file=opentabletdriver-0.6.8.1-1.x86_64.rpm
curl -fLO "https://github.com/OpenTabletDriver/OpenTabletDriver/releases/download/v0.6.8.1/$rpm_file"
sudo dnf install "./$rpm_file"
rpm -q opentabletdriver
dotnet --list-runtimes
sudo dracut --regenerate-all --force
sudo reboot
```

### EndeavourOS

Install the `opentabletdriver` AUR package as your regular desktop user. The AUR package version can differ from the upstream DEB and RPM versions.

```bash
sudo pacman -Syu
sudo pacman -S --needed base-devel
yay -S opentabletdriver
pacman -Q opentabletdriver
```

Run `yay` in an interactive terminal so it can prompt when it needs sudo. The AUR recipe builds from source using the .NET 10 SDK and declares the .NET 10 runtime. Both came from the configured package repositories in the test.

Rebuild the boot image with the command for your bootloader, then restart. For **GRUB with dracut**, use `sudo dracut-rebuild`. For **systemd-boot with dracut**, use `sudo reinstall-kernels`. The GRUB path was tested. [OpenTabletDriver EndeavourOS instructions](https://opentabletdriver.net/Wiki/Install/Linux#endeavouros) · [EndeavourOS dracut documentation](https://discovery.endeavouros.com/dracut/)

### CachyOS

CachyOS provides a prebuilt `opentabletdriver` package in its own repository. Use Pacman to update the system and install the package. [CachyOS package listing](https://packages.cachyos.org/package/cachyos/x86_64/opentabletdriver)

```bash
sudo pacman -Syu opentabletdriver
pacman -Q opentabletdriver
dotnet --list-runtimes
```

Rebuild the boot image before rebooting. For the CachyOS **Limine** setup with mkinitcpio, use the distribution's wrapper. For other bootloader configurations, follow the applicable CachyOS procedure. [CachyOS boot manager documentation](https://wiki.cachyos.org/configuration/boot_manager_configuration/)

```bash
sudo limine-mkinitcpio
sudo reboot
```

### Official GitHub tarball on EndeavourOS or CachyOS

Use this route in place of the AUR or CachyOS package when you want an exact upstream release or the current GitHub release. The commands below use the tested `v0.6.8.1` x86-64 archive. For a different release, check its runtime requirements and archive layout before applying these steps. If switching from the Pacman-managed OpenTabletDriver package, stop its user service and remove the package first. Back up any settings you want to keep. [Official v0.6.8.1 release](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/tag/v0.6.8.1)

```bash
sudo pacman -Syu --needed curl dotnet-runtime-10.0 gtk3 libevdev libx11 libxrandr

archive=opentabletdriver-0.6.8.1_linux-x64_binary.tar.gz
curl -fLO "https://github.com/OpenTabletDriver/OpenTabletDriver/releases/download/v0.6.8.1/$archive"
printf '%s  %s\n' b17929fe2071ab97381706f8f36391312c2495cd1037e1dc121a0aee7abfe1d5 "$archive" | sha256sum -c -
tar -tzf "$archive"
```

After the checksum passes, extract the archive into the system. The launcher scripts expect the binaries under `/usr/local/lib/opentabletdriver/`. The archive also places the udev rule under `/etc/udev/rules.d/`. Install the bundled module configuration in `/etc` so the host tools pick it up, then rebuild the boot image. [OpenTabletDriver Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux)

```bash
sudo tar --no-same-owner --no-overwrite-dir --strip-components=1 -xzf "$archive" -C /
sudo install -Dm644 /usr/local/lib/modprobe.d/99-opentabletdriver.conf /etc/modprobe.d/99-opentabletdriver.conf
sudo install -Dm644 /usr/local/lib/modules-load.d/opentabletdriver.conf /etc/modules-load.d/opentabletdriver.conf
/usr/local/bin/otd --version
```

Run the command for your boot setup, then reboot. We tested `sudo dracut-rebuild` on EndeavourOS with GRUB and `sudo limine-mkinitcpio` on CachyOS with Limine. For EndeavourOS with systemd-boot and dracut, EndeavourOS documents `sudo reinstall-kernels`. [EndeavourOS dracut documentation](https://discovery.endeavouros.com/dracut/) · [CachyOS boot manager documentation](https://wiki.cachyos.org/configuration/boot_manager_configuration/)

After signing in, follow the shared desktop steps below. If you previously enabled the Pacman package's service, run `systemctl --user daemon-reload` and `systemctl --user reenable opentabletdriver.service` first to refresh its login symlink. Check the unit path with `systemctl --user show opentabletdriver.service -p FragmentPath`. The tarball's unit is under `/usr/local/lib/systemd/user/`.

## 3. Start the driver and check tablet detection

After restarting, sign in to your desktop as the user who will use the tablet. Run these commands in your desktop terminal. The first command starts the daemon now and enables it for future sessions. [OpenTabletDriver Linux FAQ](https://opentabletdriver.net/Wiki/FAQ/Linux)

```bash
systemctl --user enable --now opentabletdriver.service
systemctl --user status opentabletdriver.service --no-pager
otd-gui
```

The packaged service checks for `WAYLAND_DISPLAY` or `DISPLAY` in the systemd user environment. If you run the start command over plain SSH, it can enable the service while skipping startup. Check the status from the desktop session where you plan to use the tablet.

The first launch opens the OpenTabletDriver Guide. Close it to return to the main window. Connect the tablet and confirm that OpenTabletDriver identifies the expected model. Use **Tablets → Detect tablet** to rescan, and check the **Console** tab for the result. With no tablet attached, the **Info** tab reports that no tablets are detected. Move the pen to check pointer movement once the tablet is detected.

If the app cannot connect to the daemon or the tablet is missing, inspect the user service log. Look for messages about `/dev/uinput`, `/dev/hidraw*`, or a conflicting driver. [OpenTabletDriver Linux troubleshooting](https://opentabletdriver.net/Wiki/FAQ/Linux)

```bash
journalctl --user -u opentabletdriver.service -b --no-pager
```

| What you see | What to check |
| --- | --- |
| Nothing changes in `lsusb` when you plug in the tablet | Try another USB port or a known data cable. [Upstream USB checks](https://opentabletdriver.net/Wiki/FAQ/General#my-tablet-is-supported-but-not-detected) |
| The log reports another tablet driver or denied access to `/dev/hidraw*` | Check for a running vendor driver, then verify the installed udev rules and kernel module configuration. [Upstream Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux) |
| Virtual tablet initialization fails with `ENODEV`, `ENOENT`, or `EACCES` | Upstream maps those errors to a missing device, missing kernel support, and denied access respectively. Check the matching fix. [Upstream Linux troubleshooting](https://opentabletdriver.net/Wiki/FAQ/Linux#tablet-is-detected-but-not-working) |
| Mapping is wrong with multiple monitors | Have either the desktop tablet settings or OpenTabletDriver map to all screens, then set your target area in the other. [Upstream multi-monitor steps](https://opentabletdriver.net/Wiki/FAQ/Linux#display-mapping-behaves-unexpectedly-on-a-multi-monitor-setup) |

## 4. Configure the tablet for drawing

In **Output**, choose the display you want to map and lock the tablet area's aspect ratio. Choose **Artist Mode** for pressure, then clear the existing tip binding from the advanced binding editor as directed by the Linux FAQ. Use the Artist Mode pen bindings if you configure pen buttons. Click **Apply** to activate the settings and **Save** to keep them. [OpenTabletDriver Linux FAQ on pressure](https://opentabletdriver.net/Wiki/FAQ/Linux#tablet-is-working-but-there-is-no-pressure)

Open a drawing app with a pressure-sensitive brush. Check that the pointer stays on the mapped display, a circle stays round, and light and heavy strokes look different. Check tilt separately if your tablet, pen, and brush support it.

## 5. Remove OpenTabletDriver

Quit the GUI. From the account that uses OpenTabletDriver, stop its daemon and turn off automatic startup if you enabled the user service. Repeat for each account that enabled it. If you launched `otd-daemon` manually in a terminal, stop it there with **Ctrl+C**.

```bash
systemctl --user disable --now opentabletdriver.service
```

### Package-managed installs

Use the command for the package you installed. On EndeavourOS, Pacman removes the package that `yay` built. On Fedora, `--no-autoremove` keeps shared dependencies such as the .NET runtime. Review the package manager's transaction before confirming. [Debian APT manual](https://manpages.debian.org/trixie/apt/apt.8.en.html) · [DNF5 removal manual](https://dnf5.readthedocs.io/en/stable/commands/remove.8.html) · [Pacman manual](https://man.archlinux.org/man/pacman.8)

| Install method | Remove command |
| --- | --- |
| Debian DEB | `sudo apt remove opentabletdriver` |
| Fedora RPM | `sudo dnf remove --no-autoremove opentabletdriver` |
| EndeavourOS AUR package | `sudo pacman -R opentabletdriver` |
| CachyOS repository package | `sudo pacman -R opentabletdriver` |

On Debian, use `sudo apt purge opentabletdriver` if you also want APT to remove any remaining package configuration. User settings are covered below. If you added files manually when troubleshooting, review those separately.

### Official GitHub tarball installs

These paths are for the official `v0.6.8.1` x86-64 tarball installed using the commands in this guide. For a different release or layout, check the original archive with `tar -tzf "$archive"` and remove its corresponding files. Back up any configuration files you edited before removing them. [Official v0.6.8.1 release](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/tag/v0.6.8.1)

```bash
sudo rm -f -- \
  /usr/local/bin/otd \
  /usr/local/bin/otd-daemon \
  /usr/local/bin/otd-gui \
  /usr/local/lib/opentabletdriver/OpenTabletDriver.Console \
  /usr/local/lib/opentabletdriver/OpenTabletDriver.Daemon \
  /usr/local/lib/opentabletdriver/OpenTabletDriver.UX.Gtk \
  /usr/local/lib/systemd/user/opentabletdriver.service \
  /usr/local/lib/modprobe.d/99-opentabletdriver.conf \
  /usr/local/lib/modules-load.d/opentabletdriver.conf \
  /usr/local/share/applications/opentabletdriver.desktop \
  /usr/local/share/doc/opentabletdriver/LICENSE \
  /usr/local/share/libinput/30-vendor-opentabletdriver.quirks \
  /usr/local/share/man/man8/opentabletdriver.8.gz \
  /usr/local/share/pixmaps/otd.ico \
  /usr/local/share/pixmaps/otd.png \
  /etc/udev/rules.d/70-opentabletdriver.rules \
  /etc/modprobe.d/99-opentabletdriver.conf \
  /etc/modules-load.d/opentabletdriver.conf

sudo rmdir --ignore-fail-on-non-empty -- \
  /usr/local/lib/opentabletdriver /usr/local/share/doc/opentabletdriver
```

### Rebuild the boot image and restart

Rebuilding the initramfs drops OpenTabletDriver's kernel-module overrides from the boot image after the corresponding files have been removed. Run the command for your setup and restart after it succeeds. [OpenTabletDriver Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux) · [EndeavourOS dracut guide](https://discovery.endeavouros.com/dracut/) · [CachyOS boot manager guide](https://wiki.cachyos.org/configuration/boot_manager_configuration/)

| Setup | Rebuild command |
| --- | --- |
| Debian with initramfs-tools | `sudo update-initramfs -u -k all` |
| Fedora with dracut | `sudo dracut --regenerate-all --force` |
| EndeavourOS with GRUB and dracut | `sudo dracut-rebuild` |
| EndeavourOS with systemd-boot and dracut | `sudo reinstall-kernels` |
| CachyOS with Limine and mkinitcpio | `sudo limine-mkinitcpio` |

After restarting, `command -v otd otd-daemon otd-gui` should print no paths, and `systemctl --user status opentabletdriver.service` should report that the unit could not be found. If either check finds a copy, inspect the reported path for a second installation.

### Optional settings cleanup

By default, Linux settings and plugins are in `~/.config/OpenTabletDriver`. Custom tablet definitions may also be in `~/.local/share/OpenTabletDriver/Configurations`. In your file manager, move these folders to a backup location or delete them if you want a fresh start. Repeat for other accounts as needed. If you set a custom application data path, check that location too. [OpenTabletDriver application data](https://opentabletdriver.net/Wiki/FAQ/General)

### VM removal results

| Distro and boot setup | Removal verified |
| --- | --- |
| Debian 13.7 with initramfs-tools | Official DEB `0.6.8.1-1`. APT removal, reboot, then optional purge. |
| Fedora 45 with dracut | Official RPM `0.6.8.1-1`. DNF removal with `--no-autoremove`, then reboot. |
| EndeavourOS Titan Nova with GRUB and dracut | AUR package `0.6.8-1` and official tarball `v0.6.8.1`, in separate runs. |
| EndeavourOS Titan Nova with systemd-boot and dracut | AUR package `0.6.8-1` and official tarball `v0.6.8.1`, in separate runs on the same UEFI test copy. |
| CachyOS with Limine and mkinitcpio | Repository package `0.6.8.1-2` and official tarball `v0.6.8.1`, in separate runs. |

Each run used the corresponding rebuild command and booted successfully. After reboot, the three OpenTabletDriver commands and the user service were gone. We also checked for the udev rule, kernel-module configuration, and service autostart link. For tarball installs, we checked that all 18 listed files and links were gone. The .NET runtime and user settings remained. We verified that the settings folder could be moved to a backup, including after the optional Debian purge. Physical tablet behavior after removal remains unverified.

## Lab verification

All tests used fresh x86-64 VM disks with no vendor tablet drivers or physical tablet attached. Xfce on Debian and Fedora and Plasma Wayland on EndeavourOS and CachyOS displayed the first-launch guide and connected to the OpenTabletDriver daemon. A rescan from the GUI reported that no tablets were detected on each system.

- **Debian 13.7.** APT resolved .NET Runtime `10.0.15` after adding Microsoft's Debian 13 feed. We verified the installed CLI and `/dev/uinput` after restart. Systemd skipped daemon startup in the initial headless session. The user service started once the Xfce display was available.
- **Fedora 45.** DNF installed .NET Runtime `10.0.13` from Fedora's updates repository. We ran the documented `dracut` command and verified a successful reboot into Xfce. With SELinux enforcing during the setup, the user service started, `/dev/uinput` was present, and the GUI connected to the daemon.
- **EndeavourOS Titan Nova.** The offline ISO install used GRUB and Plasma Wayland. The system upgrade required resolving a conflict with the old `plasma-x11-session` package and switching to a faster Arch mirror. We built AUR package `0.6.8-1` with `yay` at recipe commit `0000843ee4cc5d67550d99cad8da8d53a74521d8`. In the unattended test, `yay` built the package but could not prompt for sudo, so we installed the built artifact with `pacman -U`. After `dracut-rebuild` and reboot, the enabled user service started automatically at Plasma login.

- **CachyOS.** Installed from Desktop ISO `260809` with UEFI, Limine, and Plasma Wayland. Pacman installed the CachyOS repository package `0.6.8.1-2` and resolved .NET Runtime `10.0.14`. The `limine-mkinitcpio` wrapper rebuilt the boot image and updated `/boot/limine.conf`. After restart, we verified kernel `7.3.4-1-cachyos`, the presence of `/dev/uinput`, and explicit service startup with `systemctl --user enable --now` in Plasma.

- **Official tarball on EndeavourOS and CachyOS.** We made separate writable copies of the existing test VMs, removed their Pacman-managed OpenTabletDriver packages, and moved their prior user settings aside. We used the existing .NET `10.0.14` runtimes and GTK dependencies. After installing the exact GitHub archive and rebuilding the initramfs, both guests rebooted. We verified that the desktop user could write to `/dev/uinput`, that systemd loaded the service under `/usr/local`, and that both the running daemon and the GTK GUI came from the archive under `/usr/local`. A scan from each GUI reported no tablets.

Automatic startup at desktop login was verified on EndeavourOS. Physical tablet detection, mapping, pressure, and tilt remain unverified in these runs.

| Tested package | SHA-256 |
| --- | --- |
| `opentabletdriver_0.6.8.1-1_x64.deb` | `346c90ccd152f26aa4d2ef1fcb5767f6b5e73535ee809418f2c9f539fe0f42b2` |
| `opentabletdriver-0.6.8.1-1.x86_64.rpm` | `c6d3f27adba1a5a5070a13b781bb559f30533785df5de33e7d8cbb2f51bd5fa4` |
| Local AUR build `opentabletdriver-0.6.8-1-x86_64.pkg.tar.zst` | `add88f56ba13929c5849649819f3b7fb9ccd2dceb6f9d0227798e03e2eaab12f` |
| CachyOS repository package `opentabletdriver-0.6.8.1-2-x86_64.pkg.tar.zst` | `20cd326691be16efc81b3f8a4e6c964a05a8d47045323171b517ff3296578e1e` |
| Official `opentabletdriver-0.6.8.1_linux-x64_binary.tar.gz` | `b17929fe2071ab97381706f8f36391312c2495cd1037e1dc121a0aee7abfe1d5` |
