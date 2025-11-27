We need to find a way to abstract away from having to add each
ingress name to the windows hosts file and map it to the static [[MetalLB]] LoadBalancer IP:
```powershell
"C:\Windows\System32\drivers\etc\hosts"
```

## 1st Solution (Wont work, router is locked down):
I could setup my own DNS, either through pi-hole or through AdGuard. The router should point to primarily use this custom DNS and use the ISP-default one as a backup. I want the custom DNS to run inside the kubernetes cluster but I really need to consider the security risks of it. If someone controls my kubernetes cluster they will be able to quietly re-route name look-ups to fake sites, like mapping `bank.com --> hacker´s server`. So I need to consider this, be really careful, but I still want to try it. Also, I should have in mind that I WILL be port-forwarding something, i'm not sure exactly what yet, but basically the cluster will in some way or form be open to the internet, so I need to be careful about hosting the a global Home-DNS server on it.
--> better understanding below

## 2nd Solution (Works + good experience, but insecure and unstable):
No, I cannot change the primary DNS of the router and point that to a self-hosted one in my cluster. The router was given by ISP and is fully locked down and really annoying. What I would need to do is turn of the entire DHCP-server of the router and instead choose to host it fully on my own. I could then hypothetically run it inside the cluster and have all devices on the network rely on that DHCP server. But that's the problem, it would make the network rely on that cluster-running DHCP server. If it were to go down, like server PC gets shut off --> no more internet for anyone on the WiFi! Or, at least no new ips or renewals will be handed out by DHCP. So, whatever IP devices have they will keep until lease time is over. One really ugly change to mitigate that would be to increase the lease-time of each handed out IP...


## 3rd Solution (Works - costs money, secure and stable)
What I could do too, is just purchase a more customizeable router and setup a simple wildcard-policy for its built in DNS server. I'm a little unsure if my ISP allows this, it would have to be looked in to. Worst case I can use old router as modem and hook the "new" router and use that as the main router so to say. Though this might add latency and be slow? Hmm i'm not sure at all.


## TEMP Solution (The one currently used)
Keep editing windows hosts file and download a DNS changer app on phone. A little scary tho so i need to be careful!
