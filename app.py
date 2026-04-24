import copy
import random
import streamlit as st

st.set_page_config(page_title="STRATIOS", layout="wide")

# =========================================================
# START SCREEN
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.title("STRATIOS |  STRATEGY ENGINE PROTOTYPE")

    if st.button("Begin"):
        st.session_state.started = True
        st.session_state.step = "shock"
        st.session_state.shock_applied = False
        st.rerun()

    st.stop()

# =========================================================
# CONTEXT
# =========================================================

if st.session_state.step == "shock":
    st.markdown(""" 
    You are the CEO of a global EV manufacturer, dependant on a stable lithium supply. 
    Recent armed conflict in your supply region has led to insurgents seizing key mining sites, and cutting transport routes to export ports. 
    Your firm experiences a shock.
    """)

# =========================================================
# BASE INPUTS
# =========================================================

base_inputs = {
    "base_production": 100000,
    "base_price": 40000,
    "base_unit_cost": 30000,
    "supply_reduction": 0.35,
    "input_price_increase": 0.45,
    "dependency": 0.65,
    "flexibility": 0.40
}

# =========================================================
# FUNCTIONS
# =========================================================

def shock_engine(inputs):
    shock = random.uniform(0.85, 1.15)

    new_inputs = copy.deepcopy(inputs)
    new_inputs["supply_reduction"] *= shock
    new_inputs["input_price_increase"] *= shock

    return new_inputs, shock


def model(inputs):
    production = inputs["base_production"] * (
        1 - inputs["supply_reduction"] * inputs["dependency"] * (1 - inputs["flexibility"])
    )

    cost = inputs["base_unit_cost"] * (
        1 + inputs["input_price_increase"] * inputs["dependency"]
    )

    return production, cost


def calc(prod, price, cost):
    revenue = prod * price
    profit = revenue - (prod * cost)
    return revenue, profit


def pct(new, old):
    return ((new - old) / old) * 100


def insights(choice, stage):
    st.markdown("---")
    st.subheader(f"INSIGHTS")

    if choice == "Raise prices by 10%":
        st.write(
            "You chose to leverage pricing power as a short-term buffer against input cost shocks.\n\n"
            "**Pros:**\n"
            "- Immediately improves revenue per unit and protects headline margins\n"
            "- Signals premium positioning and brand strength in a constrained market\n"
            "- Helps offset short-term supply-driven cost inflation\n\n"
            "**Cons:**\n"
            "- Increases demand elasticity risk, particularly in price-sensitive EV segments\n"
            "- Potential acceleration of customer switching to competitors or substitutes\n"
            "- May weaken long-term market share if competitors maintain stable pricing"
        )

    elif choice == "Keep prices stable":
        st.write(
            "You chose to protect volume stability over margin expansion, and absorb cost shocks internally.\n\n"
            "**Pros:**\n"
            "- Preserves market share and customer demand continuity\n"
            "- Maintains competitive positioning in a price-sensitive environment\n"
            "- Reduces risk of demand contraction in the short term\n\n"
            "**Cons:**\n"
            "- Direct compression of margins under higher input costs\n"
            "- Profitability becomes more sensitive to further supply shocks\n"
            "- Limits ability to pass through inflationary pressures to customers"
        )

    elif choice == "Prioritise higher-margin models":
        st.write(
            "You chose to actively rebalance the firm's portfolio toward higher-margin output, prioritising profitability over volume.\n\n"
            "**Pros:**\n"
            "- Improves unit economics and overall margin structure\n"
            "- Enhances capital efficiency and returns on production\n"
            "- Strengthens financial resilience in constrained environments\n\n"
            "**Cons:**\n"
            "- Reduced production volume limits economies of scale\n"
            "- Weakens competitive positioning in mass-market segments\n"
            "- Higher reliance on niche demand increases volatility exposure"
        )

    elif choice == "Diversify supply chain":
        st.write(
            "You chose to reduce structural dependency on a single supply base through diversification of inputs.\n\n"
            "**Pros:**\n"
            "- Reduces exposure to geopolitical and supply-side shocks\n"
            "- Improves long-term supply chain resilience and optionality\n"
            "- Strengthens negotiating power with upstream suppliers\n\n"
            "**Cons:**\n"
            "- Higher short-term procurement and transition costs\n"
            "- Potential inefficiencies from fragmented supply networks\n"
            "- Longer implementation timelines before benefits fully materialise"
        )

    elif choice == "Integrate vertically by investing in mining and refining":
        st.write(
            "You chose to integrate and internalise key parts of the supply chain and reduce external dependency.\n\n"
            "**Pros:**\n"
            "- Greater control over critical inputs and production stability\n"
            "- Improved margin capture by eliminating intermediary costs\n"
            "- Enhanced strategic autonomy in volatile markets\n\n"
            "**Cons:**\n"
            "- Significant increase in fixed capital investment requirements\n"
            "- Reduced operational flexibility under demand fluctuations\n"
            "- Higher exposure if internalised assets become inefficient"
        )

    elif choice == "Redesign EV to be less reliant on lithium":
        st.write(
            "You chose to structurally reduce lithium intensity through product redesign.\n\n"
            "**Pros:**\n"
            "- Reduces long-term dependency on constrained inputs\n"
            "- Improves strategic resilience against future shocks\n"
            "- Enhances technological differentiation\n\n"
            "**Cons:**\n"
            "- Higher short-term R&D and retooling costs\n"
            "- Temporary production inefficiencies during transition\n"
            "- Execution risk if redesign underperforms"
        )

# =========================================================
# BASELINE (ONLY SHOW ON SHOCK SCREEN)
# =========================================================

base_prod = base_inputs["base_production"]
base_price = base_inputs["base_price"]
base_cost = base_inputs["base_unit_cost"]

base_rev, base_profit = calc(base_prod, base_price, base_cost)

if st.session_state.step == "shock":
    st.subheader("BASELINE")
    st.write(f"Production: {base_prod:,}")
    st.write(f"Revenue: £{base_rev:,}")
    st.write(f"Profit: £{base_profit:,}")

# =========================================================
# STATE INIT
# =========================================================

if "inputs" not in st.session_state:
    st.session_state.inputs = copy.deepcopy(base_inputs)
    st.session_state.step = "shock"
    st.session_state.post_shock_results = None
    st.session_state.shock_applied = False

# =========================================================
# STEP 1 — SHOCK
# =========================================================

if st.session_state.step == "shock":

    if st.button("Apply Randomised Shock"):
        st.session_state.inputs, st.session_state.shock = shock_engine(st.session_state.inputs)
        st.session_state.shock_applied = True

    if st.session_state.shock_applied:

        prod_s, cost_s = model(st.session_state.inputs)
        rev_s, prof_s = calc(prod_s, base_price, cost_s)

        st.session_state.post_shock_results = (prod_s, rev_s, prof_s)

        st.subheader("POST-SHOCK")

        st.write(f"Production: {round(prod_s):,} ({round(pct(prod_s, base_prod),2)}%)")
        st.write(f"Revenue: £{round(rev_s):,} ({round(pct(rev_s, base_rev),2)}%)")
        st.write(f"Profit: £{round(prof_s):,} ({round(pct(prof_s, base_profit),2)}%)")

    if st.session_state.shock_applied:
        if st.button("Continue"):
            st.session_state.step = "decision_1"
            st.rerun()

# =========================================================
# DECISION 1
# =========================================================

if st.session_state.step == "decision_1":

    st.markdown("---")
    st.subheader("DECISION 1 — IMMEDIATE COMMERCIAL RESPONSE")

    d1 = st.radio(
        "Choose strategy:",
        ["Raise prices by 10%", "Keep prices stable", "Prioritise higher-margin models"]
    )

    if st.button("Continue"):

        if d1 == "Raise prices by 10%":
            base_price *= 1.10
            base_prod *= 0.98

        elif d1 == "Keep prices stable":
            base_cost *= 1.02

        elif d1 == "Prioritise higher-margin models":
            base_price *= 1.05
            base_prod *= 0.85
            base_cost *= 0.95

        st.session_state.d1 = d1
        st.session_state.inputs["base_production"] = base_prod
        st.session_state.inputs["base_unit_cost"] = base_cost

        prod_s, cost_s = model(st.session_state.inputs)
        rev1, prof1 = calc(prod_s, base_price, cost_s)

        st.session_state.d1_results = (prod_s, rev1, prof1)

        st.session_state.step = "d1_insights"
        st.rerun()

# =========================================================
# DECISION 1 INSIGHTS PAGE
# =========================================================

if st.session_state.step == "d1_insights":

    insights(st.session_state.d1, "DECISION 1")

    if st.button("Continue"):
        st.session_state.step = "d1_summary"
        st.rerun()

# =========================================================
# DECISION 1 SUMMARY PAGE
# =========================================================

if st.session_state.step == "d1_summary":

    prod_s, rev1, prof1 = st.session_state.d1_results
    prod0, rev0, prof0 = st.session_state.post_shock_results

    st.markdown("### BASELINE")
    st.write(f"Production: {base_prod:,}")
    st.write(f"Revenue: £{base_rev:,}")
    st.write(f"Profit: £{base_profit:,}")

    st.markdown("### POST-SHOCK")
    st.write(f"Production: {round(prod0):,}")
    st.write(f"Revenue: £{round(rev0):,}")
    st.write(f"Profit: £{round(prof0):,}")

    st.markdown("### AFTER IMMEDIATE COMMERCIAL RESPONSE")
    st.write(f"Production: {round(prod_s):,}")
    st.write(f"Revenue: £{round(rev1):,}")
    st.write(f"Profit: £{round(prof1):,}")

    if st.button("Continue"):
        st.session_state.step = "decision_2"
        st.rerun()

# =========================================================
# DECISION 2
# =========================================================

if st.session_state.step == "decision_2":

    st.markdown("---")
    st.subheader("DECISION 2 — LONG-TERM STRUCTURAL RESPONSE")

    d2 = st.radio(
        "Choose strategy:",
        [
            "Redesign EV to be less reliant on lithium",
            "Diversify supply chain",
            "Integrate vertically by investing in mining and refining"
        ]
    )

    if st.button("Continue"):

        if d2 == "Diversify supply chain":
            st.session_state.inputs["supply_reduction"] *= 0.6
            st.session_state.inputs["input_price_increase"] *= 0.7
            st.session_state.inputs["dependency"] *= 0.75

        elif d2 == "Integrate vertically by investing in mining and refining":
            st.session_state.inputs["supply_reduction"] *= 0.8
            st.session_state.inputs["input_price_increase"] *= 0.85
            st.session_state.inputs["dependency"] *= 0.85

        elif d2 == "Redesign EV to be less reliant on lithium":
            st.session_state.inputs["supply_reduction"] *= 0.9
            st.session_state.inputs["input_price_increase"] *= 0.95
            st.session_state.inputs["dependency"] *= 0.8

        st.session_state.d2 = d2

        prod2, cost2 = model(st.session_state.inputs)
        rev2, prof2 = calc(prod2, base_price, cost2)

        st.session_state.final_results = (prod2, rev2, prof2)

        st.session_state.step = "d2_insights"
        st.rerun()

# =========================================================
# DECISION 2 INSIGHTS PAGE
# =========================================================

if st.session_state.step == "d2_insights":

    insights(st.session_state.d2, "DECISION 2")

    if st.button("Continue"):
        st.session_state.step = "final"
        st.rerun()

# =========================================================
# FINAL PAGE
# =========================================================

if st.session_state.step == "final":

    prod2, rev2, prof2 = st.session_state.final_results
    prod0, rev0, prof0 = st.session_state.post_shock_results

    st.title("FINAL STATS")

    st.markdown("### POST-SHOCK")
    st.write(f"Production: {round(prod0):,}")
    st.write(f"Revenue: £{round(rev0):,}")
    st.write(f"Profit: £{round(prof0):,}")

    st.markdown("### AFTER IMMEDIATE COMMERCIAL RESPONSE")
    st.write(f"Production: {round(st.session_state.d1_results[0]):,}")
    st.write(f"Revenue: £{round(st.session_state.d1_results[1]):,}")
    st.write(f"Profit: £{round(st.session_state.d1_results[2]):,}")

    st.markdown("### AFTER LONG-TERM STRUCTURAL RESPONSE")
    st.write(f"Production: {round(prod2):,}")
    st.write(f"Revenue: £{round(rev2):,}")
    st.write(f"Profit: £{round(prof2):,}")

    recovery_vs_shock = pct(prof2, prof0)
    shock_score = max(0, min(recovery_vs_shock * 2, 100))

    baseline_risk = base_inputs["dependency"] * base_inputs["supply_reduction"]
    new_risk = st.session_state.inputs["dependency"] * st.session_state.inputs["supply_reduction"]

    risk_delta = (baseline_risk - new_risk) / baseline_risk
    resilience_score = max(0, min(risk_delta * 120, 100))

    structural_score = {"Diversify supply chain": 60,
                        "Integrate vertically by investing in mining and refining": 80,
                        "Redesign EV to be less reliant on lithium": 95}.get(st.session_state.d2, 40)

    commercial_score = {"Keep prices stable": 45,
                        "Raise prices by 10%": 70,
                        "Prioritise higher-margin models": 85}.get(st.session_state.d1, 40)

    base_score = (
        shock_score * 0.30 +
        resilience_score * 0.30 +
        structural_score * 0.25 +
        commercial_score * 0.15
    )

    score = max(0, min(base_score, 100))

    if score >= 80:
        st.success("STRONG STRATEGY - effective trade-offs across risk and return")
    elif score >= 70:
        st.warning("DEFENSIVE STRATEGY - stability preserved but not optimised")
    else:
        st.error("HIGH RISK STRATEGY - structural vulnerabilities remain exposed")

    if st.button("Restart Simulation"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
