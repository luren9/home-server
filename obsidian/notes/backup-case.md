### Standardized k8s cluster backup solution?
There is no perfect solution that is standardized. The best backup measures that can be made to a cluster depend on requirements, complexity toleration and amount of time that can be spent setting them up. There is no fool-proof plug-n-play solution, in fact there is no fully fool-proof system at all. Its kind of like looking for a package to install that would make a large system fully unexploited out of the box, Its just not possible. 


### Case
In my case, I really don't need to avoid data-loss, really. But i want to. Because i want to simulate how enterprises would and see how backupsystems might work. So, I will setup some requirements that I think could apply to larger organisations. Though, i will not go full bank-system/healthcare grade.

Here is the requirements for the cluster backups i will setup:

#### Requirements
* Should cover the entirety of the kubernetes cluster, meaning every node across any server-PC/cloud instance.
* The backups should be done once every day.
* Backed up data needs to be paired with location, so that a restoring dev can restore the correct data at the correct spots. Example, a PV's data must be paired with where its PVC should exist, what its called and so on.
* Whilst the cluster restoration mustn't be a fast process per say, it shouldn't scale with cluster complexity and size in terms of developer time. For example, a developer shouldn't have to manually restore each backed up PVC in their places one by one.

#### Non-requirements
* Cluster restoration must not be fast or automated, some manual work and downtime is expected and okay.
* Things like k8s resource IDs must not persist, meaning they can be recreated. (apps that require ID's for lookup instead of label, are bad.)
* Each deployment and app is ephemeral, so their states do not need to be backed up. Only data in PVC's need backing up.


## Velero
To meet our needs the choice is to go with Velero.
Velero will essentially regularly take snapshots of every pvc in the cluster and send them to an AWS-S3 bucket.

Velero will only be backing up `pv`'s `pvc`'s and `secret`'s. Everything else will have to be rebuilt from the declarative manifests - the GitOps way. This means that each disaster recovery will also be a "rebuild" of the entire cluster, which is good to ensure that any odd drift gets removed. For this Disaster Recovery (DR) process to be less scary, a good process is to try rebuilding the entire cluster every so often, maybe once every year.