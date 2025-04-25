# UI/UX Design Rules & Best Practices

## Color System

### Primary Palette

- Primary: #4F46E5 (Indigo-600)
- Primary Dark: #4338CA (Indigo-700)
- Primary Light: #6366F1 (Indigo-500)
- Accent: #EC4899 (Pink-500)

### Neutral Palette

- Dark: #1F2937 (Gray-800)
- Medium: #6B7280 (Gray-500)
- Light: #F3F4F6 (Gray-100)
- White: #FFFFFF

### Semantic Colors

- Success: #10B981 (Emerald-500)
- Warning: #F59E0B (Amber-500)
- Error: #EF4444 (Red-500)
- Info: #3B82F6 (Blue-500)

## Typography

### Font Stack

- Primary: "Inter", system-ui, sans-serif
- Secondary: "Space Grotesk", monospace
- Fallback: system-ui, -apple-system, sans-serif

### Scale (REM)

- H1: 3.0rem (48px)
- H2: 2.25rem (36px)
- H3: 1.5rem (24px)
- Body: 1rem (16px)
- Small: 0.875rem (14px)

### Line Height

- Headings: 1.2
- Paragraphs: 1.6
- Buttons: 1.5

## Spacing System (8px Grid)

- XS: 0.25rem (4px)
- S: 0.5rem (8px)
- M: 1rem (16px)
- L: 1.5rem (24px)
- XL: 2rem (32px)
- XXL: 3rem (48px)

## UI Components

### Buttons

- Primary:
  - BG: Primary
  - Text: White
  - Padding: 0.75rem 1.5rem
  - Radius: 0.375rem
- Secondary:
  - BG: Transparent
  - Border: 1px Primary
  - Text: Primary

### Forms

- Input padding: 0.75rem 1rem
- Input radius: 0.375rem
- Input border: 1px Neutral Light
- Focus border: 2px Primary

## Design Principles

1. **Clarity First**

   - Clear visual hierarchy
   - Consistent navigation
   - Minimal cognitive load

2. **Responsive Behavior**

   - Mobile-first approach
   - Fluid breakpoints
   - Adaptive components

3. **Accessibility**

   - AA contrast minimum
   - Keyboard navigable
   - ARIA labels

4. **Micro-interactions**
   - Subtle hover/focus states
   - Meaningful animations (<300ms)
   - Tactile feedback

## Latest Trends (2025)

- Glassmorphism effects
- 3D depth with subtle shadows
- Dynamic color schemes
- Voice UI integration
- Neumorphism for important CTAs

## Implementation Rules

1. Review this document before creating any new UI component
2. Use CSS variables for all colors
3. Maintain consistent spacing system
4. Validate contrast ratios for accessibility
5. Test on multiple viewport sizes
