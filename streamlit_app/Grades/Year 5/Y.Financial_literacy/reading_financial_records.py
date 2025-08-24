# reading_financial_records.py
import random
import math
import streamlit as st
from dataclasses import dataclass

# ---------- Names, months, helpers ----------

MALE = {
    "Finn","Wyatt","Carter","Oliver","Duncan","Liam","Noah","Ben","Alex",
    "Ryan","Logan","Evan","Owen","James"
}
FEMALE = {
    "Zoe","Martha","Samantha","Emma","Chloe","Ruby","Nora","Mia","Ella",
    "Ava","Lily","Sarah","Grace"
}
MONTHS = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

def his_her(name:str)->str: return "his" if name in MALE else "her"
def he_she(name:str)->str:  return "he"  if name in MALE else "she"

def fmt_money(x: float) -> str:
    return f"${x:,.2f}"

def parse_money(text: str) -> float:
    t = (text or "").strip().replace("$","").replace(",","")
    return float(t) if t else math.nan

@dataclass
class Row:
    dstr: str
    desc: str
    received: float
    expense: float
    balance: float

# ---------- Problem generator (robust to edge cases) ----------

def generate_ledger(difficulty:int):
    person = random.choice(list(MALE | FEMALE))
    month_i = random.randrange(12)
    month = MONTHS[month_i]
    start = round(random.uniform(70, 500), 2)

    incomes_easy   = [("garage sale",12,65),("yard work",10,25),("walking dogs",10,20),
                      ("teaching ballet",25,50),("babysitting",20,45)]
    incomes_mid    = [("tutoring",12,30),("car wash",15,28),("bottle recycling",6,14),
                      ("part-time shift",25,45)]
    incomes_hard   = [("online sales",18,40),("mowing lawns",20,40),("weekend job",30,60)]

    expenses_easy  = [("hot chips",4,8),("box of markers",4,9),("notebook",4,8),
                      ("smoothie",4,7),("chocolate bar",2,5)]
    expenses_mid   = [("basketball",9,16),("white tights",5,9),("bus fares",4,10),
                      ("gift for Mum",12,22)]
    expenses_hard  = [("puffer vest",14,22),("school trip fee",12,20),
                      ("sports registration",18,28)]

    if difficulty==1:
        incomes = incomes_easy
        exps    = expenses_easy
        n_tx    = 3
    elif difficulty==2:
        incomes = incomes_easy+incomes_mid
        exps    = expenses_easy+expenses_mid
        n_tx    = 4
    else:
        incomes = incomes_easy+incomes_mid+incomes_hard
        exps    = expenses_easy+expenses_mid+expenses_hard
        n_tx    = 5

    # Build rows
    days = random.sample(range(1,28), n_tx)
    rows = []
    bal = start
    rows.append(Row(
        dstr="Balance: end of " + MONTHS[(month_i-1)%12],
        desc="opening",
        received=0.0, expense=0.0, balance=round(bal,2)
    ))

    # At least one income and one expense across the month (to avoid degenerate sets)
    must_make_income  = True
    must_make_expense = True

    for i, day in enumerate(sorted(days)):
        make_income = random.random() < 0.5
        if i == n_tx-1:
            # force variety on the final item if needed
            if must_make_income and not any(r.received>0 for r in rows):
                make_income = True
            if must_make_expense and not any(r.expense>0 for r in rows[1:]) and not make_income:
                make_income = False

        if make_income:
            label, lo, hi = random.choice(incomes)
            amt = round(random.uniform(lo, hi), 2)
            bal += amt
            rows.append(Row(f"{day}/{month_i+1}", label, amt, 0.0, round(bal,2)))
        else:
            label, lo, hi = random.choice(exps)
            amt = round(random.uniform(lo, hi), 2)
            bal -= amt
            rows.append(Row(f"{day}/{month_i+1}", label, 0.0, amt, round(bal,2)))

    # Decide question type and TARGET ROW safely
    qtype = random.choice(["after_purchase","income_amount","start_balance","final_balance","balance_after_date"])
    chosen = None

    exp_rows = [r for r in rows[1:] if r.expense  > 0]
    inc_rows = [r for r in rows[1:] if r.received > 0]

    def pick_any_balance_row():
        # Any transaction row (not the opening), or the last if only one
        return random.choice(rows[1:]) if len(rows) > 1 else rows[0]

    if qtype == "after_purchase":
        if exp_rows:
            chosen = random.choice(exp_rows)
        elif inc_rows:
            qtype  = "income_amount"
            chosen = random.choice(inc_rows)
        else:
            qtype  = "final_balance"

    if qtype == "income_amount":
        if inc_rows:
            chosen = random.choice(inc_rows)
        elif exp_rows:
            qtype  = "after_purchase"
            chosen = random.choice(exp_rows)
        else:
            qtype  = "final_balance"

    if qtype == "balance_after_date":
        chosen = pick_any_balance_row()

    # Build the prompt/answer (defensive guard if chosen is still None)
    if qtype == "after_purchase" and chosen:
        qtext = f"How much money did {person} have after {he_she(person)} bought **{chosen.desc}**?"
        answer = chosen.balance
        hint = f"Start at the opening balance, then add receipts and subtract expenses in order until you reach **{chosen.desc}**."
    elif qtype == "income_amount" and chosen:
        qtext = f"On **{chosen.dstr}**, how much money did {person} make for **{chosen.desc}**?"
        answer = chosen.received
        hint = "Look in the *Received* column for that row."
    elif qtype == "start_balance":
        qtext = f"At the start of **{month}**, how much money did {person} have?"
        answer = rows[0].balance
        hint = "Use the first row: Balance from the end of the previous month."
    elif qtype == "final_balance":
        qtext = f"What was {person}'s balance at the end of **{month}**?"
        answer = rows[-1].balance
        hint = "Follow the running balance down to the last row."
    else:  # balance_after_date (or any fallback)
        chosen = chosen or pick_any_balance_row()
        qtext = f"On **{chosen.dstr}**, what were {his_her(person)} available funds *after* the **{chosen.desc}** entry was applied?"
        answer = chosen.balance
        hint = "Use the balance (rightmost column) for that date."

    meta = {
        "person": person,
        "month": month,
        "rows": rows,
        "question": qtext,
        "answer": round(answer,2),
        "hint": hint,
        "qtype": qtype,
        "target_row": chosen  # may be None only for start/final balance types
    }
    return meta

# ---------- Table/solution rendering ----------

TABLE_CSS = """
<style>
.fin-table { border-collapse: collapse; width: 100%; max-width: 720px; }
.fin-table th, .fin-table td { border: 1px solid #d9dee3; padding: 8px 10px; text-align: right; }
.fin-table th:nth-child(1), .fin-table td:nth-child(1) { text-align: center; width: 90px; }
.fin-table th:nth-child(2), .fin-table td:nth-child(2) { text-align: left; }
.fin-head { background: linear-gradient(0deg, #0ca37a, #14b58b); color: white; }
.fin-open td { background:#f7fbff; }
.fin-highlight { background:#fff8e6; }
</style>
"""

def render_table(meta):
    rows = meta["rows"]
    trow = meta.get("target_row", None)
    html = [TABLE_CSS, "<table class='fin-table'>",
            "<tr class='fin-head'><th>Date</th><th>Description</th><th>Received</th><th>Expenses</th><th>Available Funds</th></tr>"]
    for i, r in enumerate(rows):
        cls = "fin-open" if i==0 else ""
        if trow is not None and r is trow:
            cls = "fin-highlight"
        html.append(
            f"<tr class='{cls}'>"
            f"<td>{r.dstr}</td>"
            f"<td style='text-align:left'>{'Balance: end of previous month' if i==0 else r.desc}</td>"
            f"<td>{'' if r.received==0 else fmt_money(r.received)}</td>"
            f"<td>{'' if r.expense==0 else fmt_money(r.expense)}</td>"
            f"<td>{fmt_money(r.balance)}</td>"
            "</tr>"
        )
    html.append("</table>")
    return "".join(html)

def render_steps(meta):
    rows = meta["rows"]
    steps = []
    steps.append(f"Start with opening balance: **{fmt_money(rows[0].balance)}**.")
    bal = rows[0].balance
    for r in rows[1:]:
        if r.received>0:
            bal += r.received
            steps.append(f"Add {fmt_money(r.received)} for *{r.desc}* → **{fmt_money(bal)}**.")
        else:
            bal -= r.expense
            steps.append(f"Subtract {fmt_money(r.expense)} for *{r.desc}* → **{fmt_money(bal)}**.")
    steps.append(f"Final shown balance: **{fmt_money(rows[-1].balance)}**.")
    return "\n".join([f"{i+1}. {s}" for i,s in enumerate(steps)])

# ---------- App ----------

def _new_set(set_size:int, difficulty:int):
    return [generate_ledger(difficulty) for _ in range(set_size)]

def run():
    st.markdown("**📚 Year 5 > Financial Literacy**")
    st.title("🧾 Reading Financial Records")

    # remember global preference across subtopics
    default_diff = st.session_state.get("global_difficulty_pref", 1)

    # init state
    if "finrec_difficulty" not in st.session_state:
        st.session_state.finrec_difficulty = default_diff
    if "finrec_set_size" not in st.session_state:
        st.session_state.finrec_set_size = 5
    if "finrec_set" not in st.session_state:
        st.session_state.finrec_set = _new_set(st.session_state.finrec_set_size, st.session_state.finrec_difficulty)
    if "finrec_idx" not in st.session_state:
        st.session_state.finrec_idx = 0
    if "finrec_submitted" not in st.session_state:
        st.session_state.finrec_submitted = False

    # top controls
    c1, c2, c3, c4 = st.columns([1.2,1,1,1])
    with c1:
        diff_label = {1:"Intro",2:"Core",3:"Challenge"}
        new_diff = st.selectbox("Difficulty", options=[1,2,3],
                                index=[1,2,3].index(st.session_state.finrec_difficulty),
                                format_func=lambda x: f"{x} – {diff_label[x]}")
        if new_diff != st.session_state.finrec_difficulty:
            st.session_state.finrec_difficulty = new_diff
            st.session_state["global_difficulty_pref"] = new_diff
            st.session_state.finrec_set = _new_set(st.session_state.finrec_set_size, new_diff)
            st.session_state.finrec_idx = 0
            st.session_state.finrec_submitted = False
            st.rerun()
    with c2:
        set_size = st.selectbox("Set size", [5,10],
                                index=[5,10].index(st.session_state.finrec_set_size))
        if set_size != st.session_state.finrec_set_size:
            st.session_state.finrec_set_size = set_size
            st.session_state.finrec_set = _new_set(set_size, st.session_state.finrec_difficulty)
            st.session_state.finrec_idx = 0
            st.session_state.finrec_submitted = False
            st.rerun()
    with c3:
        if st.button("🆕 New Set", use_container_width=True):
            st.session_state.finrec_set = _new_set(st.session_state.finrec_set_size, st.session_state.finrec_difficulty)
            st.session_state.finrec_idx = 0
            st.session_state.finrec_submitted = False
            st.rerun()
    with c4:
        if st.button("← Back", use_container_width=True):
            try:
                if "subtopic" in st.query_params:
                    del st.query_params["subtopic"]
            except Exception:
                pass
            st.rerun()

    # current problem
    n = len(st.session_state.finrec_set)
    i = st.session_state.finrec_idx
    meta = st.session_state.finrec_set[i]

    st.caption(f"Question {i+1} of {n} · Difficulty {st.session_state.finrec_difficulty}")
    st.subheader("Question")
    st.write(meta["question"])
    st.markdown(render_table(meta), unsafe_allow_html=True)

    with st.expander("💡 Hint"):
        st.write(meta["hint"])

    with st.form("finrec_answer_form", clear_on_submit=False, border=False):
        ans = st.text_input("Amount", key=f"finrec_answer_{i}",
                            placeholder="e.g., 265.10 or $265.10",
                            label_visibility="collapsed")
        submitted = st.form_submit_button("✅ Submit")

    if submitted and not st.session_state.finrec_submitted:
        user_val = parse_money(ans)
        if math.isnan(user_val):
            st.error("Please type a valid number (you can include the $ sign).")
        else:
            correct = meta["answer"]
            if abs(user_val - correct) < 0.01:
                st.success(f"Correct! **{fmt_money(correct)}**")
            else:
                st.error(f"Not quite. You entered **{fmt_money(user_val)}**.")
                with st.expander("📘 See step-by-step solution", expanded=True):
                    st.markdown(render_steps(meta))
                    st.markdown(f"**Answer:** {fmt_money(correct)}")
            st.session_state.finrec_submitted = True

    # navigation
    nc1, nc2, nc3 = st.columns([1,1,1])
    with nc1:
        if st.button("◀️ Previous", use_container_width=True, disabled=(i==0)):
            st.session_state.finrec_idx -= 1
            st.session_state.finrec_submitted = False
            st.rerun()
    with nc2:
        if st.button("Next ▶️", use_container_width=True, disabled=(i==n-1)):
            st.session_state.finrec_idx += 1
            st.session_state.finrec_submitted = False
            st.rerun()
    with nc3:
        if st.button("New Question", use_container_width=True):
            st.session_state.finrec_set[i] = generate_ledger(st.session_state.finrec_difficulty)
            st.session_state.finrec_submitted = False
            key = f"finrec_answer_{i}"
            if key in st.session_state: del st.session_state[key]
            st.rerun()

# Standalone
if __name__ == "__main__":
    run()
