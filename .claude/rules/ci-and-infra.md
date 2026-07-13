---
paths:
  - ".github/**"
  - "Dockerfile*"
  - "docker-compose*"
  - "**/terraform/**"
  - "**/*.tf"
---
Infrastructure and CI files: agents may PROPOSE diffs but the protect-paths hook
blocks direct workflow edits. Pin action versions by SHA, never @main. Secrets only
via the platform's secret store — never inline. Least-privilege `permissions:` block
required in every workflow.
