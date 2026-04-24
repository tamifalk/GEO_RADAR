import streamlit as st
import os
import textwrap
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
        # לוגואים גדולים למודלים (40px)
        _gpt_lg = brand_icon('openai', size=40)
        _gem_lg = brand_icon('gemini', size=40)
        _cld_lg = brand_icon('claude', size=40)

        # Stat icons (36px lucide-style)
        _ico_live = (
            '<svg viewBox="0 0 24 24" width="36" height="36" fill="none" '
            'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="2"/>'
            '<path d="M16.24 7.76a6 6 0 0 1 0 8.49M7.76 16.24a6 6 0 0 1 0-8.49"/>'
            '<path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 19.07a10 10 0 0 1 0-14.14"/>'
            '</svg>'
        )
        _ico_models = (
            '<svg viewBox="0 0 24 24" width="36" height="36" fill="none" '
            'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="5" cy="6" r="2"/><circle cx="5" cy="18" r="2"/>'
            '<circle cx="19" cy="12" r="2"/><circle cx="12" cy="12" r="2.2"/>'
            '<path d="M7 6h3M7 18h3M14 12h3M6.5 7.5l4 3.2M6.5 16.5l4-3.2"/>'
            '</svg>'
        )
        _ico_queries = (
            '<svg viewBox="0 0 24 24" width="36" height="36" fill="none" '
            'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M4 5h13a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H9l-4 3v-3H5a1 1 0 0 1-1-1V5z"/>'
            '<path d="M9 10h6M9 13h4"/>'
            '</svg>'
        )

        # === HERO v3 — centered, airy, no card frames ===
        hero_html = textwrap.dedent(f"""
        <div class="hero3-root">
        <div class="hero3-blob hero3-blob--crimson-tr"></div>
        <h1 class="hero3-title">
        <span class="hero3-title-word hero3-title-word--geo">GEO</span>
        <span class="hero3-title-word hero3-title-word--radar">Radar</span>
        </h1>
        <p class="hero3-tagline">AI-Powered Security Intelligence · Real Time</p>
        <div class="hero3-logos">
        <div class="hero3-logo hero3-logo--openai">
        <div class="hero3-logo-glow"></div>
        <div class="hero3-logo-icon">{_gpt_lg}</div>
        <div class="hero3-logo-name">ChatGPT</div>
        </div>
        <div class="hero3-logo hero3-logo--gemini">
        <div class="hero3-logo-glow"></div>
        <div class="hero3-logo-icon">{_gem_lg}</div>
        <div class="hero3-logo-name">Gemini</div>
        </div>
        <div class="hero3-logo hero3-logo--claude">
        <div class="hero3-logo-glow"></div>
        <div class="hero3-logo-icon">{_cld_lg}</div>
        <div class="hero3-logo-name">Claude</div>
        </div>
        </div>
        <div class="hero3-stats">
        <div class="hero3-stat hero3-stat--live">
        <div class="hero3-stat-icon">{_ico_live}</div>
        <div class="hero3-stat-num hero3-stat-num--live"><span class="hero3-live-dot"></span>Live</div>
        <div class="hero3-stat-lbl">ציטוטים חיים</div>
        </div>
        <div class="hero3-stat-div"></div>
        <div class="hero3-stat">
        <div class="hero3-stat-icon">{_ico_models}</div>
        <div class="hero3-stat-num">3</div>
        <div class="hero3-stat-lbl">מודלי AI</div>
        </div>
        <div class="hero3-stat-div"></div>
        <div class="hero3-stat">
        <div class="hero3-stat-icon">{_ico_queries}</div>
        <div class="hero3-stat-num">{len(FIXED_QUESTIONS)}</div>
        <div class="hero3-stat-lbl">שאילתות</div>
        </div>
        </div>
        </div>
        """).strip()
        st.markdown(hero_html, unsafe_allow_html=True)

        # CTA button — centered via sentinel marker (Streamlit doesn't let markdown wrap widgets)
        st.markdown('<div class="hero3-cta-marker"></div>', unsafe_allow_html=True)
        if st.button("התחל סריקה", key="hero_start_scan", type="primary"):
            st.session_state.scan_phase = 'chat'
            st.rerun()
        st.stop()

    # --- מסך סריקה פעילה (Chat) ---
    elif phase == 'chat':
        chat_ph = st.empty()
        run_chat_audit(chat_ph)
        
        # סיום הסריקה ומעבר לדשבורד
        st.session_state.scan_phase = 'done'
        st.rerun()