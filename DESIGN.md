# Rollable design framework

How Rollable pages look, read and are built. The reference implementation is
[concepts/nordic/](concepts/nordic/): a shared stylesheet, ten layout patterns
and an index page. Start every new page from there.

Open them locally: `python3 -m http.server 8765` in this folder, then
http://localhost:8765/concepts/nordic/.

## Principles

1. **Short.** A page fits about one laptop screen (1440×900). If it needs more,
   it is probably two pages.
2. **Informative and concrete.** Say plainly what Rollable Labs is, how it works,
   what is running and how to get in touch. Facts over slogans.
3. **Nordic tone.** Calm, plain, functional. Lots of air, thin rules, left-aligned
   text, nothing decorative that doesn't carry information.
4. **One typeface.** Inter only, as in the logo. No serif display fonts, no italics.
5. **No highlighted key words.** Emphasis comes from weight (400 → 500) and from
   position, never from grey or coloured words inside a sentence.
6. **Modest sizes.** Headlines are 26–28px. Nothing shouts.
7. **The layout carries meaning.** Choose a layout because its shape explains
   something, e.g. a lab's position on a track *is* its stage.
8. **Try, but don't push too far.** One idea per page. If an effect needs
   explaining, leave it out.
9. **Say little about the projects.** Public pages name a lab by field and stage
   only. No screenshots, product names or feature lists.

## Tokens

Defined once in [concepts/nordic/base.css](concepts/nordic/base.css).

| Token | Value | Use |
|---|---|---|
| `--bg` | `#f6f5f2` | Page background (warm off-white) |
| `--paper` | `#ffffff` | Cards, sheets, the letter |
| `--ink` | `#1d1d1b` | Text, strong rules, dark panels |
| `--soft` | `#55544f` | Secondary paragraphs (whole paragraphs, never single words) |
| `--mute` | `#8d8b85` | Labels, numbers, footer |
| `--line` | `#e2e0da` | Hairline rules and borders |
| `--line-2` | `#cfccc4` | Stronger borders, link underlines |
| `--on` | `#2f7d5b` | Status: open beta |
| `--pilot` | `#b9822c` | Status: pilot |
| `--idle` | `#b3b0a8` | Status: research |

Colour appears only in status dots. Dark panels use `--ink` with `--bg` text.

## Type

| Role | Size / weight | Notes |
|---|---|---|
| Headline (h1) | 26–28px / 500 | Max ~2 lines, letter-spacing −0.015em |
| Section title (h2) | 20px / 500 | In squares and panels |
| Item title (h3) | 15px / 500 | Stage names, note titles |
| Body | 15px / 400, line-height 1.6 | |
| Secondary | 14px / 400 | Table cells, descriptions |
| Label | 12px / 400, `--mute` | Numbers, column heads, "Stage 1" |
| Logo | 18px, "Roll" 600 + "able" 300 `--mute` + "Labs" 13px | |

Tabular numbers are on everywhere (`tnum`). Inter is self-hosted from `/fonts`.

## Components

All in `base.css`; reuse, don't restyle.

- **Top bar** `.top`: logo left, one link right (email or "Contact").
  Top bar, content and footer share one column (max 1080px), so the logo lines
  up with the content's left edge on wide screens.
- **Footer** `.foot`: © line left, Privacy · Terms right, 12px muted.
- **Label** `.label`: small muted text for numbers and headings of lists.
- **Link** `a.u`: text with a 1px underline that darkens on hover. No buttons
  unless a page has a single main action.
- **Status dot** `.dot` / `.dot.on` / `.dot.pilot`: 7px circle before the stage.
  Always followed by the stage in words.
- **Paper card**: `--paper` background, 1px `--line` border, square corners (or
  4–6px at most). No heavy shadows.

## Standard content

Every page draws on the same four blocks. Keep the wording consistent.

- **What:** "We build AI tools that adapt to your organisation’s processes and
  goals." Longer: a studio that invents tools built on generative AI and machine
  learning. Instead of fixed software with fixed screens, each tool has a flexible
  interface that adapts to an organisation’s processes and goals, and can be
  shaped step by step toward a solution.
- **Different:** On premise: the tools run inside your organisation, no data leaves it.
  Measured, not guessed: machine learning measures what is true in your data, so
  every solution is reliable and measurable.
- **Method (four steps):** Pick one problem with a real team · Build the smallest
  tool that solves it · Use it on real work · Keep what works, stop what does not.
- **Labs:** 01 Sales — open beta · 02 Manufacturing — pilot · 03 Maintenance — research.
- **Contact:** hello@rollable.app.

End a page with one plain next step (a sentence and the email), never only a
link in the corner. Write in short, plain sentences. No superlatives, and no numbers, dates or
promises (e.g. response times) that aren't true.

## Layout patterns

Each pattern is one file in `concepts/nordic/`. Pick by what the page needs to explain.

| # | Pattern | Idea | Use it when |
|---|---|---|---|
| 01 | [Spec sheet](concepts/nordic/01-spec.html) | Every fact on a labelled row of one sheet | You need everything at a glance, like a data sheet |
| 02 | [Stage track](concepts/nordic/02-track.html) | Four stages on a line; each lab sits under its stage | Progress or status is the main message |
| 03 | [Ledger](concepts/nordic/03-ledger.html) | One statement, then a table: no., field, question, stage | Comparing several items on the same attributes |
| 04 | [Letter](concepts/nordic/04-letter.html) | A plain letter on paper; facts in the margin | The message is personal: an invitation or an update |
| 05 | [Four squares](concepts/nordic/05-squares.html) | What / How / Now / You in a 2×2 grid, last one dark | A complete overview in four equal parts |
| 06 | [Rings](concepts/nordic/06-rings.html) | Concentric rings; labs move outward as they mature | Maturity or distance from the core matters |
| 07 | [Questions](concepts/nordic/07-questions.html) | Five numbered questions with short answers (`<details>`) | Visitors arrive with questions; answer them directly |
| 08 | [Split](concepts/nordic/08-split.html) | Dark fixed panel left (who), numbered notes right (facts) | A clear identity plus a list of points |
| 09 | [Loop](concepts/nordic/09-loop.html) | The method as a flow of boxes with a return line | Explaining a process that repeats |
| 10 | [Board](concepts/nordic/10-board.html) | A calm station sign: numbered rows on a dark board | Directing people to a few destinations |

The [index page](concepts/nordic/index.html) is itself a pattern: a numbered
list of rows (number, name, one-line description) under a strong rule. Use it
for any catalogue: labs, documents, versions.

## Japanese touch

The homepage ([index.html](index.html), built on pattern 07) adds one quiet
Japanese element. Keep it to one per page:

- **Go board, drawn with a brush:** a whole 13×13 board seen slightly from
  above, with its thickness and short legs, in black ink only (no colour, no
  paper texture). Every line is a filled brush stroke (maobi): pressed at the
  start, thinner in the middle, tapering at the end, with light dry-brush
  streaks. The outline and legs are bold, the grid is fine. Black stones are ink
  blots; white stones are a brushed ring with a gap where the brush lifts. A
  corner sequence (a 4-4 point with a 3-3 invasion) is placed stone by stone, then
  a dashed ring marks the next point. Generated by
  [scripts/go-board.py](scripts/go-board.py); edit and rerun it rather than
  hand-editing the SVG. On desktop it sits beside the headline; on phones above it.
- **Ma (empty space):** the board stands alone in white space instead of more text.

Everything stays in English: no Japanese words or characters, and no brush
fonts, ensō circles or calligraphy. Animation is off for reduced motion.

## Lab apps

The labs (`rollable/labs/crm`, `production`, `panel-intel`) follow the same
philosophy inside the product. They are dense work tools, so pages may be longer
than one screen, but the rest holds:

- **Tokens:** the same palette as `base.css`. Old values map as
  `#1a1a18 → #1d1d1b`, `#6b6960 → #55544f`, `#9b9890 → #8d8b85`,
  `#c8c5be → #cfccc4`, `#f5f4f0 → #f6f5f2`; status green `#2f7d5b`, amber
  `#b9822c`, error red `#b4483c`.
- **Type:** Inter only (`next/font`), with tabular figures. Weights 400 and 500;
  the only 600 is "Roll" in the logo. No monospace, even for IDs and numbers.
- **Labels:** sentence case, no uppercase, no letter-spacing.
- **Corners:** 6px for cards, buttons and inputs (8px for the largest panels);
  pills and avatars stay round.
- **Sidebar and sign-in:** the "**Roll**able" logo with the lab's name beneath it
  (sidebar), or logo + "Labs", the lab's name as a 26px heading and its access
  ("By invitation") on the sign-in page.
- **Charts:** data may use colour, but calmly: `--series-1` slate `#45627a`,
  then amber and green from the status palette.

[scripts/nordic-codemod.py](scripts/nordic-codemod.py) applies the tokens,
labels, monospace and corner rules to a lab's `src/` in one pass; run it on a
new lab, then typecheck and look at every page.

### Workspace (tool pages)

A lab page where people work on something — a signal, a batch, a pipeline — is
laid out like a design tool such as Figma. References:
`rollable/labs/production/src/app/(lab)/bearing-diagnosis/page.tsx` (a signal)
and `rollable/labs/panel-intel/src/app/(lab)/panels/[code]/page.tsx` (a panel,
whose first frame is a trace diagram of selectable nodes; shared styles in
Panel Intel's `globals.css` and `components/TraceWorkspace.tsx`).
Also `panel-intel/.../drivers/page.tsx` (analysis controls in the top bar) and
`crm/src/app/analytics/AnalyticsClient.tsx` (inside the CRM shell, which keeps
its own top bar; the views list is the left panel).

- **Left panel:** the lab sidebar, white with a hairline border: the logo and
  lab name, then "Pages" and "Tools" sections (12px headings, 6px row highlight).
- **Top bar (48px):** the path on the left ("Production / Bearing Diagnosis"),
  what is being worked on in the middle (e.g. the signal), the one primary action
  on the right (e.g. "Diagnose").
- **Canvas:** a slightly darker ground (`#efeeea`) holding **frames**: white,
  1px border, 6px corners, each titled with a 12px label above it. Frames hold
  the measured result as a chart drawn from real values; the empty state is a
  frame that says what to do first.
- **Inspector (300px, right):** tabs ("Result", "Method"), then sections of
  compact label/value rows. Clicking something on the canvas selects it and the
  inspector's first section shows it ("Selection"). Explanations and glossaries
  live in the "Method" tab, not on the canvas.
- **Narrow screens:** top bar, canvas and inspector stack in one column. The lab
  sidebar becomes a compact bar on top (logo, live pages, sign out; "Soon" items
  hidden). Charts keep a readable size (min 640px) and scroll sideways inside
  their frame; the page itself never scrolls sideways.

Don't add tool chrome that does nothing (fake zoom levels, layer lists, toolbars):
every control must work.

## Responsive rules

- 16px side gutter on phones, 40px on desktop; no horizontal scroll.
- Multi-column layouts collapse to one column at 760–860px.
- Diagrams keep their meaning on phones: the track and loop turn vertical,
  arrows turn into ↓.

## Build rules

- Static HTML plus `base.css`; a page's own layout CSS sits in its `<style>`.
- No JavaScript needed. If added, the page must work without it.
- No external fonts, libraries or images unless the page truly needs them.
- Animation, if any, is subtle and switched off for `prefers-reduced-motion`.

## Don't

- Serif or display fonts, italics, gradient or coloured text.
- Grey or coloured key words inside a sentence.
- Huge headlines, glows, particles, 3D, glass effects.
- Product screenshots or feature details on public pages.
- Invented metrics, logos, testimonials or promises.

## Starting a new page

1. Pick the pattern whose shape explains the content.
2. Copy its file, keep `base.css`, and replace the content using the standard blocks.
3. Check it at 1440×900 (about one screen) and at 390px wide.
