import streamlit as st
import random
import math

def run():
    """
    Main function to run the Regular and Irregular Polygons practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/regular_and_irregular_polygons.py
    """
    
    # Initialize session state
    if "regular_difficulty" not in st.session_state:
        st.session_state.regular_difficulty = 1
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.recent_shapes = []
        st.session_state.shape_type_count = {"regular": 0, "irregular": 0}
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_answer = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("🔷 Regular and Irregular Polygons")
    st.markdown("*Identify whether polygons are regular or irregular*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.regular_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic shapes with clear indicators",
            2: "Mixed shapes with measurements",
            3: "Complex shapes with angles",
            4: "Advanced with subtle differences",
            5: "Expert level - all indicators"
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
        ### Regular vs Irregular Polygons
        
        **Regular Polygon:**
        - ✅ ALL sides are equal length
        - ✅ ALL angles are equal
        - Both conditions must be true!
        
        **Irregular Polygon:**
        - ❌ Sides have different lengths, OR
        - ❌ Angles have different measures, OR
        - ❌ Both are different
        
        ### Visual Indicators:
        
        **Equal Sides:**
        - Single tick mark (|) = these sides are equal to each other
        - Double tick marks (||) = these sides are equal to each other (but different from single tick)
        - Numbers = actual measurements in units
        
        **Equal Angles:**
        - Same angle symbol (single arc) = these angles are equal
        - Right angle symbol (square corner) = 90°
        - Numbers with ° = actual angle measurements
        
        ### Common Examples:
        
        **Regular Polygons:**
        - Equilateral triangle (all sides equal, all angles 60°)
        - Square (all sides equal, all angles 90°)
        - Regular pentagon (all sides equal, all angles 108°)
        - Regular hexagon (all sides equal, all angles 120°)
        
        **Irregular Polygons:**
        - Scalene triangle (all sides different)
        - Rectangle (opposite sides equal, but not all four)
        - Rhombus (all sides equal, but angles not all equal)
        - Any polygon with different side lengths or angles
        
        ### Quick Check Method:
        1. Look at the side indicators - are they ALL the same?
        2. Look at the angle indicators - are they ALL the same?
        3. If YES to both → Regular
        4. If NO to either → Irregular
        
        ### Remember:
        - A shape needs BOTH equal sides AND equal angles to be regular
        - Even if all sides are equal, different angles make it irregular
        - Even if all angles are equal, different sides make it irregular
        """)

def generate_shape_data(difficulty):
    """Generate polygon shapes with appropriate indicators for the difficulty level"""
    
    shapes_data = []
    
    if difficulty == 1:
        # Basic shapes with clear visual indicators
        shapes_data = [
            # Regular shapes
            {
                "type": "triangle",
                "sides": 3,
                "is_regular": True,
                "side_lengths": [100, 100, 100],
                "angles": [60, 60, 60],
                "show_measurements": False,
                "show_tick_marks": True,
                "tick_pattern": [1, 1, 1],  # All same tick marks
                "description": "equilateral triangle"
            },
            {
                "type": "square",
                "sides": 4,
                "is_regular": True,
                "side_lengths": [80, 80, 80, 80],
                "angles": [90, 90, 90, 90],
                "show_measurements": False,
                "show_tick_marks": True,
                "show_right_angles": True,
                "tick_pattern": [1, 1, 1, 1],
                "description": "square"
            },
            {
                "type": "pentagon",
                "sides": 5,
                "is_regular": True,
                "side_lengths": [70, 70, 70, 70, 70],
                "angles": [108, 108, 108, 108, 108],
                "show_measurements": False,
                "show_tick_marks": True,
                "tick_pattern": [1, 1, 1, 1, 1],
                "description": "regular pentagon"
            },
            # Irregular shapes
            {
                "type": "triangle",
                "sides": 3,
                "is_regular": False,
                "side_lengths": [80, 100, 120],
                "angles": [45, 65, 70],
                "show_measurements": False,
                "show_tick_marks": True,
                "tick_pattern": [1, 2, 3],  # All different tick marks
                "description": "scalene triangle"
            },
            {
                "type": "rectangle",
                "sides": 4,
                "is_regular": False,
                "side_lengths": [100, 60, 100, 60],
                "angles": [90, 90, 90, 90],
                "show_measurements": False,
                "show_tick_marks": True,
                "show_right_angles": True,
                "tick_pattern": [1, 2, 1, 2],
                "description": "rectangle"
            },
            {
                "type": "quadrilateral",
                "sides": 4,
                "is_regular": False,
                "side_lengths": [70, 85, 90, 95],
                "angles": [85, 95, 100, 80],
                "show_measurements": False,
                "show_tick_marks": True,
                "tick_pattern": [1, 2, 3, 4],
                "description": "irregular quadrilateral"
            }
        ]
    
    elif difficulty == 2:
        # Mixed shapes with side measurements
        shapes_data = [
            # Regular shapes
            {
                "type": "triangle",
                "sides": 3,
                "is_regular": True,
                "side_lengths": [150, 150, 150],
                "angles": [60, 60, 60],
                "show_measurements": True,
                "show_tick_marks": False,
                "description": "equilateral triangle"
            },
            {
                "type": "hexagon",
                "sides": 6,
                "is_regular": True,
                "side_lengths": [50, 50, 50, 50, 50, 50],
                "angles": [120, 120, 120, 120, 120, 120],
                "show_measurements": True,
                "show_tick_marks": False,
                "description": "regular hexagon"
            },
            {
                "type": "square",
                "sides": 4,
                "is_regular": True,
                "side_lengths": [201, 201, 201, 201],
                "angles": [90, 90, 90, 90],
                "show_measurements": True,
                "show_right_angles": True,
                "description": "square"
            },
            # Irregular shapes
            {
                "type": "triangle",
                "sides": 3,
                "is_regular": False,
                "side_lengths": [120, 150, 180],
                "angles": [40, 60, 80],
                "show_measurements": True,
                "description": "scalene triangle"
            },
            {
                "type": "pentagon",
                "sides": 5,
                "is_regular": False,
                "side_lengths": [80, 80, 90, 85, 95],
                "angles": [100, 110, 108, 112, 110],
                "show_measurements": True,
                "description": "irregular pentagon"
            },
            {
                "type": "rhombus",
                "sides": 4,
                "is_regular": False,
                "side_lengths": [75, 75, 75, 75],
                "angles": [70, 110, 70, 110],
                "show_measurements": True,
                "description": "rhombus"
            }
        ]
    
    elif difficulty == 3:
        # Complex shapes with angle measurements
        shapes_data = [
            # Regular shapes
            {
                "type": "octagon",
                "sides": 8,
                "is_regular": True,
                "side_lengths": [40, 40, 40, 40, 40, 40, 40, 40],
                "angles": [135, 135, 135, 135, 135, 135, 135, 135],
                "show_measurements": False,
                "show_angles": True,
                "show_tick_marks": True,
                "tick_pattern": [1, 1, 1, 1, 1, 1, 1, 1],
                "description": "regular octagon"
            },
            {
                "type": "heptagon",
                "sides": 7,
                "is_regular": True,
                "side_lengths": [45, 45, 45, 45, 45, 45, 45],
                "angles": [128.57, 128.57, 128.57, 128.57, 128.57, 128.57, 128.57],
                "show_angles": True,
                "angle_display": ["128.6°", "128.6°", "128.6°", "128.6°", "128.6°", "128.6°", "128.6°"],
                "description": "regular heptagon"
            },
            # Irregular shapes
            {
                "type": "pentagon",
                "sides": 5,
                "is_regular": False,
                "side_lengths": [70, 80, 75, 85, 90],
                "angles": [93, 133, 83, 149, 82],
                "show_angles": True,
                "description": "irregular pentagon"
            },
            {
                "type": "hexagon",
                "sides": 6,
                "is_regular": False,
                "side_lengths": [60, 65, 70, 65, 60, 70],
                "angles": [110, 125, 130, 115, 120, 120],
                "show_angles": True,
                "description": "irregular hexagon"
            },
            {
                "type": "quadrilateral",
                "sides": 4,
                "is_regular": False,
                "side_lengths": [80, 90, 85, 95],
                "angles": [99, 90, 117, 54],
                "show_angles": True,
                "description": "irregular quadrilateral"
            }
        ]
    
    elif difficulty == 4:
        # Advanced with subtle differences
        shapes_data = [
            # Regular shapes
            {
                "type": "nonagon",
                "sides": 9,
                "is_regular": True,
                "side_lengths": [35, 35, 35, 35, 35, 35, 35, 35, 35],
                "angles": [140, 140, 140, 140, 140, 140, 140, 140, 140],
                "show_measurements": True,
                "show_angles": True,
                "description": "regular nonagon"
            },
            {
                "type": "decagon",
                "sides": 10,
                "is_regular": True,
                "side_lengths": [30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
                "angles": [144, 144, 144, 144, 144, 144, 144, 144, 144, 144],
                "show_tick_marks": True,
                "tick_pattern": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                "show_angles": True,
                "description": "regular decagon"
            },
            # Irregular shapes (subtle differences)
            {
                "type": "pentagon",
                "sides": 5,
                "is_regular": False,
                "side_lengths": [100, 100, 100, 100, 102],  # Almost regular
                "angles": [108, 108, 108, 108, 108],
                "show_measurements": True,
                "description": "almost regular pentagon"
            },
            {
                "type": "hexagon",
                "sides": 6,
                "is_regular": False,
                "side_lengths": [60, 60, 60, 60, 60, 60],
                "angles": [120, 118, 122, 120, 120, 120],  # Almost regular
                "show_angles": True,
                "description": "almost regular hexagon"
            },
            {
                "type": "octagon",
                "sides": 8,
                "is_regular": False,
                "side_lengths": [40, 41, 40, 41, 40, 41, 40, 41],
                "angles": [135, 135, 135, 135, 135, 135, 135, 135],
                "show_measurements": True,
                "show_angles": True,
                "description": "irregular octagon"
            }
        ]
    
    else:  # difficulty 5
        # Expert level - all types with various indicators
        shapes_data = [
            # Regular shapes
            {
                "type": "triangle",
                "sides": 3,
                "is_regular": True,
                "side_lengths": [200, 200, 200],
                "angles": [60, 60, 60],
                "show_measurements": True,
                "show_angles": True,
                "show_tick_marks": True,
                "tick_pattern": [1, 1, 1],
                "description": "equilateral triangle"
            },
            {
                "type": "dodecagon",
                "sides": 12,
                "is_regular": True,
                "side_lengths": [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25],
                "angles": [150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150],
                "show_measurements": True,
                "show_angles": True,
                "description": "regular dodecagon"
            },
            # Irregular shapes (tricky cases)
            {
                "type": "square_rotated",
                "sides": 4,
                "is_regular": True,  # Still regular even when rotated
                "side_lengths": [100, 100, 100, 100],
                "angles": [90, 90, 90, 90],
                "show_measurements": True,
                "show_right_angles": True,
                "rotation": 45,
                "description": "rotated square"
            },
            {
                "type": "equilateral_triangle",
                "sides": 3,
                "is_regular": False,  # Trick question - shown with unequal measurements due to rounding
                "side_lengths": [99.9, 100.1, 100],
                "angles": [60.1, 59.9, 60],
                "show_measurements": True,
                "show_angles": True,
                "description": "nearly equilateral triangle"
            },
            {
                "type": "parallelogram",
                "sides": 4,
                "is_regular": False,
                "side_lengths": [120, 80, 120, 80],
                "angles": [70, 110, 70, 110],
                "show_measurements": True,
                "show_angles": True,
                "show_tick_marks": True,
                "tick_pattern": [1, 2, 1, 2],
                "description": "parallelogram"
            }
        ]
    
    return shapes_data

def generate_new_question():
    """Generate a new regular/irregular polygon question"""
    
    difficulty = st.session_state.regular_difficulty
    
    # Keep track of recent shapes
    if len(st.session_state.recent_shapes) > 8:
        st.session_state.recent_shapes = st.session_state.recent_shapes[-4:]
    
    # Get shapes for this difficulty
    all_shapes = generate_shape_data(difficulty)
    
    # Balance regular vs irregular
    regular_count = st.session_state.shape_type_count.get("regular", 0)
    irregular_count = st.session_state.shape_type_count.get("irregular", 0)
    
    # Filter by type to balance
    if regular_count > irregular_count + 2:
        # Prefer irregular
        preferred_shapes = [s for s in all_shapes if not s["is_regular"]]
        if not preferred_shapes:
            preferred_shapes = all_shapes
    elif irregular_count > regular_count + 2:
        # Prefer regular
        preferred_shapes = [s for s in all_shapes if s["is_regular"]]
        if not preferred_shapes:
            preferred_shapes = all_shapes
    else:
        preferred_shapes = all_shapes
    
    # Filter out recent shapes
    available_shapes = [s for s in preferred_shapes if str(s) not in [str(r) for r in st.session_state.recent_shapes]]
    
    if not available_shapes:
        available_shapes = preferred_shapes
        st.session_state.recent_shapes = []
    
    # Select a shape
    shape = random.choice(available_shapes)
    
    # Track usage
    st.session_state.recent_shapes.append(shape)
    shape_type = "regular" if shape["is_regular"] else "irregular"
    st.session_state.shape_type_count[shape_type] = st.session_state.shape_type_count.get(shape_type, 0) + 1
    
    # Add rotation for variety
    if shape.get("rotation") is None:
        shape["rotation"] = random.randint(0, 359)
    
    # Generate SVG
    svg_code = generate_polygon_svg_with_indicators(shape)
    
    # Store question data
    st.session_state.question_data = {
        "shape": shape,
        "svg_code": svg_code,
        "is_regular": shape["is_regular"]
    }
    
    st.session_state.correct_answer = "yes" if shape["is_regular"] else "no"
    st.session_state.current_question = "Is this shape a regular polygon?"

def generate_polygon_svg_with_indicators(shape_data):
    """Generate SVG with visual indicators for regular/irregular identification"""
    
    width = 500
    height = 500
    center_x = width // 2
    center_y = height // 2
    
    # Random color selection
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FD79A8", "#6C5CE7", "#00B894"]
    color = random.choice(colors)
    
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg_parts.append('<rect width="500" height="500" fill="white"/>')
    
    # Get shape vertices
    num_sides = shape_data["sides"]
    rotation = shape_data.get("rotation", 0)
    
    # Calculate vertex positions
    vertices = []
    
    if shape_data["type"] == "square" or shape_data["type"] == "square_rotated":
        # Special case for square
        half_size = 120
        base_vertices = [
            (-half_size, -half_size),
            (half_size, -half_size),
            (half_size, half_size),
            (-half_size, half_size)
        ]
        for x, y in base_vertices:
            # Apply rotation
            angle_rad = rotation * math.pi / 180
            new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            vertices.append((center_x + new_x, center_y + new_y))
    
    elif shape_data["type"] == "rectangle":
        # Special case for rectangle
        width_half = 150
        height_half = 90
        base_vertices = [
            (-width_half, -height_half),
            (width_half, -height_half),
            (width_half, height_half),
            (-width_half, height_half)
        ]
        for x, y in base_vertices:
            angle_rad = rotation * math.pi / 180
            new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            vertices.append((center_x + new_x, center_y + new_y))
    
    elif shape_data["type"] == "rhombus":
        # Special case for rhombus
        vertices = [
            (center_x, center_y - 120),
            (center_x + 100, center_y),
            (center_x, center_y + 120),
            (center_x - 100, center_y)
        ]
        # Apply rotation
        rotated_vertices = []
        for x, y in vertices:
            dx = x - center_x
            dy = y - center_y
            angle_rad = rotation * math.pi / 180
            new_x = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            new_y = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
            rotated_vertices.append((center_x + new_x, center_y + new_y))
        vertices = rotated_vertices
    
    elif shape_data["type"] == "parallelogram":
        # Special case for parallelogram
        vertices = [
            (center_x - 120, center_y + 80),
            (center_x - 40, center_y - 80),
            (center_x + 120, center_y - 80),
            (center_x + 40, center_y + 80)
        ]
        # Apply rotation
        rotated_vertices = []
        for x, y in vertices:
            dx = x - center_x
            dy = y - center_y
            angle_rad = rotation * math.pi / 180
            new_x = dx * math.cos(angle_rad) - dy * math.sin(angle_rad)
            new_y = dx * math.sin(angle_rad) + dy * math.cos(angle_rad)
            rotated_vertices.append((center_x + new_x, center_y + new_y))
        vertices = rotated_vertices
    
    else:
        # Regular polygon or general case
        if shape_data["is_regular"]:
            # Regular polygon - equal angles
            for i in range(num_sides):
                angle = (i * 360/num_sides - 90 + rotation) * math.pi / 180
                radius = 150 if num_sides <= 6 else 120
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                vertices.append((x, y))
        else:
            # Irregular polygon - vary the radius and/or angle
            for i in range(num_sides):
                base_angle = (i * 360/num_sides - 90 + rotation) * math.pi / 180
                
                # Add some variation for irregular shapes
                if i % 2 == 0:
                    radius_variation = 150 + random.randint(-30, 20)
                else:
                    radius_variation = 150 + random.randint(-20, 30)
                
                # Add angle variation for some vertices
                angle_variation = 0
                if not shape_data.get("almost_regular"):
                    angle_variation = random.uniform(-0.1, 0.1)
                
                angle = base_angle + angle_variation
                x = center_x + radius_variation * math.cos(angle)
                y = center_y + radius_variation * math.sin(angle)
                vertices.append((x, y))
    
    # Draw the polygon
    points_str = " ".join([f"{x},{y}" for x, y in vertices])
    svg_parts.append(f'<polygon points="{points_str}" fill="none" stroke="{color}" stroke-width="3"/>')
    
    # Add visual indicators based on shape_data settings
    
    # 1. Tick marks for equal sides
    if shape_data.get("show_tick_marks"):
        tick_pattern = shape_data.get("tick_pattern", [])
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Calculate perpendicular direction for tick marks
            dx = x2 - x1
            dy = y2 - y1
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                perp_x = -dy / length * 10
                perp_y = dx / length * 10
                
                # Draw tick marks based on pattern
                if i < len(tick_pattern):
                    num_ticks = tick_pattern[i]
                    for t in range(num_ticks):
                        offset = (t - (num_ticks-1)/2) * 5
                        tick_x = mid_x + offset * dx / length
                        tick_y = mid_y + offset * dy / length
                        svg_parts.append(f'<line x1="{tick_x - perp_x}" y1="{tick_y - perp_y}" '
                                       f'x2="{tick_x + perp_x}" y2="{tick_y + perp_y}" '
                                       f'stroke="{color}" stroke-width="2"/>')
    
    # 2. Side length measurements
    if shape_data.get("show_measurements"):
        side_lengths = shape_data.get("side_lengths", [])
        for i in range(len(vertices)):
            if i < len(side_lengths):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i + 1) % len(vertices)]
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                
                # Offset text outside the shape
                dx = mid_x - center_x
                dy = mid_y - center_y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    offset_x = mid_x + dx/dist * 25
                    offset_y = mid_y + dy/dist * 25
                else:
                    offset_x, offset_y = mid_x, mid_y
                
                svg_parts.append(f'<text x="{offset_x}" y="{offset_y}" text-anchor="middle" '
                               f'fill="black" font-size="16" font-weight="bold">{side_lengths[i]}</text>')
    
    # 3. Angle measurements
    if shape_data.get("show_angles"):
        angles = shape_data.get("angles", [])
        angle_display = shape_data.get("angle_display", [f"{a}°" for a in angles])
        
        for i in range(len(vertices)):
            if i < len(angles):
                x = vertices[i][0]
                y = vertices[i][1]
                
                # Calculate angle arc position
                prev_vertex = vertices[i - 1]
                next_vertex = vertices[(i + 1) % len(vertices)]
                
                # Direction vectors
                dx1 = prev_vertex[0] - x
                dy1 = prev_vertex[1] - y
                dx2 = next_vertex[0] - x
                dy2 = next_vertex[1] - y
                
                # Normalize and find midpoint direction
                len1 = math.sqrt(dx1*dx1 + dy1*dy1)
                len2 = math.sqrt(dx2*dx2 + dy2*dy2)
                
                if len1 > 0 and len2 > 0:
                    dx1, dy1 = dx1/len1, dy1/len1
                    dx2, dy2 = dx2/len2, dy2/len2
                    
                    # Angle bisector direction (inward)
                    bis_x = (dx1 + dx2) / 2
                    bis_y = (dy1 + dy2) / 2
                    bis_len = math.sqrt(bis_x*bis_x + bis_y*bis_y)
                    
                    if bis_len > 0:
                        bis_x, bis_y = bis_x/bis_len, bis_y/bis_len
                        
                        # Place angle text
                        text_x = x + bis_x * 30
                        text_y = y + bis_y * 30
                        
                        # Draw angle arc
                        arc_radius = 20
                        svg_parts.append(f'<path d="M {x + dx1*arc_radius} {y + dy1*arc_radius} '
                                       f'A {arc_radius} {arc_radius} 0 0 1 '
                                       f'{x + dx2*arc_radius} {y + dy2*arc_radius}" '
                                       f'fill="none" stroke="{color}" stroke-width="1.5"/>')
                        
                        # Add angle text
                        svg_parts.append(f'<text x="{text_x}" y="{text_y}" text-anchor="middle" '
                                       f'fill="black" font-size="14" font-weight="bold">'
                                       f'{angle_display[i]}</text>')
    
    # 4. Right angle indicators
    if shape_data.get("show_right_angles"):
        for i in range(len(vertices)):
            angle = shape_data.get("angles", [])[i] if i < len(shape_data.get("angles", [])) else 0
            if abs(angle - 90) < 0.1:  # It's a right angle
                x = vertices[i][0]
                y = vertices[i][1]
                
                # Draw right angle square
                prev_vertex = vertices[i - 1]
                next_vertex = vertices[(i + 1) % len(vertices)]
                
                dx1 = prev_vertex[0] - x
                dy1 = prev_vertex[1] - y
                dx2 = next_vertex[0] - x
                dy2 = next_vertex[1] - y
                
                len1 = math.sqrt(dx1*dx1 + dy1*dy1)
                len2 = math.sqrt(dx2*dx2 + dy2*dy2)
                
                if len1 > 0 and len2 > 0:
                    dx1, dy1 = dx1/len1 * 15, dy1/len1 * 15
                    dx2, dy2 = dx2/len2 * 15, dy2/len2 * 15
                    
                    svg_parts.append(f'<path d="M {x + dx1} {y + dy1} '
                                   f'L {x + dx1 + dx2} {y + dy1 + dy2} '
                                   f'L {x + dx2} {y + dy2}" '
                                   f'fill="none" stroke="{color}" stroke-width="2"/>')
    
    svg_parts.append('</svg>')
    return "".join(svg_parts)

def display_question():
    """Display the current question with the polygon"""
    
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_question}")
    
    # Display the shape
    st.markdown("")
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(data["svg_code"], unsafe_allow_html=True)
        
        # Add hint based on difficulty
        if st.session_state.regular_difficulty >= 4:
            st.info("💡 **Hint:** Look carefully at ALL measurements. Even small differences matter!")
    
    # Answer options
    st.markdown("")
    
    if not st.session_state.answer_submitted:
        cols = st.columns(2)
        
        options = ["yes", "no"]
        for i, option in enumerate(options):
            with cols[i]:
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
        st.markdown("")
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
                    st.success(f"✓ {option}")
                elif option == st.session_state.selected_answer and option != st.session_state.correct_answer:
                    st.error(f"✗ {option}")
                else:
                    st.button(option, disabled=True, use_container_width=True)
        
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
    """Display feedback with detailed explanation"""
    
    user_answer = st.session_state.selected_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    shape = data["shape"]
    
    st.markdown("---")
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        if shape["is_regular"]:
            st.markdown(f"### ✅ This is a **REGULAR {shape['description']}**")
            st.markdown("All sides are equal AND all angles are equal!")
        else:
            st.markdown(f"### ✅ This is an **IRREGULAR {shape['description']}**")
            if shape.get("almost_regular"):
                st.markdown("Good eye! The differences were subtle but important.")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.regular_difficulty
            st.session_state.regular_difficulty = min(st.session_state.regular_difficulty + 1, 5)
            st.session_state.consecutive_correct = 0
            
            if st.session_state.regular_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.regular_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        if shape["is_regular"]:
            st.error(f"This IS a regular {shape['description']}.")
        else:
            st.error(f"This is NOT a regular polygon - it's an irregular {shape['description']}.")
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.regular_difficulty
            st.session_state.regular_difficulty = max(st.session_state.regular_difficulty - 1, 1)
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.regular_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.regular_difficulty}**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation about why the shape is regular or irregular"""
    
    data = st.session_state.question_data
    shape = data["shape"]
    
    with st.expander("📖 **Understanding the Answer**", expanded=True):
        
        if shape["is_regular"]:
            st.markdown("### Why this is a REGULAR polygon:")
            st.markdown("""
            ✅ **All sides are equal**
            ✅ **All angles are equal**
            
            Both conditions are met, making this a regular polygon!
            """)
            
            # Show the measurements
            if shape.get("side_lengths"):
                st.markdown(f"**Sides:** All {shape['side_lengths'][0]} units")
            if shape.get("angles"):
                st.markdown(f"**Angles:** All {shape['angles'][0]}°")
            
            # Special notes
            if shape["sides"] == 3:
                st.info("📐 **Note:** A regular triangle is called an equilateral triangle.")
            elif shape["sides"] == 4:
                st.info("📐 **Note:** A regular quadrilateral is a square.")
            
        else:
            st.markdown("### Why this is an IRREGULAR polygon:")
            
            # Determine what makes it irregular
            sides_equal = len(set(shape.get("side_lengths", []))) == 1
            angles_equal = len(set(shape.get("angles", []))) == 1
            
            if not sides_equal and not angles_equal:
                st.markdown("""
                ❌ **Sides are NOT all equal**
                ❌ **Angles are NOT all equal**
                
                Both sides and angles vary, making this irregular.
                """)
            elif not sides_equal:
                st.markdown("""
                ❌ **Sides are NOT all equal**
                ✅ Angles might be equal
                
                Different side lengths make this irregular.
                """)
            elif not angles_equal:
                st.markdown("""
                ✅ Sides might be equal
                ❌ **Angles are NOT all equal**
                
                Different angles make this irregular.
                """)
            
            # Show the actual measurements
            if shape.get("side_lengths"):
                sides_str = ", ".join([str(s) for s in shape["side_lengths"]])
                st.markdown(f"**Sides:** {sides_str} (not all equal)")
            if shape.get("angles"):
                angles_str = ", ".join([f"{a}°" for a in shape["angles"]])
                st.markdown(f"**Angles:** {angles_str} (not all equal)")
            
            # Special cases
            if shape["type"] == "rectangle":
                st.info("📐 **Note:** A rectangle has equal angles (all 90°) but not all sides are equal - only opposite sides. This makes it irregular!")
            elif shape["type"] == "rhombus":
                st.info("📐 **Note:** A rhombus has all sides equal but angles are not all equal - only opposite angles. This makes it irregular!")
            elif shape["type"] == "parallelogram":
                st.info("📐 **Note:** A parallelogram has opposite sides equal and opposite angles equal, but not ALL sides and angles are equal.")
            
        # Visual indicator guide
        st.markdown("### 📊 Visual Indicators Guide:")
        st.markdown("""
        **Tick Marks:**
        - | = Single tick: these sides are equal to each other
        - || = Double tick: these sides are equal (but different from single tick sides)
        - ||| = Triple tick: these sides are equal (but different from others)
        
        **Angle Marks:**
        - Arc = angle measurement shown
        - Square corner = 90° right angle
        - Same arc pattern = equal angles
        
        **Remember:** A polygon needs BOTH equal sides AND equal angles to be regular!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None