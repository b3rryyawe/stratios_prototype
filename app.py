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
    st.markdown("**ROLE:** CEO of a global EV manufacturer")
    st.markdown("**CONTEXT:** Lithium supply shock disrupting global supply chains")

    if st.button("Begin"):
        st.session_state.started = True
        st.rerun()

    st.stop()

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


def insights(choice, stage):

    st.markdown("---")
    st.subheader(f"STRATEGIC INSIGHTS — {stage}")

    if choice == "Raise EV prices":
        st.write("Pricing power strategy insights...")

    elif choice == "Keep EV prices stable":
        st.write("Stable pricing strategy insights...")

    elif choice == "Prioritise higher-margin EVs":
        st.write("Margin optimisation strategy insights...")

    elif choice == "Diversify supply chain":
        st.write("Diversification strategy insights...")

    elif choice == "Invest in mining and refining":
        st.write("Vertical integration strategy insights...")

    elif choice == "Redesign EVs to be less reliant on lithium":
        st.write("Redesign strategy insights...")


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

if st.button("Apply Shock"):
    st.session_state.inputs, st.session_state.shock = shock_engine(base_inputs)
    st.session_state.shock_applied = True

if st.session_state.shock_applied:

    # REMOVED multiplier display → replaced with clean label
    st.subheader("NEW STATS")

    prod_s, cost_s = model(st.session_state.inputs)
    rev_s, prof_s = calc(prod_s, base_price, cost_s)

    st.subheader("POST-SHOCK STATE (PRE DECISION)")
    st.write(f"Production: {round(prod_s):,} ({round(pct(prod_s, base_prod),2)}%)")
    st.write(f"Revenue: £{round(rev_s):,} ({round(pct(rev_s, base_rev),2)}%)")
    st.write(f"Profit: £{round(prof_s):,} ({round(pct(prof_s, base_profit),2)}%)")

    # =========================================================
    # DECISION 1 (RENAMED)
    # =========================================================

    st.markdown("---")
    st.subheader("DECISION 1 — COMMERCIAL RESPONSE")

    d1 = st.radio(
        "Choose strategy:",
        [
            "Raise EV prices",
            "Keep EV prices stable",
            "Prioritise higher-margin EVs"
        ]
    )

    if st.button("Apply Decision 1"):

        if d1 == "Raise EV prices":
            base_price *= 1.10
            base_prod *= 0.98

        elif d1 == "Keep EV prices stable":
            base_cost *= 1.02

        elif d1 == "Prioritise higher-margin EVs":
            base_price *= 1.05
            base_prod *= 0.85
            base_cost *= 0.95

        st.session_state.inputs["base_production"] = base_prod
        st.session_state.inputs["base_unit_cost"] = base_cost

        prod_s, cost_s = model(st.session_state.inputs)
        rev1, prof1 = calc(prod_s, base_price, cost_s)

        st.subheader("AFTER DECISION 1")
        st.write(f"Production: {round(prod_s):,}")
        st.write(f"Revenue: £{round(rev1):,}")
        st.write(f"Profit: £{round(prof1):,}")

        insights(d1, "AFTER DECISION 1")

        # =========================================================
        # DECISION 2 (RENAMED)
        # =========================================================

        st.markdown("---")
        st.subheader("DECISION 2 — STRUCTURAL RESPONSE")

        d2 = st.radio(
            "Choose structural strategy:",
            [
                "Redesign EVs to be less reliant on lithium",
                "Diversify supply chain",
                "Invest in mining and refining"
            ]
        )

        if st.button("Apply Decision 2"):

            if d2 == "Diversify supply chain":
                st.session_state.inputs["supply_reduction"] *= 0.6
                st.session_state.inputs["input_price_increase"] *= 0.7
                st.session_state.inputs["dependency"] *= 0.75
                st.session_state.inputs["flexibility"] *= 1.1

            elif d2 == "Invest in mining and refining":
                st.session_state.inputs["supply_reduction"] *= 0.8
                st.session_state.inputs["input_price_increase"] *= 0.85
                st.session_state.inputs["dependency"] *= 0.85
                st.session_state.inputs["flexibility"] *= 1.25

            elif d2 == "Redesign EVs to be less reliant on lithium":
                st.session_state.inputs["supply_reduction"] *= 0.9
                st.session_state.inputs["input_price_increase"] *= 0.95
                st.session_state.inputs["dependency"] *= 0.8
                st.session_state.inputs["flexibility"] *= 1.4

            prod2, cost2 = model(st.session_state.inputs)
            rev2, prof2 = calc(prod2, base_price, cost2)

            st.subheader("AFTER DECISION 2")
            st.write(f"Production: {round(prod2):,}")
            st.write(f"Revenue: £{round(rev2):,}")
            st.write(f"Profit: £{round(prof2):,}")

            insights(d2, "AFTER DECISION 2")
