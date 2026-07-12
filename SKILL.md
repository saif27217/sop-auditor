---
name: sop-auditor
description: "Audit SOPs and controlled documents retrieved from a Qdrant RAG collection for discrepancies, contradictions, missing steps, and compliance gaps. Use when asked to audit, review, or reconcile SOPs / work instructions / procedures against standards (ISO 15189, NABL, ISO 13485, CLIA, etc.). Covers the full workflow: broad retrieval (with a full payload dump to defeat semantic top-k blindness), discrepancy analysis, and delivery as a Google Doc via Composio MCP."
version: 1.0.0
author: Sak / Lazer
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [sop, audit, qdrant, rag, compliance, iso15189, nabl, discrepancy, composio, google-docs]
    related_skills: [composio-mcp, deep-rag, literature-review, peer-review, scientific-critical-thinking]
---

# SOP Auditor

Audit Standard Operating Procedures (SOPs), work instructions, and controlled
documents stored as chunks in a Qdrant RAG collection. Detect contradictions,
missing steps, duplicated/conflicting instructions, ambiguous wording, and
regulatory/documentation gaps — then deliver an audit-ready report as a Google Doc.

## The one hard lesson this skill encodes

**Semantic top-k retrieval misses critical data.** In the founding audit
(Risk Assessment SOPs), a normal top-k vector search surfaced ~15 of 100 chunks
for the master SOP and ~15 of 290 for the work instructions. The **risk
matrices and RPN formulas were never retrieved** — they sit in dense tables
that don't match natural-language pueries). This produced a wrong audit
(version 1.0.0
author: Sak / Lazer
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [sop, audit, qdrant, rag, compliance, iso15189, nabl, discrepancy, composio, google-docs]
    related_skills: [composio-mcp, deep-rag, literature-review, peer-review, scientific-critical-thinking]
---

# SOP Auditor

Audit Standard Operating Procedures (SOPs), work instructions, and controlled
documents stored as chunks in a Qdrant RAG collection. Detect contradictions,
missing steps, duplicated/conflicting instructions, ambiguous wording, and
regulatory/documentation gaps — then deliver an audit-ready report as a Google Doc.

## The one hard lesson this skill encodes

**Semantic top-k retrieval misses critical data.** In the founding audit
(Risk Assessment SOPs), a normal top-k vector search surfaced ~15 of 100 chunks
for the master SOP and ~15 of 290 for the work instructions. The **risk
matrices and RPN formulas were never retrieved** — they sit in dense tables
that don't match natural-language pueries). This produced a wrong audit