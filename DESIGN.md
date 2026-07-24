# Jonathan Pradipta Yudya Sulistyo

## Mission
Create implementation-ready, token-driven UI guidance for Jonathan Pradipta Yudya Sulistyo that is optimized for consistency, accessibility, and fast delivery across documentation site.

## Brand
- Product/brand: Jonathan Pradipta Yudya Sulistyo
- URL: https://fmorenil.dev/#about
- Audience: developers and technical teams
- Product surface: documentation site

## Style Foundations
- Visual style: structured, tokenized, content-first
- Main font style: `font.family.primary=Sansation`, `font.family.stack=Sansation, sans-serif`, `font.size.base=16px`, `font.weight.base=400`, `font.lineHeight.base=24px`
- Typography scale: `font.size.xs=11px`, `font.size.sm=12px`, `font.size.md=14px`, `font.size.lg=16px`, `font.size.xl=18px`, `font.size.2xl=20px`, `font.size.3xl=24px`, `font.size.4xl=36px`
- Color palette: `color.text.primary=#f4f4f4`, `color.border.muted=#ffffff`, `color.text.tertiary=oklch(0.869 0.022 252.894)`, `color.text.inverse=oklch(0.554 0.046 257.417)`, `color.surface.base=#000000`, `color.surface.muted=#1e293b`, `color.surface.raised=oklch(0.279 0.041 260.031)`, `color.surface.strong=#191925`
- Spacing scale: `space.1=4px`, `space.2=8px`, `space.3=10px`, `space.4=12px`, `space.5=16px`, `space.6=20px`, `space.7=24px`, `space.8=32px`
- Radius/shadow/motion tokens: `radius.xs=8px`, `radius.sm=12px`, `radius.md=24px` | `motion.duration.instant=150ms`, `motion.duration.fast=200ms`, `motion.duration.normal=300ms`, `motion.duration.slow=400ms`

## Accessibility
- Target: WCAG 2.2 AA
- Keyboard-first interactions required.
- Focus-visible rules required.
- Contrast constraints required.

## Writing Tone
Concise, confident, implementation-focused.

## Rules: Do
- Use semantic tokens, not raw hex values, in component guidance.
- Every component must define states for default, hover, focus-visible, active, disabled, loading, and error.
- Component behavior should specify responsive and edge-case handling.
- Interactive components must document keyboard, pointer, and touch behavior.
- Accessibility acceptance criteria must be testable in implementation.

## Rules: Don't
- Do not allow low-contrast text or hidden focus indicators.
- Do not introduce one-off spacing or typography exceptions.
- Do not use ambiguous labels or non-descriptive actions.
- Do not ship component guidance without explicit state rules.

## Guideline Authoring Workflow
1. Restate design intent in one sentence.
2. Define foundations and semantic tokens.
3. Define component anatomy, variants, interactions, and state behavior.
4. Add accessibility acceptance criteria with pass/fail checks.
5. Add anti-patterns, migration notes, and edge-case handling.
6. End with a QA checklist.

## Required Output Structure
- Context and goals.
- Design tokens and foundations.
- Component-level rules (anatomy, variants, states, responsive behavior).
- Accessibility requirements and testable acceptance criteria.
- Content and tone standards with examples.
- Anti-patterns and prohibited implementations.
- QA checklist.

## Component Rule Expectations
- Include keyboard, pointer, and touch behavior.
- Include spacing and typography token requirements.
- Include long-content, overflow, and empty-state handling.
- Include known page component density: links (28), buttons (20), inputs (5), navigation (2).

- Extraction diagnostics: Audience and product surface inference confidence is low; verify generated brand context.

## Quality Gates
- Every non-negotiable rule must use "must".
- Every recommendation should use "should".
- Every accessibility rule must be testable in implementation.
- Teams should prefer system consistency over local visual exceptions.
