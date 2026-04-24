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
# CONTEXT 
# =========================================================

st.markdown(""" You are the CEO of a global EV manufacturer, dependant on lithium supplied from Sub-Saharan Africa. Recent armed conflict in the region has led to insurgents seizing key mining sites, and cutting transport routes to export ports. As a result, your firm experiences a shock
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
    st.subheader(f"STRATEGIC INSIGHTS — {stage}")

    if choice == "raise_prices":
        st.write("""
You chose to leverage pricing power as a short-term buffer against input cost shocks.

Pros:
- Immediately improves revenue per unit and protects margins
- Signals premium positioning
- Offsets short-term inflation

Cons:
- Higher demand elasticity risk
- Possible customer switching
- Potential market share loss
""")

    elif choice == "keep_prices":
        st.write("""
You chose to protect volume stability over margin expansion.

Pros:
- Preserves market share
- Maintains competitiveness
- Avoids demand contraction

Cons:
- Margin compression
- Profit sensitivity to shocks
- No inflation pass-through
""")

    elif choice == "prioritise_high_margin":
        st.write("""
You prioritise higher-margin EVs.

Pros:
- Better unit economics
- Higher capital efficiency
- Stronger resilience

Cons:
- Lower volume
- Weaker mass-market position
- Higher volatility
""")

    elif choice == "diversify":
        st.write("""
You diversify supply chains.

Pros:
- Lower geopolitical risk
- Better resilience
- Stronger supplier leverage

Cons:
- Higher costs
- Inefficiencies
- Slow benefits
""")

    elif choice == "integrate":
        st.write("""
You integrate vertically.

Pros:
- Greater control
- Margin capture
- Strategic autonomy

Cons:
- High capital cost
- Less flexibility
- Operational risk
""")

    elif choice == "redesign":
        st.write("""
You redesign battery architecture.

Pros:
- Lower lithium dependency
- Long-term resilience
- Tech differentiation

Cons:
- R&D cost
- Transition inefficiency
- Execution risk
""")


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
# SHOCK 
# =========================================================

if "inputs" not in st.session_state:
    st.session_state.inputs = copy.deepcopy(base_inputs)
    st.session_state.shock_applied = False

if st.button("Apply Shock"):
    st.session_state.inputs, st.session_state.shock = shock_engine(base_inputs)
    st.session_state.shock_applied = True

if st.session_state.shock_applied:
    st.success(f"Shock Applied — multiplier: {round(st.session_state.shock,2)}")

    prod_s, cost_s = model(st.session_state.inputs)
    rev_s, prof_s = calc(prod_s, base_price, cost_s)

    st.subheader("POST-SHOCK STATE (PRE DECISION)")
    st.write(f"Production: {round(prod_s):,} ({round(pct(prod_s, base_prod),2)}%)")
    st.write(f"Revenue: £{round(rev_s):,} ({round(pct(rev_s, base_rev),2)}%)")
    st.write(f"Profit: £{round(prof_s):,} ({round(pct(prof_s, base_profit),2)}%)")

    # =========================================================
    # DECISION 1
    # =========================================================

    st.markdown("---")
    st.subheader("DECISION 1 — COMMERCIAL RESPONSE")

    d1 = st.radio(
        "Choose strategy:",
        ["raise_prices", "keep_prices", "prioritise_high_margin"]
    )

    if st.button("Apply Decision 1"):

        if d1 == "raise_prices":
            base_price *= 1.10
            base_prod *= 0.98
            base_cost *= 1.00

        elif d1 == "keep_prices":
            base_cost *= 1.02

        elif d1 == "prioritise_high_margin":
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
        # DECISION 2
        # =========================================================

        st.markdown("---")
        st.subheader("DECISION 2 — STRUCTURAL RESPONSE")

        d2 = st.radio(
            "Choose structural strategy:",
            ["redesign", "diversify", "integrate"]
        )

        if st.button("Apply Decision 2"):

            if d2 == "diversify":
                st.session_state.inputs["supply_reduction"] *= 0.6
                st.session_state.inputs["input_price_increase"] *= 0.7
                st.session_state.inputs["dependency"] *= 0.75
                st.session_state.inputs["flexibility"] *= 1.1

            elif d2 == "integrate":
                st.session_state.inputs["supply_reduction"] *= 0.8
                st.session_state.inputs["input_price_increase"] *= 0.85
                st.session_state.inputs["dependency"] *= 0.85
                st.session_state.inputs["flexibility"] *= 1.25

            elif d2 == "redesign":
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

            # =========================================================
            # FINAL SCORE 
            # =========================================================

            recovery_vs_shock = pct(prof2, prof_s)
            shock_score = recovery_vs_shock * 2
            shock_score = max(0, min(shock_score, 100))

            baseline_risk = base_inputs["dependency"] * base_inputs["supply_reduction"]
            new_risk = st.session_state.inputs["dependency"] * st.session_state.inputs["supply_reduction"]

            risk_delta = (baseline_risk - new_risk) / baseline_risk
            resilience_score = max(0, min(risk_delta * 120, 100))

            structural_score = {"diversify": 60, "integrate": 80, "redesign": 95}.get(d2, 40)
            commercial_score = {"keep_prices": 45, "raise_prices": 70, "prioritise_high_margin": 85}.get(d1, 40)

            base_score = (
                shock_score * 0.30 +
                resilience_score * 0.30 +
                structural_score * 0.25 +
                commercial_score * 0.15
            )

            multiplier = 1.0

            if d1 == "prioritise_high_margin" and d2 == "redesign":
                multiplier += 0.25
            if d1 == "prioritise_high_margin" and d2 == "integrate":
                multiplier += 0.18
            if d1 == "raise_prices" and d2 == "diversify":
                multiplier += 0.10

            score = max(0, min(base_score * multiplier, 100))

            st.markdown("---")
            st.subheader("FINAL RESULTS")

            st.write(f"Final Profit: £{round(prof2):,}")
            st.write(f"Final Revenue: £{round(rev2):,}")
            st.write(f"Final Production: {round(prod2):,}")

            if score >= 80:
                st.success("STRONG STRATEGY: effective trade-offs across risk and return.")
            elif score >= 70:
                st.warning("DEFENSIVE STRATEGY: stability preserved but not optimised.")
            else:
                st.error("HIGH RISK STRATEGY: structural vulnerabilities remain exposed.")
