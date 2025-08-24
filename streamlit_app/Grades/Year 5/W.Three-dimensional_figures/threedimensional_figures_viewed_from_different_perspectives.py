# three_dimensional_views.py
import streamlit as st
import random

# ----------------------------- Color helpers -----------------------------
def _clamp(v): return max(0, min(255, v))
def _hex_to_rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def _rgb_to_hex(rgb): return "#{:02x}{:02x}{:02x}".format(*rgb)
def _tint(hex_color, k=1.15):
    r,g,b=_hex_to_rgb(hex_color); return _rgb_to_hex((_clamp(int(r*k)), _clamp(int(g*k)), _clamp(int(b*k))))
def _shade(hex_color, k=0.85):
    r,g,b=_hex_to_rgb(hex_color); return _rgb_to_hex((_clamp(int(r*k)), _clamp(int(g*k)), _clamp(int(b*k))))

# ----------------------------- Isometric engine -----------------------------
def _iso(x, y, z, s, cx, cy):
    X = (x - y) * s + cx
    Y = (x + y) * 0.5 * s - z * s + cy
    return (X, Y)

def _poly(points): return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)

def _cube_faces(x, y, z, s, cx, cy, base):
    # top face
    A = _iso(x,   y,   z+1, s, cx, cy)
    B = _iso(x+1, y,   z+1, s, cx, cy)
    C = _iso(x+1, y+1, z+1, s, cx, cy)
    D = _iso(x,   y+1, z+1, s, cx, cy)
    # vertical corners
    D0 = _iso(x,   y+1, z, s, cx, cy)
    A0 = _iso(x,   y,   z, s, cx, cy)
    B0 = _iso(x+1, y,   z, s, cx, cy)
    C0 = _iso(x+1, y+1, z, s, cx, cy)
    top  = f'<polygon points="{_poly([A,B,C,D])}" fill="{_tint(base,1.18)}" stroke="#1f2937" stroke-width="1.2"/>'
    left = f'<polygon points="{_poly([D,C,C0,D0])}" fill="{base}" stroke="#1f2937" stroke-width="1.2"/>'
    right= f'<polygon points="{_poly([A,B,B0,A0])}" fill="{_shade(base,0.92)}" stroke="#1f2937" stroke-width="1.2"/>'
    return top, left, right

def draw_isometric(struct, base="#78b7ff", s=22):
    w, d, h = len(struct), len(struct[0]), len(struct[0][0])
    W = int((w + d) * s + 200)
    H = int((w + d) * 0.5 * s + h * s + 200)
    cx, cy = W // 2, 70 + h * s // 2

    # depth sort (back → front)
    order = []
    for x in range(w):
        for y in range(d):
            for z in range(h):
                if struct[x][y][z]:
                    order.append((x, y, z, x + y + z))
    order.sort(key=lambda t: t[3])

    layers = []
    layers.append(f'<ellipse cx="{cx:.1f}" cy="{cy + h*s*0.9:.1f}" rx="{(w+d)*s*0.55:.1f}" ry="{s*0.38:.1f}" fill="#00000022"/>')
    for x, y, z, _ in order:
        top, left, right = _cube_faces(x, y, z, s, cx, cy, base)
        layers += [left, right, top]

    return f"""
    <div style="text-align:center; margin:10px 0 16px 0;">
      <svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">
        {''.join(layers)}
      </svg>
    </div>
    """

# ----------------------------- Stick-figure viewer (no JS/defs) -----------------------------
def viewer_svg(view_from: str):
    active = "#10b981"  # green
    idle   = "#6b7280"  # gray
    colF = active if view_from=="front" else idle
    colS = active if view_from=="side"  else idle
    colT = active if view_from=="top"   else idle

    def fig(x, y, color):
        head = f'<circle cx="{x}" cy="{y-10}" r="5" fill="{color}"/>'
        body = f'<line x1="{x}" y1="{y-5}" x2="{x}" y2="{y+12}" stroke="{color}" stroke-width="3"/>'
        arms = f'<line x1="{x-8}" y1="{y+2}" x2="{x+8}" y2="{y+2}" stroke="{color}" stroke-width="3"/>'
        leg1 = f'<line x1="{x}" y1="{y+12}" x2="{x-8}" y2="{y+24}" stroke="{color}" stroke-width="3"/>'
        leg2 = f'<line x1="{x}" y1="{y+12}" x2="{x+8}" y2="{y+24}" stroke="{color}" stroke-width="3"/>'
        return head+body+arms+leg1+leg2

    def tiny_block(cx, cy, s=16, fill="#d9ecff"):
        top   = f'<polygon points="{cx-s},{cy-s/2} {cx},{cy-s} {cx+s},{cy-s/2} {cx},{cy}" fill="#eef6ff" stroke="#1f2937" stroke-width="1"/>'
        left  = f'<polygon points="{cx-s},{cy-s/2} {cx},{cy} {cx},{cy+s} {cx-s},{cy+s/2}" fill="{fill}" stroke="#1f2937" stroke-width="1"/>'
        right = f'<polygon points="{cx},{cy} {cx+s},{cy-s/2} {cx+s},{cy+s/2} {cx},{cy+s}" fill="#bddbff" stroke="#1f2937" stroke-width="1"/>'
        return top+left+right

    cx, cy = 100, 60
    ground = f'<ellipse cx="{cx}" cy="{cy+38}" rx="86" ry="10" fill="#00000015"/>'
    svg = f"""
    <div style="text-align:center; margin:6px 0;">
      <svg width="200" height="120" viewBox="0 0 200 120">
        {ground}
        {tiny_block(cx, cy)}
        {fig(cx,     cy+40, colF)}
        {fig(cx+70,  cy+10, colS)}
        {fig(cx,     cy-40, colT)}
        <text x="{cx}" y="{cy+56}"  text-anchor="middle" font-size="12" fill="{colF}">FRONT</text>
        <text x="{cx+70}" y="{cy+28}" text-anchor="middle" font-size="12" fill="{colS}">SIDE</text>
        <text x="{cx}" y="{cy-52}"  text-anchor="middle" font-size="12" fill="{colT}">TOP</text>
      </svg>
    </div>
    """
    return svg

# ----------------------------- Structures (many) -----------------------------
def empty(w,d,h,val=False): return [[[val for _ in range(h)] for _ in range(d)] for _ in range(w)]

def from_heightmap(Hmap, max_h):
    w, d = len(Hmap), len(Hmap[0])
    S = empty(w, d, max_h)
    for x in range(w):
        for y in range(d):
            for z in range(min(Hmap[x][y], max_h)):
                S[x][y][z] = True
    return S

def solid_cuboid(w,d,h): return [[[True for _ in range(h)] for _ in range(d)] for _ in range(w)]

def stairs(axis="x", w=4, d=3, h=3):
    hm = [[0]*d for _ in range(w)]
    if axis == "x":
        for x in range(w):
            for y in range(d): hm[x][y] = 1 + int((x/(max(1,w-1)))*(h-1))
    else:
        for x in range(w):
            for y in range(d): hm[x][y] = 1 + int((y/(max(1,d-1)))*(h-1))
    return from_heightmap(hm,h)

def L_block(w=4,d=4,h=3, bar=1):
    hm = [[0]*d for _ in range(w)]
    for x in range(w):
        for y in range(bar): hm[x][y] = max(1, h//2)
    for x in range(bar):
        for y in range(d): hm[x][y] = h
    return from_heightmap(hm,h)

def U_hall(w=5,d=4,h=3):
    S = empty(w,d,h)
    for x in range(w):
        for z in range(h-1):
            S[x][0][z] = True; S[x][d-1][z] = True
    for y in range(d):
        for z in range(h-1): S[0][y][z] = True
    for x in range(w): S[x][0][h-1] = True
    return S

def bridge(w=5,d=3,h=4):
    S = empty(w,d,h); mid = d//2
    for z in range(h-1):
        S[1][mid][z] = True; S[w-2][mid][z] = True
    for x in range(1,w-1): S[x][mid][h-1] = True
    return S

def ring_plate(w=5,d=5,h=2,thick=1):
    hm = [[0]*d for _ in range(w)]
    for x in range(w):
        for y in range(d):
            edge = (x < thick or x >= w-thick or y < thick or y >= d-thick)
            hm[x][y] = 1 if edge else 0
    return from_heightmap(hm,h)

def step_pyramid(n=5, h=4):
    c = n//2; hm = [[0]*n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            r = max(abs(x-c), abs(y-c))
            hm[x][y] = max(0, h - r)
    return from_heightmap(hm, h)

def plus_tower(w=5,d=5,h=4):
    hm = [[0]*d for _ in range(w)]
    cx, cy = w//2, d//2
    for x in range(w): hm[x][cy] = 1
    for y in range(d): hm[w//2][y] = 1
    hm[cx][cy] = h
    return from_heightmap(hm,h)

def wedge_x(w=4,d=3,h=3):
    hm = [[0]*d for _ in range(w)]
    for x in range(w):
        for y in range(d): hm[x][y] = 1 + int((x/(max(1,w-1)))*(h-1))
    return from_heightmap(hm,h)

def corner_peak(w=4,d=4,h=4):
    hm = [[0]*d for _ in range(w)]
    for x in range(w):
        for y in range(d):
            hm[x][y] = max(1, h - (x+y)//2)
    return from_heightmap(hm,h)

def random_terrace(w=5,d=4,h=4):
    hm = [[random.randint(0,h) for _ in range(d)] for _ in range(w)]
    # ensure at least one cube
    if sum(sum(1 for v in row if v>0) for row in hm)==0:
        hm[random.randrange(w)][random.randrange(d)] = random.randint(1,h)
    return from_heightmap(hm,h)

def hollow_box(n=5, h=3):
    S = empty(n,n,h)
    for x in range(n):
        for y in range(n):
            for z in range(h):
                edge = (x in (0,n-1) or y in (0,n-1) or z==0 or z==h-1)
                if edge: S[x][y][z] = True
    return S

# ----------------------------- Projections -----------------------------
def proj_front(struct):
    w,d,h = len(struct), len(struct[0]), len(struct[0][0])
    grid = [[0]*h for _ in range(w)]
    for x in range(w):
        maxh = 0
        for y in range(d):
            for z in range(h):
                if struct[x][y][z]: maxh = max(maxh, z+1)
        for z in range(maxh): grid[x][h-1-z] = 1
    return grid

def proj_side(struct):
    w,d,h = len(struct), len(struct[0]), len(struct[0][0])
    grid = [[0]*h for _ in range(d)]
    for y in range(d):
        maxh = 0
        for x in range(w):
            for z in range(h):
                if struct[x][y][z]: maxh = max(maxh, z+1)
        for z in range(maxh): grid[y][h-1-z] = 1
    return grid

def proj_top(struct):
    w,d,h = len(struct), len(struct[0]), len(struct[0][0])
    grid = [[0]*d for _ in range(w)]
    for x in range(w):
        for y in range(d):
            grid[x][y] = 1 if any(struct[x][y][z] for z in range(h)) else 0
    return grid

# ----------------------------- Grid renderer -----------------------------
def draw_grid(grid, cell=26, pad=10, filled="#27485c", empty="#9fbad0", stroke="#1f2937"):
    cols, rows = len(grid), len(grid[0])
    W = cols*cell + pad*2
    H = rows*cell + pad*2
    rects = []
    for x in range(cols):
        for y in range(rows):
            fill = filled if grid[x][y] else empty
            rx = pad + x*cell; ry = pad + y*cell
            rects.append(f'<rect x="{rx}" y="{ry}" width="{cell}" height="{cell}" fill="{fill}" stroke="{stroke}" stroke-width="1.2" />')
    return f"""
    <div style="text-align:center; margin:6px 0 14px 0;">
      <svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">
        {''.join(rects)}
      </svg>
    </div>
    """

# ----------------------------- Problem generator -----------------------------
def _transpose(grid):
    cols, rows = len(grid), len(grid[0])
    t = [[0]*cols for _ in range(rows)]
    for x in range(cols):
        for y in range(rows):
            t[y][x] = grid[x][y]
    return t

def _jitter_grid(grid):
    cols, rows = len(grid), len(grid[0])
    g = [[grid[x][y] for y in range(rows)] for x in range(cols)]
    flips = max(1, (cols*rows)//12)
    for _ in range(flips):
        x = random.randrange(cols); y = random.randrange(rows)
        g[x][y] = 1 - g[x][y]
    return g

def make_problem(level: int):
    palettes = ["#78b7ff", "#90c2ff", "#8ad5c1", "#ffd27f", "#f7b3d2", "#b1f0a5"]
    base = random.choice(palettes)

    if level == 1:
        choices = [
            lambda: solid_cuboid(3,3,2),
            lambda: solid_cuboid(4,2,2),
            lambda: stairs(axis=random.choice(["x","y"]), w=3,d=3,h=3),
            lambda: L_block(4,3,3, bar=1),
        ]
    elif level == 2:
        choices = [
            lambda: stairs(axis=random.choice(["x","y"]), w=4,d=3,h=3),
            lambda: L_block(4,4,3, bar=1),
            lambda: ring_plate(5,5,2,thick=1),
            lambda: wedge_x(4,3,3),
            lambda: solid_cuboid(3,3,3),
        ]
    elif level == 3:
        choices = [
            lambda: U_hall(5,4,3),
            lambda: bridge(5,3,4),
            lambda: plus_tower(5,5,4),
            lambda: step_pyramid(5,4),
            lambda: hollow_box(5,3),
            lambda: corner_peak(4,4,4),
        ]
    else:
        choices = [
            lambda: random_terrace(5,4,4),
            lambda: random_terrace(6,4,4),
            lambda: step_pyramid(5,4),
            lambda: plus_tower(5,5,4),
            lambda: U_hall(6,4,4),
            lambda: hollow_box(6,3),
            lambda: corner_peak(5,5,4),
        ]

    struct = random.choice(choices)()
    view = random.choice(["front","side","top"])
    object_svg = draw_isometric(struct, base=base, s=22)

    if view == "front":
        correct = proj_front(struct)
        wrong = proj_side(struct) if random.random()<0.5 else _jitter_grid(correct)
    elif view == "side":
        correct = proj_side(struct)
        wrong = proj_front(struct) if random.random()<0.5 else _jitter_grid(correct)
    else:
        correct = proj_top(struct)
        wrong = _transpose(correct) if random.random()<0.5 else _jitter_grid(correct)

    options = [
        {"label": "Option 1", "svg": draw_grid(correct), "correct": True},
        {"label": "Option 2", "svg": draw_grid(wrong),   "correct": False},
    ]
    random.shuffle(options)
    correct_idx = next(i for i,o in enumerate(options) if o["correct"])

    title = f"If you look at this object from the {view}, what will you see?"
    return {
        "title": title,
        "view_from": view,
        "viewer": viewer_svg(view),
        "object_svg": object_svg,
        "options": options,
        "correct_index": correct_idx
    }

# ----------------------------- Streamlit app -----------------------------
def run():
    st.markdown("Identify how 3D cube structures look from the **front**, **side**, or **top**.")
    if "view_lvl" not in st.session_state:
        st.session_state.view_lvl = 1
        st.session_state.problem = None
        st.session_state.sel = None
        st.session_state.answered = False
        st.session_state.show_feedback = False
        st.session_state.correct_count = 0
        st.session_state.total = 0

    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        names = {1:"Simple Shapes", 2:"Medium Shapes", 3:"Complex Shapes", 4:"Very Complex"}
        st.markdown(f"**Difficulty Level:** {names[st.session_state.view_lvl]}")
        st.progress(st.session_state.view_lvl/4)  # no 'text=' for compatibility
        st.caption(f"Level {st.session_state.view_lvl}/4")
    with col2:
        if st.session_state.total:
            acc = (st.session_state.correct_count/st.session_state.total)*100
            st.metric("Accuracy", f"{acc:.0f}%")
    with col3:
        if st.button("← Back"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

    if st.session_state.problem is None:
        st.session_state.problem = make_problem(st.session_state.view_lvl)

    p = st.session_state.problem

    st.markdown("### Question:")
    st.markdown(f"**{p['title']}**")

    # Object + viewer side-by-side
    obj_col, viewer_col = st.columns([4,2])
    with obj_col:
        st.markdown(p["object_svg"], unsafe_allow_html=True)
    with viewer_col:
        st.markdown("**Viewer position**")
        st.markdown(p["viewer"], unsafe_allow_html=True)
        st.caption("The green stick figure shows where the view is taken from.")

    # Answer options below the shapes
    st.write("")
    c1, c2 = st.columns(2)
    for i, opt in enumerate(p["options"]):
        with (c1 if i == 0 else c2):
            st.markdown(opt["svg"], unsafe_allow_html=True)
            if st.button(f"Select {opt['label']}", key=f"pick_{i}", use_container_width=True, disabled=st.session_state.answered):
                st.session_state.sel = i

    st.write("")
    mid = st.columns([1,2,1])[1]
    with mid:
        disabled = st.session_state.answered or st.session_state.sel is None
        if st.button("✅ Submit", use_container_width=True, disabled=disabled):
            st.session_state.answered = True
            st.session_state.show_feedback = True
            st.session_state.total += 1
            if st.session_state.sel == p["correct_index"]:
                st.session_state.correct_count += 1
                if (st.session_state.correct_count % 3 == 0) and st.session_state.view_lvl < 4:
                    st.session_state.view_lvl += 1
            else:
                if st.session_state.view_lvl > 1:
                    st.session_state.view_lvl -= 1

    if st.session_state.show_feedback:
        if st.session_state.sel == p["correct_index"]:
            st.success("🎉 Correct! Great spatial reasoning.")
        else:
            st.error("❌ Not quite. Match the projection to the highlighted (green) viewer position.")
            with st.expander("Why this view is correct"):
                st.markdown("""
                - **Front view**: width × height from the stick figure at **FRONT**.
                - **Side view**: depth × height from the stick figure at **SIDE**.
                - **Top view**: footprint (width × depth) from the stick figure **above** the block.
                """)

    if st.session_state.answered:
        mid2 = st.columns([1,2,1])[1]
        with mid2:
            if st.button("🔄 Next Question", use_container_width=True):
                st.session_state.problem = None
                st.session_state.sel = None
                st.session_state.answered = False
                st.session_state.show_feedback = False
                st.rerun()

# if running standalone:
# if __name__ == "__main__":
#     run()
