# Power BI AI Toolkit

Public preview of a local AI workflow for reviewing Microsoft Power BI semantic models stored as PBIP/TMDL.

The project explores how an assistant can inspect model metadata, reason about tables and measures, and support controlled changes to a semantic model. The production implementation is private, but this repository shows a small public slice of the workflow.

## What This Preview Shows

- The product idea and intended workflow.
- A readable public code sample.
- Measure suggestions with dependencies.
- Number-based user selection flow.
- A read-only TMDL preview.
- The public-facing architecture concept.

## What Is Not Public

The following parts are intentionally excluded:

- Production TMDL parser internals.
- Private model analysis rules.
- Full measure suggestion engine.
- TMDL editing, validation, and backup logic.
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

This file includes a real, runnable public example of the selection flow:

- example time intelligence suggestions,
- automatic dependency handling,
- TMDL measure block preview.

It does not include the production parser, analysis engine, prompt logic, local LLM client, or model write logic.

Run it with:

```bash
python public/preview.py
```

## Status

Private proof of concept. Public repository content is limited on purpose.
