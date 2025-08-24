# balance_a_budget.py
import random
import math
import pandas as pd
import streamlit as st

# ----------------------------- Helpers -----------------------------

NAMES = [
    "Kamal", "Kiara", "Vince", "Abigail", "Vivian", "Sanjay",
    "Leo", "Maya", "Ivy", "Mitch", "Paul", "Trent", "Kathleen"
]
MONTHS = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

INCOME_BANK = [
    "Walking dogs", "Babysitting", "House-sitting", "Lifeguarding",
    "Selling old phone", "Selling old jewellery", "Gift from Nana",
    "Teaching a lesson", "Delivering newspapers", "Bagging groceries"
]
EXPENSE_BANK = [
    "School book fair", "New gym bag", "Lacrosse jersey", "Water park",
    "Bathing suit", "Movie night with friends", "Donating to a charity",
    "Phone payment", "Saving for university", "Hair salon", "Aquarium visit",
    "Magazine subscriptions", "Video game system", "TV subscription"
]

def fmt_money(x: float) -> str:
    x = round(float(x) + 1e-9, 2)
    if abs(x - int(x)) < 1e-9:
        return f"${int(x)}"
    return f"${x:,.2f}"

def amount_space(difficulty: int):
    """Return a generator for amounts suitable to the chosen level."""
    if difficulty == 1:     # Intro – whole dollars
        def gen(): return float(random.randrange(10, 91, 5))
    elif difficulty == 2:   # Core – whole + .50 sometimes
        def gen():
            base = random.randrange(15, 121, 5)
            return base + 0.50 if random.random() < 0.4 else float(base)
    else:                   # Challenge – dollars & cents
        def gen():
            dollars = random.randint(15, 180)
            cents = random.choice([0, 25, 50, 75, 80, 95])
            return float(dollars) + cents/100.0
    return gen

# --------------------------- Problem Maker --------------------------

def make_problem(difficulty: int):
    rnd = random.Random()
    person = rnd.choice(NAMES)
    month = rnd.choice(MONTHS)

    gen = amount_space(difficulty)

    n_income = rnd.randint(3, 3 if difficulty == 1 else 4)
    n_exp    = rnd.randint(3, 3 if difficulty == 1 else 4)

    labels_income = rnd.sample(INCOME_BANK, n_income)
    labels_exp    = rnd.sample(EXPENSE_BANK, n_exp)

    incomes_vals  = [gen() for _ in range(n_income)]
    expenses_vals = [gen() for _ in range(n_exp)]

    unknown_side = rnd.choice(["income", "expense"])

    if unknown_side == "income":
        idx = rnd.randrange(n_income)
        known_income = sum(incomes_vals) - incomes_vals[idx]
        known_exp    = sum(expenses_vals)
        unknown_val  = known_exp - known_income
        if unknown_val <= 0:
            return make_problem(difficulty)
        if difficulty == 1:
            unknown_val = float(round(unknown_val))
        elif difficulty == 2:
            unknown_val = round(unknown_val * 2) / 2.0
        else:
            unknown_val = round(unknown_val, 2)
        incomes_vals[idx] = unknown_val
        unknown_label = labels_income[idx]
        unknown_prompt_side = "Income"
        unknown_pos = ("income", idx)
    else:
        idx = rnd.randrange(n_exp)
        known_exp    = sum(expenses_vals) - expenses_vals[idx]
        known_income = sum(incomes_vals)
        unknown_val  = known_income - known_exp
        if unknown_val <= 0:
            return make_problem(difficulty)
        if difficulty == 1:
            unknown_val = float(round(unknown_val))
        elif difficulty == 2:
            unknown_val = round(unknown_val * 2) / 2.0
        else:
            unknown_val = round(unknown_val, 2)
        expenses_vals[idx] = unknown_val
        unknown_label = labels_exp[idx]
        unknown_prompt_side = "Expense"
        unknown_pos = ("expense", idx)

    # Build display rows: we’ll keep EXACTLY one blank cell.
    incomes = []
    expenses = []
    if unknown_side == "income":
        for i, lab in enumerate(labels_income):
            v = incomes_vals[i]
            incomes.append({"label": lab, "value": None if i == idx else v})
        for i, lab in enumerate(labels_exp):
            expenses.append({"label": lab, "value": expenses_vals[i]})
    else:
        for i, lab in enumerate(labels_income):
            incomes.append({"label": lab, "value": incomes_vals[i]})
        for i, lab in enumerate(labels_exp):
            v = expenses_vals[i]
            expenses.append({"label": lab, "value": None if i == idx else v})

    total_income_known = sum(r["value"] for r in incomes if r["value"] is not None)
    total_exp_known    = sum(r["value"] for r in expenses if r["value"] is not None)

    answer = float(round(unknown_val, 2))

    return {
        "title": f"{person}'s {month} budget",
        "person": person,
        "month": month,
        "incomes": incomes,
        "expenses": expenses,
        "unknown_side": unknown_side,
        "unknown_pos": unknown_pos,        # ("income"/"expense", index)
        "unknown_label": unknown_label,
        "unknown_prompt_side": unknown_prompt_side,
        "answer": answer,
        "totals": {
            "income_known": total_income_known,
            "expense_known": total_exp_known
        }
    }

# ----------------------------- UI Page ------------------------------

def run():
    st.markdown("**Year 5 > Financial Literacy**")
    st.title("Adjust / Balance a Budget")

    # Session state
    ss = st.session_state
    ss.setdefault("bb_difficulty", 1)
    ss.setdefault("bb_problem", None)
    ss.setdefault("bb_submitted", False)

    # Top controls
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        level_name = st.selectbox(
            "Difficulty",
            ["Intro", "Core", "Challenge"],
            index=ss.bb_difficulty - 1,
            help="Intro: whole dollars • Core: whole/half-dollars • Challenge: dollars & cents",
        )
        ss.bb_difficulty = {"Intro": 1, "Core": 2, "Challenge": 3}[level_name]
    with c2:
        if st.button("🆕 New Record", use_container_width=True):
            ss.bb_problem = None
            ss.bb_submitted = False
            st.rerun()
    with c3:
        if st.button("← Back", use_container_width=True):
            try:
                if "subtopic" in st.query_params:
                    del st.query_params["subtopic"]
            except Exception:
                pass
            st.rerun()

    st.divider()

    # Problem
    if ss.bb_problem is None:
        ss.bb_problem = make_problem(ss.bb_difficulty)
    P = ss.bb_problem

    # Title (avoid backslash in f-string expression)
    name_for_line = P["title"].split("'")[0].strip()
    st.subheader(f"This is {name_for_line}'s financial record:")

    # Build DataFrames for editable tables (only one cell is blank)
    inc_rows = []
    for r in P["incomes"]:
        inc_rows.append(
            {
                "Description": r["label"],
                "Amount ($)": None if r["value"] is None else round(float(r["value"]), 2),
            }
        )
    exp_rows = []
    for r in P["expenses"]:
        exp_rows.append(
            {
                "Description": r["label"],
                "Amount ($)": None if r["value"] is None else round(float(r["value"]), 2),
            }
        )

    df_inc = pd.DataFrame(inc_rows)
    df_exp = pd.DataFrame(exp_rows)

    # Render side-by-side “tables” with the editable cell inside
    col_inc, col_exp = st.columns(2)

    with col_inc:
        st.markdown("#### Income")
        inc_edit = st.data_editor(
            df_inc,
            num_rows="fixed",
            use_container_width=True,
            hide_index=True,
            column_config={
                "Description": st.column_config.TextColumn(
                    "Description", help="Income items", required=False
                ),
                "Amount ($)": st.column_config.NumberColumn(
                    "Amount ($)", format="$%.2f", help="Fill only the blank cell"
                ),
            },
            key="inc_editor",
        )

    with col_exp:
        st.markdown("#### Expenses")
        exp_edit = st.data_editor(
            df_exp,
            num_rows="fixed",
            use_container_width=True,
            hide_index=True,
            column_config={
                "Description": st.column_config.TextColumn(
                    "Description", help="Expense items", required=False
                ),
                "Amount ($)": st.column_config.NumberColumn(
                    "Amount ($)", format="$%.2f", help="Fill only the blank cell"
                ),
            },
            key="exp_editor",
        )

    # Instruction + hint
    st.markdown(
        f"**Question:** How much should the **{P['unknown_prompt_side']}** item "
        f"**“{P['unknown_label']}”** be so that **Income = Expenses**?"
    )

    with st.expander("💡 Hint"):
        if P["unknown_side"] == "income":
            diff = P["totals"]["expense_known"] - P["totals"]["income_known"]
            st.write(
                f"Add known incomes and expenses. Missing **income** is the difference: "
                f"{fmt_money(P['totals']['expense_known'])} − {fmt_money(P['totals']['income_known'])} "
                f"= **{fmt_money(diff)}**."
            )
        else:
            diff = P["totals"]["income_known"] - P["totals"]["expense_known"]
            st.write(
                f"Add known incomes and expenses. Missing **expense** is the difference: "
                f"{fmt_money(P['totals']['income_known'])} − {fmt_money(P['totals']['expense_known'])} "
                f"= **{fmt_money(diff)}**."
            )

    # Buttons
    cA, cB = st.columns([1, 1])
    with cA:
        submit = st.button("✅ Submit", use_container_width=True)
    with cB:
        next_rec = st.button("➡️ Next Record", use_container_width=True)

    if next_rec:
        ss.bb_problem = None
        ss.bb_submitted = False
        st.rerun()

    # Pull the single blank cell from the edited tables
    def read_user_value() -> float | None:
        side, idx = P["unknown_pos"]
        try:
            if side == "income":
                val = inc_edit.loc[idx, "Amount ($)"]
            else:
                val = exp_edit.loc[idx, "Amount ($)"]
            if val is None or (isinstance(val, float) and math.isnan(val)):
                return None
            return round(float(val), 2)
        except Exception:
            return None

    if submit:
        ss.bb_submitted = True

    if ss.bb_submitted:
        entered = read_user_value()
        if entered is None:
            st.warning("Please enter a number in the blank cell of the table.")
            return

        ans = round(float(P["answer"]), 2)
        if abs(entered - ans) < 0.01:
            st.success(f"Great work! **{fmt_money(entered)}** balances the budget.")
        else:
            st.error(f"Not quite. You entered **{fmt_money(entered)}**.")

        with st.expander("📘 See the step-by-step solution", expanded=abs(entered-ans) >= 0.01):
            if P["unknown_side"] == "income":
                st.markdown(
                    f"""
1) Add known incomes: **{fmt_money(P['totals']['income_known'])}**  
2) Add known expenses: **{fmt_money(P['totals']['expense_known'])}**  
3) Unknown income = expenses − known incomes  
   → **{fmt_money(P['totals']['expense_known'])} − {fmt_money(P['totals']['income_known'])} = {fmt_money(ans)}**  
4) Therefore, **{P['unknown_label']} = {fmt_money(ans)}**.
"""
                )
            else:
                st.markdown(
                    f"""
1) Add known incomes: **{fmt_money(P['totals']['income_known'])}**  
2) Add known expenses: **{fmt_money(P['totals']['expense_known'])}**  
3) Unknown expense = incomes − known expenses  
   → **{fmt_money(P['totals']['income_known'])} − {fmt_money(P['totals']['expense_known'])} = {fmt_money(ans)}**  
4) Therefore, **{P['unknown_label']} = {fmt_money(ans)}**.
"""
                )

        # Show the balanced totals based on the correct value
        if P["unknown_side"] == "income":
            inc_total = P["totals"]["income_known"] + ans
            exp_total = P["totals"]["expense_known"]
        else:
            inc_total = P["totals"]["income_known"]
            exp_total = P["totals"]["expense_known"] + ans

        st.info(f"Balanced totals → **Income: {fmt_money(inc_total)}** and **Expenses: {fmt_money(exp_total)}**")


if __name__ == "__main__":
    run()
