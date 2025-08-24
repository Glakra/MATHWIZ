import streamlit as st
import streamlit.components.v1 as components
import random
import math

# --------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------

def unit_sq(u: str) -> str:
    # Return unit with squared exponent (cm², m², …)
    return {"mm": "mm²", "cm": "cm²", "m": "m²", "km": "km²"}.get(u, f"{u}²")

def unit_long(u: str) -> str:
    return {"mm":"millimetres", "cm":"centimetres", "m":"metres", "km":"kilometres"}.get(u, u)

def palette(level: int) -> str:
    return {
        1: "#BEE3F8",  # blue-100
        2: "#C6F6D5",  # green-100
        3: "#FED7E2",  # pink-100
        4: "#FEEBC8",  # orange-100
    }.get(level, "#E2E8F0")

def nfmt(x: float) -> str:
    return f"{int(x)}" if float(x).is_integer() else f"{x}"

# --------------------------------------------------------------------
# Problem builders
# Each returns a dict:
# {
#   "kind": "...",
#   "unit": "cm",
#   "svg": "<svg...>",
#   "prompt": "What is the area ...?",
#   "answer": number,
#   "meta": {...}  # for hints & steps
# }
# --------------------------------------------------------------------

def build_rectangle(unit: str, w: int, h: int, level: int):
    color = palette(level)
    svg = f"""
    <div style="text-align:center;margin:8px 0 18px;">
      <svg width="420" height="260" viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg">
        <rect x="80" y="60" width="260" height="140" fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <text x="210" y="50" font-size="14" font-weight="700" text-anchor="middle">{nfmt(w)} {unit}</text>
        <text x="350" y="140" font-size="14" font-weight="700">{nfmt(h)} {unit}</text>
      </svg>
    </div>
    """
    area = w * h
    return {
        "kind": "rectangle_area",
        "unit": unit,
        "svg": svg,
        "prompt": "What is the **area** of the rectangle?",
        "answer": area,
        "meta": {"w": w, "h": h}
    }

def build_square(unit: str, s: int, level: int):
    color = palette(level)
    svg = f"""
    <div style="text-align:center;margin:8px 0 18px;">
      <svg width="420" height="260" viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg">
        <rect x="120" y="60" width="180" height="180" fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <text x="210" y="50" font-size="14" font-weight="700" text-anchor="middle">{nfmt(s)} {unit}</text>
        <text x="320" y="150" font-size="14" font-weight="700">{nfmt(s)} {unit}</text>
      </svg>
    </div>
    """
    area = s * s
    return {
        "kind": "square_area",
        "unit": unit,
        "svg": svg,
        "prompt": "What is the **area** of the square?",
        "answer": area,
        "meta": {"s": s}
    }

def build_missing_side_rect(unit: str, w: int, h: int, reveal: str, level: int):
    # reveal ∈ {"w","h"} which side is given; the other is missing
    color = palette(level)
    show_w = f"{nfmt(w)} {unit}" if reveal == "w" else "?"
    show_h = f"{nfmt(h)} {unit}" if reveal == "h" else "?"
    svg = f"""
    <div style="text-align:center;margin:8px 0 18px;">
      <svg width="420" height="260" viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg">
        <rect x="80" y="60" width="260" height="140" fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <text x="210" y="50" font-size="14" font-weight="700" text-anchor="middle">{show_w}</text>
        <text x="350" y="140" font-size="14" font-weight="700">{show_h}</text>
      </svg>
    </div>
    """
    area = w * h
    missing_value = h if reveal == "w" else w
    return {
        "kind": "missing_side",
        "unit": unit,
        "svg": svg,
        "prompt": f"The **area** is **{nfmt(area)} {unit_sq(unit)}** and one side is shown. "
                  f"**What is the missing side length?**",
        "answer": missing_value,
        "meta": {"w": w, "h": h, "area": area, "missing": "height" if reveal == "w" else "width"}
    }

def build_frame_area(unit: str, W: int, H: int, w: int, h: int, level: int):
    # Outer (W×H) minus inner (w×h)
    color = palette(level)
    svg = f"""
    <div style="text-align:center;margin:8px 0 18px;">
      <svg width="420" height="280" viewBox="0 0 420 280" xmlns="http://www.w3.org/2000/svg">
        <rect x="60" y="40" width="300" height="200" fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <rect x="120" y="80" width="180" height="120" fill="#ffffff" stroke="#2D3748" stroke-width="2"/>
        <text x="210" y="34" font-size="13" font-weight="700" text-anchor="middle">outer: {nfmt(W)} {unit}</text>
        <text x="366" y="140" font-size="13" font-weight="700">outer: {nfmt(H)} {unit}</text>
        <text x="210" y="76" font-size="12" font-weight="700" text-anchor="middle">inner: {nfmt(w)} {unit}</text>
        <text x="306" y="140" font-size="12" font-weight="700">inner: {nfmt(h)} {unit}</text>
      </svg>
    </div>
    """
    area = W * H - w * h
    return {
        "kind": "frame",
        "unit": unit,
        "svg": svg,
        "prompt": "What is the **shaded (frame) area**?",
        "answer": area,
        "meta": {"W": W, "H": H, "w": w, "h": h}
    }

def build_L_composite(unit: str, a: int, b: int, c: int, d: int, level: int):
    # L shape as sum of two rectangles: A (a×b) and B (c×d)
    # Draw with a dashed guide to show natural split
    color = palette(level)
    svg = f"""
    <div style="text-align:center;margin:8px 0 18px;">
      <svg width="420" height="300" viewBox="0 0 420 300" xmlns="http://www.w3.org/2000/svg">
        <!-- L polygon -->
        <path d="M 80 40 L 250 40 L 250 120 L 340 120 L 340 240 L 80 240 Z"
              fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <!-- dashed guide -->
        <line x1="250" y1="120" x2="250" y2="240" stroke="#2D3748" stroke-width="2" stroke-dasharray="6,6"/>
        <text x="165" y="34" font-size="13" font-weight="700" text-anchor="middle">A: {nfmt(a)}×{nfmt(b)} {unit}</text>
        <text x="300" y="116" font-size="13" font-weight="700" text-anchor="middle">B: {nfmt(c)}×{nfmt(d)} {unit}</text>
      </svg>
    </div>
    """
    area = a * b + c * d
    return {
        "kind": "composite_L",
        "unit": unit,
        "svg": svg,
        "prompt": "This **L-shape** is made from two rectangles A and B. What is the **total area**?",
        "answer": area,
        "meta": {"a": a, "b": b, "c": c, "d": d}
    }

# --------------------------------------------------------------------
# Problem generation per difficulty
# --------------------------------------------------------------------

def make_problem(level: int):
    # side ranges and unit by difficulty
    if level == 1:
        lo, hi, unit = 2, 12, "cm"
        choice = random.choice(["rect","square"])
    elif level == 2:
        lo, hi, unit = 4, 20, "cm"
        choice = random.choice(["rect","square","missing"])
    elif level == 3:
        lo, hi, unit = 6, 25, "m"
        choice = random.choice(["rect","square","missing","frame"])
    else:
        lo, hi, unit = 8, 35, "m"
        choice = random.choice(["rect","missing","frame","composite"])

    r = lambda n=1: [random.randint(lo, hi) for _ in range(n)]

    if choice == "rect":
        w, h = r(2)
        return build_rectangle(unit, w, h, level)

    if choice == "square":
        s = random.randint(lo, hi)
        return build_square(unit, s, level)

    if choice == "missing":
        w, h = r(2)
        # randomly hide w or h, ensure integer answer
        reveal = random.choice(["w","h"])
        return build_missing_side_rect(unit, w, h, reveal, level)

    if choice == "frame":
        W, H = r(2)
        # inner must be smaller
        w = random.randint(max(1, W//4), max(2, W-1))
        h = random.randint(max(1, H//4), max(2, H-1))
        w = min(w, W-1); h = min(h, H-1)
        return build_frame_area(unit, W, H, w, h, level)

    # composite L
    a,b,c,d = r(4)
    return build_L_composite(unit, a,b,c,d, level)

# --------------------------------------------------------------------
# Hints & step-by-step
# --------------------------------------------------------------------

def render_hints(problem, hint_level: int):
    u = problem["unit"]
    k = problem["kind"]
    m = problem["meta"]

    if hint_level >= 1:
        st.info("**Hint 1:** Area means how much **space inside**. Use squared units "
                f"like **{unit_sq(u)}**.")

    if hint_level >= 2:
        if k in ("rectangle_area","square_area"):
            st.info("**Hint 2:** Rectangle area = **length × width**. "
                    "Square area = **side × side**.")
        elif k == "missing_side":
            st.info("**Hint 2:** Use **Area = length × width** and solve for the missing side: "
                    "**missing = Area ÷ known side**.")
        elif k == "frame":
            st.info("**Hint 2:** **Frame area = outer area − inner area.**")
        elif k == "composite_L":
            st.info("**Hint 2:** Split the L-shape into two rectangles and **add** their areas.")

    if hint_level >= 3:
        if k == "rectangle_area":
            st.info(f"**Hint 3:** `A = {nfmt(m['w'])} × {nfmt(m['h'])}` {unit_sq(u)} (don’t multiply yet).")
        elif k == "square_area":
            st.info(f"**Hint 3:** `A = {nfmt(m['s'])} × {nfmt(m['s'])}` {unit_sq(u)}.")
        elif k == "missing_side":
            if problem["meta"]["missing"] == "height":
                st.info(f"**Hint 3:** `missing height = {nfmt(m['area'])} ÷ {nfmt(m['w'])}` {u}.")
            else:
                st.info(f"**Hint 3:** `missing width = {nfmt(m['area'])} ÷ {nfmt(m['h'])}` {u}.")
        elif k == "frame":
            st.info(f"**Hint 3:** `A_outer = {nfmt(m['W'])} × {nfmt(m['H'])}`, "
                    f"`A_inner = {nfmt(m['w'])} × {nfmt(m['h'])}`, then subtract.")
        elif k == "composite_L":
            st.info(f"**Hint 3:** `A_total = ({nfmt(m['a'])}×{nfmt(m['b'])}) + "
                    f"({nfmt(m['c'])}×{nfmt(m['d'])})` {unit_sq(u)}.")

def render_steps(problem):
    u = problem["unit"]
    k = problem["kind"]
    m = problem["meta"]
    ans = problem["answer"]

    st.markdown("### Step-by-step solution")

    if k == "rectangle_area":
        st.markdown(f"- Use **A = length × width**.")
        st.markdown(f"- Substitute: **A = {nfmt(m['w'])} × {nfmt(m['h'])} = {nfmt(ans)} {unit_sq(u)}**.")
    elif k == "square_area":
        st.markdown(f"- For a square: **A = side × side**.")
        st.markdown(f"- **A = {nfmt(m['s'])} × {nfmt(m['s'])} = {nfmt(ans)} {unit_sq(u)}**.")
    elif k == "missing_side":
        if m["missing"] == "height":
            st.markdown(f"- **A = length × width** → missing **height = A ÷ width**.")
            st.markdown(f"- **{nfmt(m['area'])} ÷ {nfmt(m['w'])} = {nfmt(ans)} {u}**.")
        else:
            st.markdown(f"- **A = length × width** → missing **width = A ÷ height**.")
            st.markdown(f"- **{nfmt(m['area'])} ÷ {nfmt(m['h'])} = {nfmt(ans)} {u}**.")
        st.info("Remember: the **answer is a length**, so its unit is not squared.")
    elif k == "frame":
        outer = m["W"] * m["H"]
        inner = m["w"] * m["h"]
        st.markdown("- **Frame area = Outer area − Inner area**.")
        st.markdown(f"- Outer: **{nfmt(m['W'])}×{nfmt(m['H'])} = {nfmt(outer)} {unit_sq(u)}**.")
        st.markdown(f"- Inner: **{nfmt(m['w'])}×{nfmt(m['h'])} = {nfmt(inner)} {unit_sq(u)}**.")
        st.markdown(f"- Subtract: **{nfmt(outer)} − {nfmt(inner)} = {nfmt(ans)} {unit_sq(u)}**.")
    elif k == "composite_L":
        A1 = m["a"] * m["b"]
        A2 = m["c"] * m["d"]
        st.markdown("- **Split into rectangles and add their areas.**")
        st.markdown(f"- Rectangle A: **{nfmt(m['a'])}×{nfmt(m['b'])} = {nfmt(A1)} {unit_sq(u)}**.")
        st.markdown(f"- Rectangle B: **{nfmt(m['c'])}×{nfmt(m['d'])} = {nfmt(A2)} {unit_sq(u)}**.")
        st.markdown(f"- Total: **{nfmt(A1)} + {nfmt(A2)} = {nfmt(ans)} {unit_sq(u)}**.")

# --------------------------------------------------------------------
# Main app
# --------------------------------------------------------------------

def run():
    # Session
    if "area_rect_sq_level" not in st.session_state:
        st.session_state.area_rect_sq_level = 1
    if "area_problem" not in st.session_state:
        st.session_state.area_problem = None
        st.session_state.answer_submitted = False
        st.session_state.show_feedback = False
        st.session_state.user_answer = ""
        st.session_state.hint_level = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.streak = 0

    # Header
    st.markdown("**📚 Year 5 > X. Geometric measurement**")
    st.title("🧮 Area of Squares and Rectangles")
    st.markdown("*Find areas, missing sides, and areas of composite shapes.*")
    st.markdown("---")

    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        names = {1:"Simple", 2:"Standard", 3:"Challenging", 4:"Composite"}
        lvl = st.session_state.area_rect_sq_level
        st.markdown(f"**Difficulty Level:** {names[lvl]}")
        st.progress(lvl/4)
    with c2:
        if st.session_state.total_attempted > 0:
            acc = 100*st.session_state.total_correct/st.session_state.total_attempted
            st.metric("Accuracy", f"{acc:.0f}%")
    with c3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

    # New problem
    if st.session_state.area_problem is None:
        st.session_state.area_problem = make_problem(st.session_state.area_rect_sq_level)
        st.session_state.hint_level = 0
        st.session_state.answer_submitted = False
        st.session_state.show_feedback = False
        st.session_state.user_answer = ""

    prob = st.session_state.area_problem

    # Question + SVG
    st.markdown("### Question:")
    st.markdown(prob["prompt"])
    components.html(prob["svg"], height=320)

    # Hints
    hcol1, hcol2 = st.columns([1,3])
    with hcol1:
        if not st.session_state.answer_submitted and st.button("💡 Get a hint"):
            st.session_state.hint_level = min(3, st.session_state.hint_level + 1)
    with hcol2:
        if st.session_state.hint_level > 0 and not st.session_state.answer_submitted:
            render_hints(prob, st.session_state.hint_level)

    # Answer form
    colA, colB = st.columns([3,2])
    with colA:
        with st.form("ans", clear_on_submit=False):
            placeholder = "Enter a number"
            if prob["kind"] == "missing_side":
                placeholder += f" (in {unit_long(prob['unit'])})"
            else:
                placeholder += f" (in {unit_sq(prob['unit'])})"

            st.text_input("Your answer:", key="user_answer",
                          placeholder=placeholder,
                          disabled=st.session_state.answer_submitted)
            submitted = st.form_submit_button("Submit", type="primary",
                                              disabled=st.session_state.answer_submitted)
            if submitted:
                check_answer(prob)
                st.rerun()

    # Feedback
    if st.session_state.show_feedback:
        u = prob["unit"]
        ans = prob["answer"]
        try:
            guess = float(st.session_state.user_answer)
        except Exception:
            guess = None

        correct = (guess is not None) and (abs(guess - ans) < 1e-9)

        if prob["kind"] == "missing_side":
            if correct:
                st.success(f"🎉 Correct! The missing side is **{nfmt(ans)} {u}**.")
            else:
                st.error(f"❌ Not quite. The missing side is **{nfmt(ans)} {u}**.")
                render_steps(prob)
        else:
            if correct:
                st.success(f"🎉 Correct! The area is **{nfmt(ans)} {unit_sq(u)}**.")
            else:
                st.error(f"❌ Not quite. The correct area is **{nfmt(ans)} {unit_sq(u)}**.")
                render_steps(prob)

    # Next
    if st.session_state.answer_submitted:
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("Next Question", type="secondary", use_container_width=True):
                st.session_state.area_problem = None
                st.rerun()

# --------------------------------------------------------------------
# Scoring & difficulty
# --------------------------------------------------------------------

def check_answer(prob):
    st.session_state.total_attempted += 1
    st.session_state.answer_submitted = True
    st.session_state.show_feedback = True

    ans = prob["answer"]
    try:
        guess = float(st.session_state.user_answer)
    except Exception:
        st.session_state.streak = 0
        adjust_level(correct=False)
        return

    if abs(guess - ans) < 1e-9:
        st.session_state.total_correct += 1
        st.session_state.streak += 1
        adjust_level(correct=True)
    else:
        st.session_state.streak = 0
        adjust_level(correct=False)

def adjust_level(correct: bool):
    lvl = st.session_state.area_rect_sq_level
    if correct and st.session_state.streak >= 3:
        st.session_state.area_rect_sq_level = min(4, lvl + 1)
        st.session_state.streak = 0
    if not correct and st.session_state.total_attempted > st.session_state.total_correct + 1:
        st.session_state.area_rect_sq_level = max(1, lvl - 1)

# --------------------------------------------------------------------

if __name__ == "__main__":
    run()
