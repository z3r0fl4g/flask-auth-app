# UI/UX Design Rules & Best Practices

## Color System

### Brand Palette  
Use the tonal steps below for backgrounds, gradients, and stateful accents. Pair darker tones (100–400) with light neutrals for contrast and reserve 500 as the core brand intensity.

- **Amber Spotlight** (CTA/highlight)  
  - 100 `#352700` · 200 `#6a4e00` · 300 `#9f7500` · 400 `#d49c00` · 500 `#ffbe0b`  
  - 600 `#ffcb3b` · 700 `#ffd86c` · 800 `#ffe59d` · 900 `#fff2ce`
- **Orange Pulse** (secondary CTA, alerts)  
  - 100 `#331101` · 200 `#662202` · 300 `#9a3202` · 400 `#cd4303` · 500 `#fb5607`  
  - 600 `#fc773a` · 700 `#fd996b` · 800 `#febb9d` · 900 `#feddce`
- **Rose Fanfare** (emotive accents)  
  - 100 `#330016` · 200 `#66002c` · 300 `#990042` · 400 `#cc0058` · 500 `#ff006e`  
  - 600 `#ff338b` · 700 `#ff66a8` · 800 `#ff99c5` · 900 `#ffcce2`
- **Blue Violet Stage** (primary identity)  
  - 100 `#190535` · 200 `#320a6a` · 300 `#4b0fa0` · 400 `#6414d5` · 500 `#8338ec`  
  - 600 `#9b5ef0` · 700 `#b487f4` · 800 `#cdaff8` · 900 `#e6d7fb`
- **Azure Air** (informational surfaces)  
  - 100 `#00183e` · 200 `#00307c` · 300 `#0048bb` · 400 `#005ff9` · 500 `#3a86ff`  
  - 600 `#609dff` · 700 `#88b5ff` · 800 `#afceff` · 900 `#d7e6ff`

### Neutral Palette
- Background: `#f8f9ff`  
- Surface: `#ffffff`  
- Divider: `#e5e7eb`  
- Headline: `#1f2937`  
- Body: `#4b5563`  
- Muted: `#9ca3af`

### Semantic Colors
- Success `#10B981` · Warning `#F59E0B` · Error `#EF4444` · Info `#3B82F6`  
  Use 15% opacity backgrounds plus 500 text tone for alerts.

## Typography

- **Font stack**: `"Inter", system-ui, sans-serif` (body) · `"Space Grotesk", monospace` (spot headings, numbers)
- **Scale**: H1 `3.125rem`, H2 `2.25rem`, H3 `1.5rem`, H4 `1.25rem`, Body `1rem`, Small `0.875rem`
- **Line height**: headings `1.2`, paragraphs `1.65`, buttons `1.5`
- **Letter spacing**: uppercase labels use at least `0.3em`

## Spacing System
Retain the 8px grid. Helpers: `4px`, `8px`, `12px`, `16px`, `24px`, `32px`, `48px`, `64px`. Primary layout gutters: `24px` mobile, `32px` tablet, `48px` desktop.

## Components

### Buttons
- **Primary**: pill shape, gradient `linear(from #8338ec to #6414d5)` by default. Text white, subtle lift (`translateY(-2px)`) on hover, `shadow-md` with tinted glow.
- **Secondary**: pill outline `1px` with `#8338ec`, on hover gain 10% tinted fill.
- **Ghost**: neutral surface (`#f3f4f6`), dark text, hover to `#e5e7eb`.
- **Icon buttons**: round `40px`, border `#e5e7eb`, background white, icon `#6b7280`.

### Forms
- Inputs/cards are **rounded-2xl** (16px).  
- Default border `#e5e7eb`, fill white, focus border `#8338ec`, focus ring `rgba(131,56,236,0.2)`.  
- Inline helper text `0.75rem` with muted gray. OTP inputs are 6 evenly spaced boxes with same focus styling.

### Cards & Surfaces
- Use soft borders (`#e5e7eb`) and light drop shadows (`0 20px 60px rgba(15,23,42,0.08)`).
- Highlight cards (hero stats) may sit atop gradient halos (`#d7e6ff`, `#ffe59d`, `#ff99c5`) blurred at 150–200px.
- Section containers often pair white inner surfaces with gradient outer rims (`border-image` style) for call-to-actions.

### Navigation & Footer
- Navigation: translucent white background with blur, subtle shadow. Search is a pill `border-gray-200`. Active states color-shift to `#1f2937`.
- Footer: white with gradient accents and rounded newsletter input using the same focus treatment as forms.

## Layout & Imagery
- Background uses layered blurred circles in brand tints (`#d7e6ff`, `#ffe59d`, `#ff99c5`) positioned offscreen with high blur radius (120–200px).
- Max content width `1120px`; hero sections pair text and stat cards in a 55/45 split on desktop.
- Callouts utilize uppercase labels with tracking and badges (rounded-full, thin borders).

## Interaction Guidelines
- Hover transitions ≤ 200ms with ease-out; transform limited to small lifts/scale (`translateY(-2px)`, `scale(1.02)`).
- Focus states always visible (border + halo as described).  
- Motion uses CSS only; avoid heavy JS animations unless necessary.

## Accessibility
- Maintain AA contrast, especially when using soft gradient backgrounds—validate text against `#f8f9ff` or white.  
- Provide descriptive alt text (e.g., “Speaker portrait”).  
- Keyboard navigation must reach search, nav items, form controls, and modal actions.

## Implementation Notes
1. Define CSS variables (or Tailwind theme tokens) for each palette step and neutral tone.  
2. Apply shared button/input classes to avoid divergence.  
3. Gradient backgrounds should use the specified color pairs; avoid introducing new hues without sign-off.  
4. Keep spacing consistent with the 8px rule and align section padding with breakpoints described above.  
5. Revisit this guide before building or refactoring UI; document any deviations with a `// TODO:` and reasoning.
