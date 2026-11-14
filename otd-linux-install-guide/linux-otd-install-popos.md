# Install OpenTabletDriver on Pop!_OS 24.04 LTS

First, follow [Prepare your system](linux-otd-install.md#1-prepare-your-system). Run the commands in the same Bash terminal on your Pop!_OS desktop.

## Download and install the official package

These steps use the official OpenTabletDriver 0.6.8.1 DEB for 64-bit x86. On Pop!_OS 24.04 LTS, APT can install the required .NET 10 runtime from the Ubuntu repositories enabled by default. [Official OpenTabletDriver release](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/tag/v0.6.8.1) · [Microsoft’s .NET instructions for Ubuntu 24.04](https://learn.microsoft.com/dotnet/core/install/linux-ubuntu-install#ubuntu-2404)

```bash
sudo apt update
sudo apt install curl ca-certificates
deb=opentabletdriver_0.6.8.1-1_x64.deb
curl -fLO "https://github.com/OpenTabletDriver/OpenTabletDriver/releases/download/v0.6.8.1/$deb"
sudo apt install "./$deb"
```

## Rebuild the boot image and restart

Rebuild the boot image so Linux applies OpenTabletDriver’s driver settings at startup. [Why the rebuild is needed](linux-otd-install.md#preventing-built-in-linux-drivers-from-interfering-with-otd)

```bash
sudo update-initramfs -u -k all
```

After the rebuild succeeds, restart your computer.

```bash
sudo reboot
```

After restarting, return to [Start the OTD daemon and check tablet detection](linux-otd-install.md#3-start-the-otd-daemon-and-check-tablet-detection).
