---

kanban-plugin: board

---

## Backlog

- [ ] Implement/look in to [[n8n]]
- [ ] Limit [[helm]] apply usage strictly to [[helmfile]] files
- [ ] Selfhost [[DNS]] to avoid mapping each ingress-name to k8s LB-IP
- [ ] Add [[ansible]] playbook for full enviroment setup
- [ ] Look at some cool [[tools]]
- [ ] Ingress-nginx deprecated?
- [ ] Terraform + AWS Route 53 to manage DNS for home cluster Maybe only for apps in prod ns?
- [ ] Terraform + AWS for deploying AI cluster watcher


## To Do

- [ ] Implement [[ELK-stack]]
- [ ] Explore UIs for [[cert-manager]]
- [ ] Fix [[cilium]] and [[harbor]] helm-version updating everytime i apply [[helmfile]]
- [ ] Add [[datree]] to strictly enforce secure maifests and policies
- [ ] Look in to local-path-storage pvc-tester mass-restarts
- [ ] See if there are any good Vscode extensions for working with helm, especially to find which chart values can be overidden
- [ ] Add tool for calculating power consumption & cost


## In Progress

- [ ] Terraform + AWS for cluster-bootstrap artifacts & app-data backups. Can argo handle the cloud calls?
- [ ] Setup [[ArgoCD]]


## Done

**Complete**




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false]}
```
%%