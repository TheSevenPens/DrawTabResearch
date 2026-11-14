# Advanced OpenTabletDriver installation on Linux

Use these options to download a specific release, build from source, or install the official tarball on EndeavourOS or CachyOS. For the recommended path on each distro, see the [Linux install guide](linux-otd-install.md).

## Choose how to get a version

Use the **latest official release** for the current upstream build. Use an **exact GitHub tag** to reproduce a particular release. AUR and distribution repositories select their own package versions. For example, the test on EndeavourOS built `0.6.8` from the AUR while the official GitHub release was `0.6.8.1`. The CachyOS repository build `0.6.8.1-2` is upstream version `0.6.8.1` with CachyOS package revision `2`.

### Download the latest or an exact official release

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

Without `gh`, use the release page and download the asset from **Assets**. The generic `_binary.tar.gz` contains the binaries and system files for a manual install. It requires the runtime and distro-specific device permissions and initramfs setup. Use the generic binary archive for a standalone installation, including when replacing a package after removing it. Upstream describes the `_simple.tar.gz` archive as a way to test binaries on an existing installation. [Latest official release](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/latest) · [Release v0.6.8.1](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/tag/v0.6.8.1) · [Upstream Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux) · [Upstream archive formats](https://github.com/OpenTabletDriver/OpenTabletDriver/blob/v0.6.8.1/README.md#linux)

### Build an exact version locally

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

## Official GitHub tarball on EndeavourOS or CachyOS

Use this route in place of the AUR or CachyOS package when you want an exact upstream release or the current GitHub release. The commands below use the tested `v0.6.8.1` x86-64 archive. For a different release, check its runtime requirements and archive layout before applying these steps. If switching from the Pacman-managed OpenTabletDriver package, [stop its user service and remove the package](linux-otd-uninstall.md) first. Back up any settings you want to keep. [Official v0.6.8.1 release](https://github.com/OpenTabletDriver/OpenTabletDriver/releases/tag/v0.6.8.1)

On an older EndeavourOS Plasma installation, see [the Plasma X11 removal prompt](linux-otd-install.md#endeavouros) before running the dependency command.

```bash
sudo pacman -Syu --needed curl dotnet-runtime-10.0 gtk3 libevdev libx11 libxrandr

archive=opentabletdriver-0.6.8.1_linux-x64_binary.tar.gz
curl -fLO "https://github.com/OpenTabletDriver/OpenTabletDriver/releases/download/v0.6.8.1/$archive"
printf '%s  %s\n' b17929fe2071ab97381706f8f36391312c2495cd1037e1dc121a0aee7abfe1d5 "$archive" | sha256sum -c -
tar -tzf "$archive"
```

Check that the archive checksum reports `OK` before extracting. In the archive listing, the release files are under `opentabletdriver/usr/local/` and `opentabletdriver/etc/udev/rules.d/`, with parent directory entries above them. The extraction command strips the top-level `opentabletdriver/` directory. The launcher scripts expect the binaries under `/usr/local/lib/opentabletdriver/`. Copy the bundled module configuration to `/etc` so the host tools pick it up, then rebuild the boot image. [OpenTabletDriver Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux)

```bash
sudo tar --no-same-owner --no-overwrite-dir --strip-components=1 -xzf "$archive" -C /
sudo install -Dm644 /usr/local/lib/modprobe.d/99-opentabletdriver.conf /etc/modprobe.d/99-opentabletdriver.conf
sudo install -Dm644 /usr/local/lib/modules-load.d/opentabletdriver.conf /etc/modules-load.d/opentabletdriver.conf
/usr/local/bin/otd --version
```

Follow [Rebuild the boot image and restart](linux-otd-install.md#rebuild-the-boot-image-and-restart) for your EndeavourOS or CachyOS setup. The lab also extracted the official tarball on an EndeavourOS systemd-boot copy, rebuilt the boot image, rebooted, checked the CLI version, and enabled the user service. The systemd-boot run did not include a GUI check.

After signing in, follow [Start the driver and check tablet detection](linux-otd-install.md#3-start-the-driver-and-check-tablet-detection). If you previously enabled the Pacman package's service, run `systemctl --user daemon-reload` and `systemctl --user reenable opentabletdriver.service` first to refresh its login symlink. Check the unit path with `systemctl --user show opentabletdriver.service -p FragmentPath`. The tarball's unit is under `/usr/local/lib/systemd/user/`.
