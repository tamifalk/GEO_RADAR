import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter

from utils.analysts import (
    analyze_gap, compute_executive_summary, domain_of, 
    build_snapshot, simulate_degraded_baseline, 
    company, competitors, COMPANY_ALIASES
)
from components.style import apply_custom_css
from components.ui_utils import load_sidebar, brand_icon

# החלת עיצוב ותפריטים
apply_custom_css()
load_sidebar()

# ============== כותרת עמוד ראשית ==============
st.markdown('''
<div class="page-heading">
    <div class="page-heading-eyebrow">GEO RADAR · לוח בקרה</div>
    <h1 class="page-heading-title">מדד הנראות של <span class="page-heading-accent">ביטוח ישיר</span> במודלי AI</h1>
    <div class="page-heading-sub">
        סקירה אחודה של ציון הנראות, דומיננטיות מתחרים ומקורות מצוטטים - על בסיס שאלות אמיתיות שנשאלו ב-ChatGPT, Gemini ו-Claude.
    </div>
</div>
''', unsafe_allow_html=True)

# בדיקת קיום נתונים ב-Session State
has_data = bool(st.session_state.get('audit_results'))

if has_data:
    results = st.session_state.audit_results
    analyses = [analyze_gap(r, company, competitors) for r in results]
    
    # חישוב סיכום מנהלים
    exec_sum = compute_executive_summary(results, analyses, company)
    
    if exec_sum:
        # פורמט מספרים עם פסיקים
        lost_str = f"{exec_sum['lost_impressions']:,}"
        
        # בניית HTML עבור פעולה בעדיפות עליונה
        if exec_sum['priority_brief']:
            pb = exec_sum['priority_brief']
            action_html = f'''
            <div class="qx-exec-action">
                <div class="qx-exec-action-lbl">🎯 Top Priority Action</div>
                <div class="qx-exec-action-headline">{pb['headline']}</div>
                <div class="qx-exec-action-meta">
                    פרסום ב-<code>{pb['platform']}</code> · {pb['length']} מילים<br/>
                    <span style="opacity:.8">בתגובה לשאלה:</span> {pb['question']}
                </div>
            </div>
            '''
        else:
            action_html = f'''
            <div class="qx-exec-action">
                <div class="qx-exec-action-lbl">✅ Status</div>
                <div class="qx-exec-action-headline">נוכחות תקינה — אין צורך בפעולה מיידית</div>
                <div class="qx-exec-action-meta">המשיכו לעקוב אחר מטריקות חודשיות כדי לתחזק מיצוב.</div>
            </div>
            '''
            
        quick_win_val = exec_sum['quick_win'] or '—'
        quick_win_sub = 'הזדמנות קלה – המקור קיים, רק ה-AI לא בחר להזכיר' if exec_sum['quick_win'] else 'אין quick wins נוכחיים'
    # ============== DASHBOARD: GAUGE + COMPETITORS ==============
    avg_score = sum(a["score"] for a in analyses) / len(analyses)
    comp_counter = Counter()
    for a in analyses:
        comp_counter.update(a["comp_in_gemini"])
        comp_counter.update(a["comp_in_openai"])
        comp_counter.update(a["comp_in_sources"])

    critical_label = "Critical" if avg_score < 40 else ("Medium" if avg_score < 70 else "Strong")
    critical_color = "#ED1F4A" if avg_score < 40 else ("#eab308" if avg_score < 70 else "#16a34a")

    col_g, col_c = st.columns(2, gap="medium")

    with col_g:
        # Gauge Chart — טבעת התקדמות מודרנית עם קצוות מעוגלים (stroke-linecap: round).
        # ה-HTML נבנה בקריאת markdown אחת כדי שכרטיס ה-dash-card יעטוף באמת
        # את הכותרת וה-SVG (רקע לבן אחיד כמו בכרטיס שליד).
        import math
        _pct = max(0.0, min(100.0, float(avg_score))) / 100.0
        _r = 90            # רדיוס הטבעת
        _stroke = 18       # עובי
        _cx, _cy = 110, 110
        _arc_len = math.pi * _r
        _dash = _arc_len * _pct
        _gap = _arc_len - _dash
        gauge_card = f'''
        <div class="dash-card">
            <div class="card-title">AI Visibility Index: <span class="crit" style="color:{critical_color}">{critical_label}</span></div>
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                        padding:10px 0 18px;direction:ltr;">
              <svg width="220" height="140" viewBox="0 0 220 140">
                <!-- רקע -->
                <path d="M {_cx - _r} {_cy} A {_r} {_r} 0 0 1 {_cx + _r} {_cy}"
                      stroke="#f0f1f5" stroke-width="{_stroke}" fill="none" stroke-linecap="round"/>
                <!-- ערך -->
                <path d="M {_cx - _r} {_cy} A {_r} {_r} 0 0 1 {_cx + _r} {_cy}"
                      stroke="{critical_color}" stroke-width="{_stroke}" fill="none"
                      stroke-linecap="round"
                      stroke-dasharray="{_dash:.2f} {_gap:.2f}"/>
                <text x="{_cx}" y="{_cy + 6}" text-anchor="middle"
                      font-family="Assistant, sans-serif" font-size="38" font-weight="800" fill="#0a1a3a">
                  {int(round(avg_score))}%
                </text>
              </svg>
            </div>
        </div>
        '''
        st.markdown(gauge_card, unsafe_allow_html=True)

    with col_c:
        # מרקר שמאפשר ל-CSS (באמצעות :has()) לעטוף את כל תוכן הטור (כותרת + גרף)
        # בתוך כרטיס אחד - פותר את הבעיה של Streamlit שסוגר divs אוטומטית בין אלמנטים.
        st.markdown('<div class="dash-wrap-marker"></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Competitor Dominance</div>', unsafe_allow_html=True)
        
        items = comp_counter.most_common(5)
        labels = [c for c, _ in items]
        values = [v for _, v in items]
        
        # הוספת החברה שלנו להשוואה
        our_count = sum(1 for a in analyses if a["score"] > 0)
        labels.append(company)
        values.append(our_count)
        
        # מיון להצגה
        pairs = sorted(zip(labels, values), key=lambda x: -x[1])
        colors = ['#0a1a3a' if p[0] == company else '#ED1F4A' for p in pairs]
        x_lbls = [p[0] for p in pairs]
        y_vals = [p[1] for p in pairs]
        
        bar = go.Figure(go.Bar(
            x=x_lbls, y=y_vals,
            marker=dict(color=colors, cornerradius=10),
            text=[f"{v}" for v in y_vals],
            textposition='outside',
            textfont=dict(color='#6b7280', size=12, family='Assistant'),
        ))
        bar.update_layout(height=220, margin=dict(l=10, r=10, t=10, b=30),
                          paper_bgcolor='white', plot_bgcolor='white',
                          xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#6b7280', family='Assistant')),
                          yaxis=dict(showgrid=False, visible=False),
                          showlegend=False, font=dict(family='Assistant'))
        
        if not pairs or sum(y_vals) == 0:
            bar.add_annotation(text="אין נתונים עדיין", x=0.5, y=0.5, xref='paper', yref='paper',
                               showarrow=False, font=dict(color='#9aa3b2', size=14))
        
        st.plotly_chart(bar, use_container_width=True, config={'displayModeBar': False})
        
    # ============== TOP CITED SOURCES TABLE ==============
    import re as _re
    feed_rows_html = ""
    dom_stats = {}
    for res in st.session_state.audit_results:
        for s in res.get("sources", []):
            raw_url = s.get('url', '') or ''
            # דילוג על redirectים של Gemini שלא רוזולוצו - לא נציג למשתמש
            # את vertexaisearch.cloud.google.com כמקור. במקום, ננסה לחלץ
            # דומיין מהכותרת. אם גם שם אין - מדלגים על הרשומה.
            if 'vertexaisearch.cloud.google.com' in raw_url:
                title_txt = s.get('title', '') or ''
                m_dom = _re.search(r'([a-zA-Z0-9-]+\.(?:co\.il|com|org|net|gov|edu|io|ai|co))', title_txt)
                if not m_dom:
                    continue
                dom = m_dom.group(1).lower()
            else:
                dom = domain_of(raw_url)
            if not dom: continue
            
            if dom not in dom_stats:
                # הוספת unique_models כדי לספור מודלים שונים
                dom_stats[dom] = {"count": 0, "unique_models": set(), "has_us": False, "url": s['url']}
            
            dom_stats[dom]["count"] += 1
            # הוספת המודל שצוטט (by הוא רשימה של מודלים)
            dom_stats[dom]["unique_models"].update(s.get("by", []))
            
            has_us = any(al.lower() in (s.get('title','')+s.get('content','')+s.get('url','')).lower()
                         for al in [company] + COMPANY_ALIASES.get(company, []))
            if has_us: dom_stats[dom]["has_us"] = True

    # מיון לפי כמות מודלים ייחודיים (הכי חשוב) ואז לפי כמות ציטוטים
    sorted_doms = sorted(dom_stats.items(), key=lambda x: (-len(x[1]["unique_models"]), -x[1]["count"]))[:10]
    total_questions = len(st.session_state.audit_results)

    for dom, d in sorted_doms:
        initial = dom[0].upper() if dom else '?'
        by_set = d["unique_models"]
        n_models = len(by_set)
        
        # בניית ה-HTML של המודלים - עם הלוגואים הרשמיים של OpenAI/Gemini/Claude
        if n_models >= 3:
            by_html = '<span class="feed-by feed-by-all">🔥 כל השלושה</span>'
        elif n_models == 2:
            icons = []
            if 'gemini' in by_set: icons.append(brand_icon('gemini', size=14))
            if 'openai' in by_set: icons.append(brand_icon('openai', size=14))
            if 'claude' in by_set: icons.append(brand_icon('claude', size=14))
            by_html = f'<span class="feed-by feed-by-both">{"".join(icons)} שניים</span>'
        elif n_models == 1:
            m = list(by_set)[0]
            logo = brand_icon(m, size=14)
            name = 'ChatGPT' if m == 'openai' else m.capitalize()
            by_html = f'<span class="feed-by feed-by-{m}">{logo} {name}</span>'
        else:
            by_html = '<span class="feed-by">—</span>'

        # --- התיקון הקריטי: חישוב הפס לפי מודלים (מתוך 3) ---
        freq_pct = int(100 * n_models / 3) 
        freq_html = (f'<div class="feed-freq"><div class="feed-freq-bar">'
                     f'<div class="feed-freq-fill" style="width:{freq_pct}%"></div></div>'
                     f'<span class="feed-freq-txt">{n_models}/3 מודלים</span></div>')

        if d["has_us"]:
            mention_html = '<span class="pill-green">✓ מזכיר</span>'
        else:
            mention_html = '<span class="pill-red">✗ לא מזכיר</span>'

        feed_rows_html += f"""
        <tr>
            <td><div class="src-cell"><span class="src-avatar">{initial}</span>
                <a href="{d['url']}" target="_blank" style="color:#0a1a3a;text-decoration:none;font-weight:600">{dom}</a></div></td>
            <td>{by_html}</td>
            <td>{freq_html}</td>
            <td>{mention_html}</td>
        </tr>"""

    if not feed_rows_html:
        feed_rows_html = '<tr><td colspan="4" style="text-align:center;color:#9aa3b2;padding:28px">הפעל סריקה כדי לצפות בנתונים</td></tr>'

    st.markdown(f"""
    <div class="feed-wrap">
        <div class="feed-title">מקורות מובילים ש-AI מצטט · דאטה אמיתית</div>
        <table class="feed">
            <thead>
                <tr>
                    <th>דומיין</th><th>ציטט על ידי</th><th>תדירות</th><th>מזכיר את {company}?</th>
                </tr>
            </thead>
            <tbody>{feed_rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    if not feed_rows_html:
        st.info("לא נמצאו נתונים להצגה. אנא בצע סריקה בעמוד הראשי.")