import streamlit as st
import streamlit.components.v1 as components
import random

def run():
    """
    Main function to run the Count Vertices, Edges and Faces activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/W. Three-dimensional figures/count_vertices_edges_faces.py
    """
    
    # Initialize session state
    if "count_3d_difficulty" not in st.session_state:
        st.session_state.count_3d_difficulty = 1
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    if "current_counting_question" not in st.session_state:
        st.session_state.current_counting_question = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answer = ""
    
    # Page header
    st.markdown("**📚 Year 5 > W. Three-dimensional figures**")
    st.title("📐 Count Vertices, Edges and Faces")
    st.markdown("*Learn to count the parts of 3D shapes*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty = st.session_state.count_3d_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic Shapes",
            2: "Prisms & Simple Pyramids", 
            3: "Complex Pyramids",
            4: "Advanced Polyhedra",
            5: "Expert Level"
        }
        st.markdown(f"**Current Level:** {difficulty} - {difficulty_names.get(difficulty, 'Basic')}")
        progress = (difficulty - 1) / 4
        st.progress(progress, text=f"Level {difficulty}/5")
    
    with col2:
        if difficulty <= 2:
            st.markdown("**🟢 Easy**")
        elif difficulty <= 3:
            st.markdown("**🟡 Medium**")
        else:
            st.markdown("**🔴 Hard**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_counting_question is None:
        st.session_state.current_counting_question = generate_counting_question(difficulty)
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answer = ""
    
    # Display the question
    display_counting_question()
    
    # Handle feedback
    handle_counting_feedback()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Complete Shape Reference Table**", expanded=False):
        st.markdown("""
        ### 📊 All 3D Shapes Properties:
        
        | Shape | Vertices | Edges | Faces | Description |
        |-------|----------|-------|-------|-------------|
        | **Prisms** |||||
        | Cube | 8 | 12 | 6 | All faces are squares |
        | Cuboid | 8 | 12 | 6 | All faces are rectangles |
        | Triangular Prism | 6 | 9 | 5 | 2 triangles + 3 rectangles |
        | Pentagonal Prism | 10 | 15 | 7 | 2 pentagons + 5 rectangles |
        | Hexagonal Prism | 12 | 18 | 8 | 2 hexagons + 6 rectangles |
        | Octagonal Prism | 16 | 24 | 10 | 2 octagons + 8 rectangles |
        | **Pyramids** |||||
        | Triangular Pyramid | 4 | 6 | 4 | All faces are triangles |
        | Square Pyramid | 5 | 8 | 5 | 1 square + 4 triangles |
        | Rectangular Pyramid | 5 | 8 | 5 | 1 rectangle + 4 triangles |
        | Pentagonal Pyramid | 6 | 10 | 6 | 1 pentagon + 5 triangles |
        | Hexagonal Pyramid | 7 | 12 | 7 | 1 hexagon + 6 triangles |
        | **Regular Polyhedra** |||||
        | Octahedron | 6 | 12 | 8 | 8 triangular faces |
        | Dodecahedron | 20 | 30 | 12 | 12 pentagonal faces |
        | Icosahedron | 12 | 30 | 20 | 20 triangular faces |
        | **Curved Surfaces** |||||
        | Cylinder | 0 | 2 | 3 | 2 circles + 1 curved surface |
        | Cone | 1 | 1 | 2 | 1 circle + 1 curved surface |
        | Sphere | 0 | 0 | 1 | 1 curved surface only |
        
        ### 🔍 Key Formulas:
        - **Euler's Formula for Polyhedra:** V - E + F = 2
        - **Prism Formula:** If base has n sides: V = 2n, E = 3n, F = n+2
        - **Pyramid Formula:** If base has n sides: V = n+1, E = 2n, F = n+1
        """)

def render_shape_svg(shape_name, color):
    """Render SVG shape using components.html()"""
    
    svg_code = get_shape_svg_code(shape_name, color)
    
    html_code = f"""
    <div style="display: flex; justify-content: center; align-items: center; width: 100%; height: 320px;">
        {svg_code}
    </div>
    """
    
    # Use components.html to render the SVG
    components.html(html_code, height=320)

def get_shape_svg_code(shape_name, color):
    """Get SVG code for all 17 different shapes"""
    
    if shape_name == "cube":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Back face -->
                <rect x="-30" y="-30" width="60" height="60" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"
                      transform="translate(20,20)"/>
                <!-- Front face -->
                <rect x="-50" y="-50" width="100" height="100" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <!-- Connecting edges -->
                <line x1="-50" y1="-50" x2="-30" y2="-30" stroke="black" stroke-width="2"/>
                <line x1="50" y1="-50" x2="70" y2="-30" stroke="black" stroke-width="2"/>
                <line x1="50" y1="50" x2="70" y2="70" stroke="black" stroke-width="2"/>
                <line x1="-50" y1="50" x2="-30" y2="70" stroke="black" stroke-width="2"/>
                <!-- Hidden edges -->
                <line x1="-30" y1="-30" x2="70" y2="-30" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <line x1="70" y1="-30" x2="70" y2="70" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <line x1="-30" y1="70" x2="70" y2="70" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <line x1="-30" y1="-30" x2="-30" y2="70" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <!-- Vertices -->
                <circle cx="-50" cy="-50" r="4" fill="darkblue"/>
                <circle cx="50" cy="-50" r="4" fill="darkblue"/>
                <circle cx="50" cy="50" r="4" fill="darkblue"/>
                <circle cx="-50" cy="50" r="4" fill="darkblue"/>
                <circle cx="-30" cy="-30" r="4" fill="darkblue"/>
                <circle cx="70" cy="-30" r="4" fill="darkblue"/>
                <circle cx="70" cy="70" r="4" fill="darkblue"/>
                <circle cx="-30" cy="70" r="4" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Cube</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "cuboid":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Back face -->
                <rect x="-40" y="-25" width="80" height="50" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"
                      transform="translate(25,20)"/>
                <!-- Front face -->
                <rect x="-65" y="-45" width="130" height="90" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <!-- Connecting edges -->
                <line x1="-65" y1="-45" x2="-40" y2="-25" stroke="black" stroke-width="2"/>
                <line x1="65" y1="-45" x2="90" y2="-25" stroke="black" stroke-width="2"/>
                <line x1="65" y1="45" x2="90" y2="65" stroke="black" stroke-width="2"/>
                <line x1="-65" y1="45" x2="-40" y2="65" stroke="black" stroke-width="2"/>
                <!-- Hidden edges -->
                <line x1="-40" y1="-25" x2="90" y2="-25" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <line x1="90" y1="-25" x2="90" y2="65" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <line x1="-40" y1="65" x2="90" y2="65" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <line x1="-40" y1="-25" x2="-40" y2="65" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <!-- Vertices -->
                <circle cx="-65" cy="-45" r="4" fill="darkblue"/>
                <circle cx="65" cy="-45" r="4" fill="darkblue"/>
                <circle cx="65" cy="45" r="4" fill="darkblue"/>
                <circle cx="-65" cy="45" r="4" fill="darkblue"/>
                <circle cx="-40" cy="-25" r="4" fill="darkblue"/>
                <circle cx="90" cy="-25" r="4" fill="darkblue"/>
                <circle cx="90" cy="65" r="4" fill="darkblue"/>
                <circle cx="-40" cy="65" r="4" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Cuboid</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "triangular_prism":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Front triangle -->
                <path d="M -60,40 L 0,-50 L 60,40 Z" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <!-- Back triangle -->
                <path d="M -40,55 L 20,-35 L 80,55 Z" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Connecting edges -->
                <line x1="-60" y1="40" x2="-40" y2="55" stroke="black" stroke-width="2"/>
                <line x1="0" y1="-50" x2="20" y2="-35" stroke="black" stroke-width="2"/>
                <line x1="60" y1="40" x2="80" y2="55" stroke="black" stroke-width="2"/>
                <!-- Hidden edges -->
                <line x1="-40" y1="55" x2="20" y2="-35" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <line x1="20" y1="-35" x2="80" y2="55" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <line x1="-40" y1="55" x2="80" y2="55" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <!-- Vertices -->
                <circle cx="-60" cy="40" r="4" fill="darkblue"/>
                <circle cx="0" cy="-50" r="4" fill="darkblue"/>
                <circle cx="60" cy="40" r="4" fill="darkblue"/>
                <circle cx="-40" cy="55" r="4" fill="darkblue"/>
                <circle cx="20" cy="-35" r="4" fill="darkblue"/>
                <circle cx="80" cy="55" r="4" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Triangular Prism</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "pentagonal_prism":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Front pentagon -->
                <path d="M 0,-50 L -47,-15 L -29,40 L 29,40 L 47,-15 Z" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <!-- Back pentagon -->
                <path d="M 20,-40 L -27,-5 L -9,50 L 49,50 L 67,-5 Z" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Connecting edges -->
                <line x1="0" y1="-50" x2="20" y2="-40" stroke="black" stroke-width="2"/>
                <line x1="-47" y1="-15" x2="-27" y2="-5" stroke="black" stroke-width="2"/>
                <line x1="-29" y1="40" x2="-9" y2="50" stroke="black" stroke-width="2"/>
                <line x1="29" y1="40" x2="49" y2="50" stroke="black" stroke-width="2"/>
                <line x1="47" y1="-15" x2="67" y2="-5" stroke="black" stroke-width="2"/>
                <!-- Vertices (10 total) -->
                <circle cx="0" cy="-50" r="3" fill="darkblue"/>
                <circle cx="-47" cy="-15" r="3" fill="darkblue"/>
                <circle cx="-29" cy="40" r="3" fill="darkblue"/>
                <circle cx="29" cy="40" r="3" fill="darkblue"/>
                <circle cx="47" cy="-15" r="3" fill="darkblue"/>
                <circle cx="20" cy="-40" r="3" fill="darkblue"/>
                <circle cx="-27" cy="-5" r="3" fill="darkblue"/>
                <circle cx="-9" cy="50" r="3" fill="darkblue"/>
                <circle cx="49" cy="50" r="3" fill="darkblue"/>
                <circle cx="67" cy="-5" r="3" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Pentagonal Prism</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "hexagonal_prism":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Front hexagon -->
                <path d="M -50,0 L -25,-43 L 25,-43 L 50,0 L 25,43 L -25,43 Z" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <!-- Back hexagon -->
                <path d="M -30,15 L -5,-28 L 45,-28 L 70,15 L 45,58 L -5,58 Z" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Connecting edges -->
                <line x1="-50" y1="0" x2="-30" y2="15" stroke="black" stroke-width="2"/>
                <line x1="-25" y1="-43" x2="-5" y2="-28" stroke="black" stroke-width="2"/>
                <line x1="25" y1="-43" x2="45" y2="-28" stroke="black" stroke-width="2"/>
                <line x1="50" y1="0" x2="70" y2="15" stroke="black" stroke-width="2"/>
                <line x1="25" y1="43" x2="45" y2="58" stroke="black" stroke-width="2"/>
                <line x1="-25" y1="43" x2="-5" y2="58" stroke="black" stroke-width="2"/>
                <!-- Vertices (12 total) -->
                <circle cx="-50" cy="0" r="3" fill="darkblue"/>
                <circle cx="-25" cy="-43" r="3" fill="darkblue"/>
                <circle cx="25" cy="-43" r="3" fill="darkblue"/>
                <circle cx="50" cy="0" r="3" fill="darkblue"/>
                <circle cx="25" cy="43" r="3" fill="darkblue"/>
                <circle cx="-25" cy="43" r="3" fill="darkblue"/>
                <circle cx="-30" cy="15" r="3" fill="darkblue"/>
                <circle cx="-5" cy="-28" r="3" fill="darkblue"/>
                <circle cx="45" cy="-28" r="3" fill="darkblue"/>
                <circle cx="70" cy="15" r="3" fill="darkblue"/>
                <circle cx="45" cy="58" r="3" fill="darkblue"/>
                <circle cx="-5" cy="58" r="3" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Hexagonal Prism</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "octagonal_prism":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Front octagon -->
                <path d="M -30,-50 L 30,-50 L 50,-30 L 50,30 L 30,50 L -30,50 L -50,30 L -50,-30 Z" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <!-- Back octagon -->
                <path d="M -15,-35 L 45,-35 L 65,-15 L 65,45 L 45,65 L -15,65 L -35,45 L -35,-15 Z" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Some connecting edges -->
                <line x1="-30" y1="-50" x2="-15" y2="-35" stroke="black" stroke-width="2"/>
                <line x1="30" y1="-50" x2="45" y2="-35" stroke="black" stroke-width="2"/>
                <line x1="50" y1="-30" x2="65" y2="-15" stroke="black" stroke-width="2"/>
                <line x1="50" y1="30" x2="65" y2="45" stroke="black" stroke-width="2"/>
                <!-- Mark some vertices -->
                <circle cx="-30" cy="-50" r="3" fill="darkblue"/>
                <circle cx="30" cy="-50" r="3" fill="darkblue"/>
                <circle cx="50" cy="-30" r="3" fill="darkblue"/>
                <circle cx="50" cy="30" r="3" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Octagonal Prism</text>
                <text x="-120" y="90" font-size="10" fill="gray">16 vertices, 24 edges, 10 faces</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "triangular_pyramid":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Base triangle -->
                <path d="M -60,40 L 60,40 L 0,60 Z" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Visible faces -->
                <path d="M 0,-50 L -60,40 L 60,40 Z" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <!-- Hidden edge -->
                <line x1="0" y1="-50" x2="0" y2="60" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <!-- Vertices (4 total) -->
                <circle cx="0" cy="-50" r="4" fill="darkblue"/>
                <circle cx="-60" cy="40" r="4" fill="darkblue"/>
                <circle cx="60" cy="40" r="4" fill="darkblue"/>
                <circle cx="0" cy="60" r="4" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Triangular Pyramid</text>
                <text x="-120" y="90" font-size="10" fill="gray">(Tetrahedron)</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "square_pyramid":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Base square -->
                <path d="M -50,30 L 50,30 L 70,50 L -30,50 Z" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Front faces -->
                <path d="M 0,-60 L -50,30 L 50,30 Z" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <path d="M 0,-60 L 50,30 L 70,50 Z" 
                      fill="{color}" opacity="0.85" stroke="black" stroke-width="2"/>
                <!-- Hidden edges -->
                <line x1="0" y1="-60" x2="-30" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <line x1="0" y1="-60" x2="70" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <!-- Vertices (5 total) -->
                <circle cx="0" cy="-60" r="4" fill="darkblue"/>
                <circle cx="-50" cy="30" r="4" fill="darkblue"/>
                <circle cx="50" cy="30" r="4" fill="darkblue"/>
                <circle cx="70" cy="50" r="4" fill="darkblue"/>
                <circle cx="-30" cy="50" r="4" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Square Pyramid</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "rectangular_pyramid":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Base rectangle -->
                <path d="M -60,30 L 40,30 L 60,50 L -40,50 Z" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Front faces -->
                <path d="M 0,-60 L -60,30 L 40,30 Z" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <path d="M 0,-60 L 40,30 L 60,50 Z" 
                      fill="{color}" opacity="0.85" stroke="black" stroke-width="2"/>
                <!-- Hidden edges -->
                <line x1="0" y1="-60" x2="-40" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <line x1="0" y1="-60" x2="60" y2="50" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>
                <!-- Vertices (5 total) -->
                <circle cx="0" cy="-60" r="4" fill="darkblue"/>
                <circle cx="-60" cy="30" r="4" fill="darkblue"/>
                <circle cx="40" cy="30" r="4" fill="darkblue"/>
                <circle cx="60" cy="50" r="4" fill="darkblue"/>
                <circle cx="-40" cy="50" r="4" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Rectangular Pyramid</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "pentagonal_pyramid":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Base pentagon -->
                <path d="M 0,40 L -38,12 L -24,-31 L 24,-31 L 38,12 Z" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Pyramid faces -->
                <path d="M 0,-70 L 0,40 L -38,12 Z" fill="{color}" opacity="0.9" stroke="black" stroke-width="2"/>
                <path d="M 0,-70 L -38,12 L -24,-31 Z" fill="{color}" opacity="0.85" stroke="black" stroke-width="2"/>
                <path d="M 0,-70 L -24,-31 L 24,-31 Z" fill="{color}" opacity="0.8" stroke="black" stroke-width="2"/>
                <path d="M 0,-70 L 24,-31 L 38,12 Z" fill="{color}" opacity="0.75" stroke="black" stroke-width="2"/>
                <!-- Vertices (6 total) -->
                <circle cx="0" cy="-70" r="4" fill="darkblue"/>
                <circle cx="0" cy="40" r="4" fill="darkblue"/>
                <circle cx="-38" cy="12" r="4" fill="darkblue"/>
                <circle cx="-24" cy="-31" r="4" fill="darkblue"/>
                <circle cx="24" cy="-31" r="4" fill="darkblue"/>
                <circle cx="38" cy="12" r="4" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Pentagonal Pyramid</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "hexagonal_pyramid":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Base hexagon -->
                <path d="M -40,20 L -20,-20 L 20,-20 L 40,20 L 20,60 L -20,60 Z" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Pyramid faces -->
                <path d="M 0,-80 L -40,20 L -20,-20 Z" fill="{color}" opacity="0.95" stroke="black" stroke-width="2"/>
                <path d="M 0,-80 L -20,-20 L 20,-20 Z" fill="{color}" opacity="0.9" stroke="black" stroke-width="2"/>
                <path d="M 0,-80 L 20,-20 L 40,20 Z" fill="{color}" opacity="0.85" stroke="black" stroke-width="2"/>
                <!-- Vertices (7 total) -->
                <circle cx="0" cy="-80" r="4" fill="darkblue"/>
                <circle cx="-40" cy="20" r="4" fill="darkblue"/>
                <circle cx="-20" cy="-20" r="4" fill="darkblue"/>
                <circle cx="20" cy="-20" r="4" fill="darkblue"/>
                <circle cx="40" cy="20" r="4" fill="darkblue"/>
                <circle cx="20" cy="60" r="4" fill="darkblue"/>
                <circle cx="-20" cy="60" r="4" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Hexagonal Pyramid</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "octahedron":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Square middle -->
                <path d="M -50,0 L 0,-50 L 50,0 L 0,50 Z" 
                      fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Top pyramid -->
                <path d="M 0,-80 L -50,0 L 0,-50 Z" fill="{color}" opacity="0.9" stroke="black" stroke-width="2"/>
                <path d="M 0,-80 L 0,-50 L 50,0 Z" fill="{color}" opacity="0.85" stroke="black" stroke-width="2"/>
                <!-- Bottom pyramid -->
                <path d="M 0,80 L -50,0 L 0,50 Z" fill="{color}" opacity="0.6" stroke="black" stroke-width="2"/>
                <path d="M 0,80 L 0,50 L 50,0 Z" fill="{color}" opacity="0.65" stroke="black" stroke-width="2"/>
                <!-- Vertices (6 total) -->
                <circle cx="0" cy="-80" r="4" fill="darkblue"/>
                <circle cx="-50" cy="0" r="4" fill="darkblue"/>
                <circle cx="0" cy="-50" r="4" fill="darkblue"/>
                <circle cx="50" cy="0" r="4" fill="darkblue"/>
                <circle cx="0" cy="50" r="4" fill="darkblue"/>
                <circle cx="0" cy="80" r="4" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Octahedron</text>
                <text x="-120" y="90" font-size="10" fill="gray">6 vertices, 12 edges, 8 faces</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "dodecahedron":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Front pentagon -->
                <path d="M 0,-60 L -57,-19 L -35,49 L 35,49 L 57,-19 Z" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <!-- Visible adjacent pentagons -->
                <path d="M 57,-19 L 35,49 L 70,40 L 80,-5 L 60,-35 Z" 
                      fill="{color}" opacity="0.8" stroke="black" stroke-width="2"/>
                <path d="M -57,-19 L -60,-35 L -80,-5 L -70,40 L -35,49 Z" 
                      fill="{color}" opacity="0.85" stroke="black" stroke-width="2"/>
                <!-- Some vertices marked -->
                <circle cx="0" cy="-60" r="3" fill="darkblue"/>
                <circle cx="-57" cy="-19" r="3" fill="darkblue"/>
                <circle cx="-35" cy="49" r="3" fill="darkblue"/>
                <circle cx="35" cy="49" r="3" fill="darkblue"/>
                <circle cx="57" cy="-19" r="3" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Dodecahedron</text>
                <text x="-120" y="90" font-size="10" fill="gray">20 vertices, 30 edges, 12 faces</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "icosahedron":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <!-- Multiple triangular faces -->
                <path d="M 0,-70 L -40,-20 L 40,-20 Z" fill="{color}" stroke="black" stroke-width="2"/>
                <path d="M -40,-20 L -60,30 L 0,10 Z" fill="{color}" opacity="0.9" stroke="black" stroke-width="2"/>
                <path d="M 40,-20 L 0,10 L 60,30 Z" fill="{color}" opacity="0.85" stroke="black" stroke-width="2"/>
                <path d="M 0,10 L -60,30 L -30,60 Z" fill="{color}" opacity="0.8" stroke="black" stroke-width="2"/>
                <path d="M 0,10 L 30,60 L 60,30 Z" fill="{color}" opacity="0.75" stroke="black" stroke-width="2"/>
                <!-- Some vertices marked -->
                <circle cx="0" cy="-70" r="3" fill="darkblue"/>
                <circle cx="-40" cy="-20" r="3" fill="darkblue"/>
                <circle cx="40" cy="-20" r="3" fill="darkblue"/>
                <circle cx="0" cy="10" r="3" fill="darkblue"/>
                <text x="-120" y="-80" font-size="12" fill="black">Icosahedron</text>
                <text x="-120" y="90" font-size="10" fill="gray">12 vertices, 30 edges, 20 faces</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "cylinder":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <defs>
                <linearGradient id="cylGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:{color};stop-opacity:0.7" />
                    <stop offset="50%" style="stop-color:{color};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{color};stop-opacity:0.7" />
                </linearGradient>
            </defs>
            <g transform="translate(150,150)">
                <!-- Top circle -->
                <ellipse cx="0" cy="-50" rx="60" ry="20" fill="{color}" stroke="black" stroke-width="2"/>
                <!-- Body -->
                <rect x="-60" y="-50" width="120" height="100" fill="url(#cylGrad)"/>
                <!-- Bottom circle -->
                <ellipse cx="0" cy="50" rx="60" ry="20" fill="{color}" stroke="black" stroke-width="2"/>
                <!-- Edges marked in red -->
                <line x1="-60" y1="-50" x2="-60" y2="50" stroke="red" stroke-width="3"/>
                <line x1="60" y1="-50" x2="60" y2="50" stroke="red" stroke-width="3"/>
                <text x="-120" y="-80" font-size="12" fill="black">Cylinder</text>
                <text x="-120" y="90" font-size="10" fill="gray">0 vertices, 2 edges, 3 faces</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "cone":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <defs>
                <linearGradient id="coneGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:{color};stop-opacity:0.8" />
                    <stop offset="50%" style="stop-color:{color};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{color};stop-opacity:0.8" />
                </linearGradient>
            </defs>
            <g transform="translate(150,150)">
                <!-- Base circle -->
                <ellipse cx="0" cy="50" rx="70" ry="25" fill="{color}" opacity="0.7" stroke="black" stroke-width="2"/>
                <!-- Cone body -->
                <path d="M 0,-70 L -70,50 L 70,50 Z" fill="url(#coneGrad)" stroke="black" stroke-width="2"/>
                <!-- Apex vertex -->
                <circle cx="0" cy="-70" r="5" fill="darkblue"/>
                <!-- Edge indicator in red -->
                <ellipse cx="0" cy="50" rx="70" ry="25" fill="none" stroke="red" stroke-width="3"/>
                <text x="-120" y="-80" font-size="12" fill="black">Cone</text>
                <text x="-120" y="90" font-size="10" fill="gray">1 vertex, 1 edge, 2 faces</text>
            </g>
        </svg>
        '''
    
    elif shape_name == "sphere":
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <defs>
                <radialGradient id="sphereGrad">
                    <stop offset="0%" style="stop-color:{color};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:{color};stop-opacity:0.6" />
                </radialGradient>
            </defs>
            <g transform="translate(150,150)">
                <!-- Sphere -->
                <circle cx="0" cy="0" r="80" fill="url(#sphereGrad)" stroke="black" stroke-width="2"/>
                <!-- Equator line for reference -->
                <ellipse cx="0" cy="0" rx="80" ry="25" fill="none" stroke="gray" stroke-width="1" stroke-dasharray="5,5" opacity="0.5"/>
                <text x="-120" y="-100" font-size="12" fill="black">Sphere</text>
                <text x="-120" y="100" font-size="10" fill="gray">0 vertices, 0 edges, 1 face</text>
            </g>
        </svg>
        '''
    
    # Default
    else:
        return f'''
        <svg width="300" height="300" viewBox="0 0 300 300">
            <g transform="translate(150,150)">
                <rect x="-50" y="-50" width="100" height="100" 
                      fill="{color}" stroke="black" stroke-width="2"/>
                <text x="-40" y="0" font-size="14" fill="black">{shape_name}</text>
            </g>
        </svg>
        '''

def generate_counting_question(difficulty):
    """Generate a counting question based on difficulty with all 17 shapes"""
    
    # Define what to count
    count_types = ["vertices", "edges", "faces"]
    count_type = random.choice(count_types)
    
    # Complete shape data for all 17 shapes
    all_shapes = {
        "cube": {"name": "cube", "display_name": "Cube", "vertices": 8, "edges": 12, "faces": 6,
                 "hint": "A cube has 6 square faces, all edges equal"},
        "cuboid": {"name": "cuboid", "display_name": "Cuboid (Rectangular Prism)", "vertices": 8, "edges": 12, "faces": 6,
                   "hint": "A cuboid has 6 rectangular faces"},
        "triangular_prism": {"name": "triangular_prism", "display_name": "Triangular Prism", "vertices": 6, "edges": 9, "faces": 5,
                             "hint": "2 triangular faces + 3 rectangular faces"},
        "pentagonal_prism": {"name": "pentagonal_prism", "display_name": "Pentagonal Prism", "vertices": 10, "edges": 15, "faces": 7,
                             "hint": "2 pentagonal faces + 5 rectangular faces"},
        "hexagonal_prism": {"name": "hexagonal_prism", "display_name": "Hexagonal Prism", "vertices": 12, "edges": 18, "faces": 8,
                            "hint": "2 hexagonal faces + 6 rectangular faces"},
        "octagonal_prism": {"name": "octagonal_prism", "display_name": "Octagonal Prism", "vertices": 16, "edges": 24, "faces": 10,
                           "hint": "2 octagonal faces + 8 rectangular faces"},
        "triangular_pyramid": {"name": "triangular_pyramid", "display_name": "Triangular Pyramid (Tetrahedron)", 
                               "vertices": 4, "edges": 6, "faces": 4,
                               "hint": "All 4 faces are triangles"},
        "square_pyramid": {"name": "square_pyramid", "display_name": "Square Pyramid", "vertices": 5, "edges": 8, "faces": 5,
                          "hint": "1 square base + 4 triangular faces"},
        "rectangular_pyramid": {"name": "rectangular_pyramid", "display_name": "Rectangular Pyramid", "vertices": 5, "edges": 8, "faces": 5,
                               "hint": "1 rectangular base + 4 triangular faces"},
        "pentagonal_pyramid": {"name": "pentagonal_pyramid", "display_name": "Pentagonal Pyramid", "vertices": 6, "edges": 10, "faces": 6,
                              "hint": "1 pentagonal base + 5 triangular faces"},
        "hexagonal_pyramid": {"name": "hexagonal_pyramid", "display_name": "Hexagonal Pyramid", "vertices": 7, "edges": 12, "faces": 7,
                             "hint": "1 hexagonal base + 6 triangular faces"},
        "octahedron": {"name": "octahedron", "display_name": "Octahedron", "vertices": 6, "edges": 12, "faces": 8,
                      "hint": "8 triangular faces, like two pyramids joined at base"},
        "dodecahedron": {"name": "dodecahedron", "display_name": "Dodecahedron", "vertices": 20, "edges": 30, "faces": 12,
                        "hint": "12 pentagonal faces"},
        "icosahedron": {"name": "icosahedron", "display_name": "Icosahedron", "vertices": 12, "edges": 30, "faces": 20,
                       "hint": "20 triangular faces"},
        "cylinder": {"name": "cylinder", "display_name": "Cylinder", "vertices": 0, "edges": 2, "faces": 3,
                    "hint": "2 circular faces + 1 curved surface, edges where circles meet curved surface"},
        "cone": {"name": "cone", "display_name": "Cone", "vertices": 1, "edges": 1, "faces": 2,
                "hint": "1 apex vertex, 1 circular edge, 1 circular face + 1 curved surface"},
        "sphere": {"name": "sphere", "display_name": "Sphere", "vertices": 0, "edges": 0, "faces": 1,
                  "hint": "Only 1 curved surface, no vertices or edges"}
    }
    
    # Select shapes based on difficulty
    if difficulty == 1:
        # Level 1: Basic shapes
        shape_names = ["cube", "cuboid", "triangular_prism", "triangular_pyramid", "square_pyramid"]
    elif difficulty == 2:
        # Level 2: More prisms and simple pyramids
        shape_names = ["pentagonal_prism", "hexagonal_prism", "rectangular_pyramid", 
                      "pentagonal_pyramid", "triangular_prism"]
    elif difficulty == 3:
        # Level 3: Complex pyramids and basic curved surfaces
        shape_names = ["hexagonal_pyramid", "cylinder", "cone", "square_pyramid", "pentagonal_pyramid"]
    elif difficulty == 4:
        # Level 4: Regular polyhedra
        shape_names = ["octahedron", "dodecahedron", "icosahedron", "octagonal_prism"]
    else:  # difficulty 5
        # Level 5: Mix of all including sphere
        shape_names = ["sphere", "dodecahedron", "icosahedron", "octahedron", 
                      "cylinder", "cone", "octagonal_prism"]
    
    # Select a random shape from the appropriate difficulty
    shape_name = random.choice(shape_names)
    selected_shape = all_shapes[shape_name].copy()
    selected_shape["color"] = random.choice(["#FFB3D9", "#FFD4B3", "#B3E5FF", "#D4FFB3", 
                                            "#FFE6B3", "#E6B3FF", "#B3FFE6"])
    
    # Build the question
    question_data = {
        "shape": selected_shape,
        "count_type": count_type,
        "correct_answer": selected_shape[count_type],
        "difficulty": difficulty
    }
    
    return question_data

def display_counting_question():
    """Display the current counting question"""
    question_data = st.session_state.current_counting_question
    shape = question_data["shape"]
    count_type = question_data["count_type"]
    
    # Format the question
    question_text = f"How many **{count_type}** does this shape have?"
    
    # Display shape name and question
    st.markdown(f"### {shape['display_name']}")
    st.markdown(question_text)
    
    # Render the SVG shape
    render_shape_svg(shape["name"], shape["color"])
    
    # Create input field if not submitted
    if not st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Input field for answer
            user_answer = st.number_input(
                f"{count_type}",
                min_value=0,
                max_value=50,
                step=1,
                key="answer_input"
            )
            st.session_state.user_answer = user_answer
            
            # Submit button
            if st.button("✅ Submit", type="primary", use_container_width=True):
                if st.session_state.user_answer is not None:
                    st.session_state.answer_submitted = True
                    st.session_state.show_feedback = True
                    st.rerun()
    
    # Show hint button
    if not st.session_state.answer_submitted:
        with st.expander("💭 Need a hint?"):
            st.info(f"**Hint:** {shape['hint']}")
            
            # Additional hint based on count type
            if count_type == "vertices":
                st.markdown("🔵 **Vertices** are the corners/points where edges meet")
            elif count_type == "edges":
                st.markdown("📏 **Edges** are the line segments or boundaries")
            elif count_type == "faces":
                st.markdown("⬜ **Faces** are the flat or curved surfaces")

def get_step_by_step_solution(shape, count_type):
    """Generate step-by-step solution for counting"""
    
    steps = []
    shape_name = shape["display_name"]
    
    if count_type == "vertices":
        steps.append("### 🔵 How to Count Vertices (Corners):")
        steps.append("**Step 1:** Identify what vertices are - they are the corners or points where edges meet.")
        
        if "prism" in shape_name.lower():
            steps.append(f"**Step 2:** For a prism, count vertices on the front face first.")
            steps.append(f"**Step 3:** Count the same number of vertices on the back face.")
            steps.append(f"**Step 4:** Total vertices = front vertices + back vertices")
            if shape["name"] == "triangular_prism":
                steps.append("- Front triangle: 3 vertices")
                steps.append("- Back triangle: 3 vertices")
                steps.append("- Total: 3 + 3 = **6 vertices**")
            elif shape["name"] == "hexagonal_prism":
                steps.append("- Front hexagon: 6 vertices")
                steps.append("- Back hexagon: 6 vertices")
                steps.append("- Total: 6 + 6 = **12 vertices**")
        
        elif "pyramid" in shape_name.lower():
            steps.append(f"**Step 2:** For a pyramid, count the apex (top point) first: 1 vertex")
            steps.append(f"**Step 3:** Count vertices on the base shape.")
            steps.append(f"**Step 4:** Total = 1 (apex) + base vertices")
            if shape["name"] == "square_pyramid":
                steps.append("- Apex: 1 vertex")
                steps.append("- Square base: 4 vertices")
                steps.append("- Total: 1 + 4 = **5 vertices**")
        
        elif shape["name"] in ["cylinder", "cone", "sphere"]:
            if shape["name"] == "cylinder":
                steps.append("**Step 2:** A cylinder has no corners - it has smooth circular edges.")
                steps.append("**Answer:** **0 vertices**")
            elif shape["name"] == "cone":
                steps.append("**Step 2:** A cone has only one vertex at the apex (tip).")
                steps.append("**Answer:** **1 vertex**")
            elif shape["name"] == "sphere":
                steps.append("**Step 2:** A sphere is completely smooth with no corners.")
                steps.append("**Answer:** **0 vertices**")
    
    elif count_type == "edges":
        steps.append("### 📏 How to Count Edges:")
        steps.append("**Step 1:** Edges are the line segments where two faces meet.")
        
        if "prism" in shape_name.lower():
            steps.append(f"**Step 2:** For a prism, count edges in three groups:")
            steps.append("- Edges on the front face")
            steps.append("- Edges on the back face")
            steps.append("- Connecting edges between front and back")
            if shape["name"] == "triangular_prism":
                steps.append("**Step 3:** Triangle has 3 edges, so:")
                steps.append("- Front: 3 edges")
                steps.append("- Back: 3 edges")
                steps.append("- Connecting: 3 edges")
                steps.append("- Total: 3 + 3 + 3 = **9 edges**")
        
        elif "pyramid" in shape_name.lower():
            steps.append(f"**Step 2:** For a pyramid, count:")
            steps.append("- Edges on the base")
            steps.append("- Edges from base corners to apex")
            if shape["name"] == "square_pyramid":
                steps.append("**Step 3:** Square base has 4 edges")
                steps.append("**Step 4:** 4 edges connect to apex")
                steps.append("- Total: 4 + 4 = **8 edges**")
        
        elif shape["name"] in ["cylinder", "cone", "sphere"]:
            if shape["name"] == "cylinder":
                steps.append("**Step 2:** A cylinder has 2 circular edges where the circles meet the curved surface.")
                steps.append("**Answer:** **2 edges**")
            elif shape["name"] == "cone":
                steps.append("**Step 2:** A cone has 1 circular edge at the base.")
                steps.append("**Answer:** **1 edge**")
            elif shape["name"] == "sphere":
                steps.append("**Step 2:** A sphere has no edges - it's completely smooth.")
                steps.append("**Answer:** **0 edges**")
    
    elif count_type == "faces":
        steps.append("### ⬜ How to Count Faces:")
        steps.append("**Step 1:** Faces are the flat or curved surfaces of the shape.")
        
        if "prism" in shape_name.lower():
            steps.append(f"**Step 2:** For a prism, count:")
            steps.append("- 2 identical base faces (front and back)")
            steps.append("- Rectangular side faces")
            if shape["name"] == "triangular_prism":
                steps.append("**Step 3:** Count the faces:")
                steps.append("- 2 triangular faces")
                steps.append("- 3 rectangular faces")
                steps.append("- Total: 2 + 3 = **5 faces**")
        
        elif "pyramid" in shape_name.lower():
            steps.append(f"**Step 2:** For a pyramid, count:")
            steps.append("- 1 base face")
            steps.append("- Triangular faces (one for each base edge)")
            if shape["name"] == "square_pyramid":
                steps.append("**Step 3:** Count the faces:")
                steps.append("- 1 square base")
                steps.append("- 4 triangular faces")
                steps.append("- Total: 1 + 4 = **5 faces**")
        
        elif shape["name"] in ["cylinder", "cone", "sphere"]:
            if shape["name"] == "cylinder":
                steps.append("**Step 2:** A cylinder has:")
                steps.append("- 2 circular faces (top and bottom)")
                steps.append("- 1 curved surface")
                steps.append("**Total:** **3 faces**")
            elif shape["name"] == "cone":
                steps.append("**Step 2:** A cone has:")
                steps.append("- 1 circular base")
                steps.append("- 1 curved surface")
                steps.append("**Total:** **2 faces**")
            elif shape["name"] == "sphere":
                steps.append("**Step 2:** A sphere has only 1 curved surface.")
                steps.append("**Answer:** **1 face**")
    
    # Add final answer
    steps.append(f"\n**✅ Final Answer: {shape[count_type]} {count_type}**")
    
    return steps

def handle_counting_feedback():
    """Handle feedback for the counting question with step-by-step solutions"""
    if st.session_state.show_feedback and st.session_state.answer_submitted:
        question_data = st.session_state.current_counting_question
        shape = question_data["shape"]
        count_type = question_data["count_type"]
        correct_answer = question_data["correct_answer"]
        user_answer = int(st.session_state.user_answer)
        
        # Check if answer is correct
        is_correct = (user_answer == correct_answer)
        
        if is_correct:
            st.success(f"🎉 **Excellent! That's correct!**")
            st.info(f"✅ The {shape['display_name']} has **{correct_answer} {count_type}**")
            
            # Show all properties
            with st.expander("📊 Complete shape properties"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Vertices", shape["vertices"])
                with col2:
                    st.metric("Edges", shape["edges"])
                with col3:
                    st.metric("Faces", shape["faces"])
                
                # Show Euler's formula for polyhedra
                if shape["name"] not in ["cylinder", "cone", "sphere"]:
                    euler = shape["vertices"] - shape["edges"] + shape["faces"]
                    if euler == 2:
                        st.success(f"✓ Euler's Formula: V - E + F = {shape['vertices']} - {shape['edges']} + {shape['faces']} = 2")
                    else:
                        st.warning(f"Note: V - E + F = {euler} (Special polyhedron)")
            
            # Update stats
            st.session_state.total_correct += 1
            st.session_state.consecutive_correct += 1
            
            # Check for level up
            if st.session_state.consecutive_correct >= 3:
                old_difficulty = st.session_state.count_3d_difficulty
                st.session_state.count_3d_difficulty = min(5, old_difficulty + 1)
                st.session_state.consecutive_correct = 0
                
                if st.session_state.count_3d_difficulty > old_difficulty:
                    st.balloons()
                    st.success(f"🎯 **Level Up! You're now on Level {st.session_state.count_3d_difficulty}!**")
        
        else:
            st.error(f"❌ **Not quite right.**")
            st.warning(f"The correct answer is **{correct_answer} {count_type}**")
            st.info(f"You answered: **{user_answer}**")
            
            # Show step-by-step solution
            with st.expander("📚 **Step-by-Step Solution**", expanded=True):
                steps = get_step_by_step_solution(shape, count_type)
                for step in steps:
                    st.markdown(step)
                
                # Show visual breakdown
                st.markdown("---")
                st.markdown("### 📊 Complete Properties:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if count_type == "vertices":
                        st.markdown(f"**🔵 {shape['vertices']} vertices** ← We were counting this")
                    else:
                        st.markdown(f"🔵 {shape['vertices']} vertices")
                
                with col2:
                    if count_type == "edges":
                        st.markdown(f"**📏 {shape['edges']} edges** ← We were counting this")
                    else:
                        st.markdown(f"📏 {shape['edges']} edges")
                
                with col3:
                    if count_type == "faces":
                        st.markdown(f"**⬜ {shape['faces']} faces** ← We were counting this")
                    else:
                        st.markdown(f"⬜ {shape['faces']} faces")
                
                st.markdown(f"\n**💡 Remember:** {shape['hint']}")
            
            # Reset consecutive correct
            st.session_state.consecutive_correct = 0
        
        st.session_state.total_attempted += 1
        
        # Show statistics
        if st.session_state.total_attempted > 0:
            accuracy = (st.session_state.total_correct / st.session_state.total_attempted) * 100
            st.markdown(f"**📊 Score:** {st.session_state.total_correct}/{st.session_state.total_attempted} ({accuracy:.0f}%)")
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                st.session_state.current_counting_question = None
                st.session_state.show_feedback = False
                st.session_state.answer_submitted = False
                st.session_state.user_answer = ""
                st.rerun()