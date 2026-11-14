# Linux drawing tablet installer analysis

This analysis covers three official x86-64 Debian packages from Huion, XPPen, and Xencelabs. All three declare a userspace application, an application-menu launcher, a desktop-session autostart entry, and a udev rule. The [live removal results](#live-install-and-removal-results) record what the same packages left behind in Debian 13.7 VMs.

## Packages inspected

| Brand | Vendor release | DEB package name and version | SHA-256 of the inspected DEB |
| --- | --- | --- | --- |
| Huion | `15.0.0.193` | `HuionTablet`, `15.0.0.193` | `cc563c2358dd0ba13c245f97341d20fecfa8509bfa5c75c8258c895f48b6fa02` |
| XPPen | `4.0.15-260422` | `XPPenLinux`, `4.0` | `414cc9ffb9855520d31874b767920472893af0692b79f851f36c26dc2894aecb` |
| Xencelabs | `1.3.4-26` | `xencelabs`, `1.3.4` | `f2c0094b95fd9af271325d5ac1ebc67cf32a8f4e1160fc5207390db1190f3148` |

Each package declares `amd64`, and the main executables have x86-64 ELF headers. The XPPen and Xencelabs DEB versions omit details present in the vendor release identifiers. Use the DEB hash to distinguish exact samples. The vendor links and file records are in the [Linux inventory](linux-tablet-driver-filesystem.json).

## Declared filesystem paths

| Brand | Application and helpers | Menu and login autostart | Device integration |
| --- | --- | --- | --- |
| Huion | `/usr/lib/huiontablet/` contains `huiontablet`, `huionCore`, their shell wrappers, and a bundled copy of `xdotool` under `xdotool/`. | `/usr/share/applications/huiontablet.desktop` and `/etc/xdg/autostart/huiontablet.desktop` call `huiontablet.sh` with `manual_launch` and `autostart` respectively. | `/usr/lib/udev/rules.d/20-huion.rules`. The package also includes a copy under the application’s `res/rule/` directory. |
| XPPen | `/usr/lib/pentablet/` contains `PenTablet`, `PenTablet.sh`, bundled libraries, and configuration under `conf/xppen/`. | `/usr/share/applications/xppentablet.desktop` and `/etc/xdg/autostart/xppentablet.desktop` call `PenTablet.sh`. The autostart entry adds `/mini`. | `/lib/udev/rules.d/10-xp-pen.rules`. |
| Xencelabs | `/usr/lib/xencelabs/` contains `xencelabs`, `start.sh`, and `restar.sh`. | `/usr/share/applications/xencelabs.desktop` and `/etc/xdg/autostart/xencelabs.desktop` both call `start.sh`. | `/lib/udev/rules.d/10-xencelabs.rules` and `/etc/systemd/system/xencelabs.service`. The unit runs `restar.sh` and declares `WantedBy=multi-user.target`. |

These paths are from the package archives. On distributions where `/lib` resolves to `/usr/lib`, the different udev prefixes can resolve into the same directory. Xencelabs is the only sampled DEB that contains a systemd unit.

## What the package scripts do

### Huion

The `postinst` script conditionally copies the bundled `xdotool` to `/bin/xdotool` and `libxdo.so.3` to `/usr/lib/libxdo.so.3` if the respective files are absent. It also checks a distribution-specific destination for the library, `/lib/x86_64-linux-gnu/libxdo.so.3` on Ubuntu or `/usr/lib64/libxdo.so.3` on CentOS. If `/etc/bluetooth/input.conf` exists, the script uncomments a matching `#UserspaceHID=true` line.

The removal scripts attempt to stop the app processes and clean up the application directory, udev rule, and selected per-user PID and log files. The inspected removal scripts contain no corresponding reversal for the copied system tools and libraries or the Bluetooth configuration edit. [Huion DEB download](https://driverdl.huion.com/driver/Linux/HuionTablet_LinuxDriver_v15.0.0.193.x86_64.deb)

### XPPen

The `postinst` script runs permission changes on selected launchers, app files, bundled libraries, and configuration directories. Its commands add write permissions for all users to the selected paths. The same script creates `/tmp/qtsingleapp-Pentab-9c9b-lockfile`. The `prerm` script attempts to remove that lockfile, and `postrm` prints a completion message.

The `preinst` script also attempts to delete `/var/lib/dpkg/lock` and `/var/lib/dpkg/lock-frontend` if present. [XPPen Deco Pro SW/MW downloads](https://www.xp-pen.com/download/deco-pro-sw-mw.html)

### Xencelabs

The `postinst` script takes the first username from `who` and tries to copy the bundled configuration into `/home/<user>/.local/share/xencelabs/config/`. It changes permissions on the data directory and the copied configuration and creates `/tmp/qtsingleapp-Xencel-fb8d-lockfile`. Which account receives the copy depends on the sessions visible to `who` when the script runs.

The `postrm` script attempts to remove the lockfile. The `prerm` script exits before reaching its later block that would delete the user-data directory. [Xencelabs downloads](https://www.xencelabs.com/us/support/download-drivers)

## Live install and removal results

Each package was tested in a fresh, headless Debian 13.7 amd64 VM with kernel `6.12.116+deb13-amd64`, an SSH login, and no tablet connected. The installer SHA-256 matched the table above in every run. We used `apt-get install ./<file>.deb` and `apt-get remove <package>` with the package names reported by APT (`huiontablet`, `xppenlinux`, and `xencelabs`). We captured filesystem paths and permissions, package and unit state, selected file hashes, and package-manager logs at baseline, after install, after removal, and after restart. Install and removal returned exit status 0 for the runs below.

| Build | Gone after removal and restart | Still present after restart |
| --- | --- | --- |
| Huion `15.0.0.193` | App directory, menu entry, login autostart entry, and udev rule | `/usr/bin/xdotool` (also reachable through `/bin`) and `/usr/lib/libxdo.so.3`. In the BlueZ run, the edit to `/etc/bluetooth/input.conf` also persisted. |
| XPPen `4.0.15-260422` | App directory, menu entry, login autostart entry, udev rule, and `/tmp/qtsingleapp-Pentab-9c9b-lockfile` | Residual dpkg metadata. The two dpkg lock paths existed again after removal, with different inode numbers from baseline. |
| Xencelabs `1.3.4-26` | App directory, menu entry, login autostart entry, udev rule, systemd unit, and `/tmp/qtsingleapp-Xencel-fb8d-lockfile` | In the run with `~/.local/share` prepared, all 18 files copied to `~/.local/share/xencelabs/config/` remained with identical SHA-256 hashes. |

All three packages showed dpkg status `rc` after removal, indicating residual package metadata under this APT removal procedure. Huion and Xencelabs retained the additional files listed above outside dpkg’s tracked payload. [Debian apt-get manual](https://manpages.debian.org/trixie/apt/apt-get.8.en.html)

- **Huion.** The two helpers were absent before installation and retained their hashes after removal and restart. Neither had a dpkg owner. With BlueZ installed, the installer changed `#UserspaceHID=true` to `UserspaceHID=true` in BlueZ’s config file. Without BlueZ, the file was absent throughout. The app directory, both desktop entries, and the udev rule had mode `0777` while installed. APT reported success despite a missing `update-desktop-database` command in the installer log.
- **XPPen.** At the post-install checkpoint, `/var/lib/dpkg/lock-frontend` was absent and `/var/lib/dpkg/lock` had a different inode. APT recreated the frontend lock file during successful removal. The main executable, launch script, and both desktop entries had mode `0777` while installed.
- **Xencelabs.** The systemd unit was loaded, disabled, and inactive at the post-install checkpoint. In the first run, the installer selected the SSH login user from `who`, then logged directory-creation and copy errors because `~/.local` was absent. APT still reported success. In the prepared-home run, the copied files included `config.xml`, `Template.xml`, translations, and images. The remaining `~/.local/share/xencelabs/` directory was owned by `root:root` with mode `0777`.

These runs cover APT removal of the three sampled DEBs. APT purge, graphical login and first launch, physical tablet detection and pen input, multi-driver installs, and RPM and tar installer paths remain untested here. Wacom’s Linux coverage concerns the native Linux driver stack. [Wacom Linux support guidance](https://support.wacom.com/hc/en-us/articles/1500006331202-Does-Wacom-have-a-Tablet-Driver-that-will-support-Linux)

See the [investigation methodology](README.md) for how the files were extracted and identified.
