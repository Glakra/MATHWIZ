import streamlit as st
import streamlit.components.v1 as components
import random

# ------------------------------
# Helpers: UI + palette
# ------------------------------

def _palette(level:int) -> str:
    # soft but distinct fills across levels
    return {
        1: "#BEE3F8",  # light blue
        2: "#C6F6D5",  # light green
        3: "#FED7E2",  # light pink
        4: "#FEEBC8",  # light orange
    }.get(level, "#E2E8F0")

def _unit_long(unit: str) -> str:
    return {"m": "metres", "cm": "centimetres", "mm": "millimetres", "km": "kilometres"}.get(unit, unit)

def _num(n: float) -> str:
    # clean integers like 8.0 -> 8
    return f"{int(n)}" if float(n).is_integer() else f"{n}"

# ------------------------------
# Problem builders
# Each returns dict: {svg:str, edges:[("name", value)], unit:str, type:str}
# ------------------------------

def build_L(unit: str, a: int, b: int, c: int, d: int, e: int, f: int, level: int):
    # Perimeter order (clockwise): top, right1, middle, right2, bottom, left1
    edges = [("Top", a), ("Right (upper)", b), ("Middle", c), ("Right (lower)", d), ("Bottom", e), ("Left", f)]
    color = _palette(level)
    svg = f"""
    <div style="text-align:center;margin:10px 0;">
      <svg width="420" height="300" viewBox="0 0 420 300" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="10" width="400" height="280" fill="none" stroke="none"/>
        <!-- L path (fixed pixels – labels carry the maths) -->
        <path d="M 60 40 L 220 40 L 220 140 L 360 140 L 360 260 L 60 260 Z"
              fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <!-- Labels (edge values) -->
        <text x="140" y="30" font-size="14" font-weight="700" text-anchor="middle">{_num(a)} {unit}</text>
        <text x="230" y="90" font-size="14" font-weight="700">{_num(b)} {unit}</text>
        <text x="290" y="134" font-size="14" font-weight="700" text-anchor="middle">{_num(c)} {unit}</text>
        <text x="370" y="205" font-size="14" font-weight="700">{_num(d)} {unit}</text>
        <text x="210" y="276" font-size="14" font-weight="700" text-anchor="middle">{_num(e)} {unit}</text>
        <text x="48" y="150" font-size="14" font-weight="700" text-anchor="end">{_num(f)} {unit}</text>
      </svg>
    </div>
    """
    return {"svg": svg, "edges": edges, "unit": unit, "type": "L-shape"}

def build_T(unit: str, top: int, r1: int, r2: int, r3: int, bottom: int, l3: int, l2: int, l1: int, level: int):
    # Perimeter order (clockwise) = 8 edges
    edges = [("Top", top), ("Right 1", r1), ("Right 2", r2), ("Right 3", r3),
             ("Bottom", bottom), ("Left 3", l3), ("Left 2", l2), ("Left 1", l1)]
    color = _palette(level)
    svg = f"""
    <div style="text-align:center;margin:10px 0;">
      <svg width="420" height="310" viewBox="0 0 420 310" xmlns="http://www.w3.org/2000/svg">
        <path d="M 40 50 L 380 50 L 380 110 L 260 110 L 260 270 L 160 270 L 160 110 L 40 110 Z"
              fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <text x="210" y="36" font-size="14" font-weight="700" text-anchor="middle">{_num(top)} {unit}</text>
        <text x="388" y="80" font-size="14" font-weight="700">{_num(r1)} {unit}</text>
        <text x="270" y="190" font-size="14" font-weight="700">{_num(r2)} {unit}</text>
        <text x="270" y="286" font-size="14" font-weight="700">{_num(r3)} {unit}</text>
        <text x="210" y="288" font-size="14" font-weight="700" text-anchor="middle">{_num(bottom)} {unit}</text>
        <text x="152" y="286" font-size="14" font-weight="700" text-anchor="end">{_num(l3)} {unit}</text>
        <text x="152" y="190" font-size="14" font-weight="700" text-anchor="end">{_num(l2)} {unit}</text>
        <text x="32"  y="80"  font-size="14" font-weight="700" text-anchor="end">{_num(l1)} {unit}</text>
      </svg>
    </div>
    """
    return {"svg": svg, "edges": edges, "unit": unit, "type": "T-shape"}

def build_U(unit: str, left: int, bottom: int, right: int, top: int, level: int):
    # Classic "U" outline (8 edges total; we list 8 as grouped: left outer, bottom outer, right outer, inner bottom, inner sides, top gaps)
    # For practice we expose 8 labelled edges to sum.
    a,b,c,d = left, bottom, right, top
    edges = [("Left outer", a), ("Bottom outer", b), ("Right outer", c),
             ("Inner bottom", d), ("Inner right", a), ("Top gap right", d),
             ("Inner left", a), ("Top gap left", d)]
    color = _palette(level)
    svg = f"""
    <div style="text-align:center;margin:10px 0;">
      <svg width="420" height="300" viewBox="0 0 420 300" xmlns="http://www.w3.org/2000/svg">
        <path d="M 60 40 L 160 40 L 160 220 L 260 220 L 260 40 L 360 40 L 360 260 L 60 260 Z"
              fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <text x="50"  y="150" font-size="14" font-weight="700" text-anchor="end">{_num(a)} {unit}</text>
        <text x="210" y="276" font-size="14" font-weight="700" text-anchor="middle">{_num(b)} {unit}</text>
        <text x="368" y="150" font-size="14" font-weight="700">{_num(c)} {unit}</text>
        <text x="210" y="236" font-size="13" font-weight="700" text-anchor="middle">{_num(d)} {unit}</text>
        <text x="268" y="150" font-size="13" font-weight="700">{_num(a)} {unit}</text>
        <text x="240" y="60"  font-size="13" font-weight="700">{_num(d)} {unit}</text>
        <text x="152" y="150" font-size="13" font-weight="700" text-anchor="end">{_num(a)} {unit}</text>
        <text x="180" y="60"  font-size="13" font-weight="700" text-anchor="end">{_num(d)} {unit}</text>
      </svg>
    </div>
    """
    return {"svg": svg, "edges": edges, "unit": unit, "type": "U-shape"}

def build_step(unit: str, h1: int, w1: int, h2: int, w2: int, h3: int, w3: int, level: int):
    # 6 outer edges in clockwise order:
    edges = [("Left", h1+h2+h3), ("Top step 1", w3), ("Drop 1", h3), ("Top step 2", w2), ("Drop 2", h2), ("Bottom", w1+w2+w3)]
    color = _palette(level)
    svg = f"""
    <div style="text-align:center;margin:10px 0;">
      <svg width="420" height="300" viewBox="0 0 420 300" xmlns="http://www.w3.org/2000/svg">
        <path d="M 60 240 L 60 200 L 180 200 L 180 160 L 300 160 L 300 120 L 360 120 L 360 240 Z"
              fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <text x="48" y="180" font-size="14" font-weight="700" text-anchor="end">{_num(h1+h2+h3)} {unit}</text>
        <text x="330" y="112" font-size="14" font-weight="700" text-anchor="middle">{_num(w3)} {unit}</text>
        <text x="305" y="140" font-size="14" font-weight="700">{_num(h3)} {unit}</text>
        <text x="240" y="152" font-size="14" font-weight="700" text-anchor="middle">{_num(w2)} {unit}</text>
        <text x="185" y="180" font-size="14" font-weight="700">{_num(h2)} {unit}</text>
        <text x="210" y="256" font-size="14" font-weight="700" text-anchor="middle">{_num(w1+w2+w3)} {unit}</text>
      </svg>
    </div>
    """
    return {"svg": svg, "edges": edges, "unit": unit, "type": "Step shape"}

def build_Z(unit: str, v1: int, mid: int, v2: int, top: int, level: int):
    # 8 edges: left vertical, top long, small drop, middle run, small rise, bottom long, right vertical, top cap
    edges = [("Left", v1), ("Top", top), ("Down", v2), ("Middle", mid),
             ("Up", v2), ("Bottom", top), ("Right", v1), ("Cap", mid)]
    color = _palette(level)
    svg = f"""
    <div style="text-align:center;margin:10px 0;">
      <svg width="420" height="300" viewBox="0 0 420 300" xmlns="http://www.w3.org/2000/svg">
        <path d="M 60 60 L 320 60 L 320 110 L 200 110 L 200 210 L 360 210 L 360 260 L 100 260 L 100 210 L 220 210 L 220 110 L 60 110 Z"
              fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <text x="52"  y="160" font-size="14" font-weight="700" text-anchor="end">{_num(v1)} {unit}</text>
        <text x="190" y="48"  font-size="14" font-weight="700" text-anchor="middle">{_num(top)} {unit}</text>
        <text x="328" y="90"  font-size="14" font-weight="700">{_num(v2)} {unit}</text>
        <text x="260" y="126" font-size="14" font-weight="700" text-anchor="middle">{_num(mid)} {unit}</text>
        <text x="208" y="170" font-size="14" font-weight="700">{_num(v2)} {unit}</text>
        <text x="230" y="276" font-size="14" font-weight="700" text-anchor="middle">{_num(top)} {unit}</text>
        <text x="368" y="160" font-size="14" font-weight="700">{_num(v1)} {unit}</text>
        <text x="290" y="226" font-size="14" font-weight="700" text-anchor="middle">{_num(mid)} {unit}</text>
      </svg>
    </div>
    """
    return {"svg": svg, "edges": edges, "unit": unit, "type": "Z-shape"}

def build_H(unit: str, tall: int, width: int, mid: int, level: int):
    # 12 edges but we present grouped 8 sums to stay readable
    # perimeter grouped clockwise:
    edges = [("Left outer", tall), ("Top left", width//2), ("Bridge up", mid//2),
             ("Bridge", width), ("Bridge down", mid//2), ("Top right", width//2),
             ("Right outer", tall), ("Bottom", width)]
    color = _palette(level)
    svg = f"""
    <div style="text-align:center;margin:10px 0;">
      <svg width="420" height="300" viewBox="0 0 420 300" xmlns="http://www.w3.org/2000/svg">
        <path d="M 60 40 L 160 40 L 160 120 L 260 120 L 260 40 L 360 40 L 360 260 L 260 260 L 260 180 L 160 180 L 160 260 L 60 260 Z"
              fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <text x="52" y="150" font-size="14" font-weight="700" text-anchor="end">{_num(tall)} {unit}</text>
        <text x="110" y="30" font-size="14" font-weight="700" text-anchor="middle">{_num(width//2)} {unit}</text>
        <text x="200" y="112" font-size="13" font-weight="700" text-anchor="middle">{_num(mid//2)} {unit}</text>
        <text x="210" y="132" font-size="14" font-weight="700" text-anchor="middle">{_num(width)} {unit}</text>
        <text x="210" y="188" font-size="13" font-weight="700" text-anchor="middle">{_num(mid//2)} {unit}</text>
        <text x="310" y="30" font-size="14" font-weight="700" text-anchor="middle">{_num(width//2)} {unit}</text>
        <text x="368" y="150" font-size="14" font-weight="700">{_num(tall)} {unit}</text>
        <text x="210" y="276" font-size="14" font-weight="700" text-anchor="middle">{_num(width)} {unit}</text>
      </svg>
    </div>
    """
    return {"svg": svg, "edges": edges, "unit": unit, "type": "H-shape"}

def build_rectangle(unit: str, w: int, h: int, level: int):
    edges = [("Top", w), ("Right", h), ("Bottom", w), ("Left", h)]
    color = _palette(level)
    svg = f"""
    <div style="text-align:center;margin:10px 0;">
      <svg width="420" height="260" viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg">
        <rect x="80" y="60" width="260" height="140" fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <text x="210" y="50" font-size="14" font-weight="700" text-anchor="middle">{_num(w)} {unit}</text>
        <text x="350" y="140" font-size="14" font-weight="700">{_num(h)} {unit}</text>
        <text x="210" y="216" font-size="14" font-weight="700" text-anchor="middle">{_num(w)} {unit}</text>
        <text x="70"  y="140" font-size="14" font-weight="700" text-anchor="end">{_num(h)} {unit}</text>
      </svg>
    </div>
    """
    return {"svg": svg, "edges": edges, "unit": unit, "type": "Rectangle"}

def build_octagon(unit: str, a: int, b: int, c: int, d: int, e: int, f: int, g: int, h: int, level: int):
    edges = [("A", a), ("B", b), ("C", c), ("D", d), ("E", e), ("F", f), ("G", g), ("H", h)]
    color = _palette(level)
    svg = f"""
    <div style="text-align:center;margin:10px 0;">
      <svg width="420" height="300" viewBox="0 0 420 300" xmlns="http://www.w3.org/2000/svg">
        <path d="M 150 40 L 270 40 L 340 110 L 340 190 L 270 260 L 150 260 L 80 190 L 80 110 Z"
              fill="{color}" stroke="#2D3748" stroke-width="2"/>
        <text x="210" y="30" font-size="13" font-weight="700" text-anchor="middle">{_num(a)} {unit}</text>
        <text x="330" y="90" font-size="13" font-weight="700">{_num(b)} {unit}</text>
        <text x="352" y="152" font-size="13" font-weight="700">{_num(c)} {unit}</text>
        <text x="330" y="214" font-size="13" font-weight="700">{_num(d)} {unit}</text>
        <text x="210" y="276" font-size="13" font-weight="700" text-anchor="middle">{_num(e)} {unit}</text>
        <text x="90"  y="214" font-size="13" font-weight="700" text-anchor="end">{_num(f)} {unit}</text>
        <text x="68"  y="152" font-size="13" font-weight="700" text-anchor="end">{_num(g)} {unit}</text>
        <text x="90"  y="90"  font-size="13" font-weight="700" text-anchor="end">{_num(h)} {unit}</text>
      </svg>
    </div>
    """
    return {"svg": svg, "edges": edges, "unit": unit, "type": "Irregular octagon"}

# ------------------------------
# Problem generation
# ------------------------------

def make_problem(level: int):
    # ranges by difficulty
    if level == 1:
        lo, hi, unit = 2, 8, "cm"
    elif level == 2:
        lo, hi, unit = 4, 15, "cm"
    elif level == 3:
        lo, hi, unit = 6, 20, "m"
    else:
        lo, hi, unit = 10, 35, "m"

    choice = random.choice(["L","T","U","STEP","Z","H","RECT","OCT"])

    def r(n=1):
        return [random.randint(lo, hi) for _ in range(n)]

    if choice == "L":
        a,b,c,d,e,f = r(6)
        return build_L(unit, a,b,c,d,e,f, level)

    if choice == "T":
        top,r1,r2,r3,bottom,l3,l2,l1 = r(8)
        return build_T(unit, top,r1,r2,r3,bottom,l3,l2,l1, level)

    if choice == "U":
        left,bottom,right,top = r(4)
        return build_U(unit, left,bottom,right,top, level)

    if choice == "STEP":
        h1,w1,h2,w2,h3,w3 = r(6)
        return build_step(unit, h1,w1,h2,w2,h3,w3, level)

    if choice == "Z":
        v1,mid,v2,top = r(4)
        return build_Z(unit, v1,mid,v2,top, level)

    if choice == "H":
        tall,width,mid = r(3)
        # keep even for bridge halves labelling
        if width % 2: width += 1
        if mid   % 2: mid   += 1
        return build_H(unit, tall,width,mid, level)

    if choice == "RECT":
        w,h = r(2)
        return build_rectangle(unit, w,h, level)

    # OCT
    a,b,c,d,e,f,g,h = r(8)
    return build_octagon(unit, a,b,c,d,e,f,g,h, level)

# ------------------------------
# Step-by-step + hints
# ------------------------------

def perimeter(edges):
    return sum(v for _, v in edges)

def render_step_by_step(problem):
    unit = problem["unit"]
    edges = problem["edges"]
    total = perimeter(edges)

    st.markdown("### Step-by-step solution")
    st.markdown(f"**Shape:** {problem['type']} &nbsp;&nbsp; **Unit:** {_unit_long(unit)}")
    st.markdown("We add **every outer edge** once, going clockwise:")

    # Enumerate edges with running sum
    run = 0
    lines = []
    for i, (name, val) in enumerate(edges, start=1):
        run += val
        lines.append(f"{i}. {name}: **{_num(val)} {unit}** &nbsp;&nbsp; (running total = **{_num(run)} {unit}**)")
    st.markdown("\n".join([f"- {ln}" for ln in lines]))

    # Final line
    st.success(f"**Perimeter, P = {' + '.join(_num(v) for _, v in edges)} = {_num(total)} {unit}**")

def render_hints(problem, level):
    unit = problem["unit"]
    edges = problem["edges"]
    n = len(edges)

    if level >= 1:
        st.info(f"**Hint 1:** Trace the **outside boundary** with your finger (ignore any interior corners). "
                f"There are **{n} outer edges** to add.")

    if level >= 2:
        st.info("**Hint 2:** Add systematically: go clockwise and write a quick list like "
                f"`{', '.join(name for name, _ in edges)}` then fill in the numbers.")

    if level >= 3:
        # show a semi-worked structure without giving the total
        st.info("**Hint 3 (structured sum):** "
                f"`P = {' + '.join(_num(v) for _, v in edges)}`  (add these numbers). "
                f"Remember the answer is in **{_unit_long(unit)}**.")

# ------------------------------
# Main app
# ------------------------------

def run():
    """
    Perimeter of Polygons — with hints and step-by-step solutions.
    """
    # --- session ---
    if "polygon_perimeter_difficulty" not in st.session_state:
        st.session_state.polygon_perimeter_difficulty = 1
    if "current_polygon_problem" not in st.session_state:
        st.session_state.current_polygon_problem = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answer = ""
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.hint_level = 0

    # --- header ---
    st.markdown("**📚 Year 5 > X. Geometric measurement**")
    st.title("📐 Perimeter of Polygons")
    st.markdown("*Calculate the perimeter of a variety of irregular shapes. Use hints if you get stuck!*")
    st.markdown("---")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        names = {
            1: "Simple shapes (small numbers)",
            2: "Medium shapes (larger numbers)",
            3: "Complex shapes (mixed sizes)",
            4: "Advanced shapes (challenging)"
        }
        lvl = st.session_state.polygon_perimeter_difficulty
        st.markdown(f"**Difficulty Level:** {names[lvl]}")
        st.progress(lvl / 4)
    with col2:
        if st.session_state.total_attempted > 0:
            acc = 100 * st.session_state.total_correct / st.session_state.total_attempted
            st.metric("Accuracy", f"{acc:.0f}%")
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

    # --- make problem ---
    if st.session_state.current_polygon_problem is None:
        st.session_state.current_polygon_problem = make_problem(st.session_state.polygon_perimeter_difficulty)
        st.session_state.hint_level = 0
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answer = ""

    problem = st.session_state.current_polygon_problem

    # --- question ---
    st.markdown("### What is **the perimeter** of the shape?")
    components.html(problem["svg"], height=330)

    # Hints (progressive)
    hint_col1, hint_col2 = st.columns([1,3])
    with hint_col1:
        if not st.session_state.answer_submitted and st.button("💡 Get a hint"):
            st.session_state.hint_level = min(3, st.session_state.hint_level + 1)
    with hint_col2:
        if st.session_state.hint_level > 0 and not st.session_state.answer_submitted:
            render_hints(problem, st.session_state.hint_level)

    # --- answer form ---
    colA, colB = st.columns([3,2])
    with colA:
        with st.form("ans", clear_on_submit=False):
            st.text_input(
                f"Enter the perimeter in {_unit_long(problem['unit'])}:",
                key="user_answer",
                placeholder="e.g., 42",
                disabled=st.session_state.answer_submitted
            )
            submitted = st.form_submit_button(
                "Submit",
                type="primary",
                disabled=st.session_state.answer_submitted
            )
            if submitted:
                if st.session_state.user_answer.strip() == "":
                    st.warning("Please enter a number.")
                else:
                    check_and_score(problem)

    # feedback + steps
    if st.session_state.show_feedback:
        total = perimeter(problem["edges"])
        unit = problem["unit"]
        try:
            user_val = float(st.session_state.user_answer)
        except Exception:
            user_val = None

        if user_val is not None and abs(user_val - total) < 1e-9:
            st.success(f"🎉 Correct! The perimeter is **{_num(total)} {unit}**.")
            if st.session_state.consecutive_correct == 2:
                st.info("🔥 One more correct answer to level up!")
        else:
            st.error(f"❌ Not quite. The correct perimeter is **{_num(total)} {unit}**.")
            render_step_by_step(problem)  # <- full working

    # next question
    if st.session_state.answer_submitted:
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("Next Question", type="secondary", use_container_width=True):
                st.session_state.current_polygon_problem = None
                st.rerun()

# ------------------------------
# Scoring & difficulty adjust
# ------------------------------

def check_and_score(problem):
    total = perimeter(problem["edges"])
    unit = problem["unit"]

    st.session_state.answer_submitted = True
    st.session_state.show_feedback = True
    st.session_state.total_attempted += 1

    try:
        guess = float(st.session_state.user_answer)
    except Exception:
        # invalid -> count as wrong
        st.session_state.consecutive_correct = 0
        _adjust_difficulty(correct=False)
        return

    if abs(guess - total) < 1e-9:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        _adjust_difficulty(correct=True)
    else:
        st.session_state.consecutive_correct = 0
        _adjust_difficulty(correct=False)

def _adjust_difficulty(correct: bool):
    if correct and st.session_state.consecutive_correct >= 3:
        st.session_state.polygon_perimeter_difficulty = min(4, st.session_state.polygon_perimeter_difficulty + 1)
        st.session_state.consecutive_correct = 0
    if not correct and st.session_state.total_attempted > st.session_state.total_correct + 1:
        st.session_state.polygon_perimeter_difficulty = max(1, st.session_state.polygon_perimeter_difficulty - 1)

# ------------------------------
# Entry point for the platform
# ------------------------------

if __name__ == "__main__":
    run()
