---

kanban-plugin: board

---

## Backlog

- [ ] Add [[datree]] to strictly enforce secure maifests and policies
- [ ] Implement [[ELK-stack]] or maybe the LGTM or LOKI stack?
- [ ] Implement/look in to [[n8n]]
- [ ] Explore UIs for [[cert-manager]]
- [ ] Limit [[helm]] apply usage strictly to [[helmfile]] files
- [ ] Selfhost [[DNS]] to avoid mapping each ingress-name to k8s LB-IP
- [ ] See if there are any good Vscode extensions for working with helm, especially to find which chart values can be overidden
- [ ] Add [[ansible]] playbook for full enviroment setup
- [ ] Look at some cool [[tools]]
- [ ] Ingress-nginx deprecated?
- [ ] Terraform + AWS Route 53 to manage DNS for home cluster Maybe only for apps in prod ns?
- [ ] Terraform + AWS for deploying AI cluster watcher
- [ ] Migrate from [[bitnamilegacy]] docker image repository. Repository is fully deprecated.
- [ ] Add [[code-file linking]] in obsidian.
- [ ] Improve ArgoCD security (user accounts and so on)
- [ ] Look over this file:
	kubernetes/apps/velero/velero-credentials-secret.yaml
- [ ] Look over this file and add this to main README on how to bootstrap cluster:
	kubernetes/apps/metallb/README.md


## To Do

- [ ] Look in to local-path-storage pvc-tester mass-restarts
- [ ] Add tool for calculating power consumption & cost
- [ ] Move all `README.md` files onto obsidian notes with proper naming
- [ ] Give root-level `README.md` a major makeover, make it cool and explain obsidian usage.
- [ ] Add argocd application for syncing argocd application manifests. Should maybe live in the argocd bootstrap folder.
	Add to readme that this needs to be manually applied once on server setup
- [ ] Setup GitLab CE or something similar - self hosted repo yes sir.
	Then set up push-mirroring to github + description of where development is happening on github


## In Progress

- [ ] Terraform, AWS & Velero for cluster backups/disaster recovery. [[Backup-cluster]]


## Done

**Complete**
- [x] Setup [[ArgoCD]]
- [x] *CANCELLED (we will move away from helmfile to ArgoCD, this will fix the issue)* Fix [[cilium]] and [[harbor]] helm-version updating everytime i apply [[helmfile]]
- [x] Move from using [[helmfile]] to argoCD to mange helm.




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false]}
```
%%