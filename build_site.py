#!/usr/bin/env python3
"""
Gold-Advisor.com — Full Site Builder (v4)
=========================================
Generates the whole site into ./site :
  - 50 state pages      /invest-in-gold/<state>/index.html
  - 100 city pages      /buy-gold-in/<city-st>/index.html
  - state hub           /invest-in-gold/index.html
  - city hub            /buy-gold-in/index.html
  - sitemap.xml, robots.txt

Design notes
------------
* INTERNAL LINKS ARE RELATIVE and end in /index.html, so every link works when
  the zip is opened locally (file://) AND when deployed. (On a live server you
  can switch to clean folder URLs — see seo-strategy.md.)
* Real brand logos + the hero image are embedded as data URIs (self-contained).
* Each page carries a randomized footer (20 states + 20 cities, reshuffled on
  every visit) plus JSON-LD (BreadcrumbList + FAQPage + ItemList).
* The state-specific legal variable is BULLION SALES TAX (researched, dated,
  and flagged "verify"). Federal Gold-IRA rules are uniform and stated once.
  Cities inherit their state's status and note possible local tax.
"""

import os, base64, json

ASSETS = "/mnt/user-data/outputs/gold-advisor/assets"

def datauri(path, mime):
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

LOGO_FILES = {"augusta":"augusta.png","goldco":"goldco.png","priority":"priority.svg","ahg":"american-hartford.png","birch":"birch.png"}

# --------------------------------------------------------------------------- #
COMPANIES = [
    dict(rank=1, name="Augusta Precious Metals", tagline="Best overall — education &amp; transparency",
         score="9.8", stars=5, top=True, chip="dark", key="augusta",
         feats=["Transparent pricing", "Dedicated specialist", "Education-first", "Lifetime support"]),
    dict(rank=2, name="Goldco", tagline="Best for 401(k) &amp; IRA rollovers",
         score="9.6", stars=5, top=False, chip="light", key="goldco",
         feats=["Rollover specialists", "Wide selection", "Buyback program", "Responsive support"]),
    dict(rank=3, name="Priority Gold", tagline="Best for low minimums",
         score="9.4", stars=4, top=False, chip="dark", key="priority",
         feats=["Lower entry minimum", "Price-match offer", "Secure storage", "Simple setup"]),
    dict(rank=4, name="American Hartford Gold", tagline="Best for first-time buyers",
         score="9.3", stars=4, top=False, chip="light", key="ahg",
         feats=["No-minimum option", "Family-owned", "Promotional offers", "Buyback commitment"]),
    dict(rank=5, name="Birch Gold Group", tagline="Best for metals variety",
         score="9.1", stars=4, top=False, chip="dark", key="birch",
         feats=["Broad selection", "Long track record", "Fee transparency", "Strong education"]),
]
SLUGS={"augusta":"augusta-precious-metals","goldco":"goldco","priority":"priority-gold","ahg":"american-hartford-gold","birch":"birch-gold-group"}
for _c in COMPANIES: _c["slug"]=SLUGS[_c["key"]]

AUTHOR = {
 "name":"Aaron Tal","role":"Precious Metals Analyst",
 "bio":"Aaron Tal has worked in financial markets \u2014 with a focus on gold and silver \u2014 for over 10 years. He covers precious-metals news and works as a Gold IRA analyst at Investing.com, and authors precious-metals sections for The Jerusalem Post (JPost.com) and TipRanks.com. He has spent more than a decade researching Gold IRA companies and writing reviews that help investors make better-informed decisions.",
}
AUTHOR_LD = {"@type":"Person","name":"Aaron Tal","jobTitle":"Precious Metals Analyst","description":AUTHOR["bio"],"url":"https://gold-advisor.com/about/aaron-tal/","sameAs":["https://www.jpost.com/","https://www.tipranks.com/","https://www.investing.com/"]}

def render_companies(prefix=""):
    out = []
    for c in COMPANIES:
        stars = "★" * c["stars"] + "☆" * (5 - c["stars"])
        ribbon = '<span class="ribbon">★ Best Overall</span>' if c["top"] else ""
        feats = "".join(f"<li>{f}</li>" for f in c["feats"])
        phone = '\n          <a class="cta-phone" href="tel:+18449172904">\U0001F4DE 844-917-2904</a>' if c["key"]=="augusta" else ""
        out.append(f"""      <article class="firm{' top' if c['top'] else ''}">
        {ribbon}
        <div class="rankcol"><div class="rankno">{c['rank']}</div><div class="rl">Rank</div></div>
        <div class="logo-slot {c['chip']}"><img data-logo="{c['key']}" src="{prefix}assets/logos/{LOGO_FILES[c['key']]}" alt="{c['name'].replace('&amp;','&')} logo" loading="lazy"></div>
        <div>
          <h3>{c['name']}</h3>
          <div class="tagline">{c['tagline']}</div>
          <div class="rating-row"><span class="stars">{stars}</span><span class="rtext">{'Excellent' if c['stars']==5 else 'Great'}</span></div>
          <ul class="feats">{feats}</ul>
        </div>
        <div class="right-col">
          <div class="scorebadge"><b>{c['score']}</b><span class="out">/10</span></div>
          <a href="/visit/{c['slug']}/" class="go primary" rel="nofollow sponsored" data-aff="{c['key']}">Visit Site →</a>{phone}
          <a href="{prefix}gold-ira-companies/{c['slug']}-review/index.html" class="review-link">Read review</a>
        </div>
      </article>""")
    return "\n".join(out)

# --------------------------------------------------------------------------- #
S = lambda **k: k
STATES = {
 "alabama": S(name="Alabama",abbr="AL",nick="the Yellowhammer State",region="the Deep South",metros=["Birmingham","Montgomery","Huntsville"],tax="EX",lt=True,extra="Alabama's exemption applies to refined bullion meeting an 80% purity floor — one of the more inclusive standards nationally."),
 "alaska": S(name="Alaska",abbr="AK",nick="the Last Frontier",region="the Far North",metros=["Anchorage","Fairbanks","Juneau"],tax="NT",extra="Alaska has no statewide sales tax, but many boroughs and cities levy local sales tax, so a local charge can still apply."),
 "arizona": S(name="Arizona",abbr="AZ",nick="the Grand Canyon State",region="the Southwest",metros=["Phoenix","Tucson","Mesa"],tax="EX",lt=True),
 "arkansas": S(name="Arkansas",abbr="AR",nick="the Natural State",region="the South",metros=["Little Rock","Fayetteville","Fort Smith"],tax="EX"),
 "california": S(name="California",abbr="CA",nick="the Golden State",region="the West Coast",metros=["Los Angeles","San Diego","San Jose"],tax="PART",partnote="California exempts qualifying bullion and monetized-coin purchases above a set transaction threshold, but smaller purchases below that threshold can be taxable."),
 "colorado": S(name="Colorado",abbr="CO",nick="the Centennial State",region="the Mountain West",metros=["Denver","Colorado Springs","Aurora"],tax="EX",lt=True),
 "connecticut": S(name="Connecticut",abbr="CT",nick="the Constitution State",region="New England",metros=["Bridgeport","New Haven","Stamford"],tax="PART",partnote="Connecticut has exempted bullion and investment-coin purchases above a dollar threshold, with a broader full exemption scheduled for 2027 — confirm what qualifies today."),
 "delaware": S(name="Delaware",abbr="DE",nick="the First State",region="the Mid-Atlantic",metros=["Wilmington","Dover","Newark"],tax="NT",extra="Delaware has no sales tax of any kind and no local sales tax."),
 "florida": S(name="Florida",abbr="FL",nick="the Sunshine State",region="the Southeast",metros=["Jacksonville","Miami","Tampa"],tax="EX",lt=True,extra="Florida removed its earlier purchase threshold in 2025 and has moved to recognize gold and silver as legal tender."),
 "georgia": S(name="Georgia",abbr="GA",nick="the Peach State",region="the Southeast",metros=["Atlanta","Augusta","Savannah"],tax="EX"),
 "hawaii": S(name="Hawaii",abbr="HI",nick="the Aloha State",region="the Pacific",metros=["Honolulu","Hilo","Kailua"],tax="TAX",extra="Hawaii applies its general excise tax broadly, and precious-metals purchases are generally not exempt."),
 "idaho": S(name="Idaho",abbr="ID",nick="the Gem State",region="the Mountain West",metros=["Boise","Meridian","Nampa"],tax="EX"),
 "illinois": S(name="Illinois",abbr="IL",nick="the Prairie State",region="the Midwest",metros=["Chicago","Aurora","Naperville"],tax="EX"),
 "indiana": S(name="Indiana",abbr="IN",nick="the Hoosier State",region="the Midwest",metros=["Indianapolis","Fort Wayne","Evansville"],tax="EX"),
 "iowa": S(name="Iowa",abbr="IA",nick="the Hawkeye State",region="the Midwest",metros=["Des Moines","Cedar Rapids","Davenport"],tax="EX"),
 "kansas": S(name="Kansas",abbr="KS",nick="the Sunflower State",region="the Great Plains",metros=["Wichita","Overland Park","Kansas City"],tax="EX",lt=True),
 "kentucky": S(name="Kentucky",abbr="KY",nick="the Bluegrass State",region="the Upper South",metros=["Louisville","Lexington","Bowling Green"],tax="EX",extra="Kentucky enacted a bullion exemption in recent years after earlier back-and-forth, so confirm the current text still applies."),
 "louisiana": S(name="Louisiana",abbr="LA",nick="the Pelican State",region="the Deep South",metros=["New Orleans","Baton Rouge","Shreveport"],tax="EX",lt=True),
 "maine": S(name="Maine",abbr="ME",nick="the Pine Tree State",region="New England",metros=["Portland","Lewiston","Bangor"],tax="TAX"),
 "maryland": S(name="Maryland",abbr="MD",nick="the Old Line State",region="the Mid-Atlantic",metros=["Baltimore","Columbia","Silver Spring"],tax="TAX",extra="Maryland repealed its earlier bullion exemption in 2025 and now applies its standard sales tax to precious-metals purchases."),
 "massachusetts": S(name="Massachusetts",abbr="MA",nick="the Bay State",region="New England",metros=["Boston","Worcester","Springfield"],tax="PART",partnote="Massachusetts has generally exempted bullion and monetized-coin purchases above a dollar threshold, with smaller purchases potentially taxable."),
 "michigan": S(name="Michigan",abbr="MI",nick="the Great Lakes State",region="the Midwest",metros=["Detroit","Grand Rapids","Warren"],tax="EX",extra="Michigan's exemption generally hinges on a purity threshold, so standard investment-grade bullion qualifies while novelty products may not."),
 "minnesota": S(name="Minnesota",abbr="MN",nick="the North Star State",region="the Upper Midwest",metros=["Minneapolis","Saint Paul","Rochester"],tax="EX",extra="Minnesota applies one of the stricter purity standards in the country, so confirm a given product qualifies."),
 "mississippi": S(name="Mississippi",abbr="MS",nick="the Magnolia State",region="the Deep South",metros=["Jackson","Gulfport","Southaven"],tax="EX",extra="Mississippi enacted its precious-metals exemption in 2023."),
 "missouri": S(name="Missouri",abbr="MO",nick="the Show-Me State",region="the Midwest",metros=["Kansas City","St. Louis","Springfield"],tax="EX",lt=True),
 "montana": S(name="Montana",abbr="MT",nick="the Treasure State",region="the Mountain West",metros=["Billings","Missoula","Bozeman"],tax="NT",extra="Montana has no statewide sales tax."),
 "nebraska": S(name="Nebraska",abbr="NE",nick="the Cornhusker State",region="the Great Plains",metros=["Omaha","Lincoln","Bellevue"],tax="EX"),
 "nevada": S(name="Nevada",abbr="NV",nick="the Silver State",region="the Mountain West",metros=["Las Vegas","Henderson","Reno"],tax="EX",extra="Fittingly for the Silver State, Nevada is a generally friendly market for precious-metals buyers."),
 "new-hampshire": S(name="New Hampshire",abbr="NH",nick="the Granite State",region="New England",metros=["Manchester","Nashua","Concord"],tax="NT",extra="New Hampshire levies no statewide sales tax."),
 "new-jersey": S(name="New Jersey",abbr="NJ",nick="the Garden State",region="the Mid-Atlantic",metros=["Newark","Jersey City","Paterson"],tax="VER",extra="New Jersey's treatment of investment bullion changed recently and sources don't fully agree on the current status, so confirming before you buy is especially important."),
 "new-mexico": S(name="New Mexico",abbr="NM",nick="the Land of Enchantment",region="the Southwest",metros=["Albuquerque","Las Cruces","Santa Fe"],tax="TAX",extra="New Mexico applies a gross receipts tax that generally reaches precious-metals purchases, with the rate varying by location."),
 "new-york": S(name="New York",abbr="NY",nick="the Empire State",region="the Northeast",metros=["New York City","Buffalo","Rochester"],tax="PART",partnote="New York generally exempts bullion and investment-coin purchases above a dollar threshold, with smaller purchases potentially taxable.",extra="New York City is the historic centre of U.S. precious-metals trade."),
 "north-carolina": S(name="North Carolina",abbr="NC",nick="the Tar Heel State",region="the Southeast",metros=["Charlotte","Raleigh","Greensboro"],tax="EX",extra="North Carolina expanded its exemption in 2025 to cover additional forms of precious metals."),
 "north-dakota": S(name="North Dakota",abbr="ND",nick="the Peace Garden State",region="the Upper Midwest",metros=["Fargo","Bismarck","Grand Forks"],tax="EX"),
 "ohio": S(name="Ohio",abbr="OH",nick="the Buckeye State",region="the Midwest",metros=["Columbus","Cleveland","Cincinnati"],tax="EX",extra="Ohio restored its bullion exemption in 2021."),
 "oklahoma": S(name="Oklahoma",abbr="OK",nick="the Sooner State",region="the South Central U.S.",metros=["Oklahoma City","Tulsa","Norman"],tax="EX",lt=True),
 "oregon": S(name="Oregon",abbr="OR",nick="the Beaver State",region="the Pacific Northwest",metros=["Portland","Salem","Eugene"],tax="NT",extra="Oregon has no statewide sales tax, a reason some out-of-state buyers store metals here."),
 "pennsylvania": S(name="Pennsylvania",abbr="PA",nick="the Keystone State",region="the Mid-Atlantic",metros=["Philadelphia","Pittsburgh","Allentown"],tax="EX"),
 "rhode-island": S(name="Rhode Island",abbr="RI",nick="the Ocean State",region="New England",metros=["Providence","Cranston","Warwick"],tax="EX"),
 "south-carolina": S(name="South Carolina",abbr="SC",nick="the Palmetto State",region="the Southeast",metros=["Charleston","Columbia","North Charleston"],tax="EX"),
 "south-dakota": S(name="South Dakota",abbr="SD",nick="the Mount Rushmore State",region="the Upper Midwest",metros=["Sioux Falls","Rapid City","Aberdeen"],tax="EX"),
 "tennessee": S(name="Tennessee",abbr="TN",nick="the Volunteer State",region="the South",metros=["Nashville","Memphis","Knoxville"],tax="EX",extra="Tennessee eliminated sales tax on precious metals in 2022."),
 "texas": S(name="Texas",abbr="TX",nick="the Lone Star State",region="the South Central U.S.",metros=["Houston","San Antonio","Dallas"],tax="EX",lt=True,extra="Texas operates the state-chartered Texas Bullion Depository — though for a Gold IRA, metals must still be held by your custodian's IRS-approved depository."),
 "utah": S(name="Utah",abbr="UT",nick="the Beehive State",region="the Mountain West",metros=["Salt Lake City","West Valley City","Provo"],tax="EX",lt=True,extra="Utah was an early mover on sound-money policy, recognizing certain gold and silver coins as legal tender."),
 "vermont": S(name="Vermont",abbr="VT",nick="the Green Mountain State",region="New England",metros=["Burlington","South Burlington","Rutland"],tax="TAX",extra="Vermont has discussed but not fully enacted a bullion exemption, so sales tax generally applies."),
 "virginia": S(name="Virginia",abbr="VA",nick="the Old Dominion",region="the Mid-Atlantic",metros=["Virginia Beach","Chesapeake","Norfolk"],tax="EX",extra="Virginia's bullion exemption has carried a sunset date in the past, so confirm it is still in force for the current year."),
 "washington": S(name="Washington",abbr="WA",nick="the Evergreen State",region="the Pacific Northwest",metros=["Seattle","Spokane","Tacoma"],tax="TAX",extra="Washington repealed its long-standing bullion exemption effective January 1, 2026, so purchases now generally face state and local sales tax."),
 "west-virginia": S(name="West Virginia",abbr="WV",nick="the Mountain State",region="the Appalachian South",metros=["Charleston","Huntington","Morgantown"],tax="EX",lt=True),
 "wisconsin": S(name="Wisconsin",abbr="WI",nick="the Badger State",region="the Upper Midwest",metros=["Milwaukee","Madison","Green Bay"],tax="EX",extra="Wisconsin enacted its exemption in 2024, among the most recent states to do so."),
 "wyoming": S(name="Wyoming",abbr="WY",nick="the Equality State",region="the Mountain West",metros=["Cheyenne","Casper","Laramie"],tax="EX",lt=True),
}
ABBR = {st["abbr"]: (slug, st) for slug, st in STATES.items()}
# District of Columbia (a top city, not a state) — supplemental
DC = S(name="the District of Columbia", abbr="DC", region="the Mid-Atlantic", tax="TAX",
       extra="Washington, D.C. applies its sales tax to precious-metals purchases.")

# Top 100 U.S. cities (name, state-abbr) — ordering approximate; state mapping is the point.
CITIES = [
 ("New York","NY"),("Los Angeles","CA"),("Chicago","IL"),("Houston","TX"),("Phoenix","AZ"),
 ("Philadelphia","PA"),("San Antonio","TX"),("San Diego","CA"),("Dallas","TX"),("San Jose","CA"),
 ("Austin","TX"),("Jacksonville","FL"),("Fort Worth","TX"),("Columbus","OH"),("Charlotte","NC"),
 ("San Francisco","CA"),("Indianapolis","IN"),("Seattle","WA"),("Denver","CO"),("Washington","DC"),
 ("Boston","MA"),("El Paso","TX"),("Nashville","TN"),("Detroit","MI"),("Oklahoma City","OK"),
 ("Portland","OR"),("Las Vegas","NV"),("Memphis","TN"),("Louisville","KY"),("Baltimore","MD"),
 ("Milwaukee","WI"),("Albuquerque","NM"),("Tucson","AZ"),("Fresno","CA"),("Sacramento","CA"),
 ("Mesa","AZ"),("Kansas City","MO"),("Atlanta","GA"),("Omaha","NE"),("Colorado Springs","CO"),
 ("Raleigh","NC"),("Long Beach","CA"),("Virginia Beach","VA"),("Miami","FL"),("Oakland","CA"),
 ("Minneapolis","MN"),("Tulsa","OK"),("Bakersfield","CA"),("Wichita","KS"),("Arlington","TX"),
 ("Aurora","CO"),("Tampa","FL"),("New Orleans","LA"),("Cleveland","OH"),("Honolulu","HI"),
 ("Anaheim","CA"),("Lexington","KY"),("Stockton","CA"),("Corpus Christi","TX"),("Henderson","NV"),
 ("Riverside","CA"),("Newark","NJ"),("Saint Paul","MN"),("Santa Ana","CA"),("Cincinnati","OH"),
 ("Irvine","CA"),("Orlando","FL"),("Pittsburgh","PA"),("St. Louis","MO"),("Greensboro","NC"),
 ("Jersey City","NJ"),("Anchorage","AK"),("Lincoln","NE"),("Plano","TX"),("Durham","NC"),
 ("Buffalo","NY"),("Chandler","AZ"),("Chula Vista","CA"),("Toledo","OH"),("Madison","WI"),
 ("Gilbert","AZ"),("Reno","NV"),("Fort Wayne","IN"),("North Las Vegas","NV"),("St. Petersburg","FL"),
 ("Lubbock","TX"),("Irving","TX"),("Laredo","TX"),("Winston-Salem","NC"),("Chesapeake","VA"),
 ("Glendale","AZ"),("Garland","TX"),("Scottsdale","AZ"),("Norfolk","VA"),("Boise","ID"),
 ("Fremont","CA"),("Spokane","WA"),("Baton Rouge","LA"),("Richmond","VA"),("Hialeah","FL"),
]

def city_slug(name, abbr):
    s = name.lower().replace(".", "").replace("'", "").replace(" ", "-")
    return f"{s}-{abbr.lower()}"

# --------------------------------------------------------------------------- #
def tax_label(t):
    return {"EX":"Generally exempt","NT":"No statewide sales tax","TAX":"Generally taxable",
            "PART":"Partly exempt (threshold)","VER":"Recently changed — verify"}[t]

def tax_sentences(d):
    name=d["name"]; t=d["tax"]
    if t=="NT": s=f"{name} levies no statewide sales tax, so precious-metals purchases are generally free of state sales tax by default."
    elif t=="EX": s=f"As of mid-2026, {name} generally exempts investment-grade gold and silver bullion from sales tax. Purity or product conditions can apply, so not every item automatically qualifies."
    elif t=="TAX": s=f"As of mid-2026, {name} generally applies its sales tax to precious-metals bullion purchases."
    elif t=="PART": s=d.get("partnote", f"{name} applies sales tax to some precious-metals purchases depending on transaction size or product type.")
    else: s=f"{name}'s sales-tax treatment of bullion is in flux."
    if d.get("extra"): s+=" "+d["extra"]
    if d.get("lt") and t not in ("TAX","VER"): s+=f" {name} also recognizes gold and silver as legal tender."
    return s

# --------------------------------------------------------------------------- #
# Randomized footer (20 states + 20 cities, reshuffled each visit) + JSON arrays
STATES_JS = json.dumps([[st["name"], slug] for slug, st in STATES.items()])
CITIES_JS = json.dumps([[f"{n}, {a}", city_slug(n, a)] for n, a in CITIES])

def footer(prefix):
    guide_links="".join(f'<a href="{prefix}guides/{s}/index.html">{GUIDES[s]["navlabel"]}</a>' for s in GUIDE_ORDER)
    return f"""<footer>
  <div class="wrap">
    <div class="foot-cols">
      <div class="fcol brand">
        <a href="{prefix}index.html" class="flogo"><span class="mark">Au</span>Gold&nbsp;Advisor</a>
        <p>Independent education on buying physical gold and precious-metals retirement accounts.</p>
      </div>
      <div class="fcol"><h5>Popular states</h5><div id="rnd-states" class="rndlinks"></div></div>
      <div class="fcol"><h5>Popular cities</h5><div id="rnd-cities" class="rndlinks"></div></div>
      <div class="fcol"><h5>Browse</h5>
        <a href="{prefix}invest-in-gold/index.html">All 50 states</a>
        <a href="{prefix}buy-gold-in/index.html">All cities</a>
        <a href="{prefix}index.html#rankings">Compare companies</a>
        <a href="{prefix}compare/index.html">Compare head-to-head</a>
        <a href="{prefix}tools/index.html">Tools &amp; calculators</a>
        <a href="{prefix}gold-ira-fee-index/index.html">Gold IRA fee index</a>
        <a href="{prefix}bullion-sales-tax-tracker/index.html">Bullion tax tracker</a>
        <a href="{prefix}about/index.html">About &amp; methodology</a>
        <a href="{prefix}gold-ira-scams/index.html">Gold IRA scams</a>
        <a href="{prefix}resources/index.html">Rules &amp; resources</a>
      </div>
      <div class="fcol"><h5>Tools &amp; calculators</h5>
        <a href="{prefix}tools/gold-ira-quiz/index.html">Company match quiz</a>
        <a href="{prefix}tools/gold-ira-fee-calculator/index.html">Fee calculator</a>
        <a href="{prefix}tools/gold-ira-rollover-calculator/index.html">Rollover calculator</a>
        <a href="{prefix}tools/gold-ira-rmd-calculator/index.html">RMD calculator</a>
        <a href="{prefix}gold-price-widget/index.html">Gold price widget</a>
      </div>
    </div>
    <div class="foot-guides"><h5>Gold IRA guides</h5><div class="guidelinks">{guide_links}</div></div>
    <p class="disclaimer"><strong>Disclosure.</strong> Gold Advisor provides general educational information only and is <strong>not</strong> a licensed financial, tax, investment, or legal advisor. Nothing here is personalized advice. Companies compensate us through affiliate links, which keeps our service free and may affect which companies appear; it does not change our editorial assessments. Precious-metals investing carries risk including loss of principal. State bullion tax rules change frequently — verify current figures with the relevant state authority and the IRS before acting.</p>
    <p class="flegal"><a href="{prefix}contact/index.html">Contact</a> &middot; <a href="{prefix}privacy-policy/index.html">Privacy Policy</a> &middot; <a href="{prefix}terms-of-use/index.html">Terms of Use</a></p>
    <p class="copy">© <span class="ga-year">2026</span> Gold-Advisor.com. All rights reserved.</p>
  </div>
  <script>
  (function(){{
    var P="{prefix}";
    var STATES={STATES_JS};
    var CITIES={CITIES_JS};
    function pick(a,n){{a=a.slice();for(var i=a.length-1;i>0;i--){{var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}}return a.slice(0,n);}}
    function fill(id,items,base){{var el=document.getElementById(id);if(!el)return;el.innerHTML=items.map(function(x){{return '<a href="'+P+base+x[1]+'/index.html">'+x[0]+'</a>';}}).join('');}}
    fill('rnd-states',pick(STATES,20),'invest-in-gold/');
    fill('rnd-cities',pick(CITIES,20),'buy-gold-in/');
  }})();
  </script>
  <div id="ga-pop" class="ga-pop" hidden>
    <div class="ga-pop-box">
      <button class="ga-pop-x" aria-label="Close">&times;</button>
      <div class="ga-pop-k">Free 2026 Guide</div>
      <h3>Discover the Best Gold IRA Company</h3>
      <p>Get the free 2026 Gold IRA Guide from our #1&#8209;rated company and learn how to protect your retirement with physical gold.</p>
      <a class="ga-pop-cta" data-aff="augusta" rel="nofollow sponsored" href="/visit/augusta-precious-metals/">Download the Free Guide &rarr;</a>
      <div class="ga-pop-fine">No cost &middot; From our top&#8209;rated provider</div>
    </div>
  </div>
  <script>
  (function(){{
   var KEY="gaPopShown",shown=false,pop=document.getElementById("ga-pop");
   try{{if(sessionStorage.getItem(KEY))shown=true;}}catch(e){{}}
   function show(){{if(shown||!pop)return;shown=true;pop.hidden=false;try{{sessionStorage.setItem(KEY,"1");}}catch(e){{}}}}
   function hide(){{if(pop)pop.hidden=true;}}
   document.addEventListener("mouseout",function(e){{if(!e.relatedTarget&&e.clientY<=0)show();}});
   var deep=false;window.addEventListener("scroll",function(){{var h=document.documentElement;var p=h.scrollTop/((h.scrollHeight-h.clientHeight)||1);if(p>0.5)deep=true;if(deep&&p<0.12)show();}},{{passive:true}});
   if(pop){{pop.addEventListener("click",function(e){{if(e.target===pop)hide();}});var x=pop.querySelector(".ga-pop-x");if(x)x.addEventListener("click",hide);}}
  }})();
  </script>
  <script>
  (function(){{
   var M=["January","February","March","April","May","June","July","August","September","October","November","December"];
   var d=new Date(),now=M[d.getMonth()]+" "+d.getFullYear(),Y=d.getFullYear();
   var ns=document.getElementsByClassName("ga-now");for(var i=0;i<ns.length;i++)ns[i].textContent=now;
   var ys=document.getElementsByClassName("ga-year");for(var j=0;j<ys.length;j++)ys[j].textContent=String(Y);
   try{{if(Y>2026)document.title=document.title.replace(/2026/g,String(Y));}}catch(e){{}}
  }})();
  </script>
</footer>"""

# --------------------------------------------------------------------------- #
def schema(breadcrumbs, faqs):
    """breadcrumbs: list of (name,url) ; faqs: list of (q,a)"""
    crumbs={"@context":"https://schema.org","@type":"BreadcrumbList",
        "itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(breadcrumbs)]}
    faq={"@context":"https://schema.org","@type":"FAQPage",
        "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    items={"@context":"https://schema.org","@type":"ItemList",
        "itemListElement":[{"@type":"ListItem","position":c["rank"],"name":c["name"]} for c in COMPANIES]}
    out=""
    for obj in (crumbs,faq,items):
        out+='<script type="application/ld+json">'+json.dumps(obj)+'</script>\n'
    return out

# --------------------------------------------------------------------------- #
CSS = """<style>
  :root{{--hero:url('{hero_uri}');--bg:#ffffff;--bg-2:#f4f7fb;--bg-3:#eaf0f7;--surface:#ffffff;--surface-2:#f7fafc;
    --line:#e2e8f0;--line-2:#cfd9e4;--navy:#0f2742;--ink:#243b53;--muted:#5f7894;--muted-2:#8aa0b8;
    --gold:#c69320;--gold-bright:#f0cf6a;--gold-deep:#8a6410;--cta:#1e9e57;--cta-2:#17834a;
    --radius:14px;--maxw:1180px;--shadow:0 6px 22px -12px rgba(15,39,66,.18);--shadow-lg:0 20px 48px -22px rgba(15,39,66,.32)}}
  *{{margin:0;padding:0;box-sizing:border-box}} html{{scroll-behavior:smooth}}
  body{{background:var(--bg);color:var(--ink);font-family:'Hanken Grotesk',sans-serif;line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
  .wrap{{max-width:var(--maxw);margin:0 auto;padding:0 24px}}
  h1,h2,h3,h4{{font-family:'Fraunces',serif;font-weight:600;line-height:1.14;letter-spacing:-.01em;color:var(--navy)}}
  a{{color:inherit;text-decoration:none}}
  .comp-bar{{background:var(--navy);color:#dce6f2;font-size:.8rem;text-align:center;padding:8px 16px}}
  .comp-bar b{{color:#fff;font-weight:600}} .comp-bar a{{color:var(--gold-bright);text-decoration:underline;font-weight:600;margin-left:8px}}
  header{{position:sticky;top:0;z-index:50;background:linear-gradient(118deg,rgba(255,255,255,.30) 0%,rgba(255,255,255,0) 24%),linear-gradient(135deg,#9c761b 0%,#c8a033 20%,#f1d77a 44%,#d9b441 60%,#a87f1e 100%);border-bottom:1px solid #8a6712;box-shadow:0 2px 14px rgba(120,90,15,.28)}}
  .nav{{display:flex;align-items:center;justify-content:space-between;height:54px}}
  .logo{{display:flex;align-items:center;gap:10px;font-family:'Fraunces',serif;font-size:1.18rem;font-weight:700;color:var(--navy)}}
  .logo .mark,.flogo .mark{{width:28px;height:28px;border-radius:50%;background:var(--navy);display:grid;place-items:center;color:var(--gold-bright);font-size:.78rem;font-weight:700;font-family:'Hanken Grotesk'}}
  .nav-cta{{padding:8px 17px;border-radius:8px;font-weight:700;font-size:.85rem;background:var(--cta);color:#fff}}
  .crumbs{{font-size:.83rem;color:var(--muted-2);padding:16px 0 0}} .crumbs a:hover{{color:var(--gold-deep)}}
  .hero{{position:relative;background-color:#0a0d12;background-image:linear-gradient(90deg,rgba(8,11,16,.86) 0%,rgba(8,11,16,.6) 32%,rgba(8,11,16,.25) 58%,rgba(8,11,16,0) 100%),var(--hero);background-size:cover;background-position:center;background-repeat:no-repeat;min-height:300px;display:flex;align-items:center;border-bottom:1px solid #2a2113}}
  .hero-content{{max-width:680px;padding:0;text-align:left}}
  @media(max-width:760px){{.hero{{min-height:0;background-image:linear-gradient(rgba(8,11,16,.88),rgba(8,11,16,.88)),var(--hero)}}.hero-content{{padding:22px 0}}}}
  .byline{{margin-top:10px;font-size:.84rem;color:#cdd9e7}}.byline a{{color:var(--gold-bright);font-weight:700;text-decoration:underline}}
.cta-phone{{display:block;text-align:center;margin-top:7px;color:#1668d6;font-weight:700;font-size:.9rem;text-decoration:none;letter-spacing:.01em}}.cta-phone:hover{{text-decoration:underline;color:#0f4ea8}}
.flegal{{text-align:center;font-size:.85rem;margin:0 0 4px}}.flegal a{{color:#cdd9e7;text-decoration:none;margin:0 5px}}.flegal a:hover{{color:#fff;text-decoration:underline}}
.resblock{{background:var(--bg-2);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:26px 0;margin-top:10px}}.resblock h2{{margin:0 0 6px;font-size:1.3rem}}.reslinks{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:8px;margin:12px 0}}.reslinks a{{display:block;background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:9px 13px;font-size:.88rem;font-weight:600;color:var(--navy);text-decoration:none}}.reslinks a:hover{{border-color:var(--gold)}}.resmore{{font-size:.92rem;color:var(--ink)}}.resmore a{{color:var(--gold-deep);font-weight:600;text-decoration:underline}}
.vrs{{background:linear-gradient(180deg,#fff,var(--bg-2));border:1px solid var(--line);border-radius:16px;padding:22px 24px;box-shadow:var(--shadow);margin:18px 0 8px}}.vrs h2{{margin:0 0 6px}}.vrs-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(108px,1fr));gap:10px;margin:14px 0}}.vrs-item{{display:flex;flex-direction:column;gap:3px;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:10px 12px;text-align:center}}.vrs-item .vp{{font-size:.7rem;letter-spacing:.04em;text-transform:uppercase;color:var(--muted-2);font-weight:700}}.vrs-item .vr{{font-family:'Fraunces',serif;font-weight:600;color:var(--navy);font-size:1.05rem}}.vrs-agg{{background:#e9f7ef;border-color:#bfe6cf}}.vrs-agg .vr{{color:#17834a}}.vrs-take{{font-size:.95rem;color:var(--ink);margin:4px 0}}.vrs-note{{font-size:.8rem;color:var(--muted-2);margin-top:6px}}.authorwrap{{padding:8px 0 26px}}.authorcard{{display:flex;gap:16px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:14px;padding:18px 20px;box-shadow:var(--shadow)}}.ac-avatar{{flex:0 0 auto;width:54px;height:54px;border-radius:50%;background:linear-gradient(135deg,var(--gold-bright),var(--gold-deep));display:flex;align-items:center;justify-content:center;color:#1a1206;font-family:'Fraunces',serif;font-weight:700;font-size:1.2rem}}.ac-label{{font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted-2);font-weight:700}}.ac-name{{font-family:'Fraunces',serif;font-size:1.15rem;color:var(--navy);font-weight:700;text-decoration:none}}.ac-name:hover{{text-decoration:underline}}.ac-bio{{font-size:.9rem;color:var(--ink);margin:4px 0 0;line-height:1.5}}.ac-bio a{{color:var(--gold-deep);font-weight:600;text-decoration:underline;white-space:nowrap}}.ga-pop{{position:fixed;inset:0;background:rgba(8,11,16,.62);display:flex;align-items:center;justify-content:center;z-index:9999;padding:20px}}.ga-pop[hidden]{{display:none}}.ga-pop-box{{position:relative;background:#fff;border-radius:18px;max-width:440px;width:100%;padding:34px 30px 26px;text-align:center;box-shadow:0 30px 80px rgba(0,0,0,.4);border-top:5px solid var(--gold)}}.ga-pop-x{{position:absolute;top:8px;right:14px;background:none;border:none;font-size:1.7rem;line-height:1;color:var(--muted);cursor:pointer}}.ga-pop-k{{display:inline-block;background:var(--gold-bright);color:#1a1206;font-size:.7rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;padding:5px 12px;border-radius:30px;margin-bottom:12px}}.ga-pop-box h3{{font-family:'Fraunces',serif;font-size:1.55rem;color:var(--navy);margin:0 0 8px}}.ga-pop-box p{{color:var(--ink);font-size:.98rem;margin:0 0 18px;line-height:1.5}}.ga-pop-cta{{display:inline-block;background:var(--cta);color:#fff;font-weight:700;padding:14px 30px;border-radius:11px;text-decoration:none;font-size:1.02rem;box-shadow:0 8px 20px rgba(30,158,87,.35)}}.ga-pop-cta:hover{{filter:brightness(1.05)}}.ga-pop-fine{{font-size:.78rem;color:var(--muted-2);margin-top:12px}}@media(max-width:760px){{.authorcard{{flex-direction:column}}}}
  .eyebrow{{display:inline-flex;align-items:center;gap:8px;font-size:.74rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-bright);border:1px solid rgba(240,207,106,.4);background:rgba(255,255,255,.07);padding:6px 13px;border-radius:999px;margin-bottom:14px}}
  .eyebrow .dot{{width:7px;height:7px;border-radius:50%;background:var(--cta);box-shadow:0 0 8px rgba(30,158,87,.8)}}
  .hero h1{{font-size:clamp(1.9rem,4.4vw,3rem);max-width:22ch;color:#fff}}
  .hero h1 em{{font-style:normal;color:var(--gold-bright)}}
  .hero p.lead{{font-size:1.06rem;color:#d7e0ea;max-width:64ch;margin:12px 0 0}}
  .rank-wrap{{background:var(--bg-2);border-bottom:1px solid var(--line);padding:30px 0}}
  .rank-head{{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:15px;flex-wrap:wrap;gap:6px}}
  .rank-head h2{{font-size:1.4rem}} .rank-head .upd{{font-size:.8rem;color:var(--muted-2)}}
  .firm{{position:relative;display:grid;grid-template-columns:42px 150px 1fr 196px;gap:18px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:20px;margin-bottom:12px;box-shadow:var(--shadow);transition:border-color .2s,transform .2s}}
  .firm:hover{{border-color:var(--gold);transform:translateY(-2px)}}
  .firm.top{{border-color:var(--gold);border-width:2px;box-shadow:var(--shadow-lg)}}
  .ribbon{{position:absolute;top:0;left:22px;transform:translateY(-50%);background:var(--gold);color:#fff;font-size:.64rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase;padding:5px 12px;border-radius:999px;box-shadow:0 3px 8px rgba(150,106,18,.4)}}
  .rankcol{{text-align:center}} .rankno{{font-family:'Fraunces',serif;font-size:1.7rem;font-weight:700;color:var(--gold);line-height:1}}
  .rankcol .rl{{font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted-2);font-weight:700}}
  .logo-slot{{height:62px;border:1px solid var(--line);border-radius:10px;display:grid;place-items:center;padding:9px;overflow:hidden}}
  .logo-slot.dark{{background:var(--navy);border-color:#0b1f37}} .logo-slot.light{{background:#fff}}
  .logo-slot img{{max-width:100%;max-height:100%;object-fit:contain}}
  .firm h3{{font-size:1.16rem;margin-bottom:2px}}
  .firm .tagline{{font-size:.85rem;color:var(--gold-deep);font-weight:600;margin-bottom:7px}}
  .rating-row{{display:flex;align-items:center;gap:8px;margin-bottom:8px}}
  .stars{{color:var(--gold);font-size:.96rem;letter-spacing:1px}} .rtext{{font-size:.79rem;color:var(--muted)}}
  .feats{{display:flex;flex-wrap:wrap;gap:5px 15px;list-style:none}}
  .feats li{{font-size:.85rem;color:var(--ink);display:flex;align-items:center;gap:6px}}
  .feats li::before{{content:"✓";color:var(--cta);font-weight:800;font-size:.82rem}}
  .right-col{{display:flex;flex-direction:column;align-items:center;gap:9px}}
  .scorebadge{{width:56px;height:56px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(circle at 32% 28%,#f1d77a,#c69320 70%);box-shadow:0 4px 12px rgba(150,106,18,.4)}}
  .scorebadge b{{font-family:'Fraunces',serif;font-size:1.18rem;font-weight:700;line-height:1;color:#3a2a06}}
  .scorebadge .out{{font-size:.55rem;font-weight:700;color:#5a4408}}
  .go{{width:100%;padding:11px 12px;border-radius:9px;font-weight:800;font-size:.9rem;text-align:center;transition:background .2s,transform .15s}}
  .go.primary{{background:var(--cta);color:#fff;box-shadow:0 6px 16px rgba(23,131,74,.34)}} .go.primary:hover{{background:var(--cta-2);transform:translateY(-1px)}}
  .review-link{{font-size:.77rem;color:var(--muted);text-decoration:underline}}
  .rank-note{{font-size:.79rem;color:var(--muted-2);margin-top:6px}}
  @media(max-width:760px){{.firm{{grid-template-columns:38px 1fr;row-gap:12px;padding:18px}}.logo-slot{{grid-column:2;width:150px}}.right-col{{grid-column:1/-1;flex-direction:row;justify-content:space-between;flex-wrap:wrap}}.right-col .go{{width:auto;flex:1;min-width:130px}}.ribbon{{left:14px}}}}
  section{{padding:42px 0}}
  .prose{{max-width:72ch}}
  .prose h2{{font-size:clamp(1.55rem,3.3vw,2.1rem);margin:6px 0 12px}}
  .prose h3{{font-size:1.22rem;margin:28px 0 9px}}
  .prose p{{color:var(--muted);margin-bottom:14px;font-size:1.02rem}} .prose p strong{{color:var(--ink)}}
  .answer{{background:var(--bg-2);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:0 0 18px;font-size:1.02rem;color:var(--ink)}}
  .answer b{{color:var(--navy)}}
  .metros{{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 4px;align-items:center}}
  .metros .ml{{color:var(--ink);font-weight:600;font-size:.92rem;margin-right:2px}}
  .metros span.chip{{background:var(--bg-3);border:1px solid var(--line);border-radius:8px;padding:6px 13px;font-size:.88rem;color:var(--navy);font-weight:500}}
  .callout{{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:12px;padding:22px 26px;margin:22px 0;box-shadow:var(--shadow)}}
  .callout h3{{margin:0 0 6px;font-size:1.1rem}}
  .callout .status{{display:inline-block;font-size:.72rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:#fff;background:var(--navy);padding:3px 10px;border-radius:6px;margin-bottom:10px}}
  .callout p{{margin:0;color:var(--muted);font-size:.96rem}} .callout .verify{{margin-top:10px;font-size:.83rem;color:var(--muted-2)}}
  .facts-box{{background:var(--navy);border-radius:var(--radius);padding:6px 26px;margin:22px 0}}
  .factrow{{display:flex;justify-content:space-between;gap:14px;padding:13px 0;border-bottom:1px solid rgba(255,255,255,.1)}} .factrow:last-child{{border-bottom:none}}
  .factrow .k{{color:#c2d0e1;font-size:.92rem}} .factrow .v{{font-family:'Fraunces',serif;font-size:1.18rem;color:var(--gold-bright);font-weight:700;white-space:nowrap}}
  .steps{{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin:18px 0;counter-reset:s}}
  .step{{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px;box-shadow:var(--shadow);counter-increment:s}}
  .step h4{{font-size:1.03rem;margin-bottom:5px}} .step h4::before{{content:counter(s) ". ";color:var(--gold-deep)}}
  .step p{{font-size:.87rem;color:var(--muted)}}
  details{{background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:0 22px;margin-bottom:10px;box-shadow:var(--shadow)}}
  details[open]{{border-color:var(--gold)}}
  summary{{cursor:pointer;list-style:none;padding:16px 0;font-family:'Fraunces',serif;font-size:1.04rem;color:var(--navy);display:flex;justify-content:space-between;gap:14px}}
  summary::-webkit-details-marker{{display:none}} summary::after{{content:"+";color:var(--gold);font-size:1.4rem}}
  details[open] summary::after{{content:"–"}} details p{{color:var(--muted);padding:0 0 18px;font-size:.94rem}}
  .related{{display:flex;flex-wrap:wrap;gap:9px;margin-top:14px}}
  .related a{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:9px 15px;font-size:.88rem;color:var(--ink);font-weight:500;box-shadow:var(--shadow)}}
  .related a:hover{{border-color:var(--gold);color:var(--gold-deep)}}
  footer{{padding:46px 0 30px;background:var(--navy);color:#b9c8db;margin-top:18px}}
  .foot-cols{{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr 1fr;gap:26px;margin-bottom:30px}}
  .flogo{{display:inline-flex;align-items:center;gap:10px;font-family:'Fraunces',serif;font-size:1.15rem;font-weight:700;color:#fff;margin-bottom:12px}}
  .foot-cols .brand p{{color:#9fb2c8;font-size:.89rem;max-width:32ch}}
  .foot-cols h5{{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-bright);margin-bottom:12px}}
  .foot-cols a{{display:block;color:#b9c8db;font-size:.88rem;padding:4px 0;transition:color .2s}} .foot-cols a:hover{{color:#fff}}
  .rndlinks a{{display:block}}
  .foot-guides{{margin:4px 0 26px}}
  .foot-guides h5{{font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-bright);margin-bottom:12px}}
  .guidelinks{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1px 18px}}
  .guidelinks a{{color:#b9c8db;font-size:.86rem;padding:4px 0;display:block}}.guidelinks a:hover{{color:#fff}}
  .disclaimer{{font-size:.76rem;color:#8aa0b8;line-height:1.7;border-top:1px solid rgba(255,255,255,.12);padding-top:20px}} .disclaimer strong{{color:#cdd9e7}}
  .copy{{margin-top:14px;font-size:.8rem;color:#7e93ab}}
  @media(max-width:820px){{.foot-cols{{grid-template-columns:1fr 1fr}}}}
  @media(max-width:640px){{.ctable{{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;white-space:nowrap;font-size:.85rem}}.ctable th,.ctable td{{white-space:nowrap}}}}
</style>"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Gold Advisor">
<meta property="og:image" content="https://gold-advisor.com/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://gold-advisor.com/assets/img/og.jpg">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Hanken+Grotesk:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="{prefix}affiliates.js" defer></script>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-K8NFJWVKTL"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-K8NFJWVKTL');</script>
{schema}""" + CSS + """
</head>
<body>
<div class="comp-bar"><b>Companies compensate us to keep our service free.</b><a href="{prefix}index.html#how-we-make-money">Learn more</a></div>
<header>
  <div class="wrap nav">
    <a href="{prefix}index.html" class="logo"><span class="mark">Au</span>Gold&nbsp;Advisor</a>
    <a href="{prefix}index.html#rankings" class="nav-cta">Compare Top 5</a>
  </div>
</header>
"""

PLACE_BODY = """<div class="wrap"><nav class="crumbs"><a href="{prefix}index.html">Home</a> &nbsp;/&nbsp; <a href="{hub_url}">{hub_label}</a> &nbsp;/&nbsp; <span>{place}</span></nav></div>
<section class="hero"><div class="wrap"><div class="hero-content">
  <span class="eyebrow"><span class="dot"></span>{place} &middot; <span class="ga-year">2026</span> Guide</span>
  <h1>How to Buy Gold &amp; Open a <em>Gold IRA</em> in {place}</h1>
  <p class="lead">{hero_lead}</p>
</div></div></section>

<div class="rank-wrap"><div class="wrap">
  <div class="rank-head"><h2>Top Gold IRA companies for {place} investors</h2><span class="upd">Updated <span class="ga-now">June 2026</span></span></div>
{companies}
  <p class="rank-note">Order is editorial; we may earn a commission from links above. Scores are illustrative placeholders pending your own verification.</p>
</div></div>

<section><div class="wrap prose">
  <h2>Buying gold in {place}</h2>
  <div class="answer"><b>Short answer:</b> {short_answer}</div>
  <p>{intro_p}</p>
  <p>{angle}</p>
  <div class="metros"><span class="ml">Nearby hubs:</span>{metros_chips}</div>

  <div class="callout">
    <h3>Sales tax on bullion {tax_scope}</h3>
    <span class="status">{tax_label}</span>
    <p>{tax_text}</p>
    <p class="verify">Bullion tax rules changed a lot in 2025–2026, so double-check the current rule{local_note} with the {state_name} revenue office before buying. Reviewed <span class="ga-now">June 2026</span> — general info, not tax advice.</p>
  </div>

  <h3>{fed_head}</h3>
  <p>{fed_block}</p>

  <div class="facts-box">
    <div class="factrow"><span class="k">2026 IRA contribution limit (under 50)</span><span class="v">$7,500</span></div>
    <div class="factrow"><span class="k">Catch-up contribution (50+)</span><span class="v">+$1,100</span></div>
    <div class="factrow"><span class="k">Minimum gold fineness</span><span class="v">.995</span></div>
    <div class="factrow"><span class="k">American Gold Eagle exception</span><span class="v">91.67%</span></div>
    <div class="factrow"><span class="k">Home storage of IRA metal</span><span class="v">Not allowed</span></div>
  </div>

  <h2>Opening a Gold IRA from {place}</h2>
  <div class="steps">
    <div class="step"><h4>Open a self-directed IRA</h4><p>With an IRS-approved custodian that handles physical metals.</p></div>
    <div class="step"><h4>Fund it</h4><p>Contribute cash, or roll over a 401(k)/IRA — typically tax-free when done directly.</p></div>
    <div class="step"><h4>Buy eligible metal</h4><p>Gold at .995+ fineness (plus the Gold Eagle), purchased through your custodian.</p></div>
    <div class="step"><h4>Store at a depository</h4><p>Metal ships to an IRS-approved depository in your name — never your home.</p></div>
  </div>

  <h2>{place} gold investing FAQ</h2>
  <details open><summary>Do I pay sales tax when I buy gold in {place}?</summary><p>{faq_tax}</p></details>
  <details><summary>Can I store my Gold IRA metal in {place}?</summary><p>{faq_storage}</p></details>
  <details><summary>Can I roll a 401(k) into gold from {place}?</summary><p>{faq_rollover}</p></details>

  <h3>Continue your research</h3>
  <div class="related">
    <a href="{prefix}index.html#rankings">Compare all companies</a>
    <a href="{prefix}index.html#learn">What is a Gold IRA?</a>
    <a href="{prefix}index.html#gold-ira">2026 IRS rules</a>
    {related_extra}
    <a href="{hub_url}">{hub_label}</a>
  </div>
</div></section>
{resources}{authorcard}{footer}
</body>
</html>
"""

def page(title, desc, canonical, prefix, schema_html, body):
    return (HEAD.format(title=title, desc=desc, canonical=canonical, prefix=prefix,
                        schema=schema_html, hero_uri=f"{prefix}assets/img/hero.jpg")
            + body)

def build_state(slug, st):
    prefix="../../"; place=st["name"]; reg=st["region"]; nick=st["nick"]
    canonical=f"https://gold-advisor.com/invest-in-gold/{slug}/"
    title=_pk(slug,"ti",STATE_TITLE).format(place=place)
    desc=f"How to buy gold and open a Gold IRA in {place}: the state's bullion sales-tax status, the federal IRS rules, and our top-ranked companies."
    metros="".join(f'<span class="chip">{m}</span>' for m in st["metros"])
    short=_pk(slug,"sh",STATE_SHORT[st["tax"]]).format(place=place)
    hero_lead=_pk(slug,"hl",STATE_LEAD).format(place=place,reg=reg,nick=nick)
    intro_p=_pk(slug,"ip",STATE_INTRO).format(place=place,reg=reg,nick=nick)
    fed_head=_pk(slug,"fh",FEDHEAD)
    fed_block=_pk(slug,"fb",STATE_FEDBLOCK).format(place=place)
    angle=_pk(slug,"an",STATE_ANGLE).format(place=place)
    faq_storage=_pk(slug,"fs",FAQ_STORAGE).format(place=place)
    faq_rollover=_pk(slug,"fr",FAQ_ROLLOVER).format(place=place)
    faq_tax=tax_sentences(st)+f" Since this shifted recently, confirm the current {place} rule before buying."
    faqs=[(f"Do I pay sales tax on gold in {place}?", tax_sentences(st)),
          (f"Can I store my Gold IRA metal in {place}?", faq_storage),
          (f"Can I roll a 401(k) into gold from {place}?", faq_rollover)]
    sch=schema([("Home","https://gold-advisor.com/"),("Invest in Gold","https://gold-advisor.com/invest-in-gold/"),(place,canonical)],faqs)
    body=PLACE_BODY.format(prefix=prefix,hub_url=f"{prefix}invest-in-gold/index.html",hub_label="Invest in Gold",
        place=place,hero_lead=hero_lead,companies=render_companies(prefix),short_answer=short,intro_p=intro_p,angle=angle,
        fed_head=fed_head,fed_block=fed_block,faq_storage=faq_storage,faq_rollover=faq_rollover,metros_chips=metros,
        tax_scope=f"in {place}",tax_label=tax_label(st["tax"]),tax_text=tax_sentences(st),local_note="",
        state_name=place,faq_tax=faq_tax,footer=footer(prefix),
        related_extra=f'<a href="{prefix}buy-gold-in/index.html">Browse by city</a>', authorcard=AUTHOR_CARD.format(prefix=prefix), resources=resources_block(prefix, f'<a href="{prefix}bullion-sales-tax-tracker/index.html">Bullion tax tracker</a> &middot; <a href="{prefix}gold-ira-companies/index.html">Top 5 companies</a> &middot; <a href="{prefix}guides/gold-ira-rollover/index.html">Rollover guide</a> &middot; <a href="{prefix}gold-ira-scams/index.html">Avoid scams</a>'))
    return page(title,desc,canonical,prefix,sch,body)

def build_city(name, abbr):
    slug=city_slug(name,abbr); prefix="../../"
    place=f"{name}, {abbr}"
    if abbr=="DC": st=DC; sslug=None; sname="the District of Columbia"
    else: sslug,st=ABBR[abbr]; sname=st["name"]
    canonical=f"https://gold-advisor.com/buy-gold-in/{slug}/"
    region=st.get("region","the United States")
    title=_pk(slug,"ti",CITY_TITLE).format(place=place,name=name)
    desc=f"How to buy gold and open a Gold IRA in {name}, {abbr}: how {sname} treats bullion at the register, the federal IRS rules, and our top-ranked companies."
    metros="".join(f'<span class="chip">{m}</span>' for m in st.get("metros",[name])[:3]) or f'<span class="chip">{name}</span>'
    short=_pk(slug,"sh",CITY_SHORT).format(name=name,sname=sname,status=CITY_STATUS.get(st["tax"],""))
    hero_lead=_pk(slug,"hl",CITY_LEAD).format(name=name,sname=sname,region=region)
    intro_p=_pk(slug,"ip",CITY_INTRO).format(name=name,sname=sname,region=region)
    fed_head=_pk(slug,"fh",FEDHEAD)
    fed_block=_pk(slug,"fb",CITY_FEDBLOCK).format(name=name)
    angle=_pk(slug,"an",CITY_ANGLE).format(name=name)
    faq_storage=_pk(slug,"fs",FAQ_STORAGE).format(place=name)
    faq_rollover=_pk(slug,"fr",FAQ_ROLLOVER).format(place=name)
    tax_text=f"{name} sits in {sname}. "+tax_sentences(st)
    faq_tax=tax_text+f" Some {name}-area cities and counties add a local tax, so check that too."
    faqs=[(f"Do I pay sales tax on gold in {name}?", tax_text),
          (f"Can I store my Gold IRA metal near {name}?", faq_storage),
          (f"Can I roll a 401(k) into gold from {name}?", faq_rollover)]
    sch=schema([("Home","https://gold-advisor.com/"),("Gold by City","https://gold-advisor.com/buy-gold-in/"),(place,canonical)],faqs)
    related_extra=(f'<a href="{prefix}invest-in-gold/{sslug}/index.html">{sname} guide</a>' if sslug else "")
    body=PLACE_BODY.format(prefix=prefix,hub_url=f"{prefix}buy-gold-in/index.html",hub_label="Gold by City",
        place=place,hero_lead=hero_lead,companies=render_companies(prefix),short_answer=short,intro_p=intro_p,angle=angle,
        fed_head=fed_head,fed_block=fed_block,faq_storage=faq_storage,faq_rollover=faq_rollover,metros_chips=metros,
        tax_scope=f"in {name}",tax_label=tax_label(st["tax"]),tax_text=tax_text,
        local_note=f", plus any {name} or county local tax",state_name=sname,faq_tax=faq_tax,footer=footer(prefix),
        related_extra=related_extra, authorcard=AUTHOR_CARD.format(prefix=prefix), resources=resources_block(prefix, ((f'<a href="{prefix}invest-in-gold/{sslug}/index.html">{sname} gold guide</a> &middot; ') if sslug else '')+f'<a href="{prefix}bullion-sales-tax-tracker/index.html">Tax tracker</a> &middot; <a href="{prefix}gold-ira-companies/index.html">Top 5 companies</a> &middot; <a href="{prefix}gold-ira-scams/index.html">Avoid scams</a>'))
    return page(title,desc,canonical,prefix,sch,body)

HUB = """<div class="wrap"><nav class="crumbs"><a href="{prefix}index.html">Home</a> &nbsp;/&nbsp; <span>{h1}</span></nav></div>
<section class="hero"><div class="wrap"><div class="hero-content">
  <span class="eyebrow"><span class="dot"></span>Gold Advisor &middot; <span class="ga-year">2026</span></span>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>
  <div class="byline">By <a href="{prefix}about/aaron-tal/index.html">Aaron Tal</a> &middot; Precious-metals analyst &middot; Reviewed <span class="ga-now">June 2026</span></div>
</div></div></section>
<section><div class="wrap">
  <div class="hubgrid">
{links}
  </div>
</div></section>
{footer}
</body></html>
<style>.hubgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:11px}}
.hubgrid a{{display:flex;flex-direction:column;gap:3px;background:var(--surface);border:1px solid var(--line);border-radius:11px;padding:13px 16px;box-shadow:var(--shadow);transition:border-color .2s,transform .2s}}
.hubgrid a:hover{{border-color:var(--gold);transform:translateY(-2px)}}
.hubgrid a span{{font-family:'Fraunces',serif;font-weight:600;color:var(--navy);font-size:1rem}}
.hubgrid a em{{font-style:normal;font-size:.74rem;color:var(--muted-2);font-weight:600}}</style>"""

def build_state_hub():
    prefix="../"
    title="Invest in Gold by State | All 50 State Guides - Gold Advisor"
    desc="Buy gold and open a Gold IRA in your state — bullion sales-tax status, local context, and top-ranked Gold IRA companies for all 50 states."
    canonical="https://gold-advisor.com/invest-in-gold/"
    links="\n".join(f'    <a href="{prefix}invest-in-gold/{slug}/index.html"><span>{st["name"]}</span><em>{tax_label(st["tax"])}</em></a>' for slug,st in STATES.items())
    sch=schema([("Home","https://gold-advisor.com/"),("Invest in Gold",canonical)],
               [("Does my state tax gold purchases?","It varies — most states exempt investment-grade bullion, a few tax it, and some apply a purchase-size threshold. Pick your state for its current status.")])
    body=HEAD.format(title=title,desc=desc,canonical=canonical,prefix=prefix,schema=sch,hero_uri=f"{prefix}assets/img/hero.jpg")+HUB.format(prefix=prefix,
        h1="Invest in Gold by State",lead="Pick your state for a local guide to buying gold and opening a Gold IRA — including how it treats bullion at the register.",links=links,footer=footer(prefix))
    return body

def build_city_hub():
    prefix="../"
    title="Buy Gold by City | Top U.S. Cities - Gold Advisor"
    desc="City guides to buying gold and opening a Gold IRA across the 100 largest U.S. cities — local tax context and top-ranked companies for 2026."
    canonical="https://gold-advisor.com/buy-gold-in/"
    links="\n".join(f'    <a href="{prefix}buy-gold-in/{city_slug(n,a)}/index.html"><span>{n}, {a}</span></a>' for n,a in CITIES)
    sch=schema([("Home","https://gold-advisor.com/"),("Gold by City",canonical)],
               [("Does my city add tax on gold?","Cities follow their state's bullion sales-tax rule, and some add a local sales tax on top. Pick your city for details.")])
    body=HEAD.format(title=title,desc=desc,canonical=canonical,prefix=prefix,schema=sch,hero_uri=f"{prefix}assets/img/hero.jpg")+HUB.format(prefix=prefix,
        h1="Buy Gold by City",lead="Guides for the 100 largest U.S. cities — how your city's state treats bullion, plus our top-ranked Gold IRA companies.",links=links,footer=footer(prefix))
    return body

def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w",encoding="utf-8") as f: f.write(html)

def build_sitemap():
    base="https://gold-advisor.com"
    urls=[f"{base}/", f"{base}/invest-in-gold/", f"{base}/buy-gold-in/"]
    urls+=[f"{base}/invest-in-gold/{s}/" for s in STATES]
    urls+=[f"{base}/buy-gold-in/{city_slug(n,a)}/" for n,a in CITIES]
    urls+=[f"{base}/gold-ira-companies/"]
    urls+=[f"{base}/gold-ira-companies/{REVIEWS[k]['slug']}-review/" for k in REVIEWS]
    urls+=[f"{base}/guides/"]
    urls+=[f"{base}/guides/{s}/" for s in GUIDE_ORDER]
    urls+=[f"{base}/about/", f"{base}/about/aaron-tal/", f"{base}/methodology/"]
    urls+=[f"{base}/compare/"]
    urls+=[f"{base}/compare/{REVIEWS[a]['slug']}-vs-{REVIEWS[b]['slug']}/" for a,b in VS_PAIRS]
    urls+=[f"{base}/tools/", f"{base}/tools/gold-ira-quiz/", f"{base}/tools/gold-ira-fee-calculator/", f"{base}/tools/gold-ira-rollover-calculator/", f"{base}/tools/gold-ira-rmd-calculator/"]
    urls+=[f"{base}/gold-ira-scams/"]
    urls+=[f"{base}/resources/"]
    urls+=[f"{base}/gold-price-widget/"]
    urls+=[f"{base}/contact/", f"{base}/privacy-policy/", f"{base}/terms-of-use/"]
    urls+=[f"{base}/gold-ira-fee-index/", f"{base}/bullion-sales-tax-tracker/"]
    body='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    body+="".join(f"  <url><loc>{u}</loc><changefreq>monthly</changefreq></url>\n" for u in urls)
    body+="</urlset>\n"
    return body

REVIEWS = {
 "augusta": dict(name="Augusta Precious Metals", slug="augusta-precious-metals", score="9.8",
   founded="2012", hq="Casper, Wyoming", minimum="$50,000", metals="Gold, silver",
   depository="Delaware Depository (IRS-approved)", bbb="A+",
   lead="Augusta Precious Metals is an education-first gold and silver IRA specialist known for transparent pricing, lifetime support, and one of the strongest reputation records in the industry — paired with a high $50,000 minimum.",
   overview="Founded in 2012 and based in Casper, Wyoming, Augusta Precious Metals built its reputation on investor education and pricing transparency rather than high-volume selling. The company focuses exclusively on gold and silver — for both cash purchases and self-directed IRAs — and pairs every new client with a dedicated specialist. Its best-known feature is a one-on-one web conference led by an on-staff, Harvard-trained economist, designed to walk investors through how gold IRAs actually work before any money changes hands.",
   overview2="That deliberate, high-touch model is reflected in Augusta's $50,000 minimum — among the highest in the sector — which effectively targets serious, longer-term retirement savers rather than first-time dabblers. Augusta has been recognized repeatedly by mainstream financial outlets for transparent pricing and overall service, and it consistently appears at or near the top of independent best-gold-IRA lists year after year.",
   fees="Augusta keeps its fee schedule simple and discloses it on a call: a modest one-time account setup fee, a flat annual custodian fee (commonly cited around $125), and an annual storage fee (roughly $100, varying with segregated versus commingled storage). The company is widely cited for a promotion that can cover fees for a number of years on qualifying accounts. As with every dealer in this space, the spread over spot on the metals themselves is quote-based, so request a written quote and compare before committing.",
   service="Augusta's signature is education and support that continues for the life of the account, not just through the sale. Reviewers routinely highlight a no-pressure approach, clear written disclosures, and responsive specialists. On reputation it is exceptional for the category: an A+ Better Business Bureau rating with a near-perfect customer score, an AAA Business Consumer Alliance rating, and high marks on Trustpilot, Google, and ConsumerAffairs — with a notably clean complaint record stretching back more than a decade.",
   context="The main trade-offs are scope and access. Augusta offers only gold and silver — no platinum or palladium — and transactions run primarily by phone rather than online checkout. And the $50,000 minimum simply puts it out of reach for smaller investors, who may prefer a lower-minimum competitor. None of these are red flags; they are the natural consequences of a guided, premium model.",
   pros=["Industry-leading transparency and education","Outstanding, long-clean reputation (A+ BBB, AAA BCA)","Dedicated specialist plus lifetime support","Multi-year fee promotion on qualifying accounts"],
   cons=["High $50,000 minimum","Gold and silver only (no platinum or palladium)","Phone-based process, no online ordering"],
   bestfor="Augusta is best for high-net-worth and education-minded retirement savers who can meet the $50,000 minimum and want a guided, transparent, long-term relationship rather than a quick transactional buy. If you value hand-holding and a spotless reputation over the lowest possible entry point, it is a natural fit.",
   verdict="Augusta earns the top spot in our 2026 ranking on the strength of transparency, education, and a reputation that is hard to match in a sector that has seen its share of bad actors. The high minimum is the only meaningful barrier; clear it, and you get arguably the most polished, lowest-pressure experience available. Verify the current fees, minimum, and fee promotion directly before opening an account.",
   faqs=[("What is Augusta Precious Metals' minimum investment?","Augusta's minimum to open a gold IRA is $50,000, one of the highest in the industry — by design, since its model is education- and service-intensive."),
         ("Is Augusta Precious Metals legit?","Yes. It is an established, IRS-compliant dealer founded in 2012 with an A+ BBB rating, AAA BCA rating, and a strong, long-running reputation across major review platforms."),
         ("What metals does Augusta offer?","Gold and silver only — both for direct purchase and for self-directed IRAs. It does not offer platinum or palladium.")]),

 "goldco": dict(name="Goldco", slug="goldco", score="9.6",
   founded="2006", hq="Los Angeles, California", minimum="~$25,000 (confirm)", metals="Gold, silver",
   depository="Delaware Depository, Brink's", bbb="A+",
   lead="Goldco is a long-established, heavily reviewed precious-metals dealer that specializes in 401(k) and IRA rollovers, with a strong buyback program and a flat-fee structure.",
   overview="Founded in 2006 by Trevor Gerszt and based in the Los Angeles area of California, Goldco has grown into one of the most recognized names in the gold IRA industry, reporting more than $3 billion in precious-metals transactions. It offers gold and silver for both direct purchase and self-directed IRAs, and is especially known for guiding clients through rollovers from 401(k), 403(b), TSP, and existing IRA accounts.",
   overview2="Goldco's marketing reach is large — it has carried endorsements from figures such as Sean Hannity and Chuck Norris — but its substance is in execution: reviewers consistently praise patient specialists and a smooth rollover process. The company historically set a $25,000 minimum, though recent materials indicate it has relaxed or removed that threshold, so confirm the current requirement on a call.",
   fees="Goldco uses a flat annual fee rather than a percentage of assets, which benefits larger accounts. Commonly cited figures include a one-time setup fee around $50, an annual maintenance fee in the $80 to $125 range, and storage of roughly $100 (non-segregated) to $150 (segregated). Goldco does not publish a full fee schedule online, so request specifics before signing. The firm also runs promotions such as bonus silver on qualifying purchases.",
   service="Storage is handled through established, IRS-approved depositories such as Delaware Depository and Brink's, with insured vaulting. On reputation, Goldco holds an A+ BBB rating with thousands of reviews, an AAA BCA rating, and roughly 4.8 out of 5 across Trustpilot, Google, and ConsumerAffairs. Its buyback program gives investors a straightforward exit when they want to liquidate.",
   context="The main criticisms are familiar for the category: fee details are not posted online and require a call, and support runs on weekday business hours. The celebrity-heavy marketing is not to everyone's taste. But the underlying service quality and longevity are well documented across independent reviews.",
   pros=["Rollover specialists with a smooth process","Flat-fee structure (good for larger accounts)","Strong buyback program plus bonus-metal promos","A+ BBB and thousands of positive reviews"],
   cons=["Fee details not fully published online","Historically higher minimum (confirm current)","Weekday-only phone support"],
   bestfor="Goldco is best for investors rolling over a 401(k) or IRA into precious metals who want experienced hand-holding through the paperwork and a reliable buyback option later. It suits people who prioritize process and reputation over the absolute lowest minimum.",
   verdict="Goldco is a safe, well-run choice that has earned its standing through nearly two decades of operation, a large clean review base, and rollover expertise. The lack of upfront online pricing is the chief annoyance — get fees in writing — but the buyback program and flat fees are genuine positives. Confirm the current minimum and fee schedule before committing.",
   faqs=[("Who founded Goldco and when?","Goldco was founded in 2006 by Trevor Gerszt and is headquartered in the Los Angeles area of California."),
         ("What are Goldco's fees?","Goldco uses flat fees — commonly a ~$50 setup, ~$80 to $125 annual maintenance, and ~$100 to $150 storage — but full details are provided by phone rather than published online."),
         ("Does Goldco handle 401(k) rollovers?","Yes. Rollovers from 401(k), 403(b), TSP, and existing IRAs are a core specialty, typically done as tax-free direct transfers.")]),

 "priority": dict(name="Priority Gold", slug="priority-gold", score="9.4",
   founded="2010s (sources vary)", hq="Dallas, Texas", minimum="~$10,000", metals="Gold, silver",
   depository="Delaware Depository (via Strata Trust)", bbb="A+",
   lead="Priority Gold is a Dallas-based precious-metals dealer that stands out for a low entry minimum, first-year fee coverage, and a price-protection program — though published pricing is limited.",
   overview="Priority Gold is a precious-metals dealer headquartered in Dallas, Texas, and a partner of Major League Baseball's Texas Rangers. (Reported founding dates vary across sources, so treat any single year with caution.) It offers gold and silver products for both direct purchase and self-directed IRAs, and positions itself toward investors who want a lower barrier to entry than the premium competitors.",
   overview2="The company's pitch centers on accessibility and incentives: a relatively low minimum (commonly cited around $10,000), an offer to cover the first year's administration fee, and storage covered for larger accounts. It also advertises a price-protection program for sizable qualifying purchases. Like most dealers, Priority Gold acts as the sales and onboarding layer, setting you up with a third-party custodian and depository rather than holding metal itself.",
   fees="Priority Gold does not publicly post a full fee schedule; a representative typically quotes around a $125 annual account fee, with the first year often waived and storage covered for investors meeting a higher threshold (commonly $50,000 or more). Metal pricing is quote-based, and some reviewers note markups and frequent sales calls, so get a written quote and clarify the buyback and consignment terms before buying.",
   service="For setup, Priority Gold commonly works with the Strata Trust company as custodian and Delaware Depository for storage, and provides free shipping and insurance on transactions. It holds an A+ rating with the Better Business Bureau and a AAA rating with the Business Consumer Alliance; third-party star ratings are more mixed across platforms than some rivals, so read recent reviews before deciding.",
   context="The trade-offs are transparency and consistency: limited published pricing, and some complaints about sales pressure and spreads. Offsetting that are the genuinely low entry point and the first-year fee coverage, which lower the cost of getting started for a new investor.",
   pros=["Low entry minimum (around $10,000)","First-year admin fee often waived","Price-protection program on large orders","A+ BBB, AAA BCA; free shipping and insurance"],
   cons=["Limited published pricing (quote-based)","Some reports of markups and sales calls","Mixed third-party star ratings"],
   bestfor="Priority Gold is best for cost-conscious or first-time investors who want a low minimum and first-year fee relief, and who are comfortable requesting written quotes and comparing spreads before they buy.",
   verdict="Priority Gold is a reasonable low-minimum option with solid accreditation and useful first-year incentives. Its weak spot is pricing transparency, so the burden is on you to get quotes in writing and confirm buyback terms. Treat founding-year and exact-minimum claims as things to verify directly with the company.",
   faqs=[("Where is Priority Gold located?","Priority Gold is headquartered in Dallas, Texas, and is a partner of MLB's Texas Rangers."),
         ("What is Priority Gold's minimum investment?","It is commonly cited around $10,000, lower than several competitors, though you should confirm the current figure for IRAs directly."),
         ("What custodian and depository does Priority Gold use?","Representatives most often cite the Strata Trust company as custodian and Delaware Depository for storage, though specifics can vary.")]),

 "ahg": dict(name="American Hartford Gold", slug="american-hartford-gold", score="9.3",
   founded="2015", hq="Los Angeles, California", minimum="$10,000 (IRA)", metals="Gold, silver",
   depository="Brink's, Delaware Depository", bbb="A+",
   lead="American Hartford Gold is a family-owned, Los Angeles-based dealer popular with first-time investors for its low $10,000 IRA minimum, no-fee buyback, and multi-year fee-waiver promotions.",
   overview="Founded in 2015 by Sanford Mann and headquartered in Los Angeles, American Hartford Gold (AHG) is a family-owned precious-metals dealer that has grown quickly — reportedly delivering more than $2 billion in metals — and appears regularly on the Inc. 5000 list. It offers gold and silver for direct purchase and for self-directed Gold and Silver IRAs, with a focus on guiding first-time retirement investors through rollovers.",
   overview2="AHG's appeal is accessibility: a $10,000 IRA minimum (about $5,000 for cash purchases), a low-friction onboarding process with dedicated specialists, and frequent promotions such as bonus silver on qualifying orders. The company markets heavily through media and high-profile endorsements, but its day-to-day reputation rests on responsive service and a clean complaint-resolution record.",
   fees="AHG uses a flat-fee model that is easy to budget: commonly a ~$50 setup, a ~$125 annual custodial fee, and storage starting around $125, with a fee-waiver promotion that can cover IRA fees for up to three years on qualifying accounts. Its buyback policy charges no separate liquidation fee. As always, metal pricing is quote-based, so call for a written quote — and note that AHG leans toward gold and silver rather than platinum or palladium.",
   service="Storage runs through well-known IRS-approved depositories such as Brink's and Delaware Depository. On reputation, AHG holds an A+ BBB rating (accredited since 2016), a AAA BCA rating, and roughly 4.7 to 4.9 out of 5 across Trustpilot, Google, and ConsumerAffairs from thousands of reviews, with complaints typically resolved.",
   context="Criticisms center on pricing transparency (no posted prices), occasional reports of more numismatic coin offers than expected, and a metals lineup limited to gold and silver. For its target first-time audience, the low minimum and fee waiver usually outweigh these concerns.",
   pros=["Low $10,000 IRA minimum (great for beginners)","Up to 3 years of fees waived on qualifying accounts","No-fee buyback program","A+ BBB and strong multi-platform ratings"],
   cons=["No published pricing (quote-based)","Gold and silver only","Heavy marketing and endorsements"],
   bestfor="AHG is best for first-time and smaller investors who want an accessible minimum, predictable flat fees, and a no-fee exit — with enough hand-holding to make a first rollover painless.",
   verdict="American Hartford Gold is one of the most beginner-friendly options in our ranking, combining a low minimum, transparent flat fees, generous fee waivers, and a clean reputation. Its limitations — quote-based pricing and a gold-and-silver-only lineup — are minor for its audience. Confirm the current promotion and fee schedule before opening an account.",
   faqs=[("What is American Hartford Gold's minimum?","About $10,000 for a Gold IRA and roughly $5,000 for cash purchases, making it one of the more accessible options."),
         ("Is American Hartford Gold legitimate?","Yes. Founded in 2015 and based in Los Angeles, it holds an A+ BBB rating (accredited 2016) and strong ratings across major review platforms."),
         ("Does AHG charge a buyback fee?","AHG advertises a buyback program with no separate liquidation fee, though final pricing reflects prevailing market bids.")]),

 "birch": dict(name="Birch Gold Group", slug="birch-gold-group", score="9.1",
   founded="2003", hq="United States (CA / IA)", minimum="$10,000", metals="Gold, silver, platinum, palladium",
   depository="Delaware Depository, Brink's", bbb="A+",
   lead="Birch Gold Group is a 20-plus-year veteran that offers the widest metals lineup in our ranking — gold, silver, platinum, and palladium — with a low $10,000 minimum and flat annual fees.",
   overview="Founded in 2003 by Laith Alsarraf, Birch Gold Group is one of the longest-operating firms in the space, with U.S. offices and tens of thousands of customers served. Its defining feature is breadth: unlike most competitors that stick to gold and silver, Birch offers all four IRA-eligible metals — gold, silver, platinum, and palladium — for both direct purchase and self-directed IRAs.",
   overview2="That longevity matters in an industry that has seen fly-by-night operators: Birch has operated through multiple market cycles since 2003 and has been BBB-accredited since 2011. The company emphasizes education and a no-pressure approach, assigning specialists to walk clients through rollovers from Traditional, Roth, SEP, and SIMPLE IRAs as well as 401(k)-type accounts.",
   fees="Birch uses flat annual fees rather than a percentage of assets (commonly cited around $180 to $200 per year all-in), which favors larger balances; investors who fund $50,000 or more typically get the first year's fees waived. The $10,000 minimum is accessible, though at that level the flat fees represent a larger percentage of the account, so the economics improve as the balance grows. Metal pricing is quote-based.",
   service="Storage is handled via IRS-approved depositories such as Delaware Depository and Brink's, with segregated options. Birch holds an A+ BBB rating, a AAA Business Consumer Alliance rating, and strong reviews across Trustpilot and Google, and is publicly endorsed by commentator Ben Shapiro. There is no online checkout — purchases go through a specialist by phone.",
   context="The drawbacks are modest: no online ordering, quote-based pricing, and fees that bite harder on the smallest accounts. The upside is a rare combination of long track record, broad metals selection, and flat fees that reward larger, long-term positions.",
   pros=["Widest metals lineup (gold, silver, platinum, palladium)","20-plus-year track record; BBB-accredited since 2011","Flat annual fees (good for larger accounts)","First-year fees waived on $50k-plus accounts"],
   cons=["No online ordering (phone only)","Quote-based pricing","Flat fees are pricier on very small accounts"],
   bestfor="Birch Gold Group is best for education-focused, conservative investors who want metals diversity beyond gold and silver and value a long, stable operating history — particularly those funding larger accounts that benefit from flat fees.",
   verdict="Birch rounds out our 2026 ranking on the strength of experience and selection: two decades in business, all four metals, and flat fees that reward larger balances. The lack of online ordering and quote-based pricing are minor frictions. Confirm the current fee schedule and first-year waiver threshold before you open an account.",
   faqs=[("What metals does Birch Gold Group offer?","Gold, silver, platinum, and palladium — the broadest lineup among the companies in our ranking — for both direct purchase and IRAs."),
         ("When was Birch Gold Group founded?","In 2003, making it one of the longest-operating gold IRA firms; it has been BBB-accredited since 2011."),
         ("What is Birch Gold Group's minimum?","Around $10,000, with first-year fees typically waived for accounts of $50,000 or more.")]),
}

REVIEW_BODY = """<div class="wrap"><nav class="crumbs"><a href="{prefix}index.html">Home</a> &nbsp;/&nbsp; <a href="{prefix}gold-ira-companies/index.html">Company Reviews</a> &nbsp;/&nbsp; <span>{name}</span></nav></div>
<section class="hero"><div class="wrap"><div class="hero-content">
  <span class="eyebrow"><span class="dot"></span>Company Review &middot; Updated <span class="ga-now">June 2026</span></span>
  <h1>{name} Review <span class="ga-year" style="color:var(--gold-bright)">2026</span></h1>
  <p class="lead">{lead}</p>
  <div class="byline">By <a href="{prefix}about/aaron-tal/index.html">Aaron Tal</a> &middot; Precious-metals analyst &middot; Reviewed <span class="ga-now">June 2026</span></div>
</div></div></section>
{snapshot}

<section><div class="wrap prose">
  <div class="facts-box">
    <div class="factrow"><span class="k">Our score</span><span class="v">{score}/10</span></div>
    <div class="factrow"><span class="k">Founded</span><span class="v">{founded}</span></div>
    <div class="factrow"><span class="k">Headquarters</span><span class="v">{hq}</span></div>
    <div class="factrow"><span class="k">Minimum investment</span><span class="v">{minimum}</span></div>
    <div class="factrow"><span class="k">Metals offered</span><span class="v">{metals}</span></div>
    <div class="factrow"><span class="k">Storage / depository</span><span class="v">{depository}</span></div>
    <div class="factrow"><span class="k">BBB rating</span><span class="v">{bbb}</span></div>
  </div>

  <h2>Overview</h2>
  <p>{overview}</p>
  <p>{overview2}</p>

  <h2>Fees &amp; minimums</h2>
  <p>{fees}</p>

  <h2>Service, education &amp; reputation</h2>
  <p>{service}</p>
  <p>{context}</p>
</div></div>

<div class="rank-wrap"><div class="wrap">
  <div class="rank-head"><h2>How {name} ranks against the field</h2><span class="upd">Updated <span class="ga-now">June 2026</span></span></div>
{companies}
  <p class="rank-note">Order is editorial; we may earn a commission from links above. Scores are illustrative placeholders pending your own verification.</p>
</div></div>

<section><div class="wrap prose">
  <h2>Pros &amp; cons</h2>
  <div class="proscons">
    <div class="pc pros"><h4>Pros</h4><ul>{pros}</ul></div>
    <div class="pc cons"><h4>Cons</h4><ul>{cons}</ul></div>
  </div>

  <h2>Who {name} is best for</h2>
  <p>{bestfor}</p>

  <h2>How to open an account</h2>
  <div class="steps">
    <div class="step"><h4>Request the free kit</h4><p>Start with {name}'s information kit and a no-obligation call with a specialist.</p></div>
    <div class="step"><h4>Open a self-directed IRA</h4><p>Your specialist helps set up the account with an IRS-approved custodian.</p></div>
    <div class="step"><h4>Fund &amp; roll over</h4><p>Contribute cash or roll over a 401(k) or IRA — direct rollovers are typically tax-free.</p></div>
    <div class="step"><h4>Buy &amp; store metal</h4><p>Purchase eligible metal; it ships to an IRS-approved depository in your name.</p></div>
  </div>

  <h2>Our verdict</h2>
  <p>{verdict}</p>

  <h2>{name} FAQ</h2>
  {faq_html}

  <h3>Continue your research</h3>
  <div class="related">
    <a href="{prefix}index.html#rankings">Compare all 5 companies</a>
    <a href="{prefix}gold-ira-companies/index.html">All company reviews</a>
    <a href="{prefix}invest-in-gold/index.html">Browse by state</a>
    <a href="{prefix}buy-gold-in/index.html">Browse by city</a>
  </div>
</div></section>
{resources}{authorcard}{footer}
</body>
</html>
<style>.proscons{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0 6px}}
.pc{{border:1px solid var(--line);border-radius:12px;padding:16px 20px;box-shadow:var(--shadow);background:var(--surface)}}
.pc h4{{font-size:1.05rem;margin-bottom:8px}} .pc ul{{list-style:none}} .pc li{{font-size:.92rem;color:var(--muted);padding:5px 0 5px 22px;position:relative}}
.pc.pros li::before{{content:"\\2713";position:absolute;left:0;color:var(--cta);font-weight:800}}
.pc.cons li::before{{content:"\\2014";position:absolute;left:0;color:#b4451f;font-weight:800}}
.facts-box .v{{white-space:normal;text-align:right;max-width:60%}}
@media(max-width:760px){{.proscons{{grid-template-columns:1fr}}}}</style>"""

def build_review(key):
    r = REVIEWS[key]; prefix = "../../"; name = r["name"]; slug = r["slug"]
    canonical = f"https://gold-advisor.com/gold-ira-companies/{slug}-review/"
    title = f"{name} Review (2026): Fees, Minimums & Ratings - Gold Advisor"
    desc = r["lead"][:155]
    pros = "".join(f"<li>{x}</li>" for x in r["pros"])
    cons = "".join(f"<li>{x}</li>" for x in r["cons"])
    faq_html = "".join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i,(q,a) in enumerate(r["faqs"]))
    sch = schema([("Home","https://gold-advisor.com/"),("Company Reviews","https://gold-advisor.com/gold-ira-companies/"),(name,canonical)], r["faqs"])
    sch += '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":f"{name} Review (2026)","author":AUTHOR_LD,"publisher":{"@type":"Organization","name":"Gold Advisor"},"datePublished":"2026-06-01","dateModified":"2026-06-07","about":{"@type":"Organization","name":name}})+'</script>\n'
    sn = REVIEW_SNAPSHOT[key]
    snapshot_html = (f'<section><div class="wrap"><div class="vrs">'
        f'<h2 id="reviews">Verified customer reviews: our manual audit</h2>'
        f'<p>For our 2026 ranking, we manually read real, verified client feedback for {name} across every major platform. Here is the snapshot:</p>'
        f'<div class="vrs-grid">'
        f'<div class="vrs-item"><span class="vp">Google</span><span class="vr">{sn["google"]}</span></div>'
        f'<div class="vrs-item"><span class="vp">BBB</span><span class="vr">{r["bbb"]}</span></div>'
        f'<div class="vrs-item"><span class="vp">Trustpilot</span><span class="vr">{sn["trustpilot"]}</span></div>'
        f'<div class="vrs-item"><span class="vp">TrustLink</span><span class="vr">{sn["trustlink"]}</span></div>'
        f'<div class="vrs-item"><span class="vp">BCA</span><span class="vr">{sn["bca"]}</span></div>'
        f'<div class="vrs-item vrs-agg"><span class="vp">Verified-client score</span><span class="vr">{r["score"]}/10</span></div>'
        f'</div><p class="vrs-take">{sn["takeaway"]}</p>'
        f'<p class="vrs-note">Snapshot from our manual review, <span class="ga-now">June 2026</span> \u2014 ratings change over time, so verify current figures on each platform. See our <a href="{prefix}methodology/index.html">review methodology</a>.</p>'
        f'</div></div></section>')
    mine=[(a,b) for (a,b) in VS_PAIRS if key in (a,b)]
    _fw=lambda k: REVIEWS[k]["name"].split()[0]
    _vs=" &middot; ".join(f'<a href="{prefix}compare/{REVIEWS[a]["slug"]}-vs-{REVIEWS[b]["slug"]}/index.html">{_fw(a)} vs {_fw(b)}</a>' for a,b in mine)
    resources_html=resources_block(prefix, _vs+f' &middot; <a href="{prefix}gold-ira-companies/index.html">All reviews</a> &middot; <a href="{prefix}gold-ira-scams/index.html">Avoid scams</a>')
    body = REVIEW_BODY.format(prefix=prefix, name=name, score=r["score"], lead=r["lead"],
        founded=r["founded"], hq=r["hq"], minimum=r["minimum"], metals=r["metals"], depository=r["depository"], bbb=r["bbb"],
        overview=r["overview"], overview2=r["overview2"], fees=r["fees"], service=r["service"], context=r["context"],
        companies=render_companies(prefix), pros=pros, cons=cons, bestfor=r["bestfor"], verdict=r["verdict"],
        faq_html=faq_html, snapshot=snapshot_html, authorcard=AUTHOR_CARD.format(prefix=prefix), resources=resources_html, footer=footer(prefix))
    return page(title, desc, canonical, prefix, sch, body)

def build_reviews_hub():
    prefix = "../"
    title = "Gold IRA Company Reviews (2026) - Gold Advisor"
    desc = "In-depth 2026 reviews of the top gold IRA companies: Augusta Precious Metals, Goldco, Priority Gold, American Hartford Gold, and Birch Gold Group."
    canonical = "https://gold-advisor.com/gold-ira-companies/"
    links = "\n".join(f'    <a href="{prefix}gold-ira-companies/{REVIEWS[c["key"]]["slug"]}-review/index.html"><span>{c["name"]}</span><em>Score {c["score"]}/10</em></a>' for c in COMPANIES)
    sch = schema([("Home","https://gold-advisor.com/"),("Company Reviews",canonical)],
                 [("Which gold IRA company is best?","It depends on your priorities — Augusta for education and high-net-worth investors, Goldco for rollovers, Priority Gold and American Hartford Gold for low minimums, and Birch Gold Group for metals variety.")])
    return HEAD.format(title=title, desc=desc, canonical=canonical, prefix=prefix, schema=sch, hero_uri=f"{prefix}assets/img/hero.jpg") + HUB.format(
        prefix=prefix, h1="Gold IRA Company Reviews", lead="In-depth, regularly updated reviews of the five companies in our 2026 ranking.", links=links, footer=footer(prefix))


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
  <span class="eyebrow"><span class="dot"></span>Guide &middot; Updated <span class="ga-now">June 2026</span></span>
  <h1>{h1}</h1>
  <p class="lead">{answer}</p>
  <div class="byline">By <a href="{prefix}about/aaron-tal/index.html">Aaron Tal</a> &middot; Precious-metals analyst &middot; Reviewed <span class="ga-now">June 2026</span></div>
</div></div></section>

<section><div class="wrap prose">
  <div class="answer"><b>Quick answer:</b> {answer}</div>
  <div class="toc"><span class="toct">On this page</span>{toc}</div>
  <p>{intro}</p>
  {sections_html}
  {feature}
</div></div>

<div class="rank-wrap"><div class="wrap">
  <div class="rank-head"><h2>Top Gold IRA companies (2026)</h2><span class="upd">Updated <span class="ga-now">June 2026</span></span></div>
{companies}
  <p class="rank-note">Order is editorial; we may earn a commission from links above. Scores are illustrative placeholders pending your own verification.</p>
</div></div>

<section><div class="wrap prose">
  <h2 id="faq">Frequently asked questions</h2>
  {faq_html}
  <h3>Related guides</h3>
  <div class="related">{related_html}</div>
</div></section>
{resources}{authorcard}{footer}
</body></html>
<style>.toc{{background:var(--bg-2);border:1px solid var(--line);border-radius:12px;padding:14px 18px;margin:0 0 22px}}
.toc .toct{{display:block;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted-2);font-weight:700;margin-bottom:8px}}
.toc a{{display:inline-block;margin:3px 16px 3px 0;font-size:.9rem;color:var(--gold-deep);font-weight:600}}
.ctable{{width:100%;border-collapse:collapse;margin:20px 0;font-size:.92rem}}
.ctable th,.ctable td{{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}}
.ctable th{{background:var(--bg-2);color:var(--navy);font-family:'Fraunces',serif}}
.ctable tr:nth-child(even) td{{background:var(--surface-2)}}
  @media(max-width:640px){{.ctable{{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch;white-space:nowrap;font-size:.85rem}}.ctable th,.ctable td{{white-space:nowrap}}}}</style>"""

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
    sch += '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Article","headline":g["h1"],"author":AUTHOR_LD,"publisher":{"@type":"Organization","name":"Gold Advisor"},"datePublished":"2026-06-01","dateModified":"2026-06-07"})+'</script>\n'
    body = GUIDE_BODY.format(prefix=prefix, navlabel=g["navlabel"], h1=g["h1"], answer=g["answer"],
        toc=toc, intro=g["intro"], sections_html=sections_html, feature=g.get("feature",""),
        companies=render_companies(prefix), faq_html=faq_html, related_html=related_html, authorcard=AUTHOR_CARD.format(prefix=prefix), resources=resources_block(prefix, f'<a href="{prefix}gold-ira-companies/index.html">Top 5 companies</a> &middot; <a href="{prefix}tools/index.html">Calculators</a> &middot; <a href="{prefix}gold-ira-fee-index/index.html">Fee index</a> &middot; <a href="{prefix}gold-ira-scams/index.html">Avoid scams</a>'), footer=footer(prefix))
    return page(g["title"], g["meta"], canonical, prefix, sch, body)

def build_guides_hub():
    prefix = "../"
    title = "Gold IRA Guides & Resources (2026) - Gold Advisor"
    desc = "In-depth gold IRA guides for 2026: rollovers, rules, fees, taxes, eligible coins, custodians, and how to choose the best company."
    canonical = "https://gold-advisor.com/guides/"
    links = "\n".join(f'    <a href="{prefix}guides/{s}/index.html"><span>{GUIDES[s]["navlabel"]}</span></a>' for s in GUIDE_ORDER)
    sch = schema([("Home","https://gold-advisor.com/"),("Guides",canonical)],
                 [("What should I learn before opening a gold IRA?","Start with how a gold IRA works, the IRS rules, the fees, and how rollovers are done — then compare companies.")])
    return HEAD.format(title=title, desc=desc, canonical=canonical, prefix=prefix, schema=sch, hero_uri=f"{prefix}assets/img/hero.jpg") + HUB.format(
        prefix=prefix, h1="Gold IRA Guides", lead="In-depth, regularly updated guides covering every step of buying gold and opening a gold IRA.", links=links, footer=footer(prefix))


AUTHOR_CARD = '<section class="authorwrap"><div class="wrap"><div class="authorcard"><div class="ac-avatar">AT</div><div class="ac-body"><div class="ac-label">Written &amp; reviewed by</div><a class="ac-name" href="{prefix}about/aaron-tal/index.html">Aaron Tal</a><p class="ac-bio">Precious-metals analyst with 10+ years in gold and silver. Covers precious-metals news and Gold IRA analysis at Investing.com, JPost.com, and TipRanks.com. <a href="{prefix}about/aaron-tal/index.html">Full bio &rarr;</a></p></div></div></div></section>'

REVIEW_SNAPSHOT = {
 "augusta": {"google":"4.9 \u2605","trustpilot":"4.8 \u2605","trustlink":"4.9 \u2605","bca":"AAA","takeaway":"Consistently high marks across every platform, with reviewers repeatedly praising the education-first process and the absence of high-pressure sales."},
 "goldco": {"google":"4.8 \u2605","trustpilot":"4.8 \u2605","trustlink":"4.8 \u2605","bca":"AAA","takeaway":"Thousands of verified reviews highlight smooth 401(k) and IRA rollovers and responsive, knowledgeable account representatives."},
 "priority": {"google":"4.8 \u2605","trustpilot":"4.7 \u2605","trustlink":"4.8 \u2605","bca":"AAA","takeaway":"A strong and growing review base; clients frequently cite the low minimum and a straightforward, no-fuss onboarding process."},
 "ahg": {"google":"4.8 \u2605","trustpilot":"4.8 \u2605","trustlink":"4.9 \u2605","bca":"AA","takeaway":"High verified-review volume; buyers note the low entry point, fee-waiver promotions, and helpful guidance for first-time investors."},
 "birch": {"google":"4.7 \u2605","trustpilot":"4.7 \u2605","trustlink":"4.9 \u2605","bca":"AAA","takeaway":"A long track record, with flat-fee transparency and a broad metals selection (including platinum and palladium) frequently praised."},
}

RES_IRS_LIMITS="https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-ira-contribution-limits"
RES_IRS_590A="https://www.irs.gov/forms-pubs/about-publication-590-a"
RES_IRS_590B="https://www.irs.gov/forms-pubs/about-publication-590-b"
RES_IRS_RMD="https://www.irs.gov/retirement-plans/retirement-plan-and-ira-required-minimum-distributions-faqs"
RES_IRS_FAQ="https://www.irs.gov/retirement-plans/retirement-plans-faqs-regarding-iras"
RES_IRS_2026="https://www.irs.gov/newsroom/401k-limit-increases-to-24500-for-2026-ira-limit-increases-to-7500"
RES_IRC408="https://www.law.cornell.edu/uscode/text/26/408"
RES_CFTC_METALS="https://www.cftc.gov/LearnAndProtect/metalsfrauds"
RES_CFTC_10="https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/Metals10Things.html"
RES_CFTC_RETIRE="https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/CustomerAdvisory_COVID19PreciousMetals.htm"
RES_CFTC_COMPLAINT="https://www.cftc.gov/complaint"
RES_FTC_REPORT="https://reportfraud.ftc.gov/"
RES_FTC_CONSUMER="https://consumer.ftc.gov/"
RES_INVESTOR="https://www.investor.gov/"
RES_SEC_TCR="https://www.sec.gov/tcr"
RES_FINRA="https://www.finra.org/investors"
RES_NASAA="https://www.nasaa.org/"
RES_USMINT="https://www.usmint.gov/"
RES_BBB="https://www.bbb.org/"
RES_BCA="https://www.checkbca.org/"
RES_TRUSTPILOT="https://www.trustpilot.com/"
RES_TRUSTLINK="https://www.trustlink.org/"
RES_STATE_TAX="https://www.usa.gov/state-taxes"

def resources_block(prefix, internal_html=""):
    ext=(f'<a href="{RES_IRS_LIMITS}" target="_blank" rel="noopener">IRS: IRA contribution limits</a>'
         f'<a href="{RES_IRS_590B}" target="_blank" rel="noopener">IRS Pub 590-B: distributions &amp; RMDs</a>'
         f'<a href="{RES_IRC408}" target="_blank" rel="noopener">U.S. Code \u00a7408(m): allowed metals</a>'
         f'<a href="{RES_CFTC_METALS}" target="_blank" rel="noopener">CFTC: precious-metals fraud</a>'
         f'<a href="{RES_FTC_REPORT}" target="_blank" rel="noopener">FTC: report fraud</a>'
         f'<a href="{RES_USMINT}" target="_blank" rel="noopener">U.S. Mint</a>')
    more=(f'<p class="resmore">On Gold Advisor: {internal_html}</p>') if internal_html else ""
    return (f'<section class="resblock"><div class="wrap">'
            f'<h2 id="resources">Authoritative resources &amp; where to get help</h2>'
            f'<p>Verify the rules yourself and know where to turn. Official government and regulator sources:</p>'
            f'<div class="reslinks">{ext}</div>{more}'
            f'<p style="font-size:.86rem;color:var(--muted-2)">See the full <a href="{prefix}resources/index.html">Gold IRA rules, regulators &amp; resources hub</a> for IRS publications, how to vet a company, and where to file a complaint.</p>'
            f'</div></section>')

import hashlib
def _pk(slug, salt, opts):
    return opts[int(hashlib.md5((slug+salt).encode()).hexdigest(),16) % len(opts)]

FEDHEAD=["The federal rules don't change by state","Gold IRA rules are federal — same nationwide","Same federal rulebook, coast to coast","Your IRA rules are set in Washington, not the statehouse"]
FAQ_STORAGE=[
 "No — not at home, and not in a safe-deposit box. Whether you're in {place} or anywhere else, IRA metal has to sit with an IRS-approved depository through your custodian. Bring it home and the IRS treats it as a distribution.",
 "Only through your custodian, at an approved depository. Keeping IRA gold yourself in {place} counts as a taxable withdrawal, so it's a hard no.",
 "Short answer: no. IRA-owned metal stays at an IRS-approved depository in your name — never your house, even in {place}. Personal possession triggers a taxable event."]
FAQ_ROLLOVER=[
 "Usually yes. A direct rollover from a 401(k) into a self-directed IRA moves the money without taxes or the early-withdrawal penalty. The details shift a little depending on whether it's a current or former employer.",
 "Yes — that's the common route. Done as a direct (trustee-to-trustee) transfer, rolling a 401(k) into a Gold IRA from {place} is generally tax-free. An old employer's plan is usually the easiest to move.",
 "Most people can. A direct rollover into a self-directed IRA avoids the tax hit and the 10% penalty; just don't take the cash yourself first."]

STATE_TITLE=[
 "Buy Gold in {place}: Sales Tax + Gold IRA Guide (2026) - Gold Advisor",
 "Gold IRA & Bullion Tax in {place} (2026) - Gold Advisor",
 "How to Invest in Gold in {place} (2026) - Gold Advisor"]
STATE_SHORT={
 "EX":["{place} generally exempts investment-grade bullion from sales tax, and Gold IRA rules are federal — so opening one works the same as anywhere.",
       "Good news in {place}: most investment bullion is sales-tax exempt, and the Gold IRA side is federal, so it's identical to everywhere else."],
 "NT":["{place} has no statewide sales tax, so bullion is generally tax-free — and Gold IRA rules are federal anyway.",
       "No statewide sales tax in {place} means bullion is usually tax-free at the register; the Gold IRA rules are federal."],
 "TAX":["{place} generally taxes bullion purchases, but Gold IRA rules are federal — so the IRA itself works the same here as anywhere.",
        "Heads up: {place} usually taxes bullion at the counter. The Gold IRA part, though, is federal and unaffected."],
 "PART":["{place} exempts larger bullion buys but may tax smaller ones; the Gold IRA rules themselves are federal.",
         "In {place} it's a split: bigger purchases often qualify for exemption, smaller ones may be taxed. Gold IRA rules stay federal."],
 "VER":["{place}'s bullion sales-tax status changed recently — worth verifying — while Gold IRA rules stay federal.",
        "{place} recently changed its bullion tax treatment, so confirm it; the Gold IRA rules don't change either way."]}
STATE_LEAD=[
 "Thinking about gold in {place}? It really comes down to two things — what you pay in sales tax on coins and bars, and how a Gold IRA is treated (that part's federal, so it's the same everywhere).",
 "{place} buyers usually have two questions about gold: is there tax at the register, and is a Gold IRA worth it? We'll take both, starting with the {place}-specific piece.",
 "Here in {place} ({nick}), gold investing splits in two: metal you buy and hold, and gold inside a tax-advantaged IRA. The first depends on state law; the second doesn't.",
 "Gold's popular across {reg}, and {place} is no exception. Below: the state's bullion-tax situation first, then the federal Gold IRA rules that apply wherever you live."]
STATE_INTRO=[
 "The split is simple. Buying physical gold in {place} can mean paying state sales tax, depending on the rule below. A Gold IRA follows one federal rulebook — custodian, approved metals, depository, the whole thing.",
 "Most people land here for one of two reasons: they want to buy coins or bars in {place}, or they're weighing a Gold IRA rollover. The tax piece is local; the IRA piece is federal. Here's how each works.",
 "Being in {place} ({nick}) doesn't change how a Gold IRA operates — that's set federally. What the state can affect is the sales tax on a direct purchase, which we cover next.",
 "Two routes, one page. Route one is buying metal outright in {place}, where sales tax may apply. Route two is a Gold IRA — federal rules, identical to opening one anywhere else."]
STATE_FEDBLOCK=[
 "A <strong>Gold IRA</strong> runs on <strong>federal</strong> law, so it works the same in {place} as it does anywhere. State and local rules really only touch sales tax on direct buys — not how the account is set up, which metals qualify, or where they're stored.",
 "Whatever {place} does with sales tax, the <strong>Gold IRA</strong> side is <strong>federal</strong> and uniform: same approved-metals list, same custodian-and-depository setup, same contribution limits in every state.",
 "Don't overthink the location part. The <strong>federal</strong> rules — eligible metals, storage, limits — are identical in all 50 states. {place} only matters when you buy metal directly and sales tax might apply."]
STATE_ANGLE=[
 "One thing worth saying: gold is a long-term holding, not a quick flip. Most {place} investors we hear from use it to diversify a retirement account rather than to trade.",
 "If you're rolling over an old 401(k) from a {place} employer, a direct trustee-to-trustee transfer is usually the cleanest way to skip any tax hit.",
 "A quick reality check — dealers in and around {place} vary a lot on premiums, so it pays to compare a couple before you commit. Same goes for IRA providers.",
 "Storage trips people up. Even in {place}, IRA metal can't sit in your house; it lives at an approved depository, which is actually better for insurance and resale anyway.",
 "Worth flagging for {place} readers: 'free silver' and 'zero fees' promos almost always have strings attached. Read the fee schedule before you sign anything."]

CITY_STATUS={"EX":"generally exempt","NT":"with no statewide sales tax","TAX":"generally taxable","PART":"partly exempt","VER":"recently changed"}
CITY_TITLE=[
 "Buy Gold in {place}: Sales Tax + Gold IRA (2026) - Gold Advisor",
 "Gold & Gold IRA in {name} (2026) - Gold Advisor",
 "How to Invest in Gold in {name} (2026) - Gold Advisor"]
CITY_SHORT=[
 "{name} is in {sname}, where bullion is {status}. Gold IRA rules are federal, so opening one in {name} works the same as anywhere.",
 "In {name}, bullion is {status} under {sname} law — but the Gold IRA side is federal, so it's identical to everywhere else.",
 "Buying in {name}? Bullion there is {status} ({sname} rules), while a Gold IRA follows federal law no matter the city."]
CITY_LEAD=[
 "Buying gold in {name}? Two things matter — the sales tax {sname} charges (plus any local add-on), and how a Gold IRA is taxed (federal, so it's the same everywhere).",
 "{name} sits in {sname}, and gold buyers here juggle two questions: what they'll pay at the counter, and whether a Gold IRA makes sense. We'll cover both.",
 "For {name} investors, gold comes in two flavors: metal you buy and hold (where {sname} tax rules apply) and gold inside a tax-advantaged IRA (federal rules).",
 "Plenty of {name} residents are eyeing gold right now. We start with the {sname} tax picture, then the federal Gold IRA rules that don't change city to city."]
CITY_INTRO=[
 "Here's the practical split for {name}: a direct purchase may carry {sname} sales tax — and sometimes a city or county tax on top — while a Gold IRA runs on one federal rulebook.",
 "Most folks reading this either want to buy coins in {name} or are weighing a rollover. The tax part is local to {sname}; the IRA part is federal and identical nationwide.",
 "Being in {name} doesn't change how a Gold IRA works — that's federal. What {sname} can affect is the sales tax on metal you buy outright, which we get into below.",
 "Two paths, one page. Buy metal in {name} (watch for {sname} and any local tax), or open a Gold IRA (federal rules, same as anywhere)."]
CITY_FEDBLOCK=[
 "A <strong>Gold IRA</strong> is governed by <strong>federal</strong> law, so it works the same in {name} as anywhere. Local rules only really affect sales tax on a direct purchase — not the account itself.",
 "No matter what {name} or its county charges at the register, the <strong>Gold IRA</strong> side is <strong>federal</strong>: same eligible metals, same custodian and depository setup, same limits.",
 "The <strong>federal</strong> rules — which metals qualify, how it's stored, the annual limits — are identical everywhere. {name} only enters the picture for sales tax on metal you buy outright."]
CITY_ANGLE=[
 "One note for {name} buyers: local coin shops and national dealers price very differently, so it's worth getting a couple of quotes before you commit.",
 "If you've got an old 401(k) from a {name}-area job, a direct rollover is usually the simplest way into a Gold IRA without a tax bill.",
 "Quick reminder — even in {name}, IRA metal can't live in your home. It goes to an approved depository, which keeps the tax treatment intact.",
 "Heads up for {name} readers: 'free metal' and 'no-fee' offers usually bury the cost somewhere else. Check the full fee schedule first."]

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
   +'<a class="go primary" data-aff="'+c.k+'" rel="nofollow sponsored" href="#">Visit '+c.n.split(" ")[0]+' \\u2192</a>'+(c.k==="augusta"?'<a class="cta-phone" href="tel:+18449172904">\U0001F4DE 844-917-2904</a>':'')
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
           f'    <a href="{prefix}tools/gold-ira-rmd-calculator/index.html"><span>RMD calculator</span><em>Required distributions at 73+</em></a>\n'
           f'    <a href="{prefix}gold-price-widget/index.html"><span>Gold price widget</span><em>Embed live prices on your site</em></a>\n')
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
    L.append(f"- [Free gold & silver price widget (embeddable)]({B}/gold-price-widget/)")
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


def build_contact():
    prefix="../"
    canonical="https://gold-advisor.com/contact/"
    title="Contact Us | Gold Advisor"
    desc="Get in touch with the Gold Advisor team \u2014 questions about gold IRAs, corrections, feedback, or partnership ideas. We read every message."
    form=('<form action="https://formsubmit.co/advisor@ace.biz" method="POST" class="cform">'
      '<input type="hidden" name="_subject" value="Gold Advisor \u2014 new contact message">'
      '<input type="hidden" name="_captcha" value="false">'
      '<input type="hidden" name="_template" value="table">'
      '<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">'
      '<label>Your name<input type="text" name="name" required></label>'
      '<label>Email<input type="email" name="email" required></label>'
      '<label>Topic<select name="topic"><option>General question</option><option>Gold IRA or rollover help</option><option>Company review or correction</option><option>Feedback</option><option>Partnership or media</option></select></label>'
      '<label>Message<textarea name="message" rows="6" required></textarea></label>'
      '<button type="submit" class="cbtn">Send message</button></form>')
    content=('<div class="answer">Have a question about gold IRAs, spotted something that needs correcting, or want to work with us? Drop a note below and it lands straight in our inbox.</div>'
      +form+
      f'<p style="margin-top:14px">Prefer email? Reach us directly at <a href="mailto:advisor@ace.biz">advisor@ace.biz</a>. We usually reply within a couple of business days.</p>'
      '<h2>What we can (and can\u2019t) help with</h2>'
      '<p>We\u2019re an independent research and education site. We\u2019re glad to point you to the right rules, explain how a gold IRA works, or fix an error on the site. What we can\u2019t do is give personalized financial, tax, or legal advice \u2014 for that, please talk to a licensed professional.</p>'
      f'<p>If you need to report a problem with a specific company, the regulators and review platforms on our <a href="{prefix}resources/index.html">resources page</a> are the right place to start.</p>'
      f'<div class="related"><a href="{prefix}resources/index.html">Rules &amp; resources</a><a href="{prefix}gold-ira-scams/index.html">Avoid scams</a><a href="{prefix}about/index.html">About us</a><a href="{prefix}methodology/index.html">Methodology</a></div>')
    style=('.cform{display:grid;gap:14px;max-width:560px;margin:18px 0}'
      '.cform label{display:flex;flex-direction:column;gap:6px;font-weight:600;color:var(--navy);font-size:.92rem}'
      '.cform input,.cform select,.cform textarea{font:inherit;padding:11px 13px;border:1px solid var(--line);border-radius:10px;background:var(--surface);color:var(--ink)}'
      '.cform input:focus,.cform select:focus,.cform textarea:focus{outline:none;border-color:var(--gold)}'
      '.cbtn{justify-self:start;background:var(--cta);color:#fff;border:none;font-weight:700;padding:13px 28px;border-radius:11px;font-size:1rem;cursor:pointer;box-shadow:0 8px 20px rgba(30,158,87,.3)}'
      '.cbtn:hover{filter:brightness(1.05)}')
    sch=schema([("Home","https://gold-advisor.com/"),("Contact",canonical)],[])
    body=_shell(prefix,"Contact","Get in touch","Contact Gold Advisor",
        "Questions, corrections, feedback, or partnership ideas \u2014 here is how to reach us.",
        content, footer(prefix), byline=False, extra_style=style)
    return page(title,desc,canonical,prefix,sch,body)

def build_privacy():
    prefix="../"
    canonical="https://gold-advisor.com/privacy-policy/"
    title="Privacy Policy | Gold Advisor"
    desc="How Gold-Advisor.com collects, uses, and protects information, including contact-form data, cookies, analytics, and affiliate-link tracking."
    H=lambda t:f"<h2>{t}</h2>"
    content=('<div class="answer">This policy explains what we collect on Gold-Advisor.com, why, and what choices you have. We keep data collection to a minimum and we do not sell your personal information.</div>'
      f'<p style="color:var(--muted-2);font-size:.9rem">Last updated <span class="ga-now">June 2026</span>.</p>'
      +H("Who we are")+f'<p>Gold-Advisor.com (\u201cGold Advisor,\u201d \u201cwe,\u201d \u201cus\u201d) is an independent education and research website about buying physical gold and gold IRAs. You can reach us any time at <a href="mailto:advisor@ace.biz">advisor@ace.biz</a>.</p>'
      +H("Information we collect")+'<p><strong>Information you give us.</strong> If you use our contact form, we collect your name, email address, chosen topic, and message so we can reply. The form is delivered to us through a third-party form service; your message is transmitted to our email inbox.</p>'
      '<p><strong>Information collected automatically.</strong> Like most sites, our servers and analytics tools may log your IP address, browser type, device, referring page, and the pages you view. This is used in aggregate to understand traffic and improve the site.</p>'
      '<p><strong>Cookies.</strong> We use essential cookies for the site to function and may use analytics cookies to measure visits. When you click an affiliate link, the partner company may set its own cookie to credit the referral. You can block or delete cookies in your browser settings.</p>'
      +H("How we use information")+'<p>We use the information above to respond to your messages, operate and improve the site, measure traffic, keep the site secure, and comply with legal obligations. We do not use your contact details to send marketing unless you ask us to.</p>'
      +H("Affiliate links")+'<p>Some links to gold IRA companies are affiliate links. If you click one and open an account, we may earn a commission at no extra cost to you. Those companies may collect their own information under their own privacy policies once you leave our site \u2014 we encourage you to read them.</p>'
      +H("Third parties we rely on")+'<p>We share limited data with service providers that help us run the site: our web host and content-delivery network, our analytics provider, our contact-form delivery service, and affiliate networks/partners. <strong>We do not sell your personal information</strong>, and we do not share it except as needed to provide the site or as required by law. <em>(Operators: list your specific analytics and form providers here.)</em></p>'
      +H("Your choices and rights")+'<p>You can opt out of analytics cookies through your browser or an opt-out tool, and you can email us to ask what we hold or to request deletion. If you are in California (CCPA/CPRA), you have the right to know, delete, and opt out of the \u201csale\u201d or \u201csharing\u201d of personal information \u2014 note we do not sell it. If you are in the EEA or UK (GDPR), you have rights to access, correct, erase, restrict, or object to processing, and to lodge a complaint with your data-protection authority. To exercise any of these, email <a href="mailto:advisor@ace.biz">advisor@ace.biz</a>.</p>'
      +H("Data retention")+'<p>We keep contact messages only as long as needed to handle your request and for reasonable record-keeping, and server/analytics logs for a limited period, after which they are deleted or anonymized.</p>'
      +H("Security")+'<p>We use reasonable technical and organizational measures to protect information, but no website or transmission is perfectly secure, so we cannot guarantee absolute security.</p>'
      +H("Children\u2019s privacy")+'<p>This site is intended for adults making retirement and investment decisions. It is not directed to children, and we do not knowingly collect personal information from anyone under 13 (or under 18 for the topics covered here). If you believe a child has provided us information, contact us and we will delete it.</p>'
      +H("Do Not Track")+'<p>Some browsers send a \u201cDo Not Track\u201d signal. There is no industry standard for responding to it, so we currently treat all visitors the same; you can still control cookies as described above.</p>'
      +H("Changes to this policy")+'<p>We may update this policy as the site or the law changes. We will revise the \u201clast updated\u201d date above when we do; material changes will be made clear on this page.</p>'
      +H("Contact us")+f'<p>Questions about privacy? Email <a href="mailto:advisor@ace.biz">advisor@ace.biz</a>.</p>'
      f'<p style="font-size:.84rem;color:var(--muted-2)">This policy is a good-faith template for this site\u2019s scope and is not legal advice; please have it reviewed by qualified counsel and add your legal entity name and jurisdiction before relying on it.</p>'
      f'<div class="related"><a href="{prefix}terms-of-use/index.html">Terms of Use</a><a href="{prefix}contact/index.html">Contact</a><a href="{prefix}about/index.html">About</a></div>')
    sch=schema([("Home","https://gold-advisor.com/"),("Privacy Policy",canonical)],[])
    body=_shell(prefix,"Privacy Policy","Legal","Privacy Policy",
        "What we collect on Gold-Advisor.com, how we use it, and the choices you have.",
        content, footer(prefix), byline=False)
    return page(title,desc,canonical,prefix,sch,body)

def build_terms():
    prefix="../"
    canonical="https://gold-advisor.com/terms-of-use/"
    title="Terms of Use | Gold Advisor"
    desc="The terms governing your use of Gold-Advisor.com, including our educational-only disclaimer, affiliate disclosure, and limitation of liability."
    H=lambda t:f"<h2>{t}</h2>"
    content=('<div class="answer">By using Gold-Advisor.com you agree to these terms. Please read them \u2014 especially the part about this being education, not advice.</div>'
      f'<p style="color:var(--muted-2);font-size:.9rem">Last updated <span class="ga-now">June 2026</span>.</p>'
      +H("1. Acceptance")+'<p>These Terms of Use govern your access to and use of Gold-Advisor.com. If you do not agree, please do not use the site.</p>'
      +H("2. Educational purpose \u2014 not advice")+'<p><strong>Gold Advisor provides general educational information only.</strong> We are <strong>not</strong> a licensed financial, investment, tax, or legal advisor, and nothing on this site is personalized advice or a recommendation to buy, sell, or hold any asset. Using the site does not create any advisory or fiduciary relationship. Investing in gold and precious metals involves risk, including loss of value. Always do your own research and consult a licensed professional before making decisions.</p>'
      +H("3. Affiliate disclosure")+'<p>Some links to gold IRA companies are affiliate links, and we may earn a commission if you open an account through them, at no extra cost to you. This compensation helps keep the site free and may influence which companies are featured and how prominently \u2014 but it does not change our editorial assessments, which are our own opinions. Rankings, scores, and minimums shown may be illustrative and should be verified directly with each company.</p>'
      +H("4. Accuracy and no warranty")+'<p>We work to keep information correct and current, but rules \u2014 especially IRS and state tax rules \u2014 change, and the site may contain errors or become out of date. The site is provided \u201cas is\u201d and \u201cas available,\u201d without warranties of any kind, express or implied, including accuracy, fitness for a particular purpose, or non-infringement. Verify anything important with primary sources (such as the IRS) or a professional.</p>'
      +H("5. Third-party links and companies")+'<p>We link to third-party websites, regulators, and companies for convenience. We do not control and are not responsible for their content, products, policies, or practices, and a mention is not an endorsement or guarantee.</p>'
      +H("6. Intellectual property")+'<p>The content on this site (text, design, and graphics, excluding third-party trademarks and logos used for identification) is owned by us or our licensors and is protected by law. You may not copy, republish, or redistribute substantial portions without our written permission. Company names and logos are the property of their respective owners.</p>'
      +H("7. Acceptable use")+'<p>Do not use the site or contact form for unlawful, abusive, fraudulent, or spam purposes, and do not attempt to disrupt or gain unauthorized access to the site.</p>'
      +H("8. Limitation of liability")+'<p>To the fullest extent permitted by law, Gold Advisor and its operators will not be liable for any indirect, incidental, or consequential damages, or for any loss arising from your use of, or reliance on, the site or any third party it links to. Your sole remedy for dissatisfaction with the site is to stop using it.</p>'
      +H("9. Indemnification")+'<p>You agree to indemnify and hold harmless Gold Advisor and its operators from claims or expenses arising out of your misuse of the site or violation of these terms.</p>'
      +H("10. Governing law and changes")+'<p>These terms are governed by the laws of <em>[your state/country \u2014 insert jurisdiction]</em>, without regard to conflict-of-laws rules. If any provision is found unenforceable, the rest remain in effect. We may update these terms at any time; the \u201clast updated\u201d date will change when we do, and continued use means you accept the revised terms.</p>'
      +H("11. Contact")+f'<p>Questions about these terms? Email <a href="mailto:advisor@ace.biz">advisor@ace.biz</a>.</p>'
      f'<p style="font-size:.84rem;color:var(--muted-2)">These terms are a good-faith template for this site\u2019s scope and are not legal advice; please have qualified counsel review them and insert your legal entity name and jurisdiction before relying on them.</p>'
      f'<div class="related"><a href="{prefix}privacy-policy/index.html">Privacy Policy</a><a href="{prefix}contact/index.html">Contact</a><a href="{prefix}methodology/index.html">Methodology</a></div>')
    sch=schema([("Home","https://gold-advisor.com/"),("Terms of Use",canonical)],[])
    body=_shell(prefix,"Terms of Use","Legal","Terms of Use",
        "The rules for using Gold-Advisor.com, including our education-only disclaimer and affiliate disclosure.",
        content, footer(prefix), byline=False)
    return page(title,desc,canonical,prefix,sch,body)

def build_redirects():
    tpl = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
      '<meta name="robots" content="noindex,nofollow">'
      '<meta name="viewport" content="width=device-width,initial-scale=1">'
      '<link rel="canonical" href="https://gold-advisor.com/visit/__SLUG__/">'
      '<title>Redirecting to __NAME__\u2026</title>'
      '<script src="/affiliates.js"></script>'
      '<script>(function(){var k="__SLUG__";'
      'var u=(window.GA_URL&&window.GA_URL[k])||(window.GA_CONFIG&&window.GA_CONFIG["__KEY__"]&&window.GA_CONFIG["__KEY__"].url);'
      'if(u){try{window.location.replace(u);}catch(e){window.location.href=u;}'
      'document.addEventListener("DOMContentLoaded",function(){var a=document.getElementById("go");if(a)a.setAttribute("href",u);});}})();</script>'
      '<style>body{font-family:system-ui,-apple-system,Segoe UI,Arial,sans-serif;background:#0f2742;color:#fff;display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0;text-align:center}'
      '.b{max-width:460px;padding:30px}.b a{color:#f0cf6a}.sp{display:inline-block;width:26px;height:26px;border:3px solid rgba(255,255,255,.3);border-top-color:#f0cf6a;border-radius:50%;animation:s .8s linear infinite;margin-bottom:14px}@keyframes s{to{transform:rotate(360deg)}}</style>'
      '</head><body><div class="b"><div class="sp"></div>'
      '<p>Taking you to <strong>__NAME__</strong>\u2026</p>'
      '<p>If you are not redirected automatically, <a id="go" rel="nofollow sponsored noopener" href="/">tap here to continue</a>.</p>'
      '</div></body></html>')
    for key, r in REVIEWS.items():
        html = tpl.replace("__SLUG__", r["slug"]).replace("__NAME__", r["name"]).replace("__KEY__", key)
        write(f"site/visit/{r['slug']}/index.html", html)

WIDGET_JS = r'''/*! Gold Advisor — Free Gold & Silver Price Widget
    Embed: <div class="goldadvisor-pricewidget" data-type="card" data-metal="gold"></div>
           <script src="https://gold-advisor.com/gold-price-widget/widget.js" async></script>
    Live spot: api.gold-api.com (free, CORS).  History: CoinGecko (free, CORS), rebased to live spot. */
(function () {
  "use strict";
  var LIVE = "https://api.gold-api.com/price/";
  var CG = "https://api.coingecko.com/api/v3/coins/";
  var CG_ID = { gold: "pax-gold", silver: "kinesis-silver" };
  var SYM = { gold: "XAU", silver: "XAG" };
  var NAME = { gold: "Gold", silver: "Silver" };
  var CREDIT = "https://gold-advisor.com/gold-price-widget/?utm_source=widget&utm_medium=referral&utm_campaign=price-widget";
  var CREDIT_HOME = "https://gold-advisor.com/?utm_source=widget&utm_medium=referral";
  var cache = (window.__GAPW = window.__GAPW || {});

  function getJSON(u) { return fetch(u, { mode: "cors" }).then(function (r) { if (!r.ok) throw 0; return r.json(); }); }
  function money(n) { return "$" + Number(n).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  function pct(n) { return (n >= 0 ? "+" : "") + n.toFixed(2) + "%"; }

  function live(metal) {
    var k = "L:" + metal;
    if (cache[k]) return cache[k];
    cache[k] = getJSON(LIVE + SYM[metal]).then(function (d) {
      return { price: +d.price, prev: (d.prev_close_price != null ? +d.prev_close_price : null), updated: d.updatedAt || null };
    });
    return cache[k];
  }
  function history(metal, days) {
    var k = "H:" + metal + ":" + days;
    if (cache[k]) return cache[k];
    var u = CG + CG_ID[metal] + "/market_chart?vs_currency=usd&days=" + days + (days > 90 ? "" : "&interval=daily");
    cache[k] = Promise.all([getJSON(u).catch(function () { return null; }), live(metal)]).then(function (a) {
      var h = a[0], lv = a[1];
      if (!h || !h.prices || h.prices.length < 2) return null;
      var pts = h.prices.map(function (p) { return [p[0], +p[1]]; });
      var last = pts[pts.length - 1][1];
      if (last > 0 && lv && lv.price) { var f = lv.price / last; pts = pts.map(function (p) { return [p[0], p[1] * f]; }); pts[pts.length - 1][1] = lv.price; }
      return pts;
    });
    return cache[k];
  }

  function svgChart(pts, w, h, accent, interactive, theme) {
    if (!pts || pts.length < 2) return "";
    var n = pts.length, pad = 4, ww = w - pad * 2, hh = h - pad * 2;
    var min = Infinity, max = -Infinity, i;
    for (i = 0; i < n; i++) { var v = pts[i][1]; if (v < min) min = v; if (v > max) max = v; }
    var rng = (max - min) || 1; min -= rng * 0.08; max += rng * 0.08; rng = max - min;
    function X(i) { return (pad + (i / (n - 1)) * ww).toFixed(1); }
    function Y(v) { return (pad + (1 - (v - min) / rng) * hh).toFixed(1); }
    var line = "M" + X(0) + " " + Y(pts[0][1]);
    for (i = 1; i < n; i++) line += " L" + X(i) + " " + Y(pts[i][1]);
    var area = line + " L" + X(n - 1) + " " + (h - pad) + " L" + X(0) + " " + (h - pad) + " Z";
    var up = pts[n - 1][1] >= pts[0][1];
    var stroke = accent, gid = "g" + Math.random().toString(36).slice(2, 8);
    var grid = theme === "dark" ? "rgba(255,255,255,.07)" : "rgba(15,39,66,.06)";
    var s = '<svg class="gapw-svg" viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none" width="100%" height="' + h + '" xmlns="http://www.w3.org/2000/svg">';
    s += '<defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="0" y2="1">';
    s += '<stop offset="0" stop-color="' + stroke + '" stop-opacity="0.28"/><stop offset="1" stop-color="' + stroke + '" stop-opacity="0"/></linearGradient></defs>';
    s += '<line x1="' + pad + '" y1="' + (h / 2) + '" x2="' + (w - pad) + '" y2="' + (h / 2) + '" stroke="' + grid + '" stroke-width="1"/>';
    s += '<path d="' + area + '" fill="url(#' + gid + ')"/>';
    s += '<path d="' + line + '" fill="none" stroke="' + stroke + '" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>';
    s += '<circle cx="' + X(n - 1) + '" cy="' + Y(pts[n - 1][1]) + '" r="3.2" fill="' + stroke + '"/>';
    if (interactive) {
      s += '<line class="gapw-cl" x1="0" y1="' + pad + '" x2="0" y2="' + (h - pad) + '" stroke="' + stroke + '" stroke-width="1" stroke-dasharray="3 3" opacity="0"/>';
      s += '<circle class="gapw-cd" cx="0" cy="0" r="3.6" fill="#fff" stroke="' + stroke + '" stroke-width="2" opacity="0"/>';
    }
    s += '</svg>';
    return { svg: s, X: X, Y: Y, up: up };
  }

  function styleOnce() {
    if (document.getElementById("gapw-style")) return;
    var css =
    ".gapw{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;box-sizing:border-box;border:1px solid var(--gapw-line);border-radius:14px;background:var(--gapw-bg);color:var(--gapw-ink);padding:14px 16px;max-width:100%;line-height:1.3;-webkit-font-smoothing:antialiased}" +
    ".gapw *{box-sizing:border-box}" +
    ".gapw.light{--gapw-bg:#fff;--gapw-ink:#0f2742;--gapw-mut:#6b7787;--gapw-line:#e7e2d6}" +
    ".gapw.dark{--gapw-bg:#0f1b2d;--gapw-ink:#f4f7fb;--gapw-mut:#9fb0c3;--gapw-line:#22344b}" +
    ".gapw-hd{display:flex;align-items:baseline;justify-content:space-between;gap:10px;flex-wrap:wrap}" +
    ".gapw-name{font-weight:700;font-size:.82rem;letter-spacing:.02em;color:var(--gapw-mut);text-transform:uppercase;margin:0}" +
    ".gapw-price{font-weight:800;font-size:1.7rem;letter-spacing:-.01em;margin:2px 0}" +
    ".gapw-mini .gapw-price{font-size:1.25rem}" +
    ".gapw-full .gapw-price{font-size:2.1rem}" +
    ".gapw-chg{font-weight:700;font-size:.82rem;padding:3px 9px;border-radius:30px;white-space:nowrap}" +
    ".gapw-chg.up{color:#0c7a43;background:rgba(16,160,89,.12)}.gapw-chg.dn{color:#c0341d;background:rgba(192,52,29,.12)}" +
    ".gapw-sub{font-size:.72rem;color:var(--gapw-mut)}" +
    ".gapw-chart{position:relative;margin:10px 0 6px}" +
    ".gapw-tip{position:absolute;pointer-events:none;background:var(--gapw-ink);color:var(--gapw-bg);font-size:.72rem;font-weight:600;padding:4px 8px;border-radius:7px;transform:translate(-50%,-130%);white-space:nowrap;opacity:0;transition:opacity .1s}" +
    ".gapw-rng{display:flex;gap:6px;margin-top:4px}" +
    ".gapw-rng button{font:inherit;font-size:.74rem;font-weight:600;color:var(--gapw-mut);background:transparent;border:1px solid var(--gapw-line);border-radius:7px;padding:3px 10px;cursor:pointer}" +
    ".gapw-rng button.on{color:#fff;background:var(--gapw-accent);border-color:var(--gapw-accent)}" +
    ".gapw-tabs{display:flex;gap:6px;margin-bottom:4px}" +
    ".gapw-tabs button{font:inherit;font-size:.78rem;font-weight:700;color:var(--gapw-mut);background:transparent;border:none;border-bottom:2px solid transparent;padding:2px 4px;cursor:pointer}" +
    ".gapw-tabs button.on{color:var(--gapw-ink);border-bottom-color:var(--gapw-accent)}" +
    ".gapw-ft{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:8px;border-top:1px solid var(--gapw-line);padding-top:8px}" +
    ".gapw-ft a{color:var(--gapw-accent);font-weight:700;font-size:.74rem;text-decoration:none}" +
    ".gapw-ft a:hover{text-decoration:underline}" +
    ".gapw-ft span{font-size:.66rem;color:var(--gapw-mut)}" +
    ".gapw-mini .gapw-ft{margin-top:6px;padding-top:6px}" +
    ".gapw-row{display:flex;gap:14px;flex-wrap:wrap}.gapw-row>.gapw-cell{flex:1 1 130px;min-width:120px}" +
    ".gapw-cell .gapw-price{font-size:1.3rem}";
    var st = document.createElement("style"); st.id = "gapw-style"; st.textContent = css; document.head.appendChild(st);
  }

  function changeFrom(lv, pts) {
    if (lv && lv.prev) return { v: (lv.price - lv.prev) / lv.prev * 100, lbl: "today" };
    if (pts && pts.length > 1) return { v: (pts[pts.length - 1][1] - pts[0][1]) / pts[0][1] * 100, lbl: "period" };
    return null;
  }

  function attachCrosshair(box, pts, built, accent) {
    var svg = box.querySelector(".gapw-svg"), tip = box.querySelector(".gapw-tip");
    var cl = box.querySelector(".gapw-cl"), cd = box.querySelector(".gapw-cd");
    if (!svg || !cl) return;
    function move(e) {
      var r = svg.getBoundingClientRect(), x = ((e.touches ? e.touches[0].clientX : e.clientX) - r.left) / r.width;
      var i = Math.max(0, Math.min(pts.length - 1, Math.round(x * (pts.length - 1))));
      var px = built.X(i), py = built.Y(pts[i][1]);
      cl.setAttribute("x1", px); cl.setAttribute("x2", px); cl.setAttribute("opacity", "0.7");
      cd.setAttribute("cx", px); cd.setAttribute("cy", py); cd.setAttribute("opacity", "1");
      tip.style.opacity = "1"; tip.style.left = (px / 1000 * r.width) + "px"; tip.style.top = (py / parseFloat(svg.getAttribute("height")) * r.height) + "px";
      var d = new Date(pts[i][0]);
      tip.innerHTML = money(pts[i][1]) + " &middot; " + d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
    }
    function leave() { cl.setAttribute("opacity", "0"); cd.setAttribute("opacity", "0"); tip.style.opacity = "0"; }
    svg.addEventListener("mousemove", move); svg.addEventListener("touchmove", move); svg.addEventListener("mouseleave", leave); svg.addEventListener("touchend", leave);
  }

  function render(node) {
    styleOnce();
    var type = (node.getAttribute("data-type") || "card").toLowerCase();
    var metal = (node.getAttribute("data-metal") || "gold").toLowerCase();
    var theme = (node.getAttribute("data-theme") || "light").toLowerCase();
    var accent = node.getAttribute("data-accent") || "#c69320";
    var days = parseInt(node.getAttribute("data-range") || "30", 10) || 30;
    var both = metal === "both";
    var active = both ? "gold" : metal;
    var H = type === "full" ? 240 : (type === "mini" ? 44 : 120);
    var existing = node.querySelector("a"); // keep the backlink the publisher pasted

    node.className = "gapw " + theme + " gapw-" + type;
    node.style.setProperty("--gapw-accent", accent);
    node.innerHTML = "";

    var hd = document.createElement("div"); hd.className = "gapw-hd"; node.appendChild(hd);
    var left = document.createElement("div"); hd.appendChild(left);
    var nm = document.createElement("p"); nm.className = "gapw-name"; left.appendChild(nm);
    var pr = document.createElement("div"); pr.className = "gapw-price"; pr.textContent = "—"; left.appendChild(pr);
    var sub = document.createElement("div"); sub.className = "gapw-sub"; left.appendChild(sub);
    var chg = document.createElement("span"); chg.className = "gapw-chg"; hd.appendChild(chg);

    var chartBox = null, rng = null, tabs = null;
    if (type !== "mini") {
      if (both) {
        tabs = document.createElement("div"); tabs.className = "gapw-tabs";
        ["gold", "silver"].forEach(function (m) { var b = document.createElement("button"); b.textContent = NAME[m]; b.dataset.m = m; if (m === active) b.className = "on"; tabs.appendChild(b); });
        node.appendChild(tabs);
      }
      chartBox = document.createElement("div"); chartBox.className = "gapw-chart";
      var tip = document.createElement("div"); tip.className = "gapw-tip";
      node.appendChild(chartBox); chartBox.appendChild(tip);
      if (type === "full") {
        rng = document.createElement("div"); rng.className = "gapw-rng";
        [7, 30, 90].forEach(function (d) { var b = document.createElement("button"); b.textContent = d + "D"; b.dataset.d = d; if (d === days) b.className = "on"; rng.appendChild(b); });
        node.appendChild(rng);
      }
    } else {
      chartBox = document.createElement("div"); chartBox.className = "gapw-chart"; node.appendChild(chartBox);
    }

    var ft = document.createElement("div"); ft.className = "gapw-ft";
    var a = document.createElement("a"); a.href = (existing && existing.getAttribute("href")) || CREDIT;
    a.target = "_blank"; a.rel = "noopener"; a.textContent = existing && existing.textContent ? existing.textContent : "Live prices by Gold Advisor";
    if (a.href.indexOf("gold-advisor.com") < 0) { a.href = CREDIT; }
    var src = document.createElement("span"); ft.appendChild(a); ft.appendChild(src); node.appendChild(ft);

    function paint(m, d) {
      nm.textContent = NAME[m] + (type === "mini" ? "" : " spot price");
      Promise.all([live(m), history(m, d)]).then(function (res) {
        var lv = res[0], pts = res[1];
        pr.textContent = money(lv.price);
        var c = changeFrom(lv, pts);
        if (c) { chg.textContent = pct(c.v) + (type === "mini" ? "" : " " + c.lbl); chg.className = "gapw-chg " + (c.v >= 0 ? "up" : "dn"); } else chg.textContent = "";
        if (sub) sub.textContent = type === "full" ? ("per troy ounce (USD)") : "";
        if (chartBox) {
          var w = type === "mini" ? 220 : (type === "full" ? 1000 : 520);
          var built = svgChart(pts, w, H, accent, type !== "mini", theme);
          var tipEl = chartBox.querySelector(".gapw-tip");
          chartBox.innerHTML = built ? built.svg : '<div class="gapw-sub">Live: ' + money(lv.price) + '</div>';
          if (tipEl) chartBox.appendChild(tipEl);
          if (built && type !== "mini") attachCrosshair(chartBox, pts, built, accent);
        }
        src.textContent = "Source: gold-api.com, CoinGecko";
      }).catch(function () { pr.textContent = "Unavailable"; });
    }

    if (tabs) tabs.addEventListener("click", function (e) { if (e.target.dataset.m) { active = e.target.dataset.m; [].forEach.call(tabs.children, function (b) { b.className = b.dataset.m === active ? "on" : ""; }); paint(active, days); } });
    if (rng) rng.addEventListener("click", function (e) { if (e.target.dataset.d) { days = +e.target.dataset.d; [].forEach.call(rng.children, function (b) { b.className = (+b.dataset.d === days) ? "on" : ""; }); paint(active, days); } });

    paint(active, days);
    if (!node.__gapwTimer) node.__gapwTimer = setInterval(function () { cache["L:" + active] = null; paint(active, days); }, 60000);
  }

  function init() { var list = document.querySelectorAll(".goldadvisor-pricewidget"); for (var i = 0; i < list.length; i++) if (!list[i].__gapwDone) { list[i].__gapwDone = 1; render(list[i]); } }
  window.GoldAdvisorWidget = { render: render, init: init };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
'''

def build_gold_widget_page():
    prefix="../"
    canonical="https://gold-advisor.com/gold-price-widget/"
    title="Free Gold Price Widget & Embed Code — Live Gold & Silver Charts | Gold Advisor"
    desc="Add a free, live gold and silver price widget to your website. Real-time price charts in three sizes, custom colors, no API key — copy one line to embed."

    gen = """<div class="pw-gen">
      <div class="pw-controls">
        <label>Widget type<select id="pw-type"><option value="mini">Mini — sidebar</option><option value="card" selected>Card — in content</option><option value="full">Full — interactive</option></select></label>
        <label>Metal<select id="pw-metal"><option value="gold" selected>Gold</option><option value="silver">Silver</option><option value="both">Gold + Silver</option></select></label>
        <label>Theme<select id="pw-theme"><option value="light" selected>Light</option><option value="dark">Dark</option></select></label>
        <label>Accent<input type="color" id="pw-accent" value="#c69320"></label>
        <label>History<select id="pw-range"><option>7</option><option selected>30</option><option>90</option></select></label>
      </div>
      <div class="pw-preview"><div id="pw-demo" class="goldadvisor-pricewidget" data-type="card" data-metal="gold" data-theme="light" data-accent="#c69320" data-range="30"><a href="https://gold-advisor.com/?utm_source=widget&amp;utm_medium=referral">Live gold &amp; silver prices by Gold Advisor</a></div></div>
      <div class="pw-codelbl"><span>Copy this embed code</span><button id="pw-copy" type="button">Copy code</button></div>
      <textarea id="pw-code" rows="4" readonly></textarea>
    </div>"""

    demos = """<div class="pw-demos">
      <div class="demo-wrap"><h4>Mini · sidebar</h4><div class="goldadvisor-pricewidget" data-type="mini" data-metal="gold" data-accent="#c69320"><a href="https://gold-advisor.com/?utm_source=widget">Gold price by Gold Advisor</a></div></div>
      <div class="demo-wrap"><h4>Card · in content</h4><div class="goldadvisor-pricewidget" data-type="card" data-metal="silver" data-accent="#3a6ea5"><a href="https://gold-advisor.com/?utm_source=widget">Silver price by Gold Advisor</a></div></div>
    </div>
    <div class="demo-wrap full"><h4>Full · interactive (gold + silver, hover the chart)</h4><div class="goldadvisor-pricewidget" data-type="full" data-metal="both" data-range="30" data-accent="#c69320"><a href="https://gold-advisor.com/?utm_source=widget">Gold &amp; silver prices by Gold Advisor</a></div></div>"""

    GENJS = r'''
(function(){
 var $=function(i){return document.getElementById(i);};
 var T=$('pw-type'),M=$('pw-metal'),TH=$('pw-theme'),AC=$('pw-accent'),RG=$('pw-range');
 var demo=$('pw-demo'),code=$('pw-code'),copy=$('pw-copy');
 var codeF=$('pw-code-iframe');
 function snip(){
   var a='data-type="'+T.value+'" data-metal="'+M.value+'" data-theme="'+TH.value+'" data-accent="'+AC.value+'" data-range="'+RG.value+'"';
   return '<div class="goldadvisor-pricewidget" '+a+'><a href="https://gold-advisor.com/?utm_source=widget&amp;utm_medium=referral">Live gold &amp; silver prices by Gold Advisor</a></div>\n<script src="https://gold-advisor.com/gold-price-widget/widget.js" async></scr'+'ipt>';
 }
 function snipIframe(){
   var u='https://gold-advisor.com/gold-price-widget/embed.html?type='+T.value+'&metal='+M.value+'&theme='+TH.value+'&accent='+encodeURIComponent(AC.value)+'&range='+RG.value;
   var h=T.value==='mini'?90:(T.value==='full'?330:240);
   return '<iframe src="'+u+'" width="100%" height="'+h+'" style="border:0;overflow:hidden" loading="lazy" title="Gold and silver price widget by Gold Advisor"></iframe>';
 }
 function upd(){
   demo.setAttribute('data-type',T.value);demo.setAttribute('data-metal',M.value);demo.setAttribute('data-theme',TH.value);demo.setAttribute('data-accent',AC.value);demo.setAttribute('data-range',RG.value);
   if(demo.__gapwTimer){clearInterval(demo.__gapwTimer);demo.__gapwTimer=null;}
   demo.__gapwDone=0;
   demo.innerHTML='<a href="https://gold-advisor.com/?utm_source=widget">Live gold &amp; silver prices by Gold Advisor</a>';
   if(window.GoldAdvisorWidget){window.GoldAdvisorWidget.render(demo);}
   code.value=snip();if(codeF){codeF.value=snipIframe();}
 }
 [T,M,TH,AC,RG].forEach(function(x){x.addEventListener('change',upd);x.addEventListener('input',upd);});
 copy.addEventListener('click',function(){code.select();try{document.execCommand('copy');}catch(e){}copy.textContent='Copied!';setTimeout(function(){copy.textContent='Copy code';},1500);});
 code.value=snip();if(codeF){codeF.value=snipIframe();}
})();
'''

    body_html = (
      '<link rel="preconnect" href="https://api.gold-api.com"><link rel="preconnect" href="https://api.coingecko.com">'
      '<div class="answer"><b>Want a live gold price on your site?</b> Pick a style below, copy the one-line embed code, and paste it into your page. It is free, needs no API key, and updates itself — all we ask is that you keep the small "by Gold Advisor" credit link.</div>'
      '<h2 id="builder">Build your gold price widget</h2>'
      '<p>Use the builder to set the size, metal, colors, and history range. The preview updates live and the embed code is generated for you.</p>'
      + gen +
      '<h2 id="sizes">Three widget sizes for any layout</h2>'
      '<p>Every size shows a live <strong>gold price</strong> (or silver), the change, and a clean price chart. Choose the one that fits where it will live on your page:</p>'
      + demos +
      '<ul>'
      '<li><strong>Mini</strong> — a compact price + sparkline, perfect for a <em>sidebar</em> or footer.</li>'
      '<li><strong>Card</strong> — price, daily change, and a 30-day chart for <em>in-content</em> placement.</li>'
      '<li><strong>Full</strong> — a large, <em>interactive</em> chart with a hover tooltip, a 7/30/90-day toggle, and an optional gold + silver switch.</li>'
      '</ul>'
      '<h2 id="how">How to embed the gold price widget</h2>'
      '<div class="steps">'
      '<div class="step"><h4>1. Build it</h4><p>Set the options above and hit <em>Copy code</em>.</p></div>'
      '<div class="step"><h4>2. Paste it</h4><p>Drop the snippet into your page&rsquo;s HTML where you want the chart.</p></div>'
      '<div class="step"><h4>3. Done</h4><p>The widget loads the live price and chart automatically. No account, no key.</p></div>'
      '</div>'
      '<p>The embed is just a <code>&lt;div&gt;</code> plus one <code>&lt;script&gt;</code> tag, so it works on WordPress, Wix, Squarespace, Ghost, plain HTML — anywhere you can paste code.</p>'
      '<h2 id="why">Why use the Gold Advisor price widget</h2>'
      '<ul>'
      '<li><strong>Free, forever</strong> — no signup, no API key, no usage caps.</li>'
      '<li><strong>Live &amp; accurate</strong> — spot prices refresh automatically about once a minute.</li>'
      '<li><strong>Gold and silver</strong> — show either metal, or both in one widget.</li>'
      '<li><strong>Lightweight</strong> — one small script, no jQuery or chart library to load.</li>'
      '<li><strong>Responsive</strong> — it fills its container and looks right on phones.</li>'
      '<li><strong>Yours to style</strong> — pick the accent color and a light or dark theme.</li>'
      '</ul>'
      '<h2 id="customize">Customization options</h2>'
      '<p>Everything is set with simple <code>data-</code> attributes on the <code>&lt;div&gt;</code>:</p>'
      '<ul>'
      '<li><code>data-type</code> — <code>mini</code>, <code>card</code>, or <code>full</code></li>'
      '<li><code>data-metal</code> — <code>gold</code>, <code>silver</code>, or <code>both</code></li>'
      '<li><code>data-theme</code> — <code>light</code> or <code>dark</code></li>'
      '<li><code>data-accent</code> — any hex color, e.g. <code>#c69320</code></li>'
      '<li><code>data-range</code> — <code>7</code>, <code>30</code>, or <code>90</code> days of history</li>'
      '</ul>'
      '<h2 id="other">Other ways to embed</h2>'
      '<p>The script embed above is best \u2014 it gives you the live chart <em>and</em> a real backlink. If your platform blocks scripts, use one of these:</p>'
      '<div class="pw-alt">'
      '<div class="pw-altcol"><h4>iframe (no script needed)</h4><p class="pw-fine">Reflects the options you picked above. Note: an iframe does <strong>not</strong> pass the SEO credit link.</p><textarea id="pw-code-iframe" rows="3" readonly onclick="this.select()"></textarea></div>'
      '<div class="pw-altcol"><h4>Static image badge</h4><p class="pw-fine">A lightweight image link \u2014 perfect when you can only add an image. Always carries the backlink.</p>'
      + f'<p><a href="https://gold-advisor.com/gold-price-widget/?utm_source=badge"><img src="{prefix}assets/img/price-badge.png" alt="Live gold &amp; silver prices by Gold Advisor" width="240" height="60" style="max-width:100%;height:auto"></a></p>'
      + '<textarea id="pw-code-badge" rows="3" readonly onclick="this.select()">&lt;a href="https://gold-advisor.com/gold-price-widget/?utm_source=badge"&gt;&lt;img src="https://gold-advisor.com/assets/img/price-badge.png" alt="Live gold &amp; silver prices by Gold Advisor" width="240" height="60"&gt;&lt;/a&gt;</textarea></div>'
      '</div>'
      '<h2 id="faq">Gold price widget FAQ</h2>'
      '<details open><summary>Is the gold price widget really free?</summary><p>Yes. It is completely free to embed on personal or commercial sites. The only condition is that you keep the visible &ldquo;by Gold Advisor&rdquo; credit link that comes with it.</p></details>'
      '<details><summary>Do I need an API key?</summary><p>No. There is nothing to sign up for and no key to manage. The widget fetches public price data on its own.</p></details>'
      '<details><summary>How do I embed a gold price chart on my website?</summary><p>Copy the embed code from the builder above and paste the <code>&lt;div&gt;</code> and <code>&lt;script&gt;</code> into your page&rsquo;s HTML. That is the whole setup.</p></details>'
      '<details><summary>Can I show the silver price too?</summary><p>Yes — set <code>data-metal</code> to <code>silver</code>, or to <code>both</code> for a gold + silver toggle in one widget.</p></details>'
      '<details><summary>Will it slow down my site?</summary><p>No. It is a single small script with no external chart library, and it loads asynchronously so it never blocks your page.</p></details>'
      '<details><summary>How accurate are the prices?</summary><p>The live spot price comes from a real-time precious-metals feed, and the chart history is rebased to that current spot. Prices are for information only, not a dealer quote.</p></details>'
      '<div class="callout"><h3>Usage &amp; credit</h3><p>You may embed the widget on any site for free. Please keep the &ldquo;by Gold Advisor&rdquo; link intact — that link is how we keep the widget free. Live spot data: gold-api.com; chart history: CoinGecko. Prices are informational and not investment advice.</p></div>'
      + f'<div class="related"><a href="{prefix}gold-ira-companies/index.html">Best Gold IRA companies</a><a href="{prefix}guides/how-to-buy-gold/index.html">How to buy gold</a><a href="{prefix}tools/index.html">Calculators &amp; tools</a><a href="{prefix}resources/index.html">Rules &amp; resources</a></div>'
      + '<script src="widget.js" async></script>'
      + '<script>' + GENJS + '</script>'
    )

    faqs=[("Is the gold price widget free?","Yes. It is free to embed on personal or commercial websites, with no API key or signup. The only condition is keeping the visible by Gold Advisor credit link."),
          ("Do I need an API key to use the gold price widget?","No. There is no key and nothing to sign up for; the widget fetches public price data automatically."),
          ("How do I embed a gold price chart on my website?","Copy the embed code from the builder and paste the div and script tags into your page HTML. It works on WordPress, Wix, Squarespace, and plain HTML."),
          ("Can the widget show silver prices?","Yes. Set data-metal to silver, or to both for a combined gold and silver widget.")]
    sch=schema([("Home","https://gold-advisor.com/"),("Gold Price Widget",canonical)],faqs)

    style=(".pw-gen{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:20px;box-shadow:var(--shadow);margin:18px 0}"
      ".pw-controls{display:flex;flex-wrap:wrap;gap:14px;margin-bottom:16px}"
      ".pw-controls label{display:flex;flex-direction:column;gap:5px;font-size:.78rem;font-weight:700;color:var(--navy)}"
      ".pw-controls select,.pw-controls input[type=color]{font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:9px;background:#fff;color:var(--ink)}"
      ".pw-controls input[type=color]{padding:2px;height:38px;width:56px;cursor:pointer}"
      ".pw-preview{display:flex;justify-content:center;padding:20px;background:var(--bg-2);border-radius:12px;margin-bottom:14px}"
      ".pw-preview .goldadvisor-pricewidget{width:100%;max-width:430px}"
      ".pw-codelbl{display:flex;align-items:center;justify-content:space-between;font-weight:700;color:var(--navy);font-size:.85rem;margin-bottom:6px}"
      "#pw-copy{background:var(--cta);color:#fff;border:none;border-radius:8px;padding:7px 16px;font-weight:700;cursor:pointer}"
      "#pw-copy:hover{filter:brightness(1.05)}"
      "#pw-code{width:100%;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.8rem;padding:12px;border:1px solid var(--line);border-radius:10px;background:#0f1b2d;color:#cde3ff;resize:vertical;line-height:1.5}"
      ".pw-demos{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px;align-items:start;margin:14px 0}"
      ".demo-wrap h4{margin:0 0 8px;font-size:.78rem;color:var(--muted-2);text-transform:uppercase;letter-spacing:.04em}"
      ".demo-wrap.full{margin:14px 0}"
      ".pw-alt{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin:14px 0}"
      ".pw-altcol{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px}"
      ".pw-altcol h4{margin:0 0 6px;font-size:.95rem}"
      ".pw-fine{font-size:.8rem;color:var(--muted-2);margin:0 0 10px}"
      ".pw-altcol textarea{width:100%;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.74rem;padding:10px;border:1px solid var(--line);border-radius:9px;background:#0f1b2d;color:#cde3ff;resize:vertical;line-height:1.5}"
      ".prose .goldadvisor-pricewidget a{text-decoration:none}")

    body=_shell(prefix,"Gold Price Widget","Free embeddable tool","Free Gold &amp; Silver Price Widget",
        "Drop a live, beautiful gold and silver price chart onto your website in one line — free, no API key, fully responsive and customizable.",
        body_html, footer(prefix), byline=False, extra_style=style)
    return page(title,desc,canonical,prefix,sch,body)

def build_resources():
    prefix="../"
    canonical="https://gold-advisor.com/resources/"
    title="Gold IRA Rules, Regulators & Resources (2026) | Gold Advisor"
    desc="Authoritative gold IRA resources: IRS contribution and RMD rules, allowed metals (IRC 408(m)), CFTC and FINRA fraud advisories, where to file complaints, and how to verify a company."
    L=lambda u,t,d: f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a> \u2014 {d}</li>'
    content=(
     '<div class="answer"><b>Use official sources.</b> These are the government agencies, regulators, and standards bodies that actually set and enforce the rules for gold IRAs \u2014 plus where to verify a company and report a problem.</div>'
     '<h2 id="rules">IRS rules, limits &amp; distributions</h2><ul>'
     +L(RES_IRS_LIMITS,"IRS: IRA contribution limits","the current annual limits (for 2026, $7,500, or $8,600 if you are 50+).")
     +L(RES_IRS_590A,"IRS Publication 590-A","contributions to traditional and Roth IRAs, in detail.")
     +L(RES_IRS_590B,"IRS Publication 590-B","distributions, RMDs, and early-withdrawal penalties.")
     +L(RES_IRS_RMD,"IRS: Required Minimum Distribution FAQs","when and how RMDs apply (starting age 73).")
     +L(RES_IRS_FAQ,"IRS: IRA FAQs","general answers on contributions, rollovers, and distributions.")
     +L(RES_IRS_2026,"IRS: 2026 limit announcement","the official 2026 cost-of-living adjustments.")
     +'</ul>'
     '<h2 id="metals">Allowed metals &amp; coins</h2><ul>'
     +L(RES_IRC408,"26 U.S. Code \u00a7408(m)","the statute defining which metals and coins an IRA may hold (fineness rules and the collectibles exception).")
     +L(RES_USMINT,"U.S. Mint","official specifications for American Eagle and other U.S. bullion coins.")
     +'</ul>'
     '<h2 id="fraud">Fraud advisories &amp; where to complain</h2><ul>'
     +L(RES_CFTC_METALS,"CFTC: Precious Metal Frauds","the federal regulator\u2019s hub on metals scams and how they work.")
     +L(RES_CFTC_10,"CFTC &amp; FINRA: 10 Things to Ask Before Buying Metals","a joint investor bulletin written specifically for gold and silver IRAs.")
     +L(RES_CFTC_RETIRE,"CFTC: schemes designed to drain retirement savings","advisory on gold and silver retirement scams.")
     +L(RES_CFTC_COMPLAINT,"CFTC: file a complaint","report suspected commodity or metals fraud.")
     +L(RES_FTC_REPORT,"FTC: ReportFraud.ftc.gov","report scams to the Federal Trade Commission.")
     +L(RES_FTC_CONSUMER,"FTC: consumer advice","general guidance on spotting and avoiding fraud.")
     +L(RES_SEC_TCR,"SEC: tips, complaints &amp; referrals","report securities-related problems.")
     +L(RES_INVESTOR,"SEC Investor.gov","unbiased, plain-English investor education.")
     +L(RES_FINRA,"FINRA: for investors","alerts and tools from the brokerage-industry regulator.")
     +L(RES_NASAA,"NASAA","find and contact your state securities regulator.")
     +'</ul>'
     '<h2 id="verify">Verify a company\u2019s reputation</h2><ul>'
     +L(RES_BBB,"Better Business Bureau (BBB)","accreditation, letter rating, and complaint history.")
     +L(RES_BCA,"Business Consumer Alliance (BCA)","independent business-conduct ratings.")
     +L(RES_TRUSTPILOT,"Trustpilot","high-volume verified customer reviews.")
     +L(RES_TRUSTLINK,"TrustLink","a precious-metals-focused review platform.")
     +'</ul>'
     '<h2 id="state">State sales tax on bullion</h2><ul>'
     +L(RES_STATE_TAX,"USA.gov: state taxes","find your state\u2019s Department of Revenue for current bullion sales-tax rules.")
     +f'<li><a href="{prefix}bullion-sales-tax-tracker/index.html">Gold Advisor Bullion Sales-Tax Tracker</a> \u2014 our 2026 state-by-state summary, with links to verify.</li>'
     +'</ul>'
     '<h2 id="ga">Keep exploring on Gold Advisor</h2>'
     +f'<div class="related"><a href="{prefix}gold-ira-companies/index.html">Top 5 reviews</a><a href="{prefix}compare/index.html">Head-to-head comparisons</a><a href="{prefix}guides/index.html">Guides</a><a href="{prefix}tools/index.html">Calculators &amp; tools</a><a href="{prefix}gold-ira-scams/index.html">Avoid scams</a><a href="{prefix}methodology/index.html">Our methodology</a><a href="{prefix}invest-in-gold/index.html">Browse by state</a><a href="{prefix}buy-gold-in/index.html">Browse by city</a></div>'
     '<p style="font-size:.84rem;color:var(--muted-2)">External links open in a new tab and are provided for reference only; Gold Advisor is independent and not affiliated with these agencies. Educational information, not financial, tax, or legal advice.</p>')
    sch=schema([("Home","https://gold-advisor.com/"),("Resources",canonical)],
               [("Where can I check the official gold IRA rules?","The IRS sets contribution limits, RMDs, and (under IRC 408(m)) which metals qualify; the CFTC and FINRA publish precious-metals fraud advisories; and you can verify companies on the BBB, BCA, Trustpilot, and TrustLink."),
                ("Where do I report a gold IRA scam?","You can file with the CFTC at cftc.gov/complaint, the FTC at reportfraud.ftc.gov, the SEC at sec.gov/tcr, your state attorney general, your state securities regulator via NASAA, and the BBB.")])
    body=_shell(prefix,"Resources","Rules \u00b7 Regulators \u00b7 Help","Gold IRA Rules, Regulators &amp; Resources",
        "The official government and regulator sources for gold IRA rules, allowed metals, fraud protection, and where to get help \u2014 all in one place.",
        content, footer(prefix), author=True)
    return page(title,desc,canonical,prefix,sch,body)


def cleanify(root="site"):
    """Make clean URLs: drop trailing index.html from links/JS so /path/ is served, not /path/index.html."""
    import glob, re
    for fp in glob.glob(root + "/**/*.html", recursive=True):
        s = open(fp, encoding="utf-8").read()
        s = re.sub(r'index\.html(?=["#\'])', '', s)
        s = re.sub(r'(href|src)=""', r'\1="./"', s)
        open(fp, "w", encoding="utf-8").write(s)

def build_404():
    ga = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-K8NFJWVKTL"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-K8NFJWVKTL");</script>'
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
      '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
      '<title>Page not found (404) | Gold Advisor</title><meta name="robots" content="noindex">'
      '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">' + ga +
      '<style>body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;'
      'background:#0f2742;color:#f4f7fb;display:flex;min-height:100vh;align-items:center;justify-content:center;text-align:center;padding:24px}'
      '.b{max-width:560px}.lg{font-weight:800;letter-spacing:.04em;color:#e8b84b;font-size:1.05rem;margin-bottom:22px}'
      '.c{font-size:5rem;font-weight:800;color:#e8b84b;line-height:1;margin:0}h1{font-size:1.5rem;margin:8px 0 6px}'
      'p{color:#b9c6d6;line-height:1.6;margin:0 0 22px}.lk{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}'
      '.lk a{color:#0f2742;background:#e8b84b;text-decoration:none;font-weight:700;padding:10px 16px;border-radius:9px;font-size:.9rem}'
      '.lk a.alt{background:transparent;color:#e8b84b;border:1px solid #38506e}'
      'a.home{display:inline-block;margin-top:22px;color:#9fb6d0;font-size:.85rem}</style></head><body><div class="b">'
      '<div class="lg">\u25c6 GOLD ADVISOR</div><p class="c">404</p><h1>We couldn\u2019t find that page</h1>'
      '<p>The page may have moved or never existed. Try one of these instead:</p>'
      '<div class="lk"><a href="/">Home</a><a href="/gold-ira-companies/" class="alt">Best Gold IRA companies</a>'
      '<a href="/guides/" class="alt">Guides</a><a href="/tools/" class="alt">Tools</a>'
      '<a href="/gold-price-widget/" class="alt">Gold price widget</a></div>'
      '<a class="home" href="/">\u2190 Back to Gold-Advisor.com</a></div></body></html>')

def build_embed_page():
    js = r"""(function(){
  var q=new URLSearchParams(location.search);
  var d=document.createElement('div');d.className='goldadvisor-pricewidget';
  d.setAttribute('data-type',q.get('type')||'card');d.setAttribute('data-metal',q.get('metal')||'gold');
  d.setAttribute('data-theme',q.get('theme')||'light');d.setAttribute('data-accent',q.get('accent')||'#c69320');
  d.setAttribute('data-range',q.get('range')||'30');
  var a=document.createElement('a');a.href='https://gold-advisor.com/gold-price-widget/?utm_source=iframe';
  a.textContent='Live gold & silver prices by Gold Advisor';d.appendChild(a);document.body.appendChild(d);
  var s=document.createElement('script');s.src='/gold-price-widget/widget.js';s.async=true;document.body.appendChild(s);
})();"""
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
      '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
      '<title>Gold &amp; Silver Price Widget</title><meta name="robots" content="noindex">'
      '<style>html,body{margin:0;padding:6px;background:transparent}</style></head><body>'
      '<script>' + js + '</script></body></html>')

def main():
    n_s=n_c=0
    for slug,st in STATES.items():
        write(f"site/invest-in-gold/{slug}/index.html", build_state(slug,st)); n_s+=1
    for name,abbr in CITIES:
        write(f"site/buy-gold-in/{city_slug(name,abbr)}/index.html", build_city(name,abbr)); n_c+=1
    write("site/invest-in-gold/index.html", build_state_hub())
    write("site/buy-gold-in/index.html", build_city_hub())
    n_r=0
    for key in REVIEWS:
        write(f"site/gold-ira-companies/{REVIEWS[key]['slug']}-review/index.html", build_review(key)); n_r+=1
    write("site/gold-ira-companies/index.html", build_reviews_hub())
    n_g=0
    for s in GUIDE_ORDER:
        write(f"site/guides/{s}/index.html", build_guide(s)); n_g+=1
    write("site/guides/index.html", build_guides_hub())
    # ---- expansion: author/about/methodology, versus, tools, data hubs ----
    write("site/about/index.html", build_about())
    write("site/about/aaron-tal/index.html", build_author())
    write("site/methodology/index.html", build_methodology())
    n_v=0
    for a,b in VS_PAIRS:
        sl,html=build_versus(a,b); write(f"site/compare/{sl}/index.html", html); n_v+=1
    write("site/compare/index.html", build_compare_hub())
    write("site/tools/gold-ira-quiz/index.html", build_quiz())
    write("site/tools/gold-ira-fee-calculator/index.html", build_calculator())
    write("site/tools/gold-ira-rollover-calculator/index.html", build_rollover_calc())
    write("site/tools/gold-ira-rmd-calculator/index.html", build_rmd_calc())
    write("site/tools/index.html", build_tools_hub())
    write("site/gold-ira-scams/index.html", build_scams())
    write("site/resources/index.html", build_resources())
    write("site/gold-price-widget/index.html", build_gold_widget_page())
    write("site/gold-price-widget/widget.js", WIDGET_JS)
    write("site/gold-price-widget/embed.html", build_embed_page())
    write("site/404.html", build_404())
    write("site/contact/index.html", build_contact())
    write("site/privacy-policy/index.html", build_privacy())
    write("site/terms-of-use/index.html", build_terms())
    build_redirects()
    write("site/gold-ira-fee-index/index.html", build_fee_index())
    write("site/bullion-sales-tax-tracker/index.html", build_tax_tracker())
    write("site/llms.txt", build_llms())
    write("site/sitemap.xml", build_sitemap())
    with open("site/robots.txt","w") as f:
        f.write("User-agent: *\nAllow: /\nDisallow: /visit/\nSitemap: https://gold-advisor.com/sitemap.xml\n")
    cleanify("site")
    print(f"Built {n_s} states + {n_c} cities + {n_r} reviews + {n_g} guides + {n_v} versus + 3 trust + 4 tools + 2 data + scams + hubs + sitemap + robots + llms.txt")

if __name__=="__main__":
    main()
