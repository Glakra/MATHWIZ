import random
import streamlit as st
import streamlit.components.v1 as components

# --------------------------- Helpers ---------------------------

def money(lo: int, hi: int) -> float:
    """Random money with $0.05 steps."""
    cents = random.choice([0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95])
    return round(random.randint(lo, hi) + cents/100, 2)

def fmt(x: float) -> str:
    return f"${x:,.2f}"

MALE = {
    "Liam","Noah","Oliver","Elijah","James","Lucas","Mason","Ethan","Jacob","Aiden",
    "Logan","Jackson","Levi","Leo","Wyatt","Carter","Henry","Owen","Ryan","David",
    "Kevin","Tyler","Jordan","Ben","Tom","Alex","Daniel"
}
NAMES = [
    "Ava","Olivia","Emma","Sophia","Isabella","Mia","Amelia","Harper","Evelyn","Abigail",
    "Liam","Noah","Oliver","Elijah","James","Lucas","Mason","Ethan","Jacob","Aiden",
    "Logan","Jackson","Levi","Leo","Wyatt","Carter","Henry","Owen","Ryan","David",
    "Kevin","Tyler","Jordan","Ben","Tom","Alex","Daniel"
]
MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

INCOME_ACTS = [
    "walking dogs","mowing lawns","tutoring","babysitting","car-wash","yard work",
    "lemonade stand","selling old games","delivering newspapers","teaching a lesson"
]
EXPENSE_ACTS = [
    "movie night with friends","sports gear","phone plan","new shoes","snacks",
    "school trip","book fair","video game","water park","donation to a charity",
    "gym pass","art supplies","concert ticket","birthday gift","haircut"
]

def he_she(name:str)->str:  return "he" if name in MALE else "she"
def his_her(name:str)->str: return "his" if name in MALE else "her"

# ---------------------- Scenario generation --------------------

def _unique_distractors(base_set, k):
    """Utility to sample k unique items not equal to base_set[0]."""
    items = list(set(base_set))
    random.shuffle(items)
    return items[:k]

def generate_record(level:int):
    """Create one budget table + MCQ."""
    name  = random.choice(NAMES)
    month = random.choice(MONTHS)

    if level == 1:
        inc_n, exp_n = 3, 3; lo, hi = 8, 45
    elif level == 2:
        inc_n, exp_n = 3, 3; lo, hi = 10, 120
    else:
        inc_n, exp_n = 4, 4; lo, hi = 15, 180

    # ensure not already balanced
    for _ in range(200):
        incomes  = [(random.choice(INCOME_ACTS),  money(lo, hi)) for _ in range(inc_n)]
        expenses = [(random.choice(EXPENSE_ACTS), money(lo, hi)) for _ in range(exp_n)]
        total_inc = round(sum(v for _,v in incomes), 2)
        total_exp = round(sum(v for _,v in expenses), 2)
        diff = round(abs(total_inc - total_exp), 2)
        if diff >= 0.25:  # avoid trivially balanced or pennies off due to rounding
            break

    need = "increase income" if total_inc < total_exp else "decrease expenses"
    pron = he_she(name)

    # --- Correct option
    if need == "increase income":
        correct = f"{pron.capitalize()} could earn an extra {fmt(diff)} by {random.choice(INCOME_ACTS)}"
        correct_effect = ("income", +diff)
    else:
        item = random.choice(expenses)[0]
        correct = f"{pron.capitalize()} could decrease spending on {item} by {fmt(diff)}"
        correct_effect = ("expense", -diff)

    # --- Distractors
    # amount near diff but not equal & positive
    offsets = [x/2 for x in _unique_distractors([-10,-5,-2,-1,1,2,5,10], 3)]
    wrong_amounts = [max(0.05, round(diff + d, 2)) for d in offsets]

    dists = []
    # same direction, wrong amount
    if need == "increase income":
        dists.append(f"{pron.capitalize()} could earn an extra {fmt(wrong_amounts[0])} by {random.choice(INCOME_ACTS)}")
    else:
        dists.append(f"{pron.capitalize()} could decrease spending on {random.choice(EXPENSE_ACTS)} by {fmt(wrong_amounts[0])}")

    # wrong direction (makes it worse)
    if need == "increase income":
        dists.append(f"{pron.capitalize()} could spend {fmt(wrong_amounts[1])} more on {random.choice(EXPENSE_ACTS)}")
    else:
        dists.append(f"{pron.capitalize()} could earn {fmt(wrong_amounts[1])} less from {random.choice(INCOME_ACTS)}")

    # change the other side by the exact diff but wrong direction/excuse text
    if need == "increase income":
        dists.append(f"{pron.capitalize()} could decrease spending by {fmt(diff)} on {random.choice(EXPENSE_ACTS)} (this doesn’t increase income)")
    else:
        dists.append(f"{pron.capitalize()} could earn an extra {fmt(diff)} by {random.choice(INCOME_ACTS)} (this doesn’t decrease expenses)")

    options = [correct] + dists
    random.shuffle(options)
    correct_index = options.index(correct)

    return {
        "name": name, "month": month,
        "incomes": incomes, "expenses": expenses,
        "total_inc": total_inc, "total_exp": total_exp,
        "diff": diff, "need": need,
        "options": options, "correct_index": correct_index,
        "correct_effect": correct_effect
    }

# --------------------- HTML for the table ----------------------

def budget_table_html(name, month, incomes, expenses, total_inc, total_exp, theme="#159947"):
    rows = max(len(incomes), len(expenses))
    inc_cells = incomes + [("", "")] * (rows - len(incomes))
    exp_cells = expenses + [("", "")] * (rows - len(expenses))

    head = f"""
    <div style="border:1px solid #e6e6e6;border-radius:10px;overflow:hidden;font-family:Inter, system-ui, -apple-system, Segoe UI, Roboto;">
      <div style="background:{theme};color:white;padding:10px 12px;font-weight:700;">
        {name}'s {month} budget
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:15px;">
        <thead>
          <tr>
            <th style="width:50%;padding:10px;border-bottom:1px solid #eee;background:#f7fbf9;text-align:left">Income</th>
            <th style="width:50%;padding:10px;border-bottom:1px solid #eee;background:#f7fbf9;text-align:left">Expenses</th>
          </tr>
        </thead>
        <tbody>
    """
    body = ""
    for i in range(rows):
        l = inc_cells[i][0]; lv = inc_cells[i][1]
        r = exp_cells[i][0]; rv = exp_cells[i][1]
        lv_txt = "" if lv=="" else fmt(lv)
        rv_txt = "" if rv=="" else fmt(rv)
        body += f"""
          <tr>
            <td style="padding:8px 12px;border-bottom:1px solid #f0f0f0;">{(l + (': ' + lv_txt if l else '')) or '&nbsp;'}</td>
            <td style="padding:8px 12px;border-bottom:1px solid #f0f0f0;">{(r + (': ' + rv_txt if r else '')) or '&nbsp;'}</td>
          </tr>
        """

    foot = f"""
        </tbody>
        <tfoot>
          <tr>
            <td style="padding:10px 12px;background:#fafafa;border-top:1px solid #eee;"><b>Total:</b> {fmt(total_inc)}</td>
            <td style="padding:10px 12px;background:#fafafa;border-top:1px solid #eee;"><b>Total:</b> {fmt(total_exp)}</td>
          </tr>
        </tfoot>
      </table>
    </div>
    """
    return head + body + foot

def table_height(rows:int)->int:
    # header(44) + rows*40 + footer(44) + padding
    return int(44 + rows*40 + 54)

# ---------------------------- Main ------------------------------

def run():
    # session state
    if "adj_difficulty" not in st.session_state: st.session_state.adj_difficulty = 1
    if "adj_problem"   not in st.session_state: st.session_state.adj_problem   = None
    if "adj_choice"    not in st.session_state: st.session_state.adj_choice    = None
    if "adj_submitted" not in st.session_state: st.session_state.adj_submitted = False
    if "adj_stats"     not in st.session_state: st.session_state.adj_stats     = {"attempted":0,"correct":0}

    st.markdown("**📚 Year 5 > Financial Literacy**")
    st.title("🧮 Adjust a Budget")
    st.caption("Choose the change that would balance the budget (income = expenses).")

    c1,c2,c3 = st.columns([1,1,1])
    with c1:
        level_name = st.selectbox("Difficulty", ["Intro","Core","Challenge"],
                                  index=st.session_state.adj_difficulty-1)
        st.session_state.adj_difficulty = {"Intro":1,"Core":2,"Challenge":3}[level_name]
    with c2:
        if st.button("🆕 New Record", use_container_width=True):
            st.session_state.adj_problem = None
            st.session_state.adj_choice = None
            st.session_state.adj_submitted = False
            st.rerun()
    with c3:
        if st.button("← Back", use_container_width=True):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

    # generate problem
    if st.session_state.adj_problem is None:
        st.session_state.adj_problem = generate_record(st.session_state.adj_difficulty)

    P = st.session_state.adj_problem

    # render budget table with components.html (prevents HTML from showing as text)
    theme = {1:"#159947", 2:"#0a84d0", 3:"#f59f00"}[st.session_state.adj_difficulty]
    rows = max(len(P["incomes"]), len(P["expenses"]))
    html = budget_table_html(
        P["name"], P["month"], P["incomes"], P["expenses"], P["total_inc"], P["total_exp"], theme
    )
    components.html(html, height=table_height(rows), scrolling=False)

    st.markdown(f"**What could {P['name']} do to balance {his_her(P['name'])} budget?**")

    with st.expander("💡 Hint", expanded=False):
        st.write(
            f"Current totals → Income **{fmt(P['total_inc'])}**, Expenses **{fmt(P['total_exp'])}**. "
            f"The difference is **{fmt(P['diff'])}**. To balance, either "
            f"increase income by {fmt(P['diff'])} or decrease expenses by {fmt(P['diff'])}."
        )

    # one radio with all options (fixes 'index must be between 0 and length' issue)
    default_idx = 0 if st.session_state.adj_choice is None else st.session_state.adj_choice
    choice_text = st.radio("Choose one:", P["options"], index=default_idx)
    st.session_state.adj_choice = P["options"].index(choice_text)

    # Submit
    colA, colB = st.columns([1,2])
    with colA:
        if st.button("✅ Submit", use_container_width=True, disabled=st.session_state.adj_submitted):
            st.session_state.adj_submitted = True
            st.session_state.adj_stats["attempted"] += 1
            if st.session_state.adj_choice == P["correct_index"]:
                st.session_state.adj_stats["correct"] += 1

    if st.session_state.adj_submitted:
        if st.session_state.adj_choice == P["correct_index"]:
            st.success("Great job — that adjustment balances the budget!")
        else:
            st.error("Not quite. See the explanation below and try another one!")

        with st.expander("📖 See the step-by-step explanation", expanded=True):
            inc, exp, d = P["total_inc"], P["total_exp"], P["diff"]
            need = P["need"]
            st.markdown(
                f"- Current totals: **Income {fmt(inc)}**, **Expenses {fmt(exp)}**  \n"
                f"- Difference: **{fmt(d)}** → you must **{need} by {fmt(d)}**.  \n"
                f"- Your choice: _{P['options'][st.session_state.adj_choice]}_  \n"
            )
            side, delta = P["correct_effect"]
            if side == "income":
                st.markdown(f"✔️ If {P['name']} earns **{fmt(d)}** more, income becomes **{fmt(inc + d)}**, matching expenses (**{fmt(exp)}**).")
            else:
                st.markdown(f"✔️ If {P['name']} spends **{fmt(d)}** less, expenses become **{fmt(exp - d)}**, matching income (**{fmt(inc)}**).")

        acc = 0 if st.session_state.adj_stats["attempted"]==0 else \
            100*st.session_state.adj_stats["correct"]/st.session_state.adj_stats["attempted"]
        st.metric("Accuracy", f"{acc:.0f}%")

        if st.button("➡️ Next Question", use_container_width=True):
            st.session_state.adj_problem = None
            st.session_state.adj_choice = None
            st.session_state.adj_submitted = False
            st.rerun()
