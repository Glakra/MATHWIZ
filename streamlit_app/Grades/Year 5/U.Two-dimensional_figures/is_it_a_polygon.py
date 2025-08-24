import streamlit as st
import random
import math

def run():
    """
    Main function to run the Is it a Polygon practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/is_it_a_polygon.py
    """
    
    # Initialize session state
    if "polygon_difficulty" not in st.session_state:
        st.session_state.polygon_difficulty = 1
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.recent_shapes = []  # Track recent shapes to avoid repetition
        st.session_state.shape_category_count = {}  # Track shape categories for balance
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_answer = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("🔷 Is it a Polygon?")
    st.markdown("*Identify whether each shape is a polygon or not*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.polygon_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic shapes (obvious)",
            2: "Mixed regular shapes",
            3: "Irregular and open shapes",
            4: "Complex and concave shapes",
            5: "Challenging cases"
        }
        st.markdown(f"**Current Level:** {difficulty_names.get(difficulty_level, 'Level ' + str(difficulty_level))}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Show stats
    if st.session_state.total_attempted > 0:
        accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
        st.markdown(f"**📊 Accuracy:** {accuracy:.0f}% ({st.session_state.total_correct}/{st.session_state.total_attempted})")
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### What is a Polygon?
        
        A polygon is a closed figure that has:
        1. **Only straight sides** (no curves)
        2. **Sides that connect** to form a closed shape
        3. **At least 3 sides**
        
        ### ✅ Examples of Polygons:
        - **Triangle** (3 sides)
        - **Square** (4 sides)
        - **Pentagon** (5 sides)
        - **Hexagon** (6 sides)
        - **Star** (if made with straight lines)
        - **Irregular shapes** (as long as they're closed with straight sides)
        
        ### ❌ NOT Polygons:
        - **Circle** (curved, not straight sides)
        - **Oval/Ellipse** (curved)
        - **Open shapes** (not closed)
        - **Shapes with curved sides**
        - **Single lines or dots**
        
        ### Remember:
        - **Polygons can be regular** (all sides equal) or **irregular**
        - **Polygons can be convex** (no dents) or **concave** (with dents)
        - **Stars can be polygons** if they're made of straight lines
        - **The shape must be completely closed** - no gaps!
        
        ### Quick Check:
        Ask yourself:
        1. Is it closed? (Can you trace around it without lifting your pencil?)
        2. Are all the sides straight?
        3. Does it have at least 3 sides?
        
        If YES to all three → It's a polygon! ✅
        If NO to any one → It's NOT a polygon! ❌
        """)

def get_shape_category(shape_type):
    """Get the category of a shape for balancing purposes"""
    if "triangle" in shape_type:
        return "triangle"
    elif "square" in shape_type or "rectangle" in shape_type:
        return "quadrilateral"
    elif "pentagon" in shape_type:
        return "pentagon"
    elif "hexagon" in shape_type:
        return "hexagon"
    elif "star" in shape_type:
        return "star"
    elif "circle" in shape_type or "oval" in shape_type or "ellipse" in shape_type:
        return "curved"
    elif "open" in shape_type or "arc" in shape_type or any(x in shape_type for x in ["V_", "U_", "C_", "S_"]):
        return "open"
    else:
        return "other"

def generate_new_question():
    """Generate a new polygon identification question based on difficulty"""
    
    difficulty = st.session_state.polygon_difficulty
    
    # Keep track of recent shapes to avoid repetition
    if len(st.session_state.recent_shapes) > 8:
        st.session_state.recent_shapes = st.session_state.recent_shapes[-4:]
    
    # Reset category count every 20 questions for fresh distribution
    if st.session_state.total_attempted % 20 == 0:
        st.session_state.shape_category_count = {}
    
    # Generate ALL possible shapes for this difficulty level
    all_shapes = get_shapes_for_difficulty(difficulty)
    
    # Validate all shapes (ensure triangles are correctly classified)
    for shape in all_shapes:
        if "triangle" in shape["type"].lower():
            # Only open or curved triangles are non-polygons
            if "open" in shape["type"] or "curved" in shape["type"] or "rounded" in shape["type"]:
                shape["is_polygon"] = False
            else:
                shape["is_polygon"] = True  # All closed triangles are polygons
    
    # Filter out recently used shapes
    available_shapes = [s for s in all_shapes if s["type"] not in st.session_state.recent_shapes]
    
    # If we've used too many shapes, reset
    if len(available_shapes) < 5:
        st.session_state.recent_shapes = []
        available_shapes = all_shapes
    
    # Balance selection by category to avoid too many triangles
    category_weights = {}
    for shape in available_shapes:
        category = get_shape_category(shape["type"])
        count = st.session_state.shape_category_count.get(category, 0)
        # Give lower weight to frequently shown categories
        weight = 1.0 / (count + 1)
        category_weights[shape["type"]] = weight
    
    # Weighted random selection
    if category_weights:
        weights = [category_weights[s["type"]] for s in available_shapes]
        shape = random.choices(available_shapes, weights=weights, k=1)[0]
    else:
        shape = random.choice(available_shapes)
    
    # Update category count
    category = get_shape_category(shape["type"])
    st.session_state.shape_category_count[category] = st.session_state.shape_category_count.get(category, 0) + 1
    
    # Add to recent shapes
    st.session_state.recent_shapes.append(shape["type"])
    
    # Add random rotation for variety (except for certain shapes)
    if shape["type"] not in ["circle", "circle_small", "circle_large"]:
        rotation = random.randint(0, 359)
    else:
        rotation = 0
    
    # Generate SVG for the shape with rotation
    svg_code = generate_shape_svg(shape["type"], shape["color"], rotation)
    
    # Store question data
    st.session_state.question_data = {
        "shape_type": shape["type"],
        "is_polygon": shape["is_polygon"],
        "svg_code": svg_code,
        "color": shape["color"]
    }
    
    st.session_state.correct_answer = "yes" if shape["is_polygon"] else "no"
    st.session_state.current_question = "Is this a polygon?"

def get_shapes_for_difficulty(difficulty):
    """Get all available shapes for a given difficulty level"""
    
    # Extended color palette
    colors = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
        "#FD79A8", "#A29BFE", "#6C5CE7", "#00B894", "#00CEC9",
        "#0984E3", "#E17055", "#FDCB6E", "#55A3FF", "#FA8231",
        "#F8B500", "#5F27CD", "#00D2D3", "#8395A7", "#222F3E"
    ]
    
    if difficulty == 1:
        # Basic shapes - very obvious
        shapes = [
            # Polygons - ALL CLOSED SHAPES WITH STRAIGHT SIDES
            {"type": "triangle_equilateral", "is_polygon": True},
            {"type": "triangle_right", "is_polygon": True},
            {"type": "square", "is_polygon": True},
            {"type": "rectangle", "is_polygon": True},
            {"type": "pentagon_regular", "is_polygon": True},
            {"type": "hexagon_regular", "is_polygon": True},
            {"type": "diamond", "is_polygon": True},
            
            # Non-polygons - ONLY shapes with curves or gaps
            {"type": "circle", "is_polygon": False},
            {"type": "oval_horizontal", "is_polygon": False},
            {"type": "semicircle", "is_polygon": False},
            {"type": "crescent", "is_polygon": False},
            {"type": "heart", "is_polygon": False},
        ]
    
    elif difficulty == 2:
        # Mixed regular shapes
        shapes = [
            # Polygons
            {"type": "triangle_isosceles", "is_polygon": True},
            {"type": "triangle_scalene", "is_polygon": True},
            {"type": "parallelogram", "is_polygon": True},
            {"type": "rhombus", "is_polygon": True},
            {"type": "trapezoid", "is_polygon": True},
            {"type": "kite", "is_polygon": True},
            {"type": "octagon", "is_polygon": True},
            {"type": "heptagon", "is_polygon": True},
            {"type": "house_shape", "is_polygon": True},
            {"type": "arrow_simple", "is_polygon": True},
            
            # Non-polygons
            {"type": "circle_small", "is_polygon": False},
            {"type": "ellipse_wide", "is_polygon": False},
            {"type": "oval_vertical", "is_polygon": False},
            {"type": "quarter_circle", "is_polygon": False},
            {"type": "teardrop", "is_polygon": False},
            {"type": "curved_triangle", "is_polygon": False},
            {"type": "rounded_square", "is_polygon": False},
        ]
    
    elif difficulty == 3:
        # Irregular and open shapes
        shapes = [
            # Polygons
            {"type": "irregular_triangle", "is_polygon": True},
            {"type": "irregular_quadrilateral", "is_polygon": True},
            {"type": "irregular_pentagon", "is_polygon": True},
            {"type": "irregular_hexagon", "is_polygon": True},
            {"type": "L_shape", "is_polygon": True},
            {"type": "T_shape", "is_polygon": True},
            {"type": "cross_shape", "is_polygon": True},
            {"type": "plus_sign", "is_polygon": True},
            {"type": "zigzag_closed", "is_polygon": True},
            
            # Non-polygons - open shapes
            {"type": "open_triangle", "is_polygon": False},
            {"type": "open_square", "is_polygon": False},
            {"type": "open_pentagon", "is_polygon": False},
            {"type": "chevron_open", "is_polygon": False},
            {"type": "V_shape", "is_polygon": False},
            {"type": "U_shape", "is_polygon": False},
            {"type": "C_shape", "is_polygon": False},
            {"type": "arc", "is_polygon": False},
            {"type": "wavy_closed", "is_polygon": False},
        ]
    
    elif difficulty == 4:
        # Complex and concave shapes
        shapes = [
            # Polygons
            {"type": "star_5point", "is_polygon": True},
            {"type": "star_6point", "is_polygon": True},
            {"type": "star_8point", "is_polygon": True},
            {"type": "concave_pentagon", "is_polygon": True},
            {"type": "concave_hexagon", "is_polygon": True},
            {"type": "arrow_complex", "is_polygon": True},
            {"type": "E_shape", "is_polygon": True},
            {"type": "F_shape", "is_polygon": True},
            {"type": "gear_simple", "is_polygon": True},
            {"type": "irregular_octagon", "is_polygon": True},
            
            # Non-polygons
            {"type": "cloud_shape", "is_polygon": False},
            {"type": "flower_shape", "is_polygon": False},
            {"type": "curved_star", "is_polygon": False},
            {"type": "rounded_rectangle", "is_polygon": False},
            {"type": "blob_shape", "is_polygon": False},
            {"type": "S_curve", "is_polygon": False},
            {"type": "infinity", "is_polygon": False},
            {"type": "partial_circle", "is_polygon": False},
        ]
    
    else:  # difficulty 5
        # Challenging cases
        shapes = [
            # Polygons
            {"type": "self_intersecting", "is_polygon": True},
            {"type": "complex_star", "is_polygon": True},
            {"type": "irregular_complex", "is_polygon": True},
            {"type": "decagon", "is_polygon": True},
            {"type": "nonagon", "is_polygon": True},
            {"type": "concave_complex", "is_polygon": True},
            {"type": "bowtie", "is_polygon": True},
            {"type": "hourglass", "is_polygon": True},
            
            # Non-polygons (tricky)
            {"type": "almost_closed", "is_polygon": False},
            {"type": "tiny_gap", "is_polygon": False},
            {"type": "rounded_corners_subtle", "is_polygon": False},
            {"type": "mixed_straight_curved", "is_polygon": False},
            {"type": "disconnected_segments", "is_polygon": False},
            {"type": "horseshoe", "is_polygon": False},
            {"type": "spiral_open", "is_polygon": False},
        ]
    
    # Add random colors to shapes and ensure balanced distribution
    for shape in shapes:
        shape["color"] = random.choice(colors)
    
    # Shuffle to ensure random order
    random.shuffle(shapes)
    
    return shapes

def generate_shape_svg(shape_type, color, rotation=0):
    """Generate SVG code for different shape types with rotation"""
    
    # Base SVG setup
    width = 300
    height = 300
    center_x = width // 2
    center_y = height // 2
    
    # Transform for rotation
    transform = f'transform="rotate({rotation} {center_x} {center_y})"' if rotation != 0 else ''
    
    # TRIANGLES - All closed triangles are polygons
    if shape_type == "triangle_equilateral":
        points = []
        for i in range(3):
            angle = (i * 120 - 90) * math.pi / 180
            x = center_x + 80 * math.cos(angle)
            y = center_y + 80 * math.sin(angle)
            points.append(f"{x},{y}")
        svg = f'<svg width="{width}" height="{height}"><polygon points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "triangle_right":
        points = f"{center_x-70},{center_y+70} {center_x-70},{center_y-70} {center_x+70},{center_y+70}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "triangle_isosceles":
        points = f"{center_x},{center_y-80} {center_x-60},{center_y+60} {center_x+60},{center_y+60}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "triangle_scalene":
        points = f"{center_x-70},{center_y+50} {center_x-30},{center_y-70} {center_x+80},{center_y+40}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "irregular_triangle":
        points = f"{center_x-70},{center_y+60} {center_x-20},{center_y-80} {center_x+75},{center_y+45}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    # QUADRILATERALS
    elif shape_type == "square":
        svg = f'<svg width="{width}" height="{height}"><rect x="{center_x-70}" y="{center_y-70}" width="140" height="140" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "rectangle":
        svg = f'<svg width="{width}" height="{height}"><rect x="{center_x-90}" y="{center_y-50}" width="180" height="100" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "diamond":
        points = f"{center_x},50 {center_x+75},150 {center_x},250 {center_x-75},150"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "parallelogram":
        points = f"{center_x-70},{center_y+50} {center_x-30},{center_y-50} {center_x+70},{center_y-50} {center_x+30},{center_y+50}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "rhombus":
        points = f"{center_x},{center_y-70} {center_x+50},{center_y} {center_x},{center_y+70} {center_x-50},{center_y}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "trapezoid":
        points = f"{center_x-50},{center_y-40} {center_x+50},{center_y-40} {center_x+80},{center_y+40} {center_x-80},{center_y+40}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "kite":
        points = f"{center_x},{center_y-90} {center_x+40},{center_y-20} {center_x},{center_y+70} {center_x-40},{center_y-20}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "irregular_quadrilateral":
        points = f"{center_x-65},{center_y-45} {center_x+55},{center_y-60} {center_x+70},{center_y+55} {center_x-50},{center_y+65}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    # REGULAR POLYGONS
    elif shape_type == "pentagon_regular":
        points = []
        for i in range(5):
            angle = (i * 72 - 90) * math.pi / 180
            x = center_x + 80 * math.cos(angle)
            y = center_y + 80 * math.sin(angle)
            points.append(f"{x},{y}")
        svg = f'<svg width="{width}" height="{height}"><polygon points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "hexagon_regular":
        points = []
        for i in range(6):
            angle = (i * 60) * math.pi / 180
            x = center_x + 80 * math.cos(angle)
            y = center_y + 80 * math.sin(angle)
            points.append(f"{x},{y}")
        svg = f'<svg width="{width}" height="{height}"><polygon points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "heptagon":
        points = []
        for i in range(7):
            angle = (i * 360/7 - 90) * math.pi / 180
            x = center_x + 80 * math.cos(angle)
            y = center_y + 80 * math.sin(angle)
            points.append(f"{x},{y}")
        svg = f'<svg width="{width}" height="{height}"><polygon points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "octagon":
        points = []
        for i in range(8):
            angle = (i * 45) * math.pi / 180
            x = center_x + 80 * math.cos(angle)
            y = center_y + 80 * math.sin(angle)
            points.append(f"{x},{y}")
        svg = f'<svg width="{width}" height="{height}"><polygon points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "nonagon":
        points = []
        for i in range(9):
            angle = (i * 40) * math.pi / 180
            x = center_x + 80 * math.cos(angle)
            y = center_y + 80 * math.sin(angle)
            points.append(f"{x},{y}")
        svg = f'<svg width="{width}" height="{height}"><polygon points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "decagon":
        points = []
        for i in range(10):
            angle = (i * 36) * math.pi / 180
            x = center_x + 80 * math.cos(angle)
            y = center_y + 80 * math.sin(angle)
            points.append(f"{x},{y}")
        svg = f'<svg width="{width}" height="{height}"><polygon points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    # IRREGULAR POLYGONS
    elif shape_type == "irregular_pentagon":
        points = f"{center_x-60},{center_y-40} {center_x+20},{center_y-70} {center_x+70},{center_y-10} {center_x+40},{center_y+60} {center_x-50},{center_y+50}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "irregular_hexagon":
        points = f"{center_x-70},{center_y-30} {center_x-20},{center_y-60} {center_x+50},{center_y-40} {center_x+70},{center_y+20} {center_x+10},{center_y+70} {center_x-60},{center_y+40}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "irregular_octagon":
        points = f"{center_x-50},{center_y-60} {center_x+10},{center_y-70} {center_x+60},{center_y-40} {center_x+75},{center_y+5} {center_x+45},{center_y+55} {center_x-10},{center_y+70} {center_x-65},{center_y+35} {center_x-75},{center_y-20}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    # SPECIAL SHAPES
    elif shape_type == "house_shape":
        points = f"{center_x-60},{center_y+60} {center_x-60},{center_y} {center_x},{center_y-60} {center_x+60},{center_y} {center_x+60},{center_y+60}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "arrow_simple":
        points = f"{center_x-60},{center_y} {center_x},{center_y-60} {center_x},{center_y-20} {center_x+60},{center_y-20} {center_x+60},{center_y+20} {center_x},{center_y+20} {center_x},{center_y+60}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "arrow_complex":
        points = f"{center_x-70},{center_y} {center_x-20},{center_y-50} {center_x-20},{center_y-20} {center_x+50},{center_y-20} {center_x+50},{center_y-40} {center_x+80},{center_y} {center_x+50},{center_y+40} {center_x+50},{center_y+20} {center_x-20},{center_y+20} {center_x-20},{center_y+50}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "L_shape":
        points = f"{center_x-60},{center_y-60} {center_x},{center_y-60} {center_x},{center_y} {center_x+60},{center_y} {center_x+60},{center_y+60} {center_x-60},{center_y+60}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "T_shape":
        points = f"{center_x-70},{center_y-50} {center_x+70},{center_y-50} {center_x+70},{center_y-10} {center_x+20},{center_y-10} {center_x+20},{center_y+70} {center_x-20},{center_y+70} {center_x-20},{center_y-10} {center_x-70},{center_y-10}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "E_shape":
        points = f"{center_x-60},{center_y-60} {center_x+60},{center_y-60} {center_x+60},{center_y-30} {center_x-30},{center_y-30} {center_x-30},{center_y-10} {center_x+40},{center_y-10} {center_x+40},{center_y+10} {center_x-30},{center_y+10} {center_x-30},{center_y+30} {center_x+60},{center_y+30} {center_x+60},{center_y+60} {center_x-60},{center_y+60}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "F_shape":
        points = f"{center_x-60},{center_y-60} {center_x+60},{center_y-60} {center_x+60},{center_y-30} {center_x-30},{center_y-30} {center_x-30},{center_y-10} {center_x+40},{center_y-10} {center_x+40},{center_y+10} {center_x-30},{center_y+10} {center_x-30},{center_y+60} {center_x-60},{center_y+60}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "cross_shape":
        points = f"{center_x-20},{center_y-60} {center_x+20},{center_y-60} {center_x+20},{center_y-20} {center_x+60},{center_y-20} {center_x+60},{center_y+20} {center_x+20},{center_y+20} {center_x+20},{center_y+60} {center_x-20},{center_y+60} {center_x-20},{center_y+20} {center_x-60},{center_y+20} {center_x-60},{center_y-20} {center_x-20},{center_y-20}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "plus_sign":
        points = f"{center_x-10},{center_y-70} {center_x+10},{center_y-70} {center_x+10},{center_y-10} {center_x+70},{center_y-10} {center_x+70},{center_y+10} {center_x+10},{center_y+10} {center_x+10},{center_y+70} {center_x-10},{center_y+70} {center_x-10},{center_y+10} {center_x-70},{center_y+10} {center_x-70},{center_y-10} {center_x-10},{center_y-10}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "zigzag_closed":
        points = f"{center_x-60},{center_y-50} {center_x-30},{center_y-20} {center_x},{center_y-50} {center_x+30},{center_y-20} {center_x+60},{center_y-50} {center_x+60},{center_y+50} {center_x+30},{center_y+20} {center_x},{center_y+50} {center_x-30},{center_y+20} {center_x-60},{center_y+50}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    # STARS
    elif shape_type.startswith("star_"):
        if "5point" in shape_type:
            num_points = 5
        elif "6point" in shape_type:
            num_points = 6
        elif "8point" in shape_type:
            num_points = 8
        else:
            num_points = 5
        
        outer_points = []
        inner_points = []
        for i in range(num_points):
            # Outer points
            angle = (i * 360/num_points - 90) * math.pi / 180
            x = center_x + 85 * math.cos(angle)
            y = center_y + 85 * math.sin(angle)
            outer_points.append((x, y))
            # Inner points
            angle = ((i * 360/num_points) + 180/num_points - 90) * math.pi / 180
            x = center_x + 35 * math.cos(angle)
            y = center_y + 35 * math.sin(angle)
            inner_points.append((x, y))
        
        points = []
        for i in range(num_points):
            points.append(f"{outer_points[i][0]},{outer_points[i][1]}")
            points.append(f"{inner_points[i][0]},{inner_points[i][1]}")
        
        svg = f'<svg width="{width}" height="{height}"><polygon points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "complex_star":
        # 12-pointed star
        points = []
        for i in range(24):
            if i % 2 == 0:
                r = 90
            else:
                r = 40
            angle = (i * 15) * math.pi / 180
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.append(f"{x},{y}")
        svg = f'<svg width="{width}" height="{height}"><polygon points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    # CONCAVE POLYGONS
    elif shape_type == "concave_pentagon":
        points = f"{center_x-60},{center_y-60} {center_x+60},{center_y-60} {center_x+20},{center_y} {center_x+60},{center_y+60} {center_x-60},{center_y+60}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "concave_hexagon":
        points = f"{center_x-60},{center_y-50} {center_x},{center_y-30} {center_x+60},{center_y-50} {center_x+60},{center_y+50} {center_x},{center_y+30} {center_x-60},{center_y+50}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "concave_complex":
        points = f"{center_x-70},{center_y-40} {center_x-20},{center_y-60} {center_x+30},{center_y-40} {center_x+70},{center_y-60} {center_x+50},{center_y} {center_x+70},{center_y+60} {center_x},{center_y+40} {center_x-70},{center_y+60}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "gear_simple":
        points = []
        for i in range(12):
            if i % 2 == 0:
                r = 80
            else:
                r = 60
            angle = (i * 30) * math.pi / 180
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.append(f"{x},{y}")
        svg = f'<svg width="{width}" height="{height}"><polygon points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "self_intersecting":
        # Bowtie shape
        points = f"{center_x-60},{center_y-60} {center_x+60},{center_y+60} {center_x+60},{center_y-60} {center_x-60},{center_y+60}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "bowtie":
        points = f"{center_x-60},{center_y-40} {center_x},{center_y} {center_x-60},{center_y+40} {center_x+60},{center_y+40} {center_x},{center_y} {center_x+60},{center_y-40}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "hourglass":
        points = f"{center_x-50},{center_y-70} {center_x+50},{center_y-70} {center_x},{center_y} {center_x+50},{center_y+70} {center_x-50},{center_y+70} {center_x},{center_y}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "irregular_complex":
        points = f"{center_x-60},{center_y-50} {center_x-20},{center_y-70} {center_x+30},{center_y-50} {center_x+60},{center_y-60} {center_x+70},{center_y-20} {center_x+40},{center_y+10} {center_x+50},{center_y+50} {center_x},{center_y+60} {center_x-40},{center_y+40} {center_x-70},{center_y}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    # NON-POLYGONS - CIRCLES AND CURVES
    elif shape_type == "circle":
        svg = f'<svg width="{width}" height="{height}"><circle cx="{center_x}" cy="{center_y}" r="80" fill="none" stroke="{color}" stroke-width="3"/></svg>'
    
    elif shape_type == "circle_small":
        svg = f'<svg width="{width}" height="{height}"><circle cx="{center_x}" cy="{center_y}" r="50" fill="none" stroke="{color}" stroke-width="3"/></svg>'
    
    elif shape_type == "oval_horizontal":
        svg = f'<svg width="{width}" height="{height}"><ellipse cx="{center_x}" cy="{center_y}" rx="100" ry="60" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "oval_vertical":
        svg = f'<svg width="{width}" height="{height}"><ellipse cx="{center_x}" cy="{center_y}" rx="60" ry="100" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "ellipse_wide":
        svg = f'<svg width="{width}" height="{height}"><ellipse cx="{center_x}" cy="{center_y}" rx="110" ry="50" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "semicircle":
        path = f"M {center_x-80} {center_y} A 80 80 0 0 1 {center_x+80} {center_y}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "quarter_circle":
        path = f"M {center_x} {center_y} L {center_x+80} {center_y} A 80 80 0 0 1 {center_x} {center_y+80} L {center_x} {center_y}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "crescent":
        path = f"M {center_x-60} {center_y} A 60 60 0 1 1 {center_x+60} {center_y} A 40 40 0 1 0 {center_x-60} {center_y}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "heart":
        path = f"M {center_x} {center_y+40} C {center_x-40} {center_y} {center_x-40} {center_y-40} {center_x} {center_y-20} C {center_x+40} {center_y-40} {center_x+40} {center_y} {center_x} {center_y+40}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "teardrop":
        path = f"M {center_x} {center_y-60} Q {center_x-40} {center_y} {center_x} {center_y+60} Q {center_x+40} {center_y} {center_x} {center_y-60}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "curved_triangle":
        path = f"M {center_x} {center_y-60} Q {center_x-80} {center_y} {center_x-60} {center_y+60} Q {center_x} {center_y+40} {center_x+60} {center_y+60} Q {center_x+80} {center_y} {center_x} {center_y-60}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "rounded_square":
        svg = f'<svg width="{width}" height="{height}"><rect x="{center_x-70}" y="{center_y-70}" width="140" height="140" rx="35" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "rounded_rectangle":
        svg = f'<svg width="{width}" height="{height}"><rect x="{center_x-90}" y="{center_y-50}" width="180" height="100" rx="40" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "cloud_shape":
        path = f"M {center_x-40} {center_y+20} Q {center_x-60} {center_y} {center_x-50} {center_y-20} Q {center_x-40} {center_y-40} {center_x-10} {center_y-30} Q {center_x} {center_y-50} {center_x+20} {center_y-30} Q {center_x+50} {center_y-30} {center_x+50} {center_y} Q {center_x+50} {center_y+30} {center_x+20} {center_y+30} Q {center_x} {center_y+40} {center_x-20} {center_y+30} Q {center_x-40} {center_y+30} {center_x-40} {center_y+20}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "wavy_closed":
        path = f"M {center_x-60} {center_y} Q {center_x-30} {center_y-60} {center_x} {center_y} Q {center_x+30} {center_y+60} {center_x+60} {center_y} Q {center_x+30} {center_y-60} {center_x} {center_y} Q {center_x-30} {center_y+60} {center_x-60} {center_y}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "blob_shape":
        path = f"M {center_x-50} {center_y} Q {center_x-60} {center_y-40} {center_x-20} {center_y-50} Q {center_x+20} {center_y-60} {center_x+40} {center_y-30} Q {center_x+60} {center_y} {center_x+40} {center_y+30} Q {center_x+20} {center_y+60} {center_x-20} {center_y+50} Q {center_x-60} {center_y+40} {center_x-50} {center_y}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "flower_shape":
        petals = []
        for i in range(6):
            angle = i * 60 * math.pi / 180
            cx = center_x + 40 * math.cos(angle)
            cy = center_y + 40 * math.sin(angle)
            petals.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="none" stroke="{color}" stroke-width="3"/>')
        petals.append(f'<circle cx="{center_x}" cy="{center_y}" r="25" fill="none" stroke="{color}" stroke-width="3"/>')
        svg = f'<svg width="{width}" height="{height}">{"".join(petals)}</svg>'
    
    elif shape_type == "curved_star":
        path_parts = []
        for i in range(5):
            angle1 = (i * 72 - 90) * math.pi / 180
            angle2 = ((i * 72) + 36 - 90) * math.pi / 180
            x1 = center_x + 85 * math.cos(angle1)
            y1 = center_y + 85 * math.sin(angle1)
            x2 = center_x + 35 * math.cos(angle2)
            y2 = center_y + 35 * math.sin(angle2)
            if i == 0:
                path_parts.append(f"M {x1} {y1}")
            path_parts.append(f"Q {center_x} {center_y} {x2} {y2}")
            angle3 = ((i + 1) * 72 - 90) * math.pi / 180
            x3 = center_x + 85 * math.cos(angle3)
            y3 = center_y + 85 * math.sin(angle3)
            path_parts.append(f"Q {center_x} {center_y} {x3} {y3}")
        path = " ".join(path_parts)
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "infinity":
        path = f"M {center_x-50} {center_y} Q {center_x-50} {center_y-40} {center_x-20} {center_y-40} Q {center_x} {center_y-40} {center_x} {center_y} Q {center_x} {center_y+40} {center_x+20} {center_y+40} Q {center_x+50} {center_y+40} {center_x+50} {center_y} Q {center_x+50} {center_y-40} {center_x+20} {center_y-40} Q {center_x} {center_y-40} {center_x} {center_y} Q {center_x} {center_y+40} {center_x-20} {center_y+40} Q {center_x-50} {center_y+40} {center_x-50} {center_y}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "S_curve":
        path = f"M {center_x-50} {center_y+50} Q {center_x-50} {center_y} {center_x} {center_y} Q {center_x+50} {center_y} {center_x+50} {center_y-50}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    # OPEN SHAPES - NOT POLYGONS
    elif shape_type == "open_triangle":
        points = f"{center_x-60},{center_y+50} {center_x},{center_y-60} {center_x+60},{center_y+50}"
        svg = f'<svg width="{width}" height="{height}"><polyline points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "open_square":
        points = f"{center_x-60},{center_y-60} {center_x+60},{center_y-60} {center_x+60},{center_y+60} {center_x-60},{center_y+60} {center_x-60},{center_y}"
        svg = f'<svg width="{width}" height="{height}"><polyline points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "open_pentagon":
        points_list = []
        for i in range(4):  # Only 4 sides instead of 5
            angle = (i * 72 - 90) * math.pi / 180
            x = center_x + 80 * math.cos(angle)
            y = center_y + 80 * math.sin(angle)
            points_list.append(f"{x},{y}")
        points = " ".join(points_list)
        svg = f'<svg width="{width}" height="{height}"><polyline points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "chevron_open":
        points = f"{center_x-70},{center_y+30} {center_x},{center_y-50} {center_x+70},{center_y+30}"
        svg = f'<svg width="{width}" height="{height}"><polyline points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "V_shape":
        points = f"{center_x-50},{center_y-50} {center_x},{center_y+50} {center_x+50},{center_y-50}"
        svg = f'<svg width="{width}" height="{height}"><polyline points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "U_shape":
        path = f"M {center_x-60} {center_y-60} L {center_x-60} {center_y+30} Q {center_x-60} {center_y+60} {center_x-30} {center_y+60} L {center_x+30} {center_y+60} Q {center_x+60} {center_y+60} {center_x+60} {center_y+30} L {center_x+60} {center_y-60}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "C_shape":
        path = f"M {center_x+50} {center_y-50} Q {center_x-50} {center_y-50} {center_x-50} {center_y} Q {center_x-50} {center_y+50} {center_x+50} {center_y+50}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "arc":
        path = f"M {center_x-70} {center_y} A 70 70 0 0 1 {center_x+70} {center_y}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "partial_circle":
        path = f"M {center_x-60} {center_y-30} A 70 70 0 1 1 {center_x+60} {center_y-30}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "horseshoe":
        path = f"M {center_x-50} {center_y+60} L {center_x-50} {center_y-20} A 50 50 0 0 1 {center_x+50} {center_y-20} L {center_x+50} {center_y+60}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "spiral_open":
        path_parts = []
        for i in range(3):
            r = 20 + i * 25
            if i == 0:
                path_parts.append(f"M {center_x} {center_y-r}")
            path_parts.append(f"A {r} {r} 0 0 1 {center_x} {center_y+r}")
            r += 12
            path_parts.append(f"A {r} {r} 0 0 1 {center_x} {center_y-r-10}")
        path = " ".join(path_parts)
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "almost_closed":
        # Square with tiny gap
        points = f"{center_x-60},{center_y-60} {center_x+60},{center_y-60} {center_x+60},{center_y+60} {center_x-60},{center_y+60} {center_x-60},{center_y-55}"
        svg = f'<svg width="{width}" height="{height}"><polyline points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "tiny_gap":
        # Pentagon with a very small gap
        points_list = []
        for i in range(5):
            angle = (i * 72 - 90) * math.pi / 180
            x = center_x + 80 * math.cos(angle)
            y = center_y + 80 * math.sin(angle)
            if i < 4:  # Skip connecting to the last point
                points_list.append(f"{x},{y}")
        points = " ".join(points_list)
        svg = f'<svg width="{width}" height="{height}"><polyline points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "disconnected_segments":
        # Multiple disconnected lines
        seg1 = f'<line x1="{center_x-60}" y1="{center_y-60}" x2="{center_x}" y2="{center_y-60}" stroke="{color}" stroke-width="3"/>'
        seg2 = f'<line x1="{center_x+10}" y1="{center_y-60}" x2="{center_x+60}" y2="{center_y}" stroke="{color}" stroke-width="3"/>'
        seg3 = f'<line x1="{center_x+60}" y1="{center_y+10}" x2="{center_x}" y2="{center_y+60}" stroke="{color}" stroke-width="3"/>'
        seg4 = f'<line x1="{center_x-10}" y1="{center_y+60}" x2="{center_x-60}" y2="{center_y}" stroke="{color}" stroke-width="3"/>'
        svg = f'<svg width="{width}" height="{height}">{seg1}{seg2}{seg3}{seg4}</svg>'
    
    elif shape_type == "rounded_corners_subtle":
        # Square with subtle rounded corners
        svg = f'<svg width="{width}" height="{height}"><rect x="{center_x-70}" y="{center_y-70}" width="140" height="140" rx="15" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    elif shape_type == "mixed_straight_curved":
        # Shape with both straight and curved sides
        path = f"M {center_x-60} {center_y-60} L {center_x+60} {center_y-60} Q {center_x+80} {center_y} {center_x+60} {center_y+60} L {center_x-60} {center_y+60} Q {center_x-80} {center_y} {center_x-60} {center_y-60}"
        svg = f'<svg width="{width}" height="{height}"><path d="{path}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    else:
        # Default fallback - simple triangle
        points = f"{center_x},{center_y-70} {center_x-60},{center_y+50} {center_x+60},{center_y+50}"
        svg = f'<svg width="{width}" height="{height}"><polygon points="{points}" fill="none" stroke="{color}" stroke-width="3" {transform}/></svg>'
    
    return svg

def display_question():
    """Display the current question"""
    
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_question}")
    
    # Display the shape
    st.markdown("")  # Add space
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(data["svg_code"], unsafe_allow_html=True)
    
    # Create answer options
    st.markdown("")  # Add some space
    
    if not st.session_state.answer_submitted:
        # Show clickable options - horizontal layout
        cols = st.columns(2)
        
        options = ["yes", "no"]
        for i, option in enumerate(options):
            with cols[i]:
                # Style the button based on selection
                button_type = "primary" if option == st.session_state.selected_answer else "secondary"
                
                if st.button(
                    option,
                    key=f"option_{i}",
                    use_container_width=True,
                    type=button_type
                ):
                    st.session_state.selected_answer = option
                    st.rerun()
        
        # Submit button
        st.markdown("")  # Add space
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "✅ Submit",
                type="primary",
                use_container_width=True,
                disabled=(st.session_state.selected_answer is None)
            ):
                if st.session_state.selected_answer:
                    st.session_state.answer_submitted = True
                    st.session_state.total_attempted += 1
                    if st.session_state.selected_answer == st.session_state.correct_answer:
                        st.session_state.total_correct += 1
                    st.rerun()
    
    else:
        # Show results after submission
        cols = st.columns(2)
        
        options = ["yes", "no"]
        for i, option in enumerate(options):
            with cols[i]:
                if option == st.session_state.correct_answer:
                    # Correct answer - show in green
                    st.success(f"✓ {option}")
                elif option == st.session_state.selected_answer and option != st.session_state.correct_answer:
                    # Wrong answer selected - show in red
                    st.error(f"✗ {option}")
                else:
                    # Other option - show disabled
                    st.button(option, disabled=True, use_container_width=True)
        
        # Show feedback
        show_feedback()
        
        # Next question button
        st.markdown("")  # Add space
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    
    user_answer = st.session_state.selected_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    st.markdown("---")
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.polygon_difficulty
            st.session_state.polygon_difficulty = min(
                st.session_state.polygon_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.polygon_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.polygon_difficulty}**")
    
    else:
        if correct_answer == "yes":
            st.error("❌ **Not quite right. This IS a polygon.**")
        else:
            st.error("❌ **Not quite right. This is NOT a polygon.**")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.polygon_difficulty
            st.session_state.polygon_difficulty = max(
                st.session_state.polygon_difficulty - 1, 1
            )
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.polygon_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.polygon_difficulty}. Keep practicing!**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show explanation for why it is or isn't a polygon"""
    
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        shape_type = data["shape_type"]
        is_polygon = data["is_polygon"]
        
        if is_polygon:
            st.markdown("### ✅ This IS a polygon because:")
            st.markdown("""
            - It's a **closed** figure (completely enclosed)
            - All sides are **straight lines**
            - It has **3 or more sides**
            - Meets all requirements for a polygon!
            """)
            
            # Specific details for special cases
            if "self_intersecting" in shape_type or "bowtie" in shape_type:
                st.markdown("""
                **Note:** Even though the sides cross each other (self-intersecting), 
                it's still a polygon as long as it's closed with straight sides!
                """)
            elif "star" in shape_type:
                st.markdown("""
                **Note:** Stars are polygons when made with straight lines, 
                even though they have points going in and out!
                """)
            elif "concave" in shape_type:
                st.markdown("""
                **Note:** Polygons can be concave (have dents or indentations) 
                and still be valid polygons!
                """)
        
        else:
            st.markdown("### ❌ This is NOT a polygon because:")
            
            # Check for open shapes FIRST (most specific)
            if ("open" in shape_type or 
                "arc" in shape_type or 
                "partial" in shape_type or
                "almost_closed" in shape_type or
                "tiny_gap" in shape_type or
                "broken" in shape_type or
                "horseshoe" in shape_type or
                "spiral" in shape_type or
                "chevron_open" in shape_type or
                shape_type in ["V_shape", "U_shape", "C_shape", "S_curve"]):
                st.markdown("""
                - It's **not closed** (has an opening or gap)
                - Polygons must be completely closed figures
                - You can't trace around it without lifting your pencil
                """)
            
            # Then check for curved shapes
            elif ("circle" in shape_type or 
                  "oval" in shape_type or 
                  "ellipse" in shape_type or
                  "curved" in shape_type or
                  "wavy" in shape_type or
                  "rounded" in shape_type or
                  "heart" in shape_type or
                  "teardrop" in shape_type or
                  "crescent" in shape_type or
                  "cloud" in shape_type or
                  "blob" in shape_type or
                  "flower" in shape_type or
                  "infinity" in shape_type or
                  "semicircle" in shape_type or
                  "quarter_circle" in shape_type):
                st.markdown("""
                - It has **curved sides**, not straight lines
                - Polygons must have only straight sides
                - Even one curve makes it not a polygon
                """)
            
            # Mixed straight and curved
            elif "mixed" in shape_type:
                st.markdown("""
                - It has **both straight and curved parts**
                - Polygons must have ONLY straight sides
                - Any curves disqualify it as a polygon
                """)
            
            # Disconnected segments
            elif "disconnected" in shape_type:
                st.markdown("""
                - It's made of **disconnected segments**
                - Polygons must be one continuous closed figure
                - All parts must be connected
                """)
            
            else:
                # Generic explanation
                st.markdown("""
                - It doesn't meet all the requirements for a polygon
                - Check: Is it closed? Are all sides straight? Does it have 3+ sides?
                """)
        
        # General reminder
        st.markdown("""
        ### Remember the 3 Rules:
        1. **Closed** - Can you trace it without lifting your pencil? ✏️
        2. **Straight sides** - No curves allowed! 📏
        3. **At least 3 sides** - Minimum requirement! 3️⃣
        
        All three must be true for a polygon!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None