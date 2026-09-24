# 🧩 Finance Tracker — UI/UX Component Architecture

> **Purpose:** A reference blueprint for organizing React components before writing code.
> **Style:** Bespoke Neumorphic (Earth palette, 3-layer elevation, zero-scroll cockpit).

---

## 1. Golden Rule: Container vs. Presentational

Split every feature into two roles so components stay dumb and reusable:

- **Container** — knows *data* (fetches, state, handlers). Tells children what to render.
- **Presentational** — knows *look*. Receives props, renders markup, emits events.

`App.jsx` is the **composition root** (single source of truth for data). Everything below it is presentational unless marked as a feature container.

---

## 2. Directory Tree

```
frontend/src/
├── main.jsx                     # ReactDOM entry
├── App.jsx                      # COMPOSITION ROOT — owns all state + data fetching
├── index.css                    # DESIGN SYSTEM: tokens (:root) + .neu-* utility classes
│
├── components/
│   ├── layout/                  # page skeleton & placement (no business logic)
│   │   ├── DashboardLayout.jsx  # zero-scroll 100vh grid
│   │   ├── Header.jsx           # title + net balance banner
│   │   └── MobileTabBar.jsx     # mobile-only view switcher
│   │
│   ├── ui/                      # reusable dumb primitives (the "design language")
│   │   ├── NeuPanel.jsx         # elevated card surface (.neu-panel)
│   │   ├── NeuButton.jsx        # tactile button (raised / pressed via :active)
│   │   ├── NeuInput.jsx         # debossed inset field (.neu-inset)
│   │   ├── NeuToggle.jsx        # [+ Income | − Expense] switch
│   │   ├── Badge.jsx            # semantic label (income/expense/neutral)
│   │   ├── Modal.jsx            # base overlay + transition shell
│   │   ├── ConfirmDialog.jsx    # "Are you sure? This cannot be undone."
│   │   └── EmptyState.jsx       # friendly fallback when no data
│   │
│   ├── features/                # feature-scoped containers + their presenters
│   │   ├── summary/
│   │   │   ├── SummarySection.jsx     # CONTAINER: renders 3 StatCards
│   │   │   └── StatCard.jsx           # presentational metric tile
│   │   │
│   │   ├── chart/
│   │   │   ├── SpendingChart.jsx      # CONTAINER: aggregates by category
│   │   │   └── CategoryLegend.jsx     # presentational color-key list
│   │   │
│   │   └── transactions/
│   │       ├── TransactionSection.jsx # CONTAINER: feed + add + modals
│   │       ├── TransactionForm.jsx    # quick-add (controlled inputs)
│   │       ├── TransactionTable.jsx   # presentational table
│   │       ├── TransactionRow.jsx     # one row + edit/delete actions
│   │       ├── EditTransactionModal.jsx  # PATCH form
│   │       └── DeleteConfirmModal.jsx # safety confirm → DELETE
│   │
│   ├── services/
│   │   └── api.js               # ALL network I/O (5 CRUD endpoints)
│   │
│   ├── hooks/
│   │   ├── useTransactions.js   # fetch + create/update/delete state
│   │   ├── useSummary.js        # derived income/expense/net
│   │   └── useModal.js          # open/close/confirm dialog state
│   │
│   └── utils/
│       ├── format.js            # currency & number formatting (defensive || 0)
│       └── aggregate.js         # filter + reduce expenses by category
```

---

## 3. Why This Split (Rules of Thumb)

| Question | Answer |
| :--- | :--- |
| Does it fetch data or hold state? | Put it in a **container / hook**, not the UI. |
| Is it reusable in multiple places? | Put it in **`ui/`** (NeuButton, Modal). |
| Does it belong to one screen's feature? | Put it in **`features/<name>/`**. |
| Is it pure math/formatting? | Put it in **`utils/`**. |
| Is it a page structure concern? | Put it in **`layout/`**. |

- **`ui/`** must never know about transactions, categories, or your API. It only knows *look + events*.
- **`services/api.js`** is the *only* file that touches `fetch()`. Components never call fetch directly.
- **`App.jsx`** passes data down and handlers down; children never reach up to fetch again.

---

## 4. Data Flow (One-Way)

```
         ┌─────────────── App.jsx (owns state) ───────────────┐
         │  useTransactions()  useSummary()  useModal()       │
         └───────┬───────────────────────┬───────────────────┘
                 │ props                 │ props
        ┌────────▼────────┐      ┌───────▼───────────┐
        │ SummarySection  │      │ TransactionSection│
        │  → StatCard×3   │      │  → TransactionForm│
        └─────────────────┘      │  → TransactionTable
                 ┌───────────────┴────────────────────┐
                 │ SpendingChart → CategoryLegend      │
                 │ EditTransactionModal / DeleteModal  │
                 └───────────────┬────────────────────┘
                                 │ events bubble UP as callbacks
                                 ▼
                       services/api.js → fetch → backend
```

**Pattern:** State lives at the top → flows down as props → user events bubble up as callbacks → `App.jsx` updates state → re-render.

---

## 5. Wireframe — Desktop "Cockpit" (1920×1080, zero-scroll)

```
┌─────────────────────────────────────────────────────────────┐
│ HEADER            Finance Tracker        Net: ▲ $1,240.00   │
├───────────────┬─────────────────────────────────────────────┤
│  QUICK ADD    │  SUMMARY (3 StatCards in a row)             │
│  (form,       │  ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│   inset)      │  │ Income  │ │ Expense │ │   Net   │        │
│               │  │ $3,200  │ │ $1,960  │ │ $1,240  │        │
│               │  └─────────┘ └─────────┘ └─────────┘        │
│               ├─────────────────────────────────────────────┤
│               │  SPENDING (Donut)        ACTIVITY FEED      │
│               │  ┌────────────┐  ┌───────────────────┐      │
│               │  │  🍩 chart  │  │  Table of txs     │      │
│               │  │  + legend  │  │  [Edit] [Delete]  │      │
│               │  └────────────┘  └───────────────────┘      │
└───────────────┴─────────────────────────────────────────────┘
```

**Mobile (375×667):** `MobileTabBar` switches between 3 stacked views — Summary / Chart / Feed. No horizontal scroll.

---

## 6. Recommended Build Order (dependency-first)

1. **`index.css`** — tokens + `.neu-panel/.neu-inset/.neu-btn` utilities
2. **`ui/` primitives** — NeuPanel, NeuButton, NeuInput, NeuToggle, Badge, Modal
3. **`services/api.js`** + **`utils/`** (format, aggregate)
4. **`hooks/`** — useTransactions, useSummary, useModal
5. **`features/`** — summary → chart → transactions (form, table, modals)
6. **`layout/`** + **`App.jsx`** — assemble cockpit + wire data

> Build bottom-up: primitives first (no dependencies), features next, composition root last.
