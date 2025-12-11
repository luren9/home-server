We have a massive issue. In `kubernetes/apps/velero/values.yaml` we have this override:
```yaml
# values.yaml
kubectl:
  image:
    repository: bitnamilegacy/kubectl
    tag: "1.16.15"
```
It effectively overrides the default:
```yaml
# velero helm chart defaults
kubectl:
  image:
    repository: docker.io/bitnamilegacy/kubectl
    # tag: 1.16.15
```

This is super weird. I had to do this override for my setup to work. When looking at this, the only real difference is the prefix `docker.io/` missing on the override... 

I don't think this is good. At all. I believe i got lucky and hit my own caching layer or something. I'm not even sure either, where any why this `kubectl` image is used, but i believe it has something to do with the Velero node-agent (which we need as we use local-path-storage provisioner) and its ability to restore pvcs across the whole cluster, that requires kubectl access, or something i think anyways...

Either way, seems this thread talks about this exact issue, and it seems its not fully fixed yet...
https://github.com/vmware-tanzu/helm-charts/issues/698

## Problem
So if my guess is right and i just hit an older cached image from bitnamilegacy that i have had from before, then i wouldn't be able to restore my kubernetes cluster properly. This has to be looked in to more though.