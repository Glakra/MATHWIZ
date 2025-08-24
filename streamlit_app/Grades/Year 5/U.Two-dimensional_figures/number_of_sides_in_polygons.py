import streamlit as st
import random
import math

def run():
    """
    Main function to run the Number of Sides in Polygons practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/number_of_sides_in_polygons.py
    """
    
    # Initialize session state
    if "sides_difficulty" not in st.session_state:
        st.session_state.sides_difficulty = 1
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.recent_polygons = []
        st.session_state.shape_category_count = {}
        st.session_state.question_type_count = {"visual": 0, "text": 0}
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_answer = ""
        st.session_state.question_type = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("🔢 Number of Sides in Polygons")
    st.markdown("*Count the sides of different polygon shapes*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.sides_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic shapes (3-6 sides)",
            2: "Common polygons (3-8 sides)",
            3: "Advanced polygons (3-10 sides)",
            4: "Complex polygons (3-12 sides)",
            5: "Expert level (all polygons)"
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
        ### How to Count Polygon Sides:
        
        **A side is a straight line segment that forms part of the polygon's boundary.**
        
        ### Common Polygons and Their Sides:
        | Name | Sides | Memory Tip |
        |------|-------|------------|
        | **Triangle** | 3 | Tri = Three |
        | **Quadrilateral** | 4 | Quad = Four |
        | **Pentagon** | 5 | Penta = Five (like pentathlon) |
        | **Hexagon** | 6 | Hex = Six |
        | **Heptagon** | 7 | Hept = Seven |
        | **Octagon** | 8 | Oct = Eight (like octopus) |
        | **Nonagon** | 9 | Non = Nine |
        | **Decagon** | 10 | Dec = Ten (like decade) |
        | **Hendecagon** | 11 | Hendeca = Eleven |
        | **Dodecagon** | 12 | Dodeca = Twelve |
        
        ### Counting Tips:
        1. **Start at any corner** (vertex)
        2. **Count each straight line** until you return to start
        3. **Don't count corners** - count the lines between them
        4. **Regular or irregular** - the number of sides stays the same!
        
        ### Special Cases:
        - **Rectangle/Square** = 4 sides (types of quadrilaterals)
        - **Rhombus/Parallelogram** = 4 sides (also quadrilaterals)
        - **Any triangle** = 3 sides (equilateral, isosceles, scalene)
        """)

def get_polygon_reference_svg():
    """Generate a comprehensive reference chart of polygons"""
    
    width = 800
    height = 600
    
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg_parts.append('<rect width="800" height="600" fill="white" stroke="#ddd" stroke-width="2"/>')
    svg_parts.append('<text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#333">Polygon Reference Chart</text>')
    
    # Define polygon data for reference
    polygons = [
        {"name": "Triangle", "sides": 3, "pos": (100, 100)},
        {"name": "Square", "sides": 4, "pos": (250, 100)},
        {"name": "Pentagon", "sides": 5, "pos": (400, 100)},
        {"name": "Hexagon", "sides": 6, "pos": (550, 100)},
        {"name": "Heptagon", "sides": 7, "pos": (700, 100)},
        {"name": "Octagon", "sides": 8, "pos": (100, 300)},
        {"name": "Nonagon", "sides": 9, "pos": (250, 300)},
        {"name": "Decagon", "sides": 10, "pos": (400, 300)},
        {"name": "Hendecagon", "sides": 11, "pos": (550, 300)},
        {"name": "Dodecagon", "sides": 12, "pos": (700, 300)},
        {"name": "Parallelogram", "sides": 4, "pos": (100, 500), "special": True},
        {"name": "Rhombus", "sides": 4, "pos": (250, 500), "special": True},
        {"name": "Trapezoid", "sides": 4, "pos": (400, 500), "special": True},
        {"name": "Rectangle", "sides": 4, "pos": (550, 500), "special": True},
        {"name": "Kite", "sides": 4, "pos": (700, 500), "special": True},
    ]
    
    for polygon in polygons:
        cx, cy = polygon["pos"]
        radius = 40
        color = "#4CAF50" if not polygon.get("special") else "#2196F3"
        
        # Draw polygon
        if polygon["name"] == "Parallelogram":
            points = f"{cx-30},{cy+20} {cx-10},{cy-20} {cx+30},{cy-20} {cx+10},{cy+20}"
        elif polygon["name"] == "Rhombus":
            points = f"{cx},{cy-30} {cx+25},{cy} {cx},{cy+30} {cx-25},{cy}"
        elif polygon["name"] == "Trapezoid":
            points = f"{cx-20},{cy-20} {cx+20},{cy-20} {cx+30},{cy+20} {cx-30},{cy+20}"
        elif polygon["name"] == "Rectangle":
            points = f"{cx-35},{cy-20} {cx+35},{cy-20} {cx+35},{cy+20} {cx-35},{cy+20}"
        elif polygon["name"] == "Kite":
            points = f"{cx},{cy-35} {cx+20},{cy-10} {cx},{cy+25} {cx-20},{cy-10}"
        elif polygon["name"] == "Square":
            points = f"{cx-25},{cy-25} {cx+25},{cy-25} {cx+25},{cy+25} {cx-25},{cy+25}"
        else:
            # Regular polygon
            points_list = []
            for i in range(polygon["sides"]):
                angle = (i * 360/polygon["sides"] - 90) * math.pi / 180
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                points_list.append(f"{x},{y}")
            points = " ".join(points_list)
        
        svg_parts.append(f'<polygon points="{points}" fill="none" stroke="{color}" stroke-width="2"/>')
        
        # Add dots at vertices
        if polygon["sides"] <= 6 or polygon.get("special"):
            for point in points.split():
                x, y = point.split(",")
                svg_parts.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{color}"/>')
        
        # Add label
        svg_parts.append(f'<text x="{cx}" y="{cy+60}" text-anchor="middle" font-size="14" font-weight="bold" fill="#333">{polygon["name"]}</text>')
        svg_parts.append(f'<text x="{cx}" y="{cy+75}" text-anchor="middle" font-size="12" fill="#666">{polygon["sides"]} sides</text>')
    
    svg_parts.append('</svg>')
    return "".join(svg_parts)

def get_special_quadrilaterals_reference():
    """Generate reference for special quadrilaterals"""
    
    width = 700
    height = 400
    
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg_parts.append('<rect width="700" height="400" fill="#f9f9f9" stroke="#ddd" stroke-width="2"/>')
    svg_parts.append('<text x="350" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">Special Quadrilaterals (All have 4 sides)</text>')
    
    quads = [
        {
            "name": "Square",
            "properties": ["All sides equal", "All angles 90°"],
            "pos": (120, 120),
            "points": lambda cx, cy: f"{cx-40},{cy-40} {cx+40},{cy-40} {cx+40},{cy+40} {cx-40},{cy+40}"
        },
        {
            "name": "Rectangle", 
            "properties": ["Opposite sides equal", "All angles 90°"],
            "pos": (350, 120),
            "points": lambda cx, cy: f"{cx-60},{cy-35} {cx+60},{cy-35} {cx+60},{cy+35} {cx-60},{cy+35}"
        },
        {
            "name": "Rhombus",
            "properties": ["All sides equal", "Opposite angles equal"],
            "pos": (580, 120),
            "points": lambda cx, cy: f"{cx},{cy-45} {cx+40},{cy} {cx},{cy+45} {cx-40},{cy}"
        },
        {
            "name": "Parallelogram",
            "properties": ["Opposite sides equal", "Opposite angles equal"],
            "pos": (120, 280),
            "points": lambda cx, cy: f"{cx-50},{cy+30} {cx-20},{cy-30} {cx+50},{cy-30} {cx+20},{cy+30}"
        },
        {
            "name": "Trapezoid",
            "properties": ["One pair of parallel sides"],
            "pos": (350, 280),
            "points": lambda cx, cy: f"{cx-35},{cy-30} {cx+35},{cy-30} {cx+50},{cy+30} {cx-50},{cy+30}"
        },
        {
            "name": "Kite",
            "properties": ["Two pairs of adjacent equal sides"],
            "pos": (580, 280),
            "points": lambda cx, cy: f"{cx},{cy-50} {cx+30},{cy-10} {cx},{cy+40} {cx-30},{cy-10}"
        }
    ]
    
    for quad in quads:
        cx, cy = quad["pos"]
        points = quad["points"](cx, cy)
        
        # Draw shape
        svg_parts.append(f'<polygon points="{points}" fill="#E3F2FD" stroke="#1976D2" stroke-width="3"/>')
        
        # Add vertices
        for point in points.split():
            x, y = point.split(",")
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#1976D2"/>')
        
        # Add name
        svg_parts.append(f'<text x="{cx}" y="{cy+70}" text-anchor="middle" font-size="16" font-weight="bold" fill="#333">{quad["name"]}</text>')
        
        # Add properties
        for i, prop in enumerate(quad["properties"]):
            svg_parts.append(f'<text x="{cx}" y="{cy+85+i*15}" text-anchor="middle" font-size="11" fill="#666">{prop}</text>')
    
    svg_parts.append('</svg>')
    return "".join(svg_parts)

def get_polygon_data_for_difficulty(difficulty):
    """Get polygon data including text-only questions"""
    
    # Define all polygon types with their characteristics
    polygon_database = {
        # Basic (3-6 sides)
        "triangle": {"sides": 3, "difficulty": 1, "category": "basic"},
        "quadrilateral": {"sides": 4, "difficulty": 1, "category": "basic"},
        "square": {"sides": 4, "difficulty": 1, "category": "special"},
        "rectangle": {"sides": 4, "difficulty": 1, "category": "special"},
        "pentagon": {"sides": 5, "difficulty": 1, "category": "basic"},
        "hexagon": {"sides": 6, "difficulty": 1, "category": "basic"},
        
        # Common (7-8 sides)
        "heptagon": {"sides": 7, "difficulty": 2, "category": "common"},
        "septagon": {"sides": 7, "difficulty": 2, "category": "common", "alt_name": "heptagon"},
        "octagon": {"sides": 8, "difficulty": 2, "category": "common"},
        "parallelogram": {"sides": 4, "difficulty": 2, "category": "special"},
        "rhombus": {"sides": 4, "difficulty": 2, "category": "special"},
        "trapezoid": {"sides": 4, "difficulty": 2, "category": "special"},
        "trapezium": {"sides": 4, "difficulty": 2, "category": "special", "alt_name": "trapezoid"},
        "kite": {"sides": 4, "difficulty": 2, "category": "special"},
        "diamond": {"sides": 4, "difficulty": 2, "category": "special", "alt_name": "rhombus"},
        
        # Advanced (9-10 sides)
        "nonagon": {"sides": 9, "difficulty": 3, "category": "advanced"},
        "enneagon": {"sides": 9, "difficulty": 3, "category": "advanced", "alt_name": "nonagon"},
        "decagon": {"sides": 10, "difficulty": 3, "category": "advanced"},
        
        # Complex (11-12 sides)
        "hendecagon": {"sides": 11, "difficulty": 4, "category": "complex"},
        "undecagon": {"sides": 11, "difficulty": 4, "category": "complex", "alt_name": "hendecagon"},
        "dodecagon": {"sides": 12, "difficulty": 4, "category": "complex"},
        
        # Expert (13-20 sides)
        "tridecagon": {"sides": 13, "difficulty": 5, "category": "expert"},
        "triskaidecagon": {"sides": 13, "difficulty": 5, "category": "expert", "alt_name": "tridecagon"},
        "tetradecagon": {"sides": 14, "difficulty": 5, "category": "expert"},
        "pentadecagon": {"sides": 15, "difficulty": 5, "category": "expert"},
        "hexadecagon": {"sides": 16, "difficulty": 5, "category": "expert"},
        "heptadecagon": {"sides": 17, "difficulty": 5, "category": "expert"},
        "octadecagon": {"sides": 18, "difficulty": 5, "category": "expert"},
        "enneadecagon": {"sides": 19, "difficulty": 5, "category": "expert"},
        "icosagon": {"sides": 20, "difficulty": 5, "category": "expert"},
        "hectagon": {"sides": 100, "difficulty": 5, "category": "expert"},
        "chiliagon": {"sides": 1000, "difficulty": 5, "category": "expert"},
        "myriagon": {"sides": 10000, "difficulty": 5, "category": "expert"},
    }
    
    # Filter polygons by difficulty
    available_polygons = []
    for name, data in polygon_database.items():
        if data["difficulty"] <= difficulty:
            if not data.get("alt_name"):  # Skip alternate names to avoid duplicates
                available_polygons.append({
                    "name": name,
                    "sides": data["sides"],
                    "category": data["category"]
                })
    
    return available_polygons

def generate_new_question():
    """Generate a new polygon sides counting question (visual or text)"""
    
    difficulty = st.session_state.sides_difficulty
    
    # Balance between visual and text questions
    visual_count = st.session_state.question_type_count.get("visual", 0)
    text_count = st.session_state.question_type_count.get("text", 0)
    
    # Decide question type with bias toward less-used type
    if visual_count > text_count + 2:
        question_type = "text"
    elif text_count > visual_count + 2:
        question_type = "visual"
    else:
        # Random with slight preference for variety
        if difficulty >= 2:  # Start mixing in text questions from level 2
            question_type = random.choice(["visual", "visual", "text"])  # 2:1 ratio
        else:
            question_type = "visual"  # Only visual for beginners
    
    st.session_state.question_type = question_type
    st.session_state.question_type_count[question_type] = st.session_state.question_type_count.get(question_type, 0) + 1
    
    if question_type == "text":
        generate_text_question(difficulty)
    else:
        generate_visual_question(difficulty)

def generate_text_question(difficulty):
    """Generate a text-only question about polygon sides"""
    
    # Get available polygons
    available_polygons = get_polygon_data_for_difficulty(difficulty)
    
    # Filter out recently used
    if len(st.session_state.recent_polygons) > 6:
        st.session_state.recent_polygons = st.session_state.recent_polygons[-3:]
    
    available = [p for p in available_polygons if p["name"] not in st.session_state.recent_polygons]
    
    if not available:
        st.session_state.recent_polygons = []
        available = available_polygons
    
    # Select a polygon
    polygon = random.choice(available)
    st.session_state.recent_polygons.append(polygon["name"])
    
    # Create question variations
    question_templates = [
        f"How many sides does a {polygon['name']} have?",
        f"How many sides does an {polygon['name']} have?" if polygon['name'][0] in 'aeiou' else f"How many sides does a {polygon['name']} have?",
        f"A {polygon['name']} has how many sides?",
        f"What is the number of sides in a {polygon['name']}?",
        f"Count the sides: {polygon['name'].capitalize()}",
    ]
    
    # Store question data
    st.session_state.question_data = {
        "polygon_name": polygon["name"],
        "sides": polygon["sides"],
        "type": "text",
        "category": polygon["category"]
    }
    
    st.session_state.correct_answer = polygon["sides"]
    st.session_state.current_question = random.choice(question_templates)

def generate_visual_question(difficulty):
    """Generate a visual question with polygon shape"""
    
    # Color palette
    colors = [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
        "#FD79A8", "#A29BFE", "#6C5CE7", "#00B894", "#00CEC9"
    ]
    
    # Get shapes for this difficulty
    shapes = get_shapes_for_visual(difficulty)
    
    # Filter recently used
    available_shapes = [s for s in shapes if s["name"] not in st.session_state.recent_polygons]
    
    if len(available_shapes) < 3:
        st.session_state.recent_polygons = []
        available_shapes = shapes
    
    shape = random.choice(available_shapes)
    st.session_state.recent_polygons.append(shape["name"])
    
    # Random parameters
    rotation = random.randint(0, 359)
    scale = random.uniform(0.8, 1.2)
    color = random.choice(colors)
    
    # Generate SVG
    svg_code = generate_polygon_svg(shape["name"], shape["sides"], color, shape["type"], rotation, scale)
    
    # Store question data
    st.session_state.question_data = {
        "shape_name": shape["name"],
        "display_name": shape["display_name"],
        "sides": shape["sides"],
        "svg_code": svg_code,
        "color": color,
        "type": shape["type"]
    }
    
    st.session_state.correct_answer = shape["sides"]
    st.session_state.current_question = f"How many sides does this {shape['display_name']} have?"

def get_shapes_for_visual(difficulty):
    """Get shapes for visual questions based on difficulty"""
    
    if difficulty == 1:
        shapes = [
            {"name": "triangle", "display_name": "triangle", "sides": 3, "type": "regular"},
            {"name": "square", "display_name": "square", "sides": 4, "type": "regular"},
            {"name": "rectangle", "display_name": "rectangle", "sides": 4, "type": "regular"},
            {"name": "pentagon", "display_name": "pentagon", "sides": 5, "type": "regular"},
            {"name": "hexagon", "display_name": "hexagon", "sides": 6, "type": "regular"},
        ]
    elif difficulty == 2:
        shapes = [
            {"name": "triangle_irregular", "display_name": "triangle", "sides": 3, "type": "irregular"},
            {"name": "parallelogram", "display_name": "parallelogram", "sides": 4, "type": "regular"},
            {"name": "rhombus", "display_name": "rhombus", "sides": 4, "type": "regular"},
            {"name": "trapezoid", "display_name": "trapezoid", "sides": 4, "type": "regular"},
            {"name": "heptagon", "display_name": "heptagon", "sides": 7, "type": "regular"},
            {"name": "octagon", "display_name": "octagon", "sides": 8, "type": "regular"},
        ]
    elif difficulty == 3:
        shapes = [
            {"name": "pentagon_irregular", "display_name": "pentagon", "sides": 5, "type": "irregular"},
            {"name": "hexagon_irregular", "display_name": "hexagon", "sides": 6, "type": "irregular"},
            {"name": "nonagon", "display_name": "nonagon", "sides": 9, "type": "regular"},
            {"name": "decagon", "display_name": "decagon", "sides": 10, "type": "regular"},
            {"name": "star_5", "display_name": "star", "sides": 5, "type": "star"},
        ]
    elif difficulty == 4:
        shapes = [
            {"name": "hendecagon", "display_name": "hendecagon", "sides": 11, "type": "regular"},
            {"name": "dodecagon", "display_name": "dodecagon", "sides": 12, "type": "regular"},
            {"name": "star_6", "display_name": "star", "sides": 6, "type": "star"},
            {"name": "star_8", "display_name": "star", "sides": 8, "type": "star"},
            {"name": "concave_pentagon", "display_name": "pentagon", "sides": 5, "type": "complex"},
        ]
    else:
        shapes = [
            {"name": "tridecagon", "display_name": "tridecagon", "sides": 13, "type": "regular"},
            {"name": "pentadecagon", "display_name": "pentadecagon", "sides": 15, "type": "regular"},
            {"name": "icosagon", "display_name": "icosagon", "sides": 20, "type": "regular"},
            {"name": "star_10", "display_name": "star", "sides": 10, "type": "star"},
            {"name": "complex_polygon", "display_name": "polygon", "sides": random.randint(13, 20), "type": "complex"},
        ]
    
    return shapes

def generate_polygon_svg(shape_name, num_sides, color, shape_type, rotation=0, scale=1.0):
    """Generate SVG for different polygon types"""
    
    width = 400
    height = 400
    center_x = width // 2
    center_y = height // 2
    base_radius = 120 * scale
    
    transform = f'transform="rotate({rotation} {center_x} {center_y})"' if rotation != 0 else ''
    
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg_parts.append('<rect width="400" height="400" fill="white"/>')
    
    if shape_type == "star":
        # Star polygon
        outer_points = []
        inner_points = []
        for i in range(num_sides):
            angle = (i * 360/num_sides - 90) * math.pi / 180
            x = center_x + base_radius * math.cos(angle)
            y = center_y + base_radius * math.sin(angle)
            outer_points.append((x, y))
            
            angle = ((i * 360/num_sides) + 180/num_sides - 90) * math.pi / 180
            x = center_x + base_radius * 0.4 * math.cos(angle)
            y = center_y + base_radius * 0.4 * math.sin(angle)
            inner_points.append((x, y))
        
        all_points = []
        for i in range(num_sides):
            all_points.append(outer_points[i])
            all_points.append(inner_points[i])
        
        points_str = " ".join([f"{x},{y}" for x, y in all_points])
        svg_parts.append(f'<polygon points="{points_str}" fill="none" stroke="{color}" stroke-width="4" {transform}/>')
        
        # Highlight outer points
        for x, y in outer_points:
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{color}" {transform}/>')
    
    elif shape_name == "rectangle":
        width_half = base_radius
        height_half = base_radius * 0.6
        points = [(center_x-width_half, center_y-height_half), (center_x+width_half, center_y-height_half),
                 (center_x+width_half, center_y+height_half), (center_x-width_half, center_y+height_half)]
        points_str = " ".join([f"{x},{y}" for x, y in points])
        svg_parts.append(f'<polygon points="{points_str}" fill="none" stroke="{color}" stroke-width="4" {transform}/>')
        for x, y in points:
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" {transform}/>')
    
    elif shape_name == "square":
        half = base_radius * 0.8
        points = [(center_x-half, center_y-half), (center_x+half, center_y-half),
                 (center_x+half, center_y+half), (center_x-half, center_y+half)]
        points_str = " ".join([f"{x},{y}" for x, y in points])
        svg_parts.append(f'<polygon points="{points_str}" fill="none" stroke="{color}" stroke-width="4" {transform}/>')
        for x, y in points:
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" {transform}/>')
    
    elif shape_name == "parallelogram":
        points = [(center_x-base_radius*0.8, center_y+base_radius*0.5), 
                 (center_x-base_radius*0.3, center_y-base_radius*0.5),
                 (center_x+base_radius*0.8, center_y-base_radius*0.5), 
                 (center_x+base_radius*0.3, center_y+base_radius*0.5)]
        points_str = " ".join([f"{x},{y}" for x, y in points])
        svg_parts.append(f'<polygon points="{points_str}" fill="none" stroke="{color}" stroke-width="4" {transform}/>')
        for x, y in points:
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" {transform}/>')
    
    elif shape_name == "rhombus":
        points = [(center_x, center_y-base_radius), (center_x+base_radius*0.7, center_y),
                 (center_x, center_y+base_radius), (center_x-base_radius*0.7, center_y)]
        points_str = " ".join([f"{x},{y}" for x, y in points])
        svg_parts.append(f'<polygon points="{points_str}" fill="none" stroke="{color}" stroke-width="4" {transform}/>')
        for x, y in points:
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" {transform}/>')
    
    elif shape_name == "trapezoid":
        points = [(center_x-base_radius*0.5, center_y-base_radius*0.5), 
                 (center_x+base_radius*0.5, center_y-base_radius*0.5),
                 (center_x+base_radius, center_y+base_radius*0.5), 
                 (center_x-base_radius, center_y+base_radius*0.5)]
        points_str = " ".join([f"{x},{y}" for x, y in points])
        svg_parts.append(f'<polygon points="{points_str}" fill="none" stroke="{color}" stroke-width="4" {transform}/>')
        for x, y in points:
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" {transform}/>')
    
    elif shape_type == "irregular":
        # Irregular polygon
        points = []
        for i in range(num_sides):
            angle = (i * 360/num_sides - 90) * math.pi / 180
            radius_variation = base_radius * (0.7 + random.random() * 0.6)
            x = center_x + radius_variation * math.cos(angle)
            y = center_y + radius_variation * math.sin(angle)
            points.append((x, y))
        
        points_str = " ".join([f"{x},{y}" for x, y in points])
        svg_parts.append(f'<polygon points="{points_str}" fill="none" stroke="{color}" stroke-width="4" {transform}/>')
        for x, y in points:
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" {transform}/>')
    
    else:
        # Regular polygon
        points = []
        for i in range(num_sides):
            angle = (i * 360/num_sides - 90) * math.pi / 180
            x = center_x + base_radius * math.cos(angle)
            y = center_y + base_radius * math.sin(angle)
            points.append((x, y))
        
        points_str = " ".join([f"{x},{y}" for x, y in points])
        svg_parts.append(f'<polygon points="{points_str}" fill="none" stroke="{color}" stroke-width="4" {transform}/>')
        
        # Add vertex dots
        for x, y in points:
            svg_parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{color}" {transform}/>')
        
        # Add numbers for complex shapes
        if num_sides > 10:
            for i, (x, y) in enumerate(points):
                angle = math.atan2(y - center_y, x - center_x)
                text_x = x + 20 * math.cos(angle)
                text_y = y + 20 * math.sin(angle)
                svg_parts.append(f'<text x="{text_x}" y="{text_y}" text-anchor="middle" fill="{color}" font-size="14" font-weight="bold">{i+1}</text>')
    
    svg_parts.append('</svg>')
    return "".join(svg_parts)

def display_question():
    """Display the current question"""
    
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_question}")
    
    # Display visual if it's a visual question
    if data.get("type") != "text":
        st.markdown("")
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.markdown(data["svg_code"], unsafe_allow_html=True)
            
            if data.get("type") == "star":
                st.info("💡 **Hint:** For star shapes, count the number of outer points!")
    
    # Input field
    st.markdown("")
    
    if not st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_input = st.number_input(
                "Enter the number of sides:",
                min_value=3,
                max_value=10000 if st.session_state.sides_difficulty == 5 else 50,
                value=None,
                step=1,
                key="sides_input",
                placeholder="Type a number..."
            )
            
            if st.button("✅ Submit", type="primary", use_container_width=True):
                if user_input is not None:
                    st.session_state.user_answer = int(user_input)
                    st.session_state.answer_submitted = True
                    st.session_state.total_attempted += 1
                    if st.session_state.user_answer == st.session_state.correct_answer:
                        st.session_state.total_correct += 1
                    st.rerun()
                else:
                    st.warning("Please enter a number!")
    
    else:
        # Show result
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.session_state.user_answer == st.session_state.correct_answer:
                st.success(f"✅ Correct! The answer is **{st.session_state.correct_answer} sides**")
            else:
                st.error(f"❌ Your answer: {st.session_state.user_answer} sides")
                st.info(f"✅ Correct answer: **{st.session_state.correct_answer} sides**")
        
        # Show feedback
        show_feedback()
        
        # Next question button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback with reference charts for wrong answers"""
    
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    st.markdown("---")
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Show polygon name
        polygon_names = {
            3: "Triangle", 4: "Quadrilateral", 5: "Pentagon", 6: "Hexagon",
            7: "Heptagon", 8: "Octagon", 9: "Nonagon", 10: "Decagon",
            11: "Hendecagon", 12: "Dodecagon", 13: "Tridecagon", 14: "Tetradecagon",
            15: "Pentadecagon", 16: "Hexadecagon", 17: "Heptadecagon", 18: "Octadecagon",
            19: "Enneadecagon", 20: "Icosagon", 100: "Hectagon", 1000: "Chiliagon", 10000: "Myriagon"
        }
        
        if correct_answer in polygon_names:
            st.markdown(f"### This is a **{polygon_names[correct_answer]}** ({correct_answer} sides)")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.sides_difficulty
            st.session_state.sides_difficulty = min(st.session_state.sides_difficulty + 1, 5)
            st.session_state.consecutive_correct = 0
            
            if st.session_state.sides_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.sides_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite right.**")
        
        # Show specific feedback
        if user_answer == correct_answer - 1:
            st.warning("💡 You might have missed one side. Count again carefully!")
        elif user_answer == correct_answer + 1:
            st.warning("💡 You might have counted one side twice.")
        elif data.get("type") == "star" and user_answer == correct_answer * 2:
            st.warning("💡 For stars, count only the outer points, not all vertices!")
        
        # Show reference chart for wrong answers
        st.markdown("### 📚 Reference Chart")
        st.markdown("Here's a helpful reference to study polygon names and their sides:")
        
        # Display the reference chart
        reference_svg = get_polygon_reference_svg()
        st.markdown(reference_svg, unsafe_allow_html=True)
        
        # Show special quadrilaterals reference if it was a quadrilateral
        if correct_answer == 4 or (data.get("polygon_name") and "quad" in data.get("polygon_name", "").lower()):
            st.markdown("### Special Quadrilaterals")
            st.info("Remember: All these shapes have exactly **4 sides**!")
            special_quads_svg = get_special_quadrilaterals_reference()
            st.markdown(special_quads_svg, unsafe_allow_html=True)
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.sides_difficulty
            st.session_state.sides_difficulty = max(st.session_state.sides_difficulty - 1, 1)
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.sides_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.sides_difficulty}**")
    
    # Show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation"""
    
    data = st.session_state.question_data
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **Learn More**", expanded=True):
        if data.get("type") == "text":
            # Text question explanation
            st.markdown(f"### {data.get('polygon_name', 'This polygon').capitalize()} has **{correct_answer} sides**")
            
            # Etymology and memory tips
            etymology = {
                "triangle": "**Tri** = Three (Latin: tres)",
                "quadrilateral": "**Quad** = Four (Latin: quattuor)",
                "pentagon": "**Penta** = Five (Greek: pente)",
                "hexagon": "**Hexa** = Six (Greek: hex)",
                "heptagon": "**Hepta** = Seven (Greek: hepta)",
                "octagon": "**Octa** = Eight (Greek: okto)",
                "nonagon": "**Nona** = Nine (Latin: nonus)",
                "decagon": "**Deca** = Ten (Greek: deka)",
                "hendecagon": "**Hendeca** = Eleven (Greek: hendeka)",
                "dodecagon": "**Dodeca** = Twelve (Greek: dodeka)"
            }
            
            if data.get("polygon_name") in etymology:
                st.markdown("### Word Origin:")
                st.markdown(etymology[data.get("polygon_name")])
            
            # Real-world examples
            examples = {
                3: "🔺 Triangles: Traffic yield signs, pyramids, pizza slices",
                4: "🔲 Quadrilaterals: Windows, books, screens, tiles",
                5: "⭐ Pentagons: The Pentagon building, home plate in baseball",
                6: "🔶 Hexagons: Honeycomb cells, nuts and bolts, floor tiles",
                7: "🔷 Heptagons: Some coins (like UK 50p and 20p)",
                8: "🛑 Octagons: Stop signs, umbrellas, gazebos",
                10: "🔟 Decagons: Some coins, decorative windows"
            }
            
            if correct_answer in examples:
                st.markdown("### Real-World Examples:")
                st.markdown(examples[correct_answer])
        
        else:
            # Visual question explanation
            st.markdown(f"### Counting the Sides:")
            st.markdown(f"This shape has **{correct_answer} sides**")
            
            if data.get("type") == "star":
                st.markdown("""
                ### Star Polygons:
                - Count only the **outer points** 
                - Each outer point forms one side
                - Don't count the inner crossing points
                """)
        
        # Fun facts
        if correct_answer >= 13:
            st.markdown("### 🎓 Advanced Polygon Fact:")
            if correct_answer == 100:
                st.markdown("A **hectagon** has 100 sides! It looks almost like a circle.")
            elif correct_answer == 1000:
                st.markdown("A **chiliagon** has 1,000 sides! It's practically indistinguishable from a circle.")
            elif correct_answer == 10000:
                st.markdown("A **myriagon** has 10,000 sides! The word comes from the Greek 'myrias' meaning countless.")
            else:
                st.markdown(f"Polygons with {correct_answer} or more sides are rarely seen in everyday life and appear very circular!")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_answer = ""
    st.session_state.question_type = None