# SEO — morning checklist

## Done overnight (no action needed)
- [x] ProfilePage `mainEntity` with inline Person (fixes Google Rich Results critical error)
- [x] `og.png` 1200×630 for LinkedIn/Facebook/Twitter previews
- [x] `profile:username` = tatarco
- [x] `llms.txt` for AI crawlers
- [x] `robots.txt` + `sitemap.xml`

## Re-scrape after deploy (~2 min)
1. [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/?q=https://gal.tidhar.org.il/) → **Scrape Again**
2. [Rich Results Test](https://search.google.com/test/rich-results?url=https://gal.tidhar.org.il/)

## Only you can do (needs your account)
### `fb:app_id` warning
Facebook shows “missing fb:app_id” — **optional** for link previews; only needed for Facebook Insights.

1. Go to [developers.facebook.com](https://developers.facebook.com/) → Create App → type “Other”
2. Copy **App ID**
3. Add to `index.html` `<head>`:
   ```html
   <meta property="fb:app_id" content="YOUR_APP_ID" />
   ```

### Google Search Console
1. Add property `https://gal.tidhar.org.il/`
2. Verify (DNS TXT on tidhar.org.il or HTML file)
3. Submit sitemap: `https://gal.tidhar.org.il/sitemap.xml`

### HTTP 206 on Facebook scrape
GitHub Pages returns **206 Partial Content** when crawlers send `Range` headers. This is normal; previews still work. No fix required.
