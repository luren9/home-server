
# Layer2 Advertisement error fix

To ensure metallb can respond to ARP requests i needed to change this on the sevrver PC´s end:

First i ran: `sudo nano /etc/sysctl.d/99-metallb.conf` to edit the file.
I then added theese values:

```bash
net.ipv4.conf.all.arp_ignore = 0
net.ipv4.conf.default.arp_ignore = 0

net.ipv4.conf.all.arp_announce = 0
net.ipv4.conf.default.arp_announce = 0
```

Then, theese settings need applied. Running `sudo sysctl --system` works, but its not persistant across reboots. The command IS run automatically on boot, however in my case i noticed the values seem to get overidden somewhere later on in the boot process. I never managed finding exactly where. To fix this (ugly, but simple) i added a crontab like so: `sudo crontab -e` and added the following job:

```bash
@reboot sleep 10 && sudo /usr/sbin/sysctl --system
```

**NOTE**
That command essentially just applies the sysctl configurations again, overriding the override. This is a horrible and ugly solution and something to look at further on. However, this might get automatically mitigated by simply moving to Cilium for loadbalancing and IP-advertisement. So, the migration to Cilium should be done first, if this issue persists after that it will need to be looked at again.
