import streamlit as st
import copy
import random

st.set_page_config(page_title="STRATIOS", layout="wide")

# =========================================================
# START SCREEN
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.title("STRATIOS | PROTOTYPE STRATEGY ENGINE")

    if st.button("Begin"):
        st.session_state.started = True
        st.rerun()

    st.stop()

# =========================================================
# POST-BEGIN CONTEXT (MOVED HERE)
# =========================================================

st.markdown("**ROLE:** CEO of a global EV manufacturer")
st.markdown("**CONTEXT:** Lithium supply shock disrupting global supply chains")

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
# FUNCTIONS (UNCHANGED LOGIC)
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


# =========================================================
# BASELINE
# =========================================================

base_prod = base_inputs["base_production"]
base_price = base_inputs["base_price"]
base_cost = base_inputs["base_unit_cost"]

base_rev, base_profit = calc(base_prod, base_price, base_cost)

st.subheader("BASELINE STATE (PRE-SHOCK)")
st.write(f"Production: {base_prod:,}")
st.write(f"Revenue: £{base_rev:,}")
st.write(f"Profit: £{base_profit:,}")

# =========================================================
# SHOCK INIT
# =========================================================

if "inputs" not in st.session_state:
    st.session_state.inputs = copy.deepcopy(base_inputs)
    st.session_state.shock_applied = False

# =========================================================
# POST-SHOCK DISPLAY FIRST
# =========================================================

if st.session_state.shock_applied:

    st.subheader("POST-SHOCK STATE (PRE DECISION)")

    prod_s, cost_s = model(st.session_state.inputs)
    rev_s, prof_s = calc(prod_s, base_price, cost_s)

    st.write(f"Production: {round(prod_s):,} ({round(pct(prod_s, base_prod),2)}%)")
    st.write(f"Revenue: £{round(rev_s):,} ({round(pct(rev_s, base_rev),2)}%)")
    st.write(f"Profit: £{round(prof_s):,} ({round(pct(prof_s, base_profit),2)}%)")

    # =========================================================
    # MOVED SHOCK BUTTON HERE
    # =========================================================

    if st.button("Apply New Shock"):
        st.session_state.inputs, st.session_state.shock = shock_engine(base_inputs)
        st.session_state.shock_applied = True
        st.rerun()

# initial shock trigger (first time only)
if not st.session_state.shock_applied:
    if st.button("Apply New Shock"):
        st.session_state.inputs, st.session_state.shock = shock_engine(base_inputs)
        st.session_state.shock_applied = True
        st.rerun()
