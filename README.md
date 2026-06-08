# Gold-Advisor.com

Static affiliate/authority site (gold investing + Gold IRA reviews). Pure HTML/CSS/JS — no build step required to serve.

## Hosting (GitHub Pages)
1. Push this repo to GitHub (`main` branch).
2. Repo → Settings → Pages → Source: "Deploy from a branch", Branch: `main` / `/ (root)`.
3. The included `CNAME` sets the custom domain to `gold-advisor.com`. Point your DNS at GitHub:
   - Apex A records → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - (optional) `www` CNAME → `eranmeital-ship-it.github.io`
4. In Pages settings, tick **Enforce HTTPS** once the cert is issued.

`.nojekyll` is included so GitHub serves files as-is. Custom `404.html` and clean URLs (`/path/` → `/path/index.html`) work automatically.

## Notes
- The site must be served at the **domain root** over HTTPS (root-relative `/visit/...` affiliate links and `/affiliates.js`).
- After going live: submit `sitemap.xml` in Google Search Console.
