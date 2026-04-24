import streamlit as st
import os
import re
import base64

# =========================================================
# Brand Icons - SVG של הלוגואים הרשמיים של OpenAI / Gemini / Claude
# משמש בכל מקום שבו הוצגו האימוג'ים 🧠 / ✨ / 🎭 כסמלי מודלים.
# =========================================================

# OpenAI / ChatGPT - לוגו ה-"knot" בשחור (מפושט לקו-ארט נקי)
_OPENAI_SVG = (
    '<svg viewBox="0 0 24 24" width="{size}" height="{size}" '
    'xmlns="http://www.w3.org/2000/svg" aria-label="OpenAI" role="img" '
    'style="vertical-align:middle;flex-shrink:0;">'
    '<path fill="#0a0a0a" d="M22.28 9.82a5.98 5.98 0 0 0-.52-4.91 6.05 6.05 0 0 0-6.52-2.9A6.07 6.07 0 0 0 4.98 4.18a5.98 5.98 0 0 0-3.99 2.9 6.05 6.05 0 0 0 .74 7.1 5.98 5.98 0 0 0 .52 4.91 6.05 6.05 0 0 0 6.52 2.9 5.98 5.98 0 0 0 4.51 2.01 6.05 6.05 0 0 0 5.77-4.19 5.98 5.98 0 0 0 3.99-2.9 6.05 6.05 0 0 0-.76-7.09zm-9 12.61a4.5 4.5 0 0 1-2.88-1.04l.14-.08 4.78-2.76a.78.78 0 0 0 .39-.68v-6.74l2.02 1.17c.02.01.03.03.04.05v5.58a4.5 4.5 0 0 1-4.49 4.5zM3.64 18.57a4.46 4.46 0 0 1-.54-3.02l.14.08 4.78 2.76a.78.78 0 0 0 .79 0l5.84-3.37v2.33c0 .02-.01.04-.03.06l-4.83 2.79a4.5 4.5 0 0 1-6.15-1.63zM2.39 8.28a4.47 4.47 0 0 1 2.35-1.97v5.68a.78.78 0 0 0 .39.68l5.82 3.36-2.02 1.17a.07.07 0 0 1-.07 0L4.02 14.4a4.5 4.5 0 0 1-1.63-6.12zm16.6 3.86L13.15 8.78l2.02-1.17a.07.07 0 0 1 .07 0l4.83 2.79a4.5 4.5 0 0 1-.68 8.1v-5.68a.78.78 0 0 0-.4-.68zm2.01-3.02l-.14-.09-4.77-2.78a.78.78 0 0 0-.79 0l-5.84 3.37V7.29c0-.02.01-.04.03-.06l4.83-2.78a4.5 4.5 0 0 1 6.68 4.66zm-12.67 4.15l-2.02-1.17a.07.07 0 0 1-.04-.05V6.47a4.5 4.5 0 0 1 7.38-3.45l-.14.08L8.74 5.86a.78.78 0 0 0-.39.68zm1.1-2.37l2.6-1.5 2.6 1.5v3l-2.6 1.5-2.6-1.5z"/>'
    '</svg>'
)

# Gemini - כוכב מעוין 4-קודקודים עם גרדיאנט כחול-סגול-צהוב
_GEMINI_SVG = (
    '<svg viewBox="0 0 24 24" width="{size}" height="{size}" '
    'xmlns="http://www.w3.org/2000/svg" aria-label="Gemini" role="img" '
    'style="vertical-align:middle;flex-shrink:0;">'
    '<defs>'
    '<linearGradient id="gemGrad{uid}" x1="0%" y1="0%" x2="100%" y2="100%">'
    '<stop offset="0%" stop-color="#1BA1E3"/>'
    '<stop offset="35%" stop-color="#5489D6"/>'
    '<stop offset="65%" stop-color="#9B72CB"/>'
    '<stop offset="100%" stop-color="#D96570"/>'
    '</linearGradient>'
    '</defs>'
    '<path fill="url(#gemGrad{uid})" d="M12 2 L14.5 9.5 L22 12 L14.5 14.5 L12 22 L9.5 14.5 L2 12 L9.5 9.5 Z"/>'
    '</svg>'
)

# Claude / Anthropic - התפרצות כתומה (sparkle)
_CLAUDE_SVG = (
    '<svg viewBox="0 0 24 24" width="{size}" height="{size}" '
    'xmlns="http://www.w3.org/2000/svg" aria-label="Claude" role="img" '
    'style="vertical-align:middle;flex-shrink:0;">'
    '<g fill="#D97757">'
    '<path d="M12 1.5 L13.1 9.5 L12 11 L10.9 9.5 Z"/>'
    '<path d="M12 22.5 L10.9 14.5 L12 13 L13.1 14.5 Z"/>'
    '<path d="M22.5 12 L14.5 13.1 L13 12 L14.5 10.9 Z"/>'
    '<path d="M1.5 12 L9.5 10.9 L11 12 L9.5 13.1 Z"/>'
    '<path d="M19.4 4.6 L14.3 10.3 L12.7 10.5 L13.5 9 Z"/>'
    '<path d="M4.6 19.4 L9.7 13.7 L11.3 13.5 L10.5 15 Z"/>'
    '<path d="M19.4 19.4 L13.7 14.3 L13.5 12.7 L15 13.5 Z"/>'
    '<path d="M4.6 4.6 L10.3 9.7 L10.5 11.3 L9 10.5 Z"/>'
    '</g>'
    '</svg>'
)

def brand_icon(name: str, size: int = 16) -> str:
    """החזרת SVG inline של הלוגו הרשמי של מודל ה-AI.
    name: 'openai' | 'chatgpt' | 'gemini' | 'claude'
    """
    key = (name or '').lower().strip()
    # uid ייחודי למניעת התנגשות id של gradient כאשר מספר לוגואים על אותו עמוד
    uid = str(abs(hash(f"{key}-{size}")) % 10_000_000)
    if key in ('openai', 'chatgpt', 'gpt'):
        return _OPENAI_SVG.format(size=size)
    if key == 'gemini':
        return _GEMINI_SVG.format(size=size, uid=uid)
    if key in ('claude', 'anthropic'):
        return _CLAUDE_SVG.format(size=size)
    return ''


def _svg_data_uri(svg: str) -> str:
    """המרת SVG טקסטואלי ל-data URI לשימוש ב-CSS url()."""
    import urllib.parse as _urlp
    # ניקוי רווחים מיותרים + URL-encode
    compact = ' '.join(svg.split())
    return "data:image/svg+xml;charset=utf-8," + _urlp.quote(compact, safe="")


def inject_brand_logos_in_tabs():
    """מזריק CSS שמוסיף את הלוגואים הרשמיים של OpenAI / Gemini / Claude
    לפני הכיתוב של הטאבים. הסדר חייב להיות ChatGPT / Gemini / Claude
    בקריאת st.tabs כדי ש-nth-of-type יתאים."""
    uid = "tabs"
    openai_uri = _svg_data_uri(_OPENAI_SVG.format(size=16))
    gemini_uri = _svg_data_uri(_GEMINI_SVG.format(size=16, uid=uid))
    claude_uri = _svg_data_uri(_CLAUDE_SVG.format(size=16))
    st.markdown(f"""
<style>
/* הוספת לוגו המותג לפני שם הטאב (ChatGPT / Gemini / Claude).
   הסדר מבוסס על מיקום הטאב ב-st.tabs. */
.stTabs [data-baseweb="tab-list"] [data-baseweb="tab"]::before {{
    content: '';
    display: inline-block;
    width: 16px; height: 16px;
    margin-left: 8px;
    margin-right: 0;
    vertical-align: middle;
    background-repeat: no-repeat;
    background-position: center;
    background-size: contain;
}}
.stTabs [data-baseweb="tab-list"] [data-baseweb="tab"]:nth-of-type(1)::before {{
    background-image: url("{openai_uri}");
}}
.stTabs [data-baseweb="tab-list"] [data-baseweb="tab"]:nth-of-type(2)::before {{
    background-image: url("{gemini_uri}");
}}
.stTabs [data-baseweb="tab-list"] [data-baseweb="tab"]:nth-of-type(3)::before {{
    background-image: url("{claude_uri}");
}}
</style>
""", unsafe_allow_html=True)

# --- בועות צ'אט ועיצוב טקסט AI ---

def _bubble_user(q):
    """יצירת בועת משתמש לשלב הסריקה"""
    return f'<div class="bubble-row bubble-row-user"><div class="bubble-user">{q}</div></div>'

def _bubble_ai_typing():
    """יצירת אנימציית טעינה (שלוש נקודות) של ה-AI"""
    return '<div class="bubble-row bubble-row-ai"><div class="bubble-ai"><div class="typing"><span></span><span></span><span></span></div></div></div>'

def _bubble_ai_done(n_sources, domains):
    """יצירת בועת סיום שאילתה עם פירוט מקורות"""
    tags = "".join(f'<span class="src-tag">{d}</span>' for d in domains[:3])
    return (f'<div class="bubble-row bubble-row-ai"><div class="bubble-ai">'
            f'✅ קיבלתי תשובות מ-<b>ChatGPT</b>, <b>Gemini</b> ו-<b>Claude</b> · חולצו <b>{n_sources}</b> מקורות<br>'
            f'<div style="margin-top:6px">{tags}</div></div></div>')

def format_ai_text(text):
    """המרת Markdown links לקישורי HTML יפים + הסתרת URLs חשופים ארוכים"""
    if not text:
        return ""
    # [text](url) -> <a href="url" target="_blank">text</a>
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        lambda m: f'<a href="{m.group(2)}" target="_blank" class="ai-link">{m.group(1)}</a>',
        text
    )
    # URLs חשופים ארוכים -> קישור עם דומיין בלבד
    def _short_url(m):
        url = m.group(0)
        dom = re.sub(r'^https?://(www\.)?', '', url).split('/')[0]
        return f'<a href="{url}" target="_blank" class="ai-link">{dom}</a>'
    text = re.sub(r'https?://[^\s<)"]+', _short_url, text)
    # **bold** -> <b>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    # newlines
    text = text.replace('\n', '<br>')
    return text

# --- ניווט ולוגו ---

def _load_logo():
    """טעינת לוגו מקובץ מקומי או החזרת SVG חלופי של ביטוח ישיר"""
    for ext in ('png', 'jpg', 'jpeg', 'svg'):
        p = f"logo.{ext}"
        if os.path.exists(p):
            mime = 'image/svg+xml' if ext == 'svg' else f'image/{ext if ext != "jpg" else "jpeg"}'
            with open(p, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode()
            return f'<img src="data:{mime};base64,{b64}" style="max-width:100%;height:auto;display:block;">'
    
    # fallback SVG של ביטוח ישיר במידה ואין קובץ לוגו
    return ('<div class="idi-logo-row">'
            '<div class="idi-logo-text">'
            '<div class="idi-logo-top">ביטוח</div>'
            '<div class="idi-logo-bottom">ישיר</div>'
            '<div class="idi-logo-tag">IDI חברה לביטוח בע״מ</div>'
            '</div>'
            '<div class="idi-logo-dots">'
            '<svg width="56" height="40" viewBox="0 0 56 40">'
            '<circle cx="8" cy="8" r="6" fill="#ED1F4A"/>'
            '<circle cx="28" cy="8" r="6" fill="#ED1F4A"/>'
            '<circle cx="48" cy="8" r="6" fill="#ED1F4A"/>'
            '<circle cx="28" cy="28" r="6" fill="#ED1F4A"/>'
            '<circle cx="48" cy="28" r="6" fill="#ED1F4A"/>'
            '</svg></div></div>')

def load_sidebar():
    """סרגל צד מותאם אישית עם לוגו וניווט בעברית + אייקונים של Material.
    מחליף את ה-stSidebarNav האוטומטי של Streamlit (שמציג שמות קבצים באנגלית)
    בניווט מותאם עם תוויות בעברית ואייקונים קוויים מימין לטקסט."""
    with st.sidebar:
        # לוגו בראש הסרגל
        st.markdown(f'<div class="idi-logo-wrap">{_load_logo()}</div>', unsafe_allow_html=True)

        # ניווט מותאם אישית - טקסט מיושר לימין עם אייקון קווי לצידו
        st.markdown('<div class="idi-nav">', unsafe_allow_html=True)
        st.page_link("pages/1_Dashboard.py",    label="לוח בקרה",    icon=":material/monitoring:")
        st.page_link("pages/2_Audit_Detail.py", label="פרטי ביקורת", icon=":material/search_insights:")
        st.page_link("pages/3_Comparison.py",   label="השוואה",       icon=":material/balance:")
        st.markdown('</div>', unsafe_allow_html=True)


def load_top_bar():
    """טעינת ה-Top Bar המעוצב לכל עמודי האפליקציה"""
    st.markdown("""
    <div class="top-bar">
        <div class="top-bar-left">
            <span>☰</span>
            <span>★</span>
            <span>Dashboards</span>
            <span class="top-bar-sep">/</span>
            <span class="top-bar-crumb-active">Default</span>
        </div>
        <div class="top-search">
            <span>🔍 Search</span>
            <span>⌘/</span>
        </div>
        <div class="top-bar-icons">
            <span>☀️</span><span>↻</span><span>🔔</span><span>☰</span>
        </div>
    </div>
    """, unsafe_allow_html=True)