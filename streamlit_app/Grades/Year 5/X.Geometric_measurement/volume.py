import streamlit as st
import random
import math

# ============================================================
# ==============  ISO PRISM RENDERING (SVG)  =================
# ============================================================

def _iso_prism_svg(
    width_u: int,
    depth_u: int,
    height_u: int,
    tint="#7CC4FF",
    show_grid=True,
    label_dims=None,
    origin=(160.0, 76.0),
    scale=24.0,
):
    """
    Render a single rectangular prism in 30° isometric projection.

    width_u  -> along v (to the left & up)
    depth_u  -> along u (to the right & up)
    height_u -> vertical down

    label_dims: optional dict like {"w":"4","d":"3","h":"2"} or with "?" for unknown.
    """
    # 30° basis
    cos30, sin30 = 0.8660254, 0.5
    s = scale
    u = (cos30 * s, -sin30 * s)   # depth (→ right & up)
    v = (-cos30 * s, -sin30 * s)  # width (→ left  & up)
    w = (0.0, 1.0 * s)            # height (↓)

    def add(a, b): return (a[0] + b[0], a[1] + b[1])
    def mul(a, k): return (a[0] * k, a[1] * k)
    def pt(p): return f"{p[0]:.2f},{p[1]:.2f}"

    O = origin

    # Corners
    P0 = O
    P1 = add(O, mul(u, depth_u))
    P2 = add(P1, mul(v, width_u))
    P3 = add(O, mul(v, width_u))
    P0b, P1b, P2b, P3b = add(P0, mul(w, height_u)), add(P1, mul(w, height_u)), add(P2, mul(w, height_u)), add(P3, mul(w, height_u))

    # Faces
    top_pts   = " ".join([pt(P0), pt(P1), pt(P2), pt(P3)])
    right_pts = " ".join([pt(P1), pt(P2), pt(P2b), pt(P1b)])
    left_pts  = " ".join([pt(P0), pt(P3), pt(P3b), pt(P0b)])

    # Colors
    top_fill   = "url(#topGrad)"
    left_fill  = tint
    right_fill = "#4FA1F2"

    # Shadow
    shadow_cx = (P3b[0] + P1b[0]) / 2.0
    shadow_cy = max(P0b[1], P1b[1], P2b[1], P3b[1]) + 7
    rx = (width_u + depth_u) * (s * 0.35)
    ry = 6

    # Unique clip ids per call
    uid = str(random.randint(10**6, 9_999_999))

    # -------- Grid lines (now clipped per-face) --------
    top_grid, right_grid, left_grid = [], [], []
    if show_grid:
        # Top face grid (within P0-P1-P2-P3)
        for i in range(1, max(0, width_u)):
            A = add(O, mul(v, i)); B = add(A, mul(u, depth_u))
            top_grid.append((A, B))
        for j in range(1, max(0, depth_u)):
            A = add(O, mul(u, j)); B = add(A, mul(v, width_u))
            top_grid.append((A, B))

        # Right face grid (u × w) within P1-P2-P2b-P1b
        for k in range(1, max(0, height_u)):
            A = add(P1, mul(w, k)); B = add(A, mul(u, depth_u))
            if height_u > 1: right_grid.append((A, B))
        for j in range(1, max(0, depth_u)):
            A = add(P1, mul(u, j)); B = add(A, mul(w, height_u))
            if depth_u > 1: right_grid.append((A, B))

        # Left face grid (v × w) within P0-P3-P3b-P0b
        for k in range(1, max(0, height_u)):
            A = add(P0, mul(w, k)); B = add(A, mul(v, width_u))
            if height_u > 1: left_grid.append((A, B))
        for i in range(1, max(0, width_u)):
            A = add(P0, mul(v, i)); B = add(A, mul(w, height_u))
            if width_u > 1: left_grid.append((A, B))

    # Outer edges
    edges = [
        (P0, P1), (P1, P2), (P2, P3), (P3, P0),
        (P0, P0b), (P1, P1b), (P2, P2b), (P3, P3b),
        (P0b, P1b), (P1b, P2b), (P2b, P3b), (P3b, P0b)
    ]

    # Helpers for dims
    def angle_deg(vec): return math.degrees(math.atan2(vec[1], vec[0]))
    def norm(vec):
        L = math.hypot(vec[0], vec[1]); 
        return (0.0, 0.0) if L == 0 else (vec[0]/L, vec[1]/L)
    def perp(vec): return (-vec[1], vec[0])

    def draw_dim_line(svg_list, start, vec_dir, units, label, offset_px=10, outside=True):
        dir_px = mul(vec_dir, units)
        o = norm(perp(vec_dir))
        offset = mul(o, offset_px if outside else -offset_px)
        A = add(start, offset)
        B = add(add(start, dir_px), offset)

        tick = 7
        A_tick1 = add(start, mul(o, (offset_px - tick)))
        A_tick2 = add(start, mul(o, (offset_px + tick)))
        B_base = add(start, dir_px)
        B_tick1 = add(B_base, mul(o, (offset_px - tick)))
        B_tick2 = add(B_base, mul(o, (offset_px + tick)))

        ang = angle_deg(vec_dir)
        mid = ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0)

        svg_list.append(
            f"<line x1='{A[0]:.1f}' y1='{A[1]:.1f}' x2='{B[0]:.1f}' y2='{B[1]:.1f}' "
            "stroke='#0E2236' stroke-width='1.3' vector-effect='non-scaling-stroke' "
            "marker-start='url(#arrow)' marker-end='url(#arrow)'/>"
        )
        svg_list.append(
            f"<line x1='{A_tick1[0]:.1f}' y1='{A_tick1[1]:.1f}' x2='{A_tick2[0]:.1f}' y2='{A_tick2[1]:.1f}' "
            "stroke='#0E2236' stroke-width='1.1' vector-effect='non-scaling-stroke'/>"
        )
        svg_list.append(
            f"<line x1='{B_tick1[0]:.1f}' y1='{B_tick1[1]:.1f}' x2='{B_tick2[0]:.1f}' y2='{B_tick2[1]:.1f}' "
            "stroke='#0E2236' stroke-width='1.1' vector-effect='non-scaling-stroke'/>"
        )
        svg_list.append(
            f"<text x='{mid[0]:.1f}' y='{mid[1]:.1f}' "
            f"transform='rotate({ang:.1f} {mid[0]:.1f} {mid[1]:.1f})' "
            "text-anchor='middle' dominant-baseline='central' font-size='12px' fill='#0E2236'>"
            f"<tspan paint-order='stroke' stroke='white' stroke-width='3'>{label}</tspan>"
            f"</text>"
        )

    svg = []
    svg.append("<div style='text-align:center;margin:8px 0 6px'>")
    svg.append(
        "<svg width='360' height='230' viewBox='0 0 360 230' "
        "stroke-linejoin='round' stroke-linecap='round'>"
        "<defs>"
        "<marker id='arrow' viewBox='0 0 10 10' refX='5' refY='5' "
        "markerWidth='7' markerHeight='7' orient='auto-start-reverse'>"
        "<path d='M0,0 L10,5 L0,10 z' fill='#0E2236'/></marker>"
        "<linearGradient id='topGrad' x1='0' y1='0' x2='0' y2='1'>"
        "<stop offset='0%' stop-color='#F7FBFF'/><stop offset='100%' stop-color='#E6F2FF'/>"
        "</linearGradient>"
        # Clip paths — ensure grid lines never bleed outside faces
        f"<clipPath id='clipTop{uid}'><polygon points='{top_pts}'/></clipPath>"
        f"<clipPath id='clipRight{uid}'><polygon points='{right_pts}'/></clipPath>"
        f"<clipPath id='clipLeft{uid}'><polygon points='{left_pts}'/></clipPath>"
        "</defs>"
    )

    # Shadow
    svg.append(
        f"<ellipse cx='{shadow_cx:.1f}' cy='{shadow_cy:.1f}' rx='{rx:.1f}' ry='{ry:.1f}' "
        "fill='rgba(0,0,0,0.08)'/>"
    )

    # Faces (far → near)
    svg.append(
        f"<polygon points='{left_pts}' fill='{left_fill}' opacity='0.95' "
        "stroke='#1A3149' stroke-width='1.6' vector-effect='non-scaling-stroke'/>"
    )
    svg.append(
        f"<polygon points='{right_pts}' fill='{right_fill}' opacity='0.95' "
        "stroke='#1A3149' stroke-width='1.6' vector-effect='non-scaling-stroke'/>"
    )
    svg.append(
        f"<polygon points='{top_pts}' fill='{top_fill}' "
        "stroke='#1A3149' stroke-width='1.7' vector-effect='non-scaling-stroke'/>"
    )

    # Grid (clipped to each face)
    if show_grid:
        if top_grid:
            svg.append(f"<g clip-path='url(#clipTop{uid})'>")
            for a, b in top_grid:
                svg.append(
                    f"<line x1='{a[0]:.2f}' y1='{a[1]:.2f}' x2='{b[0]:.2f}' y2='{b[1]:.2f}' "
                    "stroke='#0E2236' stroke-width='0.9' opacity='0.32' vector-effect='non-scaling-stroke'/>"
                )
            svg.append("</g>")
        if right_grid:
            svg.append(f"<g clip-path='url(#clipRight{uid})'>")
            for a, b in right_grid:
                svg.append(
                    f"<line x1='{a[0]:.2f}' y1='{a[1]:.2f}' x2='{b[0]:.2f}' y2='{b[1]:.2f}' "
                    "stroke='#0E2236' stroke-width='0.9' opacity='0.32' vector-effect='non-scaling-stroke'/>"
                )
            svg.append("</g>")
        if left_grid:
            svg.append(f"<g clip-path='url(#clipLeft{uid})'>")
            for a, b in left_grid:
                svg.append(
                    f"<line x1='{a[0]:.2f}' y1='{a[1]:.2f}' x2='{b[0]:.2f}' y2='{b[1]:.2f}' "
                    "stroke='#0E2236' stroke-width='0.9' opacity='0.32' vector-effect='non-scaling-stroke'/>"
                )
            svg.append("</g>")

    # Outer edges
    for a, b in edges:
        svg.append(
            f"<line x1='{a[0]:.2f}' y1='{a[1]:.2f}' x2='{b[0]:.2f}' y2='{b[1]:.2f}' "
            "stroke='#0E2236' stroke-width='2.2' vector-effect='non-scaling-stroke'/>"
        )

    # Dimensioning (optional)
    if label_dims:
        if "d" in label_dims and depth_u > 0:
            draw_dim_line(svg, P0, u, depth_u, f"d = {label_dims['d']}", offset_px=12, outside=True)
        if "w" in label_dims and width_u > 0:
            draw_dim_line(svg, P0, v, width_u, f"w = {label_dims['w']}", offset_px=16, outside=True)
        if "h" in label_dims and height_u > 0:
            base = (P3[0] - 12, P3[1])
            draw_dim_line(svg, base, w, height_u, f"h = {label_dims['h']}", offset_px=0, outside=True)

    svg.append("</svg></div>")
    return "\n".join(svg)


def draw_unit_prism_svg(width_u: int, depth_u: int, height_u: int, tint="#7CC4FF"):
    return _iso_prism_svg(width_u, depth_u, height_u, tint=tint, show_grid=True)


def draw_two_prisms_svg(A, B):
    """Side-by-side prisms for composite problems (no CSS transforms to avoid sub-pixel jitter)."""
    wA, dA, hA, tA = A
    wB, dB, hB, tB = B
    a = _iso_prism_svg(wA, dA, hA, tint=tA, origin=(160, 76))
    b = _iso_prism_svg(wB, dB, hB, tint=tB, origin=(160, 76))
    return (
        "<div style='display:flex;gap:48px;justify-content:center;align-items:flex-start'>"
        f"{a}{b}</div>"
    )


def draw_labeled_prism_svg(w, d, h, tint="#7CC4FF", show_grid=False):
    return _iso_prism_svg(
        w, d, h,
        tint=tint,
        show_grid=show_grid,
        label_dims={"w": str(w), "d": str(d), "h": str(h)}
    )

# ============================================================
# =====================  ACTIVITY  ===========================
# ============================================================

def run():
    if "volume_level" not in st.session_state:
        st.session_state.volume_level = 1
    if "vol_problem" not in st.session_state:
        st.session_state.vol_problem = None
        st.session_state.answer_submitted = False
        st.session_state.user_answer = ""
        st.session_state.feedback = ""
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.consec_correct = 0

    st.markdown("**📚 Year 5 > Three-dimensional figures**")
    st.title("📦 Volume (Unit Cubes & Rectangular Prisms)")
    st.caption("Identify or compute the volume of 3D objects made from unit cubes, rectangular prisms, and composites.")
    st.markdown("---")

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        names = {1: "Intro", 2: "Core", 3: "Apply", 4: "Challenge"}
        st.markdown(f"**Difficulty:** {names[st.session_state.volume_level]}")
        st.progress(st.session_state.volume_level/4)
    with c2:
        if st.session_state.total_attempted:
            acc = st.session_state.total_correct / st.session_state.total_attempted * 100
            st.metric("Accuracy", f"{acc:.0f}%")
    with c3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

    if st.session_state.vol_problem is None:
        st.session_state.vol_problem = _make_problem(st.session_state.volume_level)
    prob = st.session_state.vol_problem

    st.markdown("### Question:")
    st.write(prob["prompt"])
    st.markdown(prob["svg"], unsafe_allow_html=True)

    with st.expander("💡 Hint", expanded=False):
        st.markdown(prob["hint"])

    st.markdown("Your answer:")
    col_a, _ = st.columns([2, 3])
    with col_a:
        disabled = st.session_state.answer_submitted
        v = st.text_input("Enter a number", value=st.session_state.user_answer,
                          label_visibility="collapsed", disabled=disabled,
                          placeholder="e.g., 24")
        if not disabled:
            st.session_state.user_answer = v

    st.caption(f"Units: **{prob['unit']}**")

    if st.button("✅ Submit", type="primary", disabled=st.session_state.answer_submitted):
        _check_answer()

    if st.session_state.answer_submitted:
        st.markdown(st.session_state.feedback, unsafe_allow_html=True)
        cc1, cc2 = st.columns([1, 1])
        with cc1:
            if st.button("🔄 Next Question", type="secondary"):
                _advance_level()
                _reset_problem()
                st.rerun()
        with cc2:
            if st.button("🆕 New Set (reset level)", type="secondary"):
                st.session_state.volume_level = 1
                _reset_problem()
                st.rerun()

# ============================================================
# ================  PROBLEM GENERATION  ======================
# ============================================================

def _make_problem(level: int):
    unit = "cubic units"

    if level == 1:
        dims = random.choice([(1,1,3), (2,1,2), (2,2,1), (3,1,1), (1,2,2)])
        w, d, h = dims
        vol = w*d*h
        svg = draw_unit_prism_svg(w, d, h, tint="#8FD36B")
        prompt = "What is the volume of this object?"
        hint = "- **Volume counts cubes.** Multiply the three side lengths: **V = length × width × height**."
        return dict(type="prism", dims=dims, answer=vol, unit=unit, svg=svg, prompt=prompt, hint=hint)

    if level == 2:
        w, d, h = [random.randint(2, 5) for _ in range(3)]
        vol = w*d*h
        svg = draw_labeled_prism_svg(w, d, h, tint="#7CC4FF", show_grid=False)
        prompt = "A rectangular prism is shown with its dimensions. What is its volume?"
        hint = f"- Use **V = w × d × h** → **{w} × {d} × {h}**."
        return dict(type="prism", dims=(w,d,h), answer=vol, unit=unit, svg=svg, prompt=prompt, hint=hint)

    if level == 3:
        w, d, h = random.randint(2,5), random.randint(2,4), random.randint(2,5)
        vol = w*d*h
        unknown = random.choice(["w","d","h"])
        labels = {"w": str(w), "d": str(d), "h": str(h)}
        labels[unknown] = "?"
        svg = _iso_prism_svg(w, d, h, tint="#FDBA74", show_grid=False, label_dims=labels)
        if unknown == "w":
            ans = vol//(d*h)
            prompt = f"The prism has **volume {vol}** and **depth {d}**, **height {h}**. What is the **width**?"
            hint = "Rearrange: **w = V ÷ (d × h)**."
        elif unknown == "d":
            ans = vol//(w*h)
            prompt = f"The prism has **volume {vol}** and **width {w}**, **height {h}**. What is the **depth**?"
            hint = "Rearrange: **d = V ÷ (w × h)**."
        else:
            ans = vol//(w*d)
            prompt = f"The prism has **volume {vol}** and **width {w}**, **depth {d}**. What is the **height**?"
            hint = "Rearrange: **h = V ÷ (w × d)**."
        return dict(type="missing", dims=(w,d,h), answer=ans, unit="units", svg=svg,
                    prompt=prompt, hint=hint, given_vol=vol)

    # Level 4 — Composite prisms
    w1,d1,h1 = random.randint(1,3), random.randint(2,4), random.randint(1,3)
    w2,d2,h2 = random.randint(1,3), random.randint(1,3), random.randint(2,4)
    vol = w1*d1*h1 + w2*d2*h2
    svg = draw_two_prisms_svg((w1,d1,h1,"#A7F3D0"), (w2,d2,h2,"#93C5FD"))
    prompt = "Two separate blocks are shown. What is the **total** volume?"
    hint = f"- Compute each: **V₁={w1}×{d1}×{h1}**, **V₂={w2}×{d2}×{h2}**. Then **add** them."
    return dict(type="composite", dims=((w1,d1,h1),(w2,d2,h2)),
                answer=vol, unit=unit, svg=svg, prompt=prompt, hint=hint)

# ============================================================
# ================  CHECKING & FEEDBACK  =====================
# ============================================================

def _check_answer():
    prob = st.session_state.vol_problem
    st.session_state.answer_submitted = True
    st.session_state.total_attempted += 1

    try:
        user = float(str(st.session_state.user_answer).strip())
    except Exception:
        st.session_state.feedback = "<p style='color:#b00020'>Please enter a valid number.</p>"
        return

    correct = float(prob["answer"])
    ok = abs(user - correct) < 1e-9

    if ok:
        st.session_state.total_correct += 1
        st.session_state.consec_correct += 1
        st.session_state.feedback = (
            f"<div style='background:#E7F7EB;border:1px solid #B7E1C1;padding:10px;border-radius:8px'>"
            f"✅ <b>Correct!</b> Answer: <b>{prob['answer']} {prob['unit']}</b></div>"
        )
    else:
        st.session_state.consec_correct = 0
        st.session_state.feedback = _explain_wrong(prob, user, correct)

def _explain_wrong(prob, user, correct):
    style = "background:#FFF6F6;border:1px solid #F5C2C7;padding:10px;border-radius:8px"
    if prob["type"] == "prism":
        w,d,h = prob["dims"]
        return (f"<div style='{style}'>❌ <b>Not quite.</b> "
                f"Use <b>V = w × d × h</b> → {w} × {d} × {h} = <b>{w*d*h} {prob['unit']}</b>."
                f"<br/><i>Your answer:</i> {user}</div>")
    if prob["type"] == "missing":
        w,d,h = prob["dims"]; V = prob["given_vol"]
        if prob["answer"] == V // (d*h):
            how = f"w = {V} ÷ ({d}×{h}) = <b>{prob['answer']} units</b>"
        elif prob["answer"] == V // (w*h):
            how = f"d = {V} ÷ ({w}×{h}) = <b>{prob['answer']} units</b>"
        else:
            how = f"h = {V} ÷ ({w}×{d}) = <b>{prob['answer']} units</b>"
        return (f"<div style='{style}'>❌ <b>Not quite.</b> {how}."
                f"<br/><i>Your answer:</i> {user}</div>")
    if prob["type"] == "composite":
        (w1,d1,h1),(w2,d2,h2) = prob["dims"]
        v1, v2 = w1*d1*h1, w2*d2*h2
        return (f"<div style='{style}'>❌ <b>Not quite.</b> "
                f"First block: {w1}×{d1}×{h1} = {v1}. Second: {w2}×{d2}×{h2} = {v2}. "
                f"Add: {v1}+{v2} = <b>{v1+v2} {prob['unit']}</b>."
                f"<br/><i>Your answer:</i> {user}</div>")
    return (f"<div style='{style}'>❌ Correct answer: <b>{correct} {prob['unit']}</b>.</div>")

def _advance_level():
    if st.session_state.consec_correct >= 3:
        st.session_state.consec_correct = 0
        st.session_state.volume_level = min(4, st.session_state.volume_level + 1)

def _reset_problem():
    st.session_state.vol_problem = None
    st.session_state.answer_submitted = False
    st.session_state.user_answer = ""
    st.session_state.feedback = ""
