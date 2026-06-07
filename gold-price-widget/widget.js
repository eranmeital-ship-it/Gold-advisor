/*! Gold Advisor — Free Gold & Silver Price Widget
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
