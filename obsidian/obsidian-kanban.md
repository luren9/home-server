---

kanban-plugin: board

---

## Backlog

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


## To Do

- [ ] Implement [[ELK-stack]] or maybe the LGTM stack?
- [ ] Add [[datree]] to strictly enforce secure maifests and policies
- [ ] Look in to local-path-storage pvc-tester mass-restarts
- [ ] Add tool for calculating power consumption & cost
- [ ] Move all `README.md` files onto obsidian notes with proper naming
- [ ] Give root-level `README.md` a major makeover, make it cool and explain obsidian usage.
- [ ] Move from using [[helmfile]] to argoCD to mange helm.


## In Progress

- [ ] Terraform + AWS for cluster-bootstrap artifacts & app-data backups. Can argo handle the cloud calls? [[Backup-cluster]]
- [ ] Setup [[ArgoCD]]


## Done

**Complete**
- [x] *CANCELLED (we will move away from helmfile to ArgoCD, this will fix the issue)* Fix [[cilium]] and [[harbor]] helm-version updating everytime i apply [[helmfile]]




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false]}
```
%%