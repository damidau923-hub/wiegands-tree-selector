
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
    data = pd.read_csv(path)

    # Defensive schema handling:
    # if Streamlit/GitHub temporarily serves an older CSV, the app still runs.
    defaults = {
        "preferred_soil": "Not yet populated",
        "fall_color": "Not yet populated",
        "growth_rate": "Not yet populated",
        "native_status": "Not yet populated",
        "michigan_native": "Verify species",
        "moisture_notes": "Not yet populated",
        "info_source": "",
        "info_source_url": "",
        "image_source": "",
        "image_source_url": "",
        "photo_note": "",
        "photo_source_priority": "University/arboretum preferred",
        "photo_reference_type": "Targeted public reference",
        "photo_fallback_url": "",
        "image_url": "",
    }

    for column, default in defaults.items():
        if column not in data.columns:
            data[column] = default
        else:
            data[column] = data[column].fillna(default)

    return data

df = load_data()

def format_range(min_value, max_value, unit="ft"):
    """Display a complete mature-size range consistently."""
    try:
        min_num = float(min_value)
        max_num = float(max_value)
    except (TypeError, ValueError):
        return "Not available"

    if pd.isna(min_num) or pd.isna(max_num):
        return "Not available"

    def clean(v):
        return str(int(v)) if float(v).is_integer() else f"{v:g}"

    if min_num == max_num:
        return f"{clean(min_num)} {unit}"
    return f"{clean(min_num)} to {clean(max_num)} {unit}"

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

    result_count = st.slider("Results per section", 3, 10, 5)

    st.divider()
    st.caption(
        "POC note: Wiegand's availability is provisional until the actual "
        "Wiegand's product database is connected."
    )

# ---------- Match evaluation ----------
# Michigan suitability and an explicitly selected tree type define the search pool.
candidates = df[df["michigan_suitable"].astype(str).str.lower().eq("yes")].copy()
if tree_type != "Any":
    candidates = candidates[candidates["tree_type"] == tree_type]

SUN_COMPATIBILITY = {
    "Full Sun": {"Full Sun"},
    "Partial Sun": {"Full Sun", "Partial Sun", "Partial Shade"},
    "Partial Shade": {"Partial Sun", "Partial Shade", "Shade"},
    "Shade": {"Shade", "Partial Shade"},
}

def evaluate_match(row):
    checks = []
    misses = []
    matches = []

    if max_height is not None:
        ok = row["height_max"] <= max_height
        checks.append(ok)
        if ok:
            matches.append(f"mature height stays at or below {max_height} ft")
        else:
            misses.append(
                f"maximum mature height is {int(row['height_max'])} ft; your limit is {max_height} ft"
            )

    if max_width is not None:
        ok = row["width_max"] <= max_width
        checks.append(ok)
        if ok:
            matches.append(f"mature width stays at or below {max_width} ft")
        else:
            misses.append(
                f"maximum mature width is {int(row['width_max'])} ft; your limit is {max_width} ft"
            )

    if flowering != "Either":
        ok = str(row["flowering"]) == flowering
        checks.append(ok)
        if ok:
            matches.append(f"flowering preference matches ({flowering})")
        else:
            misses.append(
                f"flowering is {row['flowering']}; you requested {flowering}"
            )

    if sun != "Either":
        acceptable = SUN_COMPATIBILITY[sun]
        plant_sun = [s.strip() for s in str(row["sun_needs"]).split(";")]
        ok = any(option in acceptable for option in plant_sun)
        checks.append(ok)
        if ok:
            matches.append(f"fits the requested {sun.lower()} conditions")
        else:
            misses.append(
                f"listed light needs are {str(row['sun_needs']).replace(';', ', ')}; you requested {sun}"
            )

    # If the customer has not selected any optional criteria, every tree in the
    # chosen category is a Full Match.
    if not checks:
        status = "Full Match"
    elif all(checks):
        status = "Full Match"
    elif any(checks):
        status = "Partial Match"
    else:
        status = "No Match"

    matched_count = sum(bool(x) for x in checks)
    total_count = len(checks)

    # Ranking is separate from the match label.
    # Partial matches with more satisfied requirements and smaller size misses rank higher.
    penalty = 0.0
    if max_height is not None and row["height_max"] > max_height:
        penalty += (row["height_max"] - max_height) / max(max_height, 1)
    if max_width is not None and row["width_max"] > max_width:
        penalty += (row["width_max"] - max_width) / max(max_width, 1)

    wiegands_bonus = 1 if (
        prioritize_wiegands and "Priority candidate" in str(row["wiegands_status"])
    ) else 0

    return pd.Series({
        "match_status": status,
        "matched_count": matched_count,
        "criteria_count": total_count,
        "match_reasons": "; ".join(matches) if matches else "No selected requirement is met",
        "miss_reasons": "; ".join(misses),
        "rank_score": (matched_count * 100) + (wiegands_bonus * 5) - penalty,
    })

if not candidates.empty:
    evaluated = pd.concat([candidates, candidates.apply(evaluate_match, axis=1)], axis=1)
else:
    evaluated = candidates.copy()

if not evaluated.empty:
    full_matches = evaluated[evaluated["match_status"] == "Full Match"].copy()
    partial_matches = evaluated[evaluated["match_status"] == "Partial Match"].copy()

    full_matches = full_matches.sort_values(
        ["rank_score", "common_name"], ascending=[False, True]
    ).head(result_count)

    partial_matches = partial_matches.sort_values(
        ["rank_score", "common_name"], ascending=[False, True]
    ).head(result_count)
else:
    full_matches = evaluated
    partial_matches = evaluated

# ---------- Results ----------
left, right = st.columns([2.3, 1], gap="large")

def render_tree_card(row):
    st.markdown('<div class="tree-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.15], gap="large")

    with c1:
        image_url = row.get("image_url", "")
        if isinstance(image_url, str) and image_url.strip():
            st.image(image_url, use_container_width=True)
        else:
            st.markdown(
                f'<div class="photo-placeholder">Whole-tree photo pending<br>{row["common_name"]}</div>',
                unsafe_allow_html=True
            )

        if isinstance(row.get("image_source_url"), str) and row.get("image_source_url"):
            st.link_button("View public photo source", row["image_source_url"], use_container_width=True)

        if row["match_status"] == "Full Match":
            st.markdown(
                '<div class="match-pill">FULL MATCH</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="status-pill"><b>PARTIAL MATCH</b></div>',
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
        with m1:
            st.markdown("**Mature Height**")
            st.write(format_range(row["height_min"], row["height_max"]))
        with m2:
            st.markdown("**Mature Width**")
            st.write(format_range(row["width_min"], row["width_max"]))
        with m3:
            st.markdown("**Flowers**")
            st.write(row["flowering"])

        st.write(row["description"])
        st.markdown(f"**Sun:** {row['sun_needs'].replace(';', ', ')}")

        d1, d2 = st.columns(2)
        with d1:
            st.markdown(f"**Preferred soil:** {row['preferred_soil']}")
            st.markdown(f"**Growth rate:** {row['growth_rate']}")
            st.markdown(f"**Michigan Native:** {row['michigan_native']}")
        with d2:
            st.markdown(f"**Fall color:** {row['fall_color']}")
            st.markdown(f"**Moisture:** {row['moisture_notes']}")

        if row["match_status"] == "Full Match":
            text = row["match_reasons"] or "Meets all selected requirements."
            st.markdown(
                f'<div class="reason"><b>Why it is a Full Match:</b> {text}</div>',
                unsafe_allow_html=True
            )
        else:
            if row["match_reasons"]:
                st.markdown(
                    f'<div class="reason"><b>What matches:</b> {row["match_reasons"]}</div>',
                    unsafe_allow_html=True
                )
            st.markdown(
                f'<div class="warning"><b>What does not match:</b> {row["miss_reasons"]}</div>',
                unsafe_allow_html=True
            )

        source_bits = []
        if isinstance(row.get("info_source_url"), str) and row.get("info_source_url"):
            source_bits.append(f"[Horticultural source]({row['info_source_url']})")
        if isinstance(row.get("image_source_url"), str) and row.get("image_source_url"):
            source_bits.append(f"[Photo source]({row['image_source_url']})")
        if source_bits:
            st.caption(" • ".join(source_bits))
        if isinstance(row.get("photo_note"), str) and row.get("photo_note"):
            st.caption(row["photo_note"])
        if isinstance(row.get("photo_reference_type"), str) and row.get("photo_reference_type"):
            st.caption(f"Photo reference: {row['photo_reference_type']}")

    st.markdown('</div>', unsafe_allow_html=True)

with left:
    st.subheader("Recommended Trees")

    if candidates.empty:
        st.warning("No Michigan-suitable trees are available in the selected tree category.")
    else:
        st.markdown("### Full Matches")
        if full_matches.empty:
            st.info("No trees meet every selected requirement.")
        else:
            st.write(
                f"These **{len(full_matches)}** tree(s) meet all selected requirements."
            )
            for _, row in full_matches.iterrows():
                render_tree_card(row)

        st.markdown("### Other Possibilities — Partial Matches")
        if partial_matches.empty:
            st.caption("No partial matches to show.")
        else:
            st.write(
                "These trees meet **some, but not all**, of the selected requirements. "
                "Each card explains exactly what falls outside your criteria."
            )
            for _, row in partial_matches.iterrows():
                render_tree_card(row)

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
    st.markdown("#### Photo policy")
    st.caption(
        "POC photo sourcing now prioritizes university and arboretum collections, especially "
        "NC State Plant Toolbox and JC Raulston Arboretum. Exact-cultivar and whole-tree images "
        "are preferred; Wikimedia Commons is retained only as a fallback. Wiegand's own approved "
        "photography can replace these references later."
    )

    st.divider()
    st.markdown("#### Michigan Native")
    st.caption(
        "Yes means the underlying tree species is originally native to Michigan. "
        "Cultivars of a Michigan-native species retain Yes; hybrids or entries whose species varies are labeled separately."
    )

    st.divider()
    st.markdown("#### Match logic")
    st.caption(
        "Full Match means every selected requirement is met. Partial Match means "
        "some selected requirements are met and the card identifies what does not match."
    )

    st.divider()
    st.markdown("#### Next POC upgrades")
    st.write("• Expand photo coverage to every exact cultivar")
    st.write("• Connect Wiegand's actual tree list")
    st.write("• Verify all cultivar-specific horticultural attributes against final Wiegand's assortment")
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
