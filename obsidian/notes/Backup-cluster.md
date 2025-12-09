
### Standardized k8s cluster backup solution?
There is no perfect solution that is standardized. The best backup measures that can be made to a cluster depend on requirements, complexity toleration and amount of time that can be spent setting them up. There is no fool-proof plug-n-play solution, in fact there is no fully fool-proof system at all. Its kind of like looking for a package to install that would make a large system fully unexploited out of the box, Its just not possible. 

So data-recovery and cyber-security share a common approach. Perfection isn't possible so we don't even try to go there. Instead we try to add layers on layers on layers to eventually be able to sleep at nights with 99,9...% trust in our system. Each new layer makes the catastrophe chance smaller, but it never removes it fully.

### Case
In my case, I really don't need to avoid data-loss, really. But i want to. Because i want to simulate how enterprises would and see how backupsystems might work. So, I will setup some requirements that I think could apply to larger organisations. Though, i will not go full bank-system/healthcare grade.

Here is the requirements for the cluster backups i will setup:

#### Requirements
* Should cover the entirety of the kubernetes cluster, meaning every node across any server-PC/cloud instance.
* Data restoration must be precise to the point where an end-user interacting with a service hosted on the cluster wouldn't notice any difference between restored and the original cluster 
* The backups should be done once every day.
* Backed up data needs to be paired with location, so that a restoring developer can restore the correct data at the correct spots. Example, a PVC's data must be paired with where this PVC should exist, what its called and so on.
* Whilst the cluster restoration mustn't be a fast process per say, it shouldn't scale with cluster complexity and size in terms of developer time. For example, a developer shouldn't have to manually restore each backed up PVC in their places one by one.

#### Non-requirements
* Cluster restoration must not be fast or automated, some manual work and downtime is expected and okay.
* Things like k8s resource IDs must not persist, meaning they can be recreated.
* Each deployment and app is ephemeral, so their states do not need to be backed up. Only data in PVC's need backing up.


## Velero
To meet our needs the choice is to go with Velero.
Velero will essentially regularly take snapshots of every pvc in the cluster and send them to an AWS-S3 bucket.

So the restoration workflow would be:
1. Rebuild cluster
2.  Apply internal kubernetes manifests in `/kuberentes` folder. 
3. Create the Velero namespace `kubectl create namespace velero`
4. Find and note down the AWS S3 bucket credentials. If lost, they may be found on the AWS website. These are the only secrets/keys that have to be manually restored. All other secrets are encrypted within the backups.
5. Uncomment the text under the `cloud` section and manually add the credentials in the marked spots in the file `./kubernetes/apps/velero/velero-credentials-secret.yaml`. Then apply the secret, like so `kubectl apply -f <SECRET_TEMPLATE_FILEPATh>`.
   **NOTE** -> Make sure theese credentials do not get tracked by git.
6. Apply helmfile for all external deployments. (Most importantly ArgoCD & Harbor & Velero)
7. Run `velero restore` ONLY for Harbor namespace
8. Wait until Harbor pods come up with restored images
9. Run full GitOps/ArgoCD sync for all internal deployments
10. Run Full-Scale Velero restore (excluding Harbor that already was restored)

