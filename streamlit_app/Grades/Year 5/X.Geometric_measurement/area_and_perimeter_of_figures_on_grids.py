# file: area_perimeter_on_grids.py
import streamlit as st
import streamlit.components.v1 as components
import random

# ----------------------------- helpers: geometry -----------------------------

DIRS = [(1,0), (-1,0), (0,1), (0,-1)]

def cells_rect(x, y, w, h):
    return {(i, j) for i in range(x, x+w) for j in range(y, y+h)}

def make_rectangle(grid_w, grid_h, min_w=1, min_h=1):
    w = random.randint(min_w, max(min_w, grid_w-1))
    h = random.randint(min_h, max(min_h, grid_h-1))
    x = random.randint(0, grid_w - w)
    y = random.randint(0, grid_h - h)
    return cells_rect(x, y, w, h)

def make_L(grid_w, grid_h):
    t = random.randint(1, 2)                       # thickness
    arm_w = random.randint(2, grid_w-1)
    arm_h = random.randint(2, grid_h-1)
    x = random.randint(0, grid_w - arm_w)
    y = random.randint(0, grid_h - arm_h)
    horiz = cells_rect(x, y, arm_w, t)
    vert  = cells_rect(x, y, t, arm_h)
    return horiz | vert

def make_T(grid_w, grid_h):
    t = random.randint(1, 2)
    cap_w = random.randint(3, grid_w)
    stem_h = random.randint(2, grid_h-1)
    x = random.randint(0, grid_w - cap_w)
    y = random.randint(0, grid_h - stem_h - 1)
    cap = cells_rect(x, y+stem_h, cap_w, t)
    stem_x = x + random.randint(0, cap_w - t)
    stem = cells_rect(stem_x, y, t, stem_h)
    return cap | stem

def make_stairs(grid_w, grid_h):
    steps = random.randint(2, 4)
    t = random.randint(1, 2)  # step thickness
    # start near bottom-left
    x0 = random.randint(0, max(0, grid_w - steps*t - 1))
    y0 = random.randint(0, max(0, grid_h - steps*t - 1))
    cells = set()
    for k in range(steps):
        # each step adds a t x ((k+1)*t) rectangle stacked
        cells |= cells_rect(x0 + k*t, y0, t, (k+1)*t)
    return cells

def make_blob(grid_w, grid_h):
    # connected random flood fill target size
    target = random.randint(6, min(14, grid_w*grid_h-1))
    start = (random.randint(0, grid_w-1), random.randint(0, grid_h-1))
    cells = {start}
    frontier = [start]
    while len(cells) < target and frontier:
        x,y = frontier.pop(random.randrange(len(frontier)))
        for dx,dy in DIRS:
            nx, ny = x+dx, y+dy
            if 0 <= nx < grid_w and 0 <= ny < grid_h and (nx,ny) not in cells:
                if random.random() < 0.6:  # grow with bias
                    cells.add((nx,ny))
                    frontier.append((nx,ny))
        if not frontier and len(cells) < target:
            frontier = list(cells)
    return cells

def area_from_cells(cells):
    return len(cells)

def perimeter_from_cells(cells):
    # count exposed unit edges
    perim = 0
    S = set(cells)
    for x,y in S:
        if (x+1,y) not in S: perim += 1
        if (x-1,y) not in S: perim += 1
        if (x,y+1) not in S: perim += 1
        if (x,y-1) not in S: perim += 1
    return perim

def row_counts(cells):
    # for step-by-step area solution
    by_row = {}
    for x,y in cells:
        by_row.setdefault(y, 0)
        by_row[y] += 1
    return dict(sorted(by_row.items()))

def boundary_breakdown(cells):
    # counts horizontal and vertical boundary segments for explanation
    S = set(cells)
    horiz = vert = 0
    for x,y in S:
        if (x+1,y) not in S: vert += 1
        if (x-1,y) not in S: vert += 1
        if (x,y+1) not in S: horiz += 1
        if (x,y-1) not in S: horiz += 1
    return horiz, vert

# --------------------------- drawing: SVG grid -------------------------------

def svg_grid(cells, grid_w, grid_h, fill="#C8EBA5"):
    size = 360  # px
    margin = 40
    total_w = size + margin*2
    total_h = size + margin*2
    cell = size / grid_w

    # axis labels 0..grid_w/h
    x_labels = "".join(
        f"<text x='{margin + i*cell}' y='{total_h-8}' text-anchor='middle' font-size='12' fill='#555'>{i}</text>"
        for i in range(grid_w+1)
    )
    y_labels = "".join(
        f"<text x='{10}' y='{total_h - (margin + i*cell)}' text-anchor='middle' font-size='12' fill='#555'>{i}</text>"
        for i in range(grid_h+1)
    )

    # grid lines
    vlines = "".join(
        f"<line x1='{margin + i*cell}' y1='{margin}' x2='{margin + i*cell}' y2='{margin+size}' stroke='#e6e6e6'/>"
        for i in range(grid_w+1)
    )
    hlines = "".join(
        f"<line x1='{margin}' y1='{margin + j*cell}' x2='{margin+size}' y2='{margin + j*cell}' stroke='#e6e6e6'/>"
        for j in range(grid_h+1)
    )

    # shaded cells
    rects = []
    for (x,y) in cells:
        # Flip y to put origin at bottom-left for display
        disp_y = grid_h - 1 - y
        rects.append(
            f"<rect x='{margin + x*cell}' y='{margin + disp_y*cell}' "
            f"width='{cell}' height='{cell}' fill='{fill}' stroke='#88b96a' stroke-width='1' />"
        )
    shaded = "".join(rects)

    svg = f"""
    <svg width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">
        <rect x="0" y="0" width="{total_w}" height="{total_h}" fill="white"/>
        {vlines}{hlines}
        <rect x="{margin}" y="{margin}" width="{size}" height="{size}" fill="none" stroke="#bbb"/>
        {shaded}
        {x_labels}{y_labels}
    </svg>
    """
    return svg

# ------------------------------ app state -----------------------------------

def new_problem(difficulty):
    # grid size grows, shapes get trickier by level
    grid_w = grid_h = {1:5, 2:6, 3:7, 4:8}.get(difficulty, 6)

    kind_pool = {
        1: ["rectangle", "L", "stairs"],
        2: ["rectangle", "L", "T", "stairs"],
        3: ["rectangle", "L", "T", "stairs", "blob"],
        4: ["L", "T", "stairs", "blob"],
    }[difficulty]

    kind = random.choice(kind_pool)

    if kind == "rectangle":
        cells = make_rectangle(grid_w, grid_h, min_w=2, min_h=1)
    elif kind == "L":
        cells = make_L(grid_w, grid_h)
    elif kind == "T":
        cells = make_T(grid_w, grid_h)
    elif kind == "stairs":
        cells = make_stairs(grid_w, grid_h)
    else:
        cells = make_blob(grid_w, grid_h)

    A = area_from_cells(cells)
    P = perimeter_from_cells(cells)
    horiz, vert = boundary_breakdown(cells)

    # question type
    qtype = random.choices(["area", "perimeter", "both"], weights=[0.4, 0.4, 0.2])[0]

    return {
        "grid_w": grid_w, "grid_h": grid_h,
        "cells": cells, "kind": kind,
        "area": A, "perimeter": P,
        "horiz_edges": horiz, "vert_edges": vert,
        "qtype": qtype,
        "row_counts": row_counts(cells)
    }

# ------------------------------ UI pieces -----------------------------------

def header():
    st.markdown("**📚 Year 5 > X. Geometric measurement**")
    st.title("🟨 Area & Perimeter of Figures on Grids")
    st.caption("Count squares for area and trace the border for perimeter.")
    st.divider()

def stats_and_nav():
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        names = {1:"Starter", 2:"Developing", 3:"Confident", 4:"Expert"}
        st.markdown(f"**Difficulty:** {names[st.session_state.level]}")
        st.progress(st.session_state.level/4)
    with c2:
        if st.session_state.attempts:
            acc = 100 * st.session_state.correct / st.session_state.attempts
            st.metric("Accuracy", f"{acc:.0f}%")
    with c3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

def show_problem():
    prob = st.session_state.problem
    q = prob["qtype"]

    question = {
        "area": "What is the **area** of the shaded figure?",
        "perimeter": "What is the **perimeter** of the shaded figure?",
        "both": "What are the **area** and **perimeter** of the shaded figure?"
    }[q]

    st.subheader("Question:")
    st.write(question)

    # draw
    svg = svg_grid(prob["cells"], prob["grid_w"], prob["grid_h"],
                   fill={"rectangle":"#FFE28A","L":"#C7E7FF","T":"#EAC4FF","stairs":"#C8EBA5","blob":"#FFD9A8"}[prob["kind"]])
    components.html(svg, height=460)

    with st.expander("💡 Hints"):
        if q in ("area", "both"):
            st.markdown(
                "- Count **full shaded squares**. Each cell = **1 square unit**.\n"
                "- Or add by **rows**: count how many shaded cells are in each row and add them.\n"
                "- For rectangles, you can use **length × width**."
            )
        if q in ("perimeter", "both"):
            st.markdown(
                "- Trace just the **outside border**. **Do not** count interior edges.\n"
                "- Each grid edge is **1 unit**.\n"
                "- Quick method: for every shaded cell, count sides that **touch blank space**. Add them all."
            )

    # answer controls
    cols = st.columns(2) if q == "both" else [st.container()]
    if q == "both":
        with cols[0]:
            st.session_state.ans_area = st.text_input("Area (square units)", value=st.session_state.ans_area)
        with cols[1]:
            st.session_state.ans_perim = st.text_input("Perimeter (units)", value=st.session_state.ans_perim)
    elif q == "area":
        st.session_state.ans_area = st.text_input("Area (square units)", value=st.session_state.ans_area)
    else:
        st.session_state.ans_perim = st.text_input("Perimeter (units)", value=st.session_state.ans_perim)

    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("✅ Submit", type="primary"):
            check()

    # feedback
    if st.session_state.feedback:
        st.markdown("---")
        st.session_state.feedback()

    if st.session_state.ready_next:
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("🔄 Next Question", type="secondary"):
                next_problem()

def check():
    prob = st.session_state.problem
    q = prob["qtype"]
    ok_area = ok_perim = True

    # evaluate
    try:
        if q in ("area", "both"):
            user_a = float(st.session_state.ans_area.strip())
            ok_area = abs(user_a - prob["area"]) < 1e-9
        if q in ("perimeter", "both"):
            user_p = float(st.session_state.ans_perim.strip())
            ok_perim = abs(user_p - prob["perimeter"]) < 1e-9
    except Exception:
        st.error("Please enter numbers only.")
        return

    st.session_state.attempts += 1
    all_ok = ok_area and ok_perim
    st.session_state.correct += 1 if all_ok else 0
    st.session_state.streak = (st.session_state.streak + 1) if all_ok else 0

    # adaptive difficulty
    if all_ok and st.session_state.streak >= 3 and st.session_state.level < 4:
        st.session_state.level += 1
        st.session_state.streak = 0
        st.info("🎯 Level up! Problems will get a little trickier.")

    # build feedback closure so we can render after submit
    def feedback():
        if all_ok:
            st.success("🎉 Correct! Nice counting.")
        else:
            msgs = []
            if q in ("area","both") and not ok_area:
                msgs.append(f"**Area** should be **{prob['area']}** square units.")
            if q in ("perimeter","both") and not ok_perim:
                msgs.append(f"**Perimeter** should be **{prob['perimeter']}** units.")
            st.error("Not quite. " + " ".join(msgs))

            # step-by-step solution
            with st.expander("📖 Step-by-step solution", expanded=True):
                if q in ("area","both") and not ok_area:
                    rc = prob["row_counts"]
                    st.markdown("**Area by rows (count shaded squares per row):**")
                    lines = [f"- Row {r}: {c} square(s)" for r,c in rc.items()]
                    st.markdown("\n".join(lines))
                    st.markdown(f"**Total area =** {' + '.join(str(c) for c in rc.values())} = **{prob['area']}**")
                    if prob["kind"] == "rectangle":
                        # also show LxW
                        # derive bounding box of rectangle
                        xs = [x for x,_ in prob["cells"]]; ys=[y for _,y in prob["cells"]]
                        w = max(xs)-min(xs)+1; h = max(ys)-min(ys)+1
                        st.markdown(f"Because it’s a rectangle: **length × width = {w} × {h} = {prob['area']}**")

                if q in ("perimeter","both") and not ok_perim:
                    h, v = prob["horiz_edges"], prob["vert_edges"]
                    st.markdown(
                        "**Perimeter by exposed edges:**\n\n"
                        f"- Horizontal boundary edges: **{h}**\n"
                        f"- Vertical boundary edges: **{v}**\n"
                        f"**Perimeter = {h} + {v} = {prob['perimeter']}**"
                    )
                    st.markdown(
                        "_Why this works:_ each shaded cell contributes edges that touch blank space. "
                        "Interior shared edges are counted twice in opposite directions and cancel out."
                    )

                st.markdown("💡 **Next time:** trace the outline with your finger or cursor and count each grid edge once.")

    st.session_state.feedback = feedback
    st.session_state.ready_next = True

def next_problem():
    st.session_state.problem = new_problem(st.session_state.level)
    st.session_state.ans_area = ""
    st.session_state.ans_perim = ""
    st.session_state.feedback = None
    st.session_state.ready_next = False

# ----------------------------------- run -------------------------------------

def run():
    if "level" not in st.session_state:
        st.session_state.level = 1
        st.session_state.problem = new_problem(st.session_state.level)
        st.session_state.ans_area = ""
        st.session_state.ans_perim = ""
        st.session_state.feedback = None
        st.session_state.ready_next = False
        st.session_state.attempts = 0
        st.session_state.correct = 0
        st.session_state.streak = 0

    header()
    stats_and_nav()
    show_problem()

if __name__ == "__main__":
    st.set_page_config(page_title="Area & Perimeter on Grids", page_icon="🟨", layout="centered")
    run()
