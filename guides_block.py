CT = '<table class="ctable">'  # shorthand

GUIDE_ORDER = ["best-gold-ira-companies","gold-ira-rollover","401k-to-gold-ira-rollover",
 "what-is-a-gold-ira","gold-ira-rules","gold-ira-fees","gold-ira-vs-physical-gold","how-to-buy-gold",
 "gold-ira-pros-and-cons","self-directed-gold-ira","home-storage-gold-ira","precious-metals-ira",
 "silver-ira","gold-ira-tax-rules","ira-approved-gold-coins","gold-ira-custodian",
 "gold-ira-withdrawal-rules","roth-gold-ira","tsp-to-gold-ira","is-gold-a-good-investment"]

def S(h2, anchor, *paras): return (h2, anchor, list(paras))

GUIDES = {
"best-gold-ira-companies": dict(navlabel="Best Gold IRA Companies",
 title="Best Gold IRA Companies of 2026 (Ranked & Reviewed) - Gold Advisor",
 h1="Best Gold IRA Companies of 2026",
 meta="The best gold IRA companies of 2026 ranked on fees, minimums, storage, and reputation — Augusta, Goldco, Priority Gold, American Hartford Gold, and Birch Gold Group.",
 answer="The best gold IRA companies in 2026 combine transparent pricing, reasonable minimums, IRS-approved storage, and strong third-party reputations. Our top five are Augusta Precious Metals, Goldco, Priority Gold, American Hartford Gold, and Birch Gold Group.",
 intro="Choosing a gold IRA company is the single most important decision in the process, because the provider sets your pricing, guides your rollover, and connects you to the custodian and depository. The right choice depends on your budget, how much guidance you want, and which metals you care about. Below is how we evaluate companies, our current shortlist, and what to watch for.",
 sections=[
  S("How we rank gold IRA companies","criteria","We weigh six factors: pricing transparency, account minimums, metals selection, storage arrangements, third-party reputation (BBB, Trustpilot, Business Consumer Alliance), and the quality of the buyback program. Because nearly every dealer prices metals on a quote basis, transparency and a clean complaint record matter more than any single advertised number.","No company pays for a higher position in our ranking; affiliate compensation keeps the site free but does not change the editorial order."),
  S("Our 2026 shortlist","shortlist","Augusta Precious Metals leads for education and transparency, though its $50,000 minimum targets larger investors. Goldco is the rollover specialist with a flat-fee structure. Priority Gold and American Hartford Gold both offer low entry minimums that suit first-time buyers. Birch Gold Group stands out for offering all four metals — gold, silver, platinum, and palladium."),
  S("What to watch out for","watch","Be cautious of high markups on numismatic or rare coins, aggressive upsells away from standard bullion, and any pitch promoting home storage of IRA metal, which the IRS does not permit. Always request a written quote that shows the premium over spot, and confirm fees in writing before funding."),
  S("Questions to ask before you sign","questions","Ask for the total first-year cost (setup, custodian, storage, and metal premium), which custodian and depository they use, whether storage is segregated or commingled, and exactly how the buyback works. A reputable company answers all of these clearly and in writing."),
 ],
 feature=CT+"<thead><tr><th>Company</th><th>Minimum</th><th>Metals</th><th>BBB</th><th>Best for</th></tr></thead><tbody>"
 "<tr><td>Augusta Precious Metals</td><td>$50,000</td><td>Gold, silver</td><td>A+</td><td>Education / high-net-worth</td></tr>"
 "<tr><td>Goldco</td><td>~$25,000</td><td>Gold, silver</td><td>A+</td><td>401(k)/IRA rollovers</td></tr>"
 "<tr><td>Priority Gold</td><td>~$10,000</td><td>Gold, silver</td><td>A+</td><td>Low minimum</td></tr>"
 "<tr><td>American Hartford Gold</td><td>$10,000</td><td>Gold, silver</td><td>A+</td><td>First-time buyers</td></tr>"
 "<tr><td>Birch Gold Group</td><td>$10,000</td><td>Gold, silver, platinum, palladium</td><td>A+</td><td>Metals variety</td></tr>"
 "</tbody></table>",
 faqs=[("Which gold IRA company is best overall?","We rank Augusta Precious Metals first for transparency and education, but the best choice depends on your minimum budget and goals."),
  ("Which gold IRA company has the lowest minimum?","Priority Gold, American Hartford Gold, and Birch Gold Group are typically the most accessible, with minimums around $10,000."),
  ("Are gold IRA companies legitimate?","The established ones are. Look for an A+ BBB rating, years in business, IRS-approved custodians and depositories, and transparent written pricing.")],
 related=["gold-ira-fees","gold-ira-rollover","what-is-a-gold-ira"]),

"gold-ira-rollover": dict(navlabel="Gold IRA Rollover",
 title="Gold IRA Rollover Guide 2026: Rules, Steps & Tax Rules - Gold Advisor",
 h1="Gold IRA Rollover: How It Works in 2026",
 meta="A gold IRA rollover moves retirement funds into a self-directed IRA holding physical gold. Learn direct vs indirect rollovers, eligible accounts, the 60-day rule, and steps.",
 answer="A gold IRA rollover moves funds from an existing retirement account into a self-directed IRA that holds physical gold. Done as a direct, custodian-to-custodian transfer, it is generally tax-free and penalty-free.",
 intro="A rollover is how most people fund a gold IRA — by moving money that is already in a 401(k) or IRA rather than contributing new cash. The mechanics matter: a direct transfer is clean and tax-free, while an indirect rollover introduces deadlines and withholding that can trigger taxes if mishandled.",
 sections=[
  S("Direct vs indirect rollovers","types","In a direct (trustee-to-trustee) transfer, funds move straight between custodians and you never take possession — the simplest, safest route. In an indirect rollover, the money is paid to you first and you have 60 days to redeposit it; miss the window and it becomes a taxable distribution, plus a possible 10% penalty if you are under 59 and a half.","Indirect IRA-to-IRA rollovers are also limited to one per 12-month period, another reason most investors choose a direct transfer."),
  S("Which accounts can be rolled over","eligible","Eligible sources generally include Traditional, Roth, SEP, and SIMPLE IRAs, plus employer plans such as 401(k), 403(b), 457(b), and the federal TSP. Roth funds should roll into a Roth gold IRA to preserve their tax treatment."),
  S("Step by step","steps","First, open a self-directed IRA with a custodian that handles metals. Second, request a direct transfer from your current plan. Third, choose IRS-eligible metals through your gold IRA company. Fourth, the custodian settles payment and the metal ships to an IRS-approved depository in your name."),
  S("Common mistakes to avoid","mistakes","The biggest errors are taking an indirect rollover and missing the 60-day deadline, rolling pre-tax funds into a Roth and creating a surprise tax bill, and buying overpriced coins. A direct transfer plus standard bullion avoids nearly all of these."),
 ],
 feature=CT+"<thead><tr><th></th><th>Direct rollover</th><th>Indirect rollover</th></tr></thead><tbody>"
 "<tr><td>Who holds funds</td><td>Custodian to custodian</td><td>Paid to you first</td></tr>"
 "<tr><td>Deadline</td><td>None</td><td>60 days to redeposit</td></tr>"
 "<tr><td>Withholding</td><td>None</td><td>Up to 20% on plan distributions</td></tr>"
 "<tr><td>Frequency limit</td><td>Unlimited</td><td>One per 12 months (IRA-to-IRA)</td></tr>"
 "<tr><td>Risk</td><td>Low</td><td>Higher (taxes if late)</td></tr></tbody></table>",
 faqs=[("Is a gold IRA rollover taxable?","A direct rollover is generally tax-free and penalty-free. An indirect rollover becomes taxable if you miss the 60-day redeposit window."),
  ("How long does a gold IRA rollover take?","Most direct transfers complete in roughly one to three weeks, depending on how quickly your current custodian releases funds."),
  ("Can I do a gold IRA rollover without penalty?","Yes — a direct trustee-to-trustee transfer avoids both taxes and the early-withdrawal penalty.")],
 related=["401k-to-gold-ira-rollover","gold-ira-rules","gold-ira-custodian"]),

"401k-to-gold-ira-rollover": dict(navlabel="401(k) to Gold IRA",
 title="401(k) to Gold IRA Rollover 2026: How to Convert Without Penalty - Gold Advisor",
 h1="401(k) to Gold IRA Rollover",
 meta="How to roll over a 401(k) into a gold IRA in 2026 without taxes or penalties — eligibility for current vs former employers, the direct-transfer steps, and pitfalls.",
 answer="You can roll a 401(k) into a gold IRA by opening a self-directed IRA and requesting a direct transfer. Done custodian-to-custodian, it is tax-free and penalty-free; eligibility depends on whether you still work for the employer.",
 intro="Rolling a 401(k) into a gold IRA is one of the most common ways Americans add physical precious metals to retirement savings. The key question is eligibility: funds from a former employer roll over freely, while a current-employer plan may restrict moves until you reach a certain age or qualify for an in-service distribution.",
 sections=[
  S("Former vs current employer","eligibility","If you have left the employer, the full 401(k) balance is generally eligible to roll over at any time. If you still work there, many plans only allow an in-service distribution after age 59 and a half, or for specific contribution types — check your plan's summary description."),
  S("Why investors convert a 401(k)","why","Typical 401(k) menus offer no physical-metal option. A gold IRA lets retirement savers diversify into an asset that has historically held value during inflation and market stress, while keeping the tax-advantaged wrapper intact."),
  S("The direct-rollover steps","steps","Open a self-directed IRA, request a direct rollover from your 401(k) administrator (so funds move custodian-to-custodian and avoid the mandatory 20% withholding), select IRS-eligible metals, and have them shipped to an approved depository in your IRA's name."),
  S("Watch the withholding trap","withholding","If a 401(k) distribution is paid to you rather than transferred directly, the plan typically withholds 20% for taxes, and you must replace that amount from other funds within 60 days to avoid tax on it. A direct rollover sidesteps the problem entirely."),
 ],
 feature="",
 faqs=[("Can I roll my 401(k) into gold without penalty?","Yes, through a direct rollover into a self-directed IRA. The funds never touch your hands, so there is no tax or early-withdrawal penalty."),
  ("Can I roll over a 401(k) while still employed?","Sometimes. Many plans allow in-service rollovers after age 59 and a half; otherwise you usually must separate from the employer first."),
  ("Does a 401(k)-to-gold rollover have an annual limit?","No. Direct rollovers are not capped by the annual contribution limit and can be done as a one-time transfer of existing funds.")],
 related=["gold-ira-rollover","tsp-to-gold-ira","gold-ira-tax-rules"]),

"what-is-a-gold-ira": dict(navlabel="What Is a Gold IRA?",
 title="What Is a Gold IRA? How It Works in 2026 - Gold Advisor",
 h1="What Is a Gold IRA?",
 meta="A gold IRA is a self-directed IRA that holds physical gold and other approved metals. Learn how it works, which metals qualify, storage rules, and who it suits.",
 answer="A gold IRA is a self-directed individual retirement account that holds physical gold (and optionally silver, platinum, or palladium) instead of, or alongside, paper assets. It follows the same contribution and distribution rules as a regular IRA but requires an IRS-approved custodian and depository.",
 intro="A gold IRA gives retirement savers a way to own tangible precious metals inside a tax-advantaged account. It works like a Traditional or Roth IRA for tax purposes, but because it holds a physical asset, it must be self-directed and the metal must be stored at an approved depository rather than at home.",
 sections=[
  S("How a gold IRA works","how","You open a self-directed IRA with a specialized custodian, fund it with a contribution or rollover, buy eligible metal through a dealer, and have it vaulted at an IRS-approved depository. The account grows tax-deferred (or tax-free in a Roth), and you take distributions in retirement either in cash or as the physical metal."),
  S("Which metals qualify","metals","The IRS sets minimum fineness standards: gold must be at least .995 pure (the American Gold Eagle is a statutory exception), silver .999, and platinum and palladium .9995. Collectible and rare coins generally do not qualify."),
  S("Storage and custody","storage","Gold IRA metal cannot be kept at home or in a personal safe-deposit box; doing so is treated as a taxable distribution. A custodian administers the account and an approved depository (such as Delaware Depository or Brink's) provides insured, audited storage."),
  S("Who a gold IRA suits","who","Gold IRAs suit investors who want to diversify a portion of retirement savings into a tangible inflation hedge and are comfortable with fees and the lack of dividend income. Most advisors suggest limiting precious metals to a modest share of a portfolio."),
 ],
 feature="",
 faqs=[("Is a gold IRA a good idea?","It can be for diversification, but gold pays no income and carries storage fees, so most advisors recommend allocating only a portion of a portfolio."),
  ("Can I hold the gold from my IRA at home?","No. IRA metal must be stored at an IRS-approved depository; home storage is treated as a taxable distribution."),
  ("What is the difference from a regular IRA?","The tax rules are the same, but a gold IRA is self-directed and holds physical metal, requiring a specialized custodian and a depository.")],
 related=["gold-ira-rules","gold-ira-fees","precious-metals-ira"]),

"gold-ira-rules": dict(navlabel="Gold IRA Rules (2026)",
 title="Gold IRA Rules 2026: IRS Requirements, Fineness & Storage - Gold Advisor",
 h1="Gold IRA Rules (2026)",
 meta="The 2026 IRS rules for gold IRAs: fineness standards, approved custodians and depositories, the home-storage ban, contribution limits, and prohibited transactions.",
 answer="Gold IRA rules are set federally by the IRS: metals must meet minimum fineness standards, be bought through a self-directed IRA, and be stored at an approved depository — never at home. The 2026 contribution limit is $7,500 (plus a $1,100 catch-up at 50+).",
 intro="Because gold IRAs are governed by federal tax law (notably Internal Revenue Code section 408(m)), the rules are the same in every state. Understanding them protects you from accidentally disqualifying your account, which can trigger taxes and penalties.",
 sections=[
  S("Eligible metals and fineness","fineness","Gold must be at least .995 fine, silver .999, and platinum and palladium .9995. The American Gold Eagle is specifically allowed despite its 91.67% purity. Proof and bullion coins from approved mints qualify; collectibles do not."),
  S("Custodian and depository required","custody","A self-directed IRA must be administered by an IRS-approved custodian, and the metal must be held by an approved depository in the account's name. You cannot take personal possession while the metal is in the IRA."),
  S("The home-storage ban","home","Schemes that promise home storage through an LLC are high-risk; the IRS treats personal possession of IRA metal as a distribution, which can mean income tax plus a 10% penalty if you are under 59 and a half."),
  S("Contributions and distributions","limits","The 2026 limit is $7,500 for those under 50 and $8,600 with the $1,100 catch-up. Required minimum distributions begin at age 73 for Traditional accounts. Prohibited transactions — like buying metal from yourself — can disqualify the whole IRA."),
 ],
 feature='<div class="facts-box">'
  '<div class="factrow"><span class="k">2026 contribution limit (under 50)</span><span class="v">$7,500</span></div>'
  '<div class="factrow"><span class="k">Catch-up (50+)</span><span class="v">+$1,100</span></div>'
  '<div class="factrow"><span class="k">Gold fineness minimum</span><span class="v">.995</span></div>'
  '<div class="factrow"><span class="k">Silver fineness minimum</span><span class="v">.999</span></div>'
  '<div class="factrow"><span class="k">RMD age (Traditional)</span><span class="v">73</span></div></div>',
 faqs=[("What are the IRS rules for a gold IRA?","Metals must meet fineness standards, be purchased through a self-directed IRA, and be stored at an approved depository. Home storage is not allowed."),
  ("What is the minimum purity for gold in an IRA?","Gold must be at least .995 fine, with the American Gold Eagle as a specific statutory exception."),
  ("When do RMDs start for a gold IRA?","Required minimum distributions begin at age 73 for Traditional gold IRAs; Roth IRAs have no lifetime RMDs.")],
 related=["gold-ira-tax-rules","gold-ira-withdrawal-rules","ira-approved-gold-coins"]),

"gold-ira-fees": dict(navlabel="Gold IRA Fees & Costs",
 title="Gold IRA Fees Explained (2026): Setup, Storage & Markups - Gold Advisor",
 h1="Gold IRA Fees & Costs in 2026",
 meta="A breakdown of gold IRA fees in 2026: account setup, annual custodian fees, storage, the metal markup over spot, and how to keep total costs low.",
 answer="Gold IRA fees typically include a one-time setup charge (around $50), an annual custodian fee (about $80 to $125), annual storage (roughly $100 to $150), and a markup over the spot price on the metal itself. Flat-fee providers are usually cheaper for larger accounts.",
 intro="Fees are the most overlooked part of a gold IRA, and they vary widely. Knowing the categories — and which ones are flat versus scaled — lets you compare providers accurately and avoid overpaying, especially on the metal premium, which is the largest cost most investors never see itemized.",
 sections=[
  S("The five fee categories","categories","Expect a one-time account setup fee, an annual custodian/administration fee, an annual storage and insurance fee, the dealer markup (premium over spot) on each purchase, and occasional wire or transaction fees. The first three are usually disclosed; the markup often is not."),
  S("Flat vs scaled fees","flat","Most reputable custodians charge flat annual fees, which favor larger accounts. Avoid providers that scale fees as a percentage of account value, since costs balloon as your balance grows."),
  S("The hidden cost: the spread","spread","The premium over spot price on coins and bars is where dealers make most of their margin. Standard bullion carries low premiums; numismatic or proof coins can carry much higher ones, so request a written quote showing the premium before buying."),
  S("How to minimize fees","minimize","Choose flat-fee custodians, buy common bullion rather than rare coins, look for first-year or multi-year fee waivers on qualifying accounts, and consolidate purchases to reduce per-transaction costs."),
 ],
 feature=CT+"<thead><tr><th>Fee</th><th>Typical range</th><th>Frequency</th></tr></thead><tbody>"
 "<tr><td>Account setup</td><td>$50</td><td>One-time</td></tr>"
 "<tr><td>Custodian / admin</td><td>$80 to $125</td><td>Annual</td></tr>"
 "<tr><td>Storage and insurance</td><td>$100 to $150</td><td>Annual</td></tr>"
 "<tr><td>Metal markup (spread)</td><td>Varies (low for bullion)</td><td>Per purchase</td></tr>"
 "<tr><td>Wire / transaction</td><td>$25 to $30</td><td>As incurred</td></tr></tbody></table>",
 faqs=[("How much does a gold IRA cost per year?","Most investors pay roughly $200 to $300 per year in flat custodian and storage fees, plus the one-time markup on metal purchases."),
  ("Are gold IRA fees worth it?","They can be if precious metals fit your diversification goals, but the fees mean gold IRAs make less sense for very small balances."),
  ("Can gold IRA fees be waived?","Several companies waive the first year — or up to three years — of fees on qualifying account sizes.")],
 related=["best-gold-ira-companies","gold-ira-custodian","what-is-a-gold-ira"]),

"gold-ira-vs-physical-gold": dict(navlabel="Gold IRA vs Physical Gold",
 title="Gold IRA vs Physical Gold: Which Is Better in 2026? - Gold Advisor",
 h1="Gold IRA vs Physical Gold",
 meta="Gold IRA vs buying physical gold: compare tax treatment, storage, liquidity, control, and costs to decide which approach fits your goals in 2026.",
 answer="A gold IRA offers tax advantages and required professional storage but less direct control; buying physical gold outright gives you immediate possession and flexibility but no tax shelter and higher long-term capital-gains treatment as a collectible.",
 intro="Both approaches put gold in your portfolio, but they differ on taxes, storage, and control. The right choice depends on whether your priority is retirement tax efficiency or hands-on ownership you can hold today.",
 sections=[
  S("Tax treatment","tax","Inside an IRA, gains grow tax-deferred (or tax-free in a Roth). Physical gold held personally is taxed as a collectible, with long-term gains taxed at a rate up to 28% — higher than the standard long-term capital-gains rate."),
  S("Storage and control","storage","IRA metal must sit at an approved depository, so you cannot hold it. Personally owned gold can be kept wherever you choose, giving immediate access but also the responsibility and cost of secure storage and insurance."),
  S("Liquidity and costs","liquidity","Personal gold can be sold to any dealer at will. IRA metal is sold through your custodian and a distribution may have tax consequences. IRAs add custodian and storage fees that personal ownership avoids, though personal storage has its own costs."),
  S("Which to choose","choose","If the goal is tax-advantaged retirement diversification, a gold IRA usually wins. If you want crisis-ready metal in hand or are investing outside retirement, buying physical gold directly is simpler."),
 ],
 feature=CT+"<thead><tr><th></th><th>Gold IRA</th><th>Physical gold</th></tr></thead><tbody>"
 "<tr><td>Tax treatment</td><td>Tax-deferred / tax-free (Roth)</td><td>Collectible (up to 28%)</td></tr>"
 "<tr><td>Storage</td><td>Approved depository (required)</td><td>Your choice</td></tr>"
 "<tr><td>Possession</td><td>Not until distribution</td><td>Immediate</td></tr>"
 "<tr><td>Ongoing fees</td><td>Custodian + storage</td><td>Self-storage / insurance</td></tr></tbody></table>",
 faqs=[("Is a gold IRA better than buying physical gold?","For retirement tax efficiency, usually yes. For immediate possession and flexibility, owning physical gold directly is better."),
  ("Can I convert physical gold I own into a gold IRA?","Generally no — you cannot contribute metal you already own; the IRA must purchase eligible metal through the account."),
  ("How is personally held gold taxed?","Physical gold is a collectible, with long-term gains taxed at a rate up to 28%, versus tax-advantaged growth inside an IRA.")],
 related=["what-is-a-gold-ira","how-to-buy-gold","gold-ira-tax-rules"]),

"how-to-buy-gold": dict(navlabel="How to Buy Gold",
 title="How to Buy Gold in 2026: Coins, Bars, IRAs & ETFs - Gold Advisor",
 h1="How to Buy Gold in 2026",
 meta="A practical guide to buying gold in 2026 — physical coins and bars, gold IRAs, and ETFs — plus where to buy, what to pay, and how to store it safely.",
 answer="You can buy gold as physical coins and bars from a reputable dealer, inside a tax-advantaged gold IRA, or as paper exposure through ETFs. For most retirement savers, physical bullion or a gold IRA offers the truest ownership.",
 intro="Buying gold is straightforward once you decide what kind of exposure you want. Physical metal gives you a tangible asset; an IRA wraps it in tax advantages; ETFs offer convenience without possession. Each has trade-offs in cost, control, and tax treatment.",
 sections=[
  S("Physical coins and bars","physical","Common bullion coins — American Gold Eagles and Buffalos, Canadian Maple Leafs — and bars from accredited refiners carry the lowest premiums over spot. Buy from established dealers, compare the premium, and avoid high-markup numismatic coins unless you are a collector."),
  S("Gold inside an IRA","ira","A gold IRA lets you hold IRS-eligible metal in a tax-advantaged retirement account, with storage at an approved depository. This is the route for retirement-focused buyers who want tax benefits rather than metal in hand."),
  S("ETFs and paper gold","etf","Gold ETFs track the price without you owning metal — convenient and liquid, but you hold a security, not bullion, and there is no physical claim you can take home. They suit traders more than long-term physical-ownership goals."),
  S("Storing what you buy","store","Personally owned gold should be insured and stored securely, whether at home in a quality safe or in a private vault. IRA metal is stored for you at an approved, insured depository."),
 ],
 feature="",
 faqs=[("What is the cheapest way to buy gold?","Common bullion coins and bars carry the lowest premiums over spot; avoid high-markup numismatic or proof coins for pure investment."),
  ("Is it better to buy gold coins or bars?","Bars usually carry lower premiums per ounce; coins are more recognizable and easier to sell in small amounts. Both work for investment."),
  ("Can I buy gold for my IRA?","Yes — through a self-directed gold IRA, which buys IRS-eligible metal and stores it at an approved depository.")],
 related=["gold-ira-vs-physical-gold","ira-approved-gold-coins","is-gold-a-good-investment"]),

"gold-ira-pros-and-cons": dict(navlabel="Gold IRA Pros & Cons",
 title="Gold IRA Pros and Cons (2026): Is It Worth It? - Gold Advisor",
 h1="Gold IRA Pros and Cons",
 meta="The real pros and cons of a gold IRA in 2026 — diversification and inflation hedging versus fees, no income, and storage rules — so you can decide if it is worth it.",
 answer="A gold IRA's main advantages are portfolio diversification, an inflation and crisis hedge, and tax-advantaged growth. Its drawbacks are fees, no dividends or interest, required depository storage, and price volatility.",
 intro="A gold IRA is neither a miracle nor a mistake — it is a tool with clear trade-offs. Weighing them honestly against your goals and time horizon is the best way to decide whether precious metals deserve a place in your retirement plan.",
 sections=[
  S("The case for a gold IRA","pros","Gold often moves independently of stocks and bonds, which can smooth a portfolio during downturns. It has historically preserved purchasing power against inflation and currency weakness, and inside an IRA those gains are tax-advantaged."),
  S("The case against","cons","Gold produces no income — no dividends or interest — so it can lag a diversified stock portfolio over long bull markets. Gold IRAs also carry custodian and storage fees, require an approved depository, and the metal price can be volatile in the short term."),
  S("Who benefits most","who","Investors nearing or in retirement who want to hedge sequence-of-returns and inflation risk, and those who already hold mostly paper assets, tend to benefit most from a modest precious-metals allocation."),
  S("How much to allocate","allocate","Many advisors suggest limiting precious metals to roughly 5% to 10% of a portfolio — enough to diversify without sacrificing the long-term growth that income-producing assets provide."),
 ],
 feature='<div class="proscons"><div class="pc pros"><h4>Pros</h4><ul>'
  "<li>Diversification away from stocks and bonds</li><li>Historical inflation and crisis hedge</li>"
  "<li>Tax-advantaged growth inside an IRA</li><li>Tangible, finite asset</li></ul></div>"
  '<div class="pc cons"><h4>Cons</h4><ul>'
  "<li>No dividends or interest</li><li>Custodian and storage fees</li>"
  "<li>Cannot store metal at home</li><li>Short-term price volatility</li></ul></div></div>",
 faqs=[("Is a gold IRA worth it?","It can be worthwhile for diversification and inflation protection, but the lack of income and the fees mean it works best as part of a portfolio, not all of it."),
  ("What is the downside of a gold IRA?","Gold earns no income, carries storage and custodian fees, and cannot be stored at home, so it suits hedging rather than growth."),
  ("How much of my retirement should be in gold?","A common guideline is 5% to 10%, though the right figure depends on your goals and risk tolerance.")],
 related=["is-gold-a-good-investment","gold-ira-fees","what-is-a-gold-ira"]),

"self-directed-gold-ira": dict(navlabel="Self-Directed Gold IRA",
 title="Self-Directed Gold IRA (2026): How It Works - Gold Advisor",
 h1="Self-Directed Gold IRA",
 meta="A self-directed gold IRA lets you hold physical metals and alternative assets. Learn the custodian's role, what is allowed, and your responsibilities in 2026.",
 answer="A self-directed IRA (SDIRA) is an IRA that can hold alternative assets such as physical gold. A specialized custodian administers it, but you direct the investments — which is what makes holding physical precious metals possible.",
 intro="Ordinary IRAs at brokerages only hold stocks, bonds, and funds. To own physical gold in a retirement account you need a self-directed IRA, where a custodian that allows alternative assets administers the account while you choose what it buys.",
 sections=[
  S("What makes an IRA self-directed","what","The label refers to the breadth of allowed assets, not a different tax status. An SDIRA follows the same contribution and distribution rules as any IRA but can hold metals, real estate, and other alternatives that mainstream brokerages do not offer."),
  S("The custodian's role","custodian","A self-directed custodian holds the account, processes transactions, files IRS paperwork, and arranges depository storage for metals. The custodian does not give investment advice — you (or your gold IRA company) direct the purchases."),
  S("Your responsibilities","responsibilities","Because you direct the account, you must keep transactions at arm's length and avoid prohibited transactions, such as buying metal from yourself or storing IRA metal personally. Violations can disqualify the entire IRA."),
  S("Setting one up","setup","Choose a reputable self-directed custodian (or let your gold IRA company recommend one), fund it by contribution or rollover, and purchase eligible metal that ships to an approved depository in the account's name."),
 ],
 feature="",
 faqs=[("What is a self-directed gold IRA?","An IRA with a custodian that permits alternative assets like physical gold, letting you hold metals in a tax-advantaged retirement account."),
  ("Do I manage a self-directed IRA myself?","You direct the investment choices, but a custodian administers the account and a depository stores any metal."),
  ("What can a self-directed IRA hold?","Beyond stocks and funds, it can hold IRS-eligible precious metals and other alternatives, subject to prohibited-transaction rules.")],
 related=["gold-ira-custodian","what-is-a-gold-ira","gold-ira-rules"]),

"home-storage-gold-ira": dict(navlabel="Home Storage Gold IRA",
 title="Home Storage Gold IRA: Is It Legal in 2026? - Gold Advisor",
 h1="Home Storage Gold IRA: The Truth",
 meta="Home storage gold IRAs are heavily marketed but risky. Learn why the IRS does not allow storing IRA metal at home, the LLC loophole risks, and the legal alternative.",
 answer="A true home storage gold IRA is not permitted: the IRS requires IRA metal to be held by an approved depository. Storing it at home is treated as a taxable distribution, with possible penalties, even when arranged through an LLC.",
 intro="Home storage gold IRAs are aggressively advertised, but the concept is largely a myth that can cost you dearly. Understanding why matters, because the penalties for getting it wrong can include taxes on the whole account and a possible early-withdrawal penalty.",
 sections=[
  S("Why home storage is not allowed","why","IRS rules require a qualified trustee or custodian to hold IRA assets, and for metals that means an approved depository. Taking personal possession of IRA metal is treated as a distribution of those assets, triggering tax and possibly a 10% penalty before age 59 and a half."),
  S("The 'checkbook LLC' loophole","llc","Some promoters suggest forming an LLC owned by your IRA to store metal at home. The IRS and courts have scrutinized these structures, and a notable tax-court case found that personally holding IRA metal through such an arrangement was a taxable distribution. The risk is substantial."),
  S("What is actually allowed","allowed","The compliant approach is simple: a self-directed IRA with an approved custodian and metal stored at an IRS-approved, insured depository in the account's name. You can choose segregated or commingled storage."),
  S("Storing gold at home (outside an IRA)","personal","If you want metal physically in your possession, buy gold personally rather than through an IRA. You give up the tax shelter, but you can store it however you like — and you avoid the home-storage trap entirely."),
 ],
 feature="",
 faqs=[("Is a home storage gold IRA legal?","No. IRA metal must be held by an approved depository. Storing it at home is treated by the IRS as a taxable distribution."),
  ("What happens if I store my IRA gold at home?","It can be deemed a distribution, making the value taxable and adding a 10% penalty if you are under 59 and a half."),
  ("How can I legally hold gold at home?","Buy it personally rather than in an IRA. Personal bullion can be stored anywhere, but it does not receive IRA tax advantages.")],
 related=["gold-ira-rules","self-directed-gold-ira","gold-ira-custodian"]),

"precious-metals-ira": dict(navlabel="Precious Metals IRA",
 title="Precious Metals IRA 2026: Gold, Silver, Platinum & Palladium - Gold Advisor",
 h1="Precious Metals IRA",
 meta="A precious metals IRA can hold gold, silver, platinum, and palladium. Learn the fineness standards for each metal, how it works, and how it differs from a gold IRA.",
 answer="A precious metals IRA is a self-directed IRA that can hold IRS-eligible gold, silver, platinum, and palladium. It works like a gold IRA but offers a broader metals lineup, each with its own minimum fineness standard.",
 intro="A precious metals IRA is essentially a gold IRA with more options. The structure, tax treatment, and storage rules are identical — the difference is that you can diversify across four metals rather than one, which appeals to investors who want broader exposure.",
 sections=[
  S("The four eligible metals","metals","Gold, silver, platinum, and palladium can all be held, provided they meet IRS fineness standards: gold .995, silver .999, and platinum and palladium .9995. Each metal has its own approved coins and bars."),
  S("Why diversify across metals","why","Silver tends to be more volatile and industrial-demand-driven than gold, while platinum and palladium are tied heavily to industrial use. Holding a mix can spread risk, though gold remains the core holding for most precious-metals investors."),
  S("How it works","how","Like any self-directed IRA, you fund it by contribution or rollover, buy eligible metal through a dealer, and store it at an approved depository. Not every company offers all four metals — Birch Gold Group is one that does."),
  S("Precious metals IRA vs gold IRA","vs","The terms are often used interchangeably. A gold IRA simply emphasizes gold; a precious metals IRA highlights the option to add silver, platinum, and palladium. The rules and custody requirements are the same."),
 ],
 feature=CT+"<thead><tr><th>Metal</th><th>Minimum fineness</th></tr></thead><tbody>"
 "<tr><td>Gold</td><td>.995 (Gold Eagle exempt)</td></tr><tr><td>Silver</td><td>.999</td></tr>"
 "<tr><td>Platinum</td><td>.9995</td></tr><tr><td>Palladium</td><td>.9995</td></tr></tbody></table>",
 faqs=[("What metals can a precious metals IRA hold?","IRS-eligible gold, silver, platinum, and palladium that meet the minimum fineness standards for each metal."),
  ("Is a precious metals IRA the same as a gold IRA?","Effectively yes — the rules are identical; a precious metals IRA just emphasizes the option to add silver, platinum, and palladium."),
  ("Which companies offer all four metals?","Birch Gold Group is a well-known provider that offers gold, silver, platinum, and palladium for IRAs.")],
 related=["silver-ira","what-is-a-gold-ira","ira-approved-gold-coins"]),

"silver-ira": dict(navlabel="Silver IRA",
 title="Silver IRA 2026: Rules, Eligible Coins & How It Works - Gold Advisor",
 h1="Silver IRA",
 meta="A silver IRA holds IRS-eligible physical silver in a tax-advantaged account. Learn the .999 fineness rule, eligible coins, why investors choose silver, and the trade-offs.",
 answer="A silver IRA is a self-directed IRA that holds physical silver meeting the IRS .999 fineness standard. It works exactly like a gold IRA, with the same custodian and depository requirements.",
 intro="Silver appeals to investors who want precious-metals exposure at a lower price per ounce and with more upside potential — though also more volatility. A silver IRA follows the same federal rules as a gold IRA but holds silver bullion that meets the .999 purity standard.",
 sections=[
  S("How a silver IRA works","how","You open a self-directed IRA, fund it, buy eligible silver through a dealer, and store it at an approved depository. The account's tax treatment matches a Traditional or Roth IRA depending on how you set it up."),
  S("Eligible silver","eligible","Silver must be at least .999 fine. Common eligible products include American Silver Eagles, Canadian Silver Maple Leafs, and bars from accredited refiners. Collectible or numismatic silver generally does not qualify."),
  S("Why investors choose silver","why","Silver is cheaper per ounce than gold, so it is accessible to smaller budgets, and it has both monetary and industrial demand. The trade-off is higher volatility — silver tends to swing more sharply than gold in both directions."),
  S("Silver vs gold in an IRA","vs","Gold is the steadier store of value; silver offers more potential upside and more risk. Many investors hold both, weighting gold as the core and silver as a satellite position."),
 ],
 feature="",
 faqs=[("What silver is eligible for an IRA?","Silver of at least .999 fineness, such as American Silver Eagles, Canadian Maple Leafs, and accredited-refiner bars."),
  ("Is a silver IRA a good investment?","Silver offers more upside and more volatility than gold; it suits investors comfortable with bigger price swings as part of a diversified plan."),
  ("Can I hold both gold and silver in one IRA?","Yes. A precious metals IRA can hold gold, silver, platinum, and palladium together.")],
 related=["precious-metals-ira","ira-approved-gold-coins","what-is-a-gold-ira"]),

"gold-ira-tax-rules": dict(navlabel="Gold IRA Tax Rules",
 title="Gold IRA Tax Rules 2026: Contributions, Growth & Distributions - Gold Advisor",
 h1="Gold IRA Tax Rules (2026)",
 meta="How gold IRAs are taxed in 2026: contribution deductibility, tax-deferred growth, distributions as ordinary income, Roth tax-free withdrawals, and the collectibles rule.",
 answer="A gold IRA is taxed like any IRA: Traditional contributions may be deductible and grow tax-deferred, with distributions taxed as ordinary income; Roth contributions are after-tax and qualified withdrawals are tax-free. The 28% collectibles rate does not apply to metal held inside an IRA.",
 intro="The tax advantages are the main reason to hold gold in an IRA rather than personally. Understanding how contributions, growth, and withdrawals are treated — and how that differs from owning bullion directly — helps you plan efficiently.",
 sections=[
  S("Contributions and growth","contrib","In a Traditional gold IRA, contributions may be tax-deductible and the account grows tax-deferred. In a Roth gold IRA, you contribute after-tax dollars and growth is tax-free. The 2026 limit is $7,500, or $8,600 with the 50-plus catch-up."),
  S("How distributions are taxed","dist","Traditional gold IRA distributions are taxed as ordinary income in the year you take them. Roth qualified distributions are tax-free. You can take distributions in cash or as the physical metal (an in-kind distribution)."),
  S("The collectibles rule","collectibles","Physical gold held personally is taxed as a collectible, with long-term gains up to 28%. A key benefit of the IRA is that metal held inside it escapes that treatment — growth is sheltered until distribution."),
  S("Early withdrawals and penalties","penalty","Taking a distribution before age 59 and a half generally adds a 10% penalty on top of any income tax, with limited exceptions. Required minimum distributions begin at 73 for Traditional accounts."),
 ],
 feature="",
 faqs=[("How is a gold IRA taxed?","Like a regular IRA: Traditional distributions are ordinary income; Roth qualified withdrawals are tax-free. Growth is sheltered while inside the account."),
  ("Does the 28% collectibles tax apply to a gold IRA?","No. That rate applies to physical gold held personally; metal inside an IRA is taxed under IRA rules instead."),
  ("Are gold IRA contributions tax-deductible?","Traditional IRA contributions may be deductible depending on income and coverage; Roth contributions are not deductible but grow tax-free.")],
 related=["gold-ira-withdrawal-rules","roth-gold-ira","gold-ira-rules"]),

"ira-approved-gold-coins": dict(navlabel="IRA-Approved Gold Coins",
 title="IRA-Approved Gold Coins & Bars (2026 List) - Gold Advisor",
 h1="IRA-Approved Gold Coins & Bars",
 meta="Which gold coins and bars are IRA-eligible in 2026: American Gold Eagle, Gold Buffalo, Canadian Maple Leaf, and .995 bars — plus what does not qualify.",
 answer="IRA-approved gold must be at least .995 fine, with the American Gold Eagle as a statutory exception. Eligible products include the Gold Eagle, Gold Buffalo, Canadian Maple Leaf, Austrian Philharmonic, and bars from accredited refiners. Collectible and rare coins do not qualify.",
 intro="Not every gold coin can go into an IRA. The IRS sets a fineness floor and approves specific products; buying ineligible metal can disqualify your account. Here is what qualifies and what to avoid.",
 sections=[
  S("The fineness standard","fineness","Gold for an IRA must be at least .995 (99.5%) pure. The American Gold Eagle is specifically permitted by statute even though it is 91.67% pure, because of how it was authorized by Congress."),
  S("Eligible coins and bars","eligible","Widely accepted products include the American Gold Eagle and Gold Buffalo, the Canadian Gold Maple Leaf, the Austrian Gold Philharmonic, and gold bars and rounds produced by accredited refiners (such as those approved by COMEX, NYMEX, or the LBMA)."),
  S("What does not qualify","not","Rare, collectible, and most foreign or pre-1933 coins are excluded, as are jewelry and novelty items. If a dealer pushes high-premium 'numismatic' coins for an IRA, treat it as a warning sign."),
  S("Buying for your IRA","buy","Purchases must be made through your self-directed IRA and shipped to an approved depository — you cannot buy the metal personally and then contribute it. Stick to standard, low-premium bullion for the best value."),
 ],
 feature=CT+"<thead><tr><th>Product</th><th>IRA-eligible?</th></tr></thead><tbody>"
 "<tr><td>American Gold Eagle</td><td>Yes (statutory exception)</td></tr>"
 "<tr><td>American Gold Buffalo (.9999)</td><td>Yes</td></tr>"
 "<tr><td>Canadian Gold Maple Leaf (.9999)</td><td>Yes</td></tr>"
 "<tr><td>Austrian Gold Philharmonic (.9999)</td><td>Yes</td></tr>"
 "<tr><td>Accredited-refiner bars (.995+)</td><td>Yes</td></tr>"
 "<tr><td>Rare / numismatic coins</td><td>No</td></tr></tbody></table>",
 faqs=[("What gold coins are IRA-approved?","The American Gold Eagle and Buffalo, Canadian Maple Leaf, Austrian Philharmonic, and .995+ bars from accredited refiners."),
  ("Why is the American Gold Eagle allowed if it is not .995 pure?","Congress specifically authorized it for IRAs as a statutory exception to the fineness rule."),
  ("Are rare or collectible coins allowed in a gold IRA?","No. Collectibles and numismatic coins are excluded; IRAs require investment-grade bullion.")],
 related=["gold-ira-rules","precious-metals-ira","how-to-buy-gold"]),

"gold-ira-custodian": dict(navlabel="Gold IRA Custodians",
 title="Gold IRA Custodians 2026: What They Do & How to Choose - Gold Advisor",
 h1="Gold IRA Custodians",
 meta="What a gold IRA custodian does, how it differs from a depository, examples like Equity Trust and Strata, and how to choose one in 2026.",
 answer="A gold IRA custodian is the IRS-approved institution that holds and administers your self-directed IRA, processes transactions, and arranges depository storage. It is required by law — you cannot hold a gold IRA without one.",
 intro="Every gold IRA needs a custodian. It is a behind-the-scenes role that many investors overlook, yet the custodian handles compliance, paperwork, and storage logistics — so understanding what it does, and how it differs from the dealer and the depository, is worthwhile.",
 sections=[
  S("What a custodian does","does","The custodian opens and administers the IRA, executes your buy and sell instructions, maintains records, files required IRS reports, and coordinates storage with an approved depository. It is the legal holder of the account's assets."),
  S("Custodian vs dealer vs depository","roles","Three parties are involved: the gold IRA company (dealer) sells the metal, the custodian administers the account, and the depository stores the metal. Some companies bundle relationships, but the roles are distinct."),
  S("Examples and how to choose","choose","Common self-directed custodians include Equity Trust and the Strata Trust company. Compare flat annual fees, responsiveness, available depositories, and whether storage can be segregated. Your gold IRA company can usually recommend a custodian it works with."),
  S("Fees to expect","fees","Custodians typically charge a one-time setup fee and a flat annual administration fee, separate from depository storage. Flat fees are preferable to percentage-of-assets pricing, which grows with your balance."),
 ],
 feature="",
 faqs=[("Do I need a custodian for a gold IRA?","Yes. The IRS requires a qualified custodian to hold and administer the account; you cannot self-custody IRA metal."),
  ("What is the difference between a custodian and a depository?","The custodian administers the IRA and handles paperwork; the depository physically stores and insures the metal."),
  ("Who are common gold IRA custodians?","Equity Trust and the Strata Trust company are among the most frequently used self-directed custodians.")],
 related=["self-directed-gold-ira","gold-ira-fees","gold-ira-rules"]),

"gold-ira-withdrawal-rules": dict(navlabel="Gold IRA Withdrawals & RMDs",
 title="Gold IRA Withdrawal Rules 2026: RMDs, Penalties & In-Kind - Gold Advisor",
 h1="Gold IRA Withdrawal Rules",
 meta="Gold IRA withdrawal rules for 2026: the age-73 RMD, the 10% early-withdrawal penalty before 59½, cash vs in-kind distributions, and how each is taxed.",
 answer="You can take gold IRA distributions in cash or as the physical metal (in-kind) starting at age 59 and a half without penalty. Traditional accounts require minimum distributions beginning at age 73; withdrawals before 59 and a half generally add a 10% penalty.",
 intro="Knowing the withdrawal rules in advance helps you avoid penalties and plan for required distributions. Gold IRAs follow the standard IRA timeline, with one twist: you can take the metal itself instead of cash.",
 sections=[
  S("When you can withdraw","when","Qualified distributions can begin at age 59 and a half. Earlier withdrawals are generally subject to a 10% early-distribution penalty on top of any income tax, with limited exceptions such as certain hardships."),
  S("Required minimum distributions","rmd","Traditional gold IRAs require minimum distributions starting at age 73. Because the asset is physical metal, satisfying an RMD may mean selling some metal for cash or taking an in-kind distribution — plan ahead for liquidity."),
  S("Cash vs in-kind distributions","inkind","You can have the custodian sell metal and distribute cash, or ship the physical metal to you (an in-kind distribution). Either way, a Traditional account's distribution is taxed as ordinary income at its value when taken."),
  S("Roth differences","roth","A Roth gold IRA has no lifetime RMDs, and qualified withdrawals are tax-free, which can make Roth accounts attractive for those who expect higher future tax rates or want to leave assets to heirs."),
 ],
 feature="",
 faqs=[("When can I withdraw from a gold IRA without penalty?","At age 59 and a half. Earlier withdrawals generally incur a 10% penalty plus income tax, with limited exceptions."),
  ("Do gold IRAs have required minimum distributions?","Traditional gold IRAs require RMDs starting at age 73. Roth IRAs have no lifetime RMDs."),
  ("Can I take my gold IRA distribution as physical metal?","Yes — an in-kind distribution ships the metal to you; it is taxed as ordinary income for a Traditional account.")],
 related=["gold-ira-tax-rules","roth-gold-ira","gold-ira-rules"]),

"roth-gold-ira": dict(navlabel="Roth Gold IRA",
 title="Roth Gold IRA 2026: Tax-Free Growth & How It Works - Gold Advisor",
 h1="Roth Gold IRA",
 meta="A Roth gold IRA holds physical gold with after-tax dollars for tax-free qualified withdrawals. Learn income limits, contributions, conversions, and the trade-offs for 2026.",
 answer="A Roth gold IRA holds physical gold funded with after-tax dollars, so qualified withdrawals — including all growth — are tax-free. It has the same metals and storage rules as any gold IRA, plus Roth income limits and no lifetime RMDs.",
 intro="A Roth gold IRA combines the tax-free growth of a Roth with physical precious-metals diversification. It is especially appealing if you expect higher tax rates later or want an account with no required distributions during your lifetime.",
 sections=[
  S("How a Roth gold IRA works","how","You contribute after-tax dollars (or convert existing funds), buy IRS-eligible metal through a self-directed IRA, and store it at an approved depository. Qualified withdrawals in retirement are entirely tax-free, including any appreciation."),
  S("Contribution and income limits","limits","Roth IRAs share the 2026 limit of $7,500 (or $8,600 with the 50-plus catch-up), but eligibility to contribute phases out at higher incomes. High earners sometimes use conversions to fund a Roth instead."),
  S("Conversions","convert","You can convert a Traditional IRA or 401(k) into a Roth gold IRA, paying income tax on the converted amount now in exchange for tax-free growth later. This can make sense in lower-income years."),
  S("Roth vs Traditional gold IRA","vs","Choose Roth if you expect higher future tax rates or want no lifetime RMDs and tax-free inheritance; choose Traditional if you want a deduction now and expect lower rates in retirement."),
 ],
 feature="",
 faqs=[("What is a Roth gold IRA?","A self-directed Roth IRA holding physical gold, funded with after-tax dollars so qualified withdrawals are tax-free."),
  ("Does a Roth gold IRA have RMDs?","No. Roth IRAs have no required minimum distributions during the owner's lifetime."),
  ("Can I convert my 401(k) to a Roth gold IRA?","Yes, through a conversion, but you will owe income tax on the converted pre-tax amount in the year of conversion.")],
 related=["gold-ira-tax-rules","gold-ira-rollover","what-is-a-gold-ira"]),

"tsp-to-gold-ira": dict(navlabel="TSP to Gold IRA",
 title="TSP to Gold IRA Rollover 2026: Federal Employees & Military - Gold Advisor",
 h1="TSP to Gold IRA Rollover",
 meta="How federal employees and military members can roll a Thrift Savings Plan (TSP) into a gold IRA in 2026 — eligibility, the direct-transfer steps, and tax rules.",
 answer="Federal employees and service members can roll a Thrift Savings Plan into a gold IRA by opening a self-directed IRA and requesting a direct transfer. It is tax-free and penalty-free; eligibility usually requires separation from service or reaching age 59 and a half for in-service rollovers.",
 intro="The TSP is the federal government's version of a 401(k), and it has no physical-metals option. Rolling some of it into a gold IRA lets federal and military savers diversify into precious metals while keeping the tax advantages — subject to the TSP's eligibility rules.",
 sections=[
  S("TSP rollover eligibility","eligibility","You can generally roll over the TSP after leaving federal service. While still employed, in-service rollovers are typically allowed once you reach age 59 and a half. Check current TSP withdrawal rules, which can change."),
  S("Why federal savers diversify","why","The TSP's low-cost funds are excellent for growth but offer no tangible-asset hedge. A gold IRA adds precious-metals diversification many federal employees and veterans use to balance market and inflation risk."),
  S("The direct-transfer steps","steps","Open a self-directed IRA, request a direct rollover from the TSP so funds move custodian-to-custodian, choose IRS-eligible metal through your gold IRA company, and have it stored at an approved depository in your IRA's name."),
  S("Tax considerations","tax","A direct rollover is tax-free and penalty-free. Roll traditional TSP funds into a Traditional gold IRA, and Roth TSP funds into a Roth gold IRA, to preserve each one's tax treatment."),
 ],
 feature="",
 faqs=[("Can I roll my TSP into a gold IRA?","Yes. After separating from service — or via an in-service rollover at 59 and a half — you can do a direct, tax-free rollover into a self-directed gold IRA."),
  ("Is a TSP-to-gold rollover taxable?","A direct rollover is tax-free and penalty-free. Keep traditional and Roth funds in matching account types."),
  ("Can I roll over my TSP while still in service?","Often only after age 59 and a half via an in-service rollover; otherwise you generally must separate from federal service first.")],
 related=["401k-to-gold-ira-rollover","gold-ira-rollover","roth-gold-ira"]),

"is-gold-a-good-investment": dict(navlabel="Is Gold a Good Investment?",
 title="Is Gold a Good Investment in 2026? Pros, Cons & Allocation - Gold Advisor",
 h1="Is Gold a Good Investment in 2026?",
 meta="Is gold a good investment in 2026? A balanced look at gold's role as an inflation hedge and diversifier, its lack of income, volatility, and how much to allocate.",
 answer="Gold can be a good investment as a diversifier and inflation hedge, but it produces no income and can be volatile, so most advisors suggest holding it as a modest 5% to 10% portion of a portfolio rather than a core holding.",
 intro="Gold's value comes from what it is not: it is not a company, a currency, or a bond. That independence is exactly why it can protect a portfolio when other assets fall — and also why it lags during long bull markets. Here is a balanced view.",
 sections=[
  S("Gold as a diversifier","diversifier","Gold often moves differently from stocks and bonds, so a small allocation can reduce overall portfolio swings. Its low correlation with paper assets is the main reason institutional and individual investors hold it."),
  S("Gold as an inflation and crisis hedge","hedge","Historically, gold has tended to preserve purchasing power over long periods and has often risen during currency weakness, geopolitical stress, and severe market downturns — though the relationship is not perfectly consistent year to year."),
  S("The downsides","downsides","Gold pays no dividends or interest, so it can underperform stocks over long horizons. Its price can also be volatile in the short term, and physical ownership carries storage and insurance costs."),
  S("How much to hold","allocation","A common guideline is 5% to 10% of a portfolio in precious metals — enough to diversify and hedge without giving up the compounding that income-producing assets provide. Your ideal figure depends on goals and risk tolerance."),
 ],
 feature="",
 faqs=[("Is gold a good investment in 2026?","Gold can be a useful diversifier and inflation hedge, but because it earns no income, most advisors treat it as a modest portion of a portfolio."),
  ("How much of my portfolio should be in gold?","A frequent guideline is 5% to 10%, adjusted for your goals, time horizon, and risk tolerance."),
  ("Does gold pay any income?","No. Gold pays no dividends or interest; its return depends entirely on price appreciation, which is why it complements rather than replaces income assets.")],
 related=["gold-ira-pros-and-cons","how-to-buy-gold","what-is-a-gold-ira"]),
}

GUIDE_BODY = """<div class="wrap"><nav class="crumbs"><a href="{prefix}index.html">Home</a> &nbsp;/&nbsp; <a href="{prefix}guides/index.html">Guides</a> &nbsp;/&nbsp; <span>{navlabel}</span></nav></div>
<section class="hero"><div class="wrap"><div class="hero-content">
  <span class="eyebrow"><span class="dot"></span>Guide &middot; Updated June 2026</span>
  <h1>{h1}</h1>
  <p class="lead">{answer}</p>
</div></div></section>

<section><div class="wrap prose">
  <div class="answer"><b>Quick answer:</b> {answer}</div>
  <div class="toc"><span class="toct">On this page</span>{toc}</div>
  <p>{intro}</p>
  {sections_html}
  {feature}
</div></div>

<div class="rank-wrap"><div class="wrap">
  <div class="rank-head"><h2>Top Gold IRA companies (2026)</h2><span class="upd">Updated June 2026</span></div>
{companies}
  <p class="rank-note">Order is editorial; we may earn a commission from links above. Scores are illustrative placeholders pending your own verification.</p>
</div></div>

<section><div class="wrap prose">
  <h2 id="faq">Frequently asked questions</h2>
  {faq_html}
  <h3>Related guides</h3>
  <div class="related">{related_html}</div>
</div></section>
{footer}
</body></html>
<style>.toc{{background:var(--bg-2);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin:0 0 22px}}
.toc .toct{{display:block;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted-2);font-weight:700;margin-bottom:8px}}
.toc a{{display:inline-block;margin:3px 16px 3px 0;font-size:.9rem;color:var(--gold-deep);font-weight:600}}
.ctable{{width:100%;border-collapse:collapse;margin:20px 0;font-size:.92rem}}
.ctable th,.ctable td{{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}}
.ctable th{{background:var(--bg-2);color:var(--navy);font-family:'Fraunces',serif}}
.ctable tr:nth-child(even) td{{background:var(--surface-2)}}</style>"""

def build_guide(slug):
    g = GUIDES[slug]; prefix = "../../"
    canonical = f"https://gold-advisor.com/guides/{slug}/"
    secs = g["sections"]
    toc = "".join(f'<a href="#{a}">{h}</a>' for (h,a,_) in secs)
    sections_html = "".join(f'<h2 id="{a}">{h}</h2>'+"".join(f"<p>{p}</p>" for p in ps) for (h,a,ps) in secs)
    faq_html = "".join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i,(q,a) in enumerate(g["faqs"]))
    related_html = "".join(f'<a href="{prefix}guides/{rs}/index.html">{GUIDES[rs]["navlabel"]}</a>' for rs in g.get("related",[]))
    related_html += f'<a href="{prefix}gold-ira-companies/index.html">Company reviews</a><a href="{prefix}invest-in-gold/index.html">Gold by state</a>'
    sch = schema([("Home","https://gold-advisor.com/"),("Guides","https://gold-advisor.com/guides/"),(g["navlabel"],canonical)], g["faqs"])
    sch += '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":g["h1"],"author":{"@type":"Organization","name":"Gold Advisor"},"publisher":{"@type":"Organization","name":"Gold Advisor"},"datePublished":"2026-06-01","dateModified":"2026-06-07"})+'</script>\n'
    body = GUIDE_BODY.format(prefix=prefix, navlabel=g["navlabel"], h1=g["h1"], answer=g["answer"],
        toc=toc, intro=g["intro"], sections_html=sections_html, feature=g.get("feature",""),
        companies=render_companies(prefix), faq_html=faq_html, related_html=related_html, footer=footer(prefix))
    return page(g["title"], g["meta"], canonical, prefix, sch, body)

def build_guides_hub():
    prefix = "../"
    title = "Gold IRA Guides & Resources (2026) - Gold Advisor"
    desc = "In-depth gold IRA guides for 2026: rollovers, rules, fees, taxes, eligible coins, custodians, and how to choose the best company."
    canonical = "https://gold-advisor.com/guides/"
    links = "\n".join(f'    <a href="{prefix}guides/{s}/index.html"><span>{GUIDES[s]["navlabel"]}</span></a>' for s in GUIDE_ORDER)
    sch = schema([("Home","https://gold-advisor.com/"),("Guides",canonical)],
                 [("What should I learn before opening a gold IRA?","Start with how a gold IRA works, the IRS rules, the fees, and how rollovers are done — then compare companies.")])
    return HEAD.format(title=title, desc=desc, canonical=canonical, prefix=prefix, schema=sch, hero_uri=HERO_URI) + HUB.format(
        prefix=prefix, h1="Gold IRA Guides", lead="In-depth, regularly updated guides covering every step of buying gold and opening a gold IRA.", links=links, footer=footer(prefix))
