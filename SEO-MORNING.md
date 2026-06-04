# SEO — your action list

Everything technical is deployed. Three items need **your** accounts (≈15 min total).

---

## 1. Google Search Console (≈10 min) — **do this first**

Gets you indexed and shows search queries.

1. Open **[Google Search Console](https://search.google.com/search-console/welcome)**
2. **Add property** → choose **URL prefix** → enter: `https://gal.tidhar.org.il`
3. **Verify ownership** — pick one:
   - **DNS** (best if you manage `tidhar.org.il`): add the TXT record Google gives you at your DNS host (Cloudflare, etc.)
   - **HTML file**: download their file → put it in the `gal-tidhar` repo root → push → click Verify in GSC
   - **HTML tag**: copy the `content="..."` value → send it to Gal / add this line to `index.html` `<head>`:
     ```html
     <meta name="google-site-verification" content="PASTE_VALUE_HERE" />
     ```
4. After verified: **Sitemaps** (left menu) → add: `https://gal.tidhar.org.il/sitemap.xml` → Submit
5. **URL inspection** → paste `https://gal.tidhar.org.il/` → **Request indexing**

---

## 2. Re-scrape social previews (≈2 min)

Confirms Facebook/LinkedIn use the new `og.png`.

1. **[Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/?q=https://gal.tidhar.org.il/)** → enter URL → **Scrape Again**
2. **[Rich Results Test](https://search.google.com/test/rich-results?url=https://gal.tidhar.org.il/)** → Test URL → confirm **no critical errors** on ProfilePage

Expected:
- Image: blueprint banner `og.png` (not portrait-only)
- Warning `fb:app_id` is OK to ignore unless you want Facebook analytics (step 3)

---

## 3. Facebook `fb:app_id` (optional, ≈5 min)

**Only if** you want to clear the debugger warning / use Facebook Insights. Link previews work without it.

1. **[developers.facebook.com](https://developers.facebook.com/)** → **My Apps** → **Create App**
2. Use case: **Other** → name e.g. `Gal Portfolio` → Create
3. **Settings → Basic** → copy **App ID** (numeric)
4. Add to `index.html` in `<head>` (after other `og:` tags):
   ```html
   <meta property="fb:app_id" content="YOUR_NUMERIC_APP_ID" />
   ```
5. Push to `gal-tidhar` → Scrape Again in debugger

---

## Already done (no action)

| Item | Status |
|------|--------|
| `robots.txt` + `sitemap.xml` | Live |
| `og.png` 1200×630 | Live |
| ProfilePage `mainEntity` → Person | Live |
| `llms.txt` | Live |
| Canonical, schema, Twitter card meta | Live |

**HTTP 206** on Facebook scrape = normal for GitHub Pages (range requests). Ignore it.

---

## Optional later

- **Bing Webmaster**: [bing.com/webmasters](https://www.bing.com/webmasters) → add site → submit same sitemap
- **LinkedIn**: post once with your portfolio URL (helps branded search)
- **Cross-links**: add `https://gal.tidhar.org.il` to GitHub profile, LinkedIn featured, ZaZet footer
