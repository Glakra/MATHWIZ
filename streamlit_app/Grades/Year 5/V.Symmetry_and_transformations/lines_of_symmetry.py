import streamlit as st
import random
import math

def run():
    """
    Main function to run the Lines of Symmetry activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/lines_of_symmetry.py
    """
    # Initialize session state
    if "symmetry_difficulty" not in st.session_state:
        st.session_state.symmetry_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_shape" not in st.session_state:
        st.session_state.current_shape = None
        st.session_state.shape_data = {}
        st.session_state.show_feedback = False
        st.session_state.user_answer = None
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.recent_shapes = []  # Track recent shapes to avoid repetition
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("🔄 Lines of Symmetry")
    st.markdown("*Identify whether the dotted line is a line of symmetry*")
    st.markdown("---")
    
    # Difficulty and stats display
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Easy (Simple shapes & objects)",
            2: "Medium (Complex shapes)", 
            3: "Hard (Tricky cases & multiple lines)"
        }
        st.markdown(f"**Difficulty:** {difficulty_text[st.session_state.symmetry_difficulty]}")
        progress = (st.session_state.symmetry_difficulty - 1) / 2
        st.progress(progress, text=f"Level {st.session_state.symmetry_difficulty}/3")
    
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
    
    # Generate new shape if needed
    if st.session_state.current_shape is None:
        generate_new_shape()
    
    # Display the symmetry problem
    display_symmetry_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### What is a Line of Symmetry?
        
        A **line of symmetry** divides a shape into two parts that are:
        - **Exact mirror images** of each other
        - **Perfect reflections** when folded along the line
        - **Identical in size and shape** on both sides
        
        ### How to Check for Symmetry:
        
        1. **Imagine folding** the shape along the dotted line
        2. **Check if both sides** would match exactly
        3. **Look for mirror images** on either side of the line
        4. **Count matching features** (dots, patterns, colors)
        
        ### Quick Test:
        - Can you fold it and have both sides match? → **Yes = Symmetry**
        - Do the sides look different? → **No = Not Symmetry**
        """)

def generate_new_shape():
    """Generate a new shape with or without symmetry"""
    difficulty = st.session_state.symmetry_difficulty
    
    # Define shape scenarios based on difficulty
    if difficulty == 1:  # Easy - simple shapes and objects
        scenarios = [
            # Symmetric cases
            {
                "name": "watermelon",
                "type": "object",
                "has_symmetry": True,
                "line_type": "vertical",
                "description": "A watermelon slice with seeds",
                "explanation": "The vertical line divides the watermelon into two identical halves. Each side has the same shape and seed pattern."
            },
            {
                "name": "heart",
                "type": "shape",
                "has_symmetry": True,
                "line_type": "vertical",
                "description": "A heart shape",
                "explanation": "The vertical line through the center creates two identical halves of the heart."
            },
            {
                "name": "butterfly",
                "type": "object",
                "has_symmetry": True,
                "line_type": "vertical",
                "description": "A butterfly with spread wings",
                "explanation": "Butterflies have natural vertical symmetry - their wings are mirror images."
            },
            {
                "name": "square",
                "type": "shape",
                "has_symmetry": True,
                "line_type": "diagonal",
                "description": "A square with diagonal line",
                "explanation": "A square has diagonal symmetry - it can be folded along the diagonal to match perfectly."
            },
            {
                "name": "circle",
                "type": "shape",
                "has_symmetry": True,
                "line_type": "any",
                "description": "A circle with any line through center",
                "explanation": "A circle has infinite lines of symmetry - any line through its center creates symmetry."
            },
            # Non-symmetric cases
            {
                "name": "letter_F",
                "type": "letter",
                "has_symmetry": False,
                "line_type": "vertical",
                "description": "The letter F",
                "explanation": "The letter F has no symmetry - the horizontal lines are only on the right side."
            },
            {
                "name": "crescent",
                "type": "shape",
                "has_symmetry": False,
                "line_type": "horizontal",
                "description": "A crescent moon",
                "explanation": "A horizontal line does not create symmetry in a crescent - the curves don't match."
            },
            {
                "name": "arrow",
                "type": "shape",
                "has_symmetry": False,
                "line_type": "diagonal",
                "description": "An arrow pointing right",
                "explanation": "A diagonal line doesn't create symmetry in a right-pointing arrow."
            }
        ]
    
    elif difficulty == 2:  # Medium - complex shapes  
        scenarios = [
            # Symmetric cases
            {
                "name": "star",
                "type": "shape",
                "has_symmetry": True,
                "line_type": "vertical",
                "description": "A five-pointed star",
                "explanation": "A five-pointed star has 5 lines of symmetry, including this vertical one."
            },
            {
                "name": "hexagon",
                "type": "shape",
                "has_symmetry": True,
                "line_type": "horizontal",
                "description": "A regular hexagon",
                "explanation": "A regular hexagon has 6 lines of symmetry, including horizontal through opposite vertices."
            },
            {
                "name": "house",
                "type": "object",
                "has_symmetry": True,
                "line_type": "vertical",
                "description": "A simple house with symmetric windows",
                "explanation": "This house has vertical symmetry with matching windows and door placement."
            },
            {
                "name": "robot",
                "type": "object",
                "has_symmetry": True,
                "line_type": "horizontal",
                "description": "A robot figure",
                "explanation": "This robot has horizontal symmetry through its middle."
            },
            # Non-symmetric cases
            {
                "name": "parallelogram",
                "type": "shape",
                "has_symmetry": False,
                "line_type": "vertical",
                "description": "A parallelogram (not rectangle)",
                "explanation": "A parallelogram has no lines of symmetry - the slanted sides prevent any symmetry."
            },
            {
                "name": "scalene_triangle",
                "type": "shape",
                "has_symmetry": False,
                "line_type": "any",
                "description": "A scalene triangle",
                "explanation": "A scalene triangle has no lines of symmetry - all sides and angles are different."
            },
            {
                "name": "letter_N",
                "type": "letter",
                "has_symmetry": False,
                "line_type": "vertical",
                "description": "The letter N",
                "explanation": "The letter N has no vertical symmetry - the diagonal goes in only one direction."
            }
        ]
    
    else:  # Hard - tricky cases
        scenarios = [
            # Tricky symmetric cases
            {
                "name": "rectangle",
                "type": "shape",
                "has_symmetry": False,
                "line_type": "diagonal",
                "description": "A rectangle with diagonal line",
                "explanation": "Rectangles do NOT have diagonal symmetry (only squares do). They only have vertical and horizontal symmetry."
            },
            {
                "name": "rhombus",
                "type": "shape",
                "has_symmetry": True,
                "line_type": "diagonal",
                "description": "A rhombus (diamond)",
                "explanation": "A rhombus has both diagonal lines as lines of symmetry."
            },
            {
                "name": "pentagon",
                "type": "shape",
                "has_symmetry": True,
                "line_type": "vertical",
                "description": "A regular pentagon",
                "explanation": "A regular pentagon has 5 lines of symmetry through each vertex and opposite side."
            },
            {
                "name": "letter_H",
                "type": "letter",
                "has_symmetry": True,
                "line_type": "horizontal",
                "description": "The letter H",
                "explanation": "H has both vertical AND horizontal symmetry - this horizontal line works!"
            },
            # Tricky non-symmetric cases
            {
                "name": "spiral",
                "type": "shape",
                "has_symmetry": False,
                "line_type": "any",
                "description": "A spiral",
                "explanation": "Spirals have no lines of symmetry - they continuously curve in one direction."
            },
            {
                "name": "letter_S",
                "type": "letter",
                "has_symmetry": False,
                "line_type": "horizontal",
                "description": "The letter S",
                "explanation": "S has no symmetry - it curves in opposite directions at top and bottom."
            }
        ]
    
    # Filter out recently used shapes
    available_scenarios = [s for s in scenarios if s['name'] not in st.session_state.recent_shapes]
    
    # If all shapes have been used, reset the recent shapes list
    if not available_scenarios:
        st.session_state.recent_shapes = []
        available_scenarios = scenarios
    
    # Choose a random scenario
    scenario = random.choice(available_scenarios)
    
    # Add to recent shapes (keep last 5)
    st.session_state.recent_shapes.append(scenario['name'])
    if len(st.session_state.recent_shapes) > 5:
        st.session_state.recent_shapes.pop(0)
    
    # Store shape data
    st.session_state.shape_data = scenario
    st.session_state.current_shape = scenario['name']

def display_symmetry_problem():
    """Display the symmetry problem"""
    data = st.session_state.shape_data
    
    # Question text
    st.markdown("### Is the dotted line a line of symmetry?")
    
    # Create the shape visualization
    create_shape_visualization(data)
    
    # Display answer options
    if not st.session_state.show_feedback:
        col1, col2 = st.columns(2)
        
        selected = None
        with col1:
            if st.button("✅ yes", key="yes_btn", use_container_width=True):
                selected = True
        
        with col2:
            if st.button("❌ no", key="no_btn", use_container_width=True):
                selected = False
        
        # Submit button
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
                    st.warning("Please select yes or no")
        
        # Store selected value if clicked
        if selected is not None:
            st.session_state.selected_answer = selected
            st.rerun()
        
        # Show selection
        if "selected_answer" in st.session_state:
            answer_text = "Yes" if st.session_state.selected_answer else "No"
            st.info(f"Selected: **{answer_text}**")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_for_next_question()
                st.rerun()

def create_shape_visualization(data):
    """Create a visual representation of the shape with symmetry line"""
    import streamlit.components.v1 as components
    
    # Get shape properties
    shape_name = data['name']
    line_type = data['line_type']
    
    # Map shape names to creation functions
    shape_creators = {
        'watermelon': create_watermelon_svg,
        'heart': create_heart_svg,
        'butterfly': create_butterfly_svg,
        'square': create_square_svg,
        'circle': create_circle_svg,
        'letter_F': create_letter_f_svg,
        'crescent': create_crescent_svg,
        'arrow': create_arrow_svg,
        'star': create_star_svg,
        'hexagon': create_hexagon_svg,
        'house': create_house_svg,
        'robot': create_robot_svg,
        'parallelogram': create_parallelogram_svg,
        'scalene_triangle': create_scalene_triangle_svg,
        'letter_N': create_letter_n_svg,
        'rectangle': create_rectangle_svg,
        'rhombus': create_rhombus_svg,
        'pentagon': create_pentagon_svg,
        'letter_H': create_letter_h_svg,
        'spiral': create_spiral_svg,
        'letter_S': create_letter_s_svg
    }
    
    # Get the appropriate SVG creator function
    svg_creator = shape_creators.get(shape_name, create_default_svg)
    shape_svg = svg_creator(line_type)
    
    # Create HTML with the shape
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 20px;
                display: flex;
                justify-content: center;
                align-items: center;
                background: white;
                font-family: Arial, sans-serif;
            }}
            svg {{
                background: #fafafa;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        {shape_svg}
    </body>
    </html>
    '''
    
    # Display the shape
    components.html(html_content, height=440, scrolling=False)

# SVG creation functions
def create_watermelon_svg(line_type):
    """Create watermelon slice with symmetry line"""
    line = '<line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>' if line_type == "vertical" else ""
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Watermelon slice -->
        <path d="M 150 200 A 100 100 0 0 0 250 200 Z" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
        <path d="M 160 200 A 80 80 0 0 0 240 200 Z" fill="#F44336"/>
        
        <!-- Seeds -->
        <circle cx="180" cy="180" r="3" fill="black"/>
        <circle cx="220" cy="180" r="3" fill="black"/>
        <circle cx="200" cy="160" r="3" fill="black"/>
        <circle cx="190" cy="170" r="3" fill="black"/>
        <circle cx="210" cy="170" r="3" fill="black"/>
        
        <!-- Symmetry line -->
        {line}
    </svg>
    '''

def create_heart_svg(line_type):
    """Create heart shape with symmetry line"""
    line = '<line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>' if line_type == "vertical" else ""
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Heart shape -->
        <path d="M 200 250 C 150 200, 100 170, 100 140 C 100 110, 130 100, 150 100 C 170 100, 190 110, 200 130 C 210 110, 230 100, 250 100 C 270 100, 300 110, 300 140 C 300 170, 250 200, 200 250 Z" 
              fill="#F44336" stroke="#C62828" stroke-width="2"/>
        
        <!-- Symmetry line -->
        {line}
    </svg>
    '''

def create_butterfly_svg(line_type):
    """Create butterfly with symmetry line"""
    line = '<line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>' if line_type == "vertical" else ""
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Butterfly body -->
        <ellipse cx="200" cy="200" rx="10" ry="40" fill="#795548"/>
        
        <!-- Left wing -->
        <ellipse cx="150" cy="180" rx="40" ry="60" fill="#2196F3" opacity="0.8"/>
        <ellipse cx="150" cy="220" rx="35" ry="40" fill="#03A9F4" opacity="0.8"/>
        
        <!-- Right wing -->
        <ellipse cx="250" cy="180" rx="40" ry="60" fill="#2196F3" opacity="0.8"/>
        <ellipse cx="250" cy="220" rx="35" ry="40" fill="#03A9F4" opacity="0.8"/>
        
        <!-- Wing spots -->
        <circle cx="140" cy="170" r="8" fill="#FFC107"/>
        <circle cx="260" cy="170" r="8" fill="#FFC107"/>
        <circle cx="145" cy="210" r="6" fill="#FFC107"/>
        <circle cx="255" cy="210" r="6" fill="#FFC107"/>
        
        <!-- Symmetry line -->
        {line}
    </svg>
    '''

def create_square_svg(line_type):
    """Create square with symmetry line"""
    if line_type == "diagonal":
        line = '<line x1="150" y1="150" x2="250" y2="250" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>'
    else:
        line = '<line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>'
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Square -->
        <rect x="150" y="150" width="100" height="100" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
        
        <!-- Symmetry line -->
        {line}
    </svg>
    '''

def create_circle_svg(line_type):
    """Create circle with symmetry line"""
    angle = random.randint(0, 180)
    x1 = 200 + 100 * math.cos(math.radians(angle))
    y1 = 200 + 100 * math.sin(math.radians(angle))
    x2 = 200 - 100 * math.cos(math.radians(angle))
    y2 = 200 - 100 * math.sin(math.radians(angle))
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Circle -->
        <circle cx="200" cy="200" r="80" fill="#2196F3" stroke="#1976D2" stroke-width="2"/>
        
        <!-- Symmetry line -->
        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    '''

def create_letter_f_svg(line_type):
    """Create letter F"""
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Letter F -->
        <path d="M 150 120 L 150 280 L 180 280 L 180 220 L 240 220 L 240 190 L 180 190 L 180 150 L 250 150 L 250 120 Z" 
              fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
        
        <!-- Vertical line -->
        <line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    '''

def create_crescent_svg(line_type):
    """Create crescent moon"""
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Crescent -->
        <path d="M 150 150 A 80 80 0 1 0 150 250 A 60 60 0 1 1 150 150" 
              fill="#FFC107" stroke="#F57C00" stroke-width="2"/>
        
        <!-- Horizontal line -->
        <line x1="100" y1="200" x2="300" y2="200" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    '''

def create_arrow_svg(line_type):
    """Create arrow pointing right"""
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Arrow -->
        <path d="M 120 200 L 240 200 L 240 170 L 280 200 L 240 230 L 240 200" 
              fill="#FF5722" stroke="#D84315" stroke-width="2"/>
        
        <!-- Diagonal line -->
        <line x1="150" y1="150" x2="250" y2="250" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    '''

def create_star_svg(line_type):
    """Create five-pointed star"""
    line = '<line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>' if line_type == "vertical" else ""
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Star -->
        <path d="M 200 140 L 220 190 L 270 190 L 230 220 L 250 270 L 200 240 L 150 270 L 170 220 L 130 190 L 180 190 Z" 
              fill="#FFC107" stroke="#F57C00" stroke-width="2"/>
        
        <!-- Symmetry line -->
        {line}
    </svg>
    '''

def create_hexagon_svg(line_type):
    """Create regular hexagon"""
    line = '<line x1="100" y1="200" x2="300" y2="200" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>' if line_type == "horizontal" else ""
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Hexagon -->
        <path d="M 150 200 L 175 150 L 225 150 L 250 200 L 225 250 L 175 250 Z" 
              fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
        
        <!-- Symmetry line -->
        {line}
    </svg>
    '''

def create_house_svg(line_type):
    """Create simple house"""
    line = '<line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>' if line_type == "vertical" else ""
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- House -->
        <rect x="150" y="200" width="100" height="80" fill="#8D6E63" stroke="#5D4037" stroke-width="2"/>
        <path d="M 130 200 L 200 150 L 270 200 Z" fill="#D84315" stroke="#BF360C" stroke-width="2"/>
        <!-- Windows -->
        <rect x="165" y="220" width="25" height="25" fill="#03A9F4"/>
        <rect x="210" y="220" width="25" height="25" fill="#03A9F4"/>
        <!-- Door -->
        <rect x="185" y="250" width="30" height="30" fill="#795548"/>
        
        <!-- Symmetry line -->
        {line}
    </svg>
    '''

def create_robot_svg(line_type):
    """Create robot figure"""
    line = '<line x1="100" y1="200" x2="300" y2="200" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>' if line_type == "horizontal" else ""
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Robot -->
        <rect x="170" y="150" width="60" height="60" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
        <rect x="160" y="210" width="80" height="60" fill="#FF9800" stroke="#E65100" stroke-width="2"/>
        <!-- Eyes -->
        <circle cx="185" cy="170" r="5" fill="white"/>
        <circle cx="215" cy="170" r="5" fill="white"/>
        <!-- Arms -->
        <rect x="140" y="220" width="20" height="40" fill="#FFC107"/>
        <rect x="240" y="220" width="20" height="40" fill="#FFC107"/>
        
        <!-- Symmetry line -->
        {line}
    </svg>
    '''

def create_parallelogram_svg(line_type):
    """Create parallelogram"""
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Parallelogram -->
        <path d="M 150 250 L 250 250 L 270 150 L 170 150 Z" 
              fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
        
        <!-- Vertical line -->
        <line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    '''

def create_scalene_triangle_svg(line_type):
    """Create scalene triangle"""
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Scalene triangle -->
        <path d="M 150 250 L 260 240 L 180 150 Z" 
              fill="#00BCD4" stroke="#00838F" stroke-width="2"/>
        
        <!-- Any line -->
        <line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    '''

def create_letter_n_svg(line_type):
    """Create letter N"""
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Letter N -->
        <path d="M 150 280 L 150 120 L 180 120 L 220 220 L 220 120 L 250 120 L 250 280 L 220 280 L 180 180 L 180 280 Z" 
              fill="#E91E63" stroke="#AD1457" stroke-width="2"/>
        
        <!-- Vertical line -->
        <line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    '''

def create_rectangle_svg(line_type):
    """Create rectangle"""
    if line_type == "diagonal":
        line = '<line x1="120" y1="170" x2="280" y2="230" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>'
    else:
        line = '<line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>'
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Rectangle -->
        <rect x="120" y="170" width="160" height="60" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
        
        <!-- Line -->
        {line}
    </svg>
    '''

def create_rhombus_svg(line_type):
    """Create rhombus"""
    if line_type == "diagonal":
        line = '<line x1="150" y1="200" x2="250" y2="200" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>'
    else:
        line = '<line x1="200" y1="150" x2="200" y2="250" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>'
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Rhombus -->
        <path d="M 200 150 L 250 200 L 200 250 L 150 200 Z" 
              fill="#FF5722" stroke="#D84315" stroke-width="2"/>
        
        <!-- Line -->
        {line}
    </svg>
    '''

def create_pentagon_svg(line_type):
    """Create regular pentagon"""
    line = '<line x1="200" y1="100" x2="200" y2="300" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>' if line_type == "vertical" else ""
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Pentagon -->
        <path d="M 200 150 L 240 180 L 225 220 L 175 220 L 160 180 Z" 
              fill="#673AB7" stroke="#4527A0" stroke-width="2"/>
        
        <!-- Line -->
        {line}
    </svg>
    '''

def create_letter_h_svg(line_type):
    """Create letter H"""
    line = '<line x1="100" y1="200" x2="300" y2="200" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>' if line_type == "horizontal" else ""
    
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Letter H -->
        <path d="M 150 120 L 150 280 L 180 280 L 180 215 L 220 215 L 220 280 L 250 280 L 250 120 L 220 120 L 220 185 L 180 185 L 180 120 Z" 
              fill="#3F51B5" stroke="#283593" stroke-width="2"/>
        
        <!-- Line -->
        {line}
    </svg>
    '''

def create_spiral_svg(line_type):
    """Create spiral"""
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Spiral -->
        <path d="M 200 200 A 20 20 0 0 1 220 220 A 40 40 0 0 1 160 240 A 60 60 0 0 1 140 180 A 80 80 0 0 1 260 160" 
              fill="none" stroke="#795548" stroke-width="3"/>
        
        <!-- Any line -->
        <line x1="150" y1="150" x2="250" y2="250" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    '''

def create_letter_s_svg(line_type):
    """Create letter S"""
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Letter S -->
        <path d="M 240 150 Q 250 120, 200 120 Q 150 120, 150 150 Q 150 180, 200 180 Q 250 180, 250 220 Q 250 250, 200 250 Q 150 250, 160 220" 
              fill="none" stroke="#4CAF50" stroke-width="20" stroke-linecap="round"/>
        
        <!-- Horizontal line -->
        <line x1="100" y1="200" x2="300" y2="200" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    '''

def create_default_svg(line_type):
    """Create default shape"""
    return f'''
    <svg width="400" height="400" viewBox="0 0 400 400">
        <!-- Default shape -->
        <rect x="150" y="150" width="100" height="100" fill="#9E9E9E" stroke="#616161" stroke-width="2"/>
        
        <!-- Line -->
        <line x1="100" y1="200" x2="300" y2="200" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>
    </svg>
    '''

def submit_answer(user_answer):
    """Process the submitted answer"""
    st.session_state.user_answer = user_answer
    st.session_state.show_feedback = True
    st.session_state.total_attempted += 1
    
    correct_answer = st.session_state.shape_data['has_symmetry']
    
    if user_answer == correct_answer:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3 and st.session_state.symmetry_difficulty < 3:
            st.session_state.symmetry_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after poor performance
        if st.session_state.symmetry_difficulty > 1:
            recent_accuracy = st.session_state.total_correct / max(st.session_state.total_attempted, 1)
            if recent_accuracy < 0.5 and st.session_state.total_attempted >= 3:
                st.session_state.symmetry_difficulty -= 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.shape_data
    user_answer = st.session_state.user_answer
    correct_answer = data['has_symmetry']
    
    if user_answer == correct_answer:
        if correct_answer:
            st.success(f"✅ **Correct!** Yes, the dotted line IS a line of symmetry!")
        else:
            st.success(f"✅ **Correct!** No, the dotted line is NOT a line of symmetry!")
        
        # Show explanation
        st.info(f"📐 **{data['description']}**: {data['explanation']}")
        
        # Special recognition
        if st.session_state.consecutive_correct == 3:
            st.balloons()
            st.info("🏆 **Excellent streak! Moving to the next level!**")
    else:
        if correct_answer:
            st.error(f"❌ **Not quite.** The dotted line IS a line of symmetry.")
        else:
            st.error(f"❌ **Not quite.** The dotted line is NOT a line of symmetry.")
        
        # Show detailed explanation
        with st.expander("📖 **Understanding this symmetry**", expanded=True):
            st.markdown(f"""
            ### Shape: {data['description']}
            
            **Explanation:** {data['explanation']}
            
            ### Remember:
            - A line of symmetry creates **exact mirror images**
            - Both sides must be **identical** when folded
            - Even small differences mean **no symmetry**
            
            ### Quick Test:
            Imagine folding the shape along the dotted line:
            - Do both halves match perfectly? → **Line of symmetry**
            - Are there any differences? → **Not a line of symmetry**
            """)

def reset_for_next_question():
    """Reset state for next question"""
    st.session_state.current_shape = None
    st.session_state.shape_data = {}
    st.session_state.show_feedback = False
    st.session_state.user_answer = None
    if "selected_answer" in st.session_state:
        del st.session_state.selected_answer