# Install OpenTabletDriver on Debian 13

First, follow [Prepare your system](linux-otd-install.md#1-prepare-your-system). Run the commands below in order in the same Bash terminal. Use `sudo -v` to check that your account can install packages.

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

For a DEB downloaded from GitHub, get new OpenTabletDriver releases manually. See [Update OpenTabletDriver](linux-otd-update.md).

After restarting, return to [Start the OTD daemon and check tablet detection](linux-otd-install.md#3-start-the-otd-daemon-and-check-tablet-detection).
