
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Wiegand's Tree Finder POC",
    page_icon="🌳",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data
def load_data():
    path = Path(__file__).with_name("tree_database.csv")
    return pd.read_csv(path)

df = load_data()

# ---------- Styling ----------
st.markdown("""
<style>
:root {
    --wg-green: #2f5d3a;
    --wg-light: #f5f8f2;
    --wg-border: #dce6d7;
    --wg-text: #243127;
}
.block-container {
    max-width: 1280px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}
.hero {
    background: linear-gradient(135deg, #f5f8f2 0%, #eef4ea 100%);
    border: 1px solid #dce6d7;
    border-radius: 18px;
    padding: 28px 30px 24px 30px;
    margin-bottom: 22px;
}
.hero-title {
    font-size: 2.15rem;
    font-weight: 800;
    color: #2f5d3a;
    margin-bottom: 6px;
}
.hero-sub {
    font-size: 1.05rem;
    color: #586458;
}
.tree-card {
    border: 1px solid #dce6d7;
    border-radius: 16px;
    padding: 18px;
    margin: 0 0 16px 0;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.035);
}
.photo-placeholder {
    height: 185px;
    border-radius: 12px;
    background: #edf3e9;
    border: 1px dashed #c8d5c2;
    display:flex;
    align-items:center;
    justify-content:center;
    color:#6d786b;
    font-weight:650;
    text-align:center;
    padding: 12px;
}
.match-pill {
    display:inline-block;
    background:#edf6e9;
    color:#2f5d3a;
    border:1px solid #cfdfc8;
    border-radius:999px;
    padding:6px 10px;
    font-size:.95rem;
    font-weight:750;
    margin-top:10px;
}
.status-pill {
    display:inline-block;
    background:#f7f7f7;
    border:1px solid #dedede;
    border-radius:999px;
    padding:5px 9px;
    font-size:.82rem;
    margin-top:8px;
}
.meta {
    color:#5f685f;
    font-size:.92rem;
}
.reason {
    background:#f5f8f2;
    border-left:4px solid #6c8f66;
    padding:10px 12px;
    border-radius:8px;
    margin-top:10px;
}
.warning {
    background:#fbf6ea;
    border-left:4px solid #c49a47;
    padding:10px 12px;
    border-radius:8px;
    margin-top:10px;
}
.small-note {
    font-size:.88rem;
    color:#697269;
}
</style>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero">
  <div class="hero-title">Wiegand's Michigan Tree Finder</div>
  <div class="hero-sub">
    Select the characteristics that matter most and see Michigan-suitable tree recommendations from the current POC database.
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar filters ----------
with st.sidebar:
    st.header("Find a Tree")

    tree_types = ["Any"] + sorted(df["tree_type"].dropna().unique().tolist())
    tree_type = st.selectbox("Tree type", tree_types)

    use_height = st.checkbox("Limit mature height", value=False)
    if use_height:
        max_height = st.slider("Maximum mature height (ft)", 5, 100, 30, step=5)
    else:
        max_height = None

    use_width = st.checkbox("Limit mature width", value=False)
    if use_width:
        max_width = st.slider("Maximum mature width (ft)", 5, 100, 30, step=5)
    else:
        max_width = None

    flowering = st.selectbox("Flowering", ["Either", "Yes", "No"])
    sun = st.selectbox(
        "Sun needs",
        ["Either", "Full Sun", "Partial Sun", "Partial Shade", "Shade"]
    )

    prioritize_wiegands = st.checkbox(
        "Prioritize Wiegand's priority candidates",
        value=True
    )

    result_count = st.slider("Number of recommendations", 3, 10, 5)

    st.divider()
    st.caption(
        "POC note: Wiegand's availability is provisional until the actual "
        "Wiegand's product database is connected."
    )

# ---------- Hard filters ----------
filtered = df[df["michigan_suitable"].astype(str).str.lower().eq("yes")].copy()

if tree_type != "Any":
    filtered = filtered[filtered["tree_type"] == tree_type]

if max_height is not None:
    # Hard constraint: exclude anything whose stated mature maximum exceeds the user's max.
    filtered = filtered[filtered["height_max"] <= max_height]

if max_width is not None:
    filtered = filtered[filtered["width_max"] <= max_width]

if flowering != "Either":
    filtered = filtered[filtered["flowering"] == flowering]

SUN_COMPATIBILITY = {
    "Full Sun": {"Full Sun"},
    "Partial Sun": {"Full Sun", "Partial Sun", "Partial Shade"},
    "Partial Shade": {"Partial Sun", "Partial Shade", "Shade"},
    "Shade": {"Shade", "Partial Shade"},
}

if sun != "Either":
    acceptable = SUN_COMPATIBILITY[sun]
    filtered = filtered[
        filtered["sun_needs"].astype(str).apply(
            lambda x: any(
                option in acceptable
                for option in [s.strip() for s in x.split(";")]
            )
        )
    ]

# ---------- Ranking ----------
def rank_row(row):
    score = 50
    reasons = []

    if tree_type != "Any":
        score += 20
        reasons.append(f"matches the requested {tree_type} category")

    if max_height is not None:
        score += 10
        reasons.append(f"stays at or below {max_height} ft mature height")

    if max_width is not None:
        score += 10
        reasons.append(f"stays at or below {max_width} ft mature width")

    if flowering != "Either":
        score += 5
        reasons.append("matches the flowering preference")

    if sun != "Either":
        score += 5
        reasons.append(f"fits the requested {sun.lower()} light conditions")

    bonus = 0
    if prioritize_wiegands and "Priority candidate" in str(row["wiegands_status"]):
        bonus = 3
        reasons.append("is flagged as a Wiegand's priority candidate in the POC")

    # Displayed match should not exceed 100.
    match = min(score, 100)
    return pd.Series({
        "match_pct": match,
        "sort_score": score + bonus,
        "reasons": "; ".join(reasons) if reasons else "Michigan-suitable option from the starter database"
    })

if not filtered.empty:
    ranked = filtered.copy()
    ranked = pd.concat([ranked, ranked.apply(rank_row, axis=1)], axis=1)
    ranked = ranked.sort_values(["sort_score", "common_name"], ascending=[False, True])
    ranked = ranked.head(result_count)
else:
    ranked = filtered

# ---------- Results ----------
left, right = st.columns([2.3, 1], gap="large")

with left:
    st.subheader("Recommended Trees")

    if ranked.empty:
        st.warning(
            "No trees in the current starter database satisfy all of those requirements. "
            "Try relaxing one constraint."
        )
    else:
        st.write(f"Showing **{len(ranked)}** recommendation(s) that satisfy the selected requirements.")

        for _, row in ranked.iterrows():
            st.markdown('<div class="tree-card">', unsafe_allow_html=True)
            c1, c2 = st.columns([1, 2.15], gap="large")

            with c1:
                image_url = row.get("image_url", "")
                if isinstance(image_url, str) and image_url.strip():
                    st.image(image_url, use_container_width=True)
                else:
                    st.markdown(
                        f'<div class="photo-placeholder">Photo ready<br>{row["common_name"]}</div>',
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f'<div class="match-pill">{int(row["match_pct"])}% match</div>',
                    unsafe_allow_html=True
                )
                st.markdown(
                    f'<div class="status-pill">{row["wiegands_status"]}</div>',
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(f"### {row['common_name']}")
                st.markdown(f"*{row['botanical_name']}*")
                st.markdown(
                    f'<div class="meta">{row["tree_type"]}</div>',
                    unsafe_allow_html=True
                )

                m1, m2, m3 = st.columns(3)
                m1.metric("Height", f"{int(row['height_min'])}–{int(row['height_max'])} ft")
                m2.metric("Width", f"{int(row['width_min'])}–{int(row['width_max'])} ft")
                m3.metric("Flowers", row["flowering"])

                st.write(row["description"])
                st.markdown(f"**Sun:** {row['sun_needs'].replace(';', ', ')}")

                st.markdown(
                    f'<div class="reason"><b>Why it matches:</b> {row["reasons"]}</div>',
                    unsafe_allow_html=True
                )

            st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.subheader("Your Criteria")
    criteria = []
    criteria.append(f"Tree type: {tree_type}")
    criteria.append(f"Maximum height: {max_height if max_height is not None else 'No limit'}")
    criteria.append(f"Maximum width: {max_width if max_width is not None else 'No limit'}")
    criteria.append(f"Flowering: {flowering}")
    criteria.append(f"Sun: {sun}")

    for item in criteria:
        st.write("• " + str(item))

    st.divider()
    st.markdown("#### Next POC upgrades")
    st.write("• Add real tree photographs")
    st.write("• Connect Wiegand's actual tree list")
    st.write("• Add growth rate, fall color, native status and soil/moisture preferences")
    st.write("• Add natural-language AI search")
    st.write("• Later connect recommendations to the landscape visualizer")

    st.divider()
    st.markdown("#### Light matching")
    st.caption(
        "The POC now treats sun exposure as overlapping ranges. "
        "For example, Partial Sun can match trees listed for Full Sun, "
        "Partial Sun, or Partial Shade."
    )

st.divider()
st.markdown(
    '<div class="small-note">'
    'POC architecture: tree data is stored separately in tree_database.csv. '
    'That lets Wiegand’s replace or expand the tree list without rebuilding the web interface.'
    '</div>',
    unsafe_allow_html=True
)
