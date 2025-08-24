import streamlit as st
import random
import math

def run():
    """
    Main function to run the Rotational Symmetry activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/U. Two-dimensional figures/rotational_symmetry.py
    """
    # Initialize session state
    if "rotation_difficulty" not in st.session_state:
        st.session_state.rotation_difficulty = 1  # 1=easy, 2=medium, 3=hard
    
    if "current_object" not in st.session_state:
        st.session_state.current_object = None
        st.session_state.object_data = {}
        st.session_state.show_feedback = False
        st.session_state.user_answer = None
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
        st.session_state.recent_objects = []  # Track recent objects to avoid repetition
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > U. Two-dimensional figures**")
    st.title("🔄 Rotational Symmetry")
    st.markdown("*Identify whether the picture has rotational symmetry*")
    st.markdown("---")
    
    # Difficulty and stats display
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        difficulty_text = {
            1: "Easy (Simple shapes)",
            2: "Medium (Complex objects)", 
            3: "Hard (Tricky cases)"
        }
        st.markdown(f"**Difficulty:** {difficulty_text[st.session_state.rotation_difficulty]}")
        progress = (st.session_state.rotation_difficulty - 1) / 2
        st.progress(progress, text=f"Level {st.session_state.rotation_difficulty}/3")
    
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
    
    # Generate new object if needed
    if st.session_state.current_object is None:
        generate_new_object()
    
    # Display the rotation problem
    display_rotation_problem()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### What is Rotational Symmetry?
        
        A shape has **rotational symmetry** if:
        - It looks **exactly the same** after being rotated
        - The rotation is **less than 360°** (a full turn)
        - It fits perfectly onto itself at certain angles
        
        ### Types of Rotational Symmetry:
        
        **Order 2 (180° rotation):**
        - Looks the same after half a turn
        - Examples: Rectangle, letter S, playing card designs
        
        **Order 3 (120° rotation):**
        - Looks the same after 1/3 turn
        - Examples: Recycling symbol, triangular designs
        
        **Order 4 (90° rotation):**
        - Looks the same after 1/4 turn
        - Examples: Square, plus sign (+)
        
        **Order 5+ (72° or less):**
        - Stars, flowers with many petals
        - Regular polygons (pentagon, hexagon, etc.)
        
        ### How to Check:
        
        1. **Imagine rotating** the shape around its center
        2. **Count how many times** it looks identical before completing a full turn
        3. If it only matches at 360° → **No rotational symmetry**
        4. If it matches before 360° → **Has rotational symmetry**
        
        ### Common Examples:
        
        **HAS Rotational Symmetry:**
        - ⭐ Star (5-fold)
        - ❄️ Snowflake (6-fold)
        - ⚙️ Gear wheel
        - 🔄 Recycling symbol (3-fold)
        - Square, Circle, Regular polygons
        - Letters: H, I, N, O, S, X, Z
        
        **NO Rotational Symmetry:**
        - 🦆 Duck
        - 🌙 Crescent moon
        - ➡️ Arrow (one direction)
        - Letters: A, B, C, D, E, F, G, J, K, L, M, P, Q, R, T, U, V, W, Y
        - Most animals and everyday objects
        
        ### Quick Test:
        - Turn the shape 180° - does it look the same?
        - If YES → It has rotational symmetry!
        - If NO → Try 120° or 90°, or it might have none
        """)

def generate_new_object():
    """Generate a new object with or without rotational symmetry"""
    difficulty = st.session_state.rotation_difficulty
    
    # Define object scenarios based on difficulty
    if difficulty == 1:  # Easy - simple shapes and obvious cases
        scenarios = [
            # Objects WITH rotational symmetry
            {
                "name": "star",
                "emoji": "⭐",
                "has_rotation": True,
                "order": 5,
                "description": "A five-pointed star",
                "explanation": "A star has 5-fold rotational symmetry. It looks identical after rotating 72°, 144°, 216°, and 288°."
            },
            {
                "name": "plus_sign",
                "emoji": "➕",
                "has_rotation": True,
                "order": 4,
                "description": "A plus sign",
                "explanation": "A plus sign has 4-fold rotational symmetry. It looks identical after rotating 90°, 180°, and 270°."
            },
            {
                "name": "circle",
                "emoji": "⭕",
                "has_rotation": True,
                "order": "infinite",
                "description": "A circle",
                "explanation": "A circle has infinite rotational symmetry - it looks the same at any angle of rotation."
            },
            {
                "name": "square",
                "shape": "square",
                "has_rotation": True,
                "order": 4,
                "description": "A square",
                "explanation": "A square has 4-fold rotational symmetry. It looks identical after rotating 90°, 180°, and 270°."
            },
            {
                "name": "hexagon",
                "shape": "hexagon",
                "has_rotation": True,
                "order": 6,
                "description": "A regular hexagon",
                "explanation": "A regular hexagon has 6-fold rotational symmetry. It looks identical every 60° rotation."
            },
            {
                "name": "letter_O",
                "text": "O",
                "has_rotation": True,
                "order": "infinite",
                "description": "The letter O",
                "explanation": "The letter O (as a circle) has rotational symmetry - it looks the same when rotated."
            },
            {
                "name": "letter_X",
                "text": "X",
                "has_rotation": True,
                "order": 4,
                "description": "The letter X",
                "explanation": "The letter X has 4-fold rotational symmetry when all arms are equal."
            },
            {
                "name": "snowflake",
                "emoji": "❄️",
                "has_rotation": True,
                "order": 6,
                "description": "A snowflake",
                "explanation": "Snowflakes have 6-fold rotational symmetry due to their crystalline structure."
            },
            {
                "name": "recycle",
                "emoji": "♻️",
                "has_rotation": True,
                "order": 3,
                "description": "Recycling symbol",
                "explanation": "The recycling symbol has 3-fold rotational symmetry - it looks identical every 120°."
            },
            {
                "name": "flower_8",
                "emoji": "🌸",
                "has_rotation": True,
                "order": 5,
                "description": "A flower with petals",
                "explanation": "This flower has rotational symmetry based on its petal arrangement."
            },
            # Objects WITHOUT rotational symmetry
            {
                "name": "arrow_right",
                "emoji": "➡️",
                "has_rotation": False,
                "order": 0,
                "description": "An arrow pointing right",
                "explanation": "An arrow pointing in one direction has no rotational symmetry - it never looks the same when rotated."
            },
            {
                "name": "moon",
                "emoji": "🌙",
                "has_rotation": False,
                "order": 0,
                "description": "A crescent moon",
                "explanation": "A crescent moon has no rotational symmetry due to its curved, asymmetric shape."
            },
            {
                "name": "letter_L",
                "text": "L",
                "has_rotation": False,
                "order": 0,
                "description": "The letter L",
                "explanation": "The letter L has no rotational symmetry - it looks different at any rotation."
            },
            {
                "name": "letter_F",
                "text": "F",
                "has_rotation": False,
                "order": 0,
                "description": "The letter F",
                "explanation": "The letter F has no rotational symmetry - the horizontal lines are only on one side."
            },
            {
                "name": "tree",
                "emoji": "🌳",
                "has_rotation": False,
                "order": 0,
                "description": "A tree",
                "explanation": "Trees are naturally asymmetric and have no rotational symmetry."
            },
            {
                "name": "house",
                "emoji": "🏠",
                "has_rotation": False,
                "order": 0,
                "description": "A house",
                "explanation": "A house with its triangular roof and rectangular base has no rotational symmetry."
            },
            {
                "name": "heart",
                "emoji": "❤️",
                "has_rotation": False,
                "order": 0,
                "description": "A heart",
                "explanation": "A heart shape has no rotational symmetry - it only has reflection symmetry."
            },
            {
                "name": "duck",
                "emoji": "🦆",
                "has_rotation": False,
                "order": 0,
                "description": "A duck",
                "explanation": "Animals like ducks have no rotational symmetry due to their natural body shape."
            }
        ]
    
    elif difficulty == 2:  # Medium - more complex objects
        scenarios = [
            # WITH rotational symmetry
            {
                "name": "peanut",
                "shape": "peanut",
                "has_rotation": True,
                "order": 2,
                "description": "A peanut shape",
                "explanation": "A peanut has 2-fold (180°) rotational symmetry - it looks the same after a half turn."
            },
            {
                "name": "football",
                "emoji": "🏈",
                "has_rotation": True,
                "order": 2,
                "description": "An American football",
                "explanation": "A football has 2-fold rotational symmetry around its long axis."
            },
            {
                "name": "letter_S",
                "text": "S",
                "has_rotation": True,
                "order": 2,
                "description": "The letter S",
                "explanation": "The letter S has 2-fold rotational symmetry - it looks the same after rotating 180°."
            },
            {
                "name": "letter_N",
                "text": "N",
                "has_rotation": True,
                "order": 2,
                "description": "The letter N",
                "explanation": "The letter N has 2-fold rotational symmetry when rotated 180°."
            },
            {
                "name": "letter_Z",
                "text": "Z",
                "has_rotation": True,
                "order": 2,
                "description": "The letter Z",
                "explanation": "The letter Z has 2-fold rotational symmetry."
            },
            {
                "name": "gear",
                "emoji": "⚙️",
                "has_rotation": True,
                "order": 8,
                "description": "A gear wheel",
                "explanation": "Gears have rotational symmetry based on their teeth - this one has 8-fold symmetry."
            },
            {
                "name": "windmill",
                "shape": "windmill",
                "has_rotation": True,
                "order": 4,
                "description": "A windmill",
                "explanation": "A windmill with 4 blades has 4-fold rotational symmetry."
            },
            {
                "name": "yin_yang",
                "emoji": "☯️",
                "has_rotation": True,
                "order": 2,
                "description": "Yin-yang symbol",
                "explanation": "The yin-yang symbol has 2-fold rotational symmetry - perfect balance after 180° rotation."
            },
            {
                "name": "fidget_spinner",
                "shape": "fidget_spinner",
                "has_rotation": True,
                "order": 3,
                "description": "A fidget spinner",
                "explanation": "A typical fidget spinner has 3-fold rotational symmetry."
            },
            {
                "name": "atom",
                "emoji": "⚛️",
                "has_rotation": True,
                "order": 3,
                "description": "Atom symbol",
                "explanation": "The atom symbol typically has 3-fold rotational symmetry from its electron orbits."
            },
            # WITHOUT rotational symmetry
            {
                "name": "lobster",
                "emoji": "🦞",
                "has_rotation": False,
                "order": 0,
                "description": "A lobster",
                "explanation": "A lobster has no rotational symmetry - its claws and tail are asymmetric."
            },
            {
                "name": "xylophone",
                "shape": "xylophone",
                "has_rotation": False,
                "order": 0,
                "description": "A xylophone",
                "explanation": "A xylophone has no rotational symmetry - the bars get progressively shorter."
            },
            {
                "name": "letter_P",
                "text": "P",
                "has_rotation": False,
                "order": 0,
                "description": "The letter P",
                "explanation": "The letter P has no rotational symmetry - the loop is only on one side."
            },
            {
                "name": "scissors",
                "emoji": "✂️",
                "has_rotation": False,
                "order": 0,
                "description": "Scissors",
                "explanation": "Open scissors have no rotational symmetry due to their asymmetric blade arrangement."
            },
            {
                "name": "key",
                "emoji": "🔑",
                "has_rotation": False,
                "order": 0,
                "description": "A key",
                "explanation": "Keys have no rotational symmetry due to their unique teeth pattern."
            },
            {
                "name": "umbrella",
                "emoji": "☂️",
                "has_rotation": False,
                "order": 0,
                "description": "An umbrella",
                "explanation": "An umbrella with its handle has no rotational symmetry."
            },
            {
                "name": "music_note",
                "emoji": "🎵",
                "has_rotation": False,
                "order": 0,
                "description": "A music note",
                "explanation": "Music notes have no rotational symmetry due to their specific directional design."
            },
            {
                "name": "checkmark",
                "emoji": "✓",
                "has_rotation": False,
                "order": 0,
                "description": "A checkmark",
                "explanation": "A checkmark has no rotational symmetry - it's distinctly directional."
            }
        ]
    
    else:  # Hard - tricky cases
        scenarios = [
            # Tricky WITH rotational symmetry
            {
                "name": "letter_H",
                "text": "H",
                "has_rotation": True,
                "order": 2,
                "description": "The letter H",
                "explanation": "The letter H has 2-fold rotational symmetry - it looks the same after 180° rotation."
            },
            {
                "name": "letter_I",
                "text": "I",
                "has_rotation": True,
                "order": 2,
                "description": "The letter I",
                "explanation": "The letter I has 2-fold rotational symmetry when the serifs are symmetric."
            },
            {
                "name": "window_shutters",
                "shape": "window_shutters",
                "has_rotation": True,
                "order": 2,
                "description": "Window with shutters",
                "explanation": "A window with symmetric shutters has 2-fold rotational symmetry."
            },
            {
                "name": "playing_card",
                "shape": "playing_card",
                "has_rotation": True,
                "order": 2,
                "description": "A playing card design",
                "explanation": "Playing cards are designed with 2-fold rotational symmetry so they look the same upside down."
            },
            {
                "name": "propeller_3",
                "shape": "propeller",
                "has_rotation": True,
                "order": 3,
                "description": "A 3-blade propeller",
                "explanation": "A 3-blade propeller has 3-fold rotational symmetry."
            },
            {
                "name": "swastika",
                "shape": "pinwheel",
                "has_rotation": True,
                "order": 4,
                "description": "A pinwheel shape",
                "explanation": "A pinwheel has 4-fold rotational symmetry."
            },
            {
                "name": "infinity",
                "emoji": "∞",
                "has_rotation": True,
                "order": 2,
                "description": "Infinity symbol",
                "explanation": "The infinity symbol has 2-fold rotational symmetry."
            },
            {
                "name": "number_8",
                "text": "8",
                "has_rotation": True,
                "order": 2,
                "description": "The number 8",
                "explanation": "The number 8 has 2-fold rotational symmetry when drawn symmetrically."
            },
            {
                "name": "percent",
                "text": "%",
                "has_rotation": True,
                "order": 2,
                "description": "Percent sign",
                "explanation": "The percent sign has 2-fold rotational symmetry."
            },
            # Tricky WITHOUT rotational symmetry
            {
                "name": "letter_A",
                "text": "A",
                "has_rotation": False,
                "order": 0,
                "description": "The letter A",
                "explanation": "Despite having reflection symmetry, the letter A has NO rotational symmetry."
            },
            {
                "name": "letter_D",
                "text": "D",
                "has_rotation": False,
                "order": 0,
                "description": "The letter D",
                "explanation": "The letter D has no rotational symmetry - the curve is only on one side."
            },
            {
                "name": "triangle_isosceles",
                "shape": "isosceles_triangle",
                "has_rotation": False,
                "order": 0,
                "description": "An isosceles triangle",
                "explanation": "An isosceles triangle has reflection symmetry but NO rotational symmetry (unless equilateral)."
            },
            {
                "name": "semicircle",
                "shape": "semicircle",
                "has_rotation": False,
                "order": 0,
                "description": "A semicircle",
                "explanation": "A semicircle has no rotational symmetry - only reflection symmetry."
            },
            {
                "name": "number_6",
                "text": "6",
                "has_rotation": False,
                "order": 0,
                "description": "The number 6",
                "explanation": "The number 6 has no rotational symmetry (rotating gives 9, which is different)."
            },
            {
                "name": "number_9",
                "text": "9",
                "has_rotation": False,
                "order": 0,
                "description": "The number 9",
                "explanation": "The number 9 has no rotational symmetry (rotating gives 6, which is different)."
            },
            {
                "name": "trapezoid",
                "shape": "trapezoid",
                "has_rotation": False,
                "order": 0,
                "description": "A trapezoid",
                "explanation": "A trapezoid has no rotational symmetry - even an isosceles trapezoid doesn't."
            },
            {
                "name": "question_mark",
                "text": "?",
                "has_rotation": False,
                "order": 0,
                "description": "A question mark",
                "explanation": "A question mark has no rotational symmetry due to its unique curve and dot."
            }
        ]
    
    # Filter out recently used objects
    available_scenarios = [s for s in scenarios if s['name'] not in st.session_state.recent_objects]
    
    # If all objects have been used, reset the recent objects list
    if not available_scenarios:
        st.session_state.recent_objects = []
        available_scenarios = scenarios
    
    # Choose a random scenario
    scenario = random.choice(available_scenarios)
    
    # Add to recent objects (keep last 5)
    st.session_state.recent_objects.append(scenario['name'])
    if len(st.session_state.recent_objects) > 5:
        st.session_state.recent_objects.pop(0)
    
    # Store object data
    st.session_state.object_data = scenario
    st.session_state.current_object = scenario['name']

def display_rotation_problem():
    """Display the rotation problem"""
    data = st.session_state.object_data
    
    # Question text
    st.markdown("### Does this picture have rotational symmetry?")
    
    # Create the object visualization
    create_object_visualization(data)
    
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

def create_object_visualization(data):
    """Create a visual representation of the object"""
    import streamlit.components.v1 as components
    
    # Check what type of visual to create
    if 'emoji' in data:
        # Display emoji in large size
        st.markdown(f"""
        <div style="
            text-align: center;
            font-size: 150px;
            padding: 40px;
            background: #f0f0f0;
            border-radius: 20px;
            margin: 20px auto;
        ">
            {data['emoji']}
        </div>
        """, unsafe_allow_html=True)
    
    elif 'text' in data:
        # Display text (letters/numbers) in large size
        st.markdown(f"""
        <div style="
            text-align: center;
            font-size: 150px;
            font-family: Arial, sans-serif;
            font-weight: bold;
            padding: 40px;
            background: #f0f0f0;
            border-radius: 20px;
            margin: 20px auto;
            color: #333;
        ">
            {data['text']}
        </div>
        """, unsafe_allow_html=True)
    
    elif 'shape' in data:
        # Create SVG for specific shapes
        shape_svg = create_shape_svg(data['shape'])
        
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
                    background: #f0f0f0;
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
        
        components.html(html_content, height=400, scrolling=False)

def create_shape_svg(shape_name):
    """Create SVG for different shapes"""
    
    svg_shapes = {
        'square': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <rect x="150" y="150" width="100" height="100" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
        </svg>
        ''',
        
        'hexagon': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <path d="M 200 120 L 260 155 L 260 225 L 200 260 L 140 225 L 140 155 Z" 
                  fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
        </svg>
        ''',
        
        'peanut': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <path d="M 150 200 Q 150 150, 180 150 Q 200 150, 200 180 Q 200 150, 220 150 Q 250 150, 250 200 Q 250 250, 220 250 Q 200 250, 200 220 Q 200 250, 180 250 Q 150 250, 150 200" 
                  fill="#D4A373" stroke="#8B5A2B" stroke-width="2"/>
            <!-- Add texture lines -->
            <line x1="160" y1="180" x2="170" y2="190" stroke="#8B5A2B" stroke-width="1" opacity="0.5"/>
            <line x1="230" y1="180" x2="240" y2="190" stroke="#8B5A2B" stroke-width="1" opacity="0.5"/>
            <line x1="195" y1="160" x2="205" y2="160" stroke="#8B5A2B" stroke-width="1" opacity="0.5"/>
        </svg>
        ''',
        
        'windmill': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <!-- Center -->
            <circle cx="200" cy="200" r="15" fill="#333"/>
            <!-- Blades -->
            <path d="M 200 185 L 190 120 L 200 125 L 210 120 Z" fill="#FF5722" stroke="#D84315" stroke-width="1"/>
            <path d="M 215 200 L 280 190 L 275 200 L 280 210 Z" fill="#FF5722" stroke="#D84315" stroke-width="1"/>
            <path d="M 200 215 L 210 280 L 200 275 L 190 280 Z" fill="#FF5722" stroke="#D84315" stroke-width="1"/>
            <path d="M 185 200 L 120 210 L 125 200 L 120 190 Z" fill="#FF5722" stroke="#D84315" stroke-width="1"/>
        </svg>
        ''',
        
        'fidget_spinner': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <!-- Center -->
            <circle cx="200" cy="200" r="20" fill="#666"/>
            <!-- Three arms -->
            <circle cx="200" cy="140" r="35" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
            <circle cx="250" cy="230" r="35" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
            <circle cx="150" cy="230" r="35" fill="#2196F3" stroke="#1565C0" stroke-width="2"/>
            <!-- Center bearing -->
            <circle cx="200" cy="200" r="15" fill="#333"/>
        </svg>
        ''',
        
        'xylophone': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <!-- Base -->
            <rect x="100" y="250" width="200" height="20" fill="#8B4513"/>
            <!-- Bars of different lengths -->
            <rect x="110" y="200" width="25" height="50" fill="#FFD700" stroke="#DAA520" stroke-width="1"/>
            <rect x="140" y="190" width="25" height="60" fill="#FFA500" stroke="#FF8C00" stroke-width="1"/>
            <rect x="170" y="180" width="25" height="70" fill="#FF6347" stroke="#FF4500" stroke-width="1"/>
            <rect x="200" y="170" width="25" height="80" fill="#DC143C" stroke="#B22222" stroke-width="1"/>
            <rect x="230" y="160" width="25" height="90" fill="#8B008B" stroke="#800080" stroke-width="1"/>
            <rect x="260" y="150" width="25" height="100" fill="#4B0082" stroke="#310062" stroke-width="1"/>
        </svg>
        ''',
        
        'window_shutters': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <!-- Window frame -->
            <rect x="150" y="150" width="100" height="100" fill="#87CEEB" stroke="#4682B4" stroke-width="3"/>
            <!-- Window panes -->
            <line x1="200" y1="150" x2="200" y2="250" stroke="#4682B4" stroke-width="2"/>
            <line x1="150" y1="200" x2="250" y2="200" stroke="#4682B4" stroke-width="2"/>
            <!-- Left shutter -->
            <rect x="100" y="150" width="45" height="100" fill="#8B4513" stroke="#654321" stroke-width="2"/>
            <line x1="105" y1="170" x2="140" y2="170" stroke="#654321" stroke-width="1"/>
            <line x1="105" y1="190" x2="140" y2="190" stroke="#654321" stroke-width="1"/>
            <line x1="105" y1="210" x2="140" y2="210" stroke="#654321" stroke-width="1"/>
            <line x1="105" y1="230" x2="140" y2="230" stroke="#654321" stroke-width="1"/>
            <!-- Right shutter -->
            <rect x="255" y="150" width="45" height="100" fill="#8B4513" stroke="#654321" stroke-width="2"/>
            <line x1="260" y1="170" x2="295" y2="170" stroke="#654321" stroke-width="1"/>
            <line x1="260" y1="190" x2="295" y2="190" stroke="#654321" stroke-width="1"/>
            <line x1="260" y1="210" x2="295" y2="210" stroke="#654321" stroke-width="1"/>
            <line x1="260" y1="230" x2="295" y2="230" stroke="#654321" stroke-width="1"/>
        </svg>
        ''',
        
        'playing_card': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <!-- Card outline -->
            <rect x="140" y="120" width="120" height="160" rx="10" fill="white" stroke="black" stroke-width="2"/>
            <!-- Top symbol -->
            <path d="M 160 150 Q 160 140, 170 140 Q 180 140, 180 150 Q 180 140, 190 140 Q 200 140, 200 150 Q 200 160, 180 180 Q 160 160, 160 150" 
                  fill="red"/>
            <!-- Bottom symbol (rotated) -->
            <path d="M 240 250 Q 240 260, 230 260 Q 220 260, 220 250 Q 220 260, 210 260 Q 200 260, 200 250 Q 200 240, 220 220 Q 240 240, 240 250" 
                  fill="red"/>
            <!-- Numbers -->
            <text x="150" y="145" font-size="20" fill="red">7</text>
            <text x="250" y="275" font-size="20" fill="red" transform="rotate(180 250 275)">7</text>
        </svg>
        ''',
        
        'propeller': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <!-- Center hub -->
            <circle cx="200" cy="200" r="20" fill="#666" stroke="#333" stroke-width="2"/>
            <!-- Three blades -->
            <path d="M 200 180 L 190 100 Q 200 95, 210 100 Z" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
            <path d="M 217 210 L 295 240 Q 300 230, 295 220 Z" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
            <path d="M 183 210 L 105 240 Q 100 230, 105 220 Z" fill="#4CAF50" stroke="#2E7D32" stroke-width="2"/>
        </svg>
        ''',
        
        'pinwheel': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <!-- Center -->
            <circle cx="200" cy="200" r="10" fill="#333"/>
            <!-- Four curved arms -->
            <path d="M 200 200 L 200 150 Q 220 150, 220 170 Z" fill="#FF5722"/>
            <path d="M 200 200 L 250 200 Q 250 220, 230 220 Z" fill="#2196F3"/>
            <path d="M 200 200 L 200 250 Q 180 250, 180 230 Z" fill="#FFC107"/>
            <path d="M 200 200 L 150 200 Q 150 180, 170 180 Z" fill="#4CAF50"/>
        </svg>
        ''',
        
        'isosceles_triangle': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <path d="M 200 150 L 260 250 L 140 250 Z" 
                  fill="#9C27B0" stroke="#6A1B9A" stroke-width="2"/>
        </svg>
        ''',
        
        'semicircle': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <path d="M 130 200 A 70 70 0 0 0 270 200 Z" 
                  fill="#FF9800" stroke="#E65100" stroke-width="2"/>
        </svg>
        ''',
        
        'trapezoid': '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <path d="M 160 250 L 240 250 L 220 150 L 180 150 Z" 
                  fill="#00BCD4" stroke="#00838F" stroke-width="2"/>
        </svg>
        '''
    }
    
    return svg_shapes.get(shape_name, '''
        <svg width="400" height="400" viewBox="0 0 400 400">
            <circle cx="200" cy="200" r="80" fill="#9E9E9E" stroke="#616161" stroke-width="2"/>
        </svg>
    ''')

def submit_answer(user_answer):
    """Process the submitted answer"""
    st.session_state.user_answer = user_answer
    st.session_state.show_feedback = True
    st.session_state.total_attempted += 1
    
    correct_answer = st.session_state.object_data['has_rotation']
    
    if user_answer == correct_answer:
        st.session_state.total_correct += 1
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3 and st.session_state.rotation_difficulty < 3:
            st.session_state.rotation_difficulty += 1
            st.session_state.consecutive_correct = 0
    else:
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after poor performance
        if st.session_state.rotation_difficulty > 1:
            recent_accuracy = st.session_state.total_correct / max(st.session_state.total_attempted, 1)
            if recent_accuracy < 0.5 and st.session_state.total_attempted >= 3:
                st.session_state.rotation_difficulty -= 1

def show_feedback():
    """Display feedback for the answer"""
    data = st.session_state.object_data
    user_answer = st.session_state.user_answer
    correct_answer = data['has_rotation']
    
    if user_answer == correct_answer:
        if correct_answer:
            st.success(f"✅ **Correct!** Yes, this picture HAS rotational symmetry!")
        else:
            st.success(f"✅ **Correct!** No, this picture does NOT have rotational symmetry!")
        
        # Show explanation
        st.info(f"📐 **{data['description']}**: {data['explanation']}")
        
        # Additional info for correct answers with rotation
        if correct_answer and data['order'] != 0 and data['order'] != "infinite":
            st.markdown(f"**Order of symmetry:** {data['order']} (rotates {data['order']} times before returning to original)")
        
        # Special recognition
        if st.session_state.consecutive_correct == 3:
            st.balloons()
            st.info("🏆 **Excellent streak! Moving to the next level!**")
    else:
        if correct_answer:
            st.error(f"❌ **Not quite.** This picture HAS rotational symmetry.")
        else:
            st.error(f"❌ **Not quite.** This picture does NOT have rotational symmetry.")
        
        # Show detailed explanation
        with st.expander("📖 **Understanding rotational symmetry**", expanded=True):
            st.markdown(f"""
            ### Object: {data['description']}
            
            **Explanation:** {data['explanation']}
            
            ### Remember:
            - **Rotational symmetry** means the shape looks identical when rotated
            - The rotation must be **less than 360°** to count
            - Try the **180° test** first - does it look the same upside down?
            
            ### Common Orders of Symmetry:
            - **Order 2:** Looks same after 180° (half turn)
            - **Order 3:** Looks same after 120° (1/3 turn)
            - **Order 4:** Looks same after 90° (1/4 turn)
            - **Order 6:** Looks same after 60° (1/6 turn)
            
            ### Quick Check:
            - Rotate the shape in your mind
            - If it matches before a full turn → **Has rotational symmetry**
            - If it only matches at 360° → **No rotational symmetry**
            """)
            
            if correct_answer and data['order'] != 0:
                st.markdown(f"""
                ### This shape's symmetry:
                - **Order:** {data['order']}
                - **Rotation angles:** Every {360/data['order'] if data['order'] != 'infinite' else 'any'}°
                """)

def reset_for_next_question():
    """Reset state for next question"""
    st.session_state.current_object = None
    st.session_state.object_data = {}
    st.session_state.show_feedback = False
    st.session_state.user_answer = None
    if "selected_answer" in st.session_state:
        del st.session_state.selected_answer