# Install OpenTabletDriver on Fedora 45

First, follow [Prepare your system](linux-otd-install.md#1-prepare-your-system). Run the commands below in order in the same Bash terminal. Use `sudo -v` to check that your account can install packages.

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

For an RPM downloaded from GitHub, get new OpenTabletDriver releases manually. See [Update OpenTabletDriver](linux-otd-update.md).

After restarting, return to [Start the OTD daemon and check tablet detection](linux-otd-install.md#3-start-the-otd-daemon-and-check-tablet-detection).
