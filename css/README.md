# CSS Directory

Stylesheets for Chunhua Shen's academic website.

## File Overview

| File | Purpose |
|------|---------|
| `cs.css` | Main layout: `#layout-content` width/padding, footer, table, and font styles |
| `menu_style.css` | Top navigation bar (`#menu`, `#nav`) |
| `content.css` | Page content styles: headings, lists, images, tables, fonts |
| `full_publication.css` | Publication list pages (paper.html, fullpaper.html, etc.) |
| `fonts_import.css` | `@font-face` declaration for EB Garamond |
| `link_icons.css` | Icon styles for paper links |
| `pub.css` | BibTeX-rendered publication styles |
| `proj.css` | Project page styles |
| `proj_index.css` | Project index page styles |
| `wider.css` | Utility class for wider layout |

## Change Log

### 2026-02-23 — Mobile responsiveness

Made the site compatible with mobile phones while preserving the existing desktop layout.

**`cs.css`**
- Added `@media (max-width: 600px)` block:
  - `#layout-content`: full-width with horizontal padding and `box-sizing: border-box`
  - `img`: fluid (`max-width: 100%; height: auto`)
  - `table`: horizontally scrollable (`display: block; overflow-x: auto`)
  - `.left`, `.right`: un-floated and centred
  - `.rounded-img2`: fluid width

**`menu_style.css`**
- Added `@media (max-width: 600px)` block at end of file:
  - `#nav`: switched from `float: right` to `display: flex; flex-wrap: wrap` for wrapping nav links on small screens

**`content.css`**
- `div#toptitle`: added `clear: both` so the heading always starts below the floated nav bar, preventing layout bleed and ensuring `h1` centering is not broken

**`cs.conf`** (site template, not a CSS file)
- Added `<meta name="viewport" content="width=device-width, initial-scale=1.0" />` to the HTML head template; also patched into all existing generated `.html` files
