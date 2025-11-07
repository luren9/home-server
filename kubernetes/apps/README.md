# `kubernetes/apps/` Structure and Usage

This directory contains all information and configuration for third-party app deployments throughout the k8s cluster.

All third party applications throughout the cluster are/should be deployed and versioned with helm.
Helm nativley versions third-party applications in the cluster through injected secrets, but to be GitOps compliant we make use of the additional `Helmfile` tool aswell as the `helm-diff` tool. Theese tools allow for writing declarative helmfiles where we can declare repositories, chart-versions aswell as our manuall overrides. We can then also catch drift between the manifests our declarative helm would create and the actual live manifests using the `helm-diff` tool.

## Directory Layout

kubernetes/
└── apps/
    ├── helmfile.yaml   <------- Main helmfile, lists all repos and all deployemnts. Says which values.yaml should be used to patched which helm-charts.
    │
    ├── <third-party-app>/   <---- Folders, in case need for additional documentation and or other files
    │ └── values.yaml
    │
    └── <another-third-party-app>/
    └── values.yaml    <----- File containing any overrides supported by the given helmchart


Helm is **only** used for these external packages. No in-house charts are created or maintained.

### In-House Deployments
Each internal deployment also has its own folder under `deployments/<deployment-name>/`.
Documentations regarding in-house deployments can be found there.

No Helm charts are authored in this repository.
No Helm packaging, templating, or chart structure should be created for first-party services.

## Helm Usage Policy

1. **Helm is strictly limited to third-party applications.**
   These apps must be installed from external, versioned charts.
   Self-built services must not use Helm charts or templating. They rely only on declarative manifests (Kustomize, raw YAML, or other non-templated mechanisms).

2. **All Helm repositories and releases must be defined through `helmfile.yaml`.**
   Direct `helm install/upgrade` commands should not be used outside Helmfile workflows.

3. **All configuration overrides live in `values.yaml`.**
   No inline values/overrides in the main-Helmfile
   Any overrides must live in its respected application folder.

4. **No kustomization allowed for third-party apps.**
   Third party versioning is strictly limited to helm and is not to be mixed with raw kustomize mainfests.
   This is because theese kustomize mainfests can be tens of thousands of lines long and they are not backwards-compatable out of the box, so any manuall overrides would have to be manually migrated for any version bumping.
   Self-built applications are managed with kustomize however.
