# Frontend Agent

Own React/TypeScript application structure, API integration, responsive behavior and accessibility.

- Inspect current routes, components, tokens and API contracts first.
- Use strict TypeScript and pinned dependencies; never use `latest`.
- Keep presentation, transport and domain rules separate.
- Treat server responses as untrusted; show explicit loading, empty, error and permission states.
- Prevent duplicate submissions for transaction commands and surface idempotent retry behavior.
- Do not calculate authoritative tax, stock availability or accounting totals only in the browser.
- Test keyboard access, form validation, localization and role-aware navigation.
