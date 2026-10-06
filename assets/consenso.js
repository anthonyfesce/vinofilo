/* Vinofilo: banner cookie e Google Analytics 4.
   Analytics si carica SOLO dopo "Accetta". La scelta resta salvata nel browser per 6 mesi.
   L'ID GA4 arriva dall'attributo data-ga dello script. */
(function () {
  var s = document.currentScript, GA = s && s.getAttribute('data-ga');
  if (!GA) return;
  var KEY = 'vf_consenso', SEI_MESI = 182 * 864e5;
  // Testi nella lingua della pagina (attributi data-* dello script); in mancanza, italiano.
  function a(n, d) { return (s && s.getAttribute(n)) || d; }
  function h(x) { return String(x).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var TXT = a('data-t', 'Usiamo cookie di statistica (Google Analytics) per capire quali articoli vengono letti. Si attivano solo se accetti.'),
      OK = a('data-ok', 'Accetta'), NO = a('data-no', 'Rifiuta'), PL = a('data-p', 'Privacy e cookie'), PU = a('data-pu', '/privacy/');

  function leggi() {
    try { var v = JSON.parse(localStorage.getItem(KEY)); if (v && Date.now() - v.t < SEI_MESI) return v.s; } catch (e) {}
    return null;
  }
  function salva(scelta) {
    try { localStorage.setItem(KEY, JSON.stringify({ s: scelta, t: Date.now() })); } catch (e) {}
  }
  function avviaGA() {
    if (window.__vfGA) return; window.__vfGA = 1;
    var g = document.createElement('script'); g.async = 1;
    g.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA;
    document.head.appendChild(g);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag('js', new Date()); gtag('config', GA);
  }
  function cancellaCookieGA() {
    document.cookie.split(';').forEach(function (c) {
      var n = c.split('=')[0].trim();
      if (n.indexOf('_ga') === 0) {
        ['', '; domain=' + location.hostname, '; domain=.' + location.hostname].forEach(function (d) {
          document.cookie = n + '=; Max-Age=0; path=/' + d;
        });
      }
    });
  }
  function banner() {
    if (document.getElementById('vf-cookie')) return;
    var b = document.createElement('div'); b.id = 'vf-cookie'; b.setAttribute('role', 'dialog');
    b.setAttribute('aria-label', PL);
    b.innerHTML = '<p>' + h(TXT) + ' <a href="' + h(PU) + '">' + h(PL) + '</a></p>' +
      '<div><button type="button" data-v="no">' + h(NO) + '</button><button type="button" data-v="si" class="si">' + h(OK) + '</button></div>';
    b.addEventListener('click', function (e) {
      var v = e.target.getAttribute && e.target.getAttribute('data-v'); if (!v) return;
      salva(v); b.remove();
      if (v === 'si') avviaGA(); else cancellaCookieGA();
    });
    document.body.appendChild(b);
  }
  window.vfPreferenzeCookie = function () { banner(); };

  var scelta = leggi();
  if (scelta === 'si') avviaGA();
  else if (scelta !== 'no') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', banner); else banner();
  }
})();
