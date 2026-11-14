# Linux tablet driver VM lab setup

The lab runs disposable Debian amd64 guests under QEMU/KVM on a CachyOS host. A Windows workstation connects to the host over SSH. Vendor packages run inside the guest. The first lab run used Debian 13.7 and tested [Huion, XPPen, and Xencelabs](linux-installer-analysis.md#live-install-and-removal-results).

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

## 3. Provision a guest and run the tests

1. Download Debian's generic amd64 cloud QCOW2 image and its published `SHA512SUMS` over HTTPS. Verify the image with the matching SHA-512 entry. Store it under `~/vm-lab/images/` as the base image.
2. For each run, create a new directory under `~/vm-lab/` and a writable QCOW2 overlay backed by that image. The initial tests used a 20 GiB virtual disk, 2 GiB RAM, and two virtual CPUs.
3. Create a cloud-init NoCloud seed with per-guest SSH keys. We used a small FAT image labeled `CIDATA`, populated with `mkfs.vfat` and `mcopy`. Boot QEMU with `-accel kvm -cpu host`, attach the overlay and seed, save the serial console to a log, and forward guest SSH to a loopback port on the CachyOS host. Use the guest's expected host key when connecting. The initial smoke test verified cloud-init completion, Debian version, architecture, SSH, and remote shutdown.
4. Stage the exact inventoried DEB, verify its SHA-256 in the guest, then capture baseline, installed, removed, and post-restart states. Record commands and exit statuses alongside filesystem paths, permissions, selected hashes, dpkg status, and systemd unit state. For these tests, use `apt-get install ./<file>.deb` and `apt-get remove <package>`. Read dpkg's package name from the guest so the removal command uses its exact spelling. Record guest boot IDs to verify the restart. Check session and filesystem prerequisites before the baseline when testing a conditional branch.
5. Export evidence to the CachyOS host before cleanup and verify the archive is readable. Shut down the guest, discard the used overlay, and verify the base image still matches its SHA-512. The next run begins from a fresh overlay.

The original runs used short shell scripts for image verification, cloud-init seeding and VM launch, and guest-side capture. When streaming a setup script to the host through SSH, give nested SSH commands that only run a remote command `-n` or redirect their standard input from `/dev/null`. Give QEMU's daemonized launch its own standard input as well. This avoids consuming the parent script from the SSH stream.

[Debian cloud images](https://cloud.debian.org/images/cloud/) · [NoCloud configuration](https://docs.cloud-init.io/en/latest/reference/datasources/nocloud.html) · [QEMU disk image utility](https://www.qemu.org/docs/master/tools/qemu-img.html)

## Tailscale for a future setup

Tailscale could simplify reaching the host from other networks. Enroll both Windows and CachyOS on the same private Tailscale network and authorize access from the Windows device to the lab host. That would replace dependence on the current LAN addresses and the UFW rule tied to the Windows LAN IP.

- **OpenSSH over Tailscale** would reuse the working account, client key, and host verification. Allow access through the host firewall on the Tailscale interface if needed.
- **Tailscale SSH** could also replace manual user-key distribution. It requires enabling Tailscale SSH on CachyOS and granting the intended user access to the `tablet-lab` account in the Tailscale policy. A policy that requires interactive reauthentication can interrupt unattended jobs.

The host still needs to be awake and configured for KVM, and Debian provisioning and evidence capture follow the same steps. The first lab used LAN OpenSSH. Tailscale is a future option.

[Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh) · [OpenSSH over Tailscale](https://tailscale.com/docs/reference/ssh-over-tailscale)
