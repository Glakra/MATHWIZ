# -------------------- Keeping Financial Records (works on older Streamlit) --------------------
import random
from datetime import date
import numpy as np
import pandas as pd
import streamlit as st

# ---------- helpers ----------
def money(x: float) -> str:
    return f"${x:,.2f}"

def rnd_amount(lo: float, hi: float, step: float = 0.05) -> float:
    n = max(1, int(round((hi - lo) / step)))
    return round(lo + random.randint(0, n) * step, 2)

def safe_spend(prev_balance: float, lo: float, hi: float) -> float:
    # keep spend < prev balance
    hi = min(hi, max(0.50, prev_balance - 0.50))
    if hi < lo:
        lo = max(0.50, hi / 2)
    return rnd_amount(lo, hi)

NAMES = ["Ava","Ben","Cara","Daniel","Ethan","Finn","Grace","Hana",
         "Ivy","Jack","Kara","Leo","Maya","Noah","Olive","Parker",
         "Quinn","Ruby","Sam","Tara","Uma","Violet","Will","Xena",
         "Yasmin","Zach"]

EARNING_ACTS = [
    "yard work","washing dishes","pet sitting","tutoring","lemonade stand",
    "garage sale","walking dogs","teaching ballet","judging a contest",
    "selling crafts","mowing a lawn","car-wash"
]

SPEND_ITEMS = [
    "movie ticket","basketball","notebook","box of markers","hot chips",
    "kite","train ticket","chocolate bar","pasta","paint brush",
    "balloon kit","roll of ribbon","blankets","disposable cups",
    "bag of dried apricots","pavlova ingredients","sandpaper"
]

# ---------- record generator ----------
def generate_record(difficulty: int):
    name = random.choice(NAMES)
    month = random.choice([2,4,5,6,7,8,9,10,12])

    bal_start = {
        1: rnd_amount(60, 120),
        2: rnd_amount(120, 240),
        3: rnd_amount(180, 320),
        4: rnd_amount(220, 420),
    }[difficulty]

    prefilled = 2 if difficulty in (1, 2) else 3

    rows = []
    cur = round(bal_start, 2)
    rows.append({
        "Date": f"Balance: end of {date(2000,month,1).strftime('%B')}",
        "Description": "Balance: end of previous month",
        "Received": np.nan, "Expenses": np.nan, "Available Funds": cur
    })

    used_days = set()
    def next_day():
        while True:
            d = random.randint(2, 28)
            if d not in used_days:
                used_days.add(d); return d

    for _ in range(prefilled):
        d = next_day()
        if random.random() < 0.5:
            item = random.choice(SPEND_ITEMS)
            amt = safe_spend(cur, 1.20, {1:9.0, 2:18.0, 3:24.0, 4:32.0}[difficulty])
            cur = round(cur - amt, 2)
            rows.append({"Date": f"{d}/{month}", "Description": item,
                         "Received": np.nan, "Expenses": amt, "Available Funds": cur})
        else:
            act = random.choice(EARNING_ACTS)
            amt = rnd_amount(5.0, {1:15.0, 2:25.0, 3:35.0, 4:50.0}[difficulty])
            cur = round(cur + amt, 2)
            rows.append({"Date": f"{d}/{month}", "Description": act,
                         "Received": amt, "Expenses": np.nan, "Available Funds": cur})

    # final editable row
    d = next_day()
    is_expense = random.random() < 0.6
    if is_expense:
        item = random.choice(SPEND_ITEMS)
        amt = safe_spend(cur, 1.20, {1:9.5, 2:19.5, 3:28.0, 4:36.5}[difficulty])
        correct_rec, correct_exp = 0.00, amt
        new_bal = round(cur - amt, 2)
        prompt = f"On {d}/{month}, {name} bought {item} for {money(amt)}. Complete that row in the record."
        desc = item
    else:
        act = random.choice(EARNING_ACTS)
        amt = rnd_amount(6.0, {1:18.0, 2:28.0, 3:40.0, 4:60.0}[difficulty])
        correct_rec, correct_exp = amt, 0.00
        new_bal = round(cur + amt, 2)
        prompt = f"On {d}/{month}, {name} earned {money(amt)} for {act}. Complete that row in the record."
        desc = act

    rows.append({"Date": f"{d}/{month}", "Description": desc,
                 "Received": np.nan, "Expenses": np.nan, "Available Funds": np.nan})

    return {
        "name": name,
        "rows": rows,
        "prev_balance": cur,
        "correct_rec": round(correct_rec, 2),
        "correct_exp": round(correct_exp, 2),
        "correct_bal": round(new_bal, 2),
        "prompt": prompt
    }

# ---------- app ----------
def run():
    st.markdown("**📚 Year 5 > Financial Literacy**")
    st.title("🧾 Keeping Financial Records")

    if "kfr_difficulty" not in st.session_state:
        st.session_state.kfr_difficulty = 1
    if "kfr_problem" not in st.session_state:
        st.session_state.kfr_problem = generate_record(st.session_state.kfr_difficulty)
    if "kfr_submitted" not in st.session_state:
        st.session_state.kfr_submitted = False

    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        level = st.selectbox(
            "Difficulty",
            ["Intro", "Standard", "Advanced", "Challenge"],
            index=st.session_state.kfr_difficulty - 1,
        )
        chosen = ["Intro","Standard","Advanced","Challenge"].index(level) + 1
        if chosen != st.session_state.kfr_difficulty:
            st.session_state.kfr_difficulty = chosen
            st.session_state.kfr_problem = generate_record(chosen)
            st.session_state.kfr_submitted = False
            st.rerun()
    with c2:
        if st.button("🔁 New Record", use_container_width=True):
            st.session_state.kfr_problem = generate_record(st.session_state.kfr_difficulty)
            st.session_state.kfr_submitted = False
            st.rerun()
    with c3:
        if st.button("← Back", use_container_width=True, type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

    st.divider()

    p = st.session_state.kfr_problem
    st.markdown(f"**This is {p['name']}'s financial record:**")

    base_df = pd.DataFrame(p["rows"])
    for col in ["Received", "Expenses", "Available Funds"]:
        base_df[col] = base_df[col].astype("float64")

    # Keep a pristine copy for restoring upper rows on submit
    original_df = base_df.copy(deep=True)

    # We can only reliably disable by *column* across Streamlit versions.
    # Leave numeric columns editable; lock the text columns.
    edited_df = st.data_editor(
        base_df,
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        disabled={"Date": True, "Description": True},  # column-level lock
        column_config={
            "Received": st.column_config.NumberColumn("Received", format="$%.2f", step=0.05, min_value=0.0, width="small"),
            "Expenses": st.column_config.NumberColumn("Expenses", format="$%.2f", step=0.05, min_value=0.0, width="small"),
            "Available Funds": st.column_config.NumberColumn("Available Funds", format="$%.2f", step=0.05, min_value=0.0, width="small"),
            "Date": st.column_config.TextColumn("Date"),
            "Description": st.column_config.TextColumn("Description"),
        },
        key="kfr_editor_v2",
    )

    st.caption("✏️ Only edit the **last row**. Edits in other rows are ignored.")

    st.markdown(f"**Question:** {p['prompt']}")
    with st.expander("💡 Hint", expanded=False):
        st.markdown(
            "- Start from the previous **Available Funds** (row above the blanks).\n"
            "- **Received** → add; **Expenses** → subtract.\n"
            "- Only one of *Received* or *Expenses* should be non-zero."
        )

    left, right = st.columns([1,1])
    with left:
        submit = st.button("✅ Submit", use_container_width=True)
    with right:
        next_rec = st.button("➡️ Next Record", use_container_width=True)

    if next_rec:
        st.session_state.kfr_problem = generate_record(st.session_state.kfr_difficulty)
        st.session_state.kfr_submitted = False
        st.rerun()

    if submit:
        st.session_state.kfr_submitted = True

    if st.session_state.kfr_submitted:
        # Sanitize: ignore edits above the last row
        last_idx = edited_df.index[-1]
        cleaned = edited_df.copy(deep=True)
        if len(cleaned) >= 2:
            cleaned.iloc[:-1, cleaned.columns.get_indexer(["Received","Expenses","Available Funds"])] = \
                original_df.iloc[:-1][["Received","Expenses","Available Funds"]].values

        last = cleaned.iloc[-1]
        rec_in = float(0 if np.isnan(last["Received"]) else last["Received"])
        exp_in = float(0 if np.isnan(last["Expenses"]) else last["Expenses"])
        bal_in = last["Available Funds"]
        bal_in = float("nan") if pd.isna(bal_in) else float(bal_in)

        if rec_in > 0 and exp_in > 0:
            st.warning("Only one of **Received** or **Expenses** should be filled (not both).")

        ok_rec = abs(rec_in - p["correct_rec"]) < 0.01
        ok_exp = abs(exp_in - p["correct_exp"]) < 0.01
        ok_bal = (not pd.isna(bal_in)) and abs(bal_in - p["correct_bal"]) < 0.01

        if ok_rec and ok_exp and ok_bal:
            st.success("Great work! All three entries are correct. 🎉")
        else:
            st.error("Not quite. See the worked answer below and try another record.")

        with st.expander("📖 Worked solution (show steps)", expanded=not (ok_rec and ok_exp and ok_bal)):
            prev = p["prev_balance"]
            if p["correct_rec"] > 0:
                st.markdown(
                    f"- Previous available funds: **{money(prev)}**\n"
                    f"- Received: **{money(p['correct_rec'])}** → add\n"
                    f"- New available funds: **{money(prev)} + {money(p['correct_rec'])} = {money(p['correct_bal'])}**"
                )
            else:
                st.markdown(
                    f"- Previous available funds: **{money(prev)}**\n"
                    f"- Expense: **{money(p['correct_exp'])}** → subtract\n"
                    f"- New available funds: **{money(prev)} − {money(p['correct_exp'])} = {money(p['correct_bal'])}**"
                )
            st.markdown(
                f"**Correct last row:**  Received = **{money(p['correct_rec'])}**, "
                f"Expenses = **{money(p['correct_exp'])}**, "
                f"Available Funds = **{money(p['correct_bal'])}**"
            )

# if __name__ == "__main__":
#     run()
