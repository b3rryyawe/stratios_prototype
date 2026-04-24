import streamlit as st
import random
import copy

st.set_page_config(page_title="STRATIOS Strategy Engine", layout="wide")

# =========================================================
# TITLE
# =========================================================

st.title("STRATIOS | Prototype Strategy Engine")
st.subheader("Role: CEO of a Global EV Manufacturer")
st.write("Scenario: Lithium supply shock disrupting global supply chains")

st.divider()

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
# CORE FUNCTIONS
# =========================================================

def shock_engine(inputs):
    shock = random.uniform(0.85, 1.15)
    new_inputs = copy.deepcopy(inputs)
    new_inputs["supply_reduction"] *= shock
    new_inputs["input_price_increase"] *= shock
    return new_inputs, shock


def model(inputs):
    production = inputs["base_production"] * (
        1 - inputs["supply_reduction"] *
        inputs["dependency"] *
        (1 - inputs["flexibility"])
    )

    cost = inputs["base_unit_cost"] * (
        1 + inputs["input_price_increase"] *
        inputs["dependency"]
    )

    return production, cost


def calc(prod, price, cost):
    revenue = prod * price
    profit = revenue - (prod * cost)
    return revenue, profit


def pct(new, old):
    return ((new - old) / old) * 100


# =========================================================
# SESSION STATE INIT
# =========================================================

if "inputs" not in st.session_state:
    st.session_state.inputs, st.session_state.shock = shock_engine(base_inputs)
    st.session_state.base_price = base_inputs["base_price"]
    st.session_state.base_prod = base_inputs["base_production"]
    st.session_state.base_cost = base_inputs["base_unit_cost"]
    st.session_state.stage = 0


# =========================================================
# BASELINE DASHBOARD
# =========================================================

base_prod = base_inputs["base_production"]
base_price = base_inputs["base_price"]
base_cost = base_inputs["base_unit_cost"]

base_rev, base_profit = calc(base_prod, base_price, base_cost)

st.subheader("Baseline (Pre-Shock)")

col1, col2, col3 = st.columns(3)
col1.metric("Production", f"{base_prod:,}")
col2.metric("Revenue", f"£{base_rev:,}")
col3.metric("Profit", f"£{base_profit:,}")

st.divider()

# =========================================================
# SHOCK STATE
# =========================================================

inputs = st.session_state.inputs

prod_s, cost_s = model(inputs)
rev_s, prof_s = calc(prod_s, st.session_state.base_price, cost_s)

st.subheader("Post-Shock (Pre-Decision)")

col1, col2, col3 = st.columns(3)
col1.metric("Production", f"{round(prod_s):,}", f"{round(pct(prod_s, base_prod),2)}%")
col2.metric("Revenue", f"£{round(rev_s):,}", f"{round(pct(rev_s, base_rev),2)}%")
col3.metric("Profit", f"£{round(prof_s):,}", f"{round(pct(prof_s, base_profit),2)}%")

st.divider()

# =========================================================
# DECISION 1
# =========================================================

st.subheader("Decision 1 — Commercial Response")

d1 = st.radio(
    "Choose strategy:",
    [
        "Raise prices by 10%",
        "Keep prices stable",
        "Prioritise high-margin models"
    ]
)

# Apply D1
if st.button("Apply Decision 1"):

    if d1 == "Raise prices by 10%":
        st.session_state.base_price *= 1.10
        st.session_state.base_prod *= 0.98
        strategy1 = "raise_prices"

    elif d1 == "Keep prices stable":
        st.session_state.base_cost *= 1.02
        strategy1 = "keep_prices"

    else:
        st.session_state.base_price *= 1.05
        st.session_state.base_prod *= 0.85
        st.session_state.base_cost *= 0.95
        strategy1 = "prioritise_high_margin"

    st.session_state.strategy1 = strategy1
    st.session_state.stage = 1


# =========================================================
# DECISION 2
# =========================================================

if st.session_state.stage >= 1:

    st.divider()
    st.subheader("Decision 2 — Structural Response")

    d2 = st.radio(
        "Choose structural strategy:",
        [
            "Redesign battery",
            "Diversify supply chain",
            "Vertical integration"
        ]
    )

    if st.button("Apply Decision 2"):

        inputs = st.session_state.inputs

        if d2 == "Diversify supply chain":
            inputs["supply_reduction"] *= 0.6
            inputs["input_price_increase"] *= 0.7
            inputs["dependency"] *= 0.75
            strategy2 = "diversify"

        elif d2 == "Vertical integration":
            inputs["supply_reduction"] *= 0.8
            inputs["input_price_increase"] *= 0.85
            inputs["dependency"] *= 0.85
            strategy2 = "integrate"

        else:
            inputs["supply_reduction"] *= 0.9
            inputs["input_price_increase"] *= 0.95
            inputs["dependency"] *= 0.8
            strategy2 = "redesign"

        st.session_state.strategy2 = strategy2
        st.session_state.stage = 2


# =========================================================
# FINAL RESULTS + SCORING
# =========================================================

if st.session_state.stage == 2:

    inputs = st.session_state.inputs

    prod2, cost2 = model(inputs)
    rev2, prof2 = calc(prod2, st.session_state.base_price, cost2)

    st.divider()
    st.subheader("Final Results")

    col1, col2, col3 = st.columns(3)
    col1.metric("Production", f"{round(prod2):,}")
    col2.metric("Revenue", f"£{round(rev2):,}")
    col3.metric("Profit", f"£{round(prof2):,}")

    # --- Simplified scoring display ---
    score = random.randint(55, 95)  # (Keep your full scoring block here if desired)

    st.divider()
    st.subheader("Strategic Assessment")

    st.metric("Strategic Score", round(score))

    if score >= 80:
        st.success("STRONG STRATEGY")
    elif score >= 70:
        st.warning("DEFENSIVE STRATEGY")
    else:
        st.error("HIGH RISK STRATEGY")

    st.divider()

    if st.button("Restart Simulation"):
        st.session_state.clear()
        st.rerun()
