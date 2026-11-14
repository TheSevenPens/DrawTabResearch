# Install OpenTabletDriver on CachyOS

First, follow [Prepare your system](linux-otd-install.md#1-prepare-your-system). Run the commands below in order in the same Bash terminal. Use `sudo -v` to check that your account can install packages.

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

After restarting, return to [Start the OTD daemon and check tablet detection](linux-otd-install.md#3-start-the-otd-daemon-and-check-tablet-detection).
