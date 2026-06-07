# Gold-Advisor.com — SEO & Content Strategy

A build plan for an authority site in the Gold IRA / precious-metals niche.
Read this before scaling pages — this niche is one of the most competitive
and most heavily spam-policed on the web.

---

## 0. Read this first: the two things that sink gold-IRA sites

This is a **YMYL ("Your Money or Your Life") + affiliate** niche. Google
holds it to its highest quality bar, and two specific mistakes get sites
deindexed:

1. **Doorway / "scaled content" pages.** Hundreds of "Invest in Gold in
   [City]" pages that are identical except for a swapped name violate
   Google's spam policies directly. This is the single most common way
   gold/affiliate sites get penalised. The generator in this project is
   built to avoid it — each page must carry unique local data and a
   hand-written local angle. **Do not remove that guardrail.**

2. **No demonstrable expertise (E-E-A-T).** Pages that make money/tax
   claims with no named author, no sources, and no editorial standards
   underperform badly here. Fixes: a real "About / Methodology" page, named
   authors with bios, citations to the IRS and primary sources, dates on
   every page, and a visible affiliate disclosure (FTC requires it anyway).

Everything below assumes you're doing those two things right.

---

## 1. Site architecture (topic silos)

Organise around clusters, not a flat pile of keyword pages. Each silo has
one **pillar page** linking down to **supporting pages**, which link back up.

```
HOME  (how to buy gold + open a gold IRA)
│
├── /gold-ira/                         ← PILLAR: "What is a Gold IRA"
│   ├── /gold-ira-rules-2026/
│   ├── /gold-ira-fees/
│   ├── /gold-ira-pros-and-cons/
│   ├── /gold-ira-vs-physical-gold/
│   ├── /ira-approved-gold-coins-bars/
│   └── /best-gold-ira-companies/       ← money page (comparison)
│
├── /precious-metals-ira/             ← PILLAR
│   ├── /silver-ira/
│   ├── /platinum-palladium-ira/
│   └── /precious-metals-ira-rules/
│
├── /401k-to-gold/                    ← PILLAR: rollovers
│   ├── /401k-to-gold-ira-rollover/
│   ├── /403b-to-gold/
│   ├── /tsp-to-gold/
│   └── /gold-ira-rollover-guide/
│
├── /how-to-buy-gold/                 ← PILLAR: physical buying
│   ├── /buy-gold-bars/
│   ├── /buy-gold-coins/
│   ├── /gold-bullion-vs-coins/
│   └── /how-to-store-physical-gold/
│
├── /gold-ira-companies/              ← reviews (one page per real, vetted firm)
│   └── /[company-name]-review/
│
└── /invest-in-gold/                  ← PILLAR: local hub
    └── /[state]/                      ← programmatic, unique-data pages
```

---

## 2. Keyword map by silo

Grouped by **search intent**. "Commercial/transactional" = closest to a
sale (your money pages). "Informational" = top-of-funnel (your traffic and
trust builders that link to the money pages).

### Silo A — Gold IRA (core)
| Keyword cluster | Intent | Target page |
|---|---|---|
| gold ira, what is a gold ira, gold ira explained | Info | /gold-ira/ |
| gold ira rules, gold ira rules 2026, irs gold ira rules | Info | /gold-ira-rules-2026/ |
| gold ira fees, gold ira cost, gold ira storage fees | Info/Comm | /gold-ira-fees/ |
| gold ira pros and cons, is a gold ira a good idea, gold ira risks | Info | /gold-ira-pros-and-cons/ |
| best gold ira, best gold ira companies, top gold ira companies | Commercial | /best-gold-ira-companies/ |
| ira approved gold, ira eligible gold coins, ira approved bullion | Info | /ira-approved-gold-coins-bars/ |
| home storage gold ira, home storage gold ira rules | Info | /gold-ira-rules-2026/ (section) |

### Silo B — Gold-backed / Precious Metals IRA
| Keyword cluster | Intent | Target page |
|---|---|---|
| gold backed ira, gold backed roth ira | Info | /gold-ira/ (variant) |
| precious metals ira, precious metals ira rules, self directed precious metals ira | Info | /precious-metals-ira/ |
| silver ira, silver ira rollover, best silver ira | Info/Comm | /silver-ira/ |
| platinum ira, palladium ira | Info | /platinum-palladium-ira/ |

### Silo C — 401(k) / rollovers (highest commercial intent in the niche)
| Keyword cluster | Intent | Target page |
|---|---|---|
| gold in 401k, can i buy gold in my 401k, 401k gold investment | Info | /401k-to-gold/ |
| 401k to gold ira rollover, rollover 401k to gold, move 401k to gold | Transactional | /401k-to-gold-ira-rollover/ |
| gold ira rollover, gold ira rollover guide, gold ira rollover without penalty | Transactional | /gold-ira-rollover-guide/ |
| 403b to gold, tsp to gold, sep ira gold | Info | silo subpages |
| convert ira to gold, transfer ira to gold | Transactional | /gold-ira-rollover-guide/ |

### Silo D — How to buy physical gold
| Keyword cluster | Intent | Target page |
|---|---|---|
| how to buy gold, how to invest in gold, buying gold for beginners | Info | /how-to-buy-gold/ |
| how to buy gold bars, where to buy gold bars | Info/Comm | /buy-gold-bars/ |
| how to buy gold coins, best gold coins to buy | Info/Comm | /buy-gold-coins/ |
| how to store gold, gold storage options, gold depository | Info | /how-to-store-physical-gold/ |
| physical gold vs etf, gold etf vs physical | Info | /gold-ira-vs-physical-gold/ |

### Silo E — Local (programmatic)
| Pattern | Intent | Target page |
|---|---|---|
| invest in gold in [state], buy gold in [state], [state] gold ira | Info/Local | /invest-in-gold/[state]/ |
| gold dealers in [city], where to buy gold in [city] | Local | optional city subpages (only with real local data) |
| [state] sales tax on gold / bullion | Info/Local | section within state page |

### Long-tail question keywords (great for FAQ blocks & featured snippets)
- is gold a good investment for retirement
- how much gold should i have in my ira
- can i take physical possession of gold in my ira
- what is the minimum to open a gold ira
- are gold iras safe / are gold iras a scam
- how is a gold ira taxed / gold ira tax rules
- best time to buy gold
- gold ira vs roth ira

---

## 3. The programmatic local pages — rules to stay safe

**Why most "[city] gold" page farms get penalised:** they're templated text
with a name swapped in and nothing locally true. Google calls this a doorway.

**How this project avoids it** (already built into `generate_state_pages.py`):
- Each state record holds **real, verifiable data**: capital, major metros,
  region, population standing.
- Each page has a **hand-written `local_angle`** (1–2 unique paragraphs) and
  a **`local_tax_note`** specific to that state's bullion sales-tax treatment.
- The generator **refuses to publish** a page whose `local_angle` is still a
  placeholder (the `[FILL...]` guardrail).

**Your rules of thumb before publishing the full 50:**
1. Every state page needs ≥150 words of genuinely unique, locally-true text.
2. **Verify the sales-tax note per state** — bullion tax treatment varies and
   changes; cite the state revenue authority. Never guess this.
3. Don't build city pages unless you have real city-level data (local dealers,
   local depositories). States first; cities only where you can differentiate.
4. Add states in **batches**, not all at once, and make sure each is indexed
   and useful before scaling. A slow ramp of quality pages reads as natural.

---

## 4. Compliance checklist (FTC + Google)

- [ ] Visible **affiliate disclosure** near any monetised link and a dedicated
      disclosure page. (FTC requires clear, conspicuous disclosure.)
- [ ] Affiliate links marked `rel="nofollow sponsored"` (done in the homepage).
- [ ] **No fabricated reviews or star ratings.** Only publish ratings you can
      substantiate; the homepage ships them as editable placeholders for this
      reason.
- [ ] Every YMYL page: named author + bio, last-updated date, cited sources.
- [ ] A standing **"not financial/tax advice"** disclaimer (in both footers).
- [ ] Don't make specific return promises or "guaranteed" language — that's
      both an SEO trust killer and a regulatory risk in this niche.

---

## 5. Suggested build order

1. **Homepage + 4 cornerstone pages** (`/gold-ira/`, `/how-to-buy-gold/`,
   `/401k-to-gold-ira-rollover/`, `/gold-ira-rules-2026/`). Depth first.
2. **About / Methodology / Disclosure** pages — these unlock trust for the rest.
3. **Best-companies comparison page** once you've actually vetted firms.
4. **Per-company review pages** (one per real company).
5. **State pages in batches of ~10**, each with verified local data.
6. City pages **only** where you can add real local value.

---

## 6. Technical SEO quick wins

- Clean URL structure (already reflected above — short, keyword-bearing slugs).
- One `<h1>` per page; logical `<h2>`/`<h3>` nesting (templates follow this).
- `FAQPage` and `Article` **schema.org JSON-LD** on guide pages (the FAQ blocks
  are snippet-ready — add the markup).
- `canonical` tags on every page (state template already includes one).
- Internal linking: every supporting page links up to its pillar and across to
  the money page; pillars link down. The templates seed this.
- Fast, mobile-first (both templates are responsive and lightweight).
- XML sitemap + submit in Search Console; monitor coverage as you scale.

---

*Figures used across the site (2026 IRA limit $7,500, +$1,100 catch-up, .995
fineness, Gold Eagle 91.67% exception) are current per the IRS (IR-2025-111)
and IRC §408(m)(3) as of this build. Re-verify each tax year — these are the
exact numbers visitors and Google will fact-check you on.*
