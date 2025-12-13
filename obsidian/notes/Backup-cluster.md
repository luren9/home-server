## Introduction
I have been going through i think about ten different "Aha!" moments where i have though that i finally found the golden path to kubernetes cluster disaster recovery, every single time i realized quite quickly how wrong i was.

Now for the 11th iteration of this architectural idea I have yet to manage to convince myself that this version in my head is all bad, at least not yet. Though im excited to learn what i missed, which i surely did right? haha ;)

If i do not find a problem in this architecture, i will start building and running with it!

## Requirement & Ideology
I want a way to recover from major disasters. I'm not talking about the disaster of a pod crashing, that's for kubernetes reconciliation controllers to fix. I'm talking about the problem of lets say, my server PC blowing up.

I'm not necessarily scared of my DR system being slow or complicated, though i do care about how they scale with cluster complexity. With this i mean, im okay with some downtime and manual work in a disaster case, so long as the manual work doesn't scale with the amount of systems i host on my cluster.

I want some DR which adheres to the GitOps ideology. I don't want to save my WHOLE cluster state and reapply that to a new cluster because that is not the GitOps way (besides im pretty sure it wouldn't even work). The GitOps way, done correctly, should allow me to rebuild my cluster from my declarative manifests at least as far as my ephemeral apps go. This means that if i ever deploy an app by surpassing the GitOps processes, then that app wouldn't exist upon cluster recreation. This forces me to truly work the GitOps-way and i believe its the right way to go. 

## My core idea
Completely divide the mental model of data in the cluster into two categories:
* **Persistent Data** (`pvc`, `pv`, and `secret`)
And:
* **Ephemeral State** (`deployment`, `statefulset`, `daemonset`, `services`, ...)

The **Persistent data** should be fully owned and managed by a **Backup-tool** (Velero).
The **Ephemeral State** should be fully owned and managed by **GitOps** (git + ArgoCD)

Backups will be created by Velero through: 
```Bash
velero backup create <backup-name> \
  --exclude-namespaces default,kube-system,<ns1,ns2,...> \
  --include-resources persistentvolumeclaims,persistentvolumes,secrets
```
Where the namespaces to exclude would be namespaces which state we don't care about, like the kube-system that never should be backed up. 
This would of course be scheduled according to needs and so on.

Everything else, everything everything else should already be backed up declaratively with the Git repository (the GitOps way). (Lets skip DR for git repo here, though that might be good aswell.)

When recovering a disaster the idea is to then first apply all **Persistent data** to the cluster and then after that apply all **Ephemeral state**. This will be handled through ArgoCD and the exact order is better explained later. 

Important is that ArgoCD *must* be configured NOT to apply/mange any `pv`, `pvc` or `secret` manifests at all. This is because helm chart deployments often try to create these, if they do they will fail the helm installations with errors like `pvc already exists`. Instead of manually overriding each helm-values file with flags to avoid generating pvc-manifests, we can simply ignore them *all* with ArgoCD. So, helm still creates and presents manifests for managing PVCs, but ArgoCD ultimatley ignores them, so they never get applied. 

Another important thing to note here is that, the *first* time (not including *first-times* for cluster recreations) helm installations occur, the PVC's must be applied, so some manual & temporary override of the ArgoCD ignore policy must be done upon first adding a new helm application.

## Workflow/restoration steps
Here are the workflow/restorations steps that needs to be taken to correctly *recreate* the kubernetes cluster with the data from the latest Velero backup.
1. Create new kubernetes cluster
2. Manually run helm install for Velero using git-repo's `values.yaml` file.
3. Manually create secret in `velero` namespace that contains cloud credentials (needed for Velero to access cloud-bucket)
4. Run full scale Velero restoration from latest backup. `velero restore create <backup_restoration_name> --from-backup <latest_backup_name>`(will create all namespaces and populate them with `pv`, `pvc` & `secret`'s)
5. Manually run helm install for ArgoCD using git-repo's `values.yaml` file. Then let ArgoCD bootstrap/create all deployments, services and so on from the manifests in the repo. They should all automatically bind to the already existing pvc's. Argo shouldn't have created any new pvcs at all.
   **Note:** Beyond this point no more manual applying should be allowed. Everything past this point should be handled by ArgoCD, the GitOps way.
6. Done!

## Problems
As with most solutions, there are some potential problems with this architecture. These are the ones i can see so far:

1. Loss/recreation of k8s metadata.
   If any services are dependent on k8s app metadata like ID's, recreation will be problematic. 
   **Solution:** This is not a problem in 99% of cases and when it is, that service is absolute at fault and should in no circumstance be used in the first place as they break the fundamental strategy of kubernetes.