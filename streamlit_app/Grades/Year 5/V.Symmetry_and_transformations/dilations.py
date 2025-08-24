import streamlit as st
import random
import math
import streamlit.components.v1 as components

def run():
    """
    Main function to run the Dilations activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/dilations.py
    """
    # Initialize session state
    if "dilation_difficulty" not in st.session_state:
        st.session_state.dilation_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.user_answer = None
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.recent_problems = []
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("🔍 Dilations")
    st.markdown("*Identify whether a shape is an enlargement or a reduction*")
    st.markdown("---")
    
    # Difficulty and stats display
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Easy (Simple shapes, clear dilations)",
            2: "Medium (Complex shapes, various scales)", 
            3: "Hard (Tricky cases, fractional scales)"
        }
        st.markdown(f"**Difficulty:** {difficulty_text[st.session_state.dilation_difficulty]}")
        progress = (st.session_state.dilation_difficulty - 1) / 2
        st.progress(progress, text=f"Level {st.session_state.dilation_difficulty}/3")
    
    with col2:
        if st.session_state.total_attempted > 0:
            accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
        else:
            st.metric("Accuracy", "---")
    
    with col3:
        st.metric("Streak", st.session_state.consecutive_correct)
    
    with col4:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display the dilation problem
    display_dilation_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### What is Dilation?
        
        **Dilation** is a transformation that changes the size of a shape while keeping its shape the same.
        
        ### Two Types of Dilation:
        
        **🔍 Enlargement**
        - Makes the shape BIGGER
        - Scale factor > 1
        - Example: Scale factor 2 means twice as big
        - All distances from center are multiplied
        
        **🔬 Reduction**
        - Makes the shape SMALLER
        - Scale factor < 1
        - Example: Scale factor 0.5 means half the size
        - All distances from center are divided
        
        ### How to Identify:
        
        1. **Compare sizes**: Is the colored shape bigger or smaller?
        2. **Check distances**: Measure from center to vertices
        3. **Look at coordinates**: Are they multiplied or divided?
        
        ### Scale Factor Quick Guide:
        
        **Enlargements (shape gets bigger):**
        - Scale factor 2 = 2× bigger
        - Scale factor 3 = 3× bigger
        - Scale factor 1.5 = 1.5× bigger
        
        **Reductions (shape gets smaller):**
        - Scale factor 0.5 = 1/2 the size
        - Scale factor 0.25 = 1/4 the size
        - Scale factor 0.33 = 1/3 the size
        
        ### Visual Clues:
        - **Enlargement**: Colored shape surrounds the black shape
        - **Reduction**: Colored shape fits inside the black shape
        - Both shapes have the same center point (usually origin)
        
        ### Remember:
        - The shape doesn't rotate or flip
        - Only the SIZE changes
        - Angles stay the same
        - The shape stays similar (same proportions)
        """)

def generate_new_problem():
    """Generate a new dilation problem"""
    difficulty = st.session_state.dilation_difficulty
    
    # Choose dilation type
    dilation_type = random.choice(["enlargement", "reduction"])
    
    # Define shapes based on difficulty
    if difficulty == 1:  # Easy - simple shapes with clear dilations
        shapes = [
            {
                "name": "square",
                "points": [(2, 2), (2, -2), (-2, -2), (-2, 2)],
                "type": "square"
            },
            {
                "name": "rectangle",
                "points": [(3, 2), (3, -2), (-3, -2), (-3, 2)],
                "type": "rectangle"
            },
            {
                "name": "right_triangle",
                "points": [(0, 0), (4, 0), (0, 3)],
                "type": "triangle"
            },
            {
                "name": "isosceles_triangle",
                "points": [(0, 4), (3, -2), (-3, -2)],
                "type": "triangle"
            },
            {
                "name": "diamond",
                "points": [(0, 3), (2, 0), (0, -3), (-2, 0)],
                "type": "diamond"
            },
            {
                "name": "line_segment",
                "points": [(-3, -3), (3, 3)],
                "type": "line"
            },
            {
                "name": "L_shape",
                "points": [(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)],
                "type": "L_shape"
            },
            {
                "name": "cross",
                "points": [(-1, 2), (1, 2), (1, 1), (2, 1), (2, -1), (1, -1), 
                          (1, -2), (-1, -2), (-1, -1), (-2, -1), (-2, 1), (-1, 1)],
                "type": "cross"
            },
            {
                "name": "pentagon",
                "points": [(0, 3), (3, 1), (2, -2), (-2, -2), (-3, 1)],
                "type": "pentagon"
            },
            {
                "name": "hexagon",
                "points": [(2, 0), (1, 2), (-1, 2), (-2, 0), (-1, -2), (1, -2)],
                "type": "hexagon"
            }
        ]
        
        # Scale factors for easy level
        if dilation_type == "enlargement":
            scale_factors = [2, 3, 2.5]
        else:
            scale_factors = [0.5, 0.33, 0.25]
    
    elif difficulty == 2:  # Medium - more complex shapes
        shapes = [
            {
                "name": "parallelogram",
                "points": [(1, 1), (4, 1), (5, 3), (2, 3)],
                "type": "parallelogram"
            },
            {
                "name": "trapezoid",
                "points": [(1, 0), (3, 0), (4, 3), (0, 3)],
                "type": "trapezoid"
            },
            {
                "name": "kite",
                "points": [(0, 4), (2, 0), (0, -2), (-2, 0)],
                "type": "kite"
            },
            {
                "name": "arrow",
                "points": [(0, 0), (2, 0), (2, -1), (3, 0), (2, 1), (2, 0), (0, 0)],
                "type": "arrow"
            },
            {
                "name": "star_5point",
                "points": [(0, 4), (1, 1), (4, 1), (1.5, -1), (2.5, -4), 
                          (0, -2), (-2.5, -4), (-1.5, -1), (-4, 1), (-1, 1)],
                "type": "star"
            },
            {
                "name": "octagon",
                "points": [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)],
                "type": "octagon"
            },
            {
                "name": "T_shape",
                "points": [(-3, 2), (3, 2), (3, 1), (1, 1), (1, -3), (-1, -3), (-1, 1), (-3, 1)],
                "type": "T_shape"
            },
            {
                "name": "zigzag_line",
                "points": [(-3, -2), (-1, 2), (1, -2), (3, 2)],
                "type": "line"
            },
            {
                "name": "irregular_quad",
                "points": [(1, 2), (3, 1), (2, -2), (-1, -1)],
                "type": "quadrilateral"
            },
            {
                "name": "bowtie",
                "points": [(-2, -2), (0, 0), (-2, 2), (2, 2), (0, 0), (2, -2)],
                "type": "bowtie"
            }
        ]
        
        # Scale factors for medium level
        if dilation_type == "enlargement":
            scale_factors = [1.5, 2, 2.5, 3]
        else:
            scale_factors = [0.5, 0.4, 0.33, 0.6]
    
    else:  # Hard - complex shapes with tricky scale factors
        shapes = [
            {
                "name": "irregular_pentagon",
                "points": [(0, 3), (2, 2), (3, -1), (0, -3), (-3, 0)],
                "type": "pentagon"
            },
            {
                "name": "complex_polygon",
                "points": [(0, 0), (2, 1), (3, 0), (3, -2), (1, -3), (-1, -3), 
                          (-3, -2), (-3, 0), (-2, 1)],
                "type": "polygon"
            },
            {
                "name": "double_triangle",
                "points": [(-3, 0), (0, 3), (3, 0), (0, -3)],
                "type": "double_triangle"
            },
            {
                "name": "gear_shape",
                "points": [(0, 2), (1, 2), (1, 1), (2, 1), (2, 0), (2, -1), 
                          (1, -1), (1, -2), (0, -2), (-1, -2), (-1, -1), (-2, -1), 
                          (-2, 0), (-2, 1), (-1, 1), (-1, 2)],
                "type": "gear"
            },
            {
                "name": "fractal_cross",
                "points": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (1, 2), (1, 3), 
                          (0, 3), (0, 2), (-1, 2), (-1, 1), (0, 1)],
                "type": "fractal"
            },
            {
                "name": "spiral_polygon",
                "points": [(0, 0), (2, 0), (2, 2), (-1, 2), (-1, -1), (3, -1), (3, 3), 
                          (-2, 3), (-2, -2), (4, -2)],
                "type": "spiral"
            },
            {
                "name": "irregular_hexagon",
                "points": [(1, 3), (3, 1), (3, -2), (0, -3), (-3, -1), (-2, 2)],
                "type": "hexagon"
            },
            {
                "name": "asymmetric_shape",
                "points": [(0, 0), (3, 1), (4, 3), (2, 4), (0, 3), (-1, 4), 
                          (-3, 2), (-2, 0), (-1, -2), (1, -1)],
                "type": "asymmetric"
            },
            {
                "name": "concave_polygon",
                "points": [(-2, 2), (2, 2), (2, 0), (0, 1), (-2, 0)],
                "type": "concave"
            },
            {
                "name": "complex_star",
                "points": [(0, 4), (1.5, 1.5), (4, 0), (1.5, -1.5), (0, -4), 
                          (-1.5, -1.5), (-4, 0), (-1.5, 1.5)],
                "type": "star"
            }
        ]
        
        # Scale factors for hard level (including fractional)
        if dilation_type == "enlargement":
            scale_factors = [1.25, 1.5, 1.75, 2.25, 2.75]
        else:
            scale_factors = [0.25, 0.33, 0.4, 0.6, 0.75]
    
    # Select random shape and scale factor
    selected_shape = random.choice(shapes)
    scale_factor = random.choice(scale_factors)
    
    # Apply dilation to create the dilated shape
    dilated_points = []
    for x, y in selected_shape["points"]:
        new_x = x * scale_factor
        new_y = y * scale_factor
        dilated_points.append((new_x, new_y))
    
    # Choose color for dilated shape
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#E91E63", "#9C27B0", "#00BCD4"]
    dilated_color = random.choice(colors)
    
    # Store problem data
    st.session_state.problem_data = {
        "original_shape": selected_shape,
        "dilated_points": dilated_points,
        "dilated_color": dilated_color,
        "scale_factor": scale_factor,
        "correct_answer": dilation_type,
        "color_name": {
            "#2196F3": "blue",
            "#4CAF50": "green",
            "#FF9800": "orange",
            "#E91E63": "pink",
            "#9C27B0": "purple",
            "#00BCD4": "cyan"
        }[dilated_color]
    }
    st.session_state.current_problem = f"{selected_shape['name']}_{dilation_type}_{scale_factor}"

def display_dilation_problem():
    """Display the dilation problem"""
    data = st.session_state.problem_data
    
    # Question text
    color_name = data["color_name"]
    st.markdown(f"### The {color_name} shape is a dilation of the black shape. Is it an enlargement or a reduction?")
    
    # Create coordinate grid with both shapes
    create_dilation_grid(data)
    
    # Display answer options
    if not st.session_state.show_feedback:
        col1, col2 = st.columns(2)
        
        selected = None
        with col1:
            if st.button("🔍 enlargement", key="enlarge_btn", use_container_width=True):
                selected = "enlargement"
        
        with col2:
            if st.button("🔬 reduction", key="reduce_btn", use_container_width=True):
                selected = "reduction"
        
        # Submit button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit", type="primary", use_container_width=True):
                if selected is not None:
                    submit_answer(selected)
                    st.rerun()
                elif "selected_answer" in st.session_state:
                    submit_answer(st.session_state.selected_answer)
                    st.rerun()
                else:
                    st.warning("Please select enlargement or reduction")
        
        # Store selected value if clicked
        if selected is not None:
            st.session_state.selected_answer = selected
            st.rerun()
        
        # Show selection
        if "selected_answer" in st.session_state:
            st.info(f"Selected: **{st.session_state.selected_answer}**")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_for_next_question()
                st.rerun()

def create_dilation_grid(data):
    """Create coordinate grid with original and dilated shapes"""
    original_points = data["original_shape"]["points"]
    dilated_points = data["dilated_points"]
    dilated_color = data["dilated_color"]
    
    # Calculate bounds for the grid
    all_points = original_points + dilated_points
    min_x = min(p[0] for p in all_points) - 2
    max_x = max(p[0] for p in all_points) + 2
    min_y = min(p[1] for p in all_points) - 2
    max_y = max(p[1] for p in all_points) + 2
    
    # Ensure grid is at least -10 to 10
    min_x = min(min_x, -10)
    max_x = max(max_x, 10)
    min_y = min(min_y, -10)
    max_y = max(max_y, 10)
    
    # Create SVG paths for shapes
    def create_path(points):
        if len(points) == 2:  # Line segment
            return f"M {points[0][0]},{-points[0][1]} L {points[1][0]},{-points[1][1]}"
        else:  # Polygon
            path = f"M {points[0][0]},{-points[0][1]}"
            for x, y in points[1:]:
                path += f" L {x},{-y}"
            path += " Z"
            return path
    
    original_path = create_path(original_points)
    dilated_path = create_path(dilated_points)
    
    # Determine if shapes are lines or polygons
    is_line = len(original_points) == 2 or data["original_shape"]["type"] == "line"
    
    # Create the complete HTML with SVG
    html_content = f'''
    <div style="display: flex; justify-content: center; margin: 20px 0;">
        <svg width="500" height="500" viewBox="{min_x} {-max_y} {max_x-min_x} {max_y-min_y}" 
             style="background: white; border: 2px solid #333;">
            
            <!-- Grid lines -->
            <defs>
                <pattern id="smallGrid" width="1" height="1" patternUnits="userSpaceOnUse">
                    <path d="M 1 0 L 0 0 0 1" fill="none" stroke="#e0e0e0" stroke-width="0.05"/>
                </pattern>
                <pattern id="grid" width="5" height="5" patternUnits="userSpaceOnUse">
                    <rect width="5" height="5" fill="url(#smallGrid)"/>
                    <path d="M 5 0 L 0 0 0 5" fill="none" stroke="#ccc" stroke-width="0.1"/>
                </pattern>
            </defs>
            
            <rect x="{min_x}" y="{-max_y}" width="{max_x-min_x}" height="{max_y-min_y}" fill="url(#grid)"/>
            
            <!-- Axes -->
            <line x1="{min_x}" y1="0" x2="{max_x}" y2="0" stroke="#666" stroke-width="0.15"/>
            <line x1="0" y1="{-max_y}" x2="0" y2="{-min_y}" stroke="#666" stroke-width="0.15"/>
            
            <!-- Axis labels -->
            <text x="{max_x-0.5}" y="-0.5" fill="#666" font-size="0.8" font-weight="bold">x</text>
            <text x="0.5" y="{-max_y+1}" fill="#666" font-size="0.8" font-weight="bold">y</text>
            
            <!-- Axis numbers -->
            <text x="0.3" y="0.5" fill="#666" font-size="0.6">0</text>
            <text x="{max_x-1}" y="0.5" fill="#666" font-size="0.6">{int(max_x)}</text>
            <text x="{min_x+0.5}" y="0.5" fill="#666" font-size="0.6">{int(min_x)}</text>
            <text x="0.3" y="{-max_y+1.5}" fill="#666" font-size="0.6">{int(max_y)}</text>
            <text x="0.3" y="{-min_y-0.5}" fill="#666" font-size="0.6">{int(min_y)}</text>
            
            <!-- Grid line markers on axes -->
            {create_axis_markers(min_x, max_x, min_y, max_y)}
            
            <!-- Dilated shape (colored, drawn first so it appears behind) -->
            {f'<path d="{dilated_path}" fill="none" stroke="{dilated_color}" stroke-width="0.3" opacity="0.8"/>' if is_line else f'<path d="{dilated_path}" fill="{dilated_color}" fill-opacity="0.3" stroke="{dilated_color}" stroke-width="0.2"/>'}
            
            <!-- Original shape (black) -->
            {f'<path d="{original_path}" fill="none" stroke="black" stroke-width="0.3"/>' if is_line else f'<path d="{original_path}" fill="none" stroke="black" stroke-width="0.3"/>'}
            
            <!-- Vertices for original shape -->
            {"".join([f'<circle cx="{x}" cy="{-y}" r="0.15" fill="black"/>' for x, y in original_points])}
            
            <!-- Vertices for dilated shape -->
            {"".join([f'<circle cx="{x}" cy="{-y}" r="0.15" fill="{dilated_color}"/>' for x, y in dilated_points])}
        </svg>
    </div>
    '''
    
    components.html(html_content, height=520)

def create_axis_markers(min_x, max_x, min_y, max_y):
    """Create tick marks on axes"""
    markers = ""
    
    # X-axis markers
    for x in range(int(min_x), int(max_x) + 1):
        if x != 0 and x % 5 == 0:
            markers += f'<line x1="{x}" y1="-0.2" x2="{x}" y2="0.2" stroke="#666" stroke-width="0.1"/>'
    
    # Y-axis markers
    for y in range(int(min_y), int(max_y) + 1):
        if y != 0 and y % 5 == 0:
            markers += f'<line x1="-0.2" y1="{-y}" x2="0.2" y2="{-y}" stroke="#666" stroke-width="0.1"/>'
    
    return markers

def submit_answer(user_answer):
    """Process the submitted answer"""
    st.session_state.user_answer = user_answer
    st.session_state.show_feedback = True
    st.session_state.total_attempted += 1
    
    correct_answer = st.session_state.problem_data["correct_answer"]
    
    if user_answer == correct_answer:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3 and st.session_state.dilation_difficulty < 3:
            st.session_state.dilation_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after poor performance
        if st.session_state.dilation_difficulty > 1:
            recent_accuracy = st.session_state.total_correct / max(st.session_state.total_attempted, 1)
            if recent_accuracy < 0.5 and st.session_state.total_attempted >= 3:
                st.session_state.dilation_difficulty -= 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.problem_data
    user_answer = st.session_state.user_answer
    correct_answer = data["correct_answer"]
    scale_factor = data["scale_factor"]
    color_name = data["color_name"]
    
    if user_answer == correct_answer:
        if correct_answer == "enlargement":
            st.success(f"✅ **Correct!** The {color_name} shape is an ENLARGEMENT with scale factor {scale_factor}!")
        else:
            st.success(f"✅ **Correct!** The {color_name} shape is a REDUCTION with scale factor {scale_factor}!")
        
        # Explain why
        if correct_answer == "enlargement":
            st.info(f"""
            📐 **Why it's an enlargement:**
            - The {color_name} shape is LARGER than the black shape
            - Scale factor {scale_factor} means each distance is multiplied by {scale_factor}
            - All points moved AWAY from the center
            """)
        else:
            st.info(f"""
            📐 **Why it's a reduction:**
            - The {color_name} shape is SMALLER than the black shape
            - Scale factor {scale_factor} means each distance is multiplied by {scale_factor}
            - All points moved TOWARD the center
            """)
        
        # Special recognition
        if st.session_state.consecutive_correct == 3:
            st.balloons()
            st.info("🏆 **Excellent streak! Moving to the next level!**")
    
    else:
        st.error(f"❌ **Not quite.** The {color_name} shape is a{'n' if correct_answer == 'enlargement' else ''} {correct_answer.upper()}.")
        
        # Show detailed explanation
        with st.expander("📖 **Understanding dilations**", expanded=True):
            st.markdown(f"""
            ### Let's analyze this dilation:
            
            **Original shape:** Black
            **Dilated shape:** {color_name.capitalize()}
            **Scale factor:** {scale_factor}
            """)
            
            if correct_answer == "enlargement":
                st.markdown(f"""
                ### Why it's an ENLARGEMENT:
                - Scale factor {scale_factor} is **greater than 1**
                - The {color_name} shape is **bigger** than the black shape
                - Each coordinate is **multiplied** by {scale_factor}
                
                **Example calculation:**
                If a point is at (2, 3) in the black shape,
                it becomes ({2 * scale_factor:.1f}, {3 * scale_factor:.1f}) in the {color_name} shape
                """)
            else:
                st.markdown(f"""
                ### Why it's a REDUCTION:
                - Scale factor {scale_factor} is **less than 1**
                - The {color_name} shape is **smaller** than the black shape
                - Each coordinate is **multiplied** by {scale_factor}
                
                **Example calculation:**
                If a point is at (4, 6) in the black shape,
                it becomes ({4 * scale_factor:.1f}, {6 * scale_factor:.1f}) in the {color_name} shape
                """)
            
            st.markdown("""
            ### Remember:
            - **Enlargement** = Scale factor > 1 (shape gets bigger)
            - **Reduction** = Scale factor < 1 (shape gets smaller)
            - **No change** = Scale factor = 1 (same size)
            """)

def reset_for_next_question():
    """Reset state for next question"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.user_answer = None
    if "selected_answer" in st.session_state:
        del st.session_state.selected_answer