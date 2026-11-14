# Linux tablet driver VM lab setup

The lab runs disposable Debian amd64 guests under QEMU/KVM on a CachyOS host. A Windows workstation connects to the host over SSH. Vendor packages run inside the guest. The first lab run used Debian 13.7 and tested [Huion, XPPen, and Xencelabs](../investigations/tablet-driver-install-footprint/linux-installer-analysis.md#live-install-and-removal-results).

## 1. Set up and verify the hypervisor

Run these checks locally on the CachyOS host before configuring remote access. The lab launches QEMU directly and uses KVM for hardware acceleration.

1. Check whether Linux sees CPU virtualization and exposes the KVM device.

   ```bash
   grep -m1 -owE 'vmx|svm' /proc/cpuinfo
   ls -l /dev/kvm
   ```

   On the original Intel host, both checks initially failed. We enabled **Intel Virtualization Technology** under **Advanced → CPU Configuration** in the ASUS UEFI, saved, and rebooted. Linux then reported `vmx` and exposed `/dev/kvm`. On AMD systems, look for **SVM Mode**. If the CPU flag is present but the device is still absent, check whether the host loaded the appropriate KVM module (`kvm_intel` or `kvm_amd`).

2. Install QEMU if it is missing. The lab used `sudo pacman -S --needed qemu-base` on CachyOS. Check that `qemu-system-x86_64` and `qemu-img` are available.
3. Run the KVM smoke test as a regular user with access to `/dev/kvm`. It starts a paused guest with no disk and exits after reporting its accelerator.

   ```bash
   printf 'info kvm\nquit\n' | timeout 10 qemu-system-x86_64 \
     -accel kvm -cpu host -m 128 -nodefaults -display none -monitor stdio -S
   ```

   Continue when QEMU reports `kvm support: enabled`. If QEMU reports a permission error, check the device's owner and group. On a host that restricts the device to the `kvm` group, an administrator can add the intended user to that group. Start a new login session before retrying.

[CachyOS QEMU setup](https://wiki.cachyos.org/virtualization/qemu_and_vmm_setup/) · [ASUS virtualization settings](https://www.asus.com/us/support/faq/1045141/) · [QEMU monitor reference](https://www.qemu.org/docs/master/system/monitor.html)

## 2. Set up SSH access

1. From an administrator terminal on CachyOS, run the bootstrap in [the original setup issue](https://github.com/TheSevenPens/DrawTabResearch/issues/3). It installs missing `openssh`, `qemu-base`, and `edk2-ovmf` packages, enables `sshd`, and creates a dedicated `tablet-lab` account without sudo. The lab uses QEMU directly under that account.
2. Generate a dedicated Ed25519 SSH key on Windows. Keep its private half on Windows and supply only the public line to the bootstrap. Before handing over the public key, run `ssh-keygen -y -f <private-key-file>` locally and check that it derives the expected public key. On Windows, also verify that the command used to generate the key handles an empty passphrase as intended if the key is for unattended use.
3. Keep the CachyOS machine awake. Record its LAN address and the host ED25519 fingerprint printed by the bootstrap. Verify the fingerprint before authenticating, then pin that verified host key in a lab-specific `known_hosts` file for future connections.
4. If UFW denies incoming traffic and OpenSSH listens on TCP 22, allow SSH from the Windows workstation’s LAN address. Replace `WINDOWS_LAN_IP` below with that address. No router port forwarding is needed on the same LAN.

```bash
sudo ufw allow from WINDOWS_LAN_IP to any port 22 proto tcp comment 'Tablet VM lab SSH'
```

After the first successful login, repeat the KVM smoke test as `tablet-lab` to verify that the account that will launch guests can use KVM.

### Problems encountered during the first setup

| Symptom | What resolved it |
| --- | --- |
| Windows could reach the host, but SSH timed out. | `sshd` was listening on port 22. UFW's default incoming policy blocked it. Adding the source-specific rule above restored connectivity. |
| Windows `ssh-keyscan` failed even after port 22 became reachable. | The installed Windows scanner selected a key-exchange method it could not use. The regular Windows SSH client negotiated successfully. We saved the host key with client authentication disabled, compared its fingerprint with the value read on CachyOS, and then used strict host checking for the login. |
| The SSH server recognized the public key but login still failed. | The first key-generation invocation produced a private key that the Windows client could not unlock. We generated a replacement, confirmed that it could derive the matching public key, and replaced the lab account's authorized key. |
[OpenSSH server manual](https://man.openbsd.org/sshd.8)

### Keep the CachyOS host awake

On the host, sign in to the KDE Plasma desktop and open **System Settings → Power Management**. In the AC power settings, set **Suspend Session → When inactive → Do nothing**. In **Display and Brightness**, disable **Turn off screen** for sessions where the VM needs to stay visible on the physical monitor. Apply the changes, then verify that SSH remains reachable and the monitor stays on past the old timeout. The desktop power settings belong to the signed-in user. The separate `tablet-lab` SSH account could neither change those settings nor acquire a system sleep inhibitor in this setup.

The host suspended during a fresh EndeavourOS installation and SSH stopped responding. The host user woke it and applied both AC power settings from the KDE desktop. The guest installer resumed from where it had paused.

[KDE Plasma Power Management](https://docs.kde.org/stable_kf6/en/powerdevil/kcontrol/powerdevil/)

## 3. Provision a guest and run the tests

1. Download Debian's generic amd64 cloud QCOW2 image and its published `SHA512SUMS` over HTTPS. Verify the image with the matching SHA-512 entry. Store it under `~/vm-lab/images/` as the base image.
2. For each run, create a new directory under `~/vm-lab/` and a writable QCOW2 overlay backed by that image. The initial tests used a 20 GiB virtual disk, 2 GiB RAM, and two virtual CPUs.
3. Create a cloud-init NoCloud seed with per-guest SSH keys. We used a small FAT image labeled `CIDATA`, populated with `mkfs.vfat` and `mcopy`. Boot QEMU with `-accel kvm -cpu host`, attach the overlay and seed, save the serial console to a log, and forward guest SSH to a loopback port on the CachyOS host. Use the guest's expected host key when connecting. The initial smoke test verified cloud-init completion, Debian version, architecture, SSH, and remote shutdown.
4. Stage the exact inventoried DEB, verify its SHA-256 in the guest, then capture baseline, installed, removed, and post-restart states. Record commands and exit statuses alongside filesystem paths, permissions, selected hashes, dpkg status, and systemd unit state. For these tests, use `apt-get install ./<file>.deb` and `apt-get remove <package>`. Read dpkg's package name from the guest so the removal command uses its exact spelling. Record guest boot IDs to verify the restart. Check session and filesystem prerequisites before the baseline when testing a conditional branch.
5. Export evidence to the CachyOS host before cleanup and verify the archive is readable. Shut down the guest, discard the used overlay, and verify the base image still matches its SHA-512. The next run begins from a fresh overlay.

The original runs used short shell scripts for image verification, cloud-init seeding and VM launch, and guest-side capture. When streaming a setup script to the host through SSH, give nested SSH commands that only run a remote command `-n` or redirect their standard input from `/dev/null`. Give QEMU's daemonized launch its own standard input as well. This avoids consuming the parent script from the SSH stream.

[Debian cloud images](https://cloud.debian.org/images/cloud/) · [NoCloud configuration](https://docs.cloud-init.io/en/latest/reference/datasources/nocloud.html) · [QEMU disk image utility](https://www.qemu.org/docs/master/tools/qemu-img.html)

## 4. Show and control the same guest desktop

Start the guest from a writable overlay and install a Debian desktop such as Xfce. Give the guest a virtual display and start QEMU with a VNC listener bound to host loopback, for example `-vnc 127.0.0.1:5`. Display 5 uses TCP port 5905. A viewer in the signed-in CachyOS desktop session can open `127.0.0.1:5` (or enter port 5905 explicitly). The viewer window shows the Debian desktop on the physical monitor.

For remote control, forward that same VNC port over the existing SSH connection. For example, with the lab identity and host key configured under an SSH alias named `tablet-lab-host`:

```bash
ssh -N -L 127.0.0.1:5905:127.0.0.1:5905 tablet-lab-host
```

Open the remote viewer in shared mode so it can connect alongside the local viewer. Both viewers show the same guest desktop, including any pointer or keyboard input sent remotely. Launch the local viewer from the host user's graphical session. Some desktop sessions require that user to open the viewer or approve access. For screenshots or scripted interaction, QEMU can also expose a monitor on a private Unix socket to capture the guest framebuffer and send input.

The lab used LightDM and Xfce inside Debian. On the CachyOS desktop, Firefox served as the viewer using a local noVNC page. The page and the QEMU display listeners were bound to loopback. With QEMU's direct WebSocket listener, connect noVNC to the listener's root path. The default `/websockify` path is for a separate proxy and returned HTTP 404 in this setup. The host's graphical session ran under a different account from `tablet-lab`, so the signed-in user opened the viewer. From SSH, we started the OpenTabletDriver user service and opened the app on the guest's Xfce display, then verified the result with a QEMU framebuffer capture.

[Debian Xfce desktop package](https://packages.debian.org/trixie/task-xfce-desktop) · [QEMU display options](https://www.qemu.org/docs/master/system/invocation.html) · [QEMU monitor commands](https://www.qemu.org/docs/master/system/monitor.html) · [noVNC documentation](https://novnc.com/noVNC/)

## Tailscale for future lab setups

Use Tailscale for remote access in future lab setups. Enroll the Windows control machine and the CachyOS host in the same private Tailscale network, then authorize access to the lab host. This avoids coordinating LAN addresses and maintaining a UFW rule tied to the Windows machine's LAN IP.

- **OpenSSH over Tailscale** can reuse the working account, client key, and host verification. Allow access through the host firewall on the Tailscale interface if needed.
- **Tailscale SSH** can simplify setup further by handling SSH authentication through Tailscale policy. Enable it on CachyOS and grant the intended user access to the `tablet-lab` account. Verify unattended login before scheduling overnight tests since interactive reauthentication can interrupt jobs.

The first lab used LAN OpenSSH. Tailscale is planned for the next setup and has yet to be tested in this lab.

[Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh) · [OpenSSH over Tailscale](https://tailscale.com/docs/reference/ssh-over-tailscale)

## RAM-backed VM disks for future tests

The CachyOS host had 62 GiB of RAM and a `tmpfs` mounted at `/dev/shm` with a 32 GiB limit when measured. For repeatable driver tests, keep the prepared base images on the SSD and create each run's writable QCOW2 overlay in a private directory under `/dev/shm`. QEMU reads existing blocks from the base and writes changes to the overlay. Most overlays from the Linux driver removal tests used about 140–270 MiB each on disk. A RAM-backed overlay reduces SSD writes from the guest. Its size grows with the writes, and the running guest needs its own memory as well.

Store logs and other evidence under `~/vm-lab/` before discarding the overlay. The overlay survives a guest reboot while the host remains up. Its contents disappear when the host reboots or the filesystem is unmounted.

To measure whether RAM storage speeds up a fresh OS install, run one VM at a time and compare the same installer and VM settings against an SSD-backed run. Allow extra space for writes during installation and updates. The existing host images occupy about 1.6 GiB for Debian, 2.1 GiB for Fedora, 15.3 GiB for EndeavourOS, and 8.4 GiB for CachyOS. These are observed sizes and can differ from peak usage during an install. RAM-backed runs and install speed have yet to be tested.

[Linux tmpfs documentation](https://docs.kernel.org/filesystems/tmpfs.html) · [QEMU backing files](https://qemu.readthedocs.io/en/master/tools/qemu-img.html)
