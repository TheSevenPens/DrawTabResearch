# Troubleshoot OpenTabletDriver on Linux

If the app cannot connect to the daemon or the tablet is missing, inspect the user service log. Look for messages about `/dev/uinput`, `/dev/hidraw*`, or a conflicting driver. [OpenTabletDriver Linux troubleshooting](https://opentabletdriver.net/Wiki/FAQ/Linux)

If you launched the app from a terminal, open a second terminal to run the log command while the app stays open.

```bash
journalctl --user -u opentabletdriver.service -b --no-pager
```

The packaged service checks for `WAYLAND_DISPLAY` or `DISPLAY` in the systemd user environment. A start requested over SSH can be skipped if neither variable is set. Check the status from the desktop session where you plan to use the tablet.

| What you see | What to check |
| --- | --- |
| Nothing changes in `lsusb` when you plug in the tablet | Try another USB port or a known data cable. If the command is missing, install the `usbutils` package with your distro's package manager. [Upstream USB checks](https://opentabletdriver.net/Wiki/FAQ/General#tablet-not-detected) |
| The log reports another tablet driver or denied access to `/dev/hidraw*` | Check for a running vendor driver, then verify the installed udev rules and kernel module configuration. [Upstream Linux permissions](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux) |
| Virtual tablet initialization fails with `ENODEV`, `ENOENT`, or `EACCES` | Upstream maps those errors to a missing device, missing kernel support, and denied access respectively. Check the matching fix. [Upstream Linux troubleshooting](https://opentabletdriver.net/Wiki/FAQ/Linux#fail-virtual-device) |
| Mapping is wrong with multiple monitors | Have either the desktop tablet settings or OpenTabletDriver map to all screens, then set your target area in the other. [Upstream multi-monitor steps](https://opentabletdriver.net/Wiki/FAQ/Linux#multi-monitor-mapping-issues) |

## Device permissions and driver conflicts

If Linux detects your tablet but OpenTabletDriver cannot access it, check for a permissions issue or a driver conflict. Older udev rules, which help Linux decide which users can access a device, can be one cause.

For legacy udev rules, kernel module conflicts, and permissions troubleshooting, see OpenTabletDriver’s [Linux permissions guide](https://opentabletdriver.net/Wiki/Documentation/RequiredPermissions#linux) and [Linux FAQ](https://opentabletdriver.net/Wiki/FAQ/Linux).
