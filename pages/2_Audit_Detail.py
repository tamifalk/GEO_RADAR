import re
import streamlit as st
from utils.analysts import (
    analyze_gap,
    domain_of,
    build_recommendation,
    company,
    competitors,
    COMPANY_ALIASES,
)
from components.style import apply_custom_css
from components.ui_utils import (
    load_sidebar,
    format_ai_text,
    brand_icon,
    inject_brand_logos_in_tabs,
)
from deep_translator import GoogleTranslator


# פונקציית עזר לתרגום (כדאי לשים בראש הקובץ)
def translate_to_hebrew(text):
    if not text:
        return ""
    try:
        # מתרגם מאנגלית לעברית
        return GoogleTranslator(source="auto", target="iw").translate(text)
    except Exception:
        return text  # אם התרגום נכשל, יחזור הטקסט המקורי (אנגלית)


# ============== הגדרות מעטפת ==============
apply_custom_css()
load_sidebar()
# הזרקת הלוגואים הרשמיים (OpenAI/Gemini/Claude) לטאבים של המודלים
inject_brand_logos_in_tabs()


# ============== פונקציות עזר ויזואליות ==============
def _score_ring(score, size=74):
    """SVG circular progress ring."""
    r = 30
    c = 2 * 3.14159 * r
    pct = max(0, min(100, score)) / 100
    dash = c * pct
    color = "#ED1F4A" if score < 40 else ("#eab308" if score < 70 else "#16a34a")
    return f"""<div class="qx-score-ring">
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
            <circle cx="{size/2}" cy="{size/2}" r="{r}" stroke="#f0f1f5" stroke-width="7" fill="none"/>
            <circle cx="{size/2}" cy="{size/2}" r="{r}" stroke="{color}" stroke-width="7" fill="none"
                    stroke-dasharray="{dash:.1f} {c-dash:.1f}" stroke-linecap="round"/>
        </svg>
        <div class="qx-score-ring-txt">
            <div class="qx-score-val">{score}</div>
            <div class="qx-score-lbl">SCORE</div>
        </div>
    </div>"""


# ============== בדיקת נתונים ==============
has_data = bool(st.session_state.get("audit_results"))

if not has_data:
    st.info("לא נמצאו נתונים להצגה. אנא בצע סריקה בעמוד הראשי.")
    st.stop()

# הכנת האנליזה
results = st.session_state.audit_results
analyses = [analyze_gap(r, company, competitors) for r in results]

# ============== כותרת העמוד ==============
st.markdown(
    '<div class="page-title" style="margin-top:36px">🔬 ניתוח מפורט לכל שאילתה</div>',
    unsafe_allow_html=True,
)

# ============== לולאת השאלות המרכזית ==============
st.markdown(
    """
<style>
    /* זה הקסם: מוצא את הקונטיינר של השאלה וצובע אותו */
    [data-testid="stVerticalBlock"] > div:has(.qx-score-ring) {
        background-color: white !important;
        padding: 30px !important;
        border-radius: 16px !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        margin-bottom: 40px !important;
        direction: rtl !important;
    }
    
    /* תיקון לטאבים בתוך הרקע הלבן */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

for idx, (res, gap) in enumerate(zip(results, analyses), 1):
    with st.container():
        # --- Tags ---
        meta_tags = []
        if gap["score"] > 0:
            meta_tags.append(f'<span class="qx-tag qx-tag-in">✓ {company} מופיע</span>')
        else:
            meta_tags.append(f'<span class="qx-tag qx-tag-out">✗ {company} חסר</span>')

        n_src = len(res.get("sources", []))
        meta_tags.append(f'<span class="qx-tag qx-tag-score">📚 {n_src} מקורות</span>')

        comp_set = set(
            gap["comp_in_gemini"] + gap["comp_in_openai"] + gap["comp_in_sources"]
        )
        for c in list(comp_set)[:4]:
            meta_tags.append(f'<span class="qx-tag qx-tag-comp">⚔ {c}</span>')

        # עטיפה ב-.qx-meta כדי להפעיל את ה-gap (flex) ולקבל מרווח בין התגיות
        meta_html = f'<div class="qx-meta">{"".join(meta_tags)}</div>'

        # --- Header ---
        header_html = f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="background: #ED1F4A; color: white; padding: 5px 15px; border-radius: 10px; font-weight: 800; font-size: 20px;">{idx:02d}</div>
                <div>
                    <div style="font-size: 22px; font-weight: 800; color: #0a1a3a;">{res["question"]}</div>
                    <div style="font-size: 13px; color: #64748b; margin-top: 5px;">{meta_html}</div>
                </div>
            </div>
            <div style="margin-right: auto;">{_score_ring(gap["score"])}</div>
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
        st.markdown(
            '<div style="color: #ED1F4A; font-weight: 800; font-size: 14px; margin-top: 20px; margin-bottom: 10px; direction: rtl; text-align: right;">תשובות מודלי ה-AI:</div>',
            unsafe_allow_html=True,
        )

        # --- AI answers ---
        # --- פונקציית עזר לקיצור טקסט ---
        def wrap_text(txt):
            if not txt or len(txt) <= 250:
                return txt
            visible_part = txt[:250]
            hidden_part = txt[250:]
            return f"""
                {visible_part}...
                <details class="read-more">
                    <summary style="color: #ED1F4A; cursor: pointer; font-weight: bold; font-size: 13px; margin-top: 5px;">קרא עוד ➔</summary>
                    <div style="margin-top: 10px; border-top: 1px dashed #e2e8f0; padding-top: 10px;">{hidden_part}</div>
                </details>
            """

        # st.tabs מקבל טקסט בלבד (לא HTML), לכן משתמשים בשמות המודלים בלי אימוג'ים.
        # הלוגואים הרשמיים מופיעים בגוף הטאב ובסטטוס.
        tab1, tab2, tab3 = st.tabs(["ChatGPT", "Gemini", "Claude"])
        # הכנת הגופים החתוכים
        chat_body = wrap_text(format_ai_text(res.get("openai", "") or ""))
        gem_body = wrap_text(format_ai_text(res.get("gemini", "") or ""))
        claude_body = wrap_text(format_ai_text(res.get("claude", "") or ""))

        # הגדרת התוכן לכל טאב — כולל "תהליך חשיבה" (thinking/reasoning) מה-API
        openai_thinking = (res.get("openai_thinking") or "").strip()
        gemini_thinking = (res.get("gemini_thinking") or "").strip()
        claude_thinking = (res.get("claude_thinking") or "").strip()

        tab_data = [
            (
                "ChatGPT",
                gap["company_in_openai"],
                chat_body,
                openai_thinking,
                "chatgpt",
            ),
            ("Gemini", gap["company_in_gemini"], gem_body, gemini_thinking, "gemini"),
            (
                "Claude",
                gap.get("company_in_claude"),
                claude_body,
                claude_thinking,
                "claude",
            ),
        ]

        for i, tab in enumerate([tab1, tab2, tab3]):
            with tab:
                name, found, body, thinking_txt, theme_key = tab_data[i]
                status_txt = "🟢 נמצא" if found else "🔴 חסר"
                logo_svg = brand_icon(theme_key, size=18)

                # מלבן עם מסגרת אדומה דקיקה שמתחברת לטאב + לוגו רשמי של המודל
                st.markdown(
                    f"""
                    <div style="direction: rtl; text-align: right; padding: 20px; background: #fffcfc; border: 1px solid #ED1F4A; border-radius: 0 0 12px 12px; border-top: none; min-height: 120px;">
                        <div style="font-weight: 800; font-size: 13px; color: #0a1a3a; margin-bottom: 10px; border-bottom: 1px solid #fce7eb; padding-bottom: 8px; display: flex; align-items: center; gap: 8px; flex-direction: row-reverse; justify-content: flex-end;">
                            <span style="display:inline-flex;align-items:center;">{logo_svg}</span>
                            <span>סטטוס נוכחות ב-{name}: {status_txt}</span>
                        </div>
                        <div style="font-size: 15px; color: #334155; line-height: 1.7;">{body}</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

        # --- בלוק תהליך חשיבה מאוחד עם תרגום אוטומטי ---
        with st.expander("💭 תהליך החשיבה המלא (Thinking Process)", expanded=False):
            st.markdown(
                """
                <div style="font-size: 14px; color: #64748b; margin-bottom: 15px; direction: rtl; text-align: right;">
                    כאן ניתן לראות את הניתוח המקדים והלוגיקה הפנימית של המודלים (מתורגם אוטומטית לעברית):
                </div>
            """,
                unsafe_allow_html=True,
            )

            t_tab1, t_tab2, t_tab3 = st.tabs(["ChatGPT", "Gemini", "Claude"])

            with t_tab1:
                if openai_thinking:
                    with st.spinner("מתרגם חשיבת ChatGPT..."):
                        translated_text = translate_to_hebrew(openai_thinking)
                        st.markdown(
                            f'<div class="thinking-box-style">{format_ai_text(translated_text)}</div>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("לא נשלח מידע על תהליך החשיבה עבור מודל זה.")

            with t_tab2:
                if gemini_thinking:
                    with st.spinner("מתרגם חשיבת Gemini..."):
                        translated_text = translate_to_hebrew(gemini_thinking)
                        st.markdown(
                            f'<div class="thinking-box-style">{format_ai_text(translated_text)}</div>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("לא נשלח מידע על תהליך החשיבה עבור מודל זה.")

            with t_tab3:
                if claude_thinking:
                    with st.spinner("מתרגם חשיבת Claude..."):
                        translated_text = translate_to_hebrew(claude_thinking)
                        st.markdown(
                            f'<div class="thinking-box-style">{format_ai_text(translated_text)}</div>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("לא נשלח מידע על תהליך החשיבה עבור מודל זה.")

        # --- עיצוב משלים (נשאר אותו דבר, רק לוודא שהוא נמצא) ---
        st.markdown(
            """
            <style>
                .thinking-box-style {
                    direction: rtl; 
                    text-align: right; 
                    background: #f8fafc; 
                    padding: 20px; 
                    border-radius: 8px; 
                    border-right: 4px solid #ED1F4A; 
                    font-size: 14px; 
                    line-height: 1.6; 
                    font-style: italic;
                    color: #334155;
                    white-space: pre-wrap;
                }
            </style>
        """,
            unsafe_allow_html=True,
        )

        # --- לוגיקת שפיטת קלוד (Judge Reasoning) ---
        if res.get("judgments"):
            with st.expander("⚖️ מאחורי הקלעים: תהליך השיפוט והניתוח של Claude"):
                st.info("כאן ניתן לראות את הנימוקים הלוגיים של קלוד עבור כל אחד מהמודלים שנבדקו.")
                
                # יצירת טאבים להפרדה בין השיפוטים של המודלים השונים
                j_tabs = st.tabs(["Gemini", "ChatGPT", "Claude"])
                
                # מיפוי בין המפתח ב-res לבין הטאב המתאים
                model_map = {
                    "gemini": (j_tabs[0], "Gemini"),
                    "openai": (j_tabs[1], "ChatGPT"),
                    "claude": (j_tabs[2], "Claude")
                }
                
                for key, (tab, name) in model_map.items():
                    with tab:
                        j_data = res["judgments"].get(key)
                        if j_data:
                            # הצגת הציון והפסקה הסופית בקצרה
                            st.subheader(f"ניתוח עבור {name}")
                            col1, col2 = st.columns([1, 4])
                            col1.metric("ציון", f"{j_data.get('score', 0)}/10")
                            col2.write(f"**פסק דין:** {j_data.get('verdict', 'אין פסק דין זמין')}")
                            
                            # הצגת תהליך החשיבה (הלוגיקה) שחילצנו
                            if j_data.get("judge_logic"):
                                st.write("**נימוקי השופט (לוגיקה פנימית):**")
                                # תרגום החשיבה לעברית
                                logic_he = translate_to_hebrew(j_data["judge_logic"])
                                st.markdown(f'<div class="thinking-box-style" style="background-color: #f8f9fa; border-right: 5px solid #6c757d; padding: 15px; font-style: italic;">{format_ai_text(logic_he)}</div>', unsafe_allow_html=True)
                            else:
                                st.warning("לא חולץ תהליך חשיבה עבור שיפוט זה.")
                        else:
                            st.write(f"לא בוצע שיפוט עבור {name}.")

        # --- Sources & Citations ---
        if res.get("sources"):
            n_gem = len(res.get("gemini_sources", []))
            n_cht = len(res.get("openai_sources", []))
            n_cld = len(res.get("claude_sources", []))

            # בניית הכותרת של המלבן עם הנתונים
            expander_title = f"🔗 מקורות שחולצו: Gemini ({n_gem}) | ChatGPT ({n_cht}) | Claude ({n_cld})"
            with st.expander(expander_title):

                src_html = '<div class="qx-src-grid" style="direction: rtl;">'
                for s in res["sources"]:
                    raw_url = s.get("url", "") or ""
                    # Fallback לתצוגה - אם ה-URL עדיין מצביע ל-redirect של Vertex
                    # (סריקות ישנות שנשמרו ב-session state לפני הפיצ' הנוכחי),
                    # ננסה לחלץ דומיין מהכותרת עצמה במקום להציג
                    # vertexaisearch.cloud.google.com למשתמש.
                    if "vertexaisearch.cloud.google.com" in raw_url:
                        title_txt = s.get("title", "") or ""
                        m_dom = re.search(
                            r"([a-zA-Z0-9-]+\.(?:co\.il|com|org|net|gov|edu|io|ai|co))",
                            title_txt,
                        )
                        dom = m_dom.group(1).lower() if m_dom else (title_txt or "מקור")
                    else:
                        dom = domain_of(raw_url)
                    has_us = any(
                        al.lower()
                        in (s.get("title", "") + s.get("content", "") + raw_url).lower()
                        for al in [company] + COMPANY_ALIASES.get(company, [])
                    )

                    title = (s.get("title") or dom)[:75]
                    if len(s.get("title") or "") > 75:
                        title += "…"
                    favicon = f"https://www.google.com/s2/favicons?domain={dom}&sz=64"

                    # לוגיקת התגים (מי השתמש במקור)
                    by = s.get("by", [])
                    by_tag = ""
                    if len(by) >= 3:
                        by_tag = '<span class="qx-src-by qx-src-by-all">🔥</span>'
                    else:
                        # הוספת לוגואים רשמיים של המודלים שהשתמשו במקור
                        if "gemini" in by:
                            by_tag += brand_icon("gemini", size=14)
                        if "openai" in by:
                            by_tag += brand_icon("openai", size=14)
                        if "claude" in by:
                            by_tag += brand_icon("claude", size=14)

                    cls = "qx-src qx-src-us" if has_us else "qx-src"

                    # בניית הכרטיסייה
                    src_html += f"""
                    <a href="{s["url"]}" target="_blank" class="{cls}" style="text-align: right; direction: rtl;">
                        <div class="qx-src-favicon"><img src="{favicon}" alt=""/></div>
                        <div class="qx-src-body">
                            <div class="qx-src-title" style="font-size: 13px;">{title}</div>
                            <div class="qx-src-meta">
                                <span>{dom}</span> {by_tag}
                            </div>
                        </div>
                    </a>"""

                src_html += "</div>"
                st.markdown(src_html, unsafe_allow_html=True)

        with st.expander("המלצות אסטרטגיות ומסקנות לביצוע"):
            # --- Content Brief ---
            brief = res.get("content_brief") or {}  # אם אין בריף, ניצור דיקשנרי ריק
            is_brief_empty = not brief or brief.get("error")

            headline = brief.get("headline", "ממתין לניתוח Claude...")
            meta_desc = brief.get(
                "meta_description", "הנתונים יופיעו לאחר הרצת המודל האסטרטגי."
            )
            outline_html = (
                "".join(f"<li>{h}</li>" for h in brief.get("outline", []))
                or "<li>סעיפי המאמר יופיעו כאן</li>"
            )
            kw_html = (
                "".join(
                    f'<span class="qx-brief-kw-chip">#{k}</span>'
                    for k in brief.get("target_keywords", [])
                )
                or "<span>...</span>"
            )
            args_html = (
                "".join(f"<li>{a}</li>" for a in brief.get("key_arguments", []))
                or "<li>טיעוני המפתח ייווצרו אוטומטית</li>"
            )

            brief_html = f"""
            <div class="qx-brief" style="opacity: {0.6 if is_brief_empty else 1};">
                <div class="qx-brief-head">Content Brief · מוכן לצוות תוכן 
                    <span class="qx-brief-head-badge">{"מיוצר על ידי Claude" if not is_brief_empty else "ממתין לסריקה"}</span>
                </div>
                <div class="qx-brief-body">
                    <div class="qx-brief-h1">{headline}</div>
                    <div class="qx-brief-meta"><b>Meta:</b> {meta_desc}</div>
                    <div class="qx-brief-grid">
                        <div class="qx-brief-box"><div class="qx-brief-box-title">מבנה המאמר (Outline)</div><ol class="qx-brief-outline">{outline_html}</ol></div>
                        <div class="qx-brief-box">
                            <div class="qx-brief-box-title">מילות מפתח</div>
                            <div class="qx-brief-kw">{kw_html}</div>
                            <div class="qx-brief-stat-row" style="margin-top:14px">
                                <span class="qx-brief-stat-key">אורך:</span> 
                                <span class="qx-brief-stat-val">{brief.get('recommended_length', '—')} מילים</span>
                            </div>
                            <div class="qx-brief-platform">
                                <div class="qx-brief-platform-label">לפרסם ב:</div>
                                <div class="qx-brief-platform-dom">{brief.get('recommended_platform', '—')}</div>
                                <div class="qx-brief-platform-reason">{brief.get('platform_reason', 'ממתין לזיהוי פלטפורמה...')}</div>
                            </div>
                        </div>
                    </div>
                    <div class="qx-brief-box"><div class="qx-brief-box-title">טיעוני מפתח לשילוב</div><ul class="qx-brief-args">{args_html}</ul></div>
                    <div class="qx-brief-angle"><span class="qx-brief-angle-label">זווית ייחודית</span> {brief.get('unique_angle', 'ממתין לניתוח זווית שיווקית...')}</div>
                    <div class="qx-brief-impact"><div><b>למה זה צפוי לעבוד:</b> {brief.get('expected_impact', '...')}</div></div>
                    <div class="qx-brief-cta">{brief.get('cta', 'CTA ייווצר בסיום')}</div>
                </div>
            </div>
            """
            st.markdown(brief_html, unsafe_allow_html=True)

            # --- 1. המותג הדומיננטי והמלצות התיקון (מזוקק למנהלים) ---
            judgments = res.get("judgments") or {}
            valid_judgments = [
                (k, v) for k, v in judgments.items() if v and not v.get("error")
            ]

            if valid_judgments:
                judge_cards_html = ""
                for model_key, j in valid_judgments:
                    dom_brand = j.get("dominant_brand") or "—"
                    fix_action = j.get("fix_recommendation", "שמירה על נוכחות קיימת.")
                    # לוגו רשמי של המודל במקום אימוג'י
                    model_logo = brand_icon(model_key, size=16)
                    # שם תצוגה: OpenAI -> ChatGPT
                    display_name = (
                        "ChatGPT"
                        if model_key.lower() == "openai"
                        else model_key.capitalize()
                    )

                    judge_cards_html += f"""
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 15px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-weight: 800; color: #0a1a3a; font-size: 14px; display: inline-flex; align-items: center; gap: 6px; flex-direction: row-reverse;">
                                {model_logo}
                                <span>ניתוח {display_name}</span>
                            </span>
                            <span style="font-size: 11px; background: #ED1F4A; color: white; padding: 2px 8px; border-radius: 6px; font-weight: 700;">
                                מותג דומיננטי: {dom_brand}
                            </span>
                        </div>
                        <div style="font-size: 13px; color: #475569; line-height: 1.5;">
                            <b>המלצת תיקון:</b> {fix_action}
                        </div>
                    </div>
                    """

                # תיקון באג רינדור: Streamlit/Markdown מפרש שורות עם 4+ רווחי הזחה
                # כבלוק קוד, ולכן ה-HTML הוצג כטקסט גולמי. מסירים הזחה מובילה מכל שורה
                # כדי שה-HTML ייפרש כאלמנטי UI ולא כקוד.
                _authority_html = f"""<div style="margin: 20px 0;">
<div style="font-size: 14px; font-weight: 800; color: #64748b; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px;">
AI Brand Authority & Fixes
</div>
{judge_cards_html}
</div>"""
                _authority_html = "\n".join(
                    line.lstrip() for line in _authority_html.splitlines()
                )
                st.markdown(_authority_html, unsafe_allow_html=True)

            # --- 2. המלצה סופית: בלוק "Summary & Final Verdict" הוסר לפי בקשת המשתמש ---
    st.markdown('<div style="height:50px"></div>', unsafe_allow_html=True)
