import streamlit as st
import random
import math

def run():
    """
    Main function to run the Special Angles (90, 180, 270, 360) practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/angles_90_180_270_360.py
    """
    
    # Initialize session state
    if "special_angle_difficulty" not in st.session_state:
        st.session_state.special_angle_difficulty = 1
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_wrong = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.recent_angles = []
        st.session_state.question_type_count = {"degrees": 0, "fraction": 0}
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_answer = None
        st.session_state.question_format = None
        st.session_state.answer_options = []  # Store the shuffled options here!
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("📐 Angles of 90°, 180°, 270° and 360°")
    st.markdown("*Recognize special angles and fractions of a turn*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.special_angle_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic angles in standard positions",
            2: "Angles in various orientations",
            3: "Mixed degrees and fractions",
            4: "Complex orientations",
            5: "Expert with all variations"
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
        ### Special Angles and Turns
        
        **Key Angles to Remember:**
        
        | Angle | Degrees | Fraction of Turn | Description |
        |-------|---------|-----------------|-------------|
        | **Right Angle** | 90° | 1/4 turn | Quarter turn, L-shape |
        | **Straight Angle** | 180° | 1/2 turn | Half turn, straight line |
        | **Three-Quarter** | 270° | 3/4 turn | Three-quarter turn |
        | **Full Turn** | 360° | 1 turn | Complete rotation |
        
        ### Understanding Turns:
        
        **A full turn = 360 degrees = 1 complete rotation**
        
        - **1/4 turn (quarter turn)** = 90° 
          - Like turning from 12 to 3 on a clock
          - Makes a right angle
        
        - **1/2 turn (half turn)** = 180°
          - Like turning from 12 to 6 on a clock
          - Makes a straight line
        
        - **3/4 turn (three-quarter turn)** = 270°
          - Like turning from 12 to 9 on a clock
          - Three right angles
        
        - **1 full turn** = 360°
          - Back to where you started
          - Complete circle
        
        ### Visual Recognition Tips:
        
        **90° (Right Angle):**
        - Perfect L-shape
        - Square corner
        - Often marked with a small square □
        
        **180° (Straight Angle):**
        - Straight line
        - Two rays pointing opposite directions
        - Like an arrow pointing both ways ←→
        
        **270° (Three-Quarter Turn):**
        - Three right angles
        - Goes around 3/4 of a circle
        - Looks like a reflex angle
        
        **360° (Full Turn):**
        - Complete rotation
        - Rays overlap (point same direction)
        - Back to starting position
        
        ### Clock Face Method:
        
        Imagine a clock face:
        - **90°** = 15 minutes (quarter past)
        - **180°** = 30 minutes (half past)
        - **270°** = 45 minutes (quarter to)
        - **360°** = 60 minutes (full hour)
        """)

def get_special_angles_reference():
    """Generate a comprehensive reference chart for special angles"""
    
    width = 900
    height = 600
    
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg_parts.append('<rect width="900" height="600" fill="white" stroke="#ddd" stroke-width="2"/>')
    svg_parts.append('<text x="450" y="30" text-anchor="middle" font-size="24" font-weight="bold" fill="#333">Special Angles Reference Chart</text>')
    
    # Define the four special angles
    angles_data = [
        {
            "degrees": 90,
            "fraction": "1/4 turn",
            "name": "Right Angle",
            "pos": (150, 180),
            "color": "#2196F3"
        },
        {
            "degrees": 180,
            "fraction": "1/2 turn",
            "name": "Straight Angle",
            "pos": (450, 180),
            "color": "#4CAF50"
        },
        {
            "degrees": 270,
            "fraction": "3/4 turn",
            "name": "Three-Quarter Turn",
            "pos": (750, 180),
            "color": "#FF9800"
        },
        {
            "degrees": 360,
            "fraction": "1 full turn",
            "name": "Full Turn",
            "pos": (300, 420),
            "color": "#9C27B0"
        }
    ]
    
    for angle in angles_data:
        cx, cy = angle["pos"]
        degrees = angle["degrees"]
        color = angle["color"]
        
        # Draw the angle
        ray_length = 70
        
        if degrees == 360:
            # Full turn - show circular arrow
            radius = 40
            svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{color}" stroke-width="3" stroke-dasharray="5,5"/>')
            
            # Add circular arrow
            arrow_angle = 45
            arrow_x = cx + radius * math.cos(math.radians(arrow_angle))
            arrow_y = cy - radius * math.sin(math.radians(arrow_angle))
            
            # Arrow head
            svg_parts.append(f'<polygon points="{arrow_x-5},{arrow_y-8} {arrow_x+5},{arrow_y} {arrow_x-5},{arrow_y+8}" fill="{color}"/>')
            
            # Center rays (overlapping)
            svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + ray_length}" y2="{cy}" stroke="{color}" stroke-width="3"/>')
            svg_parts.append(f'<polygon points="{cx + ray_length - 8},{cy - 4} {cx + ray_length},{cy} {cx + ray_length - 8},{cy + 4}" fill="{color}"/>')
            
        else:
            # First ray (horizontal to the right)
            svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + ray_length}" y2="{cy}" stroke="{color}" stroke-width="3"/>')
            svg_parts.append(f'<polygon points="{cx + ray_length - 8},{cy - 4} {cx + ray_length},{cy} {cx + ray_length - 8},{cy + 4}" fill="{color}"/>')
            
            # Second ray at the angle
            angle_rad = math.radians(degrees)
            x2 = cx + ray_length * math.cos(angle_rad)
            y2 = cy - ray_length * math.sin(angle_rad)
            
            svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3"/>')
            
            # Arrow on second ray
            dx = x2 - cx
            dy = y2 - cy
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                dx, dy = dx/length, dy/length
                arrow_x = x2 - 8*dx
                arrow_y = y2 - 8*dy
                perp_x, perp_y = -dy*4, dx*4
                svg_parts.append(f'<polygon points="{arrow_x + perp_x},{arrow_y + perp_y} {x2},{y2} {arrow_x - perp_x},{arrow_y - perp_y}" fill="{color}"/>')
            
            # Draw angle indicator
            if degrees == 90:
                # Right angle square
                square_size = 15
                svg_parts.append(f'<path d="M {cx + square_size} {cy} L {cx + square_size} {cy - square_size} L {cx} {cy - square_size}" '
                                f'fill="none" stroke="{color}" stroke-width="2"/>')
            elif degrees == 180:
                # Semicircle arc
                arc_radius = 25
                svg_parts.append(f'<path d="M {cx + arc_radius} {cy} A {arc_radius} {arc_radius} 0 0 0 {cx - arc_radius} {cy}" '
                                f'fill="none" stroke="{color}" stroke-width="2"/>')
            elif degrees == 270:
                # Three-quarter circle arc
                arc_radius = 25
                end_x = cx + arc_radius * math.cos(angle_rad)
                end_y = cy - arc_radius * math.sin(angle_rad)
                svg_parts.append(f'<path d="M {cx + arc_radius} {cy} A {arc_radius} {arc_radius} 0 1 0 {end_x} {end_y}" '
                                f'fill="none" stroke="{color}" stroke-width="2"/>')
        
        # Draw vertex dot
        svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{color}"/>')
        
        # Add labels
        svg_parts.append(f'<text x="{cx}" y="{cy + 70}" text-anchor="middle" font-size="18" font-weight="bold" fill="{color}">{angle["degrees"]}°</text>')
        svg_parts.append(f'<text x="{cx}" y="{cy + 90}" text-anchor="middle" font-size="16" fill="#666">{angle["fraction"]}</text>')
        svg_parts.append(f'<text x="{cx}" y="{cy + 110}" text-anchor="middle" font-size="14" fill="#333">{angle["name"]}</text>')
    
    # Add clock comparison
    clock_cy = 420
    clock_cx = 600
    clock_radius = 60
    
    svg_parts.append(f'<text x="{clock_cx}" y="{clock_cy - 80}" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">Clock Comparison</text>')
    svg_parts.append(f'<circle cx="{clock_cx}" cy="{clock_cy}" r="{clock_radius}" fill="none" stroke="#999" stroke-width="2"/>')
    
    # Clock numbers
    for hour in [12, 3, 6, 9]:
        angle = (hour * 30 - 90) * math.pi / 180
        num_x = clock_cx + clock_radius * 0.85 * math.cos(angle)
        num_y = clock_cy + clock_radius * 0.85 * math.sin(angle) + 5
        svg_parts.append(f'<text x="{num_x}" y="{num_y}" text-anchor="middle" font-size="14" fill="#666">{hour}</text>')
    
    # Clock hands showing quarter turns
    svg_parts.append(f'<line x1="{clock_cx}" y1="{clock_cy}" x2="{clock_cx}" y2="{clock_cy - 40}" stroke="#333" stroke-width="3" stroke-linecap="round"/>')
    svg_parts.append(f'<circle cx="{clock_cx}" cy="{clock_cy}" r="4" fill="#333"/>')
    
    # Labels for clock
    svg_parts.append(f'<text x="{clock_cx}" y="{clock_cy + 90}" text-anchor="middle" font-size="14" fill="#666">12→3 = 90° (1/4)</text>')
    svg_parts.append(f'<text x="{clock_cx}" y="{clock_cy + 105}" text-anchor="middle" font-size="14" fill="#666">12→6 = 180° (1/2)</text>')
    svg_parts.append(f'<text x="{clock_cx}" y="{clock_cy + 120}" text-anchor="middle" font-size="14" fill="#666">12→9 = 270° (3/4)</text>')
    svg_parts.append(f'<text x="{clock_cx}" y="{clock_cy + 135}" text-anchor="middle" font-size="14" fill="#666">12→12 = 360° (1)</text>')
    
    svg_parts.append('</svg>')
    return "".join(svg_parts)

def get_turn_visual_reference():
    """Generate a visual reference for understanding turns"""
    
    width = 800
    height = 400
    
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg_parts.append('<rect width="800" height="400" fill="#f9f9f9" stroke="#ddd" stroke-width="2"/>')
    svg_parts.append('<text x="400" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#333">Understanding Turns and Rotations</text>')
    
    # Show rotation examples
    examples = [
        {"start": 0, "end": 90, "label": "1/4 Turn", "desc": "90° clockwise", "pos": (150, 150)},
        {"start": 0, "end": 180, "label": "1/2 Turn", "desc": "180° rotation", "pos": (350, 150)},
        {"start": 0, "end": 270, "label": "3/4 Turn", "desc": "270° clockwise", "pos": (550, 150)},
        {"start": 0, "end": 360, "label": "Full Turn", "desc": "360° complete", "pos": (750, 150)},
    ]
    
    for ex in examples:
        cx, cy = ex["pos"]
        radius = 50
        
        # Draw circle guide
        svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#ddd" stroke-width="1"/>')
        
        # Starting position (top)
        start_x = cx
        start_y = cy - radius
        svg_parts.append(f'<circle cx="{start_x}" cy="{start_y}" r="4" fill="#4CAF50"/>')
        svg_parts.append(f'<text x="{start_x}" y="{start_y - 10}" text-anchor="middle" font-size="12" fill="#4CAF50">Start</text>')
        
        # Ending position
        angle_rad = math.radians(ex["end"] - 90)  # -90 because we start from top
        end_x = cx + radius * math.cos(angle_rad)
        end_y = cy + radius * math.sin(angle_rad)
        svg_parts.append(f'<circle cx="{end_x}" cy="{end_y}" r="4" fill="#FF5722"/>')
        
        # Draw arc
        if ex["end"] < 360:
            large_arc = 1 if ex["end"] > 180 else 0
            svg_parts.append(f'<path d="M {start_x} {start_y} A {radius} {radius} 0 {large_arc} 1 {end_x} {end_y}" '
                            f'fill="none" stroke="#2196F3" stroke-width="3"/>')
            
            # Arrowhead at end
            tangent_angle = angle_rad + math.pi/2
            arrow_dx = 8 * math.cos(tangent_angle)
            arrow_dy = 8 * math.sin(tangent_angle)
            svg_parts.append(f'<polygon points="{end_x},{end_y} {end_x - arrow_dx},{end_y - arrow_dy} '
                            f'{end_x + arrow_dx},{end_y + arrow_dy}" fill="#2196F3"/>')
        else:
            # Full circle
            svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#2196F3" stroke-width="3"/>')
            # Arrow on circle
            arrow_x = cx + radius
            arrow_y = cy
            svg_parts.append(f'<polygon points="{arrow_x},{arrow_y-5} {arrow_x+8},{arrow_y} {arrow_x},{arrow_y+5}" fill="#2196F3"/>')
        
        # Labels
        svg_parts.append(f'<text x="{cx}" y="{cy + radius + 25}" text-anchor="middle" font-size="16" font-weight="bold" fill="#333">{ex["label"]}</text>')
        svg_parts.append(f'<text x="{cx}" y="{cy + radius + 42}" text-anchor="middle" font-size="14" fill="#666">{ex["desc"]}</text>')
    
    # Add fraction equation
    svg_parts.append('<text x="400" y="280" text-anchor="middle" font-size="18" font-weight="bold" fill="#333">Quick Formula</text>')
    svg_parts.append('<rect x="250" y="295" width="300" height="80" fill="white" stroke="#999" stroke-width="1" rx="5"/>')
    svg_parts.append('<text x="400" y="320" text-anchor="middle" font-size="16" fill="#333">Degrees = Fraction × 360°</text>')
    svg_parts.append('<text x="400" y="345" text-anchor="middle" font-size="14" fill="#666">1/4 × 360° = 90°</text>')
    svg_parts.append('<text x="400" y="365" text-anchor="middle" font-size="14" fill="#666">1/2 × 360° = 180°</text>')
    
    svg_parts.append('</svg>')
    return "".join(svg_parts)

def generate_angle_configurations(difficulty):
    """Generate angle configurations for different difficulty levels"""
    
    configs = []
    
    if difficulty == 1:
        # Basic angles in standard positions
        configs = [
            # 90° angles
            {"degrees": 90, "orientations": [0, 90, 180, 270], "show_square": True},
            # 180° angles
            {"degrees": 180, "orientations": [0, 90], "show_square": False},
            # 270° angles
            {"degrees": 270, "orientations": [0, 90, 180, 270], "show_square": False},
            # 360° angles (full turn)
            {"degrees": 360, "orientations": [0], "show_square": False},
        ]
    
    elif difficulty == 2:
        # Various orientations
        configs = [
            # 90° at different angles
            {"degrees": 90, "orientations": [30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330], "show_square": True},
            # 180° at different angles
            {"degrees": 180, "orientations": [30, 45, 60, 120, 135, 150], "show_square": False},
            # 270° at different angles
            {"degrees": 270, "orientations": [30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330], "show_square": False},
        ]
    
    elif difficulty == 3:
        # Mixed with fraction questions
        configs = [
            # All angles at various orientations, sometimes without visual hints
            {"degrees": 90, "orientations": list(range(0, 360, 15)), "show_square": random.choice([True, False])},
            {"degrees": 180, "orientations": list(range(0, 180, 15)), "show_square": False},
            {"degrees": 270, "orientations": list(range(0, 360, 15)), "show_square": False},
            {"degrees": 360, "orientations": [0, 45, 90, 135, 180], "show_square": False},
        ]
    
    elif difficulty == 4:
        # Complex orientations without helpers
        configs = [
            {"degrees": 90, "orientations": list(range(0, 360, 10)), "show_square": False},
            {"degrees": 180, "orientations": list(range(0, 180, 10)), "show_square": False},
            {"degrees": 270, "orientations": list(range(0, 360, 10)), "show_square": False},
            {"degrees": 360, "orientations": list(range(0, 360, 30)), "show_square": False},
        ]
    
    else:  # difficulty 5
        # Expert level - all variations
        configs = [
            {"degrees": 90, "orientations": list(range(0, 360, 5)), "show_square": False},
            {"degrees": 180, "orientations": list(range(0, 180, 5)), "show_square": False},
            {"degrees": 270, "orientations": list(range(0, 360, 5)), "show_square": False},
            {"degrees": 360, "orientations": list(range(0, 360, 15)), "show_square": False},
        ]
    
    return configs

def generate_new_question():
    """Generate a new special angle question"""
    
    difficulty = st.session_state.special_angle_difficulty
    
    # Balance between degree and fraction questions
    degrees_count = st.session_state.question_type_count.get("degrees", 0)
    fraction_count = st.session_state.question_type_count.get("fraction", 0)
    
    # Decide question format
    if difficulty == 1:
        # Start with degree questions
        question_format = "degrees"
    elif difficulty == 2:
        # Mostly degrees, some fractions
        question_format = random.choices(["degrees", "fraction"], weights=[3, 1])[0]
    elif difficulty >= 3:
        # Balance between both
        if degrees_count > fraction_count + 2:
            question_format = "fraction"
        elif fraction_count > degrees_count + 2:
            question_format = "degrees"
        else:
            question_format = random.choice(["degrees", "fraction"])
    
    st.session_state.question_format = question_format
    st.session_state.question_type_count[question_format] = st.session_state.question_type_count.get(question_format, 0) + 1
    
    # Get angle configurations
    configs = generate_angle_configurations(difficulty)
    
    # Select a random configuration
    config = random.choice(configs)
    angle_degrees = config["degrees"]
    orientation = random.choice(config["orientations"])
    show_square = config.get("show_square", False) and angle_degrees == 90
    
    # Avoid recent angles
    if len(st.session_state.recent_angles) > 4:
        st.session_state.recent_angles = st.session_state.recent_angles[-2:]
    
    # Track usage
    st.session_state.recent_angles.append(angle_degrees)
    
    # Random color
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#00BCD4", "#E91E63", "#795548", "#607D8B"]
    color = random.choice(colors)
    
    # Generate SVG
    svg_code = generate_special_angle_svg(angle_degrees, orientation, color, show_square)
    
    # IMPORTANT: Generate and store the answer options HERE, during question generation
    if question_format == "degrees":
        if angle_degrees == 360:
            options = ["90°", "180°", "360°"]
        else:
            # Standard options for 90, 180, 270
            all_options = ["90°", "180°", "270°"]
            if f"{angle_degrees}°" not in all_options:
                all_options.append(f"{angle_degrees}°")
            
            # Select 3 options including correct answer
            correct = f"{angle_degrees}°"
            other_options = [opt for opt in all_options if opt != correct]
            random.shuffle(other_options)
            options = [correct] + other_options[:2]
            random.shuffle(options)
        
        st.session_state.answer_options = options
        st.session_state.correct_answer = str(angle_degrees)
        st.session_state.current_question = "What is the measurement of this angle?"
    
    else:  # fraction format
        if angle_degrees == 90:
            options = [("1/4", "¼ turn"), ("1/2", "½ turn"), ("3/4", "¾ turn")]
        elif angle_degrees == 180:
            options = [("1/4", "¼ turn"), ("1/2", "½ turn"), ("3/4", "¾ turn")]
        elif angle_degrees == 270:
            options = [("1/4", "¼ turn"), ("1/2", "½ turn"), ("3/4", "¾ turn")]
        elif angle_degrees == 360:
            options = [("1/2", "½ turn"), ("3/4", "¾ turn"), ("1", "1 turn")]
        
        st.session_state.answer_options = options
        
        fraction_map = {
            90: "1/4",
            180: "1/2",
            270: "3/4",
            360: "1"
        }
        st.session_state.correct_answer = fraction_map[angle_degrees]
        st.session_state.current_question = "What fraction of a turn is this angle?"
    
    # Store question data
    st.session_state.question_data = {
        "angle_degrees": angle_degrees,
        "orientation": orientation,
        "svg_code": svg_code,
        "color": color,
        "show_square": show_square
    }

def generate_special_angle_svg(degrees, orientation, color, show_square=False):
    """Generate SVG for special angles (90, 180, 270, 360)"""
    
    width = 400
    height = 400
    center_x = width // 2
    center_y = height // 2
    ray_length = 120
    
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg_parts.append('<rect width="400" height="400" fill="white"/>')
    
    if degrees == 360:
        # Full turn - special visualization
        # Show overlapping rays with circular indicator
        angle_rad = math.radians(orientation)
        x1 = center_x + ray_length * math.cos(angle_rad)
        y1 = center_y - ray_length * math.sin(angle_rad)
        
        # Draw circle to indicate full rotation
        svg_parts.append(f'<circle cx="{center_x}" cy="{center_y}" r="50" fill="none" '
                        f'stroke="{color}" stroke-width="2" stroke-dasharray="5,5" opacity="0.5"/>')
        
        # Draw the overlapping rays
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x1}" y2="{y1}" '
                        f'stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
        
        # Draw a second ray slightly offset to show overlap
        offset_angle = angle_rad + 0.05
        x2 = center_x + ray_length * math.cos(offset_angle)
        y2 = center_y - ray_length * math.sin(offset_angle)
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x2}" y2="{y2}" '
                        f'stroke="{color}" stroke-width="4" stroke-linecap="round" opacity="0.7"/>')
        
        # Add rotation arrow
        arc_radius = 60
        arrow_angle = orientation + 45
        arrow_rad = math.radians(arrow_angle)
        arrow_x = center_x + arc_radius * math.cos(arrow_rad)
        arrow_y = center_y - arc_radius * math.sin(arrow_rad)
        
        # Arrow pointing in rotation direction
        tangent = arrow_rad + math.pi/2
        dx = 8 * math.cos(tangent)
        dy = 8 * math.sin(tangent)
        svg_parts.append(f'<polygon points="{arrow_x},{arrow_y} {arrow_x-dx},{arrow_y-dy} {arrow_x+dx},{arrow_y+dy}" '
                        f'fill="{color}"/>')
        
        # Add arrows to rays
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
    
    else:
        # Regular angle visualization
        # First ray
        angle1_rad = math.radians(orientation)
        x1 = center_x + ray_length * math.cos(angle1_rad)
        y1 = center_y - ray_length * math.sin(angle1_rad)
        
        # Second ray
        angle2_rad = math.radians(orientation + degrees)
        x2 = center_x + ray_length * math.cos(angle2_rad)
        y2 = center_y - ray_length * math.sin(angle2_rad)
        
        # Draw the rays
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x1}" y2="{y1}" '
                        f'stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
        svg_parts.append(f'<line x1="{center_x}" y1="{center_y}" x2="{x2}" y2="{y2}" '
                        f'stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
        
        # Add arrows to rays
        for (x, y) in [(x1, y1), (x2, y2)]:
            dx = x - center_x
            dy = y - center_y
            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                dx, dy = dx/length, dy/length
                arrow_base_x = x - 15*dx
                arrow_base_y = y - 15*dy
                perp_x, perp_y = -dy*6, dx*6
                svg_parts.append(f'<polygon points="{arrow_base_x + perp_x},{arrow_base_y + perp_y} {x},{y} '
                                f'{arrow_base_x - perp_x},{arrow_base_y - perp_y}" fill="{color}"/>')
        
        # Draw angle indicator
        if show_square and degrees == 90:
            # Right angle square
            square_size = 20
            
            # Calculate square vectors
            sq_x1 = center_x + square_size * math.cos(angle1_rad)
            sq_y1 = center_y - square_size * math.sin(angle1_rad)
            sq_x2 = center_x + square_size * math.cos(angle2_rad)
            sq_y2 = center_y - square_size * math.sin(angle2_rad)
            
            # Calculate the corner point
            sq_corner_x = sq_x1 + (sq_x2 - center_x)
            sq_corner_y = sq_y1 + (sq_y2 - center_y)
            
            svg_parts.append(f'<path d="M {sq_x1} {sq_y1} L {sq_corner_x} {sq_corner_y} L {sq_x2} {sq_y2}" '
                            f'fill="none" stroke="{color}" stroke-width="2"/>')
        
        elif degrees == 180:
            # Semicircle arc for straight angle
            arc_radius = 30
            arc_x1 = center_x + arc_radius * math.cos(angle1_rad)
            arc_y1 = center_y - arc_radius * math.sin(angle1_rad)
            arc_x2 = center_x + arc_radius * math.cos(angle2_rad)
            arc_y2 = center_y - arc_radius * math.sin(angle2_rad)
            
            svg_parts.append(f'<path d="M {arc_x1} {arc_y1} A {arc_radius} {arc_radius} 0 0 0 {arc_x2} {arc_y2}" '
                            f'fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="3,3"/>')
        
        elif degrees == 270:
            # Three-quarter circle arc
            arc_radius = 30
            arc_x1 = center_x + arc_radius * math.cos(angle1_rad)
            arc_y1 = center_y - arc_radius * math.sin(angle1_rad)
            arc_x2 = center_x + arc_radius * math.cos(angle2_rad)
            arc_y2 = center_y - arc_radius * math.sin(angle2_rad)
            
            svg_parts.append(f'<path d="M {arc_x1} {arc_y1} A {arc_radius} {arc_radius} 0 1 0 {arc_x2} {arc_y2}" '
                            f'fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="3,3"/>')
    
    # Draw vertex dot
    svg_parts.append(f'<circle cx="{center_x}" cy="{center_y}" r="6" fill="{color}"/>')
    
    svg_parts.append('</svg>')
    return "".join(svg_parts)

def display_question():
    """Display the current question with the angle"""
    
    data = st.session_state.question_data
    question_format = st.session_state.question_format
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_question}")
    
    # Display the angle
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(data["svg_code"], unsafe_allow_html=True)
        
        # Add hint for higher difficulties
        if st.session_state.special_angle_difficulty >= 3:
            if data["angle_degrees"] == 360:
                st.info("💡 **Hint:** Look for overlapping rays - they point in the same direction!")
            elif not data.get("show_square") and data["angle_degrees"] == 90:
                st.info("💡 **Hint:** Does this form a perfect corner like the edge of a paper?")
    
    # Answer options based on question format
    st.markdown("")
    
    if not st.session_state.answer_submitted:
        # Use the stored options from session state (NO RESHUFFLING HERE!)
        options = st.session_state.answer_options
        
        if question_format == "degrees":
            # Display degree options
            cols = st.columns(3)
            for i, option in enumerate(options):
                with cols[i]:
                    value = option.replace("°", "")
                    if st.button(
                        option,
                        key=f"option_{i}",
                        use_container_width=True,
                        type="primary" if value == st.session_state.selected_answer else "secondary"
                    ):
                        st.session_state.selected_answer = value
                        st.rerun()
        
        else:  # fraction format
            # Display fraction options
            cols = st.columns(3)
            for i, (value, label) in enumerate(options):
                with cols[i]:
                    if st.button(
                        label,
                        key=f"option_{i}",
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
        show_answer_feedback()
        
        # Next question button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_answer_feedback():
    """Show answer feedback after submission"""
    
    question_format = st.session_state.question_format
    correct_answer = st.session_state.correct_answer
    selected_answer = st.session_state.selected_answer
    options = st.session_state.answer_options  # Use stored options
    
    # Display the options with correct/incorrect markers
    if question_format == "degrees":
        cols = st.columns(len(options))
        for i, option in enumerate(options):
            with cols[i]:
                value = option.replace("°", "")
                if value == correct_answer:
                    st.success(f"✓ {option}")
                elif value == selected_answer:
                    st.error(f"✗ {option}")
                else:
                    st.button(option, disabled=True, use_container_width=True)
    
    else:  # fractions
        cols = st.columns(len(options))
        for i, (value, label) in enumerate(options):
            with cols[i]:
                if value == correct_answer:
                    st.success(f"✓ {label}")
                elif value == selected_answer:
                    st.error(f"✗ {label}")
                else:
                    st.button(label, disabled=True, use_container_width=True)
    
    # Show feedback
    show_feedback()

def show_feedback():
    """Display feedback with reference charts for incorrect answers"""
    
    user_answer = st.session_state.selected_answer
    correct_answer = st.session_state.correct_answer
    data = st.session_state.question_data
    question_format = st.session_state.question_format
    
    st.markdown("---")
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        angle_degrees = data["angle_degrees"]
        
        # Show the classification
        if question_format == "degrees":
            st.markdown(f"### ✅ This angle measures **{angle_degrees}°**")
        else:
            fraction_display = {
                "1/4": "¼ turn (quarter turn)",
                "1/2": "½ turn (half turn)",
                "3/4": "¾ turn (three-quarter turn)",
                "1": "1 full turn (complete rotation)"
            }
            st.markdown(f"### ✅ This is **{fraction_display[correct_answer]}**")
            st.markdown(f"Which equals **{angle_degrees}°**")
        
        # Special notes
        if angle_degrees == 90:
            st.info("📐 **Right angle:** Perfect corner, like the edge of a paper!")
        elif angle_degrees == 180:
            st.info("📐 **Straight angle:** A straight line, half a complete turn!")
        elif angle_degrees == 270:
            st.info("📐 **Three-quarter turn:** Three right angles, almost a full circle!")
        elif angle_degrees == 360:
            st.info("📐 **Full turn:** Complete rotation, back to where you started!")
        
        # Update difficulty
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_wrong = 0
        
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.special_angle_difficulty
            st.session_state.special_angle_difficulty = min(st.session_state.special_angle_difficulty + 1, 5)
            st.session_state.consecutive_correct = 0
            
            if st.session_state.special_angle_difficulty > old_difficulty:
                st.balloons()
                st.info(f"⬆️ **Level Up! Now at Level {st.session_state.special_angle_difficulty}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        angle_degrees = data["angle_degrees"]
        
        # Show correct answer
        if question_format == "degrees":
            st.error(f"The correct answer is **{angle_degrees}°**")
        else:
            fraction_map = {
                90: "¼ turn",
                180: "½ turn",
                270: "¾ turn",
                360: "1 full turn"
            }
            st.error(f"The correct answer is **{fraction_map[angle_degrees]}** ({angle_degrees}°)")
        
        # Show reference charts for incorrect answers
        st.markdown("### 📚 Reference Charts")
        st.markdown("Study these references to better understand special angles:")
        
        # Main reference chart
        reference_svg = get_special_angles_reference()
        st.markdown(reference_svg, unsafe_allow_html=True)
        
        # Turn visualization
        st.markdown("### 🔄 Understanding Turns")
        turn_svg = get_turn_visual_reference()
        st.markdown(turn_svg, unsafe_allow_html=True)
        
        # Update difficulty
        st.session_state.consecutive_wrong += 1
        st.session_state.consecutive_correct = 0
        
        if st.session_state.consecutive_wrong >= 2:
            old_difficulty = st.session_state.special_angle_difficulty
            st.session_state.special_angle_difficulty = max(st.session_state.special_angle_difficulty - 1, 1)
            st.session_state.consecutive_wrong = 0
            
            if st.session_state.special_angle_difficulty < old_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.special_angle_difficulty}**")
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show detailed explanation about the angle"""
    
    data = st.session_state.question_data
    angle_degrees = data["angle_degrees"]
    question_format = st.session_state.question_format
    
    with st.expander("📖 **Understanding This Angle**", expanded=True):
        
        st.markdown(f"### Angle Details:")
        
        # Show both representations
        fraction_map = {
            90: ("1/4", "¼", "quarter"),
            180: ("1/2", "½", "half"),
            270: ("3/4", "¾", "three-quarter"),
            360: ("1", "1", "full")
        }
        
        if angle_degrees in fraction_map:
            frac, display, name = fraction_map[angle_degrees]
            st.markdown(f"""
            **Degrees:** {angle_degrees}°
            **Fraction:** {display} turn ({name} turn)
            **Calculation:** {frac} × 360° = {angle_degrees}°
            """)
        
        # Visual descriptions
        if angle_degrees == 90:
            st.markdown("""
            ### 90° (Right Angle) - Quarter Turn
            - Forms a perfect **L-shape**
            - Like the **corner of a square**
            - **1/4 of a full rotation**
            - Clock analogy: 12 to 3 (or any 15 minutes)
            - Common in: buildings, books, screens
            """)
            
        elif angle_degrees == 180:
            st.markdown("""
            ### 180° (Straight Angle) - Half Turn
            - Forms a **straight line**
            - Rays point in **opposite directions**
            - **1/2 of a full rotation**
            - Clock analogy: 12 to 6 (30 minutes)
            - Like turning around to face the opposite way
            """)
            
        elif angle_degrees == 270:
            st.markdown("""
            ### 270° (Three-Quarter Turn)
            - **3/4 of a full rotation**
            - Three right angles combined
            - Clock analogy: 12 to 9 (45 minutes)
            - Reflex angle (more than 180°)
            - One more quarter turn completes the circle
            """)
            
        elif angle_degrees == 360:
            st.markdown("""
            ### 360° (Full Turn) - Complete Rotation
            - **Complete circle**
            - Back to starting position
            - Rays **overlap** (point same direction)
            - Clock analogy: full hour (60 minutes)
            - Like spinning around once completely
            """)
        
        # Memory tips
        st.markdown("### 🧠 Memory Tips:")
        st.markdown("""
        **Quick Division Method:**
        - 360° ÷ 4 = 90° (quarter)
        - 360° ÷ 2 = 180° (half)
        - 360° × 3/4 = 270° (three-quarters)
        - 360° × 1 = 360° (full)
        
        **Clock Method:**
        - Each hour = 30° (360° ÷ 12)
        - 3 hours = 90° (quarter turn)
        - 6 hours = 180° (half turn)
        - 9 hours = 270° (three-quarter turn)
        - 12 hours = 360° (full turn)
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None
    st.session_state.question_format = None
    st.session_state.answer_options = []  # Clear the stored options