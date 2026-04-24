import streamlit as st

def apply_custom_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Assistant:wght@200;300;400;500;600;700;800&display=swap');
/* טעינת פונטי האייקונים של Google כדי להבטיח שאייקוני Streamlit
   יוצגו כגרפיקה ולא כטקסט גולמי (keyboard_arrow_down / link וכו') */
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

html, body, [class*="css"], .stApp, p, div, span, button, h1, h2, h3 {
    font-family: 'Assistant', sans-serif !important;
}

/* שחזור פונט האייקונים של Streamlit (Material Symbols / Icons)
   כדי למנוע הצגת טקסט גולמי כמו "keyboard_arrow_down" / "keyboard_double_arrow_left" / "link" */
span.material-icons,
span.material-icons-outlined,
span.material-icons-rounded,
span.material-icons-sharp,
span.material-icons-two-tone,
span.material-symbols-outlined,
span.material-symbols-rounded,
span.material-symbols-sharp,
[data-testid="stIconMaterial"],
[data-testid="stExpanderToggleIcon"],
.stMarkdown a.anchor-link span,
.stMarkdown a[href^="#"] span {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined',
                 'Material Icons', 'Material Icons Outlined',
                 'Material Icons Rounded' !important;
    font-weight: normal !important;
    font-style: normal !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    direction: ltr !important;
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
    font-feature-settings: 'liga';
}
.stApp { background-color: #f5f6fa; direction: rtl; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; max-width: 100% !important; }
#MainMenu, footer { visibility: hidden; }

/* משאירים את ה-<header> של Streamlit גלוי (שקוף) כדי שכפתור פתיחת ה-Sidebar
   יהיה תמיד נגיש. מסתירים רק את הרכיבים המיותרים בתוכו. */
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stHeader"] [data-testid="stToolbar"],
[data-testid="stHeader"] [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { visibility: hidden !important; }
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] {
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 9999 !important;
}

/* ======= SIDEBAR ======= */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-left: 1px solid #eef0f4;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

/* כאשר הסרגל סגור/מכווץ - להסיר כל קו או צל שנשאר גלוי
   (שורת הגבול, צל, מפרידי Streamlit הפנימיים) */
[data-testid="stSidebar"][aria-expanded="false"],
[data-testid="stSidebar"][aria-hidden="true"],
[data-testid="stSidebar"][data-collapsed="true"],
[data-testid="stSidebar"].st-emotion-cache-collapsed {
    border: none !important;
    border-left: none !important;
    border-right: none !important;
    box-shadow: none !important;
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
}
[data-testid="stSidebar"][aria-expanded="false"] *,
[data-testid="stSidebar"][aria-hidden="true"] * {
    border: none !important;
    box-shadow: none !important;
}
/* הסתרת ה-resizer / המפריד האנכי של Streamlit כשהסרגל סגור */
[data-testid="stSidebar"][aria-expanded="false"] ~ [data-testid="stSidebarResizer"],
[data-testid="stSidebarResizer"][aria-hidden="true"],
[data-testid="stDecoration"] {
    display: none !important;
    border: none !important;
    background: transparent !important;
}

/* היפוך סדר: הלוגו למעלה, תפריט הניווט (Dashboard / Audit Detail / Comparison) מתחתיו.
   משתמשים ב-CSS order על ילדי ה-flex column של הסרגל, ולכן אין שינוי בלוגיקה. */
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebarContent"],
section[data-testid="stSidebar"] > div {
    display: flex !important;
    flex-direction: column !important;
}
[data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] .block-container {
    order: 1 !important;   /* לוגו + תוכן משתמש - ראשון */
}
/* הסתרת הניווט האוטומטי של Streamlit (מציג את שמות הקבצים באנגלית).
   אנחנו מחליפים אותו בניווט מותאם אישית בעברית דרך .idi-nav + st.page_link. */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
nav[aria-label="Main navigation"] {
    display: none !important;
}

/* =========================================================
   Custom Sidebar Nav - ניווט בעברית, ממורכז, עם אנימציות פרמיום
   - ללא אייקונים, טקסט ממורכז לרוחב מלא של הסרגל
   - Hover: fade רקע עדין + קו תחתון מתרחב (slim bottom border)
   - Load-in: staggered fade-in-up עם cubic-bezier פרמיום
   ========================================================= */

/* easing משותף לכל המעברים (cubic-bezier "premium" רך) */

.idi-nav {
    padding: 8px 0 0 0;
    margin-top: 6px;
    border-top: 1px solid #f0f1f5;
    padding-top: 18px;
}

/* פריט ניווט - RTL: טקסט צמוד לימין, אייקון לשמאלו (כמו בתמונה) */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
    position: relative !important;
    direction: rtl !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;   /* נתמך עם direction:rtl -> הצמדה לימין */
    gap: 12px !important;
    text-align: right !important;
    width: calc(100% - 16px) !important;
    margin: 6px 8px !important;
    padding: 13px 18px !important;
    border-radius: 10px !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    overflow: hidden !important;

    /* staggered fade-in - כל הפריטים מתחילים בלתי-נראים ומופיעים */
    opacity: 0;
    transform: translateY(8px);
    animation: idiNavFadeIn 0.55s cubic-bezier(0.22, 1, 0.36, 1) forwards;

    /* transitions פרמיום עם cubic-bezier רך */
    transition:
        background-color 0.35s cubic-bezier(0.22, 1, 0.36, 1),
        color 0.35s cubic-bezier(0.22, 1, 0.36, 1),
        transform 0.35s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

/* האייקון של Material - גודל דק וצבע כהה כמו בתמונה */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] [data-testid="stIconMaterial"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] .material-icons,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] [data-testid="stIconMaterial"] span {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 20px !important;
    color: #0a1a3a !important;
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24 !important;
    flex-shrink: 0 !important;
    transition: color 0.35s cubic-bezier(0.22, 1, 0.36, 1), transform 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}

/* עיכוב מדורג לפי הסדר של הפריט (staggered) */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:nth-of-type(1) { animation-delay: 0.10s; }
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:nth-of-type(2) { animation-delay: 0.22s; }
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:nth-of-type(3) { animation-delay: 0.34s; }
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:nth-of-type(4) { animation-delay: 0.46s; }
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:nth-of-type(5) { animation-delay: 0.58s; }

@keyframes idiNavFadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Hover - רקע אפור בהיר רך בלבד (ללא קו תחתון) */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
    background: #f1f3f5 !important;            /* אפור בהיר עדין */
    border-color: #e5e7eb !important;
    transform: translateY(-1px) !important;
}

/* דף פעיל - רקע אפור בהיר רך כמו pill בתמונה */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"][aria-current="page"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"].active {
    background: #eef0f4 !important;
    border-color: #e5e7eb !important;
}

/* טקסט הפריט - מיושר לימין, Assistant, משקל בינוני-כבד */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] > div > div {
    font-family: 'Assistant', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    color: #0a1a3a !important;
    margin: 0 !important;
    text-align: right !important;
    letter-spacing: 0.1px;
    transition: color 0.35s cubic-bezier(0.22, 1, 0.36, 1);
}
/* דריסה של עיצוב ה-hover הדיפולטי של Streamlit שצובע את הטקסט באדום
   ומוסיף underline. כופה צבע כהה (#0a1a3a) וללא קו תחתון בכל מצבי הלינק. */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"],
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:focus,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:active,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:visited {
    text-decoration: none !important;
    color: #0a1a3a !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover *,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:focus *,
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:active * {
    color: #0a1a3a !important;
    text-decoration: none !important;
    border-bottom: none !important;
}
/* תזוזה עדינה של האייקון ב-hover (ללא שינוי צבע) */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover [data-testid="stIconMaterial"] {
    transform: translateX(-2px);
}

.idi-logo-wrap {
    padding: 22px 18px 18px 18px;
    border-bottom: 1px solid #f0f1f5;
    margin-bottom: 14px;
}
.idi-logo-row {
    display: flex;
    flex-direction: row-reverse;
    align-items: center;
    justify-content: flex-start;
    gap: 12px;
}
.idi-logo-text { text-align: right; }
.idi-logo-top {
    font-family: 'Assistant', sans-serif;
    font-weight: 800;
    font-size: 26px;
    line-height: 1;
    color: #0a1a3a;
    letter-spacing: -0.5px;
}
.idi-logo-bottom {
    font-weight: 800;
    font-size: 26px;
    line-height: 1;
    color: #0a1a3a;
    margin-top: 2px;
}
.idi-logo-dots { display: inline-flex; align-items: center; }
.idi-logo-tag {
    color: #9aa3b2;
    font-size: 9.5px;
    margin-top: 4px;
    letter-spacing: 0.3px;
    font-weight: 500;
}

.side-section-title {
    color: #9aa3b2;
    font-size: 12px;
    font-weight: 600;
    padding: 8px 22px 6px 22px;
    letter-spacing: 0.3px;
}
.side-nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 22px;
    color: #4b5563;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    border-right: 3px solid transparent;
    transition: all .15s;
}
.side-nav-item:hover { background: #f8f9fc; color: #0a1a3a; }
.side-nav-item.active {
    background: #f5f6fa;
    color: #0a1a3a;
    border-right-color: #ED1F4A;
    font-weight: 700;
}
.side-nav-icon { font-size: 17px; width: 20px; text-align: center; }

.side-footer {
    position: absolute;
    bottom: 16px;
    right: 22px;
    color: #c2c7d0;
    font-size: 12px;
    font-weight: 600;
}
.side-footer .dot { color: #ED1F4A; font-size: 14px; margin-left: 4px; }

/* ======= TOP BAR ======= */
.top-bar {
    background: white;
    border: 1px solid #eef0f4;
    border-radius: 14px;
    padding: 10px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 22px;
    box-shadow: 0 1px 2px rgba(16,24,40,.04);
}
.top-bar-left { display: flex; align-items: center; gap: 14px; color: #6b7280; font-size: 14px; font-weight: 500; }
.top-bar-sep { color: #d1d5db; }
.top-bar-crumb-active { color: #0a1a3a; font-weight: 700; }
.top-bar-icons { display: flex; gap: 14px; align-items: center; color: #9aa3b2; font-size: 16px; }
.top-search {
    background: #f5f6fa;
    border: 1px solid #eef0f4;
    border-radius: 8px;
    padding: 6px 14px;
    color: #9aa3b2;
    font-size: 13px;
    min-width: 260px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* ======= PAGE TITLE ======= */
.page-title { font-size: 26px; font-weight: 800; color: #0a1a3a; margin: 6px 0 22px 0; text-align: right !important; direction: rtl !important;}

/* ======= DASHBOARD CARDS ======= */
.dash-card {
    background: white;
    border-radius: 18px;
    padding: 24px 28px;
    box-shadow: 0 1px 2px rgba(16,24,40,.04), 0 4px 16px rgba(16,24,40,.04);
    border: 1px solid #f0f1f5;
    margin-bottom: 22px;
    overflow: hidden;
}
.card-title { font-size: 18px; font-weight: 700; color: #0a1a3a; margin-bottom: 6px; }
.card-title .crit { color: #ED1F4A; font-weight: 800; }
.card-subtitle { font-size: 13px; color: #9aa3b2; margin-bottom: 14px; }

/* ======= GAUGE ======= */
.gauge-value {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #0a1a3a;
    margin-top: -60px;
    position: relative;
    z-index: 2;
}
.gauge-label { text-align: center; color: #6b7280; font-size: 14px; margin-top: 8px; }

/* Ensure Plotly charts are contained within the white cards */
.dash-card .js-plotly-plot,
.dash-card .plotly,
.dash-card svg {
    background: white !important;
}

.dash-card .modebar {
    display: none !important;
}

/* ======= LIVE FEED TABLE ======= */
.feed-wrap { background: white; border-radius: 18px; padding: 24px 28px; border: 1px solid #f0f1f5; box-shadow: 0 1px 2px rgba(16,24,40,.04), 0 4px 16px rgba(16,24,40,.04); }
.feed-title { font-size: 15px; color: #9aa3b2; font-weight: 600; margin-bottom: 16px; }
table.feed {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}
table.feed thead th {
    text-align: right;
    color: #9aa3b2;
    font-weight: 500;
    padding: 10px 14px;
    border-bottom: 1px solid #f0f1f5;
    font-size: 13px;
}
table.feed tbody td {
    padding: 14px;
    border-bottom: 1px solid #f5f6fa;
    color: #374151;
    vertical-align: middle;
}
.src-cell { display: flex; align-items: center; gap: 10px; font-weight: 600; color: #0a1a3a; }
.src-avatar { width: 28px; height: 28px; border-radius: 50%; background: #e5e7eb; display: inline-flex; align-items: center; justify-content: center; font-size: 13px; color: #6b7280; font-weight: 700; }
.pill-red { color: #ED1F4A; font-weight: 700; }
.pill-green { color: #16a34a; font-weight: 700; }
.insight { display: inline-flex; align-items: center; gap: 6px; font-weight: 600; font-size: 13px; }
.insight::before { content: '●'; font-size: 10px; }
.insight.prog { color: #2563eb; }
.insight.comp { color: #16a34a; }
.insight.pend { color: #7c3aed; }
.insight.appr { color: #ca8a04; }

/* feed - cited by tags */
.feed-by {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; border-radius: 999px;
    font-size: 12px; font-weight: 700;
}
.feed-by-gem  { background: #fce7f3; color: #be185d; }
.feed-by-chat { background: #dbeafe; color: #1e40af; }
.feed-by-both { background: linear-gradient(90deg,#fce7f3,#dbeafe); color: #581c87; }
.feed-by-claude { background: #fef3c7; color: #b45309; }
.feed-by-all { background: linear-gradient(90deg,#fce7f3,#dbeafe,#fef3c7); color: #7c2d12; font-weight: 800; }

/* feed - frequency bar */
.feed-freq { display: flex; align-items: center; gap: 8px; min-width: 120px; }
.feed-freq-bar {
    flex: 1; height: 6px; background: #f0f1f5;
    border-radius: 999px; overflow: hidden;
}
.feed-freq-fill {
    height: 100%;
    background: linear-gradient(90deg, #ED1F4A, #ff6b8a);
    border-radius: 999px;
}
.feed-freq-txt {
    font-size: 12px; color: #6b7280; font-weight: 700;
    min-width: 32px; text-align: center;
}

/* feed - action cells */
.feed-action-hot { color: #991b1b; font-weight: 700; }
.feed-action-ok  { color: #166534; font-weight: 600; }
.feed-action-mid { color: #6b7280; font-weight: 500; }

/* ======= QUESTION CARDS (detailed results) ======= */
.q-card {
    background: white;
    border-radius: 18px;
    padding: 24px 28px;
    margin-bottom: 18px;
    border: 1px solid #f0f1f5;
    box-shadow: 0 1px 2px rgba(16,24,40,.04);
}
.q-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 14px;
    border-bottom: 1px solid #f0f1f5;
    margin-bottom: 18px;
}
.q-title { font-size: 17px; font-weight: 700; color: #0a1a3a; }
.q-badges { display: flex; gap: 6px; flex-wrap: wrap; }
.q-badge { font-size: 12px; padding: 4px 10px; border-radius: 12px; font-weight: 600; }
.q-badge-us-in { background: #dcfce7; color: #166534; }
.q-badge-us-out { background: #fee2e2; color: #991b1b; }
.q-badge-score { background: #eef0f4; color: #374151; }
.q-badge-comp { background: #fff0f3; color: #ED1F4A; border: 1px solid #ffd1dc; }

.ans-box {
    border: 1px solid #eef0f4;
    border-radius: 14px;
    padding: 16px 18px;
    background: #fbfbfd;
    font-size: 14px;
    line-height: 1.85;
    color: #1f2937;
    min-height: 150px;
    direction: rtl;
    text-align: right;
    unicode-bidi: plaintext;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
.ans-box * { direction: rtl; text-align: right; unicode-bidi: plaintext; }
.ans-head {
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding-bottom: 8px;
    border-bottom: 1px solid #eef0f4;
}
.ans-head-chat { color: #0a1a3a; }
.ans-head-gem  { color: #ED1F4A; }

.sources-title { font-size: 13px; color: #9aa3b2; font-weight: 600; margin: 16px 0 10px 0; }
.src-pill {
    display: inline-block;
    background: #f5f6fa;
    border: 1px solid #eef0f4;
    border-radius: 999px;
    padding: 6px 14px;
    margin: 4px 4px 4px 0;
    font-size: 12.5px;
    color: #374151;
    text-decoration: none;
    transition: all .15s;
}
.src-pill:hover { background: #0a1a3a; color: white !important; }
.src-pill-us { background: #fff0f3; border-color: #ffd1dc; color: #ED1F4A; font-weight: 700; }

.rec-box {
    background: #fff8e7;
    border-right: 3px solid #eab308;
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 14px;
    font-size: 13.5px;
    color: #713f12;
    line-height: 1.6;
}
.rec-box-ok { background: #ecfdf5; border-right-color: #16a34a; color: #166534; }

/* ======= HERO (landing) ======= */
.hero-card {
    background: white;
    border-radius: 22px;
    padding: 70px 40px 60px 40px;
    border: 1px solid #f0f1f5;
    box-shadow: 0 1px 2px rgba(16,24,40,.04), 0 8px 28px rgba(16,24,40,.06);
    text-align: center;
    margin: 40px auto;
    max-width: 720px;
}
.hero-icon { font-size: 56px; margin-bottom: 10px; }
.hero-title { font-size: 32px; font-weight: 800; color: #0a1a3a; margin-bottom: 10px; letter-spacing: -0.5px; }
.hero-sub { color: #6b7280; font-size: 16px; line-height: 1.7; max-width: 520px; margin: 0 auto 32px auto; }
.hero-stats { display: flex; justify-content: center; gap: 28px; margin-bottom: 32px; flex-wrap: wrap; }
.hero-stat { background: #fbfbfd; border: 1px solid #eef0f4; border-radius: 12px; padding: 14px 22px; min-width: 110px; }
.hero-stat-num { font-size: 22px; font-weight: 800; color: #ED1F4A; }
.hero-stat-lbl { color: #6b7280; font-size: 12px; font-weight: 600; margin-top: 2px; }

/* Center the big run button */
.hero-btn-wrap { text-align: center; }
.hero-btn-wrap .stButton > button {
    font-size: 18px !important;
    padding: 16px 48px !important;
    border-radius: 999px !important;
    box-shadow: 0 6px 20px rgba(237,31,74,.35) !important;
}

/* ======= CHAT ======= */
.chat-wrap {
    max-width: 780px;
    margin: 0 auto;
    background: white;
    border: 1px solid #f0f1f5;
    border-radius: 18px;
    padding: 28px 26px;
    box-shadow: 0 1px 2px rgba(16,24,40,.04), 0 4px 16px rgba(16,24,40,.04);
    min-height: 420px;
}
.chat-header {
    padding-bottom: 14px;
    border-bottom: 1px solid #f0f1f5;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.chat-avatar {
    width: 38px; height: 38px; border-radius: 50%;
    background: linear-gradient(135deg, #0a1a3a, #ED1F4A);
    display: flex; align-items: center; justify-content: center;
    color: white; font-weight: 700; font-size: 16px;
}
.chat-head-txt { flex: 1; }
.chat-head-name { font-weight: 700; color: #0a1a3a; font-size: 15px; }
.chat-head-status { font-size: 12px; color: #16a34a; display: flex; align-items: center; gap: 4px; }
.chat-head-status::before { content: '●'; font-size: 9px; }

.bubble-row { display: flex; margin: 10px 0; direction: rtl; }
.bubble-row-user { justify-content: flex-start; }
.bubble-row-ai { justify-content: flex-end; }
.bubble-user {
    background: #ED1F4A; color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 72%;
    font-size: 15px;
    line-height: 1.5;
    font-weight: 500;
    box-shadow: 0 2px 8px rgba(237,31,74,.2);
    animation: slide-in-r .35s ease;
}
.bubble-ai {
    background: #f5f6fa; color: #1f2937;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 72%;
    font-size: 14px;
    line-height: 1.6;
    border: 1px solid #eef0f4;
    animation: slide-in-l .35s ease;
}
.bubble-ai .src-tag {
    display: inline-block; background: white; border: 1px solid #e5e7eb;
    padding: 3px 10px; border-radius: 10px; font-size: 11.5px;
    margin: 4px 4px 0 0; color: #6b7280;
}
.typing { display: inline-flex; gap: 4px; padding: 6px 0; }
.typing span {
    width: 7px; height: 7px; background: #9aa3b2; border-radius: 50%;
    animation: bounce 1.2s infinite;
}
.typing span:nth-child(2) { animation-delay: .15s; }
.typing span:nth-child(3) { animation-delay: .3s; }
@keyframes bounce { 0%,60%,100%{transform:translateY(0);opacity:.5} 30%{transform:translateY(-5px);opacity:1} }
@keyframes slide-in-r { from { opacity:0; transform:translateX(-20px) } to { opacity:1; transform:translateX(0) } }
@keyframes slide-in-l { from { opacity:0; transform:translateX(20px) } to { opacity:1; transform:translateX(0) } }

/* ======= PREMIUM DETAILED QUESTION CARDS ======= */
.qx-wrap { margin-bottom: 32px; animation: fadeUp .5s ease; }
@keyframes fadeUp { from { opacity:0; transform:translateY(15px) } to { opacity:1; transform:translateY(0) } }

.qx-card {
    background: white;
    border-radius: 24px;
    border: 1px solid #f0f1f5;
    box-shadow: 0 1px 2px rgba(16,24,40,.04), 0 10px 30px rgba(16,24,40,.06);
    overflow: hidden;
    position: relative;
}

/* Top gradient strip */
.qx-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #ED1F4A, #0a1a3a);
}

.qx-header {
    display: flex; align-items: center; gap: 20px;
    padding: 26px 30px 20px 30px;
    border-bottom: 1px solid #f5f6fa;
    direction: rtl !important; 
    text-align: right !important;
}
.qx-index {
    flex-shrink: 0;
    width: 56px; height: 56px;
    border-radius: 16px;
    background: linear-gradient(135deg, #ED1F4A, #c91a3e);
    color: white;
    font-size: 22px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 6px 16px rgba(237,31,74,.3);
}
.qx-header-body { flex: 1; min-width: 0; text-align: right !important; }
.qx-question {
    font-size: 19px; font-weight: 800; color: #0a1a3a;
    margin-bottom: 8px; line-height: 1.4;
}
.qx-meta {
    display: flex;
    gap: 10px;            /* מרווח בין התגיות (בולטים/pills) */
    flex-wrap: wrap;
    row-gap: 8px;
    direction: rtl;
    align-items: center;
    margin-top: 2px;
}
.qx-tag {
    font-size: 12px; padding: 4px 11px; border-radius: 999px;
    font-weight: 700; display: inline-flex; align-items: center; gap: 5px;
}
.qx-tag-in    { background: #dcfce7; color: #14532d; }
.qx-tag-out   { background: #fee2e2; color: #7f1d1d; }
.qx-tag-score { background: #eef0f4; color: #374151; }
.qx-tag-comp  { background: #fff0f3; color: #be185d; border: 1px solid #fbcfe8; }

/* Score ring (circular progress) */
.qx-score-ring {
    flex-shrink: 0;
    width: 74px; height: 74px;
    position: relative;
}
.qx-score-ring svg { transform: rotate(-90deg); }
.qx-score-ring-txt {
    position: absolute; inset: 0;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    font-weight: 800; color: #0a1a3a;
}
.qx-score-val { font-size: 19px; line-height: 1; }
.qx-score-lbl { font-size: 9px; color: #9aa3b2; margin-top: 2px; letter-spacing: .5px; }

/* Section title inside card */
.qx-section {
    padding: 22px 30px 6px 30px;
    font-size: 12px; font-weight: 700; color: #9aa3b2;
    letter-spacing: 1.2px; text-transform: uppercase;
    display: flex; align-items: center; gap: 8px;
}
.qx-section::before {
    content: ''; width: 28px; height: 2px; background: #ED1F4A; border-radius: 2px;
}

/* AI MODEL CARDS */
.qx-ai-grid { padding: 12px 30px 0 30px; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }
@media (max-width: 1100px) { .qx-ai-grid { grid-template-columns: 1fr; } }
.qx-ai {
    border-radius: 16px;
    border: 1.5px solid #eef0f4;
    background: #fbfbfd;
    overflow: hidden;
    transition: all .2s;
}
.qx-ai:hover { transform: translateY(-2px); box-shadow: 0 8px 22px rgba(16,24,40,.08); }
.qx-ai-head {
    padding: 12px 18px;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid #eef0f4;
    font-weight: 700; font-size: 14px;
}
.qx-ai-head-left { display: flex; align-items: center; gap: 10px; }
.qx-ai-logo {
    width: 32px; height: 32px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px; color: white; font-weight: 800;
}
.qx-ai-chat .qx-ai-head { background: linear-gradient(90deg, #0a1a3a, #1e3a8a); color: white; }
.qx-ai-chat .qx-ai-logo { background: rgba(255,255,255,.22); }
.qx-ai-gem .qx-ai-head  { background: linear-gradient(90deg, #ED1F4A, #c91a3e); color: white; }
.qx-ai-gem  .qx-ai-logo { background: rgba(255,255,255,.22); }
.qx-ai-claude .qx-ai-head { background: linear-gradient(90deg, #d97706, #b45309); color: white; }
.qx-ai-claude .qx-ai-logo { background: rgba(255,255,255,.22); }
.qx-ai-status {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(255,255,255,.18);
    padding: 3px 10px; border-radius: 999px;
    font-size: 11.5px; font-weight: 600;
}
.qx-ai-body {
    padding: 16px 18px;
    font-size: 14px; line-height: 1.85; color: #1f2937;
    direction: rtl; text-align: right; unicode-bidi: plaintext;
    min-height: 130px;
}
.qx-ai-body * { direction: rtl; text-align: right; unicode-bidi: plaintext; }
.qx-ai-body .ai-link,
.ai-link {
    color: #ED1F4A !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    background: #fff5f7;
    padding: 1px 7px;
    border-radius: 6px;
    border: 1px solid #fde2ea;
    white-space: nowrap;
    display: inline-block;
    margin: 0 2px;
    max-width: 240px;
    overflow: hidden;
    text-overflow: ellipsis;
    vertical-align: middle;
    direction: ltr;
}
.qx-ai-body .ai-link:hover,
.ai-link:hover {
    background: #ED1F4A;
    color: white !important;
    border-color: #ED1F4A;
}

/* SOURCE CARDS GRID */
.qx-src-grid {
    padding: 10px 30px 4px 30px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 12px;
}
.qx-src {
    background: #fbfbfd;
    border: 1px solid #eef0f4;
    border-radius: 14px;
    padding: 14px 16px;
    display: flex; gap: 12px; align-items: flex-start;
    text-decoration: none !important;
    transition: all .18s;
    position: relative;
    overflow: hidden;
}
.qx-src:hover {
    transform: translateY(-2px);
    border-color: #0a1a3a;
    box-shadow: 0 8px 20px rgba(10,26,58,.12);
}
.qx-src-us { background: linear-gradient(135deg, #fff5f7, #fff); border-color: #ffb6c8; }
.qx-src-us::before {
    content: '★ ביטוח ישיר'; position: absolute;
    top: 8px; left: 8px;
    background: #ED1F4A; color: white;
    font-size: 10px; font-weight: 700;
    padding: 2px 8px; border-radius: 6px;
}
.qx-src-favicon {
    width: 40px; height: 40px; border-radius: 10px;
    background: white;
    border: 1px solid #eef0f4;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; overflow: hidden;
}
.qx-src-favicon img { width: 26px; height: 26px; }
.qx-src-body { flex: 1; min-width: 0; }
.qx-src-title {
    font-weight: 700; font-size: 13.5px; color: #0a1a3a;
    margin-bottom: 4px; line-height: 1.35;
    display: -webkit-box; -webkit-line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
}
.qx-src-meta {
    display: flex; gap: 6px; align-items: center; flex-wrap: wrap;
    font-size: 11px; color: #9aa3b2; font-weight: 600;
}
.qx-src-cat {
    background: #eef0f4; color: #4b5563;
    padding: 2px 7px; border-radius: 6px;
}
.qx-src-auth {
    background: #0a1a3a; color: white;
    padding: 2px 7px; border-radius: 6px;
}
.qx-src-by {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 2px 8px; border-radius: 6px;
    font-size: 10.5px; font-weight: 700;
}
.qx-src-by-gem  { background: #fce7f3; color: #be185d; }
.qx-src-by-chat { background: #dbeafe; color: #1e40af; }
.qx-src-by-both { background: linear-gradient(90deg,#fce7f3,#dbeafe); color: #581c87; }
.qx-src-by-claude { background: #fef3c7; color: #b45309; }
.qx-src-by-all { background: linear-gradient(90deg,#fce7f3,#dbeafe,#fef3c7); color: #7c2d12; font-weight: 800; }

/* CROSS JUDGMENT PANEL — Claude as Universal Judge */
.qx-judge-section {
    margin: 18px 30px 8px 30px;
}
.qx-judge-title {
    display: flex; align-items: center; gap: 10px;
    font-size: 15px; font-weight: 800;
    color: #581c87;
    padding: 10px 16px;
    background: linear-gradient(90deg, #faf5ff, #fdf4ff);
    border-radius: 12px 12px 0 0;
    border: 1.5px solid #e9d5ff;
    border-bottom: none;
}
.qx-judge-badge {
    display: inline-flex; align-items: center; gap: 4px;
    background: #a855f7; color: white;
    padding: 3px 10px; border-radius: 999px;
    font-size: 11px; font-weight: 700;
}
.qx-judge-grid {
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px;
    padding: 16px;
    background: white;
    border: 1.5px solid #e9d5ff;
    border-top: none;
    border-radius: 0 0 12px 12px;
}
@media (max-width: 1100px) { .qx-judge-grid { grid-template-columns: 1fr; } }
.qx-judge-card {
    border: 1px solid #eef0f4;
    border-radius: 12px;
    padding: 14px;
    background: #fbfbfd;
    display: flex; flex-direction: column; gap: 8px;
}
.qx-judge-card-head {
    display: flex; justify-content: space-between; align-items: center;
    gap: 8px;
}
.qx-judge-model {
    font-weight: 800; font-size: 13.5px; color: #0a1a3a;
}
.qx-judge-score {
    font-size: 20px; font-weight: 900;
    padding: 2px 12px; border-radius: 10px;
    color: white;
}
.qx-judge-score-hi  { background: linear-gradient(135deg, #16a34a, #22c55e); }
.qx-judge-score-mid { background: linear-gradient(135deg, #eab308, #f59e0b); }
.qx-judge-score-lo  { background: linear-gradient(135deg, #ED1F4A, #dc2626); }
.qx-judge-flags {
    display: flex; flex-wrap: wrap; gap: 5px;
}
.qx-judge-flag {
    font-size: 10.5px; font-weight: 700;
    padding: 2px 8px; border-radius: 999px;
}
.qx-judge-flag-bias { background: #fee2e2; color: #991b1b; }
.qx-judge-flag-fair { background: #dcfce7; color: #166534; }
.qx-judge-flag-src  { background: #dbeafe; color: #1e40af; }
.qx-judge-flag-ans  { background: #fef3c7; color: #92400e; }
.qx-judge-verdict {
    font-size: 13px; line-height: 1.55; color: #374151;
    direction: rtl; text-align: right;
    padding: 8px 10px;
    background: white;
    border-radius: 8px;
    border: 1px solid #f0f1f5;
}
.qx-judge-fix {
    font-size: 12.5px; line-height: 1.55; color: #581c87;
    direction: rtl; text-align: right;
    padding: 8px 10px;
    background: #faf5ff;
    border-radius: 8px;
    border-right: 3px solid #a855f7;
}
.qx-judge-fix b { color: #6b21a8; }
.qx-judge-dom {
    font-size: 11.5px; color: #6b7280; font-weight: 600;
    direction: rtl;
}
.qx-judge-dom b { color: #0a1a3a; }

/* EXECUTIVE SUMMARY CARD */
.qx-exec {
    margin: 10px 0 22px 0;
    border-radius: 20px; overflow: hidden;
    background: linear-gradient(135deg, #0a1a3a 0%, #0f2552 50%, #1e3a8a 100%);
    color: white;
    box-shadow: 0 10px 32px rgba(10, 26, 58, .28);
    direction: rtl;
    position: relative;
}
.qx-exec::before {
    content: ''; position: absolute;
    top: 0; right: 0; width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(245, 158, 11, .22), transparent 70%);
    pointer-events: none;
}
.qx-exec-head {
    padding: 18px 28px;
    display: flex; align-items: center; gap: 14px;
    border-bottom: 1px solid rgba(255,255,255,.1);
    position: relative;
    z-index: 2;
}
.qx-exec-head-ic {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #f59e0b, #fbbf24);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 14px rgba(245, 158, 11, .4);
}
.qx-exec-head-t { font-size: 11px; opacity: .7; letter-spacing: 2px; text-transform: uppercase; }
.qx-exec-head-h { font-size: 18px; font-weight: 900; margin-top: 2px; }
.qx-exec-head-badge {
    margin-right: auto;
    background: rgba(245, 158, 11, .22);
    border: 1px solid rgba(245, 158, 11, .45);
    color: #fde68a;
    padding: 6px 14px; border-radius: 999px;
    font-size: 12px; font-weight: 800;
}

.qx-exec-body {
    padding: 24px 28px;
    display: grid;
    grid-template-columns: 1.3fr 1fr 1fr;
    gap: 18px;
    position: relative;
    z-index: 2;
}
@media (max-width: 1000px) { .qx-exec-body { grid-template-columns: 1fr; } }

.qx-exec-hero-metric {
    background: linear-gradient(135deg, rgba(245, 158, 11, .18), rgba(245, 158, 11, .05));
    border: 1.5px solid rgba(245, 158, 11, .4);
    border-radius: 16px;
    padding: 20px 22px;
}
.qx-exec-hero-lbl {
    font-size: 11.5px; letter-spacing: 1.8px; text-transform: uppercase;
    color: #fde68a; font-weight: 700; margin-bottom: 8px;
}
.qx-exec-hero-val {
    font-size: 46px; font-weight: 900; line-height: 1;
    color: #fbbf24;
    font-variant-numeric: tabular-nums;
    margin-bottom: 6px;
}
.qx-exec-hero-unit { font-size: 14px; color: #fde68a; font-weight: 600; opacity: .85; }
.qx-exec-hero-sub {
    font-size: 12.5px; opacity: .8; margin-top: 10px;
    line-height: 1.55;
}

.qx-exec-kpis {
    display: flex; flex-direction: column; gap: 10px;
}
.qx-exec-kpi {
    background: rgba(255,255,255,.06);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 12px;
    padding: 12px 16px;
}
.qx-exec-kpi-lbl {
    font-size: 10.5px; letter-spacing: 1.5px; text-transform: uppercase;
    opacity: .7; margin-bottom: 4px;
}
.qx-exec-kpi-val {
    font-size: 20px; font-weight: 800; color: white;
    font-variant-numeric: tabular-nums;
}
.qx-exec-kpi-sub { font-size: 11.5px; opacity: .7; margin-top: 2px; }

.qx-exec-action {
    background: linear-gradient(135deg, rgba(22, 163, 74, .18), rgba(22, 163, 74, .03));
    border: 1.5px solid rgba(34, 197, 94, .45);
    border-radius: 16px;
    padding: 18px 20px;
    display: flex; flex-direction: column;
}
.qx-exec-action-lbl {
    font-size: 11px; letter-spacing: 1.8px; text-transform: uppercase;
    color: #86efac; font-weight: 800; margin-bottom: 8px;
    display: flex; align-items: center; gap: 6px;
}
.qx-exec-action-headline {
    font-size: 15px; font-weight: 800; line-height: 1.45;
    margin-bottom: 8px;
    direction: rtl;
}
.qx-exec-action-meta {
    font-size: 12px; opacity: .85;
    line-height: 1.55; margin-top: auto;
    padding-top: 10px;
    border-top: 1px dashed rgba(255,255,255,.12);
    direction: rtl;
}
.qx-exec-action-meta code {
    background: rgba(34, 197, 94, .18);
    color: #bbf7d0; padding: 1px 7px; border-radius: 5px;
    font-family: 'Consolas', monospace; font-size: 11.5px;
    direction: ltr; display: inline-block;
}

/* BEFORE / AFTER COMPARISON CARD */
.qx-ba {
    margin: 14px 0 24px 0;
    border-radius: 18px; overflow: hidden;
    background: linear-gradient(135deg, #0a1a3a 0%, #1e3a8a 100%);
    color: white;
    box-shadow: 0 8px 28px rgba(10, 26, 58, .22);
    direction: rtl;
}
.qx-ba-head {
    padding: 16px 24px;
    display: flex; align-items: center; gap: 12px;
    border-bottom: 1px solid rgba(255,255,255,.14);
}
.qx-ba-title { font-weight: 900; font-size: 17px; }
.qx-ba-sub { font-size: 12.5px; opacity: .8; margin-right: auto; }
.qx-ba-body {
    padding: 22px 24px;
    display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px;
}
@media (max-width: 950px) { .qx-ba-body { grid-template-columns: 1fr; } }
.qx-ba-metric {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.15);
    border-radius: 14px; padding: 16px 18px;
}
.qx-ba-metric-label {
    font-size: 11px; opacity: .75;
    letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: 10px;
}
.qx-ba-metric-row {
    display: flex; align-items: center; justify-content: space-between;
    gap: 10px; margin: 6px 0;
}
.qx-ba-before {
    font-size: 24px; font-weight: 800; color: rgba(255,255,255,.55);
    text-decoration: line-through;
    font-variant-numeric: tabular-nums;
}
.qx-ba-arrow { font-size: 20px; opacity: .8; }
.qx-ba-after {
    font-size: 32px; font-weight: 900;
    font-variant-numeric: tabular-nums;
}
.qx-ba-delta {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 13px; font-weight: 800;
    padding: 3px 10px; border-radius: 999px;
    margin-top: 8px;
}
.qx-ba-delta-up { background: rgba(34, 197, 94, .25); color: #86efac; }
.qx-ba-delta-dn { background: rgba(239, 68, 68, .25); color: #fca5a5; }
.qx-ba-delta-flat { background: rgba(255,255,255,.18); color: #e5e7eb; }

.qx-ba-per-q {
    padding: 16px 24px 22px 24px;
    background: rgba(0,0,0,.15);
    border-top: 1px solid rgba(255,255,255,.1);
}
.qx-ba-per-q-title {
    font-size: 12px; opacity: .8;
    letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: 12px;
}
.qx-ba-q-row {
    display: grid;
    grid-template-columns: 3fr auto auto auto;
    align-items: center; gap: 12px;
    padding: 10px 0;
    border-bottom: 1px dashed rgba(255,255,255,.12);
}
.qx-ba-q-row:last-child { border-bottom: none; }
.qx-ba-q-text { font-size: 13px; font-weight: 600; }
.qx-ba-q-score {
    font-variant-numeric: tabular-nums;
    font-size: 13px; font-weight: 800;
    padding: 3px 10px; border-radius: 8px;
    background: rgba(255,255,255,.12);
    min-width: 40px; text-align: center;
}
.qx-ba-q-score.old { color: rgba(255,255,255,.55); text-decoration: line-through; }
.qx-ba-q-score.new { background: rgba(255, 255, 255, .2); color: #fde68a; }

.qx-ba-buttons {
    display: flex; gap: 10px; flex-wrap: wrap;
    margin: 18px 0 6px 0;
}

/* CONTENT BRIEF CARD — Actionable deliverable for content team */
.qx-brief {
    margin: 18px 30px 10px 30px;
    border-radius: 16px;
    overflow: hidden;
    background: linear-gradient(135deg, #ffffff 0%, #ffffff 100%);
    border: 2px solid #ED1F4A;
    box-shadow: 0 4px 14px rgba(237, 31, 74, 0.1);
}
.qx-brief-head {
    padding: 14px 20px;
    background: linear-gradient(90deg, #ED1F4A, #ff6b8a);
    color: white;
    display: flex; align-items: center; gap: 10px;
    font-weight: 800; font-size: 15px;
}
.qx-brief-head-badge {
    background: rgba(255,255,255,.22);
    padding: 3px 10px; border-radius: 999px;
    font-size: 11.5px; font-weight: 700;
    margin-right: auto;
}
.qx-brief-body { padding: 18px 22px; direction: rtl; }
.qx-brief-h1 {
    font-size: 22px; font-weight: 900; color: #ED1F4A;
    line-height: 1.35;
    margin-bottom: 6px;
    direction: rtl; text-align: right;
}
.qx-brief-meta {
    font-size: 13px; color: #ED1F4A; line-height: 1.6;
    padding: 8px 12px; background: white; border-radius: 8px;
    border-right: 3px solid #ED1F4A;
    margin-bottom: 16px;
    direction: rtl; text-align: right;
}
.qx-brief-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 14px;
    margin-bottom: 14px;
}
@media (max-width: 900px) { .qx-brief-grid { grid-template-columns: 1fr; } }
.qx-brief-box {
    background: white; border-radius: 10px;
    /* ריווח פנימי נדיב כדי להרחיק את התוכן מהמסגרת */
    padding: 16px 20px 18px;
    border: 1px solid #ED1F4A;
}

/* רשימת טיעוני המפתח - להרחיק את הנקודות והטקסט מהמסגרת ב-RTL */
.qx-brief-args {
    list-style: disc;
    direction: rtl;
    text-align: right;
    margin: 6px 0 0 0 !important;
    /* ריווח ימני (RTL) - כדי שהבולטים לא ייצמדו למסגרת */
    padding: 0 22px 4px 6px !important;
}
.qx-brief-args li {
    margin: 6px 0;
    padding-inline-start: 6px;
    line-height: 1.7;
    color: #334155;
    font-size: 14px;
}
.qx-brief-args li::marker {
    color: #ED1F4A;
}
.qx-brief-box-title {
    font-size: 11px; font-weight: 800; color: #ED1F4A;
    letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: 8px;
    display: flex; align-items: center; gap: 6px;
}
.qx-brief-box-title::before {
    content: ''; width: 16px; height: 2px; background: #ED1F4A; border-radius: 2px;
}
.qx-brief-outline {
    list-style: none; padding: 0; margin: 0;
    counter-reset: outline-counter;
}
.qx-brief-outline li {
    counter-increment: outline-counter;
    /* RTL: העיגול בצד ימין - לכן ה-padding מימין שומר מקום לעיגול
       כדי שהטקסט לא יחפוף עליו */
    padding: 10px 44px 10px 8px;
    position: relative;
    font-size: 14px; color: #1f2937; line-height: 1.6;
    border-bottom: 1px dashed #ED1F4A;
    direction: rtl; text-align: right;
}
.qx-brief-outline li:last-child { border-bottom: none; }
.qx-brief-outline li::before {
    content: counter(outline-counter);
    position: absolute;
    right: 0; top: 6px;
    width: 28px; height: 28px;
    background: #ED1F4A; color: white;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 13px;
}
.qx-brief-kw {
    display: flex; flex-wrap: wrap; gap: 6px;
}
.qx-brief-kw-chip {
    background: #ffebeb; color: #ED1F4A;
    padding: 4px 12px; border-radius: 999px;
    font-size: 12px; font-weight: 700;
    direction: rtl;
}
.qx-brief-stat-row {
    display: flex; align-items: center; gap: 10px;
    padding: 6px 0;
    border-bottom: 1px dashed #ED1F4A;
    font-size: 13px; color: #374151;
}
.qx-brief-stat-row:last-child { border-bottom: none; }
.qx-brief-stat-key { color: #ED1F4A; font-weight: 700; min-width: 80px; }
.qx-brief-stat-val { color: #1f2937; font-weight: 600; }
.qx-brief-platform {
    background: linear-gradient(135deg, #16a34a, #22c55e);
    color: white;
    padding: 12px 16px; border-radius: 10px;
    margin-top: 10px;
    direction: rtl;
}
/* תווית "📍 לפרסם ב:" - בולטת וקריאה על רקע ירוק */
.qx-brief-platform-label {
    font-size: 13px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: .2px;
    margin-bottom: 6px;
    text-shadow: 0 1px 0 rgba(0,0,0,.08);
    direction: rtl;
    text-align: right;
}
.qx-brief-platform-dom {
    font-weight: 900; font-size: 17px;
    font-family: 'Consolas', monospace;
    direction: ltr;
    background: rgba(255,255,255,.96);
    color: #0a1a3a;
    border: 1px solid rgba(255,255,255,.4);
    border-radius: 8px;
    padding: 6px 10px;
    display: inline-block;
    overflow: hidden;
}
.qx-brief-platform-reason {
    font-size: 12.5px; opacity: .95; margin-top: 8px;
    direction: rtl;
    color: #ffffff;
    line-height: 1.55;
}
.qx-think summary {
    padding: 12px 18px;
    cursor: pointer;
    font-weight: 700;
    font-size: 13.5px;
    color: #6b21a8;
    display: flex; align-items: center; gap: 8px;
    list-style: none;
    user-select: none;
}
.qx-think summary::-webkit-details-marker { display: none; }
.qx-think summary::before {
    content: '▶';
    font-size: 10px;
    transition: transform .2s;
    color: #a855f7;
}
.qx-think[open] summary::before { transform: rotate(90deg); }
.qx-think-body {
    padding: 4px 20px 16px 20px;
    font-size: 13px; line-height: 1.75;
    color: #4c1d95;
    border-top: 1px solid #f3e8ff;
    max-height: 320px;
    overflow-y: auto;
}
.qx-think-body * { direction: rtl; text-align: right; unicode-bidi: plaintext; }
.qx-think-queries {
    display: flex; flex-wrap: wrap; gap: 6px;
    margin-bottom: 10px;
}
.qx-think-query {
    background: #a855f7; color: white;
    padding: 4px 10px; border-radius: 999px;
    font-size: 11.5px; font-weight: 600;
    direction: ltr;
}

/* RECOMMENDATION PANEL */
.qx-rec {
    margin: 20px 30px 26px 30px;
    border-radius: 16px;
    overflow: hidden;
    background: linear-gradient(135deg, #fff8e7 0%, #fffdf5 100%);
    border: 1px solid #fde68a;
}
.qx-rec-ok { background: linear-gradient(135deg, #ecfdf5 0%, #f7fffb 100%); border-color: #bbf7d0; }
.qx-rec-head {
    padding: 14px 20px 8px 20px;
    display: flex; align-items: center; gap: 10px;
    font-weight: 800; font-size: 15px; color: #713f12;
}
.qx-rec-ok .qx-rec-head { color: #166534; }
.qx-rec-head-icon {
    width: 32px; height: 32px; border-radius: 10px;
    background: #eab308; color: white;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.qx-rec-ok .qx-rec-head-icon { background: #16a34a; }
.qx-rec-body { padding: 6px 20px 18px 20px; font-size: 14px; color: #713f12; line-height: 1.7; }
.qx-rec-ok .qx-rec-body { color: #166534; }

/* ======= BUTTON ======= */
.stButton > button {
    background: #ED1F4A !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 10px 28px !important;
    font-size: 15px !important;
    box-shadow: 0 2px 8px rgba(237,31,74,.25);
}
.stButton > button:hover { background: #c91a3e !important; }

a { text-decoration: none !important; }
                
/* --- עיצוב כרטיס השאלה הכללי (המעטפת הלבנה) --- */
.qx-card-container {
    background: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    margin-bottom: 50px;
    border: 1px solid #f0f2f6;
    direction: rtl;
    text-align: right;
}

/* --- עיצוב הטאבים (Tabs) --- */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    direction: rtl;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Assistant', sans-serif !important;
    font-weight: 700 !important;
}

/* --- עיצוב ה-Expander (המלבנים המתקפלים) --- */

/* 1. המלבן עצמו - מסגרת אדומה דקיקה */
.stExpander {
    border: 1px solid #ED1F4A !important;
    border-radius: 10px !important;
    background: white !important;
    margin-top: 15px !important;
    direction: rtl !important;
}

/* 2. הכותרת של המלבן - טקסט אדום נקי */
.stExpander details summary p {
    color: #ED1F4A !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    direction: rtl !important;
    text-align: right !important;
    margin: 0 !important;
    display: block !important;
}

/* 3. העלמת "זבל" טכני (keyboard_ar, אייקונים מיותרים) */
.stExpander details summary [data-testid="stWidgetLabel"],
.stExpander details summary [data-testid="stWidgetLabel"] svg,
.stExpander details summary [data-testid="stWidgetLabel"] span {
    display: none !important;
}

/* הסתרת אייקון עוגן הקישור (link) שמופיע ליד כותרות Markdown -
   מיותר בממשק ה-RTL ולעיתים נראה כטקסט גולמי */
.stMarkdown h1 a.anchor-link,
.stMarkdown h2 a.anchor-link,
.stMarkdown h3 a.anchor-link,
.stMarkdown h4 a.anchor-link,
.stMarkdown h5 a.anchor-link,
.stMarkdown h6 a.anchor-link,
h1 > a[href^="#"],
h2 > a[href^="#"],
h3 > a[href^="#"],
h4 > a[href^="#"],
h5 > a[href^="#"],
h6 > a[href^="#"] {
    display: none !important;
}

/* 4. סידור החץ (אייקון ה-Expander) בצד שמאל וצביעתו באדום */
.stExpander details summary {
    display: flex !important;
    flex-direction: row-reverse !important;
    justify-content: flex-end !important;
    gap: 12px !important;
    padding: 12px 15px !important;
}

.stExpander details summary svg[data-testid="stExpanderIcon"] {
    fill: #ED1F4A !important;
    color: #ED1F4A !important;
    width: 20px !important;
    height: 20px !important;
}

/* 5. ביטול מסגרת ברירת המחדל של Streamlit כשהמלבן פתוח */
.stExpander details {
    border: none !important;
}
                
                /* עיצוב כפתור קרא עוד בתוך תשובות ה-AI */
.read-more {
    margin-top: 8px;
    cursor: pointer;
}

.read-more summary {
    font-weight: 700;
    color: #ED1F4A; /* אדום ביטוח ישיר */
    font-size: 13px;
    list-style: none; /* מסתיר את החץ המובנה של הדפדפן */
    outline: none;
}

.read-more summary::-webkit-details-marker {
    display: none;
}

/* כאשר התוכן פתוח - מסתירים לחלוטין את הכפתור "קרא עוד"
   כדי שהטקסט המורחב יזרום באופן טבעי ללא הפרעה */
.read-more[open] > summary,
details.read-more[open] > summary {
    display: none !important;
}

.hidden-txt {
    border-top: 1px dashed #eef0f4;
    padding-top: 10px;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* =========================================================
   ========  Global RTL Audit + Breathable Spacing  ========
   ========================================================= */

/* 1) כיוון RTL לכל מיכלי Streamlit המרכזיים */
.stApp,
.main,
section.main,
.block-container,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stSidebar"],
[data-testid="stSidebarContent"],
[data-testid="stVerticalBlock"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stHorizontalBlock"],
[data-testid="column"],
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdown"],
[data-testid="stExpander"],
[data-testid="stExpanderDetails"],
[data-testid="stNotification"],
[data-testid="stAlert"],
[data-testid="stForm"],
[data-testid="stTabs"],
[data-testid="stDataFrame"],
[data-testid="stTable"],
[data-testid="stMetric"] {
    direction: rtl !important;
}

/* 2) יישור טקסט לימין בכל ברירות המחדל של Streamlit */
.stApp p,
.stApp li,
.stApp label,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
[data-testid="stMarkdown"] *,
[data-testid="stMarkdownContainer"] *,
[data-testid="stNotification"] *,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stWidgetLabel"] {
    text-align: right;
}

/* אבל אל תשבור LTR לקטעי קוד, URL, ותגיות טכניות */
.stApp code,
.stApp pre,
.stApp kbd,
.stApp samp,
[data-testid="stCodeBlock"],
[data-testid="stCodeBlock"] *,
[dir="ltr"], [dir="ltr"] * {
    direction: ltr !important;
    text-align: left !important;
    unicode-bidi: isolate;
}

/* 3) היפוך כיוון פלקס/גריד נפוצים כדי שהפריט הראשון יופיע מימין */
[data-testid="stHorizontalBlock"] {
    flex-direction: row-reverse !important;
}
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    direction: rtl !important;
    flex-direction: row-reverse !important;
    justify-content: flex-start !important;
}
[data-testid="stRadio"] > div,
[data-testid="stCheckbox"] > label,
[data-testid="stToggle"] > label {
    direction: rtl !important;
    flex-direction: row-reverse !important;
    justify-content: flex-start !important;
    gap: 10px !important;
}
[data-testid="stForm"] [data-testid="stFormSubmitButton"] {
    display: flex;
    justify-content: flex-start; /* ב-RTL flex-start = ימין */
}

/* 4) Expander — כותרת מיושרת לימין, חץ בשמאל */
[data-testid="stExpander"] details > summary {
    flex-direction: row-reverse !important;
    justify-content: space-between !important;
    text-align: right !important;
}

/* 5) שדות קלט — placeholder/טקסט ליישור ימין */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[role="combobox"],
.stMultiSelect div[role="combobox"] {
    direction: rtl !important;
    text-align: right !important;
}

/* =========================================================
   Whitespace / Breathable Design — ריווח מקצועי
   ========================================================= */

/* מיכל ראשי — נשימה מעל ומתחת */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3.5rem !important;
    padding-inline: clamp(16px, 3vw, 40px) !important;
}

/* ריווח אנכי בין בלוקים (gap ב-Vertical stack) */
[data-testid="stVerticalBlock"] {
    gap: 1.15rem !important;
}
[data-testid="stHorizontalBlock"] {
    gap: 1.25rem !important;
}

/* כותרות — יותר מרווח מעל מתחת, היררכיה ברורה */
.stApp h1 { font-size: 1.9rem !important; line-height: 1.3 !important; margin: 0 0 .85rem !important; letter-spacing: -.3px; }
.stApp h2 { font-size: 1.45rem !important; line-height: 1.35 !important; margin: 1.25rem 0 .7rem !important; }
.stApp h3 { font-size: 1.18rem !important; line-height: 1.4 !important; margin: 1rem 0 .6rem !important; }
.stApp h4 { font-size: 1.02rem !important; margin: .9rem 0 .5rem !important; }

/* פסקאות — ריווח שורות ומרווחים נדיבים */
.stApp p, [data-testid="stMarkdown"] p {
    line-height: 1.75 !important;
    margin: 0 0 .75rem !important;
}

/* כרטיסיות / Notifications — padding מוגדל */
[data-testid="stNotification"],
[data-testid="stAlert"] {
    padding: 14px 18px !important;
    border-radius: 12px !important;
    margin: 10px 0 !important;
}

/* Expander — נשימה בפנים */
[data-testid="stExpander"] {
    margin: 14px 0 !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] details > summary {
    padding: 14px 18px !important;
}
[data-testid="stExpander"] details[open] > div {
    padding: 6px 18px 18px !important;
}

/* כפתורים — hit-area מכובד, פינות רכות */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    padding: 10px 20px !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 40px !important;
}

/* טאבים — מרווח בין טאבים והזחה */
[data-testid="stTabs"] [data-baseweb="tab"] {
    padding: 10px 18px !important;
    margin-inline-start: 4px !important;
}
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 6px !important;
    padding-bottom: 8px;
}

/* שדות טופס — ריווח פנימי נעים */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    padding: 10px 14px !important;
    border-radius: 10px !important;
}
.stTextInput, .stTextArea, .stNumberInput,
.stSelectbox, .stMultiSelect, .stDateInput {
    margin-bottom: 10px !important;
}
[data-testid="stWidgetLabel"] {
    margin-bottom: 6px !important;
    font-weight: 600 !important;
}

/* מטריקות — הבלטה של המספרים */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #eef0f4;
    border-radius: 12px;
    padding: 14px 18px !important;
    box-shadow: 0 1px 2px rgba(15, 23, 42, .03);
}
[data-testid="stMetricValue"] {
    font-size: 1.7rem !important;
    font-weight: 800 !important;
    letter-spacing: -.3px;
}
[data-testid="stMetricLabel"] {
    color: #6b7280 !important;
    font-weight: 600 !important;
}

/* Sidebar — ריווח נדיב מסביב לפריטי ניווט */
[data-testid="stSidebar"] .block-container {
    padding-top: 1rem !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: .6rem !important;
}

/* =========================================================
   Thinking Process — רכיב מתקפל להצגת לוגיקת המודל
   Streamlit מציב כל widget במיכל stElementContainer נפרד, ולכן ה-div
   עם מחלקת thinking-wrap לא עוטף את ה-expander פיזית ב-DOM.
   משתמשים ב-`:has()` כדי לזהות את ה-container שמכיל את המרקר
   ואז מעצבים את ה-expander ה-adjacent.
   ========================================================= */
.thinking-wrap {
    margin: 10px 0 4px;
    direction: rtl;
    font-size: 0;      /* המרקר עצמו בלתי נראה */
    line-height: 0;
}

/* עיצוב בסיסי אפור-ניטרלי - ברירת מחדל לכל thinking expander */
[data-testid="stElementContainer"]:has(.thinking-wrap)
    + [data-testid="stElementContainer"] [data-testid="stExpander"] {
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    background: #f9fafb !important;
    box-shadow: none !important;
    margin: 0 0 12px 0 !important;
}
[data-testid="stElementContainer"]:has(.thinking-wrap)
    + [data-testid="stElementContainer"] [data-testid="stExpander"] details > summary {
    padding: 10px 14px !important;
    background: #f3f4f6 !important;
    border-radius: 10px !important;
    direction: rtl !important;
    flex-direction: row-reverse !important;
    justify-content: space-between !important;
}
[data-testid="stElementContainer"]:has(.thinking-wrap)
    + [data-testid="stElementContainer"] [data-testid="stExpander"] details > summary p {
    color: #4b5563 !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    margin: 0 !important;
    text-align: right !important;
}
[data-testid="stElementContainer"]:has(.thinking-wrap)
    + [data-testid="stElementContainer"] [data-testid="stExpander"] details[open] > summary {
    border-bottom: 1px dashed #e5e7eb !important;
    border-radius: 10px 10px 0 0 !important;
}
.thinking-body {
    direction: rtl;
    text-align: right;
    font-family: 'Assistant', sans-serif;
    font-size: 13.5px;
    line-height: 1.75;
    color: #475569;
    padding: 6px 4px;
    white-space: pre-wrap;
}

/* --- גוון ChatGPT (ירוק דהוי) --- */
[data-testid="stElementContainer"]:has(.thinking-wrap.thinking-chatgpt)
    + [data-testid="stElementContainer"] [data-testid="stExpander"] {
    background: #f0fdf4 !important;
    border-color: #bbf7d0 !important;
}
[data-testid="stElementContainer"]:has(.thinking-wrap.thinking-chatgpt)
    + [data-testid="stElementContainer"] [data-testid="stExpander"] details > summary {
    background: #dcfce7 !important;
}
[data-testid="stElementContainer"]:has(.thinking-wrap.thinking-chatgpt)
    + [data-testid="stElementContainer"] [data-testid="stExpander"] details > summary p {
    color: #166534 !important;
}

/* --- גוון Gemini (כחול דהוי) --- */
[data-testid="stElementContainer"]:has(.thinking-wrap.thinking-gemini)
    + [data-testid="stElementContainer"] [data-testid="stExpander"] {
    background: #eff6ff !important;
    border-color: #bfdbfe !important;
}
[data-testid="stElementContainer"]:has(.thinking-wrap.thinking-gemini)
    + [data-testid="stElementContainer"] [data-testid="stExpander"] details > summary {
    background: #dbeafe !important;
}
[data-testid="stElementContainer"]:has(.thinking-wrap.thinking-gemini)
    + [data-testid="stElementContainer"] [data-testid="stExpander"] details > summary p {
    color: #1e40af !important;
}

/* =========================================================
   Brand Logos — מיקום והשחלה של SVG של OpenAI / Gemini / Claude
   בתוך שורות טקסט (סטטוס, מקורות, feed)
   ========================================================= */
.feed-by svg,
.qx-src-by svg,
[class*="qx-tag"] svg {
    vertical-align: middle;
    margin: 0 2px;
}
.feed-by {
    display: inline-flex !important;
    align-items: center;
    gap: 4px;
}
.qx-src-by {
    display: inline-flex;
    align-items: center;
    gap: 3px;
}

/* =========================================================
   Page Heading — כותרת ראשית בולטת לעמוד
   ========================================================= */
.page-heading {
    direction: rtl;
    text-align: right;
    padding: 22px 26px 20px;
    margin: 4px 0 22px;
    background: linear-gradient(135deg, #ffffff 0%, #fff5f7 100%);
    border: 1px solid #f3d5dd;
    border-right: 5px solid #ED1F4A;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(237, 31, 74, .06);
}
.page-heading-eyebrow {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #ED1F4A;
    margin-bottom: 8px;
    display: inline-block;
    padding: 4px 10px;
    background: #fff0f3;
    border-radius: 999px;
}
.page-heading-title {
    font-family: 'Assistant', sans-serif !important;
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    line-height: 1.25 !important;
    color: #0a1a3a !important;
    margin: 6px 0 10px !important;
    letter-spacing: -.3px;
}
.page-heading-accent {
    color: #ED1F4A;
    font-weight: 900;
}
.page-heading-sub {
    font-size: 15px;
    color: #475569;
    font-weight: 500;
    line-height: 1.65;
    max-width: 900px;
}

/* =========================================================
   Data Viz — פינות מעוגלות אחידות לכל תרשימים ורכיבי התקדמות
   ========================================================= */

/* מיכלי תרשים Plotly/Altair/Vega - פינות רכות וצל עדין */
.stPlotlyChart,
[data-testid="stPlotlyChart"],
.stVegaLiteChart,
[data-testid="stVegaLiteChart"],
.stArrowVegaLiteChart {
    border-radius: 12px !important;
    overflow: hidden;
}

/* עיגול קצוות לכל עמודה/בר ב-SVG של תרשימים
   (fallback למקרים שאין cornerradius במקור) */
.stPlotlyChart svg .bars path,
.stPlotlyChart svg g.points path.point,
.stPlotlyChart svg g.barlayer path,
[data-testid="stPlotlyChart"] svg .bars path {
    rx: 10px;
    ry: 10px;
}

/* טבעות התקדמות ו-SVG מותאמים אישית - קצה מעוגל */
.qx-score-ring svg circle,
.qx-score-ring svg path,
svg .progress-ring path,
svg .progress-ring circle {
    stroke-linecap: round;
}

/* ספריות progress bar פנימיות */
.stProgress > div > div > div > div {
    border-radius: 999px !important;
}
.stProgress > div > div > div {
    border-radius: 999px !important;
    overflow: hidden !important;
}

/* מפרידים עדינים */
hr, [data-testid="stDivider"] {
    margin: 1.4rem 0 !important;
    border: 0 !important;
    border-top: 1px solid #eef0f4 !important;
    opacity: 1 !important;
}

/* =========================================================
   רשת בטיחות לאייקוני Streamlit — מניעת דליפת טקסט
   כמו "keyboard_double_arrow_left" בכפתור הסרגל
   ========================================================= */
[data-testid="collapsedControl"] *,
[data-testid="stSidebarCollapseButton"] *,
[data-testid="stSidebarCollapsedControl"] *,
[data-testid="baseButton-headerNoPadding"] span,
header button span,
[data-testid="stHeader"] button span,
[kind="headerNoPadding"] span {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined',
                 'Material Icons' !important;
    font-weight: normal !important;
    font-style: normal !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    direction: ltr !important;
    font-feature-settings: 'liga';
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
}

/* =========================================================
   MODERN SAAS POLISH LAYER (appended last - wins by cascade order)
   ---------------------------------------------------------
   מטרה: מראה SaaS מודרני ונקי על כל הממשק.
   - Design tokens: gridים של 4/8 לריווח, רדיוסים ומערכת צללים רכה.
   - החלפה של borders חדים ב-shadows רכים + borders כמעט-בלתי-נראים.
   - היררכיית טיפוגרפיה עקבית (Assistant, משקלים 400/600/700/800).
   - RTL: יישור ואנימציות עקביים במצב Hebrew (direction:rtl).
   ========================================================= */
:root {
    /* Grid 4/8 spacing scale */
    --s-1: 4px;   --s-2: 8px;   --s-3: 12px;  --s-4: 16px;
    --s-5: 20px;  --s-6: 24px;  --s-8: 32px;  --s-10: 40px;

    /* Radii */
    --r-sm: 8px;  --r-md: 12px; --r-lg: 16px; --r-xl: 20px; --r-pill: 999px;

    /* Soft shadow system */
    --shadow-xs: 0 1px 2px rgba(10, 26, 58, 0.04);
    --shadow-sm: 0 2px 6px rgba(10, 26, 58, 0.05), 0 1px 2px rgba(10, 26, 58, 0.04);
    --shadow-md: 0 6px 16px rgba(10, 26, 58, 0.06), 0 2px 4px rgba(10, 26, 58, 0.04);
    --shadow-lg: 0 14px 34px rgba(10, 26, 58, 0.07), 0 4px 8px rgba(10, 26, 58, 0.04);

    /* Hairline border colors */
    --border-soft: rgba(15, 23, 42, 0.06);
    --border-hair: rgba(15, 23, 42, 0.08);

    /* Typography */
    --text-primary: #0a1a3a;
    --text-secondary: #475569;
    --text-muted: #94a3b8;

    /* Easing */
    --ease-premium: cubic-bezier(0.22, 1, 0.36, 1);
}

/* ---- Global type hierarchy ---- */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Assistant', 'Segoe UI', system-ui, -apple-system, sans-serif !important;
    color: var(--text-primary);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}
h1, h2, h3, h4, .qx-brief-h1, .page-title, .page-heading-title,
.card-title, .hero-title, .dash-card-title {
    font-family: 'Assistant', sans-serif !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.2px;
}
p, li, span, label, small { font-weight: 400; }
b, strong { font-weight: 700; }

/* ---- Hero card - SaaS refined ---- */
.hero-card {
    background: #ffffff !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: var(--r-xl) !important;
    box-shadow: var(--shadow-lg) !important;
    padding: 56px 40px 48px !important;
}
.hero-stat {
    background: #ffffff !important;
    border: 1px solid var(--border-hair) !important;
    border-radius: var(--r-md) !important;
    box-shadow: var(--shadow-xs);
    transition: transform .35s var(--ease-premium), box-shadow .35s var(--ease-premium);
}
.hero-stat:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

/* ---- Dashboard / content cards ---- */
.dash-card,
.qx-card,
.qx-brief,
.qx-brief-box {
    background: #ffffff !important;
    border: 1px solid var(--border-soft) !important;
    box-shadow: var(--shadow-sm) !important;
    border-radius: var(--r-lg) !important;
}
.dash-card {
    padding: var(--s-6) var(--s-6) !important;
}
.qx-brief-box {
    padding: var(--s-4) var(--s-5) var(--s-5) !important;
}

/* ---- Pills / tags: hairline + gentle lift ---- */
.qx-tag {
    border: 1px solid var(--border-hair);
    box-shadow: var(--shadow-xs);
    padding: 5px 12px !important;
    border-radius: var(--r-pill) !important;
    transition: transform .3s var(--ease-premium), box-shadow .3s var(--ease-premium);
}
.qx-tag:hover { transform: translateY(-1px); box-shadow: var(--shadow-sm); }

/* ---- Source cards (citations) ---- */
.qx-src {
    border: 1px solid var(--border-soft) !important;
    box-shadow: var(--shadow-xs) !important;
    border-radius: var(--r-md) !important;
    transition: transform .35s var(--ease-premium), box-shadow .35s var(--ease-premium), border-color .35s var(--ease-premium);
}
.qx-src:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md) !important;
    border-color: var(--border-hair) !important;
}

/* ---- Buttons: softer, premium shadow ---- */
.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    border-radius: var(--r-pill) !important;
    box-shadow: 0 6px 18px rgba(237, 31, 74, 0.22), 0 1px 2px rgba(237, 31, 74, 0.12) !important;
    transition: transform .35s var(--ease-premium), box-shadow .35s var(--ease-premium), background-color .25s var(--ease-premium) !important;
    font-weight: 700 !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 24px rgba(237, 31, 74, 0.28), 0 2px 4px rgba(237, 31, 74, 0.14) !important;
}

/* ---- Expanders: soft shadow, no harsh border ---- */
[data-testid="stExpander"] {
    border: 1px solid var(--border-soft) !important;
    border-radius: var(--r-md) !important;
    box-shadow: var(--shadow-xs) !important;
    overflow: hidden;
}

/* ---- Tabs: subtle, no harsh underline ---- */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 1px solid var(--border-soft) !important;
}

/* ---- Feed table polish ---- */
.feed-wrap {
    border: 1px solid var(--border-soft) !important;
    box-shadow: var(--shadow-sm) !important;
    border-radius: var(--r-lg) !important;
}
table.feed th {
    color: var(--text-muted) !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}
table.feed td {
    border-top: 1px solid var(--border-soft) !important;
}

/* ---- Sidebar premium polish ---- */
[data-testid="stSidebar"] {
    box-shadow: 1px 0 0 var(--border-soft);
    border-left: none !important;
    border-right: none !important;
}

/* ---- RTL safety net: body and app containers ---- */
html[lang="he"] body,
[data-testid="stAppViewContainer"] {
    direction: rtl;
}
/* Ensure animations use the premium easing everywhere we have transitions */
.qx-tag, .qx-src, .hero-stat, .dash-card, .stButton > button {
    transition-timing-function: var(--ease-premium) !important;
}

/* ---- Remove harsh 1px-solid borders on generic Streamlit wrappers ---- */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--border-soft) !important;
}

/* =========================================================
   Streamlit column-as-card trick: כל st.column שמכיל
   <div class="dash-wrap-marker"> יעוטף כולו בסגנון dash-card
   (כותרת + chart/plotly בתוך ריבוע אחד במקום שניים נפרדים).
   משתמש ב-:has() שנתמך בדפדפנים מודרניים.
   ========================================================= */
.dash-wrap-marker { display: none !important; }

[data-testid="stColumn"]:has(> [data-testid="stVerticalBlock"] .dash-wrap-marker) >
[data-testid="stVerticalBlock"] {
    background: #ffffff !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: var(--r-lg) !important;
    box-shadow: var(--shadow-sm) !important;
    padding: var(--s-6) var(--s-6) var(--s-5) !important;
    gap: 6px !important;
}
/* ביטול רווח/padding כפול של stMarkdownContainer הראשון בתוך הכרטיס */
[data-testid="stColumn"]:has(> [data-testid="stVerticalBlock"] .dash-wrap-marker) >
[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:first-child {
    margin-top: -4px !important;
}

/* =========================================================
   HERO - GEO RADAR premium upgrade
   - Radar icon עם גלים רדיאליים
   - כרטיסי סטטיסטיקה glassmorphism
   - Model chips עם לוגואים מיניאטוריים
   - כפתור "התחל סריקה" עם outer glow
   ========================================================= */

/* כרטיס ה-hero עצמו - ברקע gradient עדין שמעצים את הזכוכית */
.hero-card {
    position: relative;
    background:
        radial-gradient(ellipse at top right, rgba(237,31,74,0.05), transparent 55%),
        radial-gradient(ellipse at bottom left, rgba(99,102,241,0.04), transparent 55%),
        #ffffff !important;
    overflow: hidden;
}
.hero-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(circle at 85% 18%, rgba(237,31,74,0.06), transparent 45%);
    pointer-events: none;
}

/* === Radar - כותרת "GEO Radar" ממוקמת במרכז הגלים === */
.hero-radar {
    position: relative;
    width: 360px;
    max-width: 90%;
    height: 180px;
    margin: 0 auto 24px;
    display: flex; align-items: center; justify-content: center;
}
.hero-radar-title {
    position: relative;
    z-index: 2;
    font-family: 'Assistant', sans-serif;
    font-size: 46px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.8px;
    line-height: 1;
    text-align: center;
    padding: 0 14px;
    animation: heroTitleBob 4s var(--ease-premium) infinite;
}
.hero-radar-title span {
    color: #ED1F4A;
    margin-inline-start: 6px;
}
@keyframes heroTitleBob {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-3px); }
}
.hero-radar-pulse {
    position: absolute;
    top: 50%; left: 50%;
    width: 140px; height: 140px;
    border-radius: 50%;
    border: 2px solid rgba(237,31,74,0.40);
    transform: translate(-50%, -50%) scale(1);
    opacity: 0;
    animation: heroRadarWave 3s var(--ease-premium) infinite;
    pointer-events: none;
}
.hero-radar-pulse-2 { animation-delay: 1s; }
.hero-radar-pulse-3 { animation-delay: 2s; }
@keyframes heroRadarWave {
    0%   { transform: translate(-50%, -50%) scale(0.6); opacity: 0.65; border-width: 2px; }
    70%  { opacity: 0.10; }
    100% { transform: translate(-50%, -50%) scale(2.1); opacity: 0;    border-width: 1px; }
}

/* === Model chips: לוגו + שם מודל בבועה זכוכיתית === */
.hero-sub .hero-model {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    margin: 0 2px;
    background: rgba(255,255,255,0.7);
    border: 1px solid var(--border-hair);
    border-radius: var(--r-pill);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    box-shadow: var(--shadow-xs);
    white-space: nowrap;
    vertical-align: middle;
    transition: transform .3s var(--ease-premium), box-shadow .3s var(--ease-premium);
}
.hero-sub .hero-model:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
}
.hero-sub .hero-model b { font-weight: 700; color: var(--text-primary); }
.hero-sub .hero-model svg { flex-shrink: 0; }

/* === Glassmorphism stat cards === */
.hero-stats {
    gap: 24px !important;
    margin-top: 12px !important;
}
.hero-stat {
    position: relative;
    min-width: 150px !important;
    padding: 22px 26px !important;
    background: rgba(255,255,255,0.55) !important;
    border: 1px solid rgba(255,255,255,0.65) !important;
    border-radius: 18px !important;
    backdrop-filter: blur(14px) saturate(160%);
    -webkit-backdrop-filter: blur(14px) saturate(160%);
    box-shadow:
        0 14px 34px rgba(10, 26, 58, 0.08),
        0 2px 6px rgba(10, 26, 58, 0.04),
        inset 0 1px 0 rgba(255,255,255,0.8) !important;
    transition: transform .45s var(--ease-premium), box-shadow .45s var(--ease-premium);
    text-align: center;
    overflow: hidden;
}
/* הילה עדינה מאחורי הכרטיס */
.hero-stat::before {
    content: '';
    position: absolute;
    inset: -40%;
    background: radial-gradient(circle, rgba(237,31,74,0.10), transparent 60%);
    opacity: 0;
    transition: opacity .6s var(--ease-premium);
    pointer-events: none;
}
.hero-stat:hover {
    transform: translateY(-4px);
    box-shadow:
        0 20px 40px rgba(10, 26, 58, 0.12),
        0 4px 10px rgba(237, 31, 74, 0.10),
        inset 0 1px 0 rgba(255,255,255,0.9) !important;
}
.hero-stat:hover::before { opacity: 1; }
.hero-stat-ico {
    color: #ED1F4A;
    margin-bottom: 8px;
    display: inline-flex;
    padding: 8px;
    background: rgba(237, 31, 74, 0.08);
    border-radius: 12px;
    line-height: 0;
}
.hero-stat-num {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #ED1F4A !important;
    letter-spacing: -0.4px;
}
.hero-stat-lbl {
    color: var(--text-secondary) !important;
    font-size: 12.5px !important;
    font-weight: 600 !important;
    margin-top: 4px !important;
    letter-spacing: 0.2px;
}

/* === כפתור "התחל סריקה" - ממורכז מושלם + outer glow עוצמתי === */
.hero-btn-wrap {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    margin: 36px auto 8px auto !important;
}
.hero-btn-wrap [data-testid="stButton"] {
    display: flex !important;
    justify-content: center !important;
    width: auto !important;
}
.hero-btn-wrap .stButton > button {
    position: relative;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 10px !important;
    direction: rtl !important;                         /* טקסט עברי בצד ימין */
    min-width: 260px !important;
    padding: 16px 40px !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    border-radius: 999px !important;
    background: linear-gradient(135deg, #ED1F4A 0%, #c91a3e 100%) !important;
    box-shadow:
        0 0 0 3px rgba(237,31,74,0.12),
        0 12px 28px rgba(237,31,74,0.36),
        0 4px 10px rgba(237,31,74,0.22) !important;
    animation: heroBtnGlow 2.4s var(--ease-premium) infinite;
}
/* אייקון Play נקי (משולש SVG) מצד ימין לטקסט העברי.
   ב-RTL ::before מופיע ראשון = בצד ימין. */
.hero-btn-wrap .stButton > button::before {
    content: '';
    display: inline-block;
    width: 14px;
    height: 14px;
    background-color: #ffffff;
    /* משולש Play נקי באמצעות clip-path (פינות מעוגלות עדינות) */
    clip-path: polygon(0 0, 100% 50%, 0 100%);
    -webkit-clip-path: polygon(0 0, 100% 50%, 0 100%);
    transition: transform 0.3s var(--ease-premium);
    flex-shrink: 0;
}
.hero-btn-wrap .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 0 0 5px rgba(237,31,74,0.14),
        0 18px 40px rgba(237,31,74,0.46),
        0 6px 14px rgba(237,31,74,0.30) !important;
}
.hero-btn-wrap .stButton > button:hover::before {
    transform: translateX(-3px) scale(1.1);
}
@keyframes heroBtnGlow {
    0%, 100% { box-shadow: 0 0 0 3px rgba(237,31,74,0.12), 0 12px 28px rgba(237,31,74,0.36), 0 4px 10px rgba(237,31,74,0.22); }
    50%      { box-shadow: 0 0 0 6px rgba(237,31,74,0.16), 0 16px 36px rgba(237,31,74,0.44), 0 6px 14px rgba(237,31,74,0.28); }
}

/* =========================================================
   HERO v4 — RTL Hebrew landing (title + chips + cards + floating CTA)
   * White bg + soft pink/red radial top-right (blur-3xl style)
   * Big "GEO Radar" navy title (RTL-aware)
   * Red chip badges for AI models
   * Hebrew description paragraph
   * 3 white cards with rounded corners, soft shadows
   * CTA floating bottom-right, red gradient pill
   * Centered flowing CTA
   ========================================================= */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Plus+Jakarta+Sans:wght@400;600;700;800;900&display=swap');

:root {
    --h3-bg: #FFFFFF;
    --h3-navy: #1B2559;
    --h3-navy-lt: #3B4FCC;
    --h3-rose: #E8294C;
    --h3-rose-lt: #FF6B8A;
    --h3-rose-dk: #C41E3A;
    --h3-slate: #475569;
    --h3-muted: #64748B;
    --h3-muted-lt: #94A3B8;
    --h3-divider: #CBD5E1;
    --h3-green: #10B981;
    --h3-blue: #3B82F6;
    --h3-amber: #F59E0B;
    --h3-spring: cubic-bezier(0.16, 1, 0.3, 1);
    --h3-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
}

body:has(.hero3-root) .stApp,
body:has(.hero3-root) [data-testid="stAppViewContainer"],
body:has(.hero3-root) .main {
    background: var(--h3-bg) !important;
    background-image: none !important;
    animation: none !important;
}
body:has(.hero3-root) .block-container {
    max-width: 100% !important;
    padding: 0 !important;
}
body:has(.hero3-root) .hero-card { display: none !important; }

.hero3-root {
    position: relative;
    width: 100%;
    min-height: calc(100vh - 200px);
    padding: 80px 32px 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 56px;
    overflow: hidden;
    font-family: 'Plus Jakarta Sans', 'Inter', 'Assistant', sans-serif;
    isolation: isolate;
    direction: ltr;
}

/* ---- Single subtle crimson orb (top-right) ---- */
.hero3-blob {
    position: absolute;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    will-change: transform;
}
.hero3-blob--crimson-tr {
    top: -140px;
    right: -160px;
    width: 640px;
    height: 540px;
    max-width: 70vw;
    max-height: 60vw;
    background: radial-gradient(ellipse,
        rgba(232,41,76,0.12) 0%,
        rgba(232,41,76,0.05) 45%,
        transparent 75%);
    filter: blur(160px);
    animation: h3Float1 14s ease-in-out infinite;
}
@keyframes h3Float1 {
    0%,100% { transform: translate(0,0) scale(1); }
    50%     { transform: translate(20px,-25px) scale(1.06); }
}

/* ---- TITLE ---- */
.hero3-title {
    position: relative;
    z-index: 2;
    margin: 40px 0 24px;
    display: inline-flex;
    gap: 0.08em;
    align-items: baseline;
    justify-content: center;
    flex-wrap: wrap;
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    font-size: clamp(100px, 15vw, 200px);
    font-weight: 900;
    line-height: 1;
    letter-spacing: 0.02em;
    text-align: center;
    direction: ltr;
}
.hero3-title-word {
    display: inline-block;
    opacity: 0;
    will-change: transform, opacity;
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
}
.hero3-title-word--geo {
    transform: translateX(-60px);
    background-image: linear-gradient(90deg, #1B2559 0%, #3B4FCC 50%, #1B2559 100%);
    animation:
        h3FlyInLeft 0.6s var(--h3-spring) 0.20s forwards,
        h3Shimmer 4s linear 1s infinite;
}
.hero3-title-word--radar {
    transform: translateX(60px);
    background-image: linear-gradient(135deg, #E8294C 0%, #FF6B8A 50%, #C41E3A 100%);
    animation:
        h3FlyInRight 0.6s var(--h3-spring) 0.30s forwards,
        h3Shimmer 3s linear 1s infinite;
}
@keyframes h3FlyInLeft  { from{opacity:0;transform:translateX(-60px);} to{opacity:1;transform:translateX(0);} }
@keyframes h3FlyInRight { from{opacity:0;transform:translateX(60px);}  to{opacity:1;transform:translateX(0);} }
@keyframes h3FlyUp      { from{opacity:0;transform:translateY(30px);}  to{opacity:1;transform:translateY(0);} }
@keyframes h3Shimmer    { 0%{background-position:0% center;} 100%{background-position:200% center;} }

/* ---- Tagline ---- */
.hero3-tagline {
    position: relative;
    z-index: 2;
    margin: -32px 0 0 0;
    font-size: 16px;
    font-weight: 400;
    color: var(--h3-muted-lt);
    letter-spacing: 0.02em;
    text-align: center;
    direction: ltr;
    opacity: 0;
    animation: h3FlyUp 0.55s var(--h3-spring) 0.50s forwards;
}

/* ---- AI LOGOS ---- */
.hero3-logos {
    position: relative;
    z-index: 2;
    display: inline-flex;
    align-items: flex-end;
    justify-content: center;
    gap: 60px;
    direction: ltr;
}
.hero3-logo {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    cursor: default;
    opacity: 0;
    transform: translateY(24px);
    animation: h3FlyUp 0.6s var(--h3-spring) forwards;
    transition: transform 0.25s var(--h3-bounce);
    will-change: transform;
}
.hero3-logo:nth-of-type(1) { animation-delay: 0.45s; }
.hero3-logo:nth-of-type(2) { animation-delay: 0.55s; }
.hero3-logo:nth-of-type(3) { animation-delay: 0.65s; }
.hero3-logo-icon { position: relative; z-index: 2; transition: transform 0.25s var(--h3-bounce); }
.hero3-logo-icon svg { display: block; }
.hero3-logo-glow {
    position: absolute;
    top: 6px;
    left: 50%;
    width: 56px;
    height: 56px;
    transform: translateX(-50%);
    border-radius: 50%;
    filter: blur(22px);
    opacity: 0.55;
    z-index: 0;
    transition: opacity 0.25s ease, filter 0.25s ease, width 0.25s ease;
    pointer-events: none;
}
.hero3-logo--openai .hero3-logo-glow { background: var(--h3-green); }
.hero3-logo--gemini .hero3-logo-glow { background: var(--h3-blue); }
.hero3-logo--claude .hero3-logo-glow { background: var(--h3-amber); }
.hero3-logo-name {
    font-size: 13px;
    font-weight: 600;
    color: var(--h3-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    position: relative;
    z-index: 2;
}
.hero3-logo:hover { transform: translateY(-3px); }
.hero3-logo:hover .hero3-logo-icon { transform: scale(1.1); }
.hero3-logo:hover .hero3-logo-glow { opacity: 0.85; filter: blur(26px); width: 68px; }

/* ---- STATS ---- */
.hero3-stats {
    position: relative;
    z-index: 2;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    direction: ltr;
}
.hero3-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 0 48px;
    min-width: 180px;
    opacity: 0;
    transform: translateY(30px);
    animation: h3FlyUp 0.6s var(--h3-spring) forwards;
}
.hero3-stat:nth-of-type(1) { animation-delay: 0.70s; }
.hero3-stat:nth-of-type(3) { animation-delay: 0.82s; }
.hero3-stat:nth-of-type(5) { animation-delay: 0.94s; }
.hero3-stat-div {
    width: 1px;
    height: 96px;
    background: var(--h3-divider);
    flex-shrink: 0;
    opacity: 0;
    animation: h3FlyUp 0.6s var(--h3-spring) 0.76s forwards;
}
.hero3-stat-icon {
    color: var(--h3-slate);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 4px;
}
.hero3-stat-icon svg { width: 36px; height: 36px; }
.hero3-stat-num {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
    font-size: clamp(40px, 5vw, 52px);
    font-weight: 900;
    line-height: 1;
    color: var(--h3-navy);
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
}
.hero3-stat-lbl {
    font-size: 12px;
    font-weight: 600;
    color: var(--h3-muted-lt);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    direction: rtl;
}

/* Live column: gradient text + halo */
.hero3-stat--live .hero3-stat-icon { color: var(--h3-rose); }
.hero3-stat-num--live {
    display: inline-flex !important;
    align-items: center;
    gap: 14px;
    background: linear-gradient(135deg, #E8294C 0%, #FF4D6D 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent !important;
    filter: drop-shadow(0 0 16px rgba(232,41,76,0.4));
    animation: h3LiveHalo 2.4s ease-in-out infinite;
}
@keyframes h3LiveHalo {
    0%,100% { filter: drop-shadow(0 0 16px rgba(232,41,76,0.4)); }
    50%     { filter: drop-shadow(0 0 28px rgba(232,41,76,0.65)); }
}
.hero3-live-dot {
    position: relative;
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--h3-rose);
    box-shadow: 0 0 12px rgba(232,41,76,0.8);
}
.hero3-live-dot::before,
.hero3-live-dot::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 2px solid var(--h3-rose);
    opacity: 0;
    animation: h3Ping 2s ease-out infinite;
    pointer-events: none;
}
.hero3-live-dot::after { animation-delay: 0.8s; }
@keyframes h3Ping {
    0%   { transform: scale(1);   opacity: 0.8; }
    100% { transform: scale(2.4); opacity: 0;   }
}

/* ---- CTA BUTTON (centered horizontally below stats) ----
   NOTE: st.markdown open/close divs don't actually wrap Streamlit widgets
   in the DOM (each markdown is its own sibling block). So we use a sentinel
   div `.hero3-cta-marker` and style the NEXT sibling [data-testid="stElementContainer"]
   which contains the button. */

/* The marker's container itself (empty) — we hide it */
[data-testid="stElementContainer"]:has(> [data-testid="stMarkdownContainer"] > .hero3-cta-marker) {
    display: none !important;
}

/* Center the button's element-container (the sibling AFTER the marker). */
body:has(.hero3-cta-marker) [data-testid="stElementContainer"]:has([data-testid="stBaseButton-primary"]) {
    display: flex !important;
    flex-direction: row !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    margin: 60px auto 0 auto !important;
    padding: 0 32px 64px !important;
    direction: ltr !important;
    animation: h3FlyUp 0.7s var(--h3-spring) 0.9s both,
               h3CtaBob 3s ease-in-out 2s infinite !important;
}
/* The stButton wrapper itself — also flex-centered so inner button stays centered */
body:has(.hero3-cta-marker) [data-testid="stElementContainer"]:has([data-testid="stBaseButton-primary"]) .stButton,
body:has(.hero3-cta-marker) [data-testid="stElementContainer"]:has([data-testid="stBaseButton-primary"]) > div {
    display: flex !important;
    justify-content: center !important;
    width: auto !important;
    margin: 0 auto !important;
}
@keyframes h3CtaBob {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-5px); }
}
body:has(.hero3-cta-marker) [data-testid="stBaseButton-primary"],
body:has(.hero3-cta-marker) [data-testid="stElementContainer"]:has([data-testid="stBaseButton-primary"]) button {
    background: linear-gradient(135deg, var(--h3-rose) 0%, var(--h3-rose-dk) 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 18px 60px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    font-family: 'Plus Jakarta Sans', 'Assistant', sans-serif !important;
    letter-spacing: 0.02em !important;
    min-width: 220px !important;
    direction: rtl !important;
    cursor: pointer;
    box-shadow:
        0 8px 30px rgba(232,41,76,0.4),
        0 2px 8px rgba(232,41,76,0.2) !important;
    transition: all 0.3s var(--h3-bounce) !important;
    animation: none !important;
}
body:has(.hero3-cta-marker) [data-testid="stBaseButton-primary"]::before,
body:has(.hero3-cta-marker) [data-testid="stElementContainer"]:has([data-testid="stBaseButton-primary"]) button::before {
    display: none !important;
}
body:has(.hero3-cta-marker) [data-testid="stBaseButton-primary"]:hover,
body:has(.hero3-cta-marker) [data-testid="stElementContainer"]:has([data-testid="stBaseButton-primary"]) button:hover {
    transform: scale(1.06) !important;
    box-shadow: 0 16px 50px rgba(232,41,76,0.55) !important;
    background: linear-gradient(135deg, #FF3358 0%, #E8294C 100%) !important;
}
body:has(.hero3-cta-marker) [data-testid="stBaseButton-primary"]:active,
body:has(.hero3-cta-marker) [data-testid="stElementContainer"]:has([data-testid="stBaseButton-primary"]) button:active {
    transform: scale(0.98) !important;
    transition-duration: 0.1s !important;
}

/* ---- Mobile ---- */
@media (max-width: 860px) {
    .hero3-root { padding: 48px 20px 24px; gap: 40px; }
    .hero3-title { font-size: clamp(52px, 14vw, 88px); }
    .hero3-logos { gap: 32px; flex-wrap: wrap; }
    .hero3-stats { flex-direction: column; gap: 28px; }
    .hero3-stat { padding: 0; }
    .hero3-stat-div { width: 60px; height: 1px; }
}

</style>
""", unsafe_allow_html=True)