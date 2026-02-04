# Tikepam - AI Assistant Instructions

Tikepam is a Haitian event ticketing platform. The app has a Vue 3 SPA frontend and a Flask backend with REST API.

## How to Work on This Codebase

### Plan Before You Code

Before writing any code, describe your approach and wait for approval. If requirements are ambiguous, ask clarifying questions first. Never assume intent — a wrong assumption costs more than a quick question.

When planning, consider:
- Which files will be touched and why
- Whether the change follows the module pattern (see Architecture below)
- What could break as a side effect

### Keep Changes Small

If a task requires changes to more than 3 files, stop and break it into smaller, independently verifiable tasks first. Each sub-task should be completable and testable on its own. This prevents large, hard-to-review changes and makes rollback easier.

### Verify After Every Change

After writing code, explicitly list:
1. What could break as a result of the change
2. Which existing flows might be affected
3. Suggested tests to cover the new or changed behavior

Don't assume it works — verify it. Run the build, check the browser, run the Selenium test if the change touches auth or navigation.

### Bug Fixing Protocol

When fixing a bug:
1. First, write a test (or describe a manual reproduction) that demonstrates the bug
2. Confirm the test fails / the bug reproduces
3. Fix the code
4. Confirm the test passes / the bug is resolved
5. Check for regressions in related flows

Never skip straight to a fix without understanding the root cause.

### Learn From Corrections

Every time the user corrects you, add a new rule to this CLAUDE.md file under "Learned Rules" at the bottom so the mistake never happens again. Be specific about what went wrong and what to do instead.

## Tech Stack

- **Frontend:** Vue 3 (Composition API, `<script setup>`), Vite, Pinia, Vue Router, Tailwind CSS, Axios
- **Backend:** Flask, SQLAlchemy, Flask-Login, Flask-Mail, Flask-Session (Redis), Flask-Limiter
- **Database:** PostgreSQL (prod/dev), SQLite (fallback)
- **Auth:** Session-based with 2FA email verification

## Architecture

### Modular Frontend

Each feature lives in `frontend/src/modules/{name}/` with this structure:

```
modules/{name}/
  routes/index.js      # Route definitions with guards
  store/{name}.js      # Pinia store (setup syntax)
  views/               # Page components
  components/          # Feature-specific components
  composables/         # Reusable logic (useFormValidation, etc.)
```

Shared components go in `frontend/src/components/`:
- `layout/` - Navbar, Footer, AppLayout
- `home/` - Landing page sections (HeroSection, FeaturedEvents, etc.)

### Store Pattern

Stores are defined in the module and re-exported via a wrapper for clean imports:

```js
// modules/auth/store/auth.js — actual implementation
export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)
  // ... setup syntax with refs, computed, functions
})

// stores/auth.js — wrapper (one-liner re-export)
export { useAuthStore } from '@/modules/auth/store/auth'
```

All components import from `@/stores/auth`, not from the module path directly. Follow this pattern for new modules.

### Routing

Routes are defined per module and spread into the main router:

```js
// router/index.js
import { authRoutes } from '@/modules/auth/routes'
const router = createRouter({
  routes: [...authRoutes]
})
```

Route guards use `meta.requiresAuth` and `meta.requiresGuest`. Named routes use kebab-case.

### Flask Blueprints

Each feature maps to a backend blueprint:

```
api/{name}.py          # JSON API endpoints
  - Blueprint prefix: /api/{name}
  - Registered in app.py
```

Current blueprints:
- `api/auth.py` → `/api/auth` (login, signup, logout, session)
- `api/twofa.py` → `/api/2fa` (verify, enable, disable, resend)

Legacy Jinja2 routes exist in `auth/routes/` at `/auth` prefix — keep but don't extend.

### API Conventions

Response format:
```json
{ "success": true, "message": "...", "data": {...} }
```

The Axios client (`services/api.js`) handles:
- 401 → redirect to `/login` (except on login/signup endpoints)
- 403 with `VERIFICATION_REQUIRED` → redirect to `/2fa/verify`
- `withCredentials: true` for session cookies
- Empty `baseURL` — requests go through Vite's proxy (same-origin)

## Development Setup

Both servers must run simultaneously:

```bash
# Terminal 1: Flask backend
PYTHONUNBUFFERED=1 python app.py    # runs on port 5001

# Terminal 2: Vue frontend
cd frontend && npm run dev          # runs on port 5173
```

Vite proxies `/api` and `/auth` requests to `localhost:5001`. Never set `baseURL` to `http://localhost:5001` directly — use the proxy to avoid cross-origin cookie issues.

## CSS / Styling

Use Tailwind utility classes. These custom component classes are defined in `frontend/src/assets/style.css`:

- `.btn-primary` — Pill-shaped gradient button with hover lift. Use `btn-primary w-full justify-center` for full-width form buttons.
- `.btn-secondary` — Outline variant
- `.input` — Rounded-2xl input with focus ring
- `.card` — Rounded border with soft shadow

Brand colors (defined in `tailwind.config.js`): amber, orange, rose, violet (primary), azure. Use the tonal scale (100-900).

Fonts: Inter (body), Space Grotesk (mono/headings).

## Auth Flow

1. User signs up → account created → 2FA code sent via email
2. Redirect to `/2fa/verify` → user enters 6-digit code
3. Code verified → session established → redirect to `/profile`
4. Login follows same flow if 2FA is enabled

Session cookie: `SameSite=Lax`, 24-hour permanent session, Redis-backed.

## Key Rules

- **Module pattern:** Every new feature gets a frontend module + Flask blueprint. Don't scatter views or routes outside modules.
- **Store wrappers:** Always re-export from `stores/{name}.js`. Components import from `@/stores/`, never from `@/modules/.../store/`.
- **No unused files:** Don't leave dead views, components, or imports. Clean up as you go.
- **Button consistency:** Use `btn-primary` class for submit/CTA buttons. Don't inline gradient styles.
- **Proxy-first:** API calls go through Vite proxy. Never hardcode backend URLs in frontend code.
- **Nav visibility:** Login, signup, and 2FA verify pages hide the navbar and footer (controlled by `hideNav` computed in Navbar.vue).
- **2FA codes:** In dev, codes print to Flask stdout. Start Flask with `PYTHONUNBUFFERED=1` and tail the log.

## Testing

Selenium tests live in `tests/`. The main flow test (`test_user_flow.py`) runs headless Chrome through signup → 2FA → dashboard → navbar verification. It reads 2FA codes from Flask's stdout log at `/tmp/flask_output.log`.

Run with: `python tests/test_user_flow.py`

## Learned Rules

Rules added from past corrections. Each entry documents a specific mistake and the correct approach.

- **Use shared CSS classes, not inline styles.** The login and signup pages were built with inline Tailwind button styles instead of the existing `btn-primary` class, creating visual inconsistency. Always check `style.css` for existing component classes before writing inline styles.
- **Don't write more code than asked for.** When asked to run a simple Selenium login, a full test suite was written instead. Match the scope of your output to the scope of the request.
- **Use Vite proxy, never direct backend URLs.** Setting `baseURL: 'http://localhost:5001'` in Axios caused cross-origin cookie failures. The Vite proxy is already configured — leave `baseURL` empty so requests stay same-origin.
