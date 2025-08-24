import streamlit as st
import streamlit.components.v1 as components
import random
import math

# =========================
# 3D helpers (isometric SVG)
# =========================
SQRT3 = math.sqrt(3)
COS30 = SQRT3 / 2.0   # ~0.866
SIN30 = 0.5

def iso_project(x, y, z, scale=80):
    """Isometric projection of 3D point -> 2D SVG coords (centered at 0,0)."""
    X = (x - y) * COS30 * scale
    Y = (x + y) * SIN30 * scale - z * scale
    return (X, Y)

def polygon_points_str(points2d):
    return " ".join(f"{x:.2f},{y:.2f}" for (x, y) in points2d)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def shade_color(hex_color, factor):
    """
    factor < 1.0 -> darker; factor > 1.0 -> lighter
    """
    r, g, b = hex_to_rgb(hex_color)
    if factor < 1:
        r, g, b = int(r*factor), int(g*factor), int(b*factor)
    else:
        r = int(r + (255 - r) * (factor - 1))
        g = int(g + (255 - g) * (factor - 1))
        b = int(b + (255 - b) * (factor - 1))
    return rgb_to_hex((min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b))))

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def mul(a, s):
    return (a[0]*s, a[1]*s, a[2]*s)

def length(v):
    return math.sqrt(dot(v, v))

def normalize(v):
    L = length(v) or 1.0
    return (v[0]/L, v[1]/L, v[2]/L)

def face_normal(a, b, c):
    """Return unnormalized face normal from three 3D points."""
    return cross(sub(b, a), sub(c, a))

def normalize_safe(v):
    L = length(v)
    if L < 1e-12:
        return (0.0, 0.0, 1.0)
    return (v[0]/L, v[1]/L, v[2]/L)

LIGHT_DIR = normalize((1, 1, 1))  # diagonal light for pleasant shading

def light_intensity(face):
    """Compute a 0..1 intensity from face normal and LIGHT_DIR."""
    n = face_normal(face[0], face[1], face[2])
    n = normalize_safe(n)
    d = max(0.0, dot(n, LIGHT_DIR))
    return 0.35 + 0.65 * d

def depth_key(face):
    """Sort key for painter's algorithm (back->front). Larger sum is closer."""
    avg = [sum(c[i] for c in face)/len(face) for i in range(3)]
    return avg[0] + avg[1] + avg[2]

def svg_wrap(inner, w=360, h=400, vb=("-220 -240 440 480")):
    return f"""
    <div style="text-align:center;margin:8px 0;">
      <svg width="{w}" height="{h}" viewBox="{vb}" preserveAspectRatio="xMidYMid meet"
           xmlns="http://www.w3.org/2000/svg">
        <style>
          .edge {{ stroke:#333; stroke-width:1.5; fill-opacity:1; vector-effect:non-scaling-stroke; }}
        </style>
        {inner}
      </svg>
    </div>
    """

def draw_polyhedron(faces, color):
    """
    faces: list of faces, each face is a list of 3D vertices [(x,y,z), ...]
    Returns SVG with faces sorted and shaded.
    """
    faces_sorted = sorted(faces, key=depth_key)
    parts = []
    for f in faces_sorted:
        intensity = light_intensity(f)   # 0..1
        shade = 0.7 + 0.55 * intensity
        face_color = shade_color(color, shade)
        pts2d = [iso_project(*p) for p in f]
        parts.append(f'<polygon class="edge" fill="{face_color}" points="{polygon_points_str(pts2d)}" />')
    return svg_wrap("\n".join(parts))

# =========================
# Shape builders (3D meshes)
# =========================

def cuboid_faces(lx=1.2, ly=0.9, lz=0.8):
    """Axis-aligned box centered so it sits 'on the ground' (z>=0)."""
    x0, x1 = -lx/2, lx/2
    y0, y1 = -ly/2, ly/2
    z0, z1 = 0.0, lz
    p000 = (x0, y0, z0); p100 = (x1, y0, z0); p110 = (x1, y1, z0); p010 = (x0, y1, z0)
    p001 = (x0, y0, z1); p101 = (x1, y0, z1); p111 = (x1, y1, z1); p011 = (x0, y1, z1)
    return [
        [p000, p100, p110, p010],  # bottom
        [p001, p011, p111, p101],  # top
        [p000, p010, p011, p001],  # left
        [p100, p101, p111, p110],  # right
        [p010, p110, p111, p011],  # front
        [p000, p001, p101, p100],  # back
    ]

def regular_ngon_xy(n, r):
    """Regular n-gon centered at (0,0) on z=0 plane, starting at angle -90°."""
    pts = []
    start = -math.pi/2
    for i in range(n):
        ang = start + 2*math.pi*i/n
        pts.append((r*math.cos(ang), r*math.sin(ang)))
    return pts

def prism_faces(n, r=0.7, h=0.9):
    base = regular_ngon_xy(n, r)
    bottom = [(x, y, 0.0) for (x, y) in base]
    top = [(x, y, h) for (x, y) in base]
    faces = [bottom[::-1], top]  # base and top
    for i in range(n):
        j = (i + 1) % n
        faces.append([bottom[i], bottom[j], top[j], top[i]])
    return faces

def pyramid_faces(n, r=0.8, h=1.1):
    base = regular_ngon_xy(n, r)
    bottom = [(x, y, 0.0) for (x, y) in base]
    apex = (0.0, 0.0, h)
    faces = [bottom[::-1]]
    for i in range(n):
        j = (i + 1) % n
        faces.append([apex, bottom[i], bottom[j]])
    return faces

def rectangular_pyramid_faces(lx=1.4, ly=1.0, h=1.1):
    x0, x1 = -lx/2, lx/2
    y0, y1 = -ly/2, ly/2
    base = [(x0, y0, 0.0), (x1, y0, 0.0), (x1, y1, 0.0), (x0, y1, 0.0)]
    apex = (0.0, 0.0, h)
    faces = [base[::-1]]
    for i in range(4):
        j = (i + 1) % 4
        faces.append([apex, base[i], base[j]])
    return faces

def octahedron_faces(a=0.9):
    """Regular octahedron with vertices on axes."""
    v = [
        ( a, 0, 0), (-a, 0, 0),
        (0,  a, 0), (0, -a, 0),
        (0, 0,  a), (0, 0, -a)
    ]
    return [
        [v[4], v[0], v[2]], [v[4], v[2], v[1]], [v[4], v[1], v[3]], [v[4], v[3], v[0]],
        [v[5], v[2], v[0]], [v[5], v[1], v[2]], [v[5], v[3], v[1]], [v[5], v[0], v[3]],
    ]

# ---------- Icosahedron (convex hull) ----------
def icosahedron_vertices():
    """12 vertices of a regular icosahedron centered at origin."""
    phi = (1 + math.sqrt(5)) / 2
    V = []
    # (0, ±1, ±φ)
    for s1 in (-1, 1):
        for s2 in (-1, 1):
            V.append((0.0, s1*1.0, s2*phi))
    # (±1, ±φ, 0)
    for s0 in (-1, 1):
        for s1 in (-1, 1):
            V.append((s0*1.0, s1*phi, 0.0))
    # (±φ, 0, ±1)
    for s0 in (-1, 1):
        for s2 in (-1, 1):
            V.append((s0*phi, 0.0, s2*1.0))
    # Slightly normalize radius so overall scale is ~1.2 for nice canvas fit
    maxr = max(length(p) for p in V)
    scale = 1.15 / maxr
    return [mul(p, scale) for p in V]

def convex_hull_tri_faces(points, eps=1e-7):
    """Return list of triangular faces (as index triples) of the convex hull."""
    n = len(points)
    faces = []
    seen = set()
    for i in range(n-2):
        for j in range(i+1, n-1):
            for k in range(j+1, n):
                a, b, c = points[i], points[j], points[k]
                nrm = face_normal(a, b, c)
                if length(nrm) < eps:
                    continue
                # Check sidedness for all other points
                pos = neg = False
                for m in range(n):
                    if m in (i, j, k):
                        continue
                    dval = dot(nrm, sub(points[m], a))
                    if dval > eps:
                        pos = True
                    elif dval < -eps:
                        neg = True
                    if pos and neg:
                        break
                if pos and neg:
                    continue  # not a hull face
                # It is a hull face; orient outward (away from origin)
                centroid = mul(add(add(a, b), c), 1/3)
                if dot(nrm, centroid) < 0:
                    tri = (i, k, j)
                else:
                    tri = (i, j, k)
                key = tuple(sorted(tri))
                if key not in seen:
                    seen.add(key)
                    faces.append(tri)
    return faces

def icosahedron_faces_points():
    V = icosahedron_vertices()
    F_idx = convex_hull_tri_faces(V)
    F_pts = [[V[i], V[j], V[k]] for (i, j, k) in F_idx]
    return F_pts, V, F_idx

# ---------- Dodecahedron (dual of icosahedron) ----------
def dodecahedron_faces_points():
    """
    Construct a regular dodecahedron as the dual of the icosahedron:
    - Dodeca vertices = icosa face centroids
    - Dodeca pentagon faces correspond to each icosa vertex (5 adjacent faces)
    """
    icosa_faces_pts, V, F_idx = icosahedron_faces_points()

    # Centroids of icosa faces -> dodeca vertices
    C = []
    for f in icosa_faces_pts:
        c = mul(add(add(f[0], f[1]), f[2]), 1/3)
        C.append(c)

    # Map: icosa vertex -> list of adjacent face indices
    vert_to_faces = {i: [] for i in range(len(V))}
    for fi, (i, j, k) in enumerate(F_idx):
        vert_to_faces[i].append(fi)
        vert_to_faces[j].append(fi)
        vert_to_faces[k].append(fi)

    faces = []
    for vi, face_ids in vert_to_faces.items():
        v = V[vi]
        n = normalize_safe(v)  # outward direction near this vertex

        # Local tangent basis (u, w) around n
        ref = (0.0, 0.0, 1.0) if abs(n[2]) < 0.9 else (1.0, 0.0, 0.0)
        u = normalize_safe(cross(ref, n))
        w = normalize_safe(cross(n, u))

        # Order the 5 neighboring face-centers counter-clockwise around v
        ang_list = []
        for fidx in face_ids:
            t = sub(C[fidx], v)
            ang = math.atan2(dot(t, w), dot(t, u))
            ang_list.append((ang, fidx))
        ang_list.sort()

        ordered_idx = [fidx for (ang, fidx) in ang_list]
        poly = [C[idx] for idx in ordered_idx]

        # Ensure polygon normal points outward ~ along +n (towards v)
        if len(poly) >= 3:
            nrm = face_normal(poly[0], poly[1], poly[2])
            if dot(nrm, v) < 0:
                poly.reverse()

        faces.append(poly)

    # Optional: normalize radius to a pleasant size
    # (center around origin, then scale to ~1.2 radius)
    all_pts = [p for face in faces for p in face]
    avg = (
        sum(p[0] for p in all_pts)/len(all_pts),
        sum(p[1] for p in all_pts)/len(all_pts),
        sum(p[2] for p in all_pts)/len(all_pts),
    )
    centered = [[sub(p, avg) for p in face] for face in faces]
    maxr = max(length(p) for face in centered for p in face)
    scale = 1.2 / maxr
    scaled = [[mul(p, scale) for p in face] for face in centered]
    return scaled

# Cylinders / cones / sphere remain as properly layered SVGs (not polygonal)
def draw_cylinder(color):
    inner = f"""
      <g>
        <!-- back rim -->
        <path d="M -80,-80 C -40,-100 40,-100 80,-80"
              fill="none" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5" opacity="0.6"/>
        <!-- side -->
        <rect x="-80" y="-80" width="160" height="160" fill="{color}" opacity="0.85" stroke="#333" stroke-width="1.5"/>
        <!-- top ellipse -->
        <ellipse cx="0" cy="-80" rx="80" ry="20" fill="{shade_color(color,1.15)}" stroke="#333" stroke-width="1.5"/>
        <!-- bottom ellipse -->
        <ellipse cx="0" cy="80" rx="80" ry="20" fill="{shade_color(color,0.95)}" stroke="#333" stroke-width="1.5"/>
      </g>
    """
    return svg_wrap(inner)

def draw_cone(color):
    inner = f"""
      <g>
        <!-- side -->
        <path d="M 0,-110 L -90,80 L 90,80 Z" fill="{shade_color(color,1.0)}" stroke="#333" stroke-width="1.5"/>
        <!-- base -->
        <ellipse cx="0" cy="80" rx="90" ry="22" fill="{shade_color(color,0.95)}" stroke="#333" stroke-width="1.5"/>
        <!-- hidden edge -->
        <path d="M -90,80 C -45,58 45,58 90,80" fill="none" stroke="#333" stroke-width="1.2" stroke-dasharray="5,5" opacity="0.6"/>
      </g>
    """
    return svg_wrap(inner)

def draw_sphere(color):
    gid = f"sphereGrad_{random.randint(1000,9999)}"
    inner = f"""
      <defs>
        <radialGradient id="{gid}" cx="40%" cy="35%" r="65%">
          <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.75"/>
          <stop offset="100%" stop-color="{color}" stop-opacity="1"/>
        </radialGradient>
      </defs>
      <g>
        <circle cx="0" cy="0" r="110" fill="url(#{gid})" stroke="#333" stroke-width="1.5"/>
        <ellipse cx="0" cy="0" rx="110" ry="35" fill="none" stroke="#333" stroke-width="1" opacity="0.25"/>
        <ellipse cx="0" cy="0" rx="35" ry="110" fill="none" stroke="#333" stroke-width="1" opacity="0.25"/>
      </g>
    """
    return svg_wrap(inner)

# =========================
# Public drawing API (names kept)
# =========================

def draw_cube(color):
    return draw_polyhedron(cuboid_faces(1.1, 1.1, 1.1), color)

def draw_cuboid(color):
    return draw_polyhedron(cuboid_faces(1.6, 1.0, 1.0), color)

def draw_triangular_prism(color):
    return draw_polyhedron(prism_faces(3, r=0.9, h=1.0), color)

def draw_pentagonal_prism(color):
    return draw_polyhedron(prism_faces(5, r=0.85, h=1.0), color)

def draw_hexagonal_prism(color):
    return draw_polyhedron(prism_faces(6, r=0.8, h=1.0), color)

def draw_octagonal_prism(color):
    return draw_polyhedron(prism_faces(8, r=0.75, h=1.0), color)

def draw_square_pyramid(color):
    return draw_polyhedron(pyramid_faces(4, r=1.0, h=1.2), color)

def draw_triangular_pyramid(color):
    return draw_polyhedron(pyramid_faces(3, r=1.05, h=1.2), color)

def draw_pentagonal_pyramid(color):
    return draw_polyhedron(pyramid_faces(5, r=0.95, h=1.3), color)

def draw_hexagonal_pyramid(color):
    return draw_polyhedron(pyramid_faces(6, r=0.9, h=1.25), color)

def draw_rectangular_pyramid(color):
    return draw_polyhedron(rectangular_pyramid_faces(1.8, 1.2, 1.25), color)

def draw_octahedron(color):
    return draw_polyhedron(octahedron_faces(0.95), color)

def draw_icosahedron(color):
    faces_pts, _, _ = icosahedron_faces_points()
    return draw_polyhedron(faces_pts, color)

def draw_dodecahedron(color):
    faces_pts = dodecahedron_faces_points()
    return draw_polyhedron(faces_pts, color)

# =========================
# Your original app (kept, with shape list updated)
# =========================

def run():
    if "faces_3d_difficulty" not in st.session_state:
        st.session_state.faces_3d_difficulty = 1
    if "current_shape_question" not in st.session_state:
        st.session_state.current_shape_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.shape_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0

    st.markdown("**📚 Year 5 > W. Three-dimensional figures**")
    st.title("🎲 Identify Faces of 3D Figures")
    st.markdown("*Learn to identify the 2D shapes that form the faces of 3D objects*")
    st.markdown("---")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        difficulty_names = {1: "Basic Shapes", 2: "Prisms & Pyramids", 3: "Complex Polyhedra"}
        st.markdown(f"**Difficulty Level:** {difficulty_names[st.session_state.faces_3d_difficulty]}")
        progress = (st.session_state.faces_3d_difficulty - 1) / 2
        st.progress(progress, text=f"Level {st.session_state.faces_3d_difficulty}/3")
    with col2:
        difficulty_colors = {1: "🟢", 2: "🟡", 3: "🔴"}
        st.markdown(f"**{difficulty_colors[st.session_state.faces_3d_difficulty]} {difficulty_names[st.session_state.faces_3d_difficulty]}**")
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()

    if st.session_state.current_shape_question is None:
        generate_new_shape_question()

    display_shape_question()

    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the 3D shape** shown in the diagram
        - **Read the question** asking about a specific face shape
        - **Think about all the faces** of the 3D object
        - **Answer Yes or No** based on whether that face exists

        ### Understanding Faces:
        - A **face** is a flat surface of a 3D shape
        - Faces are 2D shapes like circles, triangles, squares, etc.
        - Some shapes have all the same faces (like a cube with 6 squares)
        - Others have different types of faces (like a pyramid)

        ### Common 3D Shapes & Their Faces:

        **Basic Shapes:**
        - **Cube:** 6 square faces
        - **Cuboid:** 6 rectangular faces
        - **Sphere:** 1 curved surface (no flat faces)
        - **Cylinder:** 2 circular faces, 1 curved surface
        - **Cone:** 1 circular face, 1 curved surface

        **Prisms:**
        - **Triangular Prism:** 2 triangular faces, 3 rectangular faces
        - **Pentagonal Prism:** 2 pentagonal faces, 5 rectangular faces
        - **Hexagonal Prism:** 2 hexagonal faces, 6 rectangular faces
        - **Octagonal Prism:** 2 octagonal faces, 8 rectangular faces

        **Pyramids:**
        - **Square Pyramid:** 1 square base, 4 triangular faces
        - **Triangular Pyramid:** 4 triangular faces
        - **Rectangular Pyramid:** 1 rectangular base, 4 triangular faces
        - **Pentagonal Pyramid:** 1 pentagonal base, 5 triangular faces
        - **Hexagonal Pyramid:** 1 hexagonal base, 6 triangular faces

        **Polyhedra:**
        - **Octahedron:** 8 triangular faces
        - **Dodecahedron:** 12 pentagonal faces
        - **Icosahedron:** 20 triangular faces
        """)

def generate_new_shape_question():
    difficulty = st.session_state.faces_3d_difficulty

    if difficulty == 1:
        shapes = [
            {"name":"cube","display_name":"Cube","faces":["square"],"face_counts":{"square":6},"color":"#90EE90","svg_function":draw_cube},
            {"name":"cuboid","display_name":"Rectangular Prism (Cuboid)","faces":["rectangle"],"face_counts":{"rectangle":6},"color":"#87CEEB","svg_function":draw_cuboid},
            {"name":"cylinder","display_name":"Cylinder","faces":["circle"],"face_counts":{"circle":2},"color":"#FFB6C1","svg_function":draw_cylinder},
            {"name":"cone","display_name":"Cone","faces":["circle"],"face_counts":{"circle":1},"color":"#FFDAB9","svg_function":draw_cone},
            {"name":"sphere","display_name":"Sphere","faces":[],"face_counts":{},"color":"#E6E6FA","svg_function":draw_sphere},
            {"name":"triangular_prism","display_name":"Triangular Prism","faces":["triangle","rectangle"],"face_counts":{"triangle":2,"rectangle":3},"color":"#98FB98","svg_function":draw_triangular_prism},
        ]
    elif difficulty == 2:
        shapes = [
            {"name":"square_pyramid","display_name":"Square Pyramid","faces":["square","triangle"],"face_counts":{"square":1,"triangle":4},"color":"#F0E68C","svg_function":draw_square_pyramid},
            {"name":"triangular_pyramid","display_name":"Triangular Pyramid (Tetrahedron)","faces":["triangle"],"face_counts":{"triangle":4},"color":"#DDA0DD","svg_function":draw_triangular_pyramid},
            {"name":"pentagonal_prism","display_name":"Pentagonal Prism","faces":["pentagon","rectangle"],"face_counts":{"pentagon":2,"rectangle":5},"color":"#FFE4B5","svg_function":draw_pentagonal_prism},
            {"name":"hexagonal_prism","display_name":"Hexagonal Prism","faces":["hexagon","rectangle"],"face_counts":{"hexagon":2,"rectangle":6},"color":"#B0E0E6","svg_function":draw_hexagonal_prism},
            {"name":"pentagonal_pyramid","display_name":"Pentagonal Pyramid","faces":["pentagon","triangle"],"face_counts":{"pentagon":1,"triangle":5},"color":"#F5DEB3","svg_function":draw_pentagonal_pyramid},
            {"name":"hexagonal_pyramid","display_name":"Hexagonal Pyramid","faces":["hexagon","triangle"],"face_counts":{"hexagon":1,"triangle":6},"color":"#FFA07A","svg_function":draw_hexagonal_pyramid},
        ]
    else:
        shapes = [
            {"name":"octahedron","display_name":"Octahedron","faces":["triangle"],"face_counts":{"triangle":8},"color":"#98D8C8","svg_function":draw_octahedron},
            {"name":"dodecahedron","display_name":"Dodecahedron","faces":["pentagon"],"face_counts":{"pentagon":12},"color":"#F7DC6F","svg_function":draw_dodecahedron},
            {"name":"icosahedron","display_name":"Icosahedron","faces":["triangle"],"face_counts":{"triangle":20},"color":"#BB8FCE","svg_function":draw_icosahedron},
            {"name":"octagonal_prism","display_name":"Octagonal Prism","faces":["octagon","rectangle"],"face_counts":{"octagon":2,"rectangle":8},"color":"#85C1E2","svg_function":draw_octagonal_prism},
            {"name":"rectangular_pyramid","display_name":"Rectangular Pyramid","faces":["rectangle","triangle"],"face_counts":{"rectangle":1,"triangle":4},"color":"#F8B88B","svg_function":draw_rectangular_pyramid},
        ]

    shape = random.choice(shapes)
    all_face_types = ["circle","triangle","square","rectangle","pentagon","hexagon","octagon"]

    if random.random() < 0.7 and shape["faces"]:
        face_to_ask = random.choice(shape["faces"])
        correct_answer = "yes"
    else:
        wrong_faces = [f for f in all_face_types if f not in shape["faces"]]
        if wrong_faces:
            face_to_ask = random.choice(wrong_faces)
            correct_answer = "no"
        else:
            face_to_ask = random.choice(shape["faces"])
            correct_answer = "yes"

    st.session_state.shape_data = {"shape": shape, "face_to_ask": face_to_ask, "correct_answer": correct_answer}
    st.session_state.correct_answer = correct_answer
    st.session_state.current_shape_question = f"Does this shape have a **{face_to_ask}** as a face?"

def display_shape_question():
    shape_data = st.session_state.shape_data
    if not shape_data:
        return

    st.markdown("### 🎯 Question:")
    st.markdown(f"**{st.session_state.current_shape_question}**")

    shape = shape_data["shape"]
    st.markdown(f"#### {shape['display_name']}")

    svg_content = shape["svg_function"](shape["color"])
    components.html(svg_content, height=420)

    st.markdown("### Select your answer:")
    col1, col2 = st.columns(2)
    with col1:
        yes_button = st.button("✅ Yes", key="yes_btn", use_container_width=True)
    with col2:
        no_button = st.button("❌ No", key="no_btn", use_container_width=True)

    if yes_button or no_button:
        st.session_state.user_answer = "yes" if yes_button else "no"
        st.session_state.show_feedback = True
        st.session_state.answer_submitted = True
        handle_feedback()

    if st.session_state.show_feedback:
        show_feedback()

    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def handle_feedback():
    if st.session_state.user_answer == st.session_state.correct_answer:
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        if st.session_state.consecutive_correct >= 3:
            old = st.session_state.faces_3d_difficulty
            st.session_state.faces_3d_difficulty = min(st.session_state.faces_3d_difficulty + 1, 3)
            if st.session_state.faces_3d_difficulty > old:
                st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        if st.session_state.consecutive_wrong >= 2:
            old = st.session_state.faces_3d_difficulty
            st.session_state.faces_3d_difficulty = max(st.session_state.faces_3d_difficulty - 1, 1)
            if st.session_state.faces_3d_difficulty < old:
                st.session_state.consecutive_wrong = 0

def show_feedback():
    shape_data = st.session_state.shape_data
    shape = shape_data["shape"]
    face_asked = shape_data["face_to_ask"]

    if st.session_state.user_answer == st.session_state.correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        if st.session_state.correct_answer == "yes":
            count = shape["face_counts"].get(face_asked, 0)
            st.info(f"✅ The {shape['display_name']} has **{count} {face_asked} face{'s' if count != 1 else ''}**.")
        else:
            st.info(f"✅ The {shape['display_name']} does **NOT** have any {face_asked} faces.")
        if shape["faces"]:
            face_list = [f"{shape['face_counts'][ft]} {ft}{'s' if shape['face_counts'][ft] != 1 else ''}" for ft in shape["faces"]]
            st.markdown(f"**This shape has:** {', '.join(face_list)}")
        else:
            st.markdown("**This shape has:** No flat faces (only curved surfaces)")
        if st.session_state.consecutive_correct >= 2:
            st.info("🌟 Great streak! One more correct answer to level up!")
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{st.session_state.correct_answer.upper()}**.")
        if st.session_state.correct_answer == "yes":
            count = shape["face_counts"].get(face_asked, 0)
            st.warning(f"The {shape['display_name']} DOES have **{count} {face_asked} face{'s' if count != 1 else ''}**.")
        else:
            st.warning(f"The {shape['display_name']} does NOT have any {face_asked} faces.")
        show_detailed_explanation()

def show_detailed_explanation():
    shape_data = st.session_state.shape_data
    shape = shape_data["shape"]
    with st.expander("📖 **Click here for detailed explanation**", expanded=True):
        st.markdown(f"### Understanding the {shape['display_name']}")
        st.markdown("#### All faces of this shape:")
        if shape["faces"]:
            for face_type in shape["faces"]:
                count = shape["face_counts"][face_type]
                st.markdown(f"- **{count} {face_type} face{'s' if count != 1 else ''}**")
        else:
            st.markdown("- **No flat faces** (only curved surfaces)")
        if "prism" in shape["name"].lower():
            st.markdown("""
            **Remember about prisms:**
            - Two parallel bases (same shape, top and bottom)
            - Rectangular faces connecting the bases
            - Named after the shape of their bases
            """)
        elif "pyramid" in shape["name"].lower():
            st.markdown("""
            **Remember about pyramids:**
            - One base (bottom face)
            - Triangular faces meeting at a point (apex)
            - Named after the shape of their base
            """)
        elif shape["name"] == "cylinder":
            st.markdown("""
            **Remember about cylinders:**
            - Two circular faces (top and bottom)
            - One curved surface (not a flat face)
            """)
        elif shape["name"] == "cone":
            st.markdown("""
            **Remember about cones:**
            - One circular face (base)
            - One curved surface (not a flat face)
            - Pointed top (apex)
            """)

def reset_question_state():
    st.session_state.current_shape_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.shape_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer
