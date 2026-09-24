# 💹 Top Metric Cards — `StatCards` Guide

> **Phase Goal:** Build the three Top Metric Cards — **Total Income**, **Total Expenses**, **Net Savings** — as a clean, presentational component, styled to our Figma "North Star" with the bespoke Neumorphic Earth palette.
> **Component path:** `src/components/features/summary/StatCards.jsx`
> **Data contract (Flask API):** `{ summary: { total_income, total_expenses, net_savings } }`

---

## 1. CSS — Add to `frontend/src/index.css`

These rules define the dark card surface, the ambient Wine glow + dual neumorphic shadows, the pill badges, and the typography tokens.

```css
/* ============================================================
   STAT CARDS — Dark Charcoal surface, Wine ambient glow
   ============================================================ */
.stat-card {
  flex: 1;                             /* Distribute 3 cards evenly across metrics-row */
  min-width: 0;                        /* Prevent flex child from overflowing text container */
  background: #181212;                 /* dark charcoal surface */
  border-radius: 16px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  color: #F8E0A4;                      /* champagne cream text */

  /* Ambient Wine glow + dual neumorphic shadows */
  box-shadow:
    0 8px 24px rgba(108, 26, 26, 0.45),      /* ambient wine glow */
    0 10px 20px rgba(0, 0, 0, 0.35),          /* soft drop shadow */
    inset 0 1px 0 rgba(255, 255, 255, 0.06);  /* subtle top edge highlight */
  border: 1px solid rgba(108, 26, 26, 0.35);
}

.stat-card__label {
  font-size: 0.8rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  opacity: 0.75;
  font-weight: 600;
}

.stat-card__amount {
  font-size: clamp(1.4rem, 2vw, 2rem);  /* Fluid scaling across responsive viewports */
  font-weight: 800;
  line-height: 1.1;
  font-variant-numeric: tabular-nums;   /* keep digits aligned */
}

/* Pill badges */
.stat-badge {
  align-self: flex-start;
  padding: 4px 12px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}
.stat-badge--income   { background: #31AAA9; color: #181212; } /* +Inflow */
.stat-badge--expense  { background: #A82020; color: #F8E0A4; } /* -Outflow */
.stat-badge--surplus  { background: #F8E0A4; color: #181212; } /* Surplus */
.stat-badge--deficit  { background: #A82020; color: #F8E0A4; } /* Deficit */
```

---

## 2. Component — `src/components/features/summary/StatCards.jsx`

```jsx
// A small presentational tile for a single metric, reused 3x.
function StatCard({ label, badge, badgeClass, amount }) {
  return (
    <article className="stat-card">
      <span className="stat-card__label">{label}</span>
      <span className="stat-card__amount">{amount}</span>
      <span className={`stat-badge ${badgeClass}`}>{badge}</span>
    </article>
  )
}

export default function StatCards({ summary }) {
  // Defensive normalization: never crash on null/undefined values.
  const income  = Number(summary?.total_income  || 0)
  const expense = Number(summary?.total_expenses || 0)
  const net     = Number(summary?.net_savings   || 0)

  // Dynamic badge: Surplus vs Deficit based on sign.
  const netBadge = net >= 0 ? 'Surplus' : 'Deficit'
  const netBadgeClass = net >= 0 ? 'stat-badge--surplus' : 'stat-badge--deficit'

  const fmt = (value) =>
    value.toLocaleString(undefined, { minimumFractionDigits: 2 })

  return (
    <header className="metrics-row">
      <StatCard label="Total Income"  badge="+Inflow"  badgeClass="stat-badge--income"  amount={fmt(income)} />
      <StatCard label="Total Expenses" badge="-Outflow" badgeClass="stat-badge--expense" amount={fmt(expense)} />
      <StatCard label="Net Savings"   badge={netBadge} badgeClass={netBadgeClass}      amount={fmt(net)} />
    </header>
  )
}
```

---

## 3. Wiring into `src/App.jsx`

Because `App.jsx` is the **composition root** (it owns the data), it fetches `summary` and passes it down.

```jsx
import StatCards from './components/features/summary/StatCards'

export default function App() {
  // ... existing app-shell & resize logic ...

  // Data comes from the Flask summary endpoint, e.g.:
  const summary = { total_income: 3200, total_expenses: 1960, net_savings: 1240 }

  return (
    <div className="app-shell">
      {/* ---- Top row: StatCards is its own semantic header flex container ---- */}
      <StatCards summary={summary} />

      {/* ... body-grid / body-stacked ... */}
    </div>
  )
}
```

> `StatCards` renders semantic `<header className="metrics-row">` (with `display: flex; gap: 12px;`), so the three cards distribute evenly across the top. Placing `<StatCards summary={summary} />` directly inside `.app-shell` replaces the temporary wireframe `<header className="metrics-row">` without requiring a double-nested flex wrapper.

---

## 4. Line-by-Line Breakdown

### 4.1 React props & object destructuring

```jsx
export default function StatCards({ summary }) { ... }
```

- `function StatCards({ summary })` is a **function component**. It receives a single argument object — the "props" — and React calls it with the JSX attributes you wrote in `App.jsx`: `<StatCards summary={summary} />`.
- `{ summary }` is **object destructuring** in the parameter list. The props object looks like `{ summary: {...} }`, and destructuring pulls out only the `summary` key into a local variable. It's shorthand for `function StatCards(props) { const summary = props.summary }`.
- Inside, `function StatCard({ label, badge, badgeClass, amount })` does the same: it pulls exactly the four props it needs. Keeping cards presentational this way makes them **reusable and testable** — they render whatever they're given and never fetch anything themselves.

### 4.2 Why defensive normalization (`data?.total_income || 0`) prevents crashes

```jsx
const income = Number(summary?.total_income || 0)
```

- `summary?.total_income` uses the **optional chaining** operator (`?.`). If `summary` is `null`/`undefined`, the expression short-circuits to `undefined` **instead of throwing** `TypeError: Cannot read properties of undefined`. Without `?.`, `summary.total_income` on a `undefined` summary crashes the whole app on first render.
- `|| 0` is the **nullish fallback** for empty values. If `total_income` is `null`, `''`, or `undefined`, the result becomes `0`. (Note: `|| 0` also converts `NaN`, and treats falsy values as zero — acceptable here for a money display.)
- `Number(...)` wraps the result to guarantee a **number type** even if the API returns a string like `"3200"`. This matters because a string would silently break `.toLocaleString()` and any later arithmetic.
- Net effect: **no matter what the API returns** (missing, null, string, or a real number), the component renders a valid `0.00` rather than crashing or printing `undefined`.

### 4.3 How `toLocaleString()` formats commas & decimals

```jsx
const fmt = (value) => value.toLocaleString(undefined, { minimumFractionDigits: 2 })
```

- `.toLocaleString(undefined, options)` converts a number to a **locale-aware string**. The first arg `undefined` means "use the user's runtime locale" (e.g. `en-US`, `en-GB`), which automatically picks the right **thousands separator** (`,` in US, `.` in many European locales) and decimal symbol.
- The options object controls precision:
  - `minimumFractionDigits: 2` forces **at least two decimals**, so `1240` → `"1,240.00"` (or `"1.240,00"` in a comma-decimal locale). This makes monetary values always show a clean cents pair.
  - You can also add `maximumFractionDigits` if you want to cap precision, but for currency you usually want exactly two, so `minimumFractionDigits: 2` is the key one.
- Because `fmt` is applied to the already-normalized number, `fmt(1240)` returns the formatted string; the component never has to worry about `NaN` or non-numeric input.

### 4.4 Flex distribution (`flex: 1`) & fluid typography (`clamp`)

- `flex: 1`: In `.stat-card`, `flex: 1` instructs the flex container (`.metrics-row`) to divide the horizontal width into 3 equal 33.3% columns (accounting for `gap: 12px`).
- `min-width: 0`: Flexbox items by default have `min-width: auto`, which prevents them from shrinking below their content size. Adding `min-width: 0` prevents large numbers from pushing the cards beyond the screen edges on narrow viewports.
- `font-size: clamp(1.4rem, 2vw, 2rem)`: Fluid typography calculates an optimal font size: a minimum of `1.4rem` on small mobile screens, scaling dynamically with viewport width (`2vw`), capped at a crisp `2rem` on desktop displays.

---

## 5. Quick Visual & Logic Check

- **Income card:** label `Total Income`, badge `+Inflow` (teal `#31AAA9`), amount formatted like `3,200.00`.
- **Expense card:** label `Total Expenses`, badge `-Outflow` (crimson `#A82020`), amount like `1,960.00`.
- **Net card:** label `Net Savings`, badge **`Surplus`** (champagne) if `net >= 0`, else **`Deficit`** (crimson). Pass `net_savings` negative in the API to confirm the badge flips.
- All numbers use tabular numerals (`font-variant-numeric: tabular-nums`) so the digit columns stay aligned as values change.
