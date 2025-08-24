import math
import random
import textwrap
import streamlit as st
import streamlit.components.v1 as components

# =============================
# Responsive HTML/SVG renderer
# =============================
def show_html(html: str, height: int = 300, max_width: int = 420):
    """Render raw SVG/HTML responsively with non-scaling strokes."""
    wrapped = f"""
<div class="svgfix" style="display:flex;justify-content:center">
  <style>
    .svgfix svg {{
      width: 100% !important;
      height: auto !important;
      max-width: {max_width}px;
      display: block;
    }}
    .svgfix svg * {{
      vector-effect: non-scaling-stroke;
      shape-rendering: geometricPrecision;
      stroke-linejoin: round;
      stroke-linecap: round;
    }}
  </style>
  {textwrap.dedent(html)}
</div>
"""
    components.html(wrapped, height=height, scrolling=False)

# =============================
# Geometry helpers
# =============================
def _poly_points(cx: float, cy: float, r: float, sides: int, rotate_deg: float = -90) -> str:
    """Return 'x,y x,y ...' for a regular polygon (string form)."""
    pts = []
    rot = math.radians(rotate_deg)
    for i in range(sides):
        ang = rot + 2 * math.pi * i / sides
        pts.append(f"{cx + r*math.cos(ang):.2f},{cy + r*math.sin(ang):.2f}")
    return " ".join(pts)

def _poly_points_list(cx: float, cy: float, r: float, sides: int, rotate_deg: float = -90):
    """Return [(x,y), ...] for a regular polygon (list form)."""
    pts = []
    rot = math.radians(rotate_deg)
    for i in range(sides):
        ang = rot + 2 * math.pi * i / sides
        pts.append((cx + r*math.cos(ang), cy + r*math.sin(ang)))
    return pts

def _n_gon(cx, cy, r, sides, fill, stroke="#333", sw=2, rotate=-90, extra=""):
    return f'<polygon points="{_poly_points(cx, cy, r, sides, rotate)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

# =============================
# App
# =============================
def run():
    """
    Nets of 3D Figures — now includes cylinder, cone, sphere, rectangular & pentagonal pyramids,
    with options shown BELOW each image.
    """
    if "nets_difficulty" not in st.session_state:
        st.session_state.nets_difficulty = 1  # 1 Basic, 2 Prisms & Pyramids, 3 Complex
    if "current_nets_question" not in st.session_state:
        st.session_state.current_nets_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.nets_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.selected_option = None

    # Header
    st.markdown("**📚 Year 5 > W. Three-dimensional figures**")
    st.title("📐 Nets of Three-Dimensional Figures")
    st.markdown("*Learn to identify and match 2D nets with their 3D shapes*")
    st.markdown("---")

    # Difficulty strip
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        names = {1: "Basic Shapes", 2: "Prisms & Pyramids", 3: "Complex Shapes"}
        st.markdown(f"**Difficulty Level:** {names[st.session_state.nets_difficulty]}")
        st.progress((st.session_state.nets_difficulty - 1) / 2, text=f"Level {st.session_state.nets_difficulty}/3")
    with col2:
        dots = {1: "🟢", 2: "🟡", 3: "🔴"}
        st.markdown(f"**{dots[st.session_state.nets_difficulty]} {names[st.session_state.nets_difficulty]}**")
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

    # Set up question
    if st.session_state.current_nets_question is None:
        generate_new_nets_question()

    display_nets_question()

    # Footer help
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        - You’ll either match a **net → shape** or **shape → net**.
        - **Count faces** and **visualize folding**.
        - Quick checks:
            - **Cube:** 6 squares
            - **Rectangular prism:** 6 rectangles
            - **Triangular prism:** 2 triangles + 3 rectangles
            - **Square/Rectangular/Pentagonal pyramids:** 1 base + triangular faces all around
            - **Cylinder:** 1 rectangle + 2 circles
            - **Cone:** 1 circle + 1 sector
            - **Sphere:** gores (curved “petals”) rather than flat polygon faces
        """)

# =============================
# Question generation
# =============================
def generate_new_nets_question():
    difficulty = st.session_state.nets_difficulty
    qtype = random.choice(["net_to_shape", "shape_to_net"])

    if difficulty == 1:
        # Add cylinder, cone, sphere to basics
        if qtype == "net_to_shape":
            scenarios = [
                {"net": draw_cube_net_cross(),
                 "options": [("cube", "Cube", draw_cube_3d()),
                             ("pyramid", "Square Pyramid", draw_square_pyramid_3d())],
                 "correct": 0,
                 "explanation": "Cross of 6 squares folds to a cube."},

                {"net": draw_rectangular_prism_net(),
                 "options": [("rect", "Rectangular Prism", draw_rectangular_prism_3d()),
                             ("tri", "Triangular Prism", draw_triangular_prism_3d())],
                 "correct": 0,
                 "explanation": "Six rectangles arranged as a cross → cuboid."},

                {"net": draw_triangular_prism_net(),
                 "options": [("cube", "Cube", draw_cube_3d()),
                             ("tri", "Triangular Prism", draw_triangular_prism_3d())],
                 "correct": 1,
                 "explanation": "Three rectangles + triangles on ends → triangular prism."},

                {"net": draw_cylinder_net(),
                 "options": [("cyl", "Cylinder", draw_cylinder_3d()),
                             ("cone", "Cone", draw_cone_3d())],
                 "correct": 0,
                 "explanation": "A rectangle with a circle at each end → cylinder."},

                {"net": draw_cone_net(),
                 "options": [("cyl", "Cylinder", draw_cylinder_3d()),
                             ("cone", "Cone", draw_cone_3d())],
                 "correct": 1,
                 "explanation": "Circle + sector (pie-slice) → cone."},

                {"net": draw_sphere_net(),
                 "options": [("sphere", "Sphere", draw_sphere_3d()),
                             ("cube", "Cube", draw_cube_3d())],
                 "correct": 0,
                 "explanation": "A sphere is made from several curved gores (orange-peel style)."},
            ]
        else:
            scenarios = [
                {"shape": draw_cube_3d(), "shape_name": "Cube",
                 "options": [("ok", draw_cube_net_cross()),
                             ("no", draw_square_pyramid_net())],
                 "correct": 0, "explanation": "A cube needs 6 squares; the cross net fits."},

                {"shape": draw_triangular_prism_3d(), "shape_name": "Triangular Prism",
                 "options": [("ok", draw_triangular_prism_net()),
                             ("no", draw_cube_net_t())],
                 "correct": 0, "explanation": "2 triangles + 3 rectangles → triangular prism net."},

                {"shape": draw_rectangular_prism_3d(), "shape_name": "Rectangular Prism",
                 "options": [("no", draw_triangular_prism_net()),
                             ("ok", draw_rectangular_prism_net())],
                 "correct": 1, "explanation": "6 rectangles arranged properly → cuboid."},

                {"shape": draw_cylinder_3d(), "shape_name": "Cylinder",
                 "options": [("ok", draw_cylinder_net()),
                             ("no", draw_cone_net())],
                 "correct": 0, "explanation": "Cylinder net = rectangle + 2 circles."},

                {"shape": draw_cone_3d(), "shape_name": "Cone",
                 "options": [("no", draw_cylinder_net()),
                             ("ok", draw_cone_net())],
                 "correct": 1, "explanation": "Cone net = circle + sector."},

                {"shape": draw_sphere_3d(), "shape_name": "Sphere",
                 "options": [("ok", draw_sphere_net()),
                             ("no", draw_cube_net_cross())],
                 "correct": 0, "explanation": "Sphere uses gores; not flat polygons like a cube."},
            ]

    elif difficulty == 2:
        if qtype == "net_to_shape":
            scenarios = [
                {"net": draw_square_pyramid_net(),
                 "options": [("pyr", "Square Pyramid", draw_square_pyramid_3d()),
                             ("cube", "Cube", draw_cube_3d())],
                 "correct": 0, "explanation": "1 square + 4 triangles → square pyramid."},

                {"net": draw_rectangular_pyramid_net(),
                 "options": [("rectp", "Rectangular Pyramid", draw_rectangular_pyramid_3d()),
                             ("pentp", "Pentagonal Pyramid", draw_pentagonal_pyramid_3d())],
                 "correct": 0, "explanation": "Rectangle base + 4 triangles → rectangular pyramid."},

                {"net": draw_pentagonal_pyramid_net(),
                 "options": [("pentp", "Pentagonal Pyramid", draw_pentagonal_pyramid_3d()),
                             ("hexp", "Hexagonal Pyramid", draw_hexagonal_pyramid_3d())],
                 "correct": 0, "explanation": "Pentagon base + 5 triangles → pentagonal pyramid."},

                {"net": draw_pentagonal_prism_net(),
                 "options": [("pentpr", "Pentagonal Prism", draw_pentagonal_prism_3d()),
                             ("hexpr", "Hexagonal Prism", draw_hexagonal_prism_3d())],
                 "correct": 0, "explanation": "2 pentagons + 5 rectangles → pentagonal prism."},

                {"net": draw_cube_net_t(),
                 "options": [("cube", "Cube", draw_cube_3d()),
                             ("rect", "Rectangular Prism", draw_rectangular_prism_3d())],
                 "correct": 0, "explanation": "Classic T-shaped cube net."},
            ]
        else:
            scenarios = [
                {"shape": draw_square_pyramid_3d(), "shape_name": "Square Pyramid",
                 "options": [("ok", draw_square_pyramid_net()),
                             ("no", draw_cube_net_cross())],
                 "correct": 0, "explanation": "Square base + 4 triangles."},

                {"shape": draw_rectangular_pyramid_3d(), "shape_name": "Rectangular Pyramid",
                 "options": [("ok", draw_rectangular_pyramid_net()),
                             ("no", draw_pentagonal_pyramid_net())],
                 "correct": 0, "explanation": "Rectangle base + 4 triangles."},

                {"shape": draw_pentagonal_pyramid_3d(), "shape_name": "Pentagonal Pyramid",
                 "options": [("no", draw_square_pyramid_net()),
                             ("ok", draw_pentagonal_pyramid_net())],
                 "correct": 1, "explanation": "Pentagon base + 5 triangles."},

                {"shape": draw_pentagonal_prism_3d(), "shape_name": "Pentagonal Prism",
                 "options": [("no", draw_hexagonal_prism_net()),
                             ("ok", draw_pentagonal_prism_net())],
                 "correct": 1, "explanation": "2 pentagons + 5 rectangles."},

                {"shape": draw_cube_3d(), "shape_name": "Cube",
                 "options": [("ok", draw_cube_net_t()),
                             ("no", draw_triangular_pyramid_net())],
                 "correct": 0, "explanation": "This T-shape folds to a cube."},
            ]

    else:
        if qtype == "net_to_shape":
            scenarios = [
                {"net": draw_octahedron_net(),
                 "options": [("oct", "Octahedron", draw_octahedron_3d()),
                             ("cube", "Cube", draw_cube_3d())],
                 "correct": 0, "explanation": "Eight triangles → octahedron."},

                {"net": draw_cube_net_l(),
                 "options": [("pyr", "Square Pyramid", draw_square_pyramid_3d()),
                             ("cube", "Cube", draw_cube_3d())],
                 "correct": 1, "explanation": "L-shaped arrangement for a cube."},

                {"net": draw_dodecahedron_net_simplified(),
                 "options": [("dod", "Dodecahedron", draw_dodecahedron_3d()),
                             ("ico", "Icosahedron", draw_icosahedron_3d())],
                 "correct": 0, "explanation": "Twelve regular pentagons → dodecahedron (simplified view)."},

                {"net": draw_hexagonal_prism_net(),
                 "options": [("hexp", "Hexagonal Prism", draw_hexagonal_prism_3d()),
                             ("octp", "Octagonal Prism", draw_octagonal_prism_3d())],
                 "correct": 0, "explanation": "2 hexagons + 6 rectangles → hexagonal prism."},
            ]
        else:
            scenarios = [
                {"shape": draw_octahedron_3d(), "shape_name": "Octahedron",
                 "options": [("no", draw_cube_net_cross()),
                             ("ok", draw_octahedron_net())],
                 "correct": 1, "explanation": "Strip of 6 triangles + 2 more."},

                {"shape": draw_cube_3d(), "shape_name": "Cube",
                 "options": [("ok", draw_cube_net_l()),
                             ("no", draw_square_pyramid_net())],
                 "correct": 0, "explanation": "Another valid cube net."},

                {"shape": draw_hexagonal_prism_3d(), "shape_name": "Hexagonal Prism",
                 "options": [("ok", draw_hexagonal_prism_net()),
                             ("no", draw_pentagonal_prism_net())],
                 "correct": 0, "explanation": "2 hexagons + 6 rectangles."},
            ]

    scenario = random.choice(scenarios)
    st.session_state.nets_data = {"scenario": scenario, "question_type": qtype, "correct_answer": scenario["correct"]}
    st.session_state.correct_answer = scenario["correct"]
    st.session_state.current_nets_question = "Which figure will this net make?" if qtype == "net_to_shape" else "Which net will make this figure?"

# =============================
# Display & feedback (buttons BELOW the images)
# =============================
def display_nets_question():
    data = st.session_state.nets_data
    if not data:
        return
    sc = data["scenario"]
    qtype = data["question_type"]

    st.markdown("### 🎯 Question:")
    st.markdown(f"**{st.session_state.current_nets_question}**")

    if qtype == "net_to_shape":
        # Show the net
        show_html(sc["net"], height=380, max_width=560)

        # Options: image first, then the button (so options are BELOW images)
        cols = st.columns(len(sc["options"]))
        for i, (_k, name, svg) in enumerate(sc["options"]):
            with cols[i]:
                show_html(svg, height=260, max_width=240)
                st.markdown(f"<div style='text-align:center;margin-top:6px'>{name}</div>", unsafe_allow_html=True)
                st.button(f"Select {name}", key=f"option_{i}", use_container_width=True,
                          on_click=select_option, args=(i,))
                if st.session_state.selected_option == i:
                    st.success("✓ Selected")
    else:
        # Show the 3D shape
        st.markdown(f"#### {sc['shape_name']}")
        show_html(sc["shape"], height=300, max_width=280)

        # Options (nets): image first, then button
        cols = st.columns(len(sc["options"]))
        for i, (_k, net_svg) in enumerate(sc["options"]):
            with cols[i]:
                show_html(net_svg, height=360, max_width=560)
                st.button("Select", key=f"option_{i}", use_container_width=True,
                          on_click=select_option, args=(i,))
                if st.session_state.selected_option == i:
                    st.success("✓ Selected")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("✅ Submit", type="primary", use_container_width=True):
            if st.session_state.selected_option is not None:
                st.session_state.answer_submitted = True
                st.session_state.show_feedback = True
                handle_feedback()
            else:
                st.warning("Please select an option first!")

    if st.session_state.show_feedback:
        show_feedback()

    if st.session_state.answer_submitted:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def select_option(i: int): st.session_state.selected_option = i

def handle_feedback():
    if st.session_state.selected_option == st.session_state.correct_answer:
        st.success("Nice! That's right.")
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        if st.session_state.consecutive_correct >= 3:
            old = st.session_state.nets_difficulty
            st.session_state.nets_difficulty = min(old + 1, 3)
            if st.session_state.nets_difficulty > old:
                st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        if st.session_state.consecutive_wrong >= 2:
            old = st.session_state.nets_difficulty
            st.session_state.nets_difficulty = max(old - 1, 1)
            if st.session_state.nets_difficulty < old:
                st.session_state.consecutive_wrong = 0

def show_feedback():
    sc = st.session_state.nets_data["scenario"]
    if st.session_state.selected_option == st.session_state.correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        st.info(f"✅ {sc['explanation']}")
        if st.session_state.consecutive_correct >= 2:
            st.info("🌟 Great streak! One more correct answer to level up!")
    else:
        st.error("❌ **Not quite right.**")
        st.warning(f"The correct answer was option {st.session_state.correct_answer + 1}.")
        st.info(f"📖 {sc['explanation']}")
        with st.expander("💡 **Tips for Understanding Nets**", expanded=True):
            st.markdown("Count the faces, check their shapes, imagine folding, and look for symmetry.")

def reset_question_state():
    st.session_state.current_nets_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.nets_data = {}
    st.session_state.selected_option = None

# =============================
# SVG: Nets (regular polygons where needed)
# =============================
def draw_cube_net_cross():
    return '''
    <svg width="300" height="300" viewBox="-150 -150 300 300">
      <rect x="-25" y="-125" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="-125" y="-25" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="-25"  y="-25" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="75"   y="-25" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="-25"  y="25"  width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="-25"  y="75"  width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
    </svg>
    '''

def draw_cube_net_t():
    return '''
    <svg width="300" height="250" viewBox="-150 -125 300 250">
      <rect x="-25" y="-100" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="25"  y="-100" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="-125" y="-50" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="-75"  y="-50" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="-25"  y="-50" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="25"   y="-50" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
    </svg>
    '''

def draw_cube_net_l():
    return '''
    <svg width="300" height="300" viewBox="-150 -150 300 300">
      <rect x="-25" y="-100" width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="-25" y="-50"  width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="-25" y="0"    width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="-25" y="50"   width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="25"  y="50"   width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
      <rect x="75"  y="50"   width="50" height="50" fill="#90EE90" stroke="#333" stroke-width="2"/>
    </svg>
    '''

def draw_triangular_pyramid_net():
    return '''
    <svg width="300" height="250" viewBox="-150 -125 300 250">
      <path d="M 0,-100 L 120,80 L -120,80 Z" fill="#DDA0DD" stroke="#333" stroke-width="2"/>
      <line x1="0" y1="-100" x2="0" y2="80" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="0" y1="80" x2="60" y2="-10" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="0" y1="80" x2="-60" y2="-10" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
    </svg>
    '''

def draw_square_pyramid_net():
    return '''
    <svg width="300" height="300" viewBox="-150 -150 300 300">
      <rect x="-40" y="-40" width="80" height="80" fill="#F0E68C" stroke="#333" stroke-width="2"/>
      <path d="M -40,-40 L 40,-40 L 0,-100 Z" fill="#F0E68C" stroke="#333" stroke-width="2"/>
      <path d="M 40,-40 L 40,40 L 100,0 Z" fill="#F0E68C" stroke="#333" stroke-width="2"/>
      <path d="M 40,40 L -40,40 L 0,100 Z" fill="#F0E68C" stroke="#333" stroke-width="2"/>
      <path d="M -40,40 L -40,-40 L -100,0 Z" fill="#F0E68C" stroke="#333" stroke-width="2"/>
    </svg>
    '''

def draw_rectangular_pyramid_net():
    # Base rectangle with four triangles around
    return '''
    <svg width="360" height="300" viewBox="-180 -150 360 300">
      <rect x="-70" y="-35" width="140" height="70" fill="#F8B88B" stroke="#333" stroke-width="2"/>
      <path d="M -70,-35 L 70,-35 L 0,-110 Z" fill="#F8B88B" stroke="#333" stroke-width="2"/>
      <path d="M 70,-35 L 70,35 L 140,0 Z"  fill="#F8B88B" stroke="#333" stroke-width="2"/>
      <path d="M 70,35  L -70,35 L 0,110 Z" fill="#F8B88B" stroke="#333" stroke-width="2"/>
      <path d="M -70,35 L -70,-35 L -140,0 Z" fill="#F8B88B" stroke="#333" stroke-width="2"/>
    </svg>
    '''

def draw_pentagonal_pyramid_net():
    # Pentagonal base + 5 outward triangles (computed)
    base_pts = _poly_points_list(0, 0, 40, 5)  # CCW, one vertex up
    polys = [_n_gon(0, 0, 40, 5, "#F5DEB3")]
    # build triangles on each edge
    tri_paths = []
    for i in range(5):
        x1, y1 = base_pts[i]
        x2, y2 = base_pts[(i + 1) % 5]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # outward direction ~ from center (0,0) to midpoint
        vx, vy = mx, my
        vlen = (vx**2 + vy**2) ** 0.5 or 1.0
        nx, ny = vx / vlen, vy / vlen
        ax, ay = mx + nx * 55, my + ny * 55   # apex
        tri_paths.append(f'<path d="M {x1:.1f},{y1:.1f} L {x2:.1f},{y2:.1f} L {ax:.1f},{ay:.1f} Z" fill="#F5DEB3" stroke="#333" stroke-width="2"/>')
    return f'''
    <svg width="360" height="320" viewBox="-180 -160 360 320">
      {''.join(tri_paths)}
      {_n_gon(0, 0, 40, 5, "#F5DEB3")}
    </svg>
    '''

def draw_triangular_prism_net():
    return '''
    <svg width="350" height="200" viewBox="-175 -100 350 200">
      <rect x="-150" y="-30" width="80" height="60" fill="#98FB98" stroke="#333" stroke-width="2"/>
      <rect x="-70"  y="-30" width="80" height="60" fill="#98FB98" stroke="#333" stroke-width="2"/>
      <rect x="10"   y="-30" width="80" height="60" fill="#98FB98" stroke="#333" stroke-width="2"/>
      <path d="M -70,-30 L 10,-30 L -30,-80 Z" fill="#98FB98" stroke="#333" stroke-width="2"/>
      <path d="M -70,30  L 10,30  L -30,80  Z" fill="#98FB98" stroke="#333" stroke-width="2"/>
    </svg>
    '''

def draw_rectangular_prism_net():
    return '''
    <svg width="350" height="250" viewBox="-175 -125 350 250">
      <rect x="-30"  y="-100" width="60" height="40" fill="#87CEEB" stroke="#333" stroke-width="2"/>
      <rect x="-150" y="-20"  width="60" height="40" fill="#87CEEB" stroke="#333" stroke-width="2"/>
      <rect x="-90"  y="-20"  width="60" height="40" fill="#87CEEB" stroke="#333" stroke-width="2"/>
      <rect x="-30"  y="-20"  width="60" height="40" fill="#87CEEB" stroke="#333" stroke-width="2"/>
      <rect x="30"   y="-20"  width="60" height="40" fill="#87CEEB" stroke="#333" stroke-width="2"/>
      <rect x="-30"  y="60"   width="60" height="40" fill="#87CEEB" stroke="#333" stroke-width="2"/>
    </svg>
    '''

def draw_pentagonal_prism_net():
    pent_top  = _n_gon(0, -60, 32, 5, "#FFE4B5")
    pent_bot  = _n_gon(0,  60, 32, 5, "#FFE4B5")
    return f'''
    <svg width="420" height="200" viewBox="-210 -100 420 200">
      <rect x="-180" y="-20" width="60" height="40" fill="#FFE4B5" stroke="#333" stroke-width="2"/>
      <rect x="-120" y="-20" width="60" height="40" fill="#FFE4B5" stroke="#333" stroke-width="2"/>
      <rect x="-60"  y="-20" width="60" height="40" fill="#FFE4B5" stroke="#333" stroke-width="2"/>
      <rect x="0"    y="-20" width="60" height="40" fill="#FFE4B5" stroke="#333" stroke-width="2"/>
      <rect x="60"   y="-20" width="60" height="40" fill="#FFE4B5" stroke="#333" stroke-width="2"/>
      {pent_top}
      {pent_bot}
      <line x1="-120" y1="-20" x2="-120" y2="20" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="-60"  y1="-20" x2="-60"  y2="20" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="0"    y1="-20" x2="0"    y2="20" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="60"   y1="-20" x2="60"   y2="20" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
    </svg>
    '''

def draw_hexagonal_prism_net():
    hex_top = _n_gon(0, -64, 34, 6, "#B0E0E6")
    hex_bot = _n_gon(0,  64, 34, 6, "#B0E0E6")
    return f'''
    <svg width="480" height="220" viewBox="-240 -110 480 220">
      <rect x="-210" y="-20" width="60" height="40" fill="#B0E0E6" stroke="#333" stroke-width="2"/>
      <rect x="-150" y="-20" width="60" height="40" fill="#B0E0E6" stroke="#333" stroke-width="2"/>
      <rect x="-90"  y="-20" width="60" height="40" fill="#B0E0E6" stroke="#333" stroke-width="2"/>
      <rect x="-30"  y="-20" width="60" height="40" fill="#B0E0E6" stroke="#333" stroke-width="2"/>
      <rect x="30"   y="-20" width="60" height="40" fill="#B0E0E6" stroke="#333" stroke-width="2"/>
      <rect x="90"   y="-20" width="60" height="40" fill="#B0E0E6" stroke="#333" stroke-width="2"/>
      {hex_top}
      {hex_bot}
      <line x1="-150" y1="-20" x2="-150" y2="20" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="-90"  y1="-20" x2="-90"  y2="20" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="-30"  y1="-20" x2="-30"  y2="20" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="30"   y1="-20" x2="30"   y2="20" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="90"   y1="-20" x2="90"   y2="20" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
    </svg>
    '''

def draw_octahedron_net():
    return '''
    <svg width="420" height="200" viewBox="-210 -100 420 200">
      <path d="M -180,50 L -150,0 L -120,50 Z" fill="#98D8C8" stroke="#333" stroke-width="2"/>
      <path d="M -120,50 L -90,0  L -60,50 Z" fill="#98D8C8" stroke="#333" stroke-width="2"/>
      <path d="M -60,50  L -30,0  L 0,50   Z" fill="#98D8C8" stroke="#333" stroke-width="2"/>
      <path d="M 0,50    L 30,0   L 60,50  Z" fill="#98D8C8" stroke="#333" stroke-width="2"/>
      <path d="M 60,50   L 90,0   L 120,50 Z" fill="#98D8C8" stroke="#333" stroke-width="2"/>
      <path d="M 120,50  L 150,0  L 180,50 Z" fill="#98D8C8" stroke="#333" stroke-width="2"/>
      <path d="M -90,0   L -60,-50 L -30,0  Z" fill="#98D8C8" stroke="#333" stroke-width="2"/>
      <path d="M 30,0    L 60,-50  L 90,0   Z" fill="#98D8C8" stroke="#333" stroke-width="2"/>
    </svg>
    '''

def draw_dodecahedron_net_simplified():
    center = _n_gon(0, -10, 26, 5, "#F7DC6F")
    ring = []
    ring += [_n_gon(0, -62, 26, 5, "#F7DC6F")]
    ring += [_n_gon(42, -36, 26, 5, "#F7DC6F")]
    ring += [_n_gon(26, 22, 26, 5, "#F7DC6F")]
    ring += [_n_gon(-26, 22, 26, 5, "#F7DC6F")]
    ring += [_n_gon(-42, -36, 26, 5, "#F7DC6F")]
    tail = _n_gon(0, 70, 26, 5, "#F7DC6F")
    return f'''
    <svg width="360" height="360" viewBox="-180 -180 360 360">
      {center}
      {''.join(ring)}
      {tail}
      <text x="0" y="140" text-anchor="middle" font-size="12" fill="#666">(Simplified – 12 pentagons total)</text>
    </svg>
    '''

def draw_octagonal_prism_net():
    return '''
    <svg width="500" height="200" viewBox="-250 -100 500 200">
      <rect x="-240" y="-20" width="50" height="40" fill="#85C1E2" stroke="#333" stroke-width="2"/>
      <rect x="-190" y="-20" width="50" height="40" fill="#85C1E2" stroke="#333" stroke-width="2"/>
      <rect x="-140" y="-20" width="50" height="40" fill="#85C1E2" stroke="#333" stroke-width="2"/>
      <rect x="-90"  y="-20" width="50" height="40" fill="#85C1E2" stroke="#333" stroke-width="2"/>
      <rect x="-40"  y="-20" width="50" height="40" fill="#85C1E2" stroke="#333" stroke-width="2"/>
      <rect x="10"   y="-20" width="50" height="40" fill="#85C1E2" stroke="#333" stroke-width="2"/>
      <rect x="60"   y="-20" width="50" height="40" fill="#85C1E2" stroke="#333" stroke-width="2"/>
      <rect x="110"  y="-20" width="50" height="40" fill="#85C1E2" stroke="#333" stroke-width="2"/>
      <polygon points="-20,-20 20,-20 35,-35 35,-55 20,-70 -20,-70 -35,-55 -35,-35" fill="#85C1E2" stroke="#333" stroke-width="2"/>
      <polygon points="-20,20 20,20 35,35 35,55 20,70 -20,70 -35,55 -35,35" fill="#85C1E2" stroke="#333" stroke-width="2"/>
      <text x="0" y="90" text-anchor="middle" font-size="10" fill="#666">(2 octagons + 8 rectangles)</text>
    </svg>
    '''

def draw_octagonal_prism_3d():
    # Reuse the generic prism helper with an 8-gon base
    return _prism_3d(8, "#85C1E2")

# NEW: Curved-surface nets
def draw_cylinder_net():
    return '''
    <svg width="360" height="220" viewBox="-180 -110 360 220">
      <rect x="-120" y="-30" width="240" height="60" fill="#CFE8FF" stroke="#333" stroke-width="2"/>
      <circle cx="-120" cy="0" r="30" fill="#CFE8FF" stroke="#333" stroke-width="2"/>
      <circle cx="120"  cy="0" r="30" fill="#CFE8FF" stroke="#333" stroke-width="2"/>
    </svg>
    '''

def draw_cone_net():
    # sector + circle (simple 120° sector)
    return '''
    <svg width="360" height="240" viewBox="-180 -120 360 240">
      <path d="M 0,0 L 120,0 A 120 120 0 0 1 -60,103.92 Z" fill="#FFD6B0" stroke="#333" stroke-width="2"/>
      <circle cx="0" cy="-70" r="35" fill="#FFD6B0" stroke="#333" stroke-width="2"/>
    </svg>
    '''

def draw_sphere_net():
    # 8 gores (curved “petals”)
    return '''
    <svg width="360" height="260" viewBox="-180 -130 360 260">
      <g fill="#E6E6FA" stroke="#333" stroke-width="2">
        <path d="M0,-100 C -10,-60 -10,60 0,100 C 10,60 10,-60 0,-100 Z"/>
        <path d="M30,-95 C 20,-55 20,55 30,95 C 40,55 40,-55 30,-95 Z"/>
        <path d="M60,-85 C 50,-50 50,50 60,85 C 70,50 70,-50 60,-85 Z"/>
        <path d="M90,-70 C 80,-45 80,45 90,70 C 100,45 100,-45 90,-70 Z"/>
        <path d="M0,-100 C 10,-60 10,60 0,100 C -10,60 -10,-60 0,-100 Z"/>
        <path d="M-30,-95 C -20,-55 -20,55 -30,95 C -40,55 -40,-55 -30,-95 Z"/>
        <path d="M-60,-85 C -50,-50 -50,50 -60,85 C -70,50 -70,-50 -60,-85 Z"/>
        <path d="M-90,-70 C -80,-45 -80,45 -90,70 C -100,45 -100,-45 -90,-70 Z"/>
      </g>
    </svg>
    '''

# =============================
# SVG: 3D Shapes
# =============================
def _prism_3d(sides: int, fill: str) -> str:
    """Generic extruded regular prism icon."""
    front = [(x, y) for x, y in [map(float, p.split(',')) for p in _poly_points(0, 18, 22, sides).split()]]
    dx, dy = 16, -12
    back = [(x+dx, y+dy) for (x, y) in front]
    def pts(arr): return " ".join(f"{x:.1f},{y:.1f}" for x, y in arr)
    faces = []
    for i in range(sides):
        a1, a2 = front[i], front[(i+1) % sides]
        b1, b2 = back[i], back[(i+1) % sides]
        if i < sides//2 + 1:
            faces.append(f'<polygon points="{pts([a1,a2,b2,b1])}" fill="{fill}" opacity="0.6" stroke="#333" stroke-width="2"/>')
    svg = f'''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.9)">
        <polygon points="{pts(back)}" fill="{fill}" opacity="0.35" stroke="#333" stroke-width="2"/>
        {''.join(faces)}
        <polygon points="{pts(front)}" fill="{fill}" stroke="#333" stroke-width="2"/>
      </g>
    </svg>'''
    return svg

def draw_pentagonal_prism_3d():   return _prism_3d(5, "#FFE4B5")
def draw_hexagonal_prism_3d():    return _prism_3d(6, "#B0E0E6")
def draw_triangular_prism_3d():   return _prism_3d(3, "#98FB98")

def draw_cube_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.85)">
        <path d="M -40,-40 L 0,-60 L 0,-20 L -40,0 Z" fill="#90EE90" opacity="0.4" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 40,-40 L 40,0 L 0,-20 Z"  fill="#90EE90" opacity="0.6" stroke="#333" stroke-width="2"/>
        <path d="M -40,0 L 0,-20 L 0,20 L -40,40 Z"  fill="#90EE90" opacity="0.7" stroke="#333" stroke-width="2"/>
        <path d="M 0,-20 L 40,0 L 40,40 L 0,20 Z"    fill="#90EE90" opacity="0.9" stroke="#333" stroke-width="2"/>
        <path d="M -40,40 L 0,20 L 40,40 L 0,60 Z"   fill="#90EE90" opacity="0.8" stroke="#333" stroke-width="2"/>
        <path d="M -40,-40 L 0,-60 L 40,-40 L 0,-20 Z" fill="#90EE90" stroke="#333" stroke-width="2"/>
      </g>
    </svg>
    '''

def draw_rectangular_prism_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.8)">
        <path d="M -60,-30 L 0,-50 L 0,-10 L -60,10 Z" fill="#87CEEB" opacity="0.4" stroke="#333" stroke-width="2"/>
        <path d="M 0,-50 L 60,-30 L 60,10 L 0,-10 Z" fill="#87CEEB" opacity="0.6" stroke="#333" stroke-width="2"/>
        <path d="M -60,10 L 0,-10 L 0,30 L -60,50 Z" fill="#87CEEB" opacity="0.7" stroke="#333" stroke-width="2"/>
        <path d="M 0,-10 L 60,10 L 60,50 L 0,30 Z"  fill="#87CEEB" opacity="0.9" stroke="#333" stroke-width="2"/>
        <path d="M -60,-30 L 0,-50 L 60,-30 L 0,-10 Z" fill="#87CEEB" stroke="#333" stroke-width="2"/>
        <path d="M -60,50 L 0,30 L 60,50 L 0,70 Z"  fill="#87CEEB" opacity="0.8" stroke="#333" stroke-width="2"/>
      </g>
    </svg>
    '''

def draw_triangular_pyramid_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.9)">
        <path d="M -50,30 L 0,50 L 50,30 Z" fill="#DDA0DD" opacity="0.5" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L -50,30 L 0,50 Z" fill="#DDA0DD" opacity="0.7" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 0,50 L 50,30 Z" fill="#DDA0DD" opacity="0.9" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 50,30 L -50,30 Z" fill="#DDA0DD" opacity="0.6" stroke="#333" stroke-width="2"/>
      </g>
    </svg>
    '''

def draw_square_pyramid_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.9)">
        <path d="M -40,20 L 0,40 L 40,20 L 0,0 Z" fill="#F0E68C" opacity="0.5" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L -40,20 L 0,0 Z" fill="#F0E68C" opacity="0.6" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 0,0 L 40,20 Z" fill="#F0E68C" opacity="0.8" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 40,20 L 0,40 Z" fill="#F0E68C" opacity="0.9" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 0,40 L -40,20 Z" fill="#F0E68C" opacity="0.7" stroke="#333" stroke-width="2"/>
      </g>
    </svg>
    '''

def draw_rectangular_pyramid_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.9)">
        <path d="M -50,15 L 50,15 L 20,-5 L -20,-5 Z" fill="#F8B88B" opacity="0.5" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L -50,15 L -20,-5 Z" fill="#F8B88B" opacity="0.7" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L -20,-5 L 20,-5 Z" fill="#F8B88B" opacity="0.85" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 20,-5 L 50,15 Z" fill="#F8B88B" opacity="0.9" stroke="#333" stroke-width="2"/>
      </g>
    </svg>
    '''

def draw_pentagonal_pyramid_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.85)">
        <path d="M 0,30 L 25,20 L 15,0 L -15,0 L -25,20 Z" fill="#F5DEB3" opacity="0.5" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 0,30 L 25,20 Z" fill="#F5DEB3" opacity="0.8" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 25,20 L 15,0 Z" fill="#F5DEB3" opacity="0.9" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 15,0 L -15,0 Z" fill="#F5DEB3" opacity="0.7" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L -15,0 L -25,20 Z" fill="#F5DEB3" opacity="0.6" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L -25,20 L 0,30 Z" fill="#F5DEB3" opacity="0.65" stroke="#333" stroke-width="2"/>
      </g>
    </svg>
    '''

def draw_hexagonal_pyramid_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.85)">
        <path d="M -25,30 L 25,30 L 40,15 L 25,0 L -25,0 L -40,15 Z" fill="#FFA07A" opacity="0.5" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 25,30 L 40,15 Z" fill="#FFA07A" opacity="0.8" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 40,15 L 25,0 Z"  fill="#FFA07A" opacity="0.9" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 25,0  L -25,0 Z" fill="#FFA07A" opacity="0.7" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L -25,0 L -40,15 Z" fill="#FFA07A" opacity="0.6" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L -40,15 L -25,30 Z" fill="#FFA07A" opacity="0.65" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L -25,30 L 25,30 Z" fill="#FFA07A" opacity="0.75" stroke="#333" stroke-width="2"/>
      </g>
    </svg>
    '''

def draw_octahedron_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.8)">
        <path d="M 0,60 L -40,0 L 0,-25 Z" fill="#98D8C8" opacity="0.5" stroke="#333" stroke-width="2"/>
        <path d="M 0,60 L 0,-25 L 40,0 Z"  fill="#98D8C8" opacity="0.6" stroke="#333" stroke-width="2"/>
        <path d="M 0,60 L 40,0  L 25,15 Z" fill="#98D8C8" opacity="0.7" stroke="#333" stroke-width="2"/>
        <path d="M 0,60 L 25,15 L -25,15 Z" fill="#98D8C8" opacity="0.8" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L -40,0 L 0,-25 Z" fill="#98D8C8" opacity="0.85" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 0,-25 L 40,0 Z"  fill="#98D8C8" opacity="0.9" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 40,0  L 25,15 Z" fill="#98D8C8" opacity="0.95" stroke="#333" stroke-width="2"/>
        <path d="M 0,-60 L 25,15 L -25,15 Z" fill="#98D8C8" stroke="#333" stroke-width="2"/>
      </g>
    </svg>
    '''

def draw_dodecahedron_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.65)">
        <path d="M 0,-35 L 25,-20 L 15,5 L -15,5 L -25,-20 Z" fill="#F7DC6F" stroke="#333" stroke-width="2"/>
        <path d="M 0,-35 L -25,-20 L -40,-30 L -30,-50 L 0,-45 Z" fill="#F7DC6F" opacity="0.8" stroke="#333" stroke-width="2"/>
        <path d="M 0,-35 L 0,-45 L 30,-50 L 40,-30 L 25,-20 Z" fill="#F7DC6F" opacity="0.85" stroke="#333" stroke-width="2"/>
        <path d="M 25,-20 L 40,-30 L 50,-5 L 35,10 L 15,5 Z" fill="#F7DC6F" opacity="0.9" stroke="#333" stroke-width="2"/>
        <path d="M 15,5 L 35,10 L 25,30 L 0,35 L -15,5 Z" fill="#F7DC6F" opacity="0.75" stroke="#333" stroke-width="2"/>
        <path d="M -15,5 L 0,35 L -25,30 L -35,10 L -25,-20 Z" fill="#F7DC6F" opacity="0.7" stroke="#333" stroke-width="2"/>
      </g>
    </svg>
    '''

def draw_icosahedron_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.8)">
        <path d="M 0,-50 L -25,-15 L 0,-25 Z" fill="#BB8FCE" opacity="0.9" stroke="#333" stroke-width="2"/>
        <path d="M 0,-50 L 0,-25 L 25,-15 Z"  fill="#BB8FCE" opacity="0.95" stroke="#333" stroke-width="2"/>
        <path d="M 0,-50 L 25,-15 L 15,-30 Z" fill="#BB8FCE" stroke="#333" stroke-width="2"/>
        <path d="M -25,-15 L -30,10 L -15,0 Z" fill="#BB8FCE" opacity="0.8" stroke="#333" stroke-width="2"/>
        <path d="M -15,0 L 0,15 L 0,-25 Z"     fill="#BB8FCE" opacity="0.85" stroke="#333" stroke-width="2"/>
        <path d="M 0,-25 L 0,15 L 15,0 Z"     fill="#BB8FCE" opacity="0.9" stroke="#333" stroke-width="2"/>
        <path d="M 15,0 L 30,10 L 25,-15 Z"   fill="#BB8FCE" opacity="0.95" stroke="#333" stroke-width="2"/>
        <path d="M -30,10 L -15,35 L -15,0 Z" fill="#BB8FCE" opacity="0.7" stroke="#333" stroke-width="2"/>
        <path d="M -15,0 L -15,35 L 0,15 Z"   fill="#BB8FCE" opacity="0.75" stroke="#333" stroke-width="2"/>
        <path d="M 0,15 L 15,35 L 15,0 Z"     fill="#BB8FCE" opacity="0.8" stroke="#333" stroke-width="2"/>
      </g>
    </svg>
    '''

# NEW: Curved-surface 3D icons
def draw_cylinder_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.9)">
        <ellipse cx="0" cy="-35" rx="30" ry="12" fill="#CFE8FF" stroke="#333" stroke-width="2"/>
        <rect x="-30" y="-35" width="60" height="70" fill="#CFE8FF" opacity="0.7" stroke="#333" stroke-width="2"/>
        <ellipse cx="0" cy="35" rx="30" ry="12" fill="#CFE8FF" stroke="#333" stroke-width="2"/>
        <path d="M -30,-35 Q 0,-47 30,-35" stroke="#333" stroke-width="1" stroke-dasharray="4,4" fill="none" opacity="0.6"/>
      </g>
    </svg>
    '''

def draw_cone_3d():
    return '''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <g transform="scale(0.9)">
        <path d="M 0,-55 L -35,35 L 35,35 Z" fill="#FFD6B0" opacity="0.85" stroke="#333" stroke-width="2"/>
        <ellipse cx="0" cy="35" rx="35" ry="12" fill="#FFD6B0" stroke="#333" stroke-width="2"/>
        <path d="M -35,35 Q 0,23 35,35" stroke="#333" stroke-width="1" stroke-dasharray="4,4" fill="none" opacity="0.6"/>
      </g>
    </svg>
    '''

def draw_sphere_3d():
    grad_id = f"sphGrad{random.randint(1000,9999)}"
    return f'''
    <svg width="150" height="150" viewBox="-75 -75 150 150">
      <defs>
        <radialGradient id="{grad_id}">
          <stop offset="0%"  stop-color="#ffffff" stop-opacity="0.6"/>
          <stop offset="100%" stop-color="#E6E6FA" stop-opacity="1"/>
        </radialGradient>
      </defs>
      <g transform="scale(0.9)">
        <circle cx="0" cy="0" r="45" fill="url(#{grad_id})" stroke="#333" stroke-width="2"/>
        <ellipse cx="0" cy="0" rx="45" ry="16" fill="none" stroke="#333" stroke-width="1" opacity="0.3"/>
        <ellipse cx="0" cy="0" rx="16" ry="45" fill="none" stroke="#333" stroke-width="1" opacity="0.3"/>
      </g>
    </svg>
    '''

# =============================
if __name__ == "__main__":
    run()
