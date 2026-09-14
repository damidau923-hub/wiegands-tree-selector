
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Wiegand's Tree Finder POC", page_icon="🌳", layout="wide")

@st.cache_data
def load_data():
    path = Path(__file__).with_name("tree_database.csv")
    return pd.read_csv(path)

df = load_data()

st.markdown("""
<style>
.block-container {max-width: 1250px; padding-top: 1.5rem;}
.tree-card {
    border: 1px solid #d9e2d5;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    background: #fbfdf9;
}
.match {
    font-size: 1.35rem;
    font-weight: 700;
}
.muted {color:#5f6b5b;}
.small {font-size:0.9rem;}
.placeholder {
    height: 180px; border-radius: 10px; background: #eef3ea;
    display:flex; align-items:center; justify-content:center;
    color:#6d7968; font-weight:600; margin-bottom:12px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌳 Wiegand's Michigan Tree Finder")
st.caption("Proof of concept — recommends Michigan-suitable trees from a curated starter database. Wiegand's availability is provisional until the full product database is connected.")

with st.sidebar:
    st.header("Tree characteristics")
    tree_types = ["Any"] + sorted(df["tree_type"].dropna().unique().tolist())
    tree_type = st.selectbox("Tree type", tree_types)

    height_range = st.slider("Mature height (ft)", 0, 100, (0, 100), step=5)
    width_range = st.slider("Mature width (ft)", 0, 100, (0, 100), step=5)
    flowering = st.selectbox("Flowering", ["Either", "Yes", "No"])
    sun = st.selectbox("Sun needs", ["Either", "Full Sun", "Partial Sun", "Partial Shade", "Shade"])
    wiegands_pref = st.checkbox("Prioritize Wiegand's priority candidates", value=True)
    max_results = st.slider("Number of recommendations", 3, 10, 5)

    st.divider()
    st.subheader("POC request helper")
    request = st.text_area(
        "Describe what you need",
        placeholder="Example: I need a flowering tree under 25 feet for partial shade."
    )
    if request:
        text = request.lower()
        hints = []
        if "flower" in text or "bloom" in text:
            hints.append("Flowering = Yes")
        if "shade" in text and "partial" in text:
            hints.append("Sun = Partial Shade")
        elif "shade" in text:
            hints.append("Sun = Shade")
        elif "full sun" in text or "sunny" in text:
            hints.append("Sun = Full Sun")
        if "small" in text:
            hints.append("Consider max height around 20–30 ft")
        if hints:
            st.info("POC interpretation: " + " • ".join(hints))
        else:
            st.caption("This helper is rule-based in the POC. A true AI parser can be connected later.")

def overlaps(tree_min, tree_max, user_min, user_max):
    return tree_max >= user_min and tree_min <= user_max

def score_row(row):
    possible = 0
    earned = 0
    reasons = []
    cautions = []

    # Tree type: only score it when user actually specifies one.
    if tree_type != "Any":
        possible += 40
        if row["tree_type"] == tree_type:
            earned += 40
            reasons.append(f"matches the requested {tree_type} type")
        else:
            cautions.append("different tree type")

    # Height
    if height_range != (0, 100):
        possible += 20
        if overlaps(row["height_min"], row["height_max"], *height_range):
            earned += 20
            reasons.append("mature height fits the requested range")
        else:
            cautions.append("height is outside the preferred range")

    # Width
    if width_range != (0, 100):
        possible += 20
        if overlaps(row["width_min"], row["width_max"], *width_range):
            earned += 20
            reasons.append("mature width fits the requested range")
        else:
            cautions.append("width is outside the preferred range")

    # Flowering
    if flowering != "Either":
        possible += 10
        if row["flowering"] == flowering:
            earned += 10
            reasons.append("flowering preference matches")
        else:
            cautions.append("flowering preference does not match")

    # Sun
    if sun != "Either":
        possible += 10
        options = [s.strip() for s in str(row["sun_needs"]).split(";")]
        if sun in options:
            earned += 10
            reasons.append(f"suited to {sun.lower()}")
        else:
            cautions.append("sun requirement does not match")

    # If the user left everything open, use a neutral base.
    if possible == 0:
        possible = 1
        earned = 1
        reasons.append("Michigan-suitable option from the starter database")

    pct = earned / possible * 100

    # Small Wiegand's tie-break bonus only, not part of the displayed match percentage.
    bonus = 0
    if wiegands_pref and "Priority candidate" in str(row["wiegands_status"]):
        bonus = 3

    return pd.Series({
        "match_pct": round(pct),
        "sort_score": pct + bonus,
        "reasons": "; ".join(reasons),
        "cautions": "; ".join(cautions)
    })

scored = df.copy()
extra = scored.apply(score_row, axis=1)
scored = pd.concat([scored, extra], axis=1)

# Hard-filter tree type when specified because this is a primary user choice.
if tree_type != "Any":
    scored = scored[scored["tree_type"] == tree_type]

scored = scored.sort_values(["sort_score", "common_name"], ascending=[False, True]).head(max_results)

st.subheader("Recommended trees")
st.write(f"Showing **{len(scored)}** best matches from the current POC database.")

if scored.empty:
    st.warning("No trees in the starter database match that tree type yet.")
else:
    for _, row in scored.iterrows():
        with st.container():
            st.markdown('<div class="tree-card">', unsafe_allow_html=True)
            left, right = st.columns([1, 2.2], gap="large")
            with left:
                if isinstance(row.get("image_url"), str) and row["image_url"].strip():
                    st.image(row["image_url"], use_container_width=True)
                else:
                    st.markdown('<div class="placeholder">Tree photo will appear here</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="match">{int(row["match_pct"])}% match</div>', unsafe_allow_html=True)
                st.caption(row["wiegands_status"])
            with right:
                st.markdown(f"### {row['common_name']}")
                st.markdown(f"*{row['botanical_name']}*")
                c1, c2, c3 = st.columns(3)
                c1.metric("Mature height", f"{int(row['height_min'])}–{int(row['height_max'])} ft")
                c2.metric("Mature width", f"{int(row['width_min'])}–{int(row['width_max'])} ft")
                c3.metric("Flowers", row["flowering"])
                st.write(row["description"])
                st.markdown(f"**Sun:** {row['sun_needs'].replace(';', ', ')}")
                if row["reasons"]:
                    st.success("Why it matches: " + row["reasons"])
                if row["cautions"] and row["match_pct"] < 100:
                    st.caption("Tradeoffs: " + row["cautions"])
            st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("POC design: the plant database is stored separately in tree_database.csv, so Wiegand's inventory and cultivar data can replace or expand it without rebuilding the user interface.")
