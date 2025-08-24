# Grades/Year 5/X. Geometric measurement/use_area_perimeter_to_determine_cost.py
import streamlit as st
import random

# ----------------------------- Utilities ---------------------------------- #
def money(x: float) -> str:
    if abs(x - round(x)) < 1e-9:
        return f"${int(round(x))}"
    return f"${x:,.2f}"

def parse_number(txt: str) -> float | None:
    if txt is None:
        return None
    try:
        cleaned = txt.replace("$", "").replace(",", "").strip()
        if cleaned == "":
            return None
        return float(cleaned)
    except Exception:
        return None

def inc_accuracy(correct: bool):
    st.session_state.total_attempted += 1
    if correct:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        if st.session_state.difficulty < 4 and st.session_state.consecutive_correct >= 3:
            st.session_state.difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        if st.session_state.difficulty > 1 and st.session_state.consecutive_wrong >= 2:
            st.session_state.difficulty -= 1
            st.session_state.consecutive_wrong = 0

# --------------------------- Problem builder ------------------------------- #
def random_rate(min_rate, max_rate, step=1):
    r = random.randrange(int(min_rate), int(max_rate) + 1, step)
    return float(r)

def build_problem(difficulty: int) -> dict:
    unit = "metres" if difficulty >= 2 else random.choice(["metres", "centimetres"])
    if unit == "metres":
        small, large = (2, 10) if difficulty == 1 else (3, 15) if difficulty == 2 else (4, 20) if difficulty == 3 else (6, 25)
    else:
        small, large = (20, 80) if difficulty == 1 else (30, 120) if difficulty == 2 else (40, 160) if difficulty == 3 else (50, 200)

    scenario = random.choice([
        "fence_garden", "frame_poster", "rope_court",
        "carpet_room", "tile_patio", "paint_wall"
    ])

    rate_per_m  = random_rate(3, 20)       # $/m
    rate_per_sm = random_rate(12, 60, 2)   # $/m²

    if scenario in {"fence_garden", "rope_court", "carpet_room", "tile_patio"}:
        L = random.randint(small+1, large)
        W = random.randint(small, L-1)
    elif scenario == "paint_wall":
        L = random.randint(small, large)   # width
        W = random.randint(small, large)   # height
    else:
        L = random.randint(small, large)
        W = random.randint(small, large)

    unit_singular = "metre" if unit == "metres" else "centimetre"

    if scenario == "fence_garden":
        rate = rate_per_m
        P = 2 * (L + W)
        cost = P * rate
        text = (
            f"A rectangular garden is {L} {unit} long and {W} {unit} wide. "
            f"Fencing costs {money(rate)} per {unit_singular}. "
            f"How much will it cost to fence around the garden?"
        )
        hint = [
            "This is a **perimeter** problem.",
            f"Perimeter of a rectangle: **P = 2 × (L + W)**.",
            f"Cost = P × {money(rate)} per {unit_singular}."
        ]
        steps = [
            f"Compute perimeter: P = 2 × ({L} + {W}) = 2 × {L+W} = **{P} {unit}**.",
            f"Multiply by rate: Cost = {P} × {money(rate)} = **{money(cost)}**."
        ]
        rate_unit = "per metre" if unit == "metres" else "per centimetre"

    elif scenario == "rope_court":
        rate = rate_per_m
        P = 2 * (L + W)
        cost = P * rate
        text = (
            f"A beach volleyball court is {W} {unit} wide and {L} {unit} long. "
            f"Rope for the boundary costs {money(rate)} per {unit_singular}. "
            f"What will a new boundary line cost?"
        )
        hint = [
            "Boundary line goes **around** the court → perimeter.",
            f"P = 2 × ({L} + {W}). Then multiply by {money(rate)}."
        ]
        steps = [
            f"P = 2 × ({L}+{W}) = 2×{L+W} = **{2*(L+W)} {unit}**.",
            f"Cost = {2*(L+W)} × {money(rate)} = **{money(cost)}**."
        ]
        rate_unit = "per metre" if unit == "metres" else "per centimetre"

    elif scenario == "frame_poster":
        rate = rate_per_m
        P = 2 * (L + W)
        cost = P * rate
        text = (
            f"A rectangular portrait is {W} {unit} wide and {L} {unit} high. "
            f"A gold frame costs {money(rate)} per {unit_singular}. "
            f"How much will the frame cost?"
        )
        hint = [
            "A frame goes around the edge → use **perimeter**.",
            f"P = 2×(L+W) and cost = P × {money(rate)}."
        ]
        steps = [
            f"P = 2×({L}+{W}) = 2×{L+W} = **{2*(L+W)} {unit}**.",
            f"Cost = {2*(L+W)} × {money(rate)} = **{money(cost)}**."
        ]
        rate_unit = "per metre" if unit == "metres" else "per centimetre"

    elif scenario == "carpet_room":
        rate = rate_per_sm
        A = L * W
        cost = A * rate
        text = (
            f"A rectangular room is {L} {unit} long and {W} {unit} wide. "
            f"Carpet costs {money(rate)} per square {unit_singular}. "
            f"How much will enough carpet cost to cover the floor?"
        )
        hint = [
            "Floor covering uses **area**.",
            "Area of a rectangle: **A = L × W**.",
            f"Cost = A × {money(rate)} per square {unit_singular}."
        ]
        steps = [
            f"A = {L} × {W} = **{A} square {unit}**.",
            f"Cost = {A} × {money(rate)} = **{money(cost)}**."
        ]
        rate_unit = "per square metre" if unit == "metres" else "per square centimetre"

    elif scenario == "tile_patio":
        rate = rate_per_sm
        A = L * W
        cost = A * rate
        text = (
            f"A patio measures {L} by {W} {unit}. "
            f"Tiles cost {money(rate)} per square {unit_singular}. "
            f"What is the cost to tile the whole patio?"
        )
        hint = [
            "Tiling covers the surface → **area**.",
            f"A = L × W; then multiply by {money(rate)}."
        ]
        steps = [
            f"A = {L} × {W} = **{A} square {unit}**.",
            f"Cost = {A} × {money(rate)} = **{money(cost)}**."
        ]
        rate_unit = "per square metre" if unit == "metres" else "per square centimetre"

    else:  # paint_wall
        rate = rate_per_sm
        A = L * W
        cost = A * rate
        text = (
            f"A wall is {L} {unit} wide and {W} {unit} high. "
            f"Paint covers the wall at {money(rate)} per square {unit_singular}. "
            f"How much will it cost to paint the wall?"
        )
        hint = [
            "Painting a wall uses **area**.",
            "A = width × height.",
            f"Multiply by {money(rate)} to get the cost."
        ]
        steps = [
            f"A = {L} × {W} = **{A} square {unit}**.",
            f"Cost = {A} × {money(rate)} = **{money(cost)}**."
        ]
        rate_unit = "per square metre" if unit == "metres" else "per square centimetre"

    return {
        "text": text,
        "unit": unit,
        "rate_unit": rate_unit,
        "answer": round(cost, 2),
        "hint_lines": hint,
        "steps": steps
    }

# ------------------------------ UI logic ----------------------------------- #
def new_problem():
    st.session_state.current_problem = build_problem(st.session_state.difficulty)
    st.session_state.answer_submitted = False
    st.session_state.show_feedback = False
    if "cost_answer" in st.session_state:
        del st.session_state["cost_answer"]

def run():
    st.markdown("**📚 Year 5 > X. Geometric measurement**")
    st.title("💵 Use Area and Perimeter to Determine Cost")
    st.caption("Find the cost of fencing, framing, carpeting, tiling, or painting by using area or perimeter.")

    # ---- session state init
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = 1
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False
    if "show_feedback" not in st.session_state:
        st.session_state.show_feedback = False
    if "consecutive_correct" not in st.session_state:
        st.session_state.consecutive_correct = 0
    if "consecutive_wrong" not in st.session_state:
        st.session_state.consecutive_wrong = 0
    if "total_attempted" not in st.session_state:
        st.session_state.total_attempted = 0
    if "total_correct" not in st.session_state:
        st.session_state.total_correct = 0

    # ---- header widgets (now includes Back)
    cols = st.columns([2, 1, 1, 1])
    with cols[0]:
        names = {1:"Intro", 2:"Developing", 3:"Secure", 4:"Mastery"}
        st.write(f"**Difficulty:** {names[st.session_state.difficulty]}")
        st.progress(st.session_state.difficulty/4)
    with cols[1]:
        if st.session_state.total_attempted > 0:
            acc = 100*st.session_state.total_correct/max(1, st.session_state.total_attempted)
            st.metric("Accuracy", f"{acc:.0f}%")
        else:
            st.metric("Accuracy", "—")
    with cols[2]:
        if st.button("↻ New set", use_container_width=True):
            st.session_state.total_attempted = 0
            st.session_state.total_correct = 0
            st.session_state.consecutive_correct = 0
            st.session_state.consecutive_wrong = 0
            st.session_state.current_problem = None
            if "cost_answer" in st.session_state:
                del st.session_state["cost_answer"]
            st.rerun()
    with cols[3]:
        if st.button("← Back", use_container_width=True):
            # Navigate back to curriculum by clearing the 'subtopic' query param (same pattern as other pages)
            try:
                if "subtopic" in st.query_params:
                    del st.query_params["subtopic"]
            except Exception:
                pass
            st.rerun()

    # ---- problem
    if st.session_state.current_problem is None:
        new_problem()

    prob = st.session_state.current_problem
    st.markdown("### Question:")
    st.write(prob["text"])

    with st.expander("💡 Hint", expanded=False):
        for line in prob["hint_lines"]:
            st.write("• " + line)

    st.markdown("---")

    with st.form("answer_form", clear_on_submit=False):
        left, mid = st.columns([2, 3])
        with left:
            st.text_input("Your answer (enter the **total cost**)", key="cost_answer",
                          value=st.session_state.get("cost_answer", ""))
        with mid:
            st.caption(f"Units: currency ({prob['rate_unit']})")
        submitted = st.form_submit_button("✅ Submit", use_container_width=True, disabled=st.session_state.answer_submitted)

    if submitted and not st.session_state.answer_submitted:
        val = parse_number(st.session_state.get("cost_answer"))
        if val is None:
            st.warning("Please enter a number (you can include a $ sign).")
        else:
            correct = abs(val - prob["answer"]) < 0.01
            inc_accuracy(correct)
            st.session_state.answer_submitted = True
            st.session_state.show_feedback = True
            st.session_state.correct = correct

    if st.session_state.show_feedback:
        if st.session_state.correct:
            st.success(f"Correct! The cost is **{money(prob['answer'])}**.")
            if st.session_state.consecutive_correct == 2:
                st.info("🔥 Great streak! One more correct answer to level up.")
        else:
            st.error(f"Not quite. The correct cost is **{money(prob['answer'])}**.")
            with st.expander("📘 Step-by-step solution", expanded=True):
                for step in prob["steps"]:
                    st.write(step)

    if st.session_state.answer_submitted:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("➡️ Next Question", use_container_width=True):
                new_problem()
                st.rerun()

if __name__ == "__main__":
    run()
