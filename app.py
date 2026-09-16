
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Acme Nursery Tree Sales Assistant",
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
        "size_basis": "Starter range — cultivar verification pending",
        "size_confidence": "Needs verification",
        "size_source_name": "",
        "size_source_url": "",
        "image_url": "",
        "form": "Tree Form",
        "flower_color": "To verify",
        "bloom_season": "To verify",
    }

    for column, default in defaults.items():
        if column not in data.columns:
            data[column] = default
        else:
            data[column] = data[column].fillna(default)

    return data


def sales_group_for_row(row):
    name = str(row.get("common_name", ""))

    if "Hydrangea" in name and "Standard" in name:
        return "Hydrangea Tree on Standard"
    if "Lilac on Standard" in name or "Korean Lilac on Standard" in name:
        return "Lilac Tree on Standard"
    if "Japanese Tree Lilac" in name or "Ivory Silk" in name:
        return "Japanese Tree Lilac"
    if "Rose of Sharon" in name:
        return "Rose of Sharon Tree Form"
    if "Japanese Maple" in name:
        return "Japanese Maple"
    if "Serviceberry" in name:
        return "Serviceberry"
    if "Redbud" in name:
        return "Redbud"
    if "Dogwood" in name:
        return "Dogwood"
    if "Crabapple" in name:
        return "Crabapple"
    if "Birch" in name:
        return "Birch"
    if "Beech" in name:
        return "Beech"
    if "Oak" in name:
        return "Oak"
    if "Maple" in name:
        return "Maple"
    if "Ginkgo" in name:
        return "Ginkgo"
    return "Other"

df = load_data()
df["sales_group"] = df.apply(sales_group_for_row, axis=1)

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


GROUP_OVERVIEWS = {
    "Hydrangea Tree on Standard": {
        "label": "Hydrangea Tree on Standard",
        "summary": "Small flowering tree-form hydrangeas with large summer blooms.",
        "why": "Good for compact spaces where the customer wants strong flower impact."
    },
    "Lilac Tree on Standard": {
        "label": "Lilac Tree on Standard",
        "summary": "Shrub lilacs trained or grafted onto a single trunk, giving the appearance of a small ornamental tree.",
        "why": "Good when a customer wants familiar lilac flowers and fragrance in tree form."
    },
    "Japanese Tree Lilac": {
        "label": "Japanese Tree Lilac",
        "summary": "Naturally tree-form lilacs with creamy summer flowers and a true small-tree structure.",
        "why": "Useful when the customer wants a flowering small tree rather than a shrub trained on a standard."
    },
    "Rose of Sharon Tree Form": {
        "label": "Rose of Sharon on Standard",
        "summary": "A narrow ornamental tree form with a long summer flowering period.",
        "why": "Useful where late-season flowers and a relatively compact footprint are important."
    },
    "Japanese Maple": {
        "label": "Japanese Maple",
        "summary": "Small ornamental maples valued for foliage color, graceful form, and specimen character.",
        "why": "Best for customers who value foliage and structure more than flowers."
    },
    "Serviceberry": {
        "label": "Serviceberry",
        "summary": "Small ornamental trees with spring flowers, berries, fall color, and wildlife value.",
        "why": "A strong all-season choice for customers who want several seasons of interest."
    },
    "Redbud": {
        "label": "Redbud",
        "summary": "Small spring-flowering trees with pink to purple flowers before leaf-out.",
        "why": "Excellent where spring flower impact and modest mature size are priorities."
    },
    "Dogwood": {
        "label": "Dogwood",
        "summary": "Refined ornamental trees known for flowers, layered branching, and seasonal interest.",
        "why": "Useful as a focal-point flowering tree."
    },
    "Crabapple": {
        "label": "Flowering Crabapple",
        "summary": "Compact ornamental trees with abundant spring flowers and decorative fruit.",
        "why": "Good for customers who want a classic flowering ornamental."
    },
    "Birch": {
        "label": "Birch",
        "summary": "Trees valued for distinctive bark, graceful form, and light canopy character.",
        "why": "Useful when bark and overall tree character are priorities."
    },
    "Beech": {
        "label": "Beech",
        "summary": "Long-lived specimen or shade trees with dense canopies and strong foliage character.",
        "why": "Best where there is enough room for a substantial long-term tree."
    },
    "Oak": {
        "label": "Oak",
        "summary": "Large, durable shade trees with strong structure and long life spans.",
        "why": "Best for customers with room for a major canopy tree."
    },
    "Maple": {
        "label": "Maple",
        "summary": "Shade and ornamental trees commonly selected for fall color, form, and dependable landscape performance.",
        "why": "Useful where shade and fall color are important."
    },
    "Ginkgo": {
        "label": "Ginkgo",
        "summary": "Distinctive trees with fan-shaped leaves and bright yellow fall color.",
        "why": "A durable choice when unique foliage and fall color are desirable."
    },
    "Other": {
        "label": "Other Recommended Trees",
        "summary": "Additional tree choices that fit or nearly fit the customer's requirements.",
        "why": "Worth reviewing when they satisfy the site and size requirements."
    },
}


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

<style>
button, [data-testid="stBaseButton-secondary"], [data-testid="stBaseButton-primary"] {
    min-height: 50px !important;
    font-size: 1rem !important;
}
[data-testid="stSidebar"] label {
    font-size: 1rem !important;
    font-weight: 650 !important;
}
.tree-card { padding: 20px !important; }
.tree-card img { border-radius: 14px; }
.match-pill { font-size: 1rem !important; padding: 8px 12px !important; }
.status-pill { font-size: .9rem !important; padding: 7px 10px !important; }
@media (max-width: 1100px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .hero-title { font-size: 1.8rem; }
}
</style>

""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero">
  <div class="hero-title">Acme Nursery Tree Sales Assistant</div>
  <div class="hero-sub">
    Guide a customer from site criteria to recommended tree types, then drill down to the actual cultivars.
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

    flowering = st.selectbox("Flowering tree?", ["Either", "Yes", "No"])
    sun = st.selectbox(
        "Sun needs",
        ["Any", "Full Sun", "Partial Sun", "Partial Shade", "Shade"]
    )

    prioritize_wiegands = st.checkbox(
        "Prioritize Acme Nursery priority candidates",
        value=True
    )

    result_count = st.slider("Results per section", 3, 10, 5)

    if "search_started" not in st.session_state:
        st.session_state.search_started = False
    if "review_recommendations" not in st.session_state:
        st.session_state.review_recommendations = False
    if "comparison_started" not in st.session_state:
        st.session_state.comparison_started = False

    if not st.session_state.search_started:
        if st.button("Find Trees", type="primary", use_container_width=True):
            st.session_state.search_started = True
            st.session_state.review_recommendations = False
            st.session_state.comparison_started = False
            st.rerun()
    else:
        # Disabled buttons render gray and confirm the search has already been run.
        st.button("✓ Trees Found", disabled=True, use_container_width=True)

    find_trees = st.session_state.search_started

    if find_trees and st.button("Start New Search", use_container_width=True):
        st.session_state.search_started = False
        st.session_state.review_recommendations = False
        st.session_state.comparison_started = False
        st.rerun()

    st.divider()
    st.caption(
        "Sales POC: product availability is provisional until Acme Nursery live inventory is connected."
    )

# ---------- Match evaluation ----------
# Michigan suitability, an explicitly selected tree type, and an explicit
# flowering choice define the hard search pool.
candidates = df[df["michigan_suitable"].astype(str).str.lower().eq("yes")].copy()

if tree_type != "Any":
    candidates = candidates[candidates["tree_type"] == tree_type]

# Flowering is a hard customer requirement when selected.
# This prevents a non-flowering tree from appearing as a Partial Match
# when the customer specifically requests a flowering tree.
if flowering != "Either":
    candidates = candidates[
        candidates["flowering"].astype(str).str.strip().str.lower()
        == flowering.strip().lower()
    ]

SUN_MATCH = {
    "Full Sun": {
        "preferred": {"Full Sun"},
        "tolerated": {"Partial Sun"},
    },
    "Partial Sun": {
        "preferred": {"Partial Sun"},
        "tolerated": {"Full Sun", "Partial Shade"},
    },
    "Partial Shade": {
        "preferred": {"Partial Shade"},
        "tolerated": {"Partial Sun", "Shade"},
    },
    "Shade": {
        "preferred": {"Shade"},
        "tolerated": {"Partial Shade"},
    },
}

def evaluate_match(row):
    checks = []
    misses = []
    matches = []
    borderlines = []

    if max_height is not None:
        if row["height_max"] <= max_height:
            ok = True
            matches.append(
                f"expected mature height {format_range(row['height_min'], row['height_max'])} fits the {max_height} ft limit"
            )
        elif row["height_min"] <= max_height < row["height_max"]:
            ok = False
            borderlines.append(
                f"height may fit: expected mature height is {format_range(row['height_min'], row['height_max'])}; "
                f"customer maximum is {max_height} ft"
            )
        else:
            ok = False
            misses.append(
                f"expected mature height starts at {int(row['height_min'])} ft, above the {max_height} ft limit"
            )
        checks.append(ok)

    if max_width is not None:
        if row["width_max"] <= max_width:
            ok = True
            matches.append(
                f"expected mature width {format_range(row['width_min'], row['width_max'])} fits the {max_width} ft limit"
            )
        elif row["width_min"] <= max_width < row["width_max"]:
            ok = False
            borderlines.append(
                f"width may fit: expected mature width is {format_range(row['width_min'], row['width_max'])}; "
                f"customer maximum is {max_width} ft"
            )
        else:
            ok = False
            misses.append(
                f"expected mature width starts at {int(row['width_min'])} ft, above the {max_width} ft limit"
            )
        checks.append(ok)

    if flowering != "Either":
        # Flowering has already been enforced as a hard search-pool requirement.
        ok = True
        checks.append(ok)
        matches.append(f"flowering requirement matches ({flowering})")

    if sun != "Any":
        tree_sun = {s.strip() for s in str(row["sun_needs"]).split(";") if s.strip()}
        preferred = SUN_MATCH.get(sun, {}).get("preferred", set())
        tolerated = SUN_MATCH.get(sun, {}).get("tolerated", set())

        if tree_sun & preferred:
            ok = True
            matches.append(f"preferred light match ({sun})")
        elif tree_sun & tolerated:
            ok = False
            borderlines.append(
                f"light is tolerated rather than preferred for this site ({sun}); "
                "growth, flowering, or fall color may be reduced"
            )
        else:
            ok = False
            misses.append(f"light requirement does not fit the selected site ({sun})")
        checks.append(ok)

    if not checks:
        status = "Full Match"
    elif all(checks) and not borderlines and not misses:
        status = "Full Match"
    elif any(checks) or borderlines:
        status = "Partial Match"
    else:
        status = "No Match"

    matched_count = sum(bool(x) for x in checks)
    total_count = len(checks)

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
        "match_reasons": "; ".join(matches) if matches else "",
        "borderline_reasons": "; ".join(borderlines),
        "miss_reasons": "; ".join(misses),
        "rank_score": (matched_count * 100) + (len(borderlines) * 50) + (wiegands_bonus * 5) - penalty,
    })

if not candidates.empty:
    evaluated = pd.concat([candidates, candidates.apply(evaluate_match, axis=1)], axis=1)
else:
    # Preserve the result schema even when no candidates survive the initial filters.
    evaluated = candidates.copy()
    for col in [
        "match_status", "matched_count", "criteria_count", "match_reasons",
        "borderline_reasons", "miss_reasons", "rank_score"
    ]:
        if col not in evaluated.columns:
            evaluated[col] = pd.Series(dtype="object")

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
comparison_focus = st.session_state.get("comparison_started", False)
if comparison_focus:
    st.markdown(
        """<style>
        [data-testid="stAppViewContainer"] .main .block-container {
            max-width: 100%;
            padding-left: 1.25rem;
            padding-right: 1.25rem;
        }
        </style>""",
        unsafe_allow_html=True,
    )
if comparison_focus:
    # Focused comparison view: give the working table essentially the whole page.
    left, right = st.columns([20, 0.01], gap="small")
else:
    left, right = st.columns([2.6, 1], gap="large")

def render_tree_card(row):
    st.markdown('<div class="tree-card">', unsafe_allow_html=True)
    c1, c2 = st.columns([1.25, 1.75], gap="large")

    with c1:
        image_url = row.get("image_url", "")
        if isinstance(image_url, str) and image_url.strip():
            st.image(image_url, use_container_width=True)
        else:
            st.markdown(
                f'<div class="photo-placeholder">Whole-tree photo pending<br>{row["common_name"]}</div>',
                unsafe_allow_html=True
            )

        if row["match_status"] == "Full Match":
            st.markdown('<div class="match-pill">FULL MATCH</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-pill"><b>PARTIAL MATCH</b></div>', unsafe_allow_html=True)

        st.markdown(f'<div class="status-pill">{row["wiegands_status"]}</div>', unsafe_allow_html=True)

    with c2:
        st.markdown(f"### {row['common_name']}")
        st.markdown(f"*{row['botanical_name']}*")
        st.markdown(f'<div class="meta">{row["tree_type"]}</div>', unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown("**Expected Mature Height**")
            st.write(format_range(row["height_min"], row["height_max"]))
        with m2:
            st.markdown("**Expected Mature Width**")
            st.write(format_range(row["width_min"], row["width_max"]))
        with m3:
            st.markdown("**Flowers**")
            st.write(row["flowering"])

        if row.get("size_confidence") == "Verified":
            st.caption(f"Size basis: {row.get('size_basis', 'Michigan/regional reference')}")
        else:
            st.caption("Size basis: starter estimate — exact cultivar/Michigan verification pending")

        st.write(row["description"])
        st.markdown(f"**Flower Color:** {row['flower_color']}")
        st.markdown(f"**Bloom Season:** {row['bloom_season']}")
        st.markdown(f"**Sun:** {row['sun_needs'].replace(';', ', ')}")
        st.markdown(f"**Form:** {row['form']}")

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
            if row.get("match_reasons", ""):
                st.markdown(
                    f'<div class="reason"><b>What fits:</b> {row["match_reasons"]}</div>',
                    unsafe_allow_html=True
                )
            if row.get("borderline_reasons", ""):
                st.markdown(
                    f'<div class="warning"><b>May fit:</b> {row["borderline_reasons"]}</div>',
                    unsafe_allow_html=True
                )
            if row.get("miss_reasons", ""):
                st.markdown(
                    f'<div class="warning"><b>Exceeds / does not match:</b> {row["miss_reasons"]}</div>',
                    unsafe_allow_html=True
                )

    st.markdown('</div>', unsafe_allow_html=True)

def group_summary_table(matches_df):
    if matches_df.empty:
        return pd.DataFrame(columns=["sales_group", "full_count", "partial_count", "best_rank"])
    g = matches_df.groupby("sales_group").agg(
        full_count=("match_status", lambda s: int((s == "Full Match").sum())),
        partial_count=("match_status", lambda s: int((s == "Partial Match").sum())),
        best_rank=("rank_score", "max")
    ).reset_index()
    g["total"] = g["full_count"] + g["partial_count"]
    # Always place the catch-all Other Recommended Trees group last.
    g["other_last"] = g["sales_group"].eq("Other")
    return g.sort_values(
        ["other_last", "full_count", "best_rank", "total"],
        ascending=[True, False, False, False]
    ).drop(columns=["other_last"])

with left:
    st.subheader("1. Broad Choices That Fit the Customer")

    if not find_trees:
        st.info("Choose the customer's criteria, then tap **Find Trees**.")
    else:
        visible_matches = evaluated[evaluated["match_status"].isin(["Full Match", "Partial Match"])].copy()

        if visible_matches.empty:
            st.warning("No tree types meet or partially meet the selected criteria. Try adjusting one of the customer requirements.")
        else:
            group_table = group_summary_table(visible_matches)
            available_groups = group_table["sales_group"].tolist()

            st.write(
                "Start with the types of trees that could work. Review the overview with the customer, "
                "then select one or more groups to see the actual cultivars."
            )

            if not st.session_state.review_recommendations:
                if st.button("Review Recommended Trees", type="primary", use_container_width=True):
                    st.session_state.review_recommendations = True
                    st.rerun()
                st.stop()

            cols = st.columns(2)
            for pos, (_, grow) in enumerate(group_table.iterrows()):
                group = grow["sales_group"]
                meta = GROUP_OVERVIEWS.get(group, GROUP_OVERVIEWS["Other"])
                group_rows = visible_matches[visible_matches["sales_group"] == group]
                hmin = int(group_rows["height_min"].min())
                hmax = int(group_rows["height_max"].max())
                wmin = int(group_rows["width_min"].min())
                wmax = int(group_rows["width_max"].max())

                with cols[pos % 2]:
                    st.markdown('<div class="tree-card">', unsafe_allow_html=True)
                    st.markdown(f"### {meta['label']}")
                    st.write(meta["summary"])
                    st.caption(meta["why"])
                    st.markdown(f"**Typical range in current POC:** {hmin}–{hmax} ft tall · {wmin}–{wmax} ft wide")
                    st.markdown(f"**Matches:** {int(grow['full_count'])} full · {int(grow['partial_count'])} partial")
                    st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("2. Choose Tree Types to Review")
            st.caption("You can select multiple tree types.")
            selected_groups = st.multiselect(
                "Which types does the customer want to see?",
                options=available_groups,
                default=[],
                placeholder="Example: Serviceberry, Hydrangea Tree on Standard"
            )

            current_group_selection = tuple(selected_groups)
            previous_group_selection = st.session_state.get("previous_group_selection")
            if previous_group_selection is not None and previous_group_selection != current_group_selection:
                st.session_state.comparison_started = False
            st.session_state.previous_group_selection = current_group_selection

            if not selected_groups:
                st.session_state.comparison_started = False
                st.info("Select one or more tree types above, then tap **Continue to Quick Comparison**.")
            elif not st.session_state.comparison_started:
                if st.button("Continue to Quick Comparison", type="primary", use_container_width=True):
                    st.session_state.comparison_started = True
                    st.rerun()
            else:
                if comparison_focus:
                    if st.button("← Back to Recommendations", use_container_width=True):
                        st.session_state.comparison_started = False
                        st.rerun()
                    st.markdown("## Quick Comparison — Focus View")
                    st.caption("Select the cultivars the customer wants to review in detail.")

                selected_rows = visible_matches[visible_matches["sales_group"].isin(selected_groups)].copy()
                selected_rows["status_order"] = selected_rows["match_status"].map({"Full Match": 0, "Partial Match": 1})
                selected_rows = selected_rows.sort_values(
                    ["status_order", "sales_group", "rank_score"],
                    ascending=[True, True, False]
                )

                if not comparison_focus:
                    st.subheader("3. Quick Comparison")
                    st.caption(
                        "Compare the matching cultivars at a glance. Full Matches appear first, followed by Partial Matches."
                    )

                comparison = selected_rows.copy()
                comparison["Select"] = False
                comparison["Tree / Cultivar"] = comparison["common_name"]
                comparison["Match"] = comparison["match_status"]
                comparison["Height"] = comparison.apply(
                    lambda r: format_range(r["height_min"], r["height_max"]), axis=1
                )
                comparison["Width"] = comparison.apply(
                    lambda r: format_range(r["width_min"], r["width_max"]), axis=1
                )
                comparison["Flowers"] = comparison["flowering"].apply(
                    lambda x: "Yes" if str(x).strip().lower() == "yes" else "No"
                )
                comparison["Flower Color"] = comparison["flower_color"].fillna("To verify")
                comparison["Bloom Season"] = comparison["bloom_season"].fillna("To verify")
                comparison["Fall Color"] = comparison["fall_color"].fillna("Not specified")
                comparison["Sun"] = comparison["sun_needs"].fillna("Not specified").str.replace(";", ", ", regex=False)
                comparison["Form"] = comparison["form"].fillna("Tree Form")

                comparison = comparison[
                    ["Select", "id", "Tree / Cultivar", "Match", "Height", "Width", "Flowers", "Flower Color", "Bloom Season", "Fall Color", "Sun", "Form"]
                ]

                edited_comparison = st.data_editor(
                    comparison,
                    hide_index=True,
                    use_container_width=True,
                    disabled=["id", "Tree / Cultivar", "Match", "Height", "Width", "Flowers", "Flower Color", "Bloom Season", "Fall Color", "Sun", "Form"],
                    column_config={
                        "Select": st.column_config.CheckboxColumn(
                            "Show Details",
                            help="Check the cultivars you want to review in detail below.",
                            default=False,
                            width="small",
                        ),
                        "id": None,
                        "Tree / Cultivar": st.column_config.TextColumn("Tree / Cultivar", width="large"),
                        "Match": st.column_config.TextColumn("Match", width="medium"),
                        "Height": st.column_config.TextColumn("Mature Height", width="medium"),
                        "Width": st.column_config.TextColumn("Mature Width", width="medium"),
                        "Flowers": st.column_config.TextColumn("Flowers", width="small"),
                        "Flower Color": st.column_config.TextColumn("Flower Color", width="medium"),
                        "Bloom Season": st.column_config.TextColumn("Bloom Season", width="medium"),
                        "Fall Color": st.column_config.TextColumn("Fall Color", width="medium"),
                        "Sun": st.column_config.TextColumn("Sun", width="medium"),
                        "Form": st.column_config.TextColumn("Form", width="medium"),
                    },
                    key="quick_comparison_editor_" + "_".join(
                        str(g).lower().replace(" ", "_") for g in sorted(selected_groups)
                    ),
                )

                selected_ids = edited_comparison.loc[
                    edited_comparison["Select"] == True, "id"
                ].tolist()

                if not selected_ids:
                    st.info("Check one or more cultivars under **Show Details** to display detailed cards.")
                else:
                    st.subheader("4. Review Selected Cultivars")
                    detail_rows = selected_rows[selected_rows["id"].isin(selected_ids)].copy()

                    for group in selected_groups:
                        group_rows = detail_rows[detail_rows["sales_group"] == group]
                        if group_rows.empty:
                            continue

                        meta = GROUP_OVERVIEWS.get(group, GROUP_OVERVIEWS["Other"])
                        st.markdown(f"## {meta['label']}")
                        st.caption(meta["summary"])

                        for _, row in group_rows.iterrows():
                            render_tree_card(row)

if not comparison_focus:
    with right:
        st.subheader("Customer Criteria")
        criteria = [
            f"Tree type: {tree_type}",
            f"Maximum height: {max_height if max_height is not None else 'No limit'}",
            f"Maximum width: {max_width if max_width is not None else 'No limit'}",
            f"Flowering: {flowering}",
            f"Sun: {sun}",
        ]
        for item in criteria:
            st.write("• " + str(item))

        st.divider()
        st.markdown("#### Sales flow")
        st.caption("1) Enter criteria. 2) Review broad choices. 3) Select the types the customer likes. 4) Compare cultivars and check the ones to review. 5) Review only the selected detailed cultivar cards.")

        st.divider()
        st.markdown("#### Mature size")
        st.caption("Verified Michigan/regional size values are used when available. Other entries remain starter estimates pending cultivar verification.")

        st.divider()
        st.markdown("#### Match logic")
        st.caption(
            "Full Match means every selected requirement fully fits. "
            "For height and width, May Fit means the lower end of the expected mature range is within the customer's limit "
            "but the upper end exceeds it. For sun, preferred light can be a Full Match; tolerated light remains "
            "visible as a Partial Match with an explanation."
        )

        with st.expander("POC development notes"):
            st.write("• Connect live nursery cultivar/product inventory")
            st.write("• Add approved nursery or supplier photography")
            st.write("• Let AI summarize why each tree type fits the customer's request")
            st.write("• Pass selected cultivars into the landscape visualizer")

    st.divider()
    st.markdown(
        '<div class="small-note">'
        'POC architecture: tree data is stored separately in tree_database.csv. '
        'That lets Acme Nursery replace or expand the tree list without rebuilding the web interface.'
        '</div>',
        unsafe_allow_html=True
    )
