# 📋 TASK: Build React Neumorphic Dashboard for Finance Tracker

> **Assigned Agent:** OpenCode LLM (Nemotron 3.5 / DeepSeek / Frontend Specialist)  
> **Architecture Style:** React (Vite) + Vanilla CSS (Custom Properties) + Dark Neumorphism  
> **Backend Integration:** Flask REST API (`http://localhost:5000`) inside Docker  
> **Reference Skill:** `SKILL_NEUMORPHIC_DESIGN.md` (Consult for shadow math & tactile button states)

---

## 🎯 1. Mission & Objectives

Build a responsive, high-performance, single-page financial dashboard using **React (Vite)**.  
The app will display live financial summaries, a category spending chart, a quick transaction entry form, and a scrollable transaction history feed.

### Core Constraints:
1. **No Top Header Banner:** As requested, do NOT include a web app title bar or UTC status pill. The screen starts directly with the dashboard controls and stat cards.
2. **Zero-Scroll Cockpit on Desktop (`>= 1024px`):** The entire desktop experience must fit into `100vh` without outer page scrollbars. Only the transaction list should have internal scrolling.
3. **Responsive on All Screen Sizes:**
   - **Desktop (`>= 1024px`):** 2-column cockpit layout (Left: Stats + Chart + Quick Add; Right: Transaction Feed).
   - **Tablet (`768px - 1023px`):** Balanced 2-column layout with comfortable touch targets.
   - **Mobile (`< 768px`):** Tabbed panel switcher (`[Overview] [History] [Add Record]`) so the UI stays clean and zero-scroll even on mobile.
4. **Pedagogical Code Quality:** Clean, modular React functional components with descriptive prop types, hooks (`useState`, `useEffect`), and zero bloat.

---

## 🎨 2. Color Palette & Neumorphic Tokens

Use the user's curated Earth/Forest palette:
* Canvas/Background: `#283618` (Deep Forest Olive)
* Income/Highlight: `#606c38` (Muted Leaf Olive)
* Text/Primary Light: `#fefae0` (Warm Cornsilk Cream)
* Accent/Buttons: `#dda15e` (Golden Sand/Ochre)
* Expense/Alert: `#bc6c25` (Warm Terracotta / Rust)

Put these tokens into `frontend/src/index.css`:

```css
:root {
  /* Earth-Tone Canvas & Accents */
  --bg-canvas: #283618;
  --color-income: #606c38;
  --color-text-primary: #fefae0;
  --color-text-secondary: rgba(254, 250, 224, 0.7);
  --color-accent: #dda15e;
  --color-expense: #bc6c25;

  /* Earth Neumorphic Shadow Math (Light from Top-Left, Dark to Bottom-Right) */
  --neu-light: rgba(254, 250, 224, 0.08); /* Soft sunlit rim */
  --neu-dark: #17200e;                    /* Deep moss shadow */

  /* Surface Elevations */
  --neu-card-shadow: 8px 8px 18px var(--neu-dark), -8px -8px 18px var(--neu-light);
  --neu-card-shadow-sm: 4px 4px 10px var(--neu-dark), -4px -4px 10px var(--neu-light);
  --neu-inset-shadow: inset 4px 4px 8px var(--neu-dark), inset -4px -4px 8px var(--neu-light);
  --neu-pressed-shadow: inset 3px 3px 6px var(--neu-dark), inset -3px -3px 6px var(--neu-light);

  /* Radii & Typography */
  --radius-card: 16px;
  --radius-input: 10px;
  --radius-pill: 9999px;
  --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
```

---

## 🧩 3. Component Architecture

Organize the React application into clear, single-responsibility components inside `frontend/src/`:

```
frontend/src/
├── components/
│   ├── StatCards.jsx        <-- 3 Extruded cards: Total Income, Total Expenses, Net Savings
│   ├── SpendingChart.jsx    <-- Donut chart showing expenses breakdown by category
│   ├── TransactionForm.jsx  <-- Debossed inset inputs + tactile submit button
│   ├── TransactionFeed.jsx  <-- Scrollable feed/table with delete buttons
│   └── MobileNav.jsx        <-- Panel switcher for screens < 768px
├── services/
│   └── api.js               <-- Centralized fetch helper functions (GET, POST, DELETE)
├── App.jsx                  <-- State management (transactions, summary), responsive layout
├── main.jsx                 <-- React root entry point
└── index.css                <-- Neumorphic CSS variables, utility classes, and responsive grid
```

### Component Roles:
1. **`StatCards.jsx`**:
   - 3 Neumorphic extruded cards.
   - Income displayed with `#606c38` indicator badge.
   - Expense displayed with `#bc6c25` indicator badge.
   - Net Savings displayed with dynamic color (`#606c38` if positive, `#bc6c25` if negative).
2. **`SpendingChart.jsx`**:
   - Donut chart (using `chart.js` + `react-chartjs-2`, or pure SVG/CSS donut).
   - Shows expense distribution across categories.
3. **`TransactionForm.jsx`**:
   - Inset debossed input fields for: `amount`, `category`, `description`.
   - Tactile pill toggle button for `type`: `[ Income | Expense ]`.
   - Submit button extruded with `--color-accent: #dda15e`, flipping to pressed state on click.
4. **`TransactionFeed.jsx`**:
   - Fixed height container with `overflow-y: auto` and a custom sleek scrollbar.
   - Shows date, description, category tag, colored amount (+ for income, - for expense).
   - Tactile trash/delete button on each row.
5. **`MobileNav.jsx`**:
   - Rendered only on mobile (`< 768px`).
   - Switches active view: `[Summary]`, `[Chart]`, `[History]`, `[Add]`.

---

## 🔌 4. API Endpoints & Contracts

All requests go to the backend (via Vite proxy configured to `http://localhost:5000`):

1. **Get Summary:**
   - `GET /finance_tracker/summary`
   - Response:
     ```json
     {
       "summary": {
         "total_income": 1500.00,
         "total_expenses": 450.50,
         "net_savings": 1049.50
       }
     }
     ```
2. **Get Transactions:**
   - `GET /finance_tracker`
   - Response: Array of transaction objects `[ { id, amount, type, category, description, logged_at }, ... ]`
3. **Add Transaction:**
   - `POST /finance_tracker`
   - Headers: `{ "Content-Type": "application/json" }`
   - Body:
     ```json
     {
       "amount": 45.00,
       "type": "expense",
       "category": "groceries",
       "description": "Weekly grocery trip"
     }
     ```
4. **Delete Transaction:**
   - `DELETE /finance_tracker/<id>`
   - Headers: `{ "Content-Type": "application/json" }`
   - Body: `{ "type": "expense" }` (or `"income"`)

---

## 🛠️ 5. Step-by-Step Execution Plan

### Step 1: Initialize Vite React Project
Run in project root:
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install chart.js react-chartjs-2
```

### Step 2: Configure Vite Proxy
In `frontend/vite.config.js`, configure proxy so API requests forward cleanly to Flask at `http://localhost:5000`:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/finance_tracker': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      }
    }
  }
})
```

### Step 3: Implement Design Tokens & Utilities
Write `frontend/src/index.css` with the Earth Neumorphic tokens, utility classes (`.neu-card`, `.neu-inset`, `.neu-btn`), and the desktop 100vh zero-scroll layout.

### Step 4: Build Components & Wire State
Create `api.js`, `StatCards.jsx`, `SpendingChart.jsx`, `TransactionForm.jsx`, `TransactionFeed.jsx`, and assemble in `App.jsx`.
Ensure when a transaction is added or deleted, both the summary and transaction feed refresh immediately!
