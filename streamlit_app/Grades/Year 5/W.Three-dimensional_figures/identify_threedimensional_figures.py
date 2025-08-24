import streamlit as st
import random

def run():
    """
    Main function to run the Identify 3D Figures activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/O. Two-dimensional figures/identify_three_dimensional_figures.py
    """
    
    # Initialize session state for difficulty and tracking
    if "identify_3d_difficulty" not in st.session_state:
        st.session_state.identify_3d_difficulty = 1
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    if "current_3d_question" not in st.session_state:
        st.session_state.current_3d_question = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.selected_answer = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > W. Three-dimensional figures**")
    st.title("🎯 Identify Three-dimensional Figures")
    st.markdown("*Learn to recognize and name 3D shapes*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty = st.session_state.identify_3d_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic Shapes",
            2: "More Shapes", 
            3: "Complex Shapes",
            4: "Real-world Objects",
            5: "Advanced Concepts"
        }
        st.markdown(f"**Current Level:** {difficulty} - {difficulty_names.get(difficulty, 'Basic')}")
        progress = (difficulty - 1) / 4
        st.progress(progress, text=f"Level {difficulty}/5")
    
    with col2:
        if difficulty <= 2:
            st.markdown("**🟢 Beginner**")
        elif difficulty <= 3:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_3d_question is None:
        st.session_state.current_3d_question = generate_3d_question(difficulty)
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.selected_answer = None
    
    # Display the question
    display_3d_question()
    
    # Handle feedback and progression
    handle_3d_feedback()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Shape Properties**", expanded=False):
        st.markdown("""
        ### 📚 3D Shape Properties:
        
        **Basic Shapes:**
        - **Sphere** 🌐: Perfectly round like a ball
        - **Cylinder** 🥫: Two circular bases with curved sides (like a can)
        - **Cone** 🍦: Circular base coming to a point
        - **Cube** 🎲: 6 square faces, all edges equal
        - **Pyramid** 🔺: Polygon base with triangular faces meeting at apex
        
        **Prisms:**
        - **Rectangular Prism** 📦: 6 rectangular faces (like a box)
        - **Triangular Prism** ⛺: Two triangular bases, three rectangular faces
        - **Hexagonal Prism** 🔩: Two hexagonal bases, six rectangular faces
        
        **Special Shapes:**
        - **Octahedron** 💎: 8 triangular faces
        - **Dodecahedron** ⚽: 12 pentagonal faces  
        - **Icosahedron** 🎯: 20 triangular faces
        - **Torus** 🍩: Donut shape
        
        ### 🎯 Level Progression:
        - **Level 1**: Basic shapes (sphere, cone, cylinder, cube)
        - **Level 2**: More shapes (various prisms and pyramids)
        - **Level 3**: Complex polyhedra and wireframes
        - **Level 4**: Real-world objects made of shapes
        - **Level 5**: Advanced concepts (cross-sections, nets)
        
        ### 💡 Tips:
        - Look for the **base shape** (circle, square, triangle, etc.)
        - Count the **faces** (flat surfaces)
        - Check if it has **curved surfaces**
        - Notice if faces are **identical** (prisms) or **meet at a point** (pyramids)
        """)

def generate_3d_question(difficulty):
    """Generate a 3D shape identification question based on difficulty"""
    
    if difficulty == 1:
        # Level 1: Basic shapes
        shapes = [
            {
                "name": "sphere",
                "svg": create_sphere_svg("#FFD4B3"),
                "options": ["sphere", "cone", "cylinder", "cube"],
                "explanation": "This is a sphere - a perfectly round 3D shape like a ball. All points on its surface are the same distance from the center."
            },
            {
                "name": "cone",
                "svg": create_cone_svg("#A8D5A8"),
                "options": ["cone", "cylinder", "pyramid", "sphere"],
                "explanation": "This is a cone - it has a circular base and comes to a point (apex) at the top."
            },
            {
                "name": "cylinder",
                "svg": create_cylinder_svg("#B3D9FF"),
                "options": ["cylinder", "cone", "rectangular prism", "sphere"],
                "explanation": "This is a cylinder - it has two circular bases connected by a curved surface, like a can."
            },
            {
                "name": "cube",
                "svg": create_cube_svg("#FFB3B3"),
                "options": ["cube", "rectangular prism", "pyramid", "sphere"],
                "explanation": "This is a cube - all 6 faces are squares and all 12 edges are equal length."
            },
            {
                "name": "pyramid",
                "svg": create_pyramid_svg("#E6B3FF"),
                "options": ["pyramid", "cone", "prism", "cube"],
                "explanation": "This is a pyramid - it has a square base with 4 triangular faces meeting at a point."
            }
        ]
    
    elif difficulty == 2:
        # Level 2: More shapes and prisms
        shapes = [
            {
                "name": "rectangular prism",
                "svg": create_rectangular_prism_svg("#FFE6B3"),
                "options": ["rectangular prism", "cube", "pyramid", "cylinder"],
                "explanation": "This is a rectangular prism - like a box with 6 rectangular faces."
            },
            {
                "name": "triangular prism",
                "svg": create_triangular_prism_svg("#B3FFE6"),
                "options": ["triangular prism", "pyramid", "cone", "rectangular prism"],
                "explanation": "This is a triangular prism - it has 2 triangular bases connected by 3 rectangular faces."
            },
            {
                "name": "hexagonal prism",
                "svg": create_hexagonal_prism_svg("#FFB3D4"),
                "options": ["hexagonal prism", "cylinder", "octagonal prism", "pyramid"],
                "explanation": "This is a hexagonal prism - it has 2 hexagonal bases connected by 6 rectangular faces."
            },
            {
                "name": "pentagonal pyramid",
                "svg": create_pentagonal_pyramid_svg("#D4B3FF"),
                "options": ["pentagonal pyramid", "triangular pyramid", "cone", "hexagonal pyramid"],
                "explanation": "This is a pentagonal pyramid - it has a pentagon base with 5 triangular faces."
            },
            {
                "name": "octahedron",
                "svg": create_octahedron_svg("#B3D4FF"),
                "options": ["octahedron", "pyramid", "diamond", "cube"],
                "explanation": "This is an octahedron - it has 8 triangular faces, like two pyramids joined at their bases."
            }
        ]
    
    elif difficulty == 3:
        # Level 3: Complex shapes and wireframes
        shapes = [
            {
                "name": "sphere",
                "svg": create_sphere_wireframe("#4A90E2"),
                "options": ["sphere", "ellipsoid", "cylinder", "torus"],
                "explanation": "This wireframe shows a sphere with latitude and longitude lines, like a globe."
            },
            {
                "name": "torus",
                "svg": create_torus_svg("#E94B3C"),
                "options": ["torus", "cylinder", "sphere", "ring"],
                "explanation": "This is a torus - a donut-shaped figure formed by rotating a circle around an axis."
            },
            {
                "name": "dodecahedron",
                "svg": create_dodecahedron_svg("#6ACC65"),
                "options": ["dodecahedron", "icosahedron", "octahedron", "hexagonal prism"],
                "explanation": "This is a dodecahedron - it has 12 pentagonal faces and is one of the Platonic solids."
            },
            {
                "name": "icosahedron", 
                "svg": create_icosahedron_svg("#FFA500"),
                "options": ["icosahedron", "dodecahedron", "octahedron", "pyramid"],
                "explanation": "This is an icosahedron - it has 20 triangular faces and is one of the Platonic solids."
            },
            {
                "name": "truncated cone",
                "svg": create_truncated_cone_svg("#9B59B6"),
                "options": ["truncated cone", "cylinder", "cone", "truncated pyramid"],
                "explanation": "This is a truncated cone (frustum) - a cone with the top cut off parallel to the base."
            }
        ]
    
    elif difficulty == 4:
        # Level 4: Real-world objects
        shapes = [
            {
                "name": "rectangular prism and triangular prism",
                "svg": create_house_svg(),
                "question": "This house is made of which two 3D shapes?",
                "options": ["rectangular prism and triangular prism", "cube and pyramid", "cylinder and cone", "two rectangular prisms"],
                "explanation": "The house has a rectangular prism for the main structure and a triangular prism for the roof."
            },
            {
                "name": "hemisphere and cone",
                "svg": create_ice_cream_svg(),
                "question": "An ice cream cone combines which shapes?",
                "options": ["hemisphere and cone", "sphere and cylinder", "sphere and pyramid", "cylinder and cone"],
                "explanation": "Ice cream is typically a hemisphere (half sphere) on top of a cone."
            },
            {
                "name": "cylinder and cone",
                "svg": create_pencil_svg(),
                "question": "A pencil combines which shapes?",
                "options": ["cylinder and cone", "rectangular prism and pyramid", "cylinder and pyramid", "prism and cone"],
                "explanation": "A pencil has a cylindrical body with a cone-shaped sharpened tip."
            },
            {
                "name": "cube",
                "svg": create_dice_svg(),
                "question": "What 3D shape is a standard die?",
                "options": ["cube", "rectangular prism", "octahedron", "square pyramid"],
                "explanation": "A standard die is a cube with dots on each of its 6 square faces."
            },
            {
                "name": "truncated icosahedron",
                "svg": create_soccer_ball_svg(),
                "question": "A soccer ball approximates which shape?",
                "options": ["truncated icosahedron", "sphere", "dodecahedron", "icosahedron"],
                "explanation": "A soccer ball is made of pentagons and hexagons forming a truncated icosahedron."
            }
        ]
    
    else:  # difficulty 5+
        # Level 5: Advanced concepts
        shapes = [
            {
                "name": "cylinder or sphere",
                "svg": create_cross_section_circle(),
                "question": "A circular cross-section could come from cutting which shape?",
                "options": ["cylinder or sphere", "cube", "pyramid", "rectangular prism"],
                "explanation": "A circular cross-section can result from cutting through a cylinder or sphere horizontally."
            },
            {
                "name": "cube",
                "svg": create_net_cube(),
                "question": "This net folds into which 3D shape?",
                "options": ["cube", "rectangular prism", "pyramid", "octahedron"],
                "explanation": "This cross-shaped net of 6 squares folds into a cube."
            },
            {
                "name": "L-shaped prism",
                "svg": create_orthographic_views(),
                "question": "These views (top, front, side) represent which shape?",
                "options": ["L-shaped prism", "rectangular prism", "triangular prism", "cube"],
                "explanation": "The different orthographic views show an L-shaped prism."
            },
            {
                "name": "oblique cylinder",
                "svg": create_oblique_cylinder_svg(),
                "question": "What type of cylinder is this?",
                "options": ["oblique cylinder", "right cylinder", "truncated cylinder", "elliptical cylinder"],
                "explanation": "This is an oblique cylinder - its axis is not perpendicular to the base."
            },
            {
                "name": "tetrahedron",
                "svg": create_tetrahedron_svg(),
                "question": "This shape with 4 triangular faces is called?",
                "options": ["tetrahedron", "pyramid", "octahedron", "triangular prism"],
                "explanation": "This is a tetrahedron - the simplest 3D shape with 4 triangular faces."
            }
        ]
    
    selected = random.choice(shapes)
    selected["difficulty"] = difficulty
    
    # Set default question if not specified
    if "question" not in selected:
        selected["question"] = "What shape is this?"
    
    # RANDOMIZE THE OPTIONS ORDER
    correct_answer = selected["options"][0]  # Store the correct answer (always first initially)
    shuffled_options = selected["options"].copy()
    random.shuffle(shuffled_options)  # Shuffle the options
    selected["shuffled_options"] = shuffled_options
    selected["correct_answer"] = correct_answer  # Store the correct answer separately
    
    return selected

def display_3d_question():
    """Display the current 3D shape question"""
    question_data = st.session_state.current_3d_question
    
    # Display question
    st.markdown(f"### 📝 {question_data['question']}")
    
    # Display the SVG shape
    st.markdown(question_data['svg'], unsafe_allow_html=True)
    
    # Create answer options as clickable tiles if not already submitted
    if not st.session_state.answer_submitted:
        st.markdown("**Choose your answer:**")
        
        # Create a 2x2 grid of buttons for the options
        cols = st.columns(2)
        
        for i, option in enumerate(question_data['shuffled_options']):
            col_index = i % 2
            with cols[col_index]:
                # Create a button styled as a tile
                button_style = """
                <style>
                div.stButton > button {
                    width: 100%;
                    height: 80px;
                    font-size: 16px;
                    font-weight: 500;
                    margin: 5px 0;
                    border-radius: 10px;
                    border: 2px solid #e0e0e0;
                    background-color: white;
                    color: #333;
                    transition: all 0.3s;
                }
                div.stButton > button:hover {
                    border-color: #1f77b4;
                    background-color: #f0f8ff;
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }
                </style>
                """
                st.markdown(button_style, unsafe_allow_html=True)
                
                # Create button with emoji icons for visual appeal
                shape_emojis = {
                    "sphere": "🌐",
                    "cone": "🍦",
                    "cylinder": "🥫",
                    "cube": "🎲",
                    "pyramid": "🔺",
                    "rectangular prism": "📦",
                    "triangular prism": "⛺",
                    "hexagonal prism": "🔩",
                    "octahedron": "💎",
                    "dodecahedron": "⚽",
                    "icosahedron": "🎯",
                    "torus": "🍩",
                    "tetrahedron": "▲",
                    "truncated cone": "⏸️",
                    "oblique cylinder": "🔧",
                    "pentagonal pyramid": "⭐",
                    "truncated icosahedron": "⚽",
                    "hemisphere and cone": "🍦",
                    "cylinder and cone": "✏️",
                    "L-shaped prism": "🔲",
                    "rectangular prism and triangular prism": "🏠",
                    "cylinder or sphere": "⭕"
                }
                
                # Get emoji or use default
                emoji = shape_emojis.get(option.split(" and ")[0], "🔷")
                
                if st.button(f"{emoji} {option}", key=f"option_{i}", use_container_width=True):
                    st.session_state.selected_answer = option
                    st.session_state.answer_submitted = True
                    st.session_state.show_feedback = True
                    st.rerun()

def handle_3d_feedback():
    """Handle feedback and next question"""
    if st.session_state.show_feedback and st.session_state.answer_submitted:
        question_data = st.session_state.current_3d_question
        user_answer = st.session_state.selected_answer
        correct_answer = question_data['correct_answer']  # Use the stored correct answer
        
        # Check if answer is correct
        is_correct = user_answer == correct_answer
        
        if is_correct:
            st.success("🎉 **Excellent! That's correct!**")
            st.info(f"✨ {question_data['explanation']}")
            
            # Update stats
            st.session_state.total_correct += 1
            st.session_state.consecutive_correct += 1
            
            # Check for level up
            if st.session_state.consecutive_correct >= 3:
                old_difficulty = st.session_state.identify_3d_difficulty
                st.session_state.identify_3d_difficulty = min(5, old_difficulty + 1)
                st.session_state.consecutive_correct = 0
                
                if st.session_state.identify_3d_difficulty > old_difficulty:
                    st.balloons()
                    st.success(f"🎯 **Level Up! You're now on Level {st.session_state.identify_3d_difficulty}!**")
        
        else:
            st.error(f"❌ **Not quite. The correct answer is: {correct_answer}**")
            st.warning(f"📚 {question_data['explanation']}")
            
            # Reset consecutive correct
            st.session_state.consecutive_correct = 0
            
            # Show what the user selected
            st.info(f"You selected: **{user_answer}**")
        
        st.session_state.total_attempted += 1
        
        # Show statistics
        if st.session_state.total_attempted > 0:
            accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
            st.markdown(f"**📊 Stats:** {st.session_state.total_correct}/{st.session_state.total_attempted} correct ({accuracy:.0f}%)")
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                st.session_state.current_3d_question = None
                st.session_state.show_feedback = False
                st.session_state.answer_submitted = False
                st.session_state.selected_answer = None
                st.rerun()

# ============ ALL SVG CREATION FUNCTIONS ============

def create_sphere_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <defs>
                <radialGradient id="sphereGrad">
                    <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{color};stop-opacity:0.6" />
                </radialGradient>
            </defs>
            <circle cx="125" cy="125" r="80" fill="url(#sphereGrad)" stroke="#333" stroke-width="2"/>
            <ellipse cx="125" cy="125" rx="80" ry="25" fill="none" stroke="#666" stroke-width="1" stroke-dasharray="2,2" opacity="0.5"/>
        </svg>
    </div>
    '''

def create_cone_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <defs>
                <linearGradient id="coneGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:{color};stop-opacity:0.8" />
                    <stop offset="50%" style="stop-color:{color};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{color};stop-opacity:0.8" />
                </linearGradient>
            </defs>
            <ellipse cx="125" cy="200" rx="70" ry="20" fill="{color}" opacity="0.6"/>
            <path d="M 125 50 L 55 200 L 195 200 Z" fill="url(#coneGrad)" stroke="#333" stroke-width="2"/>
            <path d="M 55 200 Q 125 220 195 200" fill="{color}" stroke="#333" stroke-width="2"/>
        </svg>
    </div>
    '''

def create_cylinder_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <defs>
                <linearGradient id="cylGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:{color};stop-opacity:0.7" />
                    <stop offset="50%" style="stop-color:{color};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{color};stop-opacity:0.7" />
                </linearGradient>
            </defs>
            <ellipse cx="125" cy="70" rx="60" ry="20" fill="{color}" stroke="#333" stroke-width="2"/>
            <rect x="65" y="70" width="120" height="110" fill="url(#cylGrad)"/>
            <ellipse cx="125" cy="180" rx="60" ry="20" fill="{color}" stroke="#333" stroke-width="2"/>
        </svg>
    </div>
    '''

def create_cube_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <g transform="translate(125,125)">
                <!-- Back face -->
                <path d="M -40,-40 L 40,-40 L 40,40 L -40,40 Z" 
                      fill="{color}" opacity="0.6" stroke="#333" stroke-width="2"
                      transform="translate(15,15)"/>
                <!-- Front face -->
                <path d="M -40,-40 L 40,-40 L 40,40 L -40,40 Z" 
                      fill="{color}" stroke="#333" stroke-width="2"
                      transform="translate(-15,-15)"/>
                <!-- Connecting edges -->
                <line x1="-55" y1="-55" x2="-25" y2="-25" stroke="#333" stroke-width="2"/>
                <line x1="25" y1="-55" x2="55" y2="-25" stroke="#333" stroke-width="2"/>
                <line x1="25" y1="25" x2="55" y2="55" stroke="#333" stroke-width="2"/>
                <line x1="-55" y1="25" x2="-25" y2="55" stroke="#333" stroke-width="2"/>
            </g>
        </svg>
    </div>
    '''

def create_pyramid_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <!-- Base -->
            <path d="M 70,180 L 180,180 L 160,200 L 50,200 Z" 
                  fill="{color}" opacity="0.5" stroke="#333" stroke-width="2"/>
            <!-- Front face -->
            <path d="M 125,50 L 50,200 L 160,200 Z" 
                  fill="{color}" opacity="0.8" stroke="#333" stroke-width="2"/>
            <!-- Right face -->
            <path d="M 125,50 L 160,200 L 180,180 Z" 
                  fill="{color}" opacity="0.6" stroke="#333" stroke-width="2"/>
            <!-- Back edge -->
            <line x1="125" y1="50" x2="70" y2="180" stroke="#333" stroke-width="2" stroke-dasharray="3,3"/>
        </svg>
    </div>
    '''

def create_rectangular_prism_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <g transform="translate(125,125)">
                <!-- Back face -->
                <path d="M -60,-30 L 60,-30 L 60,30 L -60,30 Z" 
                      fill="{color}" opacity="0.6" stroke="#333" stroke-width="2"
                      transform="translate(15,15)"/>
                <!-- Front face -->
                <path d="M -60,-30 L 60,-30 L 60,30 L -60,30 Z" 
                      fill="{color}" stroke="#333" stroke-width="2"
                      transform="translate(-15,-15)"/>
                <!-- Connecting edges -->
                <line x1="-75" y1="-45" x2="-45" y2="-15" stroke="#333" stroke-width="2"/>
                <line x1="45" y1="-45" x2="75" y2="-15" stroke="#333" stroke-width="2"/>
                <line x1="45" y1="15" x2="75" y2="45" stroke="#333" stroke-width="2"/>
                <line x1="-75" y1="15" x2="-45" y2="45" stroke="#333" stroke-width="2"/>
            </g>
        </svg>
    </div>
    '''

def create_triangular_prism_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <!-- Front triangle -->
            <path d="M 60,180 L 125,80 L 190,180 Z" 
                  fill="{color}" stroke="#333" stroke-width="2"/>
            <!-- Back triangle -->
            <path d="M 80,160 L 145,60 L 210,160 Z" 
                  fill="{color}" opacity="0.6" stroke="#333" stroke-width="2"/>
            <!-- Connecting edges -->
            <line x1="60" y1="180" x2="80" y2="160" stroke="#333" stroke-width="2"/>
            <line x1="125" y1="80" x2="145" y2="60" stroke="#333" stroke-width="2"/>
            <line x1="190" y1="180" x2="210" y2="160" stroke="#333" stroke-width="2"/>
        </svg>
    </div>
    '''

def create_hexagonal_prism_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <g transform="translate(125,125)">
                <!-- Front hexagon -->
                <path d="M -40,0 L -20,-35 L 20,-35 L 40,0 L 20,35 L -20,35 Z" 
                      fill="{color}" stroke="#333" stroke-width="2"/>
                <!-- Back hexagon -->
                <path d="M -40,0 L -20,-35 L 20,-35 L 40,0 L 20,35 L -20,35 Z" 
                      fill="{color}" opacity="0.6" stroke="#333" stroke-width="2"
                      transform="translate(20,20)"/>
                <!-- Connecting edges -->
                <line x1="-40" y1="0" x2="-20" y2="20" stroke="#333" stroke-width="2"/>
                <line x1="40" y1="0" x2="60" y2="20" stroke="#333" stroke-width="2"/>
                <line x1="20" y1="35" x2="40" y2="55" stroke="#333" stroke-width="2"/>
            </g>
        </svg>
    </div>
    '''

def create_pentagonal_pyramid_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <!-- Base pentagon -->
            <path d="M 125,190 L 85,170 L 100,130 L 150,130 L 165,170 Z" 
                  fill="{color}" opacity="0.5" stroke="#333" stroke-width="2"/>
            <!-- Faces -->
            <path d="M 125,60 L 85,170 L 125,190 Z" fill="{color}" opacity="0.8" stroke="#333" stroke-width="2"/>
            <path d="M 125,60 L 125,190 L 165,170 Z" fill="{color}" opacity="0.7" stroke="#333" stroke-width="2"/>
            <path d="M 125,60 L 165,170 L 150,130 Z" fill="{color}" opacity="0.6" stroke="#333" stroke-width="2"/>
            <!-- Hidden edges -->
            <line x1="125" y1="60" x2="100" y2="130" stroke="#333" stroke-width="1" stroke-dasharray="2,2"/>
            <line x1="125" y1="60" x2="150" y2="130" stroke="#333" stroke-width="1" stroke-dasharray="2,2"/>
        </svg>
    </div>
    '''

def create_octahedron_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <g transform="translate(125,125)">
                <!-- Top pyramid -->
                <path d="M 0,-60 L -50,0 L 0,0 Z" fill="{color}" opacity="0.8" stroke="#333" stroke-width="2"/>
                <path d="M 0,-60 L 0,0 L 50,0 Z" fill="{color}" opacity="0.7" stroke="#333" stroke-width="2"/>
                <path d="M 0,-60 L 50,0 L 0,30 Z" fill="{color}" opacity="0.6" stroke="#333" stroke-width="2"/>
                <path d="M 0,-60 L 0,30 L -50,0 Z" fill="{color}" opacity="0.9" stroke="#333" stroke-width="2"/>
                <!-- Bottom pyramid -->
                <path d="M 0,60 L -50,0 L 0,0 Z" fill="{color}" opacity="0.5" stroke="#333" stroke-width="2"/>
                <path d="M 0,60 L 0,0 L 50,0 Z" fill="{color}" opacity="0.4" stroke="#333" stroke-width="2"/>
            </g>
        </svg>
    </div>
    '''

def create_sphere_wireframe(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <circle cx="125" cy="125" r="80" fill="none" stroke="{color}" stroke-width="2"/>
            <ellipse cx="125" cy="125" rx="80" ry="25" fill="none" stroke="{color}" stroke-width="1"/>
            <ellipse cx="125" cy="125" rx="80" ry="50" fill="none" stroke="{color}" stroke-width="1"/>
            <ellipse cx="125" cy="125" rx="25" ry="80" fill="none" stroke="{color}" stroke-width="1"/>
            <ellipse cx="125" cy="125" rx="50" ry="80" fill="none" stroke="{color}" stroke-width="1"/>
            <line x1="45" y1="125" x2="205" y2="125" stroke="{color}" stroke-width="1"/>
            <line x1="125" y1="45" x2="125" y2="205" stroke="{color}" stroke-width="1"/>
        </svg>
    </div>
    '''

def create_torus_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <ellipse cx="125" cy="125" rx="70" ry="35" fill="none" stroke="{color}" stroke-width="20" stroke-linecap="round"/>
            <ellipse cx="125" cy="125" rx="70" ry="35" fill="none" stroke="white" stroke-width="10"/>
            <path d="M 55,125 Q 125,160 195,125" fill="none" stroke="{color}" stroke-width="20" stroke-linecap="round"/>
        </svg>
    </div>
    '''

def create_dodecahedron_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <g transform="translate(125,125)">
                <!-- Front pentagon -->
                <path d="M 0,-50 L -48,-15 L -30,40 L 30,40 L 48,-15 Z" 
                      fill="{color}" stroke="#333" stroke-width="2"/>
                <!-- Visible side pentagons -->
                <path d="M 48,-15 L 30,40 L 60,30 L 70,-10 L 50,-30 Z" 
                      fill="{color}" opacity="0.7" stroke="#333" stroke-width="2"/>
                <path d="M -48,-15 L -50,-30 L -70,-10 L -60,30 L -30,40 Z" 
                      fill="{color}" opacity="0.8" stroke="#333" stroke-width="2"/>
                <!-- Top pentagon -->
                <path d="M 0,-50 L -48,-15 L -50,-30 L 0,-60 L 50,-30 L 48,-15 Z" 
                      fill="{color}" opacity="0.6" stroke="#333" stroke-width="2"/>
            </g>
        </svg>
    </div>
    '''

def create_icosahedron_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <g transform="translate(125,125)">
                <!-- Multiple triangular faces -->
                <path d="M 0,-60 L -35,-20 L 35,-20 Z" fill="{color}" stroke="#333" stroke-width="2"/>
                <path d="M -35,-20 L -50,20 L 0,0 Z" fill="{color}" opacity="0.8" stroke="#333" stroke-width="2"/>
                <path d="M 35,-20 L 0,0 L 50,20 Z" fill="{color}" opacity="0.7" stroke="#333" stroke-width="2"/>
                <path d="M 0,0 L -50,20 L -20,50 Z" fill="{color}" opacity="0.6" stroke="#333" stroke-width="2"/>
                <path d="M 0,0 L 20,50 L 50,20 Z" fill="{color}" opacity="0.65" stroke="#333" stroke-width="2"/>
                <path d="M -20,50 L 20,50 L 0,60 Z" fill="{color}" opacity="0.5" stroke="#333" stroke-width="2"/>
            </g>
        </svg>
    </div>
    '''

def create_truncated_cone_svg(color):
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <defs>
                <linearGradient id="frustumGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:{color};stop-opacity:0.7" />
                    <stop offset="50%" style="stop-color:{color};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{color};stop-opacity:0.7" />
                </linearGradient>
            </defs>
            <ellipse cx="125" cy="80" rx="40" ry="15" fill="{color}" stroke="#333" stroke-width="2"/>
            <path d="M 85,80 L 65,180 L 185,180 L 165,80" fill="url(#frustumGrad)" stroke="#333" stroke-width="2"/>
            <ellipse cx="125" cy="180" rx="60" ry="20" fill="{color}" stroke="#333" stroke-width="2"/>
        </svg>
    </div>
    '''

def create_house_svg():
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <!-- House body (rectangular prism) -->
            <rect x="60" y="120" width="130" height="100" fill="#D2691E" stroke="#8B4513" stroke-width="2"/>
            <rect x="80" y="140" width="30" height="30" fill="#87CEEB" stroke="#4682B4" stroke-width="2"/>
            <rect x="140" y="140" width="30" height="30" fill="#87CEEB" stroke="#4682B4" stroke-width="2"/>
            <rect x="105" y="170" width="40" height="50" fill="#8B4513" stroke="#654321" stroke-width="2"/>
            <!-- Roof (triangular prism) -->
            <path d="M 50,120 L 125,70 L 200,120 Z" fill="#B22222" stroke="#8B0000" stroke-width="2"/>
            <path d="M 125,70 L 200,120 L 210,110 L 135,60 Z" fill="#8B0000" opacity="0.8" stroke="#8B0000" stroke-width="2"/>
        </svg>
    </div>
    '''

def create_ice_cream_svg():
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <!-- Ice cream scoop (hemisphere) -->
            <path d="M 75,120 Q 125,40 175,120 Z" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
            <!-- Cone -->
            <path d="M 85,120 L 125,220 L 165,120 Z" fill="#D2691E" stroke="#8B4513" stroke-width="2"/>
            <!-- Waffle pattern -->
            <line x1="95" y1="140" x2="155" y2="140" stroke="#8B4513" stroke-width="1"/>
            <line x1="100" y1="160" x2="150" y2="160" stroke="#8B4513" stroke-width="1"/>
            <line x1="105" y1="180" x2="145" y2="180" stroke="#8B4513" stroke-width="1"/>
        </svg>
    </div>
    '''

def create_pencil_svg():
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <!-- Pencil body (cylinder) -->
            <rect x="70" y="80" width="110" height="120" fill="#FFD700" stroke="#FFA500" stroke-width="2"/>
            <rect x="70" y="80" width="110" height="20" fill="#FFB6C1" stroke="#FF69B4" stroke-width="2"/>
            <!-- Pencil tip (cone) -->
            <path d="M 70,200 L 125,240 L 180,200 Z" fill="#D2691E" stroke="#8B4513" stroke-width="2"/>
            <path d="M 115,230 L 125,240 L 135,230 Z" fill="#2F4F4F" stroke="#000" stroke-width="1"/>
            <!-- Metal band -->
            <rect x="70" y="190" width="110" height="10" fill="#C0C0C0" stroke="#808080" stroke-width="2"/>
        </svg>
    </div>
    '''

def create_dice_svg():
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <g transform="translate(125,125)">
                <!-- Front face with dots -->
                <rect x="-50" y="-50" width="100" height="100" fill="white" stroke="black" stroke-width="3" rx="10"/>
                <circle cx="-25" cy="-25" r="6" fill="black"/>
                <circle cx="25" cy="-25" r="6" fill="black"/>
                <circle cx="0" cy="0" r="6" fill="black"/>
                <circle cx="-25" cy="25" r="6" fill="black"/>
                <circle cx="25" cy="25" r="6" fill="black"/>
                <!-- Top face -->
                <path d="M -50,-50 L -30,-70 L 70,-70 L 50,-50 Z" fill="#f0f0f0" stroke="black" stroke-width="3"/>
                <circle cx="10" cy="-60" r="5" fill="black"/>
                <!-- Right face -->
                <path d="M 50,-50 L 70,-70 L 70,30 L 50,50 Z" fill="#e0e0e0" stroke="black" stroke-width="3"/>
                <circle cx="60" cy="-10" r="5" fill="black"/>
                <circle cx="60" cy="10" r="5" fill="black"/>
            </g>
        </svg>
    </div>
    '''

def create_soccer_ball_svg():
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <circle cx="125" cy="125" r="75" fill="white" stroke="black" stroke-width="3"/>
            <!-- Pentagon patches -->
            <path d="M 125,60 L 105,75 L 112,100 L 138,100 L 145,75 Z" fill="black"/>
            <path d="M 70,110 L 60,130 L 70,150 L 90,150 L 95,130 Z" fill="black"/>
            <path d="M 160,110 L 155,130 L 160,150 L 180,150 L 190,130 Z" fill="black"/>
            <path d="M 125,170 L 105,175 L 112,190 L 138,190 L 145,175 Z" fill="black"/>
        </svg>
    </div>
    '''

def create_cross_section_circle():
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <text x="125" y="30" text-anchor="middle" font-size="14" fill="black">Cross-section view:</text>
            <circle cx="125" cy="125" r="60" fill="#FFE6B3" stroke="black" stroke-width="3"/>
            <text x="125" y="220" text-anchor="middle" font-size="12" fill="gray">
                (Horizontal cut through a 3D shape)
            </text>
        </svg>
    </div>
    '''

def create_net_cube():
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <text x="125" y="20" text-anchor="middle" font-size="14" fill="black">Net Pattern:</text>
            <!-- Cross-shaped net for cube -->
            <g transform="translate(125,135)">
                <rect x="-25" y="-75" width="50" height="50" fill="#FFE6B3" stroke="black" stroke-width="2"/>
                <rect x="-75" y="-25" width="50" height="50" fill="#FFE6B3" stroke="black" stroke-width="2"/>
                <rect x="-25" y="-25" width="50" height="50" fill="#FFE6B3" stroke="black" stroke-width="2"/>
                <rect x="25" y="-25" width="50" height="50" fill="#FFE6B3" stroke="black" stroke-width="2"/>
                <rect x="-25" y="25" width="50" height="50" fill="#FFE6B3" stroke="black" stroke-width="2"/>
                <rect x="-25" y="75" width="50" height="50" fill="#FFE6B3" stroke="black" stroke-width="2"/>
            </g>
        </svg>
    </div>
    '''

def create_orthographic_views():
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <text x="125" y="20" text-anchor="middle" font-size="14" fill="black">Orthographic Views:</text>
            <!-- Top view -->
            <g transform="translate(60,60)">
                <text x="30" y="-5" text-anchor="middle" font-size="10" fill="gray">Top</text>
                <rect x="0" y="0" width="40" height="40" fill="#B3D9FF" stroke="black" stroke-width="2"/>
                <rect x="20" y="20" width="20" height="20" fill="#B3D9FF" stroke="black" stroke-width="2"/>
            </g>
            <!-- Front view -->
            <g transform="translate(60,120)">
                <text x="30" y="-5" text-anchor="middle" font-size="10" fill="gray">Front</text>
                <rect x="0" y="0" width="40" height="60" fill="#FFB3B3" stroke="black" stroke-width="2"/>
                <rect x="20" y="0" width="20" height="40" fill="#FFB3B3" stroke="black" stroke-width="2"/>
            </g>
            <!-- Side view -->
            <g transform="translate(150,120)">
                <text x="30" y="-5" text-anchor="middle" font-size="10" fill="gray">Side</text>
                <rect x="0" y="0" width="40" height="60" fill="#B3FFB3" stroke="black" stroke-width="2"/>
                <rect x="0" y="0" width="20" height="40" fill="#B3FFB3" stroke="black" stroke-width="2"/>
            </g>
        </svg>
    </div>
    '''

def create_oblique_cylinder_svg():
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <defs>
                <linearGradient id="obliqueGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#B3D9FF;stop-opacity:0.7" />
                    <stop offset="50%" style="stop-color:#B3D9FF;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#B3D9FF;stop-opacity:0.7" />
                </linearGradient>
            </defs>
            <ellipse cx="145" cy="70" rx="60" ry="20" fill="#B3D9FF" stroke="black" stroke-width="2"/>
            <path d="M 85,70 L 65,180 L 125,180 L 145,70" fill="url(#obliqueGrad)"/>
            <path d="M 145,70 L 125,180 L 185,180 L 205,70" fill="url(#obliqueGrad)"/>
            <ellipse cx="125" cy="180" rx="60" ry="20" fill="#B3D9FF" stroke="black" stroke-width="2"/>
        </svg>
    </div>
    '''

def create_tetrahedron_svg():
    return f'''
    <div style="text-align: center; margin: 20px 0;">
        <svg width="250" height="250" viewBox="0 0 250 250">
            <g transform="translate(125,125)">
                <!-- Base triangle -->
                <path d="M -60,40 L 60,40 L 0,-40 Z" 
                      fill="#FFD4B3" opacity="0.5" stroke="#333" stroke-width="2"/>
                <!-- Front face -->
                <path d="M -60,40 L 60,40 L 0,-60 Z" 
                      fill="#FFD4B3" opacity="0.8" stroke="#333" stroke-width="2"/>
                <!-- Left face -->
                <path d="M -60,40 L 0,-40 L 0,-60 Z" 
                      fill="#FFD4B3" opacity="0.7" stroke="#333" stroke-width="2"/>
                <!-- Right face -->
                <path d="M 60,40 L 0,-60 L 0,-40 Z" 
                      fill="#FFD4B3" opacity="0.6" stroke="#333" stroke-width="2"/>
            </g>
        </svg>
    </div>
    '''