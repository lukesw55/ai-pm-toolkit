# Design Guidelines

Use this file as the visual and interaction source of truth for active projects.

## Design stance

Design should feel:

- clear before clever
- fast to scan
- calm under complexity
- honest about state
- lightweight enough for startup iteration

## Core rules

- Prefer a strong visual hierarchy over decorative density.
- Use spacing and typography to create structure before adding borders or color.
- Every interactive element must have visible hover, focus, disabled, and error states where relevant.
- Error messages must explain what happened and what the user can do next.
- Loading states should preserve layout stability.
- Empty states should help the user recover or continue.
- Respect reduced motion preferences.

## Tokens to define per project

### Color
Define:
- primary
- accent
- surface
- background
- text
- muted
- border
- success
- warning
- danger

### Typography
Define:
- display
- heading
- body
- caption
- mono (if code-heavy UI exists)

### Spacing
Use a consistent spacing scale and document it.

## Components that usually need explicit design rules

- navigation
- cards
- forms
- buttons
- tables
- lists
- modals / drawers
- toasts / alerts
- dashboards / metrics blocks

## Responsiveness

Document the intended behavior for:
- mobile
- tablet
- desktop

## Accessibility

Minimum expectations:

- keyboard-accessible interactions
- visible focus states
- semantic labels
- color-independent status meaning
- sufficient contrast
- touch targets that are usable on mobile

## Project-specific addendum

Add project-specific visual rules below when the active context is known.
