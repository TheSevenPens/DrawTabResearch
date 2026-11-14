# Start OpenTabletDriver automatically at desktop login

After [installing OpenTabletDriver](linux-otd-install.md), enable the user service and check whether your desktop supports this startup method.

```bash
systemctl --user enable opentabletdriver.service
systemctl --user is-active graphical-session.target
```

If the desktop check prints `active`, the enabled service starts at login. This worked on **Pop!_OS with COSMIC Wayland**, **Fedora Workstation with GNOME Wayland**, **EndeavourOS with Plasma Wayland**, and **CachyOS with Plasma Wayland**.

If the check prints `inactive` on a desktop other than Xfce, see the [upstream autostart guidance](https://opentabletdriver.net/Wiki/FAQ/Linux#autostart).

## Xfce login entry

If the desktop check prints `inactive` on **Xfce**, add the login entry below. This was verified on Debian and Fedora.

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/opentabletdriver-xfce.desktop <<'DESKTOP'
[Desktop Entry]
Type=Application
Name=OpenTabletDriver Daemon
Exec=systemctl --user start opentabletdriver.service
OnlyShowIn=XFCE;
DESKTOP
```

## Verify automatic startup

Restart and sign in. After the desktop finishes loading, run `systemctl --user is-active opentabletdriver.service` and `systemctl --user is-enabled opentabletdriver.service`. Expect `active` and `enabled`, respectively. [OpenTabletDriver guidance on desktop autostart](https://opentabletdriver.net/Wiki/FAQ/Linux#autostart)
