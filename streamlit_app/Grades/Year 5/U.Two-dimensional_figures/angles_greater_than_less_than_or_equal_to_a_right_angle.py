import streamlit as st
import random
import math

def run():
    """
    Main function to run the Angles comparison with right angle practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/angles_greater_less_equal_right.py
    """
    
    # Initialize session state
    if "angle_difficulty" not in st.session_state:
        st.session_state.angle_difficulty = 1
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.recent_angles = []
        st.session_state.angle_type_count = {"acute": 0, "right": 0, "obtuse": 0}
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_answer = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("📐 Angles: Greater Than, Equal To, or Less Than a Right Angle")
    st.markdown("*Compare angles to a right angle (90°)*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.angle_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Clear angles (obvious differences)",
            2: "Standard angles (moderate)",
            3: "Challenging angles (close to 90°)",
            4: "Various orientations",
            5: "Expert (includes straight & reflex)"
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
        ### Understanding Angles and Right Angles
        
        **A right angle = exactly 90 degrees (90°)**
        - Forms a perfect "L" shape
        - Often marked with a small square □ at the vertex
        - Found in squares, rectangles, and perpendicular lines
        
        ### Types of Angles:
        
        **Less than a right angle (ACUTE):**
        - Measures between 0° and 90°
        - Looks "sharp" or "narrow"
        - The rays are closer together
        - Examples: 30°, 45°, 60°, 89°
        
        **Equal to a right angle (RIGHT):**
        - Measures exactly 90°
        - Forms a perfect corner
        - Like the corner of a book or paper
        - Marked with a small square □
        
        **Greater than a right angle (OBTUSE):**
        - Measures between 90° and 180°
        - Looks "wide" or "open"
        - The rays are farther apart
        - Examples: 91°, 120°, 135°, 179°
        
        ### Visual Comparison Tips:
        
        1. **Imagine a square corner** - that's your 90° reference
        2. **Look at the opening** between the two rays:
           - Narrow opening → Less than 90° (acute)
           - Perfect L-shape → Exactly 90° (right)
           - Wide opening → Greater than 90° (obtuse)
        
        3. **Use the "corner test":**
           - Would a book corner fit perfectly? → Right angle
           - Too narrow for a book corner? → Acute
           - Too wide for a book corner? → Obtuse
        
        ### Special Cases:
        - **Straight angle:** Exactly 180° (a straight line)
        - **Reflex angle:** Greater than 180° (advanced)
        
        ### Remember:
        - The orientation doesn't matter - an angle stays the same when rotated
        - Focus on the opening between the rays, not their length
        - Right angles are marked with a small square □
        """)

def get_angle_reference_chart():
    """Generate a comprehensive reference chart of angle types"""
    
    width = 800
    height = 500
    
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg_parts.append('<rect width="800" height="500" fill="white" stroke="#ddd" stroke-width="2"/>')
    svg_parts.append('<text x="400" y="30" text-anchor="middle" font-size="22" font-weight="bold" fill="#333">Angle Types Reference Chart</text>')
    
    # Define angle examples
    angles = [
        # Acute angles
        {"type": "acute", "degrees": 30, "name": "30° Acute", "pos": (120, 150)},
        {"type": "acute", "degrees": 45, "name": "45° Acute", "pos": (280, 150)},
        {"type": "acute", "degrees": 60, "name": "60° Acute", "pos": (440, 150)},
        {"type": "acute", "degrees": 75, "name": "75° Acute", "pos": (600, 150)},
        
        # Right angle
        {"type": "right", "degrees": 90, "name": "90° Right", "pos": (120, 320)},
        
        # Obtuse angles
        {"type": "obtuse", "degrees": 105, "name": "105° Obtuse", "pos": (280, 320)},
        {"type": "obtuse", "degrees": 120, "name": "120° Obtuse", "pos": (440, 320)},
        {"type": "obtuse", "degrees": 135, "name": "135° Obtuse", "pos": (600, 320)},
        {"type": "obtuse", "degrees": 150, "name": "150° Obtuse", "pos": (720, 320)},
    ]
    
    for angle_data in angles:
        cx, cy = angle_data["pos"]
        degrees = angle_data["degrees"]
        ray_length = 60
        
        # Determine color based on type
        if angle_data["type"] == "acute":
            color = "#4CAF50"  # Green for acute
            category = "< 90°"
        elif angle_data["type"] == "right":
            color = "#2196F3"  # Blue for right
            category = "= 90°"
        else:  # obtuse
            color = "#FF9800"  # Orange for obtuse
            category = "> 90°"
        
        # Draw the angle
        # First ray (horizontal)
        svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + ray_length}" y2="{cy}" '
                        f'stroke="{color}" stroke-width="3"/>')
        
        # Add arrow to first ray
        svg_parts.append(f'<polygon points="{cx + ray_length - 8},{cy - 4} {cx + ray_length},{cy} '
                        f'{cx + ray_length - 8},{cy + 4}" fill="{color}"/>')
        
        # Second ray at the specified angle
        angle_rad = math.radians(degrees)
        x2 = cx + ray_length * math.cos(angle_rad)
        y2 = cy - ray_length * math.sin(angle_rad)  # Negative because SVG y increases downward
        
        svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x2}" y2="{y2}" '
                        f'stroke="{color}" stroke-width="3"/>')
        
        # Add arrow to second ray
        dx = x2 - cx
        dy = y2 - cy
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx, dy = dx/length, dy/length
            arrow_x = x2 - 8*dx
            arrow_y = y2 - 8*dy
            perp_x, perp_y = -dy*4, dx*4
            svg_parts.append(f'<polygon points="{arrow_x + perp_x},{arrow_y + perp_y} {x2},{y2} '
                            f'{arrow_x - perp_x},{arrow_y - perp_y}" fill="{color}"/>')
        
        # Draw angle arc
        arc_radius = 20
        if degrees == 90:
            # Draw right angle square
            square_size = 15
            svg_parts.append(f'<path d="M {cx + square_size} {cy} L {cx + square_size} {cy - square_size} '
                            f'L {cx} {cy - square_size}" fill="none" stroke="{color}" stroke-width="2"/>')
        else:
            # Draw arc
            end_x = cx + arc_radius * math.cos(angle_rad)
            end_y = cy - arc_radius * math.sin(angle_rad)
            large_arc = 1 if degrees > 180 else 0
            svg_parts.append(f'<path d="M {cx + arc_radius} {cy} A {arc_radius} {arc_radius} 0 {large_arc} 0 '
                            f'{end_x} {end_y}" fill="none" stroke="{color}" stroke-width="2"/>')
        
        # Add vertex dot
        svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{color}"/>')
        
        # Add labels
        svg_parts.append(f'<text x="{cx}" y="{cy + 50}" text-anchor="middle" font-size="14" font-weight="bold" '
                        f'fill="#333">{angle_data["name"]}</text>')
        svg_parts.append(f'<text x="{cx}" y="{cy + 68}" text-anchor="middle" font-size="12" '
                        f'fill="{color}">{category}</text>')
    
    # Add category headers
    svg_parts.append('<text x="200" y="90" text-anchor="middle" font-size="18" font-weight="bold" fill="#4CAF50">ACUTE ANGLES (Less than 90°)</text>')
    svg_parts.append('<text x="120" y="260" text-anchor="middle" font-size="18" font-weight="bold" fill="#2196F3">RIGHT ANGLE</text>')
    svg_parts.append('<text x="500" y="260" text-anchor="middle" font-size="18" font-weight="bold" fill="#FF9800">OBTUSE ANGLES (Greater than 90°)</text>')
    
    # Add visual guide box
    svg_parts.append('<rect x="50" y="400" width="700" height="80" fill="#f5f5f5" stroke="#999" stroke-width="1"/>')
    svg_parts.append('<text x="400" y="425" text-anchor="middle" font-size="16" font-weight="bold" fill="#333">Quick Reference:</text>')
    svg_parts.append('<text x="200" y="450" text-anchor="middle" font-size="14" fill="#4CAF50">Acute: Sharp/Narrow (< 90°)</text>')
    svg_parts.append('<text x="400" y="450" text-anchor="middle" font-size="14" fill="#2196F3">Right: Perfect Corner (= 90°)</text>')
    svg_parts.append('<text x="600" y="450" text-anchor="middle" font-size="14" fill="#FF9800">Obtuse: Wide/Open (> 90°)</text>')
    svg_parts.append('<text x="400" y="470" text-anchor="middle" font-size="12" fill="#666">Tip: Compare to a book corner or square edge!</text>')
    
    svg_parts.append('</svg>')
    return "".join(svg_parts)

def generate_angle_data(difficulty):
    """Generate angle configurations for different difficulty levels"""
    
    angles_data = []
    
    if difficulty == 1:
        # Clear, obvious angles
        angles_data = [
            # Very acute angles
            {"degrees": 30, "type": "acute", "show_square": False},
            {"degrees": 35, "type": "acute", "show_square": False},
            {"degrees": 45, "type": "acute", "show_square": False},
            {"degrees": 50, "type": "acute", "show_square": False},
            
            # Right angles (with square marker)
            {"degrees": 90, "type": "right", "show_square": True},
            
            # Very obtuse angles
            {"degrees": 120, "type": "obtuse", "show_square": False},
            {"degrees": 135, "type": "obtuse", "show_square": False},
            {"degrees": 140, "type": "obtuse", "show_square": False},
            {"degrees": 150, "type": "obtuse", "show_square": False},
        ]
    
    elif difficulty == 2:
        # Standard angles, less obvious
        angles_data = [
            # Acute angles
            {"degrees": 55, "type": "acute", "show_square": False},
            {"degrees": 60, "type": "acute", "show_square": False},
            {"degrees": 65, "type": "acute", "show_square": False},
            {"degrees": 70, "type": "acute", "show_square": False},
            {"degrees": 75, "type": "acute", "show_square": False},
            
            # Right angles
            {"degrees": 90, "type": "right", "show_square": True},
            {"degrees": 90, "type": "right", "show_square": False},  # Without marker
            
            # Obtuse angles
            {"degrees": 105, "type": "obtuse", "show_square": False},
            {"degrees": 110, "type": "obtuse", "show_square": False},
            {"degrees": 115, "type": "obtuse", "show_square": False},
            {"degrees": 125, "type": "obtuse", "show_square": False},
        ]
    
    elif difficulty == 3:
        # Challenging - angles close to 90°
        angles_data = [
            # Acute angles close to 90
            {"degrees": 80, "type": "acute", "show_square": False},
            {"degrees": 82, "type": "acute", "show_square": False},
            {"degrees": 85, "type": "acute", "show_square": False},
            {"degrees": 87, "type": "acute", "show_square": False},
            {"degrees": 89, "type": "acute", "show_square": False},
            
            # Right angles without markers
            {"degrees": 90, "type": "right", "show_square": False},
            {"degrees": 90, "type": "right", "show_square": True},
            
            # Obtuse angles close to 90
            {"degrees": 91, "type": "obtuse", "show_square": False},
            {"degrees": 93, "type": "obtuse", "show_square": False},
            {"degrees": 95, "type": "obtuse", "show_square": False},
            {"degrees": 98, "type": "obtuse", "show_square": False},
            {"degrees": 100, "type": "obtuse", "show_square": False},
        ]
    
    elif difficulty == 4:
        # Various orientations, mixed difficulty
        angles_data = [
            # Mixed acute
            {"degrees": 40, "type": "acute", "show_square": False},
            {"degrees": 72, "type": "acute", "show_square": False},
            {"degrees": 88, "type": "acute", "show_square": False},
            
            # Right angles at various orientations
            {"degrees": 90, "type": "right", "show_square": False},
            {"degrees": 90, "type": "right", "show_square": True},
            
            # Mixed obtuse
            {"degrees": 92, "type": "obtuse", "show_square": False},
            {"degrees": 108, "type": "obtuse", "show_square": False},
            {"degrees": 145, "type": "obtuse", "show_square": False},
            
            # Near-straight angles
            {"degrees": 160, "type": "obtuse", "show_square": False},
            {"degrees": 170, "type": "obtuse", "show_square": False},
        ]
    
    else:  # difficulty 5 - Expert level
        # Include straight and reflex angles
        angles_data = [
            # Very small acute
            {"degrees": 15, "type": "acute", "show_square": False},
            {"degrees": 25, "type": "acute", "show_square": False},
            
            # Borderline angles
            {"degrees": 89.5, "type": "acute", "show_square": False},
            {"degrees": 90, "type": "right", "show_square": False},
            {"degrees": 90.5, "type": "obtuse", "show_square": False},
            
            # Wide obtuse
            {"degrees": 155, "type": "obtuse", "show_square": False},
            {"degrees": 175, "type": "obtuse", "show_square": False},
            
            # Straight angle
            {"degrees": 180, "type": "straight", "show_square": False},
            
            # Reflex angles (advanced)
            {"degrees": 210, "type": "reflex", "show_square": False},
            {"degrees": 270, "type": "reflex", "show_square": False},
            {"degrees": 315, "type": "reflex", "show_square": False},
        ]
    
    return angles_data

def generate_new_question():
    """Generate a new angle comparison question"""
    
    difficulty = st.session_state.angle_difficulty
    
    # Keep track of recent angles
    if len(st.session_state.recent_angles) > 6:
        st.session_state.recent_angles = st.session_state.recent_angles[-3:]
    
    # Get angles for this difficulty
    all_angles = generate_angle_data(difficulty)
    
    # Balance angle types
    acute_count = st.session_state.angle_type_count.get("acute", 0)
    right_count = st.session_state.angle_type_count.get("right", 0)
    obtuse_count = st.session_state.angle_type_count.get("obtuse", 0)
    
    # Filter by type to balance
    min_count = min(acute_count, right_count, obtuse_count)
    if min_count < max(acute_count, right_count, obtuse_count) - 2:
        # Prefer the underrepresented type
        if acute_count == min_count:
            preferred_angles = [a for a in all_angles if a["type"] == "acute"]
        elif right_count == min_count:
            preferred_angles = [a for a in all_angles if a["type"] == "right"]
        else:
            preferred_angles = [a for a in all_angles if a["type"] == "obtuse"]
        
        if not preferred_angles:
            preferred_angles = all_angles
    else:
        preferred_angles = all_angles
    
    # Filter out recent angles
    available_angles = [a for a in preferred_angles if a["degrees"] not in st.session_state.recent_angles]
    
    if not available_angles:
        available_angles = preferred_angles
        st.session_state.recent_angles = []
    
    # Select an angle
    angle = random.choice(available_angles)
    
    # Track usage
    st.session_state.recent_angles.append(angle["degrees"])
    if angle["type"] in ["acute", "right", "obtuse"]:
        st.session_state.angle_type_count[angle["type"]] = st.session_state.angle_type_count.get(angle["type"], 0) + 1
    
    # Random rotation for the angle orientation
    base_rotation = random.choice([0, 45, 90, 135, 180, 225, 270, 315])
    
    # Random color
    colors = ["#2196F3", "#FF6B6B", "#4CAF50", "#9C27B0", "#FF9800", "#00BCD4", "#E91E63", "#8BC34A"]
    color = random.choice(colors)
    
    # Generate SVG
    svg_code = generate_angle_svg(angle["degrees"], base_rotation, color, angle.get("show_square", False))
    
    # Determine correct answer
    if angle["type"] == "acute":
        correct_answer = "less"
    elif angle["type"] == "right":
        correct_answer = "equal"
    elif angle["type"] in ["obtuse", "straight"]:
        correct_answer = "greater"
    elif angle["type"] == "reflex":
        correct_answer = "greater"  # Reflex is > 180°, definitely > 90°
    
    # Store question data
    st.session_state.question_data = {
        "angle_degrees": angle["degrees"],
        "angle_type": angle["type"],
        "svg_code": svg_code,
        "color": color,
        "base_rotation": base_rotation,
        "show_square": angle.get("show_square", False)
    }
    
    st.session_state.correct_answer = correct_answer
    st.session_state.current_question = "Is this angle greater than, equal to, or less than a right angle?"

def generate_angle_svg(degrees, base_rotation, color, show_square=False):
    """Generate SVG for an angle with specified properties"""
    
    width = 400
    height = 400
    center_x = width // 2
    center_y = height // 2
    ray_length = 120
    
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg_parts.append('<rect width="400" height="400" fill="white"/>')
    
    # Calculate ray positions with base rotation
    # First ray
    angle1_rad = math.radians(base_rotation)
    x1 = center_x + ray_length * math.cos(angle1_rad)
    y1 = center_y - ray_length * math.sin(angle1_rad)  # Negative for SVG coordinate system
    
    # Second ray
    angle2_rad = math.radians(base_rotation + degrees)
    x2 = center_x + ray_length * math.cos(angle2_rad)
    y2 = center_y - ray_length * math.sin(angle2_rad)
    
    # Draw the rays
    svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x1}" y2="{y1}" '
                    f'stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
    svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x2}" y2="{y2}" '
                    f'stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
    
    # Add arrows to the rays
    # Arrow for first ray
    dx1 = x1 - center_x
    dy1 = y1 - center_y
    length1 = math.sqrt(dx1*dx1 + dy1*dy1)
    if length1 > 0:
        dx1, dy1 = dx1/length1, dy1/length1
        arrow_base_x = x1 - 15*dx1
        arrow_base_y = y1 - 15*dy1
        perp_x, perp_y = -dy1*6, dx1*6
        svg_parts.append(f'<polygon points="{arrow_base_x + perp_x},{arrow_base_y + perp_y} {x1},{y1} '
                        f'{arrow_base_x - perp_x},{arrow_base_y - perp_y}" fill="{color}"/>')
    
    # Arrow for second ray
    dx2 = x2 - center_x
    dy2 = y2 - center_y
    length2 = math.sqrt(dx2*dx2 + dy2*dy2)
    if length2 > 0:
        dx2, dy2 = dx2/length2, dy2/length2
        arrow_base_x = x2 - 15*dx2
        arrow_base_y = y2 - 15*dy2
        perp_x, perp_y = -dy2*6, dx2*6
        svg_parts.append(f'<polygon points="{arrow_base_x + perp_x},{arrow_base_y + perp_y} {x2},{y2} '
                        f'{arrow_base_x - perp_x},{arrow_base_y - perp_y}" fill="{color}"/>')
    
    # Draw angle indicator
    if show_square and abs(degrees - 90) < 0.5:
        # Draw right angle square
        square_size = 20
        
        # Calculate square corner positions
        sq_x1 = center_x + square_size * math.cos(angle1_rad)
        sq_y1 = center_y - square_size * math.sin(angle1_rad)
        sq_x2 = center_x + square_size * math.cos(angle2_rad)
        sq_y2 = center_y - square_size * math.sin(angle2_rad)
        
        # Calculate the fourth corner of the square
        sq_x3 = sq_x1 + (sq_x2 - center_x)
        sq_y3 = sq_y1 + (sq_y2 - center_y)
        
        svg_parts.append(f'<path d="M {sq_x1} {sq_y1} L {sq_x3} {sq_y3} L {sq_x2} {sq_y2}" '
                        f'fill="none" stroke="{color}" stroke-width="2"/>')
    elif degrees < 180:
        # Draw angle arc for non-straight angles
        arc_radius = 30
        
        # Calculate arc endpoints
        arc_x1 = center_x + arc_radius * math.cos(angle1_rad)
        arc_y1 = center_y - arc_radius * math.sin(angle1_rad)
        arc_x2 = center_x + arc_radius * math.cos(angle2_rad)
        arc_y2 = center_y - arc_radius * math.sin(angle2_rad)
        
        # Determine if we need a large arc
        large_arc = 1 if degrees > 180 else 0
        
        svg_parts.append(f'<path d="M {arc_x1} {arc_y1} A {arc_radius} {arc_radius} 0 {large_arc} 0 '
                        f'{arc_x2} {arc_y2}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="2,2"/>')
    
    # Draw vertex dot
    svg_parts.append(f'<circle cx="{center_x}" cy="{center_y}" r="6" fill="{color}"/>')
    
    svg_parts.append('</svg>')
    return "".join(svg_parts)

def display_question():
    """Display the current question with the angle"""
    
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_question}")
    
    # Display the angle
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(data["svg_code"], unsafe_allow_html=True)
        
        # Add hint for difficult levels
        if st.session_state.angle_difficulty >= 3 and not data.get("show_square"):
            st.info("💡 **Tip:** Imagine a book corner or square edge at the vertex. How does this angle compare?")
    
    # Answer options
    st.markdown("")
    
    if not st.session_state.answer_submitted:
        # Three option buttons
        options = [
            ("greater", "greater than a right angle"),
            ("equal", "equal to a right angle"),
            ("less", "less than a right angle")
        ]
        
        for value, label in options:
            if st.button(
                label,
                key=f"option_{value}",
                use_container_width=True,
                type="primary" if value == st.session_state.selected_answer else "secondary"
            ):
                st.session_state.selected_answer = value
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
        options = [
            ("greater", "greater than a right angle"),
            ("equal", "equal to a right angle"),
            ("less", "less than a right angle")
        ]
        
        for value, label in options:
            if value == st.session_state.correct_answer:
                st.success(f"✓ {label}")
            elif value == st.session_state.selected_answer and value != st.session_state.correct_answer:
                st.error(f"✗ {label}")
            else:
                st.button(label, disabled=True, use_container_width=True)
        
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
    """Display feedback with reference chart for incorrect answers"""
    
    user_answer = st.session_state.selected_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    
    st.markdown("---")
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        angle_degrees = data["angle_degrees"]
        angle_type = data["angle_type"]
        
        # Show the angle classification
        if angle_type == "acute":
            st.markdown(f"### ✅ This is an **ACUTE angle** ({angle_degrees}°)")
            st.markdown("It's **less than** a right angle (< 90°)")
        elif angle_type == "right":
            st.markdown(f"### ✅ This is a **RIGHT angle** (90°)")
            st.markdown("It's **exactly equal to** 90°")
        elif angle_type == "obtuse":
            st.markdown(f"### ✅ This is an **OBTUSE angle** ({angle_degrees}°)")
            st.markdown("It's **greater than** a right angle (> 90°)")
        elif angle_type == "straight":
            st.markdown(f"### ✅ This is a **STRAIGHT angle** (180°)")
            st.markdown("It's **much greater than** a right angle")
        elif angle_type == "reflex":
            st.markdown(f"### ✅ This is a **REFLEX angle** ({angle_degrees}°)")
            st.markdown("It's **much greater than** a right angle (> 180°)")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.angle_difficulty
            st.session_state.angle_difficulty = min(st.session_state.angle_difficulty + 1, 5)
            st.session_state.consecutive_correct = 0
            
            if st.session_state.angle_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.angle_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        angle_degrees = data["angle_degrees"]
        angle_type = data["angle_type"]
        
        # Show what it actually is
        if angle_type == "acute":
            st.error(f"This angle is **LESS THAN** a right angle. It's an acute angle ({angle_degrees}°).")
        elif angle_type == "right":
            st.error(f"This angle is **EQUAL TO** a right angle. It's exactly 90°.")
        elif angle_type == "obtuse":
            st.error(f"This angle is **GREATER THAN** a right angle. It's an obtuse angle ({angle_degrees}°).")
        
        # Show reference chart for incorrect answers
        st.markdown("### 📚 Angle Reference Chart")
        st.markdown("Study this reference to better understand angle types:")
        
        reference_svg = get_angle_reference_chart()
        st.markdown(reference_svg, unsafe_allow_html=True)
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.angle_difficulty
            st.session_state.angle_difficulty = max(st.session_state.angle_difficulty - 1, 1)
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.angle_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.angle_difficulty}**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation about the angle"""
    
    data = st.session_state.question_data
    angle_degrees = data["angle_degrees"]
    angle_type = data["angle_type"]
    
    with st.expander("📖 **Understanding This Angle**", expanded=True):
        
        st.markdown(f"### This angle measures **{angle_degrees}°**")
        
        # Classification
        if angle_degrees < 90:
            st.markdown("""
            **Classification: ACUTE ANGLE**
            - Measures less than 90°
            - Looks sharp or narrow
            - The opening is smaller than a square corner
            """)
            
            # Distance from right angle
            difference = 90 - angle_degrees
            st.markdown(f"📏 This angle is **{difference}° less** than a right angle")
            
        elif angle_degrees == 90:
            st.markdown("""
            **Classification: RIGHT ANGLE**
            - Measures exactly 90°
            - Forms a perfect corner
            - Like the corner of a book or paper
            - Often marked with a small square □
            """)
            
        elif 90 < angle_degrees < 180:
            st.markdown("""
            **Classification: OBTUSE ANGLE**
            - Measures more than 90° but less than 180°
            - Looks wide or open
            - The opening is larger than a square corner
            """)
            
            # Distance from right angle
            difference = angle_degrees - 90
            st.markdown(f"📏 This angle is **{difference}° more** than a right angle")
            
        elif angle_degrees == 180:
            st.markdown("""
            **Classification: STRAIGHT ANGLE**
            - Measures exactly 180°
            - Forms a straight line
            - Twice as large as a right angle
            """)
            
        elif angle_degrees > 180:
            st.markdown("""
            **Classification: REFLEX ANGLE**
            - Measures more than 180°
            - The larger angle when two rays meet
            - Goes "around" more than halfway
            """)
        
        # Visual comparison tips
        st.markdown("### 🎯 Quick Recognition Tips:")
        
        if angle_type == "acute":
            st.markdown("""
            - **Acute angles** look like:
              - The letter "V"
              - A bird's beak
              - Pizza slice (narrow)
              - Clock hands at 1:00 or 2:00
            """)
        elif angle_type == "right":
            st.markdown("""
            - **Right angles** look like:
              - The letter "L"
              - Corner of a square
              - Corner of a book
              - Clock hands at 3:00 or 9:00
            """)
        elif angle_type == "obtuse":
            st.markdown("""
            - **Obtuse angles** look like:
              - An open book
              - Wide pizza slice
              - Clock hands at 4:00 or 5:00
              - A reclining chair back
            """)
        
        # Memory device
        st.markdown("### 🧠 Memory Trick:")
        st.markdown("""
        **A**cute = **A** small angle (< 90°)
        **R**ight = **R**ight at 90°
        **O**btuse = **O**pen wide (> 90°)
        """)
        
        # Real-world examples
        st.markdown("### 🌎 Real-World Examples:")
        
        angle_examples = {
            30: "Roof pitch on some houses",
            45: "Diagonal of a square, ramp incline",
            60: "Equilateral triangle corners",
            90: "Square corners, crossroads",
            120: "Wide-open scissors",
            135: "Open laptop screen",
            180: "Straight line, flat surface"
        }
        
        closest_example = min(angle_examples.keys(), key=lambda x: abs(x - angle_degrees))
        if abs(closest_example - angle_degrees) < 5:
            st.info(f"💡 Similar to: {angle_examples[closest_example]}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None