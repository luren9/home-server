Unfortunatley kustomize really cant handle declarative patching for nested key values inside configmap generators. At first i thought i would inclkude the full live manifest and just edit the values i needed to patch, but that proved insecure, ugly and meta-data values gets messed up. So instead i just wrote this little documentaion for this little change made in the kube proxy manually:

i ran:
```bash
kubectl -n kube-system edit configmap kube-proxy
```

Then edited theese values:
```yaml
mode: ""
strictARP: false
```

to:
```yaml
mode: "ipvs"
strictARP: true
```