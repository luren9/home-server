
# Manual edit on bare-metal PC needed.
On each bare metal server PC running clusters nodes, the cer-manager root certificate authority certificate needs to be installed. This is done like so:

```sh
scp rootCA.crt <SERVER_HOSTNAME>:/usr/local/share/ca-certificates/
sudo update-ca-certificates
```

This step should be automated, maybe through an ansible playbook.
