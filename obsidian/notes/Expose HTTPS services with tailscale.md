Doing this with tailscale ingress proxygroups is a mess when it comes to complex helm deployments like Harbor.
In the case of harbor there are multiple pods where diffrent apis route to diffrent pods, each one of theese rules which originate from the buried manifests under the helm chart would need to be manually ovcerriden and would defeat the purpose of using helm.

The solution, expose the entire cluster as is and let tailscale only solve the networking problem like so:

Laptop
	│
Tailscale
    │
Home subnet
    │
192.168.0.241 (metallb)
    │
NGINX
    │
Harbor

Tailscale subnet router usage here.

The kubernetes cluster doesnt even need to know tailscale exists (except for the api-server access which is already setup)

## DNS

How do i make harbor.home resolve to my home ip?

I will manually configure Tailscale DNS so that

harbor.home --> resolves to --> 192.168.0.241


## Result

Nothing needs to change and everything just works.