import json, itertools

# Short positioning tags per company (for versus tables)
SHORT = {"augusta":"Education &amp; high-net-worth","goldco":"401(k)/IRA rollovers",
         "priority":"Low minimum","ahg":"First-time buyers","birch":"Metals variety"}
MIN_NUM = {"augusta":50000,"goldco":25000,"priority":10000,"ahg":10000,"birch":10000}

CT_CSS = (".ctable{width:100%;border-collapse:collapse;margin:18px 0;font-size:.93rem}"
 ".ctable th,.ctable td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}"
 ".ctable th{background:var(--bg-2);color:var(--navy);font-family:'Fraunces',serif}"
 ".ctable tr:nth-child(even) td{background:var(--surface-2)}"
 ".ctable td.win{background:#e9f7ef!important;font-weight:600;color:#17834a}")

def _shell(prefix, crumb, eyebrow, h1, lead, content, footer_html, byline=True, extra_style="", author=False):
    by = (f'<div class="byline">By <a href="{prefix}about/aaron-tal/index.html">Aaron Tal</a> &middot; Precious-metals analyst &middot; Reviewed <span class="ga-now">June 2026</span></div>') if byline else ""
    ac = AUTHOR_CARD.format(prefix=prefix) if author else ""
    return (f'<div class="wrap"><nav class="crumbs"><a href="{prefix}index.html">Home</a> &nbsp;/&nbsp; <span>{crumb}</span></nav></div>\n'
        f'<section class="hero"><div class="wrap"><div class="hero-content">\n'
        f'  <span class="eyebrow"><span class="dot"></span>{eyebrow}</span>\n  <h1>{h1}</h1>\n  <p class="lead">{lead}</p>\n  {by}\n'
        f'</div></div></section>\n<section><div class="wrap prose">\n{content}\n</div></section>\n{ac}{footer_html}\n</body></html>\n'
        f'<style>{CT_CSS}{extra_style}</style>')

# ---------------------------------------------------------------- author / about / methodology
def build_author():
    prefix="../../"
    canonical="https://gold-advisor.com/about/aaron-tal/"
    title="Aaron Tal \u2014 Precious Metals Analyst & Gold IRA Researcher | Gold Advisor"
    desc="Aaron Tal is a financial-markets analyst focused on gold and silver for 10+ years, author of precious-metals sections at JPost.com and TipRanks.com."
    content=(f'<p>{AUTHOR["bio"]}</p>'
     '<h2 id="experience">Experience &amp; credentials</h2>'
     '<ul class="checks">'
     '<li>10+ years working in financial markets with a focus on gold and silver</li>'
     '<li>Author of the precious-metals news section at <strong>The Jerusalem Post (JPost.com)</strong></li>'
     '<li>Author of the precious-metals news section at <strong>TipRanks.com</strong></li><li>Precious-metals news writer and Gold IRA analyst at <strong>Investing.com</strong></li>'
     '<li>A decade of hands-on research into Gold IRA companies, fees, and custody</li>'
     '<li>Author of in-depth company reviews that help investors make better-informed decisions</li><li>Manually audits verified customer reviews across Google, BBB, Trustpilot, TrustLink, and BCA for every company reviewed</li>'
     '</ul>'
     '<h2 id="approach">How I approach reviews</h2>'
     '<p>My goal is simple: cut through the marketing so readers can compare Gold IRA providers on what actually matters \u2014 transparent pricing, account minimums, metals selection, storage, and verifiable reputation. Every review is dated, sourced where possible, and updated as the market changes. I disclose that this site earns affiliate commissions; that keeps it free and never changes the editorial assessment.</p>'
     f'<p>See the full <a href="{prefix}methodology/index.html">ranking methodology</a> or read the <a href="{prefix}gold-ira-companies/index.html">company reviews</a>.</p>')
    person={"@context":"https://schema.org","@type":"Person","name":"Aaron Tal","jobTitle":"Precious Metals Analyst",
            "description":AUTHOR["bio"],"url":canonical,"sameAs":["https://www.jpost.com/","https://www.tipranks.com/","https://www.investing.com/"],
            "knowsAbout":["Gold IRA","precious metals investing","gold","silver","retirement accounts"]}
    sch=schema([("Home","https://gold-advisor.com/"),("About","https://gold-advisor.com/about/"),("Aaron Tal",canonical)],[])
    sch+='<script type="application/ld+json">'+json.dumps(person)+'</script>\n'
    body=_shell(prefix,"Aaron Tal","Author \u00b7 Precious Metals Analyst","Aaron Tal",
        "Financial-markets analyst focused on gold and silver for over a decade \u2014 and the researcher behind Gold Advisor's reviews.",
        content, footer(prefix), byline=False,
        extra_style=".checks{list-style:none;margin:6px 0 4px}.checks li{position:relative;padding:6px 0 6px 26px;color:var(--ink)}.checks li::before{content:'\\2713';position:absolute;left:0;color:var(--cta);font-weight:800}")
    return page(title,desc,canonical,prefix,sch,body)

def build_about():
    prefix="../"
    canonical="https://gold-advisor.com/about/"
    title="About Gold Advisor \u2014 Independent Gold IRA Reviews"
    desc="Gold Advisor is an independent research site comparing Gold IRA companies on fees, minimums, storage, and reputation. Reviews by analyst Aaron Tal."
    content=('<div class="answer"><b>In short:</b> Gold Advisor is an independent education and review site that helps Americans compare Gold IRA companies and understand how to buy gold the right way.</div>'
     '<p>We exist because the Gold IRA space is full of marketing and short on plain, comparable facts. We publish transparent rankings, state-by-state and city guides, plain-English explainers, and head-to-head comparisons \u2014 all kept current for 2026.</p>'
     '<h2 id="author">Who writes Gold Advisor</h2>'
     f'<p>Reviews and guides are written by <a href="{prefix}about/aaron-tal/index.html"><strong>Aaron Tal</strong></a>, a financial-markets analyst focused on gold and silver for over 10 years and author of precious-metals sections at JPost.com and TipRanks.com.</p>'
     '<h2 id="independence">How we stay independent</h2>'
     '<p>Gold Advisor earns affiliate commissions when readers visit some companies through our links. This keeps the site free and may affect which companies appear, but it does not change our editorial assessments or rankings. See our full <a href="'+prefix+'methodology/index.html">methodology</a> for exactly how we score companies.</p>'
     '<h2 id="explore">Explore</h2>'
     f'<div class="related"><a href="{prefix}gold-ira-companies/index.html">Company reviews</a><a href="{prefix}compare/index.html">Head-to-head comparisons</a><a href="{prefix}guides/index.html">Guides</a><a href="{prefix}tools/index.html">Tools &amp; calculators</a><a href="{prefix}gold-ira-fee-index/index.html">Fee index</a><a href="{prefix}bullion-sales-tax-tracker/index.html">Tax tracker</a><a href="{prefix}gold-ira-scams/index.html">Avoid scams</a><a href="{prefix}resources/index.html">Rules &amp; resources</a></div>')
    sch=schema([("Home","https://gold-advisor.com/"),("About",canonical)],[])
    body=_shell(prefix,"About","About Gold Advisor","About Gold Advisor",
        "Independent research and reviews to help you compare Gold IRA companies with confidence.",
        content, footer(prefix), byline=False)
    return page(title,desc,canonical,prefix,sch,body)

def build_methodology():
    prefix="../"
    canonical="https://gold-advisor.com/methodology/"
    title="Our Gold IRA Ranking Methodology (2026) | Gold Advisor"
    desc="How Gold Advisor ranks Gold IRA companies: a manual audit of verified customer reviews across Google, BBB, Trustpilot, TrustLink, and BCA \u2014 plus fees, minimums, metals, and storage."
    content=('<div class="answer"><b>Quick answer:</b> Our rankings rest on the one thing in this industry that cannot be faked \u2014 verified customer reviews. For every company on this site we manually audited each major review platform (Google, BBB, Trustpilot, TrustLink, BCA) and scored real verified-client feedback, then layered in fees, minimums, metals, and storage.</div>'
     '<h2 id="reviews">The one thing that can\u2019t be ignored</h2>'
     '<p>After more than 10 years in the Gold IRA space \u2014 much of it working alongside the largest precious-metals companies in the United States \u2014 I\u2019ve learned that almost everything in this industry can be polished: the website, the sales script, the glossy kit that arrives in the mail. The one thing that can\u2019t be spun is what thousands of real, verified clients say <em>after</em> their money has moved and their metals have shipped.</p>'
     '<p>That is why verified customer reviews are the backbone of every ranking on this page. For each company we feature, I personally carried out a complete, manual review of every major independent review platform \u2014 not a glance at a star rating, but a careful read through the actual customer experiences, complaints, and how each company responded.</p>'
     '<h2 id="platforms">The review platforms we manually audit</h2>'
     '<p>For every company on this site, we evaluated its standing and verified-client feedback across each of these independent sources:</p>'
     '<ul class="checks">'
     '<li><strong>Google Reviews</strong> \u2014 the largest pool of unfiltered, verified customer feedback.</li>'
     '<li><strong>Better Business Bureau (BBB)</strong> \u2014 accreditation, letter rating, and how complaints were resolved.</li>'
     '<li><strong>Trustpilot</strong> \u2014 high-volume verified reviews and how responsive the company is.</li>'
     '<li><strong>TrustLink</strong> \u2014 a precious-metals-focused review platform widely used in this industry.</li>'
     '<li><strong>Business Consumer Alliance (BCA)</strong> \u2014 independent business-conduct ratings and complaint history.</li>'
     '<li><strong>ConsumerAffairs</strong> \u2014 additional verified buyer experiences where available.</li>'
     '</ul>'
     '<h2 id="audit">How we audit each company</h2>'
     '<p>On every platform, for every company, the manual review looked past the headline score at four things:</p>'
     '<table class="ctable"><thead><tr><th>What we measured</th><th>Why it matters</th></tr></thead><tbody>'
     '<tr><td>Aggregate verified rating</td><td>The blended star and letter score from real, verified clients across every platform.</td></tr>'
     '<tr><td>Review volume &amp; recency</td><td>A 4.9 from 4,000 recent reviews carries far more weight than a 5.0 from a dozen.</td></tr>'
     '<tr><td>Recurring themes</td><td>We read individual reviews for patterns \u2014 pressure tactics, hidden fees, shipping times, and the buyback experience.</td></tr>'
     '<tr><td>Complaint resolution</td><td>Every company gets complaints; what separates the best is whether they are answered and made right.</td></tr>'
     '</tbody></table>'
     '<h2 id="score">How the verified-client score is built</h2>'
     '<p>We combine those platform-by-platform findings into a single verified-client reputation score for each company \u2014 weighted toward review volume, recency, and complaint resolution rather than one cherry-picked rating. That reputation score is the single heaviest input in the overall ranking, because it reflects real outcomes for real investors instead of marketing.</p>'
     '<h2 id="factors">The full scoring model</h2>'
     '<p>Verified reviews lead, but they are not the only factor. The overall score blends six weighted inputs:</p>'
     '<table class="ctable"><thead><tr><th>Factor</th><th>Weight</th><th>What it captures</th></tr></thead><tbody>'
     '<tr><td><strong>Verified customer reviews</strong></td><td class="win">35%</td><td>Manual audit across Google, BBB, Trustpilot, TrustLink, BCA, and ConsumerAffairs.</td></tr>'
     '<tr><td>Pricing transparency &amp; fees</td><td>20%</td><td>Clear, written pricing and reasonable flat fees.</td></tr>'
     '<tr><td>Account minimum &amp; accessibility</td><td>15%</td><td>Who can realistically open and fund an account.</td></tr>'
     '<tr><td>Metals selection &amp; storage</td><td>15%</td><td>IRS-approved metals, depositories, and segregated options.</td></tr>'
     '<tr><td>Buyback program</td><td>10%</td><td>A clear, fair exit when it is time to sell.</td></tr>'
     '<tr><td>Education &amp; support</td><td>5%</td><td>Quality of guidance, without high-pressure tactics.</td></tr>'
     '</tbody></table>'
     '<h2 id="data">How we keep it current</h2>'
     '<p>Ratings and complaint counts move over time, so we re-check the major platforms periodically and date every page. Figures such as fees and minimums change too \u2014 we mark them \u201cverify directly\u201d and refresh as needed.</p>'
     '<h2 id="disclosure">Independence &amp; disclosure</h2>'
     '<p>Companies cannot pay for a higher ranking or a better verified-review score. We earn affiliate commissions from some outbound links, marked <code>rel="nofollow sponsored"</code>; this keeps the site free but is kept entirely separate from how companies are scored. Nothing here is financial, tax, or legal advice.</p>')
    sch=schema([("Home","https://gold-advisor.com/"),("Methodology",canonical)],
               [("How do you rank gold IRA companies?","We begin with a manual audit of verified customer reviews across Google, BBB, Trustpilot, TrustLink, BCA, and ConsumerAffairs for each company, then weight in fees, minimums, metals, storage, and buyback. Verified reviews are the heaviest factor."),
                ("Can companies pay for a better ranking?","No. Rankings and verified-review scores are editorial; affiliate compensation keeps the site free but does not influence them.")])
    body=_shell(prefix,"Methodology","Editorial Standards \u00b7 Verified Reviews","How We Rank Gold IRA Companies",
        "Our rankings start with the one signal that can\u2019t be faked: a manual audit of verified customer reviews for every company we feature.",
        content, footer(prefix),
        extra_style=".checks{list-style:none;margin:6px 0 4px;padding:0}.checks li{position:relative;padding:7px 0 7px 28px;color:var(--ink);border-bottom:1px solid var(--line)}.checks li::before{content:'\\2713';position:absolute;left:0;top:7px;color:var(--cta);font-weight:800}")
    return page(title,desc,canonical,prefix,sch,body)

# versus pages
VS_PAIRS = list(itertools.combinations(["augusta","goldco","priority","ahg","birch"], 2))

def build_versus(a, b):
    ra, rb = REVIEWS[a], REVIEWS[b]; prefix="../../"
    slug=f"{ra['slug']}-vs-{rb['slug']}"
    na, nb = ra["name"], rb["name"]
    canonical=f"https://gold-advisor.com/compare/{slug}/"
    title=f"{na} vs {nb} (2026): Which Gold IRA Is Better? - Gold Advisor"
    desc=f"{na} vs {nb} compared on fees, minimums, metals, storage, and reputation for 2026 \u2014 and which one is the better Gold IRA company for you."
    def cell(x,y,lower_better=False,numa=None,numb=None):
        # mark winner cell green when comparable
        return x,y
    rows=[("Our score",ra["score"]+"/10",rb["score"]+"/10"),
          ("Founded",ra["founded"],rb["founded"]),
          ("Headquarters",ra["hq"],rb["hq"]),
          ("Minimum investment",ra["minimum"],rb["minimum"]),
          ("Metals offered",ra["metals"],rb["metals"]),
          ("Storage / depository",ra["depository"],rb["depository"]),
          ("BBB rating",ra["bbb"],rb["bbb"]),
          ("Best for",SHORT[a],SHORT[b])]
    trs=""
    for k,va,vb in rows:
        ca=cb=""
        if k=="Our score":
            if float(ra["score"])>float(rb["score"]): ca=" class=win"
            elif float(rb["score"])>float(ra["score"]): cb=" class=win"
        if k=="Minimum investment":
            if MIN_NUM[a]<MIN_NUM[b]: ca=" class=win"
            elif MIN_NUM[b]<MIN_NUM[a]: cb=" class=win"
        if k=="Metals offered":
            if len(ra["metals"])>len(rb["metals"]): ca=" class=win"
            elif len(rb["metals"])>len(ra["metals"]): cb=" class=win"
        trs+=f"<tr><td><strong>{k}</strong></td><td{ca}>{va}</td><td{cb}>{vb}</td></tr>"
    table=(f'<table class="ctable"><thead><tr><th></th><th>{na}</th><th>{nb}</th></tr></thead><tbody>{trs}</tbody></table>')
    content=(f'<div class="answer"><b>Quick answer:</b> {na} is the stronger pick for {SHORT[a].lower().replace("&amp;","and")}, while {nb} is better for {SHORT[b].lower().replace("&amp;","and")}. The right choice comes down to your budget and what you value most.</div>'
     f'<p>Both {na} and {nb} are reputable, A+ BBB-rated Gold IRA companies in our 2026 ranking. Here is how they stack up head to head, followed by where each one pulls ahead.</p>'
     f'<h2 id="table">{na} vs {nb}: head to head</h2>{table}'
     f'<h2 id="where-a">Where {na} wins</h2><p>{ra["verdict"]}</p>'
     f'<h2 id="where-b">Where {nb} wins</h2><p>{rb["verdict"]}</p>'
     f'<h2 id="choose">Which should you choose?</h2>'
     f'<p>Choose <strong>{na}</strong> if your priority is {SHORT[a].lower().replace("&amp;","and")}; choose <strong>{nb}</strong> if it is {SHORT[b].lower().replace("&amp;","and")}. Read the full <a href="{prefix}gold-ira-companies/{ra["slug"]}-review/index.html">{na} review</a> or <a href="{prefix}gold-ira-companies/{rb["slug"]}-review/index.html">{nb} review</a> before deciding.</p>')
    faqs=[(f"Is {na} or {nb} better?",f"{na} is better for {SHORT[a].lower().replace('&amp;','and')}; {nb} is better for {SHORT[b].lower().replace('&amp;','and')}. Both are reputable A+ BBB companies."),
          (f"What is the minimum for {na} vs {nb}?",f"{na}: {ra['minimum']}. {nb}: {rb['minimum']}. Confirm current figures directly before opening an account.")]
    faq_html="".join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{ans}</p></details>' for i,(q,ans) in enumerate(faqs))
    content+=f'<h2 id="faq">FAQ</h2>{faq_html}'
    content+=(f'<h3>Compare more</h3><div class="related">'
        f'<a href="{prefix}compare/index.html">All comparisons</a>'
        f'<a href="{prefix}index.html#rankings">Full top 5</a>'
        f'<a href="{prefix}tools/gold-ira-quiz/index.html">Take the quiz</a></div>')
    sch=schema([("Home","https://gold-advisor.com/"),("Compare","https://gold-advisor.com/compare/"),(f"{na} vs {nb}",canonical)],faqs)
    sch+='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":f"{na} vs {nb} (2026)","author":AUTHOR_LD,"publisher":{"@type":"Organization","name":"Gold Advisor"},"datePublished":"2026-06-01","dateModified":"2026-06-07"})+'</script>\n'
    body=_shell(prefix,f"{na} vs {nb}","Head-to-Head \u00b7 2026",f"{na} <span style='color:var(--gold-bright)'>vs</span> {nb}",
        f"Which Gold IRA company is the better fit? A side-by-side look at fees, minimums, metals, storage, and reputation.",
        content, footer(prefix), author=True)
    return slug, page(title,desc,canonical,prefix,sch,body)

def build_compare_hub():
    prefix="../"
    canonical="https://gold-advisor.com/compare/"
    title="Gold IRA Company Comparisons (2026) | Gold Advisor"
    desc="Head-to-head Gold IRA company comparisons for 2026 \u2014 Augusta vs Goldco, Goldco vs Birch, and every other matchup of our top five."
    links=""
    for a,b in VS_PAIRS:
        ra,rb=REVIEWS[a],REVIEWS[b]; sl=f"{ra['slug']}-vs-{rb['slug']}"
        links+=f'    <a href="{prefix}compare/{sl}/index.html"><span>{ra["name"]} vs {rb["name"]}</span></a>\n'
    sch=schema([("Home","https://gold-advisor.com/"),("Compare",canonical)],
               [("How do the top gold IRA companies compare?","Each matchup weighs fees, minimums, metals, storage, and reputation. Augusta leads on education, Goldco on rollovers, Birch on metals variety, and Priority/AHG on low minimums.")])
    return HEAD.format(title=title,desc=desc,canonical=canonical,prefix=prefix,schema=sch,hero_uri=f"{prefix}assets/img/hero.jpg")+HUB.format(
        prefix=prefix,h1="Gold IRA Comparisons",lead="Every head-to-head matchup of our top five Gold IRA companies, compared side by side.",links=links,footer=footer(prefix))

# ---------------------------------------------------------------- tools: quiz + calculator
def build_quiz():
    prefix="../../"
    canonical="https://gold-advisor.com/tools/gold-ira-quiz/"
    title="Gold IRA Quiz: Which Company Fits You? (2026) | Gold Advisor"
    desc="Answer 3 quick questions and get a personalized Gold IRA company recommendation from our 2026 top five \u2014 based on your budget, goals, and metals."
    quiz='''<div class="answer"><b>Find your match:</b> answer three quick questions and we'll point you to the company in our 2026 top five that best fits your budget and goals.</div>
<div id="quiz" class="quiz"></div>
<script>
var Q=[
 {q:"What can you start with?",a:[["Under $10,000","budget0"],["$10,000 \u2013 $25,000","budget1"],["$25,000 \u2013 $50,000","budget2"],["$50,000 or more","budget3"]]},
 {q:"What matters most to you?",a:[["Lowest cost / minimum","low"],["Help rolling over a 401(k)/IRA","rollover"],["Education and transparency","edu"],["First-timer hand-holding","first"]]},
 {q:"Which metals do you want?",a:[["Gold &amp; silver only","gs"],["Also platinum / palladium","ppt"]]}
];
var COMP={augusta:{n:"Augusta Precious Metals",s:"9.8",slug:"augusta-precious-metals",k:"augusta"},
 goldco:{n:"Goldco",s:"9.6",slug:"goldco",k:"goldco"},
 priority:{n:"Priority Gold",s:"9.4",slug:"priority-gold",k:"priority"},
 ahg:{n:"American Hartford Gold",s:"9.3",slug:"american-hartford-gold",k:"ahg"},
 birch:{n:"Birch Gold Group",s:"9.1",slug:"birch-gold-group",k:"birch"}};
var ans=[],step=0;
function pick(tag){ans[step]=tag;step++;render();}
function decide(){
 if(ans.indexOf("ppt")>-1) return "birch";
 if(ans.indexOf("rollover")>-1) return "goldco";
 if(ans.indexOf("edu")>-1 || ans.indexOf("budget3")>-1) return "augusta";
 if(ans.indexOf("first")>-1) return "ahg";
 return "priority";
}
function render(){
 var el=document.getElementById("quiz");
 if(step<Q.length){
  var s=Q[step];
  var h='<div class="qprog">Question '+(step+1)+' of '+Q.length+'</div><h3 class="qq">'+s.q+'</h3><div class="qopts">';
  for(var i=0;i<s.a.length;i++){h+='<button class="qopt" onclick="pick(\\''+s.a[i][1]+'\\')">'+s.a[i][0]+'</button>';}
  h+='</div>';
  if(step>0)h+='<button class="qback" onclick="step--;render()">\\u2190 Back</button>';
  el.innerHTML=h;
 } else {
  var c=COMP[decide()];
  el.innerHTML='<div class="qresult"><div class="qrlabel">Your best match</div><h3>'+c.n+'</h3>'
   +'<div class="qrscore">'+c.s+'<span>/10</span></div>'
   +'<a class="go primary" data-aff="'+c.k+'" rel="nofollow sponsored" href="#">Visit '+c.n.split(" ")[0]+' \\u2192</a>'
   +'<a class="qrev" href="'+PFX+'gold-ira-companies/'+c.slug+'-review/index.html">Read the full review</a>'
   +'<button class="qback" onclick="ans=[];step=0;render()">\\u21ba Start over</button></div>';
  {var a=el.querySelector("[data-aff]");if(a)a.href="/visit/"+c.slug+"/";}
 }
}
var PFX="__PFX__";
render();
</script>'''.replace("__PFX__", prefix)
    qstyle=(".quiz{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:28px;box-shadow:var(--shadow);max-width:640px}"
     ".qprog{font-size:.74rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted-2);font-weight:700;margin-bottom:8px}"
     ".qq{font-size:1.4rem;margin-bottom:16px}.qopts{display:grid;gap:10px}"
     ".qopt{text-align:left;background:var(--bg-2);border:1px solid var(--line);border-radius:11px;padding:14px 16px;font:inherit;font-weight:600;color:var(--navy);cursor:pointer;transition:border-color .2s,transform .15s}"
     ".qopt:hover{border-color:var(--gold);transform:translateY(-1px)}"
     ".qback{margin-top:14px;background:none;border:none;color:var(--muted);font:inherit;font-size:.86rem;cursor:pointer;text-decoration:underline}"
     ".qresult{text-align:center}.qrlabel{font-size:.74rem;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-deep);font-weight:700}"
     ".qresult h3{font-size:1.8rem;margin:6px 0}.qrscore{font-family:'Fraunces',serif;font-size:2.4rem;color:var(--gold-deep);font-weight:700;margin-bottom:14px}.qrscore span{font-size:1rem;color:var(--muted)}"
     ".qresult .go{display:inline-block;width:auto;padding:12px 28px;margin-bottom:10px}.qrev{display:block;font-size:.9rem;color:var(--gold-deep);text-decoration:underline;margin-bottom:8px}")
    sch=schema([("Home","https://gold-advisor.com/"),("Tools","https://gold-advisor.com/tools/"),("Gold IRA Quiz",canonical)],
               [("How do I choose a gold IRA company?","Match the company to your budget and goals \u2014 Augusta for education/larger accounts, Goldco for rollovers, Birch for metals variety, Priority and American Hartford for low minimums.")])
    body=_shell(prefix,"Gold IRA Quiz","Interactive Tool","Which Gold IRA Company Fits You?",
        "Three quick questions, one personalized recommendation from our 2026 top five.",
        quiz, footer(prefix), extra_style=qstyle)
    return page(title,desc,canonical,prefix,sch,body)

def build_calculator():
    prefix="../../"
    canonical="https://gold-advisor.com/tools/gold-ira-fee-calculator/"
    title="Gold IRA Fee Calculator (2026): Flat vs % Fees | Gold Advisor"
    desc="Free Gold IRA fee calculator: estimate total custodian and storage costs over time and see how much a flat-fee custodian saves versus a percentage-of-assets model."
    calc='''<div class="answer"><b>Why it matters:</b> flat annual fees can save thousands over time versus custodians that charge a percentage of your account value. Try your own numbers below.</div>
<div class="calc">
 <label>Account value ($)<input id="amt" type="number" value="50000" min="0" step="1000"></label>
 <label>Years held<input id="yrs" type="number" value="15" min="1" max="40"></label>
 <label>Flat annual fee ($)<input id="flat" type="number" value="225" min="0" step="5"></label>
 <label>Percentage model (% / year)<input id="pct" type="number" value="1" min="0" step="0.1"></label>
 <div class="calc-out" id="out"></div>
</div>
<script>
function fmt(n){return "$"+Math.round(n).toLocaleString();}
function calc(){
 var amt=+document.getElementById("amt").value||0, yrs=+document.getElementById("yrs").value||0,
     flat=+document.getElementById("flat").value||0, pct=(+document.getElementById("pct").value||0)/100;
 var flatTotal=flat*yrs, pctTotal=amt*pct*yrs, diff=pctTotal-flatTotal;
 var html='<div class="cr"><span>Flat-fee total ('+yrs+' yrs)</span><b>'+fmt(flatTotal)+'</b></div>'
  +'<div class="cr"><span>Percentage-model total</span><b>'+fmt(pctTotal)+'</b></div>'
  +'<div class="cr big"><span>'+(diff>=0?"You save with flat fees":"Percentage is cheaper here")+'</span><b>'+fmt(Math.abs(diff))+'</b></div>';
 document.getElementById("out").innerHTML=html;
}
["amt","yrs","flat","pct"].forEach(function(id){document.getElementById(id).addEventListener("input",calc);});
calc();
</script>
<p style="font-size:.86rem;color:var(--muted-2);margin-top:14px">Estimates only, for education \u2014 not financial advice. Real fees vary by company; most of our top picks use flat annual fees in the $200\u2013$300 range. Metal premiums over spot are separate.</p>'''
    cstyle=(".calc{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:24px;box-shadow:var(--shadow);max-width:560px;display:grid;gap:14px}"
     ".calc label{display:flex;flex-direction:column;gap:6px;font-weight:600;color:var(--navy);font-size:.9rem}"
     ".calc input{padding:11px 13px;border:1px solid var(--line);border-radius:9px;font:inherit;font-size:1rem}"
     ".calc-out{margin-top:6px;border-top:1px solid var(--line);padding-top:14px;display:grid;gap:8px}"
     ".cr{display:flex;justify-content:space-between;align-items:center;font-size:.95rem;color:var(--ink)}.cr b{font-family:'Fraunces',serif;font-size:1.1rem;color:var(--navy)}"
     ".cr.big{background:#e9f7ef;border-radius:10px;padding:12px 14px;margin-top:4px}.cr.big b{color:#17834a;font-size:1.4rem}")
    sch=schema([("Home","https://gold-advisor.com/"),("Tools","https://gold-advisor.com/tools/"),("Fee Calculator",canonical)],
               [("How much does a gold IRA cost per year?","Most flat-fee custodians charge about $200\u2013$300 per year combined; percentage-of-assets models cost more as your balance grows.")])
    body=_shell(prefix,"Fee Calculator","Interactive Tool","Gold IRA Fee Calculator",
        "See how flat annual fees compare to a percentage-of-assets model over time.",
        calc, footer(prefix), extra_style=cstyle)
    return page(title,desc,canonical,prefix,sch,body)

def build_tools_hub():
    prefix="../"
    canonical="https://gold-advisor.com/tools/"
    title="Gold IRA Tools & Calculators (2026) | Gold Advisor"
    desc="Free Gold IRA tools: a company-match quiz and a fee calculator to compare flat versus percentage costs."
    links=(f'    <a href="{prefix}tools/gold-ira-quiz/index.html"><span>Gold IRA company quiz</span><em>Find your match in 3 questions</em></a>\n'
           f'    <a href="{prefix}tools/gold-ira-fee-calculator/index.html"><span>Gold IRA fee calculator</span><em>Flat vs percentage fees</em></a>\n'
           f'    <a href="{prefix}tools/gold-ira-rollover-calculator/index.html"><span>Rollover growth calculator</span><em>Project a rollover + contributions</em></a>\n'
           f'    <a href="{prefix}tools/gold-ira-rmd-calculator/index.html"><span>RMD calculator</span><em>Required distributions at 73+</em></a>\n')
    sch=schema([("Home","https://gold-advisor.com/"),("Tools",canonical)],[])
    return HEAD.format(title=title,desc=desc,canonical=canonical,prefix=prefix,schema=sch,hero_uri=f"{prefix}assets/img/hero.jpg")+HUB.format(
        prefix=prefix,h1="Tools &amp; Calculators",lead="Interactive tools to help you choose a Gold IRA company and understand the costs.",links=links,footer=footer(prefix))

# ---------------------------------------------------------------- fee index (Dataset)
def build_fee_index():
    prefix="../"
    canonical="https://gold-advisor.com/gold-ira-fee-index/"
    title="Gold IRA Fee & Minimum Index (2026 Data) | Gold Advisor"
    desc="The 2026 Gold IRA Fee & Minimum Index: account minimums, setup, custodian, and storage fees across leading providers, with averages updated regularly."
    fees={"augusta":("$50,000","$50","$125","$100\u2013150"),"goldco":("~$25,000","$50","$80\u2013125","$100\u2013150"),
          "priority":("~$10,000","\u2014","$125","covered $50k+"),"ahg":("$10,000","$50","$125","$125"),
          "birch":("$10,000","\u2014","flat ~$180\u2013200 all-in","incl.")}
    trs=""
    for c in COMPANIES:
        k=c["key"]; f=fees[k]
        trs+=f'<tr><td>{c["name"]}</td><td>{f[0]}</td><td>{f[1]}</td><td>{f[2]}</td><td>{f[3]}</td></tr>'
    avg_min=sum(MIN_NUM.values())//len(MIN_NUM)
    low_min=min(MIN_NUM.values())
    content=(f'<div class="answer"><b>Key 2026 figures:</b> the lowest Gold IRA minimum among leading providers is <b>${low_min:,}</b>, the average across our tracked companies is about <b>${avg_min:,}</b>, and typical all-in annual fees run roughly <b>$200\u2013$300</b> (flat).</div>'
     '<p>This index tracks account minimums and the published fee components for the leading Gold IRA companies, updated as the market changes. Figures are compiled from company disclosures and current third-party sources; metal premiums over spot are quoted separately by each dealer.</p>'
     '<table class="ctable"><thead><tr><th>Company</th><th>Minimum</th><th>Setup</th><th>Annual custodian</th><th>Storage</th></tr></thead><tbody>'+trs+'</tbody></table>'
     f'<h2 id="stats">At a glance (2026)</h2>'
     '<div class="facts-box">'
     f'<div class="factrow"><span class="k">Lowest minimum</span><span class="v">${low_min:,}</span></div>'
     f'<div class="factrow"><span class="k">Average minimum</span><span class="v">${avg_min:,}</span></div>'
     '<div class="factrow"><span class="k">Typical setup fee</span><span class="v">~$50</span></div>'
     '<div class="factrow"><span class="k">Typical all-in annual</span><span class="v">$200\u2013$300</span></div></div>'
     f'<p>See the full company breakdowns in our <a href="{prefix}gold-ira-companies/index.html">reviews</a>, or estimate your own costs with the <a href="{prefix}tools/gold-ira-fee-calculator/index.html">fee calculator</a>.</p>'
     '<p style="font-size:.84rem;color:var(--muted-2)">Last updated <span class="ga-now">June 2026</span>. Figures change \u2014 verify current pricing with each company. Educational information, not financial advice.</p>')
    dataset={"@context":"https://schema.org","@type":"Dataset","name":"Gold IRA Fee & Minimum Index 2026",
     "description":"Account minimums and fee components (setup, custodian, storage) for leading U.S. Gold IRA companies, 2026.",
     "creator":{"@type":"Organization","name":"Gold Advisor"},"dateModified":"2026-06-07","url":canonical,
     "variableMeasured":["account minimum","setup fee","annual custodian fee","storage fee"]}
    sch=schema([("Home","https://gold-advisor.com/"),("Fee Index",canonical)],
               [("What is the average Gold IRA minimum in 2026?",f"Across the leading companies we track, the average minimum is about ${avg_min:,}, with the lowest at ${low_min:,}."),
                ("What are typical gold IRA fees?","Most flat-fee custodians total about $200\u2013$300 per year, plus a one-time setup around $50 and the dealer's metal premium over spot.")])
    sch+='<script type="application/ld+json">'+json.dumps(dataset)+'</script>\n'
    body=_shell(prefix,"Fee Index","Live Data \u00b7 2026","Gold IRA Fee &amp; Minimum Index",
        f"The current minimums and fees across leading Gold IRA companies \u2014 lowest minimum ${low_min:,}, typical all-in fees $200\u2013$300/year.",
        content, footer(prefix))
    return page(title,desc,canonical,prefix,sch,body)

# ---------------------------------------------------------------- bullion tax tracker (Dataset)
def build_tax_tracker():
    prefix="../"
    canonical="https://gold-advisor.com/bullion-sales-tax-tracker/"
    cats={"TAX":0,"EX":0,"NT":0,"PART":0,"VER":0}
    for st in STATES.values(): cats[st["tax"]]+=1
    taxing=cats["TAX"]; exempt=cats["EX"]; nostate=cats["NT"]; partial=cats["PART"]; verify=cats["VER"]
    title="U.S. Bullion Sales-Tax Tracker (2026, All 50 States) | Gold Advisor"
    desc=f"Which U.S. states tax gold and silver bullion in 2026: {taxing} states generally tax it, {exempt} exempt it, {nostate} have no state sales tax. Updated state-by-state tracker."
    order=["TAX","PART","VER","NT","EX"]
    label={"TAX":"Generally taxable","PART":"Partly exempt (threshold)","VER":"Recently changed \u2014 verify","NT":"No statewide sales tax","EX":"Generally exempt"}
    trs=""
    for cat in order:
        for slug,st in STATES.items():
            if st["tax"]==cat:
                trs+=f'<tr><td><a href="{prefix}invest-in-gold/{slug}/index.html">{st["name"]}</a></td><td>{label[cat]}</td></tr>'
    content=(f'<div class="answer"><b>2026 snapshot:</b> {taxing} states (plus Washington, D.C.) generally apply sales tax to investment bullion, {partial} apply a threshold/partial rule, {nostate} have no statewide sales tax, and {exempt} generally exempt it. State rules changed a lot in 2025\u20132026 \u2014 always verify before buying.</div>'
     '<p>This tracker monitors how each U.S. state treats sales tax on investment-grade gold and silver bullion. Federal Gold-IRA rules are the same everywhere; state sales tax only affects direct purchases. We refresh this as states change their laws.</p>'
     '<h2 id="counts">By the numbers (2026)</h2>'
     '<div class="facts-box">'
     f'<div class="factrow"><span class="k">Generally taxable</span><span class="v">{taxing} + DC</span></div>'
     f'<div class="factrow"><span class="k">Partly exempt (threshold)</span><span class="v">{partial}</span></div>'
     f'<div class="factrow"><span class="k">No statewide sales tax</span><span class="v">{nostate}</span></div>'
     f'<div class="factrow"><span class="k">Generally exempt</span><span class="v">{exempt}</span></div></div>'
     '<h2 id="table">State-by-state</h2>'
     '<table class="ctable"><thead><tr><th>State</th><th>Bullion sales-tax status (2026)</th></tr></thead><tbody>'+trs+'</tbody></table>'
     '<p style="font-size:.84rem;color:var(--muted-2)">Last reviewed <span class="ga-now">June 2026</span>. Volatile states (NJ, VA, CT, WA, MD, NM, ME, VT, HI) change frequently \u2014 confirm with the state revenue authority. General information, not tax advice.</p>')
    dataset={"@context":"https://schema.org","@type":"Dataset","name":"U.S. Bullion Sales-Tax Tracker 2026",
     "description":"Sales-tax treatment of investment gold and silver bullion across all 50 U.S. states, 2026.",
     "creator":{"@type":"Organization","name":"Gold Advisor"},"dateModified":"2026-06-07","url":canonical,
     "spatialCoverage":"United States","temporalCoverage":"2026","variableMeasured":"bullion sales-tax status"}
    sch=schema([("Home","https://gold-advisor.com/"),("Bullion Tax Tracker",canonical)],
               [("How many states tax gold bullion?",f"As of 2026, about {taxing} states plus Washington, D.C. generally tax investment bullion; {exempt} exempt it and {nostate} have no statewide sales tax."),
                ("Does buying gold for an IRA avoid sales tax?","Gold purchased inside an IRA is handled by your custodian and is not a retail sale; state sales tax mainly affects direct personal purchases.")])
    sch+='<script type="application/ld+json">'+json.dumps(dataset)+'</script>\n'
    body=_shell(prefix,"Bullion Tax Tracker","Live Data \u00b7 2026","U.S. Bullion Sales-Tax Tracker",
        f"How all 50 states tax gold and silver bullion in 2026 \u2014 {taxing} tax it, {exempt} exempt it, {nostate} have no state sales tax.",
        content, footer(prefix))
    return page(title,desc,canonical,prefix,sch,body)

# ---------------------------------------------------------------- llms.txt
def build_llms():
    avg_min=sum(MIN_NUM.values())//len(MIN_NUM); low_min=min(MIN_NUM.values())
    cats={"TAX":0,"EX":0,"NT":0,"PART":0,"VER":0}
    for st in STATES.values(): cats[st["tax"]]+=1
    B="https://gold-advisor.com"
    L=[]
    L.append("# Gold Advisor")
    L.append("")
    L.append("> Independent 2026 reviews and original data comparing U.S. Gold IRA companies on fees, minimums, metals, storage, and reputation. Written by precious-metals analyst Aaron Tal (JPost.com, TipRanks.com).")
    L.append("")
    L.append("## Key data (2026)")
    L.append(f"- Lowest Gold IRA minimum among leading providers: ${low_min:,}")
    L.append(f"- Average Gold IRA minimum (tracked companies): ~${avg_min:,}")
    L.append("- Typical all-in annual fees: $200-$300 (flat-fee custodians)")
    L.append(f"- U.S. states that generally tax investment bullion: {cats['TAX']} plus Washington, D.C.; generally exempt: {cats['EX']}; no statewide sales tax: {cats['NT']}")
    L.append("")
    L.append("## Top 5 Gold IRA companies (ranked)")
    for i,c in enumerate(COMPANIES,1):
        L.append(f"{i}. {c['name']} — {REVIEWS[c['key']]['score']}/10 — {SHORT[c['key']].replace('&amp;','and')} — {B}/gold-ira-companies/{REVIEWS[c['key']]['slug']}-review/")
    L.append("")
    L.append("## Primary pages")
    L.append(f"- [Homepage / full ranking]({B}/)")
    L.append(f"- [Company reviews]({B}/gold-ira-companies/)")
    L.append(f"- [Head-to-head comparisons]({B}/compare/)")
    L.append(f"- [Gold IRA Fee & Minimum Index]({B}/gold-ira-fee-index/)")
    L.append(f"- [U.S. Bullion Sales-Tax Tracker]({B}/bullion-sales-tax-tracker/)")
    L.append(f"- [Guides]({B}/guides/)")
    L.append(f"- [Tools: quiz, fee, rollover & RMD calculators]({B}/tools/)")
    L.append(f"- [Gold IRA scams & how to avoid them]({B}/gold-ira-scams/)")
    L.append(f"- [Rules, regulators & resources]({B}/resources/)")
    L.append(f"- [Methodology]({B}/methodology/)")
    L.append(f"- [About]({B}/about/) · [Author: Aaron Tal]({B}/about/aaron-tal/)")
    L.append(f"- [Buy gold by state]({B}/invest-in-gold/) · [by city]({B}/buy-gold-in/)")
    L.append("")
    L.append("## Notes")
    L.append("- Affiliate disclosure: some outbound company links earn commissions (rel=nofollow sponsored); this does not affect editorial rankings.")
    L.append("- All figures reviewed June 2026 and may change; verify directly. Educational information, not financial, tax, or legal advice.")
    L.append("")
    return "\n".join(L)

# ---------------------------------------------------------------- gold IRA scams
def build_scams():
    prefix="../"
    canonical="https://gold-advisor.com/gold-ira-scams/"
    title="Gold IRA Scams: 9 Red Flags & How to Protect Yourself (2026) | Gold Advisor"
    desc="The most common Gold IRA scams in 2026 \u2014 home-storage myths, overpriced collectible coins, fear-based sales, hidden spreads \u2014 with red flags and how to verify a company before you invest."
    content=(f'<div class="answer"><b>Quick answer:</b> A gold IRA itself is legal and legitimate, but the industry attracts bad actors. The most common scams involve the \u201chome-storage\u201d myth, overpriced collectible coins, fear-based high-pressure sales, and hidden spreads. Below are nine red flags and a checklist to vet any company before you move retirement money.</div>'
     '<p>After a decade reviewing this industry, I\u2019ve seen the same playbooks repeat. None of this means gold IRAs are a scam \u2014 they\u2019re a legitimate, IRS-sanctioned way to hold physical metals for retirement. It means you should know the warning signs before you wire a rollover.</p>'
     '<h2 id="common">9 common gold IRA scams &amp; tactics</h2>'
     '<h3>1. The \u201chome storage\u201d gold IRA myth</h3>'
     '<p>Ads promise you can store IRA gold in a home safe through a \u201ccheckbook LLC.\u201d The IRS has never blessed this, and it can disqualify your entire IRA, triggering taxes and penalties. IRA metals must sit with an approved custodian and depository (IRC \u00a7408(m)).</p>'
     '<h3>2. Overpriced \u201crare\u201d or collectible coins</h3>'
     '<p>The biggest profit center for bad dealers is steering you from low-margin bullion into \u201crare,\u201d \u201cproof,\u201d or \u201ccollectible\u201d numismatic coins at huge markups. Many collectibles aren\u2019t even IRA-eligible, and the premiums can take years to earn back.</p>'
     '<h3>3. Bait-and-switch on bullion</h3>'
     '<p>You\u2019re drawn in by an ad for low-premium bullion, then pressured on the phone into a different, far pricier product \u201cbecause it\u2019s a better deal right now.\u201d</p>'
     '<h3>4. Fear-based, high-pressure selling</h3>'
     '<p>Doomsday scripts \u2014 imminent dollar collapse, \u201cgold confiscation,\u201d one-day-only pricing \u2014 are designed to rush you past due diligence. Legitimate firms let you take your time.</p>'
     '<h3>5. Hidden or excessive spreads</h3>'
     '<p>The real cost is often the spread between buy and sell price, not the advertised \u201cfee.\u201d A 30\u201340% spread can quietly erase years of gains. Always ask for the buy price, the current sell/buyback price, and the spread in writing.</p>'
     '<h3>6. \u201cFree silver\u201d &amp; bonus-metal promotions</h3>'
     '<p>\u201cGet $10,000 in free silver\u201d offers are typically baked into inflated prices elsewhere in the order. Nothing is free; check the all-in math.</p>'
     '<h3>7. Unallocated metal with no audit</h3>'
     '<p>Some schemes sell \u201cunallocated\u201d or \u201cpooled\u201d metal you never actually own in segregated form, with no independent audit. Insist on allocated, segregated storage at a named, insured depository.</p>'
     '<h3>8. Fake reviews &amp; celebrity endorsements</h3>'
     '<p>Paid \u201creviews,\u201d invented award badges, and implied celebrity backing are common. Cross-check ratings on independent platforms and read the actual complaints, not just the star score.</p>'
     '<h3>9. Leasing &amp; \u201cstore-it-for-you\u201d gimmicks</h3>'
     '<p>Arrangements where the dealer \u201cleases\u201d or holds your metal off the books, outside an IRS-approved depository, put your assets and your IRA status at risk.</p>'
     '<h2 id="redflags">Red-flag checklist</h2>'
     '<ul class="checks">'
     '<li>Pressure to \u201cact today\u201d or fear-based scripts about collapse/confiscation</li>'
     '<li>Pushing collectible/proof/\u201crare\u201d coins over standard bullion</li>'
     '<li>Refusal to put buy price, sell price, and spread in writing</li>'
     '<li>Promises of \u201chome storage\u201d or a \u201ccheckbook IRA\u201d for your metals</li>'
     '<li>\u201cFree\u201d metals, vague fees, or no clear total cost</li>'
     '<li>No named, insured, IRS-approved depository</li>'
     '<li>Thin or suspiciously perfect reviews; no complaint history at all</li>'
     '</ul>'
     '<h2 id="verify">How to verify a company before you invest</h2>'
     '<p>This is exactly what our reviews do \u2014 and what you can repeat yourself:</p>'
     '<ul class="checks">'
     '<li>Check ratings <em>and</em> complaints on <a href="https://www.bbb.org/" target="_blank" rel="noopener">BBB</a>, <a href="https://www.checkbca.org/" target="_blank" rel="noopener">BCA</a>, <a href="https://www.trustpilot.com/" target="_blank" rel="noopener">Trustpilot</a>, <a href="https://www.trustlink.org/" target="_blank" rel="noopener">TrustLink</a>, and Google.</li>'
     '<li>Confirm metals are IRA-eligible (gold .995+, silver .999+) and stored at a named depository (e.g., Delaware Depository, Brink\u2019s).</li>'
     '<li>Get the spread and all annual fees in writing before funding.</li>'
     '<li>Make sure there\u2019s a clear, fair buyback policy.</li>'
     '<li>Verify the custodian is a legitimate, regulated trust company.</li>'
     '</ul>'
     '<h2 id="report">What to do if you\u2019ve been scammed</h2>'
     '<p>Act quickly and report it \u2014 reporting also helps regulators build cases:</p>'
     '<ul class="checks">'
     '<li><strong>CFTC</strong> \u2014 <a href="https://www.cftc.gov/LearnAndProtect/metalsfrauds" target="_blank" rel="noopener">precious-metals fraud center</a> &amp; <a href="https://www.cftc.gov/complaint" target="_blank" rel="noopener">file a complaint</a></li>'
     '<li><strong>FTC</strong> \u2014 <a href="https://reportfraud.ftc.gov/" target="_blank" rel="noopener">reportfraud.ftc.gov</a></li>'
     '<li><strong>SEC</strong> (if securities were involved) \u2014 <a href="https://www.sec.gov/tcr" target="_blank" rel="noopener">sec.gov/tcr</a></li>'
     '<li>Your <strong>state attorney general</strong>, the <a href="https://www.bbb.org/" target="_blank" rel="noopener">BBB</a>, and your <a href="https://www.nasaa.org/" target="_blank" rel="noopener">state securities regulator (NASAA)</a></li>'
     '<li>Document everything and consult a licensed attorney</li>'
     '</ul>'
     f'<p>Ready to compare vetted companies? See our <a href="{prefix}gold-ira-companies/index.html">reviewed top five</a> and the <a href="{prefix}methodology/index.html">verified-review methodology</a> behind the rankings.</p>'
     '<p style="font-size:.84rem;color:var(--muted-2)">Educational information, not financial, tax, or legal advice. Reviewed <span class="ga-now">June 2026</span>.</p>' + resources_block(prefix, f'<a href="{prefix}gold-ira-companies/index.html">Vetted top 5</a> &middot; <a href="{prefix}methodology/index.html">Our methodology</a> &middot; <a href="{prefix}tools/gold-ira-quiz/index.html">Company quiz</a>'))
    faqs=[("Is a gold IRA a scam?","No. A gold IRA is a legitimate, IRS-sanctioned retirement account for physical metals. The risk comes from specific dishonest dealers and tactics, not the account type itself."),
          ("What is the most common gold IRA scam?","Steering buyers from low-margin bullion into overpriced \u201crare\u201d or collectible coins, and the false \u201chome-storage\u201d gold IRA, are the two most common."),
          ("How do I check if a gold IRA company is legitimate?","Review ratings and complaints across BBB, BCA, Trustpilot, TrustLink, and Google; confirm IRA-eligible metals and a named depository; and get the spread and fees in writing.")]
    sch=schema([("Home","https://gold-advisor.com/"),("Gold IRA Scams",canonical)],faqs)
    sch+='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":"Gold IRA Scams: Red Flags & How to Protect Yourself","author":AUTHOR_LD,"publisher":{"@type":"Organization","name":"Gold Advisor"},"datePublished":"2026-06-01","dateModified":"2026-06-07"})+'</script>\n'
    body=_shell(prefix,"Gold IRA Scams","Investor Protection","Gold IRA Scams &amp; How to Avoid Them",
        "A gold IRA is legitimate \u2014 but the industry attracts bad actors. Here are the nine most common scams, the red flags, and how to vet any company.",
        content, footer(prefix), author=True,
        extra_style=".checks{list-style:none;margin:6px 0 4px;padding:0}.checks li{position:relative;padding:7px 0 7px 28px;color:var(--ink);border-bottom:1px solid var(--line)}.checks li::before{content:'\\2713';position:absolute;left:0;top:7px;color:var(--cta);font-weight:800}")
    return page(title,desc,canonical,prefix,sch,body)

# ---------------------------------------------------------------- rollover growth calculator
def build_rollover_calc():
    prefix="../../"
    canonical="https://gold-advisor.com/tools/gold-ira-rollover-calculator/"
    title="Gold IRA Rollover Calculator (2026): Project Your Balance | Gold Advisor"
    desc="Free Gold IRA rollover calculator: project the future value of a rollover plus annual contributions over time at an assumed growth rate. Educational, not investment advice."
    calc='''<div class="answer"><b>How to use it:</b> enter what you'd roll over, any yearly contributions, a time horizon, and an assumed annual return. The tool compounds it so you can see contributions vs growth. Gold returns aren't guaranteed \u2014 this is an illustration, not a forecast.</div>
<div class="calc">
 <label>Amount to roll over ($)<input id="amt" type="number" value="50000" min="0" step="1000"></label>
 <label>Annual contribution ($)<input id="contrib" type="number" value="7500" min="0" step="500"></label>
 <label>Years<input id="yrs" type="number" value="20" min="1" max="50"></label>
 <label>Assumed annual return (%)<input id="ret" type="number" value="5" min="0" max="30" step="0.5"></label>
 <div class="calc-out" id="out"></div>
</div>
<script>
function id(x){return document.getElementById(x);}
function fmt(n){return "$"+Math.round(n).toLocaleString();}
function calc(){
 var p=+id("amt").value||0,c=+id("contrib").value||0,y=+id("yrs").value||0,r=(+id("ret").value||0)/100;
 var fv=(r===0)?(p+c*y):(p*Math.pow(1+r,y)+c*((Math.pow(1+r,y)-1)/r));
 var put=p+c*y, growth=fv-put;
 id("out").innerHTML='<div class="cr"><span>Total contributed</span><b>'+fmt(put)+'</b></div>'
  +'<div class="cr"><span>Projected growth</span><b>'+fmt(growth)+'</b></div>'
  +'<div class="cr big"><span>Projected balance after '+y+' yrs</span><b>'+fmt(fv)+'</b></div>';
}
["amt","contrib","yrs","ret"].forEach(function(k){id(k).addEventListener("input",calc);});
calc();
</script>
<p style="font-size:.86rem;color:var(--muted-2);margin-top:14px">Illustration only \u2014 not a forecast or investment advice. Gold can rise or fall; past performance doesn't predict future results. 2026 IRA contribution limits: $7,500, or $8,600 if you're 50 or older. Verify limits and rollover rules with your custodian or a tax professional.</p>'''
    cstyle=(".calc{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:24px;box-shadow:var(--shadow);max-width:560px;display:grid;gap:14px}"
     ".calc label{display:flex;flex-direction:column;gap:6px;font-weight:600;color:var(--navy);font-size:.9rem}"
     ".calc input{padding:11px 13px;border:1px solid var(--line);border-radius:9px;font:inherit;font-size:1rem}"
     ".calc-out{margin-top:6px;border-top:1px solid var(--line);padding-top:14px;display:grid;gap:8px}"
     ".cr{display:flex;justify-content:space-between;align-items:center;font-size:.95rem;color:var(--ink)}.cr b{font-family:'Fraunces',serif;font-size:1.1rem;color:var(--navy)}"
     ".cr.big{background:#e9f7ef;border-radius:10px;padding:12px 14px;margin-top:4px}.cr.big b{color:#17834a;font-size:1.4rem}")
    sch=schema([("Home","https://gold-advisor.com/"),("Tools","https://gold-advisor.com/tools/"),("Rollover Calculator",canonical)],
               [("How much can I contribute to a gold IRA in 2026?","The 2026 limit is $7,500, or $8,600 if you are 50 or older. Rollovers from an existing 401(k) or IRA are separate and not capped by the annual limit.")])
    body=_shell(prefix,"Rollover Calculator","Interactive Tool","Gold IRA Rollover Calculator",
        "Project a rollover plus future contributions over time at an assumed growth rate.",
        calc, footer(prefix), extra_style=cstyle)
    return page(title,desc,canonical,prefix,sch,body)

# ---------------------------------------------------------------- RMD calculator
def build_rmd_calc():
    prefix="../../"
    canonical="https://gold-advisor.com/tools/gold-ira-rmd-calculator/"
    title="Gold IRA RMD Calculator (2026, IRS Uniform Lifetime Table) | Gold Advisor"
    desc="Estimate your Required Minimum Distribution for a traditional gold IRA using the IRS Uniform Lifetime Table. RMDs begin at age 73."
    calc='''<div class="answer"><b>What this does:</b> traditional gold IRAs require minimum withdrawals starting at age 73. Enter last year's account value and your age to estimate this year's RMD using the IRS Uniform Lifetime Table. Roth IRAs have no RMDs during your lifetime.</div>
<div class="calc">
 <label>Account value on Dec 31 last year ($)<input id="val" type="number" value="250000" min="0" step="1000"></label>
 <label>Your age this year<input id="age" type="number" value="73" min="50" max="115"></label>
 <div class="calc-out" id="out"></div>
</div>
<script>
function id(x){return document.getElementById(x);}
function fmt(n){return "$"+Math.round(n).toLocaleString();}
var ULT={73:26.5,74:25.5,75:24.6,76:23.7,77:22.9,78:22.0,79:21.1,80:20.2,81:19.4,82:18.5,83:17.7,84:16.8,85:16.0,86:15.2,87:14.4,88:13.7,89:12.9,90:12.2,91:11.5,92:10.8,93:10.1,94:9.5,95:8.9,96:8.4,97:7.8,98:7.3,99:6.8,100:6.4,101:6.0,102:5.6,103:5.2,104:4.9,105:4.6};
function calc(){
 var v=+id("val").value||0, age=Math.floor(+id("age").value||0), out=id("out");
 if(age<73){ out.innerHTML='<div class="cr big"><span>No RMD required yet</span><b>Begins at age 73</b></div>'; return; }
 var f=ULT[age]; if(!f){ f=ULT[105]; }
 var rmd=v/f;
 out.innerHTML='<div class="cr"><span>IRS distribution factor (age '+age+')</span><b>'+f+'</b></div>'
  +'<div class="cr big"><span>Estimated RMD this year</span><b>'+fmt(rmd)+'</b></div>';
}
["val","age"].forEach(function(k){id(k).addEventListener("input",calc);});
calc();
</script>
<p style="font-size:.86rem;color:var(--muted-2);margin-top:14px">Estimate only, based on the IRS Uniform Lifetime Table (most account holders). A different table applies if your sole beneficiary is a spouse more than 10 years younger. RMDs begin at age 73; missing one carries a penalty. Confirm with your custodian or a tax professional.</p>'''
    cstyle=(".calc{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:24px;box-shadow:var(--shadow);max-width:560px;display:grid;gap:14px}"
     ".calc label{display:flex;flex-direction:column;gap:6px;font-weight:600;color:var(--navy);font-size:.9rem}"
     ".calc input{padding:11px 13px;border:1px solid var(--line);border-radius:9px;font:inherit;font-size:1rem}"
     ".calc-out{margin-top:6px;border-top:1px solid var(--line);padding-top:14px;display:grid;gap:8px}"
     ".cr{display:flex;justify-content:space-between;align-items:center;font-size:.95rem;color:var(--ink)}.cr b{font-family:'Fraunces',serif;font-size:1.1rem;color:var(--navy)}"
     ".cr.big{background:#e9f7ef;border-radius:10px;padding:12px 14px;margin-top:4px}.cr.big b{color:#17834a;font-size:1.4rem}")
    sch=schema([("Home","https://gold-advisor.com/"),("Tools","https://gold-advisor.com/tools/"),("RMD Calculator",canonical)],
               [("When do gold IRA RMDs start?","Required minimum distributions from a traditional gold IRA begin at age 73. Roth IRAs have no RMDs during the owner's lifetime."),
                ("How is the RMD calculated?","Divide the prior year-end account value by the IRS Uniform Lifetime Table factor for your age. For example, at 73 the factor is 26.5.")])
    body=_shell(prefix,"RMD Calculator","Interactive Tool","Gold IRA RMD Calculator",
        "Estimate your required minimum distribution using the IRS Uniform Lifetime Table.",
        calc, footer(prefix), extra_style=cstyle)
    return page(title,desc,canonical,prefix,sch,body)


