# Uninstall OpenTabletDriver on Linux

These steps cover the Debian DEB, Fedora RPM, EndeavourOS AUR package, CachyOS repository package, and official GitHub tarball described in the [Linux install guide](linux-otd-install.md).

## Stop OpenTabletDriver and turn off automatic startup

Quit the GUI. From the account that uses OpenTabletDriver, stop its daemon and turn off automatic startup if you enabled the user service. Repeat for each account that enabled it. If you launched `otd-daemon` manually in a terminal, stop it there with **Ctrl+C**.

```bash
systemctl --user disable --now opentabletdriver.service
```

If you created the [Xfce login entry](linux-otd-install.md#start-automatically-at-desktop-login), remove it from the same account before uninstalling:

```bash
rm -f -- ~/.config/autostart/opentabletdriver-xfce.desktop
```

## Package-managed installs

Use the command for the package you installed. On EndeavourOS, Pacman removes the package that `yay` built. On Fedora, `--no-autoremove` keeps shared dependencies such as the .NET runtime. Review the package manager's transaction before confirming. [Debian APT manual](https://manpages.debian.org/trixie/apt/apt.8.en.html) · [DNF5 removal manual](https://dnf5.readthedocs.io/en/stable/commands/remove.8.html) · [Pacman manual](https://man.archlinux.org/man/pacman.8)

| Install method | Remove command |
| --- | --- |
| Debian DEB | `sudo apt remove opentabletdriver` |
| Fedora RPM | `sudo dnf remove --no-autoremove opentabletdriver` |
| EndeavourOS AUR package | `sudo pacman -R opentabletdriver` |
| CachyOS repository package | `sudo pacman -R opentabletdriver` |

On Debian, use `sudo apt purge opentabletdriver` if you also want APT to remove any remaining package configuration. User settings are covered below. If you added files manually when troubleshooting, review those separately.

These steps deliberately keep shared dependencies such as .NET. On Debian they also leave the Microsoft feed installed if you added it.

## Official GitHub tarball installs

These paths are for the official `v0.6.8.1` x86-64 tarball installed using the [Linux tarball install steps](linux-otd-advanced.md#official-github-tarball-on-endeavouros-or-cachyos). For a different release or layout, check the original archive with `tar -tzf "$archive"` and remove its corresponding files. Back up any configuration files you edited before removing them. [Official v0.6.8.1 release](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/tag/v0.6.8.1)

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

## Verify removal

Follow [Rebuild the boot image and restart](linux-otd-install.md#rebuild-the-boot-image-and-restart) to clear any OpenTabletDriver kernel-module overrides from the boot image.

After restarting, `command -v otd otd-daemon otd-gui` should print no paths, and `systemctl --user status opentabletdriver.service` should report that the unit could not be found. If either check finds a copy, inspect the reported path for a second installation.

## Optional settings cleanup

By default, Linux settings and plugins are in `~/.config/OpenTabletDriver`. Custom tablet definitions may also be in `~/.local/share/OpenTabletDriver/Configurations`. In your file manager, move these folders to a backup location or delete them if you want a fresh start. Repeat for other accounts as needed. If you set a custom application data path, check that location too. [OpenTabletDriver application data](https://opentabletdriver.net/Wiki/FAQ/General)

## VM removal results

| Distro and boot setup | Removal verified |
| --- | --- |
| Debian 13.7 with initramfs-tools | Official DEB `0.6.8.1-1`. APT removal, reboot, then optional purge. |
| Fedora 45 with dracut | Official RPM `0.6.8.1-1`. DNF removal with `--no-autoremove`, then reboot. |
| EndeavourOS Titan Nova with GRUB and dracut | AUR package `0.6.8-1` and official tarball `v0.6.8.1`, in separate runs. |
| EndeavourOS Titan Nova with systemd-boot and dracut | AUR package `0.6.8-1` and official tarball `v0.6.8.1`, in separate runs on the same UEFI test copy. |
| CachyOS with Limine and mkinitcpio | Repository package `0.6.8.1-2` and official tarball `v0.6.8.1`, in separate runs. |

Each run used the corresponding rebuild command and booted successfully. After reboot, the three OpenTabletDriver commands and the user service were gone. We also checked for the udev rule, kernel-module configuration, and service autostart link. For tarball installs, we checked that all 18 listed files and links were gone. The .NET runtime and user settings remained. We verified that the settings folder could be moved to a backup, including after the optional Debian purge. Physical tablet behavior after removal remains unverified.
