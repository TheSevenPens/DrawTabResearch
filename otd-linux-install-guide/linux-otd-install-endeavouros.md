# Install OpenTabletDriver on EndeavourOS

First, follow [Prepare your system](linux-otd-install.md#1-prepare-your-system). Run the commands below in order in the same Bash terminal. Use `sudo -v` to check that your account can install packages.

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

Follow the [boot-image rebuild and restart instructions](linux-otd-install.md#preventing-built-in-linux-drivers-from-interfering-with-otd). That section shows how to choose the EndeavourOS command for your bootloader. [OpenTabletDriver EndeavourOS instructions](https://opentabletdriver.net/Wiki/Install/Linux#endeavouros)

After restarting, return to [Start the OTD daemon and check tablet detection](linux-otd-install.md#3-start-the-otd-daemon-and-check-tablet-detection).
