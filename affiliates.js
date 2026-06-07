/* ============================================================================
   GOLD ADVISOR — ONE control file for ALL affiliate destinations + logos
   ----------------------------------------------------------------------------
   HOW IT WORKS
   - Every "Visit Site" button on the site points to an INTERNAL redirect URL:
       gold-advisor.com/visit/<company-slug>/
   - Those /visit/ pages (and the buttons) read the FINAL destination below and
     forward the visitor to it.
   - To change where a company link goes, edit ONLY its "url" value below.
     Do NOT change the "slug" (that is the public /visit/ URL and is fixed).

   url  : the real affiliate / tracking link (the redirect target).
   slug : the internal /visit/<slug>/ path (leave as-is).
   logo : leave "" to keep the built-in logo, or set an absolute https URL.
   ============================================================================ */
window.GA_CONFIG = {
  "augusta":  { name: "Augusta Precious Metals", slug: "augusta-precious-metals",
                url: "https://learn.augustapreciousmetals.com/company-checklist-1/?apmtrkr_cid=1696&aff_id=474&apmtrkr_cph=844-917-2904&sub_id=Gold-Advisor",
                logo: "" },
  "goldco":   { name: "Goldco", slug: "goldco",
                url: "https://www.gcjdjhs3e.com/KRBJ13/5RNNCW/?source_id=gold-advisor",
                logo: "" },
  "priority": { name: "Priority Gold", slug: "priority-gold",
                url: "https://ef.prioritygoldpartners-9.com/3XLJTL/73RMHN/?source_id=gold-advisor",
                logo: "" },
  "ahg":      { name: "American Hartford Gold", slug: "american-hartford-gold",
                url: "https://tracking.hgoldgroup.com/aff_c?offer_id=234&aff_id=1091&source=gold-advisor",
                logo: "" },
  "birch":    { name: "Birch Gold Group", slug: "birch-gold-group",
                url: "https://bitira.go2cloud.org/aff_c?offer_id=5&aff_id=656&source=gold-advisor",
                logo: "" }
};

/* --- do not edit below this line --- */
/* Flat lookup so the /visit/ redirect pages can resolve a destination by key OR slug. */
window.GA_URL = (function () {
  var m = {}, c = window.GA_CONFIG || {};
  for (var k in c) { if (c[k] && c[k].url) { m[k] = c[k].url; if (c[k].slug) m[c[k].slug] = c[k].url; } }
  return m;
})();

(function () {
  function visitPath(c, k) { return "/visit/" + ((c[k] && c[k].slug) || k) + "/"; }
  function apply() {
    var c = window.GA_CONFIG || {};
    document.querySelectorAll('a[data-aff]').forEach(function (a) {
      var k = a.getAttribute('data-aff');
      if (!c[k]) return;
      a.setAttribute('href', visitPath(c, k));          /* internal redirect URL */
      var rel = a.getAttribute('rel') || '';
      if (rel.indexOf('sponsored') < 0) a.setAttribute('rel', (rel + ' nofollow sponsored').trim());
    });
    document.querySelectorAll('img[data-logo]').forEach(function (img) {
      var k = img.getAttribute('data-logo');
      if (c[k] && c[k].logo) img.setAttribute('src', c[k].logo);
    });
  }
  if (document.readyState !== 'loading') apply();
  else document.addEventListener('DOMContentLoaded', apply);
})();
