# 🎨 SKILL: Dark Neumorphic (Soft UI) Frontend Architecture

> **Skill Type:** Reusable Frontend Design & Engineering Capability  
> **Applicability:** Any Web Application, Dashboard, or Control Panel  
> **Tech Stack:** Semantic HTML5, Modern Vanilla CSS (Custom Properties), Vanilla JS

---

## 🧭 1. Skill Overview & Visual Philosophy

**Neumorphism (Soft UI)** merges flat design with realistic 3D physical modeling. Instead of floating elements on top of a background using arbitrary drop shadows, Neumorphic elements appear to be **sculpted directly from the background canvas**.

### The Core Physical Principle: A Single Directional Light Source
All Neumorphic illusions depend on a **single light source** positioned at the **top-left (-45°)**:
* **Top-Left Edges:** Catch light reflection ➔ **Light Highlight Shadow** (soft glow or tint).
* **Bottom-Right Edges:** Cast a shadow away from the light ➔ **Deep Dark Shadow**.
* **Canvas Uniformity:** Elements must share the **exact same background color** as the page canvas, differentiated only by their elevation shadows and curvature.

---

## 📐 2. The Neumorphic Mathematical Formula (CSS Tokens)

A Neumorphic system requires two distinct states: **Extruded (Outset)** and **Debossed (Inset)**.

```css
:root {
  /* 1. Base Canvas & Surface (Must Match or Closely Harmonize) */
  --neu-bg: #1e232d;
  --neu-surface: #212732;

  /* 2. Light & Shadow Values */
  --neu-shadow-dark: #14171f;                  /* Deep dark shadow (bottom-right) */
  --neu-shadow-light: rgba(255, 255, 255, 0.05); /* Soft highlight (top-left) */

  /* 3. Outset (Extruded / Raised Surfaces - Cards, Badges, Unpressed Buttons) */
  --neu-outset-lg: 8px 8px 18px var(--neu-shadow-dark),
                   -8px -8px 18px var(--neu-shadow-light);
  --neu-outset-sm: 4px 4px 10px var(--neu-shadow-dark),
                   -4px -4px 10px var(--neu-shadow-light);

  /* 4. Inset (Debossed / Carved Surfaces - Input Fields, Sliders, Active State) */
  --neu-inset-lg: inset 5px 5px 10px var(--neu-shadow-dark),
                  inset -5px -5px 10px var(--neu-shadow-light);
  --neu-inset-sm: inset 3px 3px 6px var(--neu-shadow-dark),
                  inset -3px -3px 6px var(--neu-shadow-light);

  /* 5. Radii (Neumorphism Requires Soft, Organic Curves) */
  --radius-card: 20px;
  --radius-input: 12px;
  --radius-pill: 9999px;
  
  /* 6. High-Contrast Semantic Accents (Crucial for Accessibility) */
  --color-success: #10b981;
  --color-danger: #f43f5e;
  --color-info: #6366f1;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
}
```

---

## 🛠️ 3. Component Blueprints

### A. The Extruded Card (Container / Panel)
Cards look molded outward from the canvas surface.
```css
.neu-card {
  background: var(--neu-bg);
  border-radius: var(--radius-card);
  box-shadow: var(--neu-outset-lg);
  padding: 24px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.neu-card:hover {
  transform: translateY(-2px);
  box-shadow: 10px 10px 22px var(--neu-shadow-dark),
              -10px -10px 22px var(--neu-shadow-light);
}
```

### B. The Debossed Input Field (Form Control)
Input fields look pressed into the canvas, as if carved out to receive text.
```css
.neu-input {
  width: 100%;
  background: var(--neu-bg);
  border: 1px solid transparent;
  border-radius: var(--radius-input);
  box-shadow: var(--neu-inset-lg);
  padding: 12px 16px;
  color: var(--text-primary);
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.neu-input:focus {
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: inset 6px 6px 12px var(--neu-shadow-dark),
              inset -6px -6px 12px var(--neu-shadow-light);
}
```

### C. The Tactile Interactive Button
A button starts extruded. When clicked (`:active`), it flips its shadow to inset, simulating a real physical switch.
```css
.neu-button {
  background: var(--neu-bg);
  border: none;
  border-radius: var(--radius-pill);
  box-shadow: var(--neu-outset-sm);
  padding: 12px 24px;
  color: var(--text-primary);
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.neu-button:active,
.neu-button.active {
  box-shadow: var(--neu-inset-sm);
  transform: scale(0.98);
}
```

---

## 🖥️ 4. Layout Architecture: The "Zero-Scroll Cockpit"

When tasked with building a modern cockpit/dashboard:
1. **Desktop Viewport Rule (`min-width: 1024px`):**
   * `body { height: 100vh; overflow: hidden; margin: 0; }`
   * Never let the outer webpage scroll vertically.
   * If a table, activity feed, or list has 50 items, that specific component must have its own internal scrolling:
     ```css
     .scroll-pane {
       overflow-y: auto;
       max-height: 100%;
     }
     ```
2. **The 8-Point Spacing Grid:**
   * All padding and margins must be multiples of 4 or 8 (`8px`, `16px`, `24px`, `32px`). This ensures structural harmony.
3. **Mobile Adaptability (`max-width: 1023px`):**
   * On smaller screens where 100vh cannot fit everything comfortably, implement a **Panel Switcher** (tabs) to view one panel at a time, keeping the interface uncluttered.

---

## ♿ 5. The Accessibility Golden Rule (Overcoming Neumorphic Pitfalls)

> [!WARNING]
> Traditional light neumorphism often fails accessibility because of poor contrast between white plastic and light gray text.

To ensure professional-grade, WCAG-compliant design:
1. **Always Use High-Contrast Dark Themes:** White/light gray text (`#f8fafc`) on deep dark slate surfaces (`#1e232d`) ensures high readability.
2. **Never Rely on Shadows Alone:** Always accompany key metrics and buttons with **vibrant color accents** (emerald green for positive metrics, coral red for negative metrics, indigo for primary actions).
3. **Explicit Focus States:** Form inputs must display a subtle colored border or accent glow on `:focus-visible`.

---

## 📋 6. Agent Implementation Protocol

When instructed to apply this skill to a project:
1. **Define the CSS tokens first** in a master stylesheet.
2. **Build clean semantic HTML** adhering to the 100vh layout hierarchy.
3. **Wire user interactions** with tactile CSS `:active` / `:hover` states.
4. **Keep code modular and readable**, clearly explaining design tokens so the human engineer can understand and refine the interface.
