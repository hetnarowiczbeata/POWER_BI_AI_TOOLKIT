# Power BI AI Toolkit

Public preview of a local AI workflow for reviewing Microsoft Power BI semantic models stored as PBIP/TMDL.

The project explores how an assistant can inspect model metadata, reason about tables and measures, and support controlled changes to a semantic model. The full implementation is private; this repository intentionally exposes only a small, non-sensitive preview.

## What This Preview Shows

- The product idea and intended workflow.
- A small illustrative code sample.
- The public-facing architecture concept.

## What Is Not Public

The following parts are intentionally excluded:

- TMDL parser internals.
- Model analysis rules.
- Measure suggestion engine.
- TMDL editing and backup logic.
- Prompt templates and local LLM integration details.
- Sample Power BI project files.
- Local configuration and model paths.

## Concept

```text
Power BI PBIP/TMDL
        |
        v
Local model scanner
        |
        v
AI-assisted review
        |
        v
User-approved suggestions
        |
        v
Controlled TMDL changes
```

## Public Code Preview

See:

```text
public/preview.py
```

This file is only a simplified preview. It does not include the production parser, analysis engine, or TMDL write logic.

## Status

Private proof of concept. Public repository content is limited on purpose.
