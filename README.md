# Home Server

> ⚠️ **Read-only GitHub Mirror**
> This repository is automatically synchronized from a self-hosted Forgejo instance. GitHub is provided for browsing, discovery, and backup only.

---

## About the Repository

This repository contains all of the code and configuration for my self hosted on prem kubernetes cluster and its deployments. It hosts the IaC for the entirety of my homelab setup and all code for managing my GitOps deployment of self hosted applications

### Purpose

This project is for personal learning purposes.

---

## Goals

* Enterprise grade GitOps workflow
* HA with multiple on-prem or cloud failover servers
* Potential to host scalable enterprise grade applications

---

## Documentation

Project documentation are all written in markdown format and primarily built around Obsidian.

To track development see [[obsidian-kanban]]

Using the graph view in obsidian can also give a better overview of the documentation and how service documentations are related


---

## Forgejo Development Workflow

The canonical source for this project is a self-hosted Forgejo instance. All development, code reviews, issue tracking, releases, and CI/CD are managed there. Changes in the form of commits and branches are automatically mirrored to GitHub on push. PR comments, pipeline runs and other non source control related data is excluded from the push mirroring.

The workflow is intentionally simple:

```text
Developer
    │
    ▼
Self-hosted Forgejo
    │
    ├── Source control (mirrored)
    └── CI/CD using self-hosted runners (not mirrored)
            │
            ▼
     Automatic Push Mirror
            │
            ▼
GitHub (read-only mirror)
```

GitHub exists for:

* Public visibility
* Repository backup

No development is performed directly on GitHub.
