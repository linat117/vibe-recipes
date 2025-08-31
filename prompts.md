# Prompts for Cursor AI — Recipe Generator App (Django + MySQL + PWA)

> **How to use this file**
> Copy each prompt block (in code fences) into Cursor AI sequentially. Cursor should implement the changes, explain what it did, what *you* need to do (commands, env vars, runs), and append an entry to `CHANGELOG.md` after each step. If Cursor proposes deviations, it must justify them and keep scope tight.

---

## 0) Global Instruction (paste first)

```prompt
You are the **lead engineer** building a hackathon project called **Recipe Generator** using **Django (backend), MySQL (database), HTML/CSS + Bootstrap (frontend), and PWA basics**. You will:
- Work in small, verifiable iterations.
- For **every step**: (1) list a brief plan, (2) show the file changes or new files, (3) give exact commands I must run, (4) update/append a `CHANGELOG.md` entry with clear bullet points, (5) propose quick smoke tests I can run.
- Prefer **simple, maintainable** solutions. Don’t over-architect. Time limit is 3–4 days.
- If something is ambiguous, assume sensible defaults and move forward. Do **not** stall.
- Keep UI **clean and responsive** using Bootstrap via CDN (fastest path). Add minimal custom CSS where helpful.
- Always ensure the app starts and basic navigation works after each step.
- Use the following **project structure** as north star (adapt if needed, but explain why):
  - `vibe_recipes/` (project)
  - `apps/accounts/` (auth & profile)
  - `apps/recipes/` (ingredients, recipes, generation, history)
  - `apps/community/` (public sharing feed)
  - `core/` (static, templates, PWA, utilities)

**Functional requirements** (MVP):
1) **Authentication**: register, login, logout; user profile page minimal.
2) **Ingredient selection**: grid/list of ingredient cards with search/filter.
3) **Cuisine selection**: dropdown/chips (e.g., Italian, Ethiopian, Indian, etc.).
4) **Recipe generation**: rule-based logic that either (a) matches an existing recipe by ingredient coverage & cuisine, or (b) creates a new **generated recipe** entry with templated steps. Show substitutes if a common item is missing.
5) **History**: per-user list of generated recipes (with view details page).
6) **Community feed**: users can share a recipe they tried; public page lists posts.
7) **PWA basics**: `manifest.json`, `service-worker.js` to cache static files and last viewed recipe pages; installable.

**Non-functional constraints**:
- Use **Django ORM** and **mysqlclient**. Keep migrations consistent.
- Use **Bootstrap 5 via CDN**; no heavy JS frameworks.
- Use Django Templates; keep JS light and progressive.
- Code must be clear, commented, and suitable for a hackathon demo.

At the end of each step, output sections titled:
- **What I changed** (files, diffs or summaries)
- **Commands to run**
- **Smoke test**
- **CHANGELOG.md** (append-only entry)
- **Next suggested step**
```

---

## 1) Initialize Project & MySQL Config

```prompt
**Step 1 — Project bootstrap & DB config**
Goal: Create a Django project `vibe_recipes`, set up apps, connect to MySQL, add Bootstrap base template, and home route.

Tasks:
1. Create virtualenv, requirements, and Django project `vibe_recipes` with apps: `accounts`, `recipes`, `community` under `apps/` package. Add `core/` for global assets.
2. Add `requirements.txt` with: django, mysqlclient, python-dotenv, pillow, whitenoise (optional), pytest-django (optional for tests).
3. Configure **MySQL** in `settings.py` using environment variables from `.env` (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `SECRET_KEY`, `DEBUG`).
4. Setup `TEMPLATES`, `STATIC_URL`, `STATICFILES_DIRS`, `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`.
5. Create `core/templates/base.html` with Bootstrap 5 CDN and a nav: Home, Generate, History, Community, Login/Logout.
6. Add root URL routing and a simple `home` view/template.
7. Ensure server runs and base loads.

Deliverables: new project files, `.env.example`, base template, working home page.
Remember to output: What I changed, Commands to run, Smoke test, CHANGELOG.md, Next step.
```

---

## 2) Auth: Register/Login/Logout + Minimal Profile

```prompt
**Step 2 — Authentication**
Goal: Implement user registration, login, logout, minimal profile view.

Tasks:
1. Use Django’s `User` model. Create forms for register/login in `apps/accounts/forms.py`.
2. Views & URLs: `/auth/register/`, `/auth/login/`, `/auth/logout/`, `/auth/profile/`.
3. Templates with Bootstrap forms; add flash messages; update navbar to reflect auth state.
4. Protect authenticated routes with `login_required` where needed.

Deliverables: forms, views, urls, templates, navbar conditional links.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 3) Data Models: Ingredients, Recipes, History, Community

```prompt
**Step 3 — Models & Admin**
Goal: Define data schema and register in admin.

Models:
- `Ingredient(name:str, category:str|null)`
- `Recipe(title:str, cuisine:str, description:text|null, instructions:text, cooking_time:int|null, difficulty:choice|null, image_url:str|null, is_generated:bool default False)`
- `Recipe.ingredients` — ManyToMany to `Ingredient`.
- `UserRecipeHistory(user:FK->User, recipe:FK->Recipe, selected_ingredients:JSON|null, created_at:datetime)`
- `CommunityPost(user:FK->User, recipe:FK->Recipe, description:text, created_at:datetime)`

Tasks:
1. Create these models under appropriate apps (`recipes` for Ingredient/Recipe/UserRecipeHistory; `community` for CommunityPost).
2. Add reasonable `__str__` and admin registrations with list filters & search.
3. Make & run migrations.
4. Seed script: a Django management command or fixture to populate common ingredients (milk, tomato, onion, beef, garlic, pasta, butter, spices...) and a few sample recipes across cuisines (Italian, Ethiopian, Indian, etc.).

Deliverables: models, admin, seeds.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 4) Ingredient Selection UI + Cuisine Picker

```prompt
**Step 4 — Ingredient & Cuisine selection UI**
Goal: Create a page to pick ingredients (cards or checklist) and a cuisine dropdown, then submit to generation endpoint.

Tasks:
1. URL `/generate/` (GET: form; POST: process). Keep route under `recipes` app.
2. Template shows: search box, responsive grid of ingredient cards with checkboxes; cuisine dropdown (Italian/Ethiopian/Indian/Chinese/Mexican/Arabic/…); CTA button **Generate Recipe**.
3. Store selections in POST and pass to generation view.

Deliverables: view, template, url, small CSS/JS for filtering.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 5) Rule‑Based Recipe Generation Logic

```prompt
**Step 5 — Generation logic**
Goal: Implement backend logic to either match an existing recipe or synthesize a simple generated one.

Rules:
- If matching recipes exist: pick the one with **highest ingredient coverage** (intersection size / selected size), cuisine must match if provided. If tie, prefer fewer missing ingredients and lower cooking_time.
- If no match, create a new `Recipe(is_generated=True)` with a **templated title** using key ingredients + cuisine (e.g., "Italian Creamy Tomato Beef Pasta").
- Build `instructions` from a **template**: prep → cook base → combine → finish; include timers and optional substitutions.
- Save a `UserRecipeHistory` row with `selected_ingredients` JSON snapshot.
- Provide a lightweight **substitution dict** (e.g., cream→milk+butter, beef→mushrooms for veg option, butter→oil, etc.) and render them in the result if relevant items are missing.

Tasks:
1. Implement a service/helper in `apps/recipes/services/generator.py` with pure functions: `match_recipe(...)`, `synthesize_recipe(...)`, `generate_recipe(...)`.
2. Wire POST from `/generate/` to call `generate_recipe`, then redirect to `/recipes/<id>/`.
3. Create a `recipe_detail` view and template showing: title, cuisine, ingredients list, instructions (step list), and buttons **Save/Share** (share if logged in).

Deliverables: services module, updated views, detail page.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 6) History (per‑user) List & Detail

```prompt
**Step 6 — History**
Goal: Show a page for logged-in users listing their generated recipes with timestamps.

Tasks:
1. URL: `/history/` lists `UserRecipeHistory` for current user (paginate, newest first).
2. Each item links to recipe detail. Add delete action (optional) for history rows.
3. Add link to navbar.

Deliverables: view, template, url, pagination, optional delete.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 7) Community: Share & Public Feed

```prompt
**Step 7 — Community feed**
Goal: Allow users to share a recipe and browse a public feed.

Tasks:
1. From recipe detail page, add a **Share to Community** button (if logged in) → creates `CommunityPost(user, recipe, description)`.
2. URL: `/community/` shows a public feed (cards with recipe title, user, cuisine, short description, link to detail). Order by newest.
3. Optional: simple search/filter by cuisine or ingredient.

Deliverables: create & list posts, templates, urls.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 8) PWA: Manifest + Service Worker (cache static & last-viewed)

```prompt
**Step 8 — PWA basics**
Goal: Make the app installable and cache essential assets + last viewed recipe pages.

Tasks:
1. Add `core/static/manifest.json` with app name, theme colors, and icons (generate placeholder icons if needed).
2. Add `core/static/service-worker.js` to cache: Bootstrap CSS/JS (CDN via `crossorigin` OK), our static CSS/JS, logo icons, and the most recent recipe detail pages visited (cache-first strategy with versioning).
3. In `base.html`, link manifest and register service worker.
4. Add a small install prompt hint in the footer (optional).

Deliverables: manifest, service worker, base template hooks, icons.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 9) Styling Polish & Accessibility

```prompt
**Step 9 — UI polish**
Goal: Make the app visually appealing and accessible.

Tasks:
1. Apply consistent spacing, typography, card layouts, and responsive grids using Bootstrap utilities.
2. Ensure color contrast and ARIA labels for forms, nav, buttons.
3. Add a lightweight `core/static/css/styles.css` for minor tweaks.
4. Test mobile breakpoints.

Deliverables: CSS improvements and template refinements.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 10) Seeding Data & Demo Safety

```prompt
**Step 10 — Seed & fixtures**
Goal: Ensure demo never shows empty screens.

Tasks:
1. Management command `python manage.py seed_demo` to create:
   - Common ingredients
   - 6–10 sample recipes across cuisines with realistic instructions
   - A demo user (`demo@example.com` / password shown in console) and a few history entries
   - A few community posts
2. Ensure idempotency (safe to run multiple times).

Deliverables: management command or fixtures, README notes.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 11) Minimal Tests (sanity)

```prompt
**Step 11 — Tests (sanity)**
Goal: Add minimal unit tests to protect core logic.

Tasks:
1. Tests for: model creation, `generate_recipe` logic (match vs synthesize), and views (200 responses for key pages when logged-in vs anonymous where appropriate).
2. Provide `pytest.ini` and basic setup, or use Django’s `TestCase`.

Deliverables: tests, instructions to run them.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 12) README, Prompts Log, and Changelog discipline

```prompt
**Step 12 — Docs & hygiene**
Goal: Document the project and enforce change logging.

Tasks:
1. Create/update `README.md` (project intro, stack, features, setup, env, run commands, seed, PWA notes, demo flow).
2. Create `prompts.md` section template for my future prompts (this file). Ensure `CHANGELOG.md` has dated entries for all steps completed.
3. Add `.env.example` and basic `.gitignore`.

Deliverables: README, prompts stub confirmation, changelog entries.
Output standard sections + append to `CHANGELOG.md`.
```

---

## 13) Optional Enhancements (only if time permits)

```prompt
**Step 13 — Optional enhancements**
Pick 1–2 only if there is time.

Options:
- Ingredient substitutes UI: show inline suggestions with quick “replace” action.
- Badges/Gamification: grant a badge after 3 recipes in same cuisine.
- Simple upvotes on community posts.
- Voice mode: read recipe steps aloud using Web Speech API (progressive enhancement).
Provide plan, changes, commands, smoke tests, and add to `CHANGELOG.md`.
```

---

## Global Acceptance Criteria (Cursor must respect these on every step)

* App runs locally with `python manage.py runserver` after migrations.
* MySQL connection via env vars works; migrations succeed.
* Navbar links function; unauthorized access redirects to login where appropriate.
* Ingredient selection → cuisine → **Generate** → recipe detail → **Share** works end-to-end.
* History lists items for the current user.
* PWA install prompt available; offline page serves cached content for at least the last viewed recipe and static assets.
* Code is **clean, commented, and minimal**; templates responsive.
* Each step includes: **What I changed / Commands / Smoke test / CHANGELOG.md / Next step**.

---

## One‑Shot Kickoff Prompt (if you want Cursor to start from scratch now)

```prompt
Start Step 1 now. Assume clean repo and no files present. Generate the project exactly as specified (Django + MySQL + Bootstrap + base template). Provide:
- Plan
- File changes (paths + content snippets, or full files for new ones)
- Commands to run (venv, pip install, startproject, startapp, migrations, runserver)
- How to create `.env` from `.env.example`
- Smoke test instructions
- Append a `CHANGELOG.md` entry for Step 1
- Propose the Next step (which should be Step 2: Auth)
Proceed.
```

---

## Notes for Me (the developer)

* Keep this `prompts.md` open. After each Cursor step, skim `CHANGELOG.md` and try the smoke test.
* If something fails, ask Cursor for a **fix step** and insist it includes the same sections.
* For the demo, prepare a flow: Login → Generate → View Recipe → Save/Share → View History → Community.
