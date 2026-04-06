import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image
import pandas as pd
from collections import Counter
from utils import load_colors, get_closest_color_name

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ColorSnap · Color Detector",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Premium CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: #07090f;
    min-height: 100vh;
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"], .stDeployButton,
section[data-testid="stSidebar"] { display: none !important; }

/* ── Main container ── */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── TOP NAV BAR ── */
.top-nav {
    background: rgba(255,255,255,0.02);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 1rem 3rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(20px);
}
.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.nav-logo {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #00d4aa, #0ea5e9);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.nav-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.02em;
}
.nav-badge {
    font-size: 0.65rem;
    font-weight: 600;
    color: #00d4aa;
    background: rgba(0,212,170,0.12);
    border: 1px solid rgba(0,212,170,0.25);
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.nav-stats {
    display: flex;
    gap: 2rem;
    align-items: center;
}
.nav-stat {
    text-align: right;
}
.nav-stat-val {
    font-size: 1.1rem;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1;
}
.nav-stat-lbl {
    font-size: 0.65rem;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 2px;
}

/* ── PAGE WRAPPER ── */
.page-wrap {
    padding: 3rem 4rem;
    max-width: 1280px;
    margin: 0 auto;
}

/* ── HERO ── */
.hero {
    margin-bottom: 3rem;
}
.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #00d4aa;
    margin-bottom: 0.8rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 24px; height: 2px;
    background: #00d4aa;
    border-radius: 2px;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.2rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 1rem;
}
.hero-title span {
    background: linear-gradient(90deg, #00d4aa 0%, #0ea5e9 50%, #f59e0b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    font-size: 1rem;
    color: #64748b;
    line-height: 1.7;
    max-width: 540px;
    font-weight: 400;
}

/* ── DIVIDER ── */
.h-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 2.5rem 0;
}

/* ── UPLOAD ZONE ── */
.upload-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.7rem;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(0,212,170,0.3) !important;
    border-radius: 16px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(0,212,170,0.6) !important;
    background: rgba(0,212,170,0.03) !important;
}
[data-testid="stFileUploader"] label p { display: none !important; }
[data-testid="stFileUploaderDropzone"] span { color: #94a3b8 !important; }
[data-testid="stFileUploaderDropzone"] small { color: #475569 !important; }

/* ── CANVAS SECTION ── */
.canvas-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.7rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.canvas-label .dot {
    width: 6px; height: 6px;
    background: #00d4aa;
    border-radius: 50%;
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── RESULT CARD ── */
.result-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 2rem;
    height: 100%;
    min-height: 480px;
}
.result-header {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 1.5rem;
}

.big-swatch {
    width: 100%;
    height: 140px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    margin-bottom: 1.5rem;
    transition: all 0.4s ease;
}

.detected-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.02em;
    margin-bottom: 0.8rem;
    line-height: 1.2;
}

.badge-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1.8rem;
}
.chip {
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-family: 'Courier New', monospace;
    letter-spacing: 0.02em;
}
.chip-teal  { background: rgba(0,212,170,0.12);  border:1px solid rgba(0,212,170,0.3);  color:#00d4aa; }
.chip-amber { background: rgba(245,158,11,0.12); border:1px solid rgba(245,158,11,0.3); color:#f59e0b; }
.chip-sky   { background: rgba(14,165,233,0.12); border:1px solid rgba(14,165,233,0.3); color:#38bdf8; }

/* ── CHANNEL BARS ── */
.ch-section { margin-bottom: 1rem; }
.ch-label {
    display: flex; justify-content: space-between;
    margin-bottom: 5px;
}
.ch-name { font-size: 0.72rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; }
.ch-val  { font-size: 0.72rem; font-weight: 700; }
.ch-track {
    height: 5px;
    background: rgba(255,255,255,0.05);
    border-radius: 999px;
    overflow: hidden;
}
.ch-fill { height: 100%; border-radius: 999px; }

/* ── METRIC STRIP ── */
.metric-strip {
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
    flex-wrap: wrap;
}
.m-card {
    flex: 1;
    min-width: 160px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.m-card:hover {
    border-color: rgba(0,212,170,0.2);
    background: rgba(0,212,170,0.03);
    transform: translateY(-2px);
}
.m-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%; height: 2px;
}
.m-teal::after  { background: linear-gradient(90deg, #00d4aa, transparent); }
.m-sky::after   { background: linear-gradient(90deg, #0ea5e9, transparent); }
.m-amber::after { background: linear-gradient(90deg, #f59e0b, transparent); }
.m-rose::after  { background: linear-gradient(90deg, #f43f5e, transparent); }

.m-val {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.m-lbl {
    font-size: 0.68rem;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.m-sub {
    font-size: 0.78rem;
    color: #94a3b8;
    font-weight: 500;
    margin-top: 0.2rem;
}

/* ── PALETTE PREVIEW ── */
.palette-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 0.5rem;
}
.pal-chip {
    display: flex; align-items: center; gap: 7px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 999px;
    padding: 0.3rem 0.8rem 0.3rem 0.4rem;
    transition: all 0.2s;
}
.pal-chip:hover {
    border-color: rgba(0,212,170,0.3);
    background: rgba(0,212,170,0.04);
    transform: scale(1.04);
}
.pal-dot {
    width: 20px; height: 20px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.15);
    flex-shrink: 0;
}
.pal-name { font-size: 0.72rem; font-weight: 500; color: #94a3b8; }

/* ── LOG TABLE ── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    overflow: hidden !important;
    background: rgba(255,255,255,0.02) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: rgba(255,255,255,0.05) !important;
    color: #ef4444 !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    background: rgba(239,68,68,0.1) !important;
    border-color: rgba(239,68,68,0.5) !important;
    transform: translateY(-1px) !important;
}
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, rgba(0,212,170,0.15), rgba(14,165,233,0.15)) !important;
    color: #00d4aa !important;
    border: 1px solid rgba(0,212,170,0.35) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.25s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(0,212,170,0.2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(0,212,170,0.2) !important;
}

/* ── Misc ── */
.stMarkdown p { color: #94a3b8 !important; }
[data-testid="stAlert"] {
    background: rgba(0,212,170,0.07) !important;
    border: 1px solid rgba(0,212,170,0.2) !important;
    border-radius: 12px !important;
    color: #94a3b8 !important;
}
[data-testid="stWarning"] {
    background: rgba(245,158,11,0.07) !important;
    border-color: rgba(245,158,11,0.25) !important;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #334155;
}
.empty-icon { font-size: 3rem; margin-bottom: 0.8rem; }
.empty-title { font-size: 1rem; font-weight: 600; color: #475569; margin-bottom: 0.4rem; }
.empty-desc  { font-size: 0.85rem; color: #334155; }

/* ── SECTION TITLE ── */
.sec-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #334155;
    display: flex; align-items: center; gap: 0.7rem;
    margin-bottom: 1rem;
}
.sec-title::after {
    content: ''; flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.05);
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
if "color_log"      not in st.session_state: st.session_state.color_log      = []
if "last_click_pos" not in st.session_state: st.session_state.last_click_pos = None
if "last_color"     not in st.session_state: st.session_state.last_color     = None

colors_df = load_colors()

n_samples = len(st.session_state.color_log)
n_unique  = len(set(e["Color Name"] for e in st.session_state.color_log)) if n_samples else 0
last_name = st.session_state.last_color["name"] if st.session_state.last_color else "—"
last_hex  = st.session_state.last_color["hex"]  if st.session_state.last_color else "—"

# ── TOP NAV ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-nav">
  <div class="nav-brand">
    <div class="nav-logo">🎨</div>
    <div>
      <div class="nav-title">ColorSnap</div>
    </div>
    <span class="nav-badge">v2.0</span>
  </div>
  <div class="nav-stats">
    <div class="nav-stat">
      <div class="nav-stat-val">{n_samples}</div>
      <div class="nav-stat-lbl">Samples</div>
    </div>
    <div class="nav-stat">
      <div class="nav-stat-val">{n_unique}</div>
      <div class="nav-stat-lbl">Unique</div>
    </div>
    <div class="nav-stat">
      <div class="nav-stat-val" style="color:#00d4aa;">{last_hex}</div>
      <div class="nav-stat-lbl">Last HEX</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── PAGE CONTENT ──────────────────────────────────────────────────────────────
with st.container():
    # Padding wrapper via columns
    _, center, _ = st.columns([0.08, 11.84, 0.08])

    with center:
        st.markdown("<br>", unsafe_allow_html=True)

        # ── HERO ──────────────────────────────────────────────────────────────
        st.markdown("""
        <div class="hero">
          <div class="hero-eyebrow">Pixel Intelligence Tool</div>
          <div class="hero-title">
            Detect any color,<br><span>instantly & precisely.</span>
          </div>
          <div class="hero-desc">
            Upload an image, click any pixel, and ColorSnap identifies the exact color — 
            name, RGB, and HEX — matched against 148 CSS3 named colors in milliseconds.
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── METRIC STRIP ──────────────────────────────────────────────────────
        most_common_name = "—"
        if st.session_state.color_log:
            most_common_name = Counter(e["Color Name"] for e in st.session_state.color_log).most_common(1)[0][0]

        st.markdown(f"""
        <div class="metric-strip">
          <div class="m-card m-teal">
            <div class="m-val">{n_samples}</div>
            <div class="m-lbl">Pixels Sampled</div>
          </div>
          <div class="m-card m-sky">
            <div class="m-val">{n_unique}</div>
            <div class="m-lbl">Unique Colors</div>
          </div>
          <div class="m-card m-amber">
            <div class="m-val">{len(colors_df)}</div>
            <div class="m-lbl">Color Database</div>
          </div>
          <div class="m-card m-rose" style="flex:2;">
            <div class="m-val" style="font-size:1.3rem;">{most_common_name}</div>
            <div class="m-lbl">Most Sampled</div>
            <div class="m-sub">{last_hex}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── UPLOAD ────────────────────────────────────────────────────────────
        st.markdown('<div class="sec-title">Upload Image</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "upload",
            type=["png", "jpg", "jpeg"],
            label_visibility="collapsed",
        )

        if uploaded_file:
            try:
                image = Image.open(uploaded_file).convert("RGB")
            except Exception:
                st.error("Could not open the image. Please upload a valid PNG/JPG file.")
                st.stop()

            MAX_WIDTH = 860
            if image.width > MAX_WIDTH:
                scale = MAX_WIDTH / image.width
                image = image.resize((MAX_WIDTH, int(image.height * scale)), Image.LANCZOS)
            image_np = np.array(image)

            st.markdown('<div class="h-line"></div>', unsafe_allow_html=True)

            # ── CANVAS + RESULT SPLIT ─────────────────────────────────────────
            img_col, res_col = st.columns([3, 2], gap="large")

            with img_col:
                st.markdown("""
                <div class="canvas-label">
                    <span class="dot"></span>
                    Live Canvas — click a pixel
                </div>""", unsafe_allow_html=True)

                canvas_result = st_canvas(
                    fill_color="rgba(0,0,0,0)",
                    stroke_width=0,
                    background_image=image,
                    update_streamlit=True,
                    height=image_np.shape[0],
                    width=image_np.shape[1],
                    drawing_mode="point",
                    key="canvas",
                )

            with res_col:
                # ── Process click ─────────────────────────────────────────────
                if canvas_result.json_data and len(canvas_result.json_data["objects"]) > 0:
                    last_obj = canvas_result.json_data["objects"][-1]
                    x, y = int(last_obj["left"]), int(last_obj["top"])

                    if 0 <= x < image_np.shape[1] and 0 <= y < image_np.shape[0]:
                        r = int(image_np[y, x, 0])
                        g = int(image_np[y, x, 1])
                        b = int(image_np[y, x, 2])
                        color_name = get_closest_color_name(r, g, b, colors_df)
                        hex_val    = f"#{r:02X}{g:02X}{b:02X}"

                        # Luminance to pick text color on swatch
                        lum = 0.299*r + 0.587*g + 0.114*b
                        txt = "#000000" if lum > 160 else "#ffffff"

                        st.markdown(f"""
                        <div class="result-card">
                          <div class="result-header">Color Analysis</div>

                          <div class="big-swatch" style="background:rgb({r},{g},{b});
                               display:flex; align-items:flex-end; padding:0.8rem 1rem;">
                            <span style="font-size:0.75rem; font-weight:700;
                                         color:{txt}; opacity:0.7; font-family:'Courier New',monospace;">
                              {hex_val}
                            </span>
                          </div>

                          <div class="detected-name">{color_name}</div>

                          <div class="badge-row">
                            <span class="chip chip-teal">RGB({r}, {g}, {b})</span>
                            <span class="chip chip-amber">{hex_val}</span>
                            <span class="chip chip-sky">x={x} · y={y}</span>
                          </div>

                          <div class="ch-section">
                            <div class="ch-label">
                              <span class="ch-name">Red</span>
                              <span class="ch-val" style="color:#ef4444;">{r}</span>
                            </div>
                            <div class="ch-track">
                              <div class="ch-fill" style="width:{round(r/255*100,1)}%;
                                   background:linear-gradient(90deg,#ef4444,#fca5a5);"></div>
                            </div>
                          </div>

                          <div class="ch-section">
                            <div class="ch-label">
                              <span class="ch-name">Green</span>
                              <span class="ch-val" style="color:#22c55e;">{g}</span>
                            </div>
                            <div class="ch-track">
                              <div class="ch-fill" style="width:{round(g/255*100,1)}%;
                                   background:linear-gradient(90deg,#22c55e,#86efac);"></div>
                            </div>
                          </div>

                          <div class="ch-section">
                            <div class="ch-label">
                              <span class="ch-name">Blue</span>
                              <span class="ch-val" style="color:#3b82f6;">{b}</span>
                            </div>
                            <div class="ch-track">
                              <div class="ch-fill" style="width:{round(b/255*100,1)}%;
                                   background:linear-gradient(90deg,#3b82f6,#93c5fd);"></div>
                            </div>
                          </div>

                        </div>
                        """, unsafe_allow_html=True)

                        # ── Deduplicate & log ─────────────────────────────────
                        pos = (x, y)
                        if pos != st.session_state.last_click_pos:
                            st.session_state.last_click_pos = pos
                            st.session_state.last_color = {"name": color_name, "hex": hex_val}
                            st.session_state.color_log.append({
                                "Color Name": color_name,
                                "HEX": hex_val,
                                "R": r, "G": g, "B": b,
                                "X": x, "Y": y,
                            })
                            st.experimental_rerun()
                    else:
                        st.warning("Click inside the image bounds.")
                else:
                    st.markdown("""
                    <div class="result-card">
                      <div class="result-header">Color Analysis</div>
                      <div class="empty-state">
                        <div class="empty-icon">👆</div>
                        <div class="empty-title">No pixel selected</div>
                        <div class="empty-desc">Click anywhere on the<br>image to detect a color</div>
                      </div>
                    </div>""", unsafe_allow_html=True)

            # ── PALETTE STRIP ─────────────────────────────────────────────────
            if st.session_state.color_log:
                st.markdown('<div class="h-line"></div>', unsafe_allow_html=True)
                st.markdown('<div class="sec-title">Sampled Palette</div>', unsafe_allow_html=True)

                seen = {}
                for entry in st.session_state.color_log:
                    nm = entry["Color Name"]
                    if nm not in seen:
                        seen[nm] = (entry["R"], entry["G"], entry["B"])

                chips_html = '<div class="palette-row">'
                for nm, (pr, pg, pb) in list(seen.items())[:24]:
                    chips_html += f"""
                    <div class="pal-chip">
                      <div class="pal-dot" style="background:rgb({pr},{pg},{pb});"></div>
                      <span class="pal-name">{nm}</span>
                    </div>"""
                chips_html += "</div>"
                st.markdown(chips_html, unsafe_allow_html=True)

                # ── LOG TABLE ─────────────────────────────────────────────────
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f'<div class="sec-title">Color Log — {n_samples} samples</div>',
                            unsafe_allow_html=True)

                df_log = pd.DataFrame(st.session_state.color_log)

                tbl, dl, clr = st.columns([5, 1, 1])
                with tbl:
                    st.dataframe(
                        df_log, use_container_width=True, hide_index=True,
                        column_config={
                            "Color Name": st.column_config.TextColumn("Color Name", width="medium"),
                            "HEX":        st.column_config.TextColumn("HEX",        width="small"),
                            "R":          st.column_config.NumberColumn("R",         width="small"),
                            "G":          st.column_config.NumberColumn("G",         width="small"),
                            "B":          st.column_config.NumberColumn("B",         width="small"),
                            "X":          st.column_config.NumberColumn("X Pos",     width="small"),
                            "Y":          st.column_config.NumberColumn("Y Pos",     width="small"),
                        }
                    )
                with dl:
                    csv = df_log.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Export CSV", csv, "colorsnap_log.csv",
                                       "text/csv", use_container_width=True)
                with clr:
                    if st.button("🗑️ Clear", use_container_width=True):
                        st.session_state.color_log      = []
                        st.session_state.last_click_pos = None
                        st.session_state.last_color     = None
                        st.rerun()

        else:
            # ── EMPTY STATE ───────────────────────────────────────────────────
            st.markdown("""
            <div style="text-align:center; padding:6rem 2rem;
                        border:1.5px dashed rgba(255,255,255,0.06);
                        border-radius:20px; margin-top:2rem;
                        background:rgba(255,255,255,0.01);">
              <div style="font-size:3.5rem; margin-bottom:1rem;">🖼️</div>
              <div style="font-size:1.1rem; font-weight:600; color:#334155; margin-bottom:0.4rem;">
                Upload an image to get started
              </div>
              <div style="font-size:0.85rem; color:#1e293b;">
                Supports PNG · JPG · JPEG
              </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)
