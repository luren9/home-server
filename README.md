# Home Server

> ⚠️ **Read-only GitHub Mirror**
> This repository is automatically synchronized from a self-hosted Forgejo instance. GitHub is provided for browsing, discovery, and backup only.

The canonical source for this project is a self-hosted Forgejo instance. All development, code reviews, issue tracking, releases, and CI/CD are managed there. Changes in the form of commits and branches are automatically mirrored to GitHub on push. PR comments, pipeline runs and other non source control related data is excluded from the push mirroring.

---

## Development Workflow

This repository is mirrored from my self-hosted Forgejo instance.

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