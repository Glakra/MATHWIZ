# area_perimeter_word_problems.py
import streamlit as st
import random
import math

# ----------------------------
# Helpers
# ----------------------------
def safe_rerun():
    """Use st.rerun() on modern Streamlit; fall back if needed."""
    try:
        st.rerun()
    except Exception:
        # Older Streamlit versions
        try:
            st.experimental_rerun()  # type: ignore[attr-defined]
        except Exception:
            pass

def unit_word(u: str, square=False):
    names = {"mm": "millimetres", "cm": "centimetres", "m": "metres", "km": "kilometres"}
    base = names.get(u, u)
    return f"square {base}" if square else base

def fmt(x):
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.2f}".rstrip("0").rstrip(".")

def area_rect(L, W): return L * W
def perim_rect(L, W): return 2 * (L + W)
def choose_units(): return random.choice(["cm", "m"])

def correct_num(user_val, answer, tol=0.01):
    try:
        return abs(float(user_val) - float(answer)) <= tol
    except Exception:
        return False

# ----------------------------
# Problem generators
# ----------------------------
def prob_area_rectangle_simple():
    u = choose_units()
    L = random.randint(5, 14)
    W = random.randint(3, 11)
    A = area_rect(L, W)
    q = f"A garden bed is {L} {unit_word(u)} long and {W} {unit_word(u)} wide. What is its area?"
    steps = [
        "Area of a rectangle = **length × width**.",
        f"{L} × {W} = **{A} {unit_word(u, square=True)}**."
    ]
    return {"format":"numeric","question":q,"answer":A,"answer_unit":unit_word(u, square=True),
            "hint":"Multiply length by width.","steps":steps}

def prob_area_square_simple():
    u = choose_units()
    s = random.randint(4, 12)
    A = s*s
    q = f"A square poster has side {s} {unit_word(u)}. What is its area?"
    steps = ["Area of a square = **side × side**.", f"{s} × {s} = **{A} {unit_word(u, square=True)}**."]
    return {"format":"numeric","question":q,"answer":A,"answer_unit":unit_word(u, square=True),
            "hint":"Square = side².","steps":steps}

def prob_perimeter_rectangle_simple():
    u = choose_units()
    L = random.randint(4, 15)
    W = random.randint(3, 12)
    P = perim_rect(L, W)
    q = f"A garden bed is {L} {unit_word(u)} long and {W} {unit_word(u)} wide. What is its perimeter?"
    steps = [
        "Perimeter of a rectangle = **2 × (length + width)**.",
        f"2 × ({L} + {W}) = 2 × {L+W} = **{P} {unit_word(u)}**."
    ]
    return {"format":"numeric","question":q,"answer":P,"answer_unit":unit_word(u),
            "hint":"Add all four sides, or use 2(L+W).","steps":steps}

def prob_missing_side_from_area():
    u = choose_units()
    W = random.randint(3, 12)
    L = random.randint(6, 18)
    A = area_rect(L, W)
    q = f"A rectangle has area {A} {unit_word(u, square=True)} and width {W} {unit_word(u)}. Find its length."
    steps = ["Area = L × W → L = Area ÷ W.",
             f"{A} ÷ {W} = **{fmt(A/W)} {unit_word(u)}**."]
    return {"format":"numeric","question":q,"answer":A/W,"answer_unit":unit_word(u),
            "hint":"Length = Area ÷ Width.","steps":steps}

def prob_missing_side_from_perimeter():
    u = choose_units()
    L = random.randint(6, 16)
    W = random.randint(3, 10)
    P = perim_rect(L, W)
    ask_width = random.choice([True, False])
    if ask_width:
        q = f"A rectangle has perimeter {P} {unit_word(u)} and length {L} {unit_word(u)}. What is its width?"
        ans = P/2 - L
        steps = ["P = 2(L+W) → P/2 = L + W → W = P/2 − L.",
                 f"{P/2} − {L} = **{fmt(ans)} {unit_word(u)}**."]
    else:
        q = f"A rectangle has perimeter {P} {unit_word(u)} and width {W} {unit_word(u)}. What is its length?"
        ans = P/2 - W
        steps = ["P = 2(L+W) → P/2 = L + W → L = P/2 − W.",
                 f"{P/2} − {W} = **{fmt(ans)} {unit_word(u)}**."]
    return {"format":"numeric","question":q,"answer":ans,"answer_unit":unit_word(u),
            "hint":"Use P = 2(L+W).","steps":steps}

def prob_cost_fencing():
    u = choose_units()
    L = random.randint(8, 20)
    W = random.randint(4, 12)
    rate = random.choice([5, 7, 10, 12])
    P = perim_rect(L, W)
    cost = P * rate
    q = (f"A rectangular paddock is {L} {unit_word(u)} by {W} {unit_word(u)}. "
         f"Fencing costs ${rate} per {unit_word(u)}. What is the total cost?")
    steps = [f"Perimeter = 2({L}+{W}) = **{P} {unit_word(u)}**.",
             f"Cost = P × rate = {P} × {rate} = **${fmt(cost)}**."]
    return {"format":"numeric","question":q,"answer":cost,"answer_unit":"dollars",
            "hint":"Cost = (perimeter) × (rate per unit).","steps":steps}

def prob_tiles_needed():
    u = choose_units()
    side = random.randint(2, 5)
    L = random.randint(6, 12) * side
    W = random.randint(4, 10) * side
    A_floor = area_rect(L, W)
    A_tile = side*side
    n = A_floor // A_tile
    q = (f"A floor is {L}×{W} {unit_word(u)}. Square tiles are {side} {unit_word(u)} on a side. "
         f"How many tiles are needed (no cutting)?")
    steps = [f"Floor area = {L}×{W} = {A_floor} {unit_word(u, square=True)}.",
             f"Tile area = {side}×{side} = {A_tile} {unit_word(u, square=True)}.",
             f"Tiles = {A_floor} ÷ {A_tile} = **{fmt(n)}**."]
    return {"format":"numeric","question":q,"answer":n,"answer_unit":"tiles",
            "hint":"Tiles = floor area ÷ tile area.","steps":steps}

def prob_compare_areas_mcq():
    u = choose_units()
    L1,W1 = random.randint(4,12), random.randint(3,11)
    L2,W2 = random.randint(4,12), random.randint(3,11)
    A1,A2 = area_rect(L1,W1), area_rect(L2,W2)
    correct = "Rectangle A" if A1>A2 else "Rectangle B" if A2>A1 else "They have the same area"
    q = (f"Two rectangles:\n\n"
         f"- **A**: {L1}×{W1} {unit_word(u)}\n"
         f"- **B**: {L2}×{W2} {unit_word(u)}\n\n"
         f"Which has the **greater area**?")
    steps = [f"A: {L1}×{W1} = {A1}", f"B: {L2}×{W2} = {A2}", f"Answer: **{correct}**."]
    return {"format":"mcq","question":q,"choices":["Rectangle A","Rectangle B","They have the same area"],
            "answer":correct,"hint":"Compute both areas and compare.","steps":steps}

def prob_walkway_border_area():
    u = choose_units()
    outer_L = random.randint(12, 20)
    outer_W = random.randint(8, 16)
    t = random.randint(1, 3)
    inner_L = max(outer_L - 2*t, 1)
    inner_W = max(outer_W - 2*t, 1)
    border = area_rect(outer_L, outer_W) - area_rect(inner_L, inner_W)
    q = (f"A {outer_L}×{outer_W} {unit_word(u)} garden has a walkway {t} {unit_word(u)} wide "
         f"**around the inside edge**. What is the area of the walkway?")
    steps = [
        "Walkway area = outer area − inner area.",
        f"Outer: {outer_L}×{outer_W} = {area_rect(outer_L, outer_W)}.",
        f"Inner: {inner_L}×{inner_W} = {area_rect(inner_L, inner_W)}.",
        f"Difference = **{border} {unit_word(u, square=True)}**."
    ]
    return {"format":"numeric","question":q,"answer":border,"answer_unit":unit_word(u, square=True),
            "hint":"Big rectangle minus small rectangle.","steps":steps}

def prob_L_shape_area_perimeter():
    u = choose_units()
    a,b = random.randint(10,18), random.randint(8,14)        # big rectangle
    c,d = random.randint(3, a-4), random.randint(3, b-4)     # cutout at top-right
    A = area_rect(a,b) - area_rect(c,d)
    # perimeter by tracing axis-aligned polygon
    verts = [(0,0),(a,0),(a,b-d),(a-c,b-d),(a-c,b),(0,b)]
    P = 0
    for i in range(len(verts)):
        x1,y1 = verts[i]; x2,y2 = verts[(i+1)%len(verts)]
        P += abs(x2-x1) + abs(y2-y1)
    q = (f"An L-shaped patio is made by removing a {c}×{d} {unit_word(u)} rectangle from the "
         f"**top-right corner** of a {a}×{b} {unit_word(u)} rectangle. "
         f"Find **both** the area and the perimeter of the L-shape.")
    steps = [
        "Area = big − small.",
        f"({a}×{b}) − ({c}×{d}) = {a*b} − {c*d} = **{A} {unit_word(u, square=True)}**.",
        "Perimeter: add the lengths of all **outside** edges.",
        f"P = {a} + {b-d} + {c} + {d} + {a-c} + {b} = **{P} {unit_word(u)}**."
    ]
    return {"format":"multi","question":q,
            "answers":{"area":A,"perimeter":P},
            "units":{"area":unit_word(u, square=True),"perimeter":unit_word(u)},
            "hint":"Area: big − small. Perimeter: walk the outer edge.",
            "steps":steps}

def prob_scale_change_mcq():
    u = choose_units()
    L,W = random.randint(3,8), random.randint(2,7)
    change = random.choice(["double length","double width","double both"])
    if change == "double both":
        prompt = f"A rectangle is {L}×{W} {unit_word(u)}. If you **double both length and width**, what happens?"
        choices = ["Perimeter doubles; area quadruples","Area doubles; perimeter stays the same",
                   "Both area and perimeter double","Both stay the same"]
        steps = ["Double both dimensions.","Area scales by 2×2 = **4**.","Perimeter doubles."]
        correct = "Perimeter doubles; area quadruples"
    else:
        prompt = f"A rectangle is {L}×{W} {unit_word(u)}. If you **{change} only**, what happens?"
        choices = ["Area doubles; perimeter increases (but does not double)",
                   "Perimeter doubles; area stays the same",
                   "Both area and perimeter double","Both stay the same"]
        steps = ["Area = L×W: doubling one side ⇒ **area doubles**.",
                 "Perimeter = 2(L+W): the sum increases, but not by a factor of 2, so perimeter **does not double**."]
        correct = "Area doubles; perimeter increases (but does not double)"
    return {"format":"mcq","question":prompt,"choices":choices,"answer":correct,
            "hint":"Consider how L×W and 2(L+W) change.","steps":steps}

POOLS = {
    1: [prob_area_rectangle_simple, prob_area_square_simple, prob_perimeter_rectangle_simple, prob_compare_areas_mcq],
    2: [prob_missing_side_from_area, prob_missing_side_from_perimeter, prob_cost_fencing, prob_tiles_needed, prob_compare_areas_mcq],
    3: [prob_walkway_border_area, prob_L_shape_area_perimeter, prob_cost_fencing, prob_tiles_needed, prob_scale_change_mcq],
    4: [prob_L_shape_area_perimeter, prob_walkway_border_area, prob_scale_change_mcq, prob_missing_side_from_perimeter, prob_missing_side_from_area]
}

# ----------------------------
# State
# ----------------------------
def _init_state():
    if "ap_wp_difficulty" not in st.session_state:
        st.session_state.ap_wp_difficulty = 1
    if "ap_current" not in st.session_state:
        st.session_state.ap_current = None
        st.session_state.answer_submitted = False
        st.session_state.show_feedback = False
        st.session_state.streak = 0
        st.session_state.total = 0
        st.session_state.correct = 0
        st.session_state.show_hint = False
        st.session_state.ap_qid = 0  # unique id per question

def new_problem():
    diff = st.session_state.ap_wp_difficulty
    gen = random.choice(POOLS.get(diff, POOLS[1]))
    st.session_state.ap_current = gen()
    st.session_state.answer_submitted = False
    st.session_state.show_feedback = False
    st.session_state.show_hint = False
    st.session_state.ap_qid += 1  # bump id so widget keys change

def _keys():
    qid = st.session_state.ap_qid
    return {
        "ans":  f"ap_ans_{qid}",
        "ans2": f"ap_ans2_{qid}",
        "mcq":  f"ap_mcq_{qid}",
    }

# ----------------------------
# UI
# ----------------------------
def show_problem():
    prob = st.session_state.ap_current
    if not prob: return

    st.markdown("### Question:")
    st.markdown(prob["question"])

    # Hint
    c1, _, _ = st.columns([1,6,1])
    with c1:
        if st.button("💡 Hint", disabled=st.session_state.answer_submitted):
            st.session_state.show_hint = True
    if st.session_state.show_hint:
        st.info(prob["hint"])

    st.markdown("---")

    keys = _keys()

    # Inputs
    if prob["format"] == "numeric":
        c1, c2 = st.columns([2,3])
        with c1:
            st.text_input("Your answer:", key=keys["ans"], disabled=st.session_state.answer_submitted, placeholder="Type a number")
        with c2:
            st.write(f"Unit: **{prob['answer_unit']}**")

    elif prob["format"] == "multi":
        st.write("Enter both values:")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input(f"Area ({prob['units']['area']})", key=keys["ans"], disabled=st.session_state.answer_submitted, placeholder="e.g. 48")
        with c2:
            st.text_input(f"Perimeter ({prob['units']['perimeter']})", key=keys["ans2"], disabled=st.session_state.answer_submitted, placeholder="e.g. 28")

    else:  # mcq
        st.radio("Choose one:", prob["choices"], key=keys["mcq"], index=None, disabled=st.session_state.answer_submitted)

    # Submit
    center = st.columns([1,2,1])[1]
    with center:
        if st.button("✅ Submit", type="primary", disabled=st.session_state.answer_submitted):
            check_answer()
            safe_rerun()

    if st.session_state.show_feedback:
        show_feedback()

    if st.session_state.answer_submitted:
        center2 = st.columns([1,2,1])[1]
        with center2:
            if st.button("🔁 Next Question", type="secondary"):
                new_problem()
                safe_rerun()

def check_answer():
    prob = st.session_state.ap_current
    keys = _keys()
    st.session_state.total += 1

    # Read current values via dynamic keys
    ok = False
    if prob["format"] == "numeric":
        val = st.session_state.get(keys["ans"], "")
        ok = correct_num(val, prob["answer"])
    elif prob["format"] == "multi":
        val1 = st.session_state.get(keys["ans"], "")
        val2 = st.session_state.get(keys["ans2"], "")
        ok = correct_num(val1, prob["answers"]["area"]) and correct_num(val2, prob["answers"]["perimeter"])
    else:
        choice = st.session_state.get(keys["mcq"], None)
        ok = (choice == prob["answer"])

    st.session_state.answer_submitted = True
    st.session_state.show_feedback = True

    if ok:
        st.session_state.correct += 1
        st.session_state.streak += 1
        if st.session_state.streak >= 3 and st.session_state.ap_wp_difficulty < 4:
            st.session_state.ap_wp_difficulty += 1
            st.session_state.streak = 0
    else:
        st.session_state.streak = 0
        if st.session_state.total - st.session_state.correct >= 3 and st.session_state.ap_wp_difficulty > 1:
            st.session_state.ap_wp_difficulty -= 1

def show_feedback():
    prob = st.session_state.ap_current
    keys = _keys()

    if prob["format"] == "numeric":
        val = st.session_state.get(keys["ans"], "")
        if correct_num(val, prob["answer"]):
            st.success(f"Correct! ✅  **{fmt(prob['answer'])} {prob['answer_unit']}**")
        else:
            st.error(f"Not quite. The correct answer is **{fmt(prob['answer'])} {prob['answer_unit']}**.")
            with st.expander("See the step-by-step solution"):
                for s in prob["steps"]:
                    st.markdown(f"- {s}")

    elif prob["format"] == "multi":
        v1 = st.session_state.get(keys["ans"], "")
        v2 = st.session_state.get(keys["ans2"], "")
        ok_area = correct_num(v1, prob["answers"]["area"])
        ok_peri = correct_num(v2, prob["answers"]["perimeter"])
        if ok_area and ok_peri:
            st.success(
                f"Correct! ✅  Area = **{fmt(prob['answers']['area'])} {prob['units']['area']}**, "
                f"Perimeter = **{fmt(prob['answers']['perimeter'])} {prob['units']['perimeter']}**"
            )
        else:
            st.error(
                f"Not quite.\n\n- Area should be **{fmt(prob['answers']['area'])} {prob['units']['area']}**\n"
                f"- Perimeter should be **{fmt(prob['answers']['perimeter'])} {prob['units']['perimeter']}**"
            )
            with st.expander("See the step-by-step solution"):
                for s in prob["steps"]:
                    st.markdown(f"- {s}")

    else:  # mcq
        choice = st.session_state.get(keys["mcq"], None)
        if choice == prob["answer"]:
            st.success(f"Correct! ✅  **{prob['answer']}**")
        else:
            st.error(f"Not quite. The correct choice is **{prob['answer']}**.")
            with st.expander("Why? See the working"):
                for s in prob["steps"]:
                    st.markdown(f"- {s}")

# ----------------------------
# Entrypoint
# ----------------------------
def run():
    """
    Area & Perimeter: Word Problems
    - Adaptive difficulty
    - Hints + step-by-step solutions
    - Dynamic widget keys per question to avoid session state conflicts
    - Uses st.rerun() (with safe fallback) instead of deprecated experimental_rerun()
    """
    _init_state()

    st.markdown("**📚 Year 5 > X. Geometric measurement**")
    st.title("🧮 Area & Perimeter: Word Problems")
    st.markdown("*Solve real-world questions using area and perimeter.*")
    st.markdown("---")

    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        names = {1:"Intro",2:"Developing",3:"Confident",4:"Challenge"}
        st.markdown(f"**Difficulty:** {names[st.session_state.ap_wp_difficulty]}")
        st.progress(st.session_state.ap_wp_difficulty/4, text=f"Level {st.session_state.ap_wp_difficulty}/4")
    with c2:
        if st.session_state.total:
            acc = 100*st.session_state.correct/max(st.session_state.total,1)
            st.metric("Accuracy", f"{acc:.0f}%")
        else:
            st.metric("Accuracy", "—")
    with c3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

    if st.session_state.ap_current is None:
        new_problem()

    show_problem()

    with st.expander("📘 Quick Reference", expanded=False):
        st.markdown("""
        - **Rectangle:** Area = *L × W*, Perimeter = *2(L + W)*
        - **Square:** Area = *s²*, Perimeter = *4s*
        - **Composite L-shape:** Area = big − small; perimeter = sum of the **outer** edges
        - **Scaling both dimensions by 2:** Perimeter doubles; area **quadruples**
        """)
