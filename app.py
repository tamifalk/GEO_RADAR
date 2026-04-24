import streamlit as st
import os
from utils.ai_engine import run_chat_audit, FIXED_QUESTIONS
from utils.analysts import analyze_gap, company, competitors
from components.style import apply_custom_css
from components.ui_utils import load_sidebar, brand_icon

# ============== הגדרות דף חובה (חייב להיות ראשון) ==============
st.set_page_config(
    page_title="GEO RADAR – ביטוח ישיר",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== אתחול זיכרון (Session State) ==============
if 'audit_results' not in st.session_state:
    st.session_state.audit_results = []
if 'baseline_snapshot' not in st.session_state:
    st.session_state.baseline_snapshot = None
if 'scan_phase' not in st.session_state:
    st.session_state.scan_phase = 'hero'

# ============== החלת עיצוב ותפריטים ==============
apply_custom_css()
load_sidebar()

# ============== לוגיקת ניתוב ==============
has_data = bool(st.session_state.audit_results)

# # כותרת הדף המשתנה
# header_text = "AI Visibility Snapshot" if has_data else "GEO Radar – סריקת נוכחות AI"
# st.markdown(f'''
#     <div style="display: flex; justify-content: center; width: 100%; margin: 20px 0;">
#         <div class="page-title" style="text-align: center !important; width: auto;">
#             {header_text}
#         </div>
#     </div>
# ''', unsafe_allow_html=True)

if has_data and st.session_state.scan_phase == 'done':
    st.switch_page("pages/1_Dashboard.py")

# ============== מסכי טרום-סריקה (Hero / Chat) ==============
if not has_data:
    phase = st.session_state.scan_phase

    # --- מסך פתיחה (Hero) ---
    if phase == 'hero':
        # לוגואים קטנים ליד שמות המודלים (ChatGPT / Gemini / Claude)
        _gpt_ico = brand_icon('openai', size=14)
        _gem_ico = brand_icon('gemini', size=14)
        _cld_ico = brand_icon('claude', size=14)

        # אייקוני Outline לסטטיסטיקות - SVG מובנים
        _icon_live = (
            '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="2"/>'
            '<path d="M16.24 7.76a6 6 0 0 1 0 8.49M7.76 16.24a6 6 0 0 1 0-8.49"/>'
            '<path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 19.07a10 10 0 0 1 0-14.14"/>'
            '</svg>'
        )
        _icon_models = (
            '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="5" cy="6" r="2"/><circle cx="5" cy="18" r="2"/>'
            '<circle cx="19" cy="12" r="2"/><circle cx="12" cy="12" r="2.2"/>'
            '<path d="M7 6h3M7 18h3M14 12h3M6.5 7.5l4 3.2M6.5 16.5l4-3.2"/>'
            '</svg>'
        )
        _icon_queries = (
            '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" '
            'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M4 5h13a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H9l-4 3v-3H5a1 1 0 0 1-1-1V5z"/>'
            '<path d="M9 10h6M9 13h4"/>'
            '</svg>'
        )

        st.markdown(f"""
        <div class="hero-card">
            <div class="hero-radar">
                <span class="hero-radar-pulse"></span>
                <span class="hero-radar-pulse hero-radar-pulse-2"></span>
                <span class="hero-radar-pulse hero-radar-pulse-3"></span>
                <div class="hero-radar-title">GEO <span>Radar</span></div>
            </div>
            <div class="hero-sub">
                ננתח איך
                <span class="hero-model">{_gpt_ico}<b>ChatGPT</b></span>,
                <span class="hero-model">{_gem_ico}<b>Gemini</b></span> ו-
                <span class="hero-model">{_cld_ico}<b>Claude</b></span>
                עונים על שאלות ביטוח נפוצות, נזהה מאיפה ה-AI שואב מידע,
                ונגלה מתי <b>ביטוח ישיר</b> מוזכר — ומתי לא.
            </div>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="hero-stat-ico">{_icon_queries}</div>
                    <div class="hero-stat-num">{len(FIXED_QUESTIONS)}</div>
                    <div class="hero-stat-lbl">שאילתות</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-ico">{_icon_models}</div>
                    <div class="hero-stat-num">3</div>
                    <div class="hero-stat-lbl">מודלי AI</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-ico">{_icon_live}</div>
                    <div class="hero-stat-num">Live</div>
                    <div class="hero-stat-lbl">ציטוטים חיים</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # כפתור ממורכז מושלם מתחת לכרטיסיות - ללא קולונות, flex centering טהור
        st.markdown('<div class="hero-btn-wrap">', unsafe_allow_html=True)
        if st.button("התחל סריקה", key="hero_start_scan", type="primary"):
            st.session_state.scan_phase = 'chat'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    # --- מסך סריקה פעילה (Chat) ---
    elif phase == 'chat':
        chat_ph = st.empty()
        run_chat_audit(chat_ph)
        
        # סיום הסריקה ומעבר לדשבורד
        st.session_state.scan_phase = 'done'
        st.rerun()