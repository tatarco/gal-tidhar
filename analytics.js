/* Consent-gated GA4 + Clarity, self-contained.
   Injects its own consent bar, so any page gets tracking with one script tag.
   Blog posts had no tag at all: 76 GSC clicks reported as 2 GA4 sessions. */
(function(){
  var GA_ID='G-MEKXX27Y8Q';      /* GA4 measurement ID — consent-gated */
  var CLARITY_ID='ycoqemazfm';   /* Microsoft Clarity — heatmaps + recordings, consent-gated */

  window.dataLayer=window.dataLayer||[];
  function gtag(){dataLayer.push(arguments);}
  window.gtag=window.gtag||gtag;
  gtag('consent','default',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});
  window.__consent=false; window.__loaded=false;

  function loadClarity(){
    if(!CLARITY_ID||window.__cl)return; window.__cl=true;
    (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};t=l.createElement(r);t.async=1;t.src='https://www.clarity.ms/tag/'+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y)})(window,document,'clarity','script',CLARITY_ID);
  }
  function loadAnalytics(){
    if(window.__loaded)return; window.__loaded=true;
    if(GA_ID){var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+GA_ID;document.head.appendChild(s);
      s.onload=function(){gtag('js',new Date());gtag('config',GA_ID);};}
    loadClarity();
  }
  function grantConsent(){window.__consent=true;gtag('consent','update',{analytics_storage:'granted'});loadAnalytics();}

  var CSS="#consent-bar{position:fixed;inset-inline:0;bottom:0;z-index:9999;display:none;"+
    "gap:.9rem;align-items:center;justify-content:center;flex-wrap:wrap;"+
    "padding:.75rem 1rem;background:rgba(10,22,40,.96);border-top:1px solid var(--border,#1e3a5f);"+
    "color:var(--text,#e2e8f0);font-family:'IBM Plex Mono','Courier New',monospace;font-size:.8rem;"+
    "backdrop-filter:blur(6px);}"+
    "#consent-bar p{margin:0;max-width:52ch;color:var(--muted,#94a3b8);}"+
    "#consent-bar button{font-family:inherit;font-size:.78rem;font-weight:600;cursor:pointer;"+
    "padding:.4rem .9rem;border-radius:3px;border:1px solid var(--border,#1e3a5f);background:transparent;"+
    "color:var(--text,#e2e8f0);transition:all .15s;white-space:nowrap;}"+
    "#consent-bar button.accept{background:var(--accent,#7dd3fc);color:#0a1628;border-color:var(--accent,#7dd3fc);}"+
    "#consent-bar button:hover{opacity:.85;}";

  var HTML='<p>With your consent, this site uses Google Analytics and Microsoft Clarity '+
    '(incl. anonymised session recordings, text masked) to understand and improve usage. '+
    'No ads, no selling data. <a href="/privacy.html" style="color:var(--cyan,#7dd3fc)">Privacy</a>.</p>'+
    '<button id="consent-accept" class="accept" type="button">Accept</button>'+
    '<button id="consent-reject" type="button">Decline</button>';

  function injectBar(){
    if(document.getElementById('consent-bar'))return;   /* index.html has its own */
    var st=document.createElement('style'); st.textContent=CSS; document.head.appendChild(st);
    var bar=document.createElement('div');
    bar.id='consent-bar'; bar.setAttribute('role','dialog');
    bar.setAttribute('aria-label','Analytics consent'); bar.innerHTML=HTML;
    document.body.appendChild(bar);
  }
  function showBar(){injectBar();var bar=document.getElementById('consent-bar');if(bar)bar.style.display='flex';}

  if(!GA_ID&&!CLARITY_ID)return;                        /* nothing to load → no banner */
  var decided=null;
  try{decided=localStorage.getItem('analyticsConsent');}catch(e){}
  if(decided==='granted'){grantConsent();}
  else if(decided!=='denied'){
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',showBar);
    else showBar();
  }

  document.addEventListener('click',function(e){
    var t=e.target;
    if(!t||!t.closest)return;
    var a=t.closest('#consent-accept'), r=t.closest('#consent-reject');
    if(a){try{localStorage.setItem('analyticsConsent','granted')}catch(e){};grantConsent();document.getElementById('consent-bar').style.display='none';}
    if(r){try{localStorage.setItem('analyticsConsent','denied')}catch(e){};document.getElementById('consent-bar').style.display='none';}
  });
})();
