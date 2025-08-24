import streamlit as st
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Wedge, Rectangle, Polygon
import numpy as np
import math

def run():
    """
    Main function to run the Compare Fractions with Like Denominators Using Models activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/compare_fractions_with_like_denominators_using_models.py
    """
    # Initialize session state
    if "like_fractions_level" not in st.session_state:
        st.session_state.like_fractions_level = 1
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_fraction = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("📊 Compare Fractions with Like Denominators Using Models")
    st.markdown("*Use visual models to compare fractions with the same denominator*")
    st.markdown("---")
    
    # Add custom CSS for button styling
    st.markdown("""
    <style>
    /* Style for fraction buttons */
    .stButton > button {
        min-height: 60px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        border: 2px solid #c3c7cf !important;
    }
    
    /* Selected button style */
    .stButton > button[kind="primary"] {
        background-color: #d1e7ff !important;
        border: 2px solid #0066cc !important;
        color: #0066cc !important;
    }
    
    /* Hover effect */
    .stButton > button:hover {
        transform: scale(1.02);
        transition: transform 0.2s;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Difficulty indicator
    difficulty_level = st.session_state.like_fractions_level
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = ["Simple fractions", "Standard fractions", "Complex fractions"][min(difficulty_level-1, 2)]
        st.markdown(f"**Current Level:** {difficulty_text}")
        progress = min(difficulty_level / 3, 1.0)
        st.progress(progress, text=difficulty_text)
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Standard**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("### How to Play:")
        st.markdown("- **Look at the visual models** showing two fractions")
        st.markdown("- **Count the shaded parts** in each model")
        st.markdown("- **Compare the fractions** and select the correct answer")
        st.markdown("- **Remember:** Both fractions have the same denominator (bottom number)")
        
        st.markdown("### Key Concept:")
        st.markdown("When fractions have the **same denominator:**")
        st.markdown("- Just compare the **numerators** (top numbers)")
        st.markdown("- Bigger numerator = Bigger fraction")
        st.markdown("- More shaded parts = Larger fraction")
        
        st.markdown("### Examples:")
        st.markdown("- **3/5 > 2/5** (3 parts > 2 parts)")
        st.markdown("- **4/8 < 6/8** (4 parts < 6 parts)")
        st.markdown("- **7/10 > 5/10** (7 parts > 5 parts)")
        
        st.markdown("### Visual Tip:")
        st.markdown("- The model with **more colored sections** represents the larger fraction")
        st.markdown("- Count carefully - the total parts are the same in both models!")

def generate_new_question():
    """Generate a new like denominators comparison question"""
    difficulty = st.session_state.like_fractions_level
    
    # Define denominator ranges based on difficulty
    if difficulty == 1:
        # Basic: Small denominators
        denominators = [3, 4, 5, 6]
    elif difficulty == 2:
        # Standard: Medium denominators
        denominators = [5, 6, 8, 10]
    else:
        # Advanced: Larger denominators
        denominators = [8, 10, 12, 15, 16]
    
    # Select a denominator
    denominator = random.choice(denominators)
    
    # Generate two different numerators
    possible_numerators = list(range(1, denominator))
    num1, num2 = random.sample(possible_numerators, 2)
    
    # Create the fractions
    fraction1 = (num1, denominator)
    fraction2 = (num2, denominator)
    
    # Choose shape type based on denominator for better visual representation
    shape_types = ["circle", "rectangle", "triangle", "diamond"]
    if denominator == 3:
        shape_type = "triangle"  # Triangles work well for thirds
    elif denominator == 4:
        shape_type = random.choice(["rectangle", "diamond", "circle"])  # All work well for fourths
    elif denominator == 5:
        shape_type = random.choice(["circle", "diamond"])  # These work well for fifths
    elif denominator % 2 == 0 and denominator <= 8:
        shape_type = random.choice(["rectangle", "circle"])  # Even numbers work well with rectangles
    else:
        shape_type = "circle"  # Default to circle for other cases
    
    # Randomly decide whether to ask for less or greater
    comparison_type = random.choice(["less", "greater"])
    
    # Store question data
    st.session_state.question_data = {
        "fraction1": fraction1,
        "fraction2": fraction2,
        "comparison_type": comparison_type,
        "shape_type": shape_type,
        "correct_answer": None
    }
    
    # Determine correct answer
    if comparison_type == "less":
        st.session_state.question_data["correct_answer"] = fraction1 if num1 < num2 else fraction2
        st.session_state.current_question = "Which fraction is less?"
    else:
        st.session_state.question_data["correct_answer"] = fraction1 if num1 > num2 else fraction2
        st.session_state.current_question = "Which fraction is greater?"
    
    # Reset selection
    st.session_state.selected_fraction = None

def create_visual_models(fraction1, fraction2, shape_type):
    """Create visual models for the two fractions"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.patch.set_facecolor('white')
    
    # Colors for shaded parts - choose different colors for variety
    colors = ['#87CEEB', '#FFA07A', '#90EE90', '#98FB98', '#FFB6C1']  # Light blue, salmon, light green, pale green, light pink
    color1 = random.choice(colors)
    color2 = random.choice([c for c in colors if c != color1])  # Ensure different colors
    
    for ax, fraction, color in [(ax1, fraction1, color1), (ax2, fraction2, color2)]:
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')
        
        numerator, denominator = fraction
        
        if shape_type == "circle":
            # Draw circle divided into equal parts
            for i in range(denominator):
                angle1 = i * 360 / denominator
                angle2 = (i + 1) * 360 / denominator
                
                # Determine if this section should be shaded
                if i < numerator:
                    wedge = Wedge((0, 0), 1, angle1, angle2, 
                                 facecolor=color, edgecolor='black', linewidth=2)
                else:
                    wedge = Wedge((0, 0), 1, angle1, angle2, 
                                 facecolor='white', edgecolor='black', linewidth=2)
                ax.add_patch(wedge)
        
        elif shape_type == "rectangle":
            # Draw rectangle divided into equal parts
            if denominator <= 6:
                # Vertical divisions
                width = 2 / denominator
                for i in range(denominator):
                    x = -1 + i * width
                    if i < numerator:
                        rect = Rectangle((x, -0.5), width, 1, 
                                       facecolor=color, edgecolor='black', linewidth=2)
                    else:
                        rect = Rectangle((x, -0.5), width, 1, 
                                       facecolor='white', edgecolor='black', linewidth=2)
                    ax.add_patch(rect)
            else:
                # Grid layout for larger denominators
                cols = int(np.sqrt(denominator))
                rows = int(np.ceil(denominator / cols))
                cell_width = 2 / cols
                cell_height = 2 / rows
                
                for i in range(denominator):
                    row = i // cols
                    col = i % cols
                    x = -1 + col * cell_width
                    y = 1 - (row + 1) * cell_height
                    
                    if i < numerator:
                        rect = Rectangle((x, y), cell_width, cell_height,
                                       facecolor=color, edgecolor='black', linewidth=2)
                    else:
                        rect = Rectangle((x, y), cell_width, cell_height,
                                       facecolor='white', edgecolor='black', linewidth=2)
                    ax.add_patch(rect)
        
        elif shape_type == "triangle":
            # Draw triangular divisions
            if denominator == 3:
                # Special case for thirds - equilateral triangle divided into 3
                h = np.sqrt(3) / 2
                
                # Main triangle vertices
                main_points = [(-0.5, -h/2), (0.5, -h/2), (0, h/2)]
                
                # Draw the main triangle outline
                main_triangle = Polygon(main_points, facecolor='none', 
                                      edgecolor='black', linewidth=3)
                ax.add_patch(main_triangle)
                
                # Draw internal lines from center to vertices
                ax.plot([0, -0.5], [0, -h/2], 'k-', linewidth=2)
                ax.plot([0, 0.5], [0, -h/2], 'k-', linewidth=2)
                ax.plot([0, 0], [0, h/2], 'k-', linewidth=2)
                
                # Draw the three sections (from center outward)
                sections = [
                    [(0, 0), (-0.5, -h/2), (0, h/2)],   # Left section
                    [(0, 0), (0, h/2), (0.5, -h/2)],    # Right section
                    [(0, 0), (0.5, -h/2), (-0.5, -h/2)] # Bottom section
                ]
                
                for i, section_points in enumerate(sections):
                    if i < numerator:
                        triangle = Polygon(section_points, facecolor=color,
                                         edgecolor='black', linewidth=2, alpha=0.8)
                    else:
                        triangle = Polygon(section_points, facecolor='white',
                                         edgecolor='black', linewidth=2)
                    ax.add_patch(triangle)
            else:
                # For other denominators, use pie-like triangular sections
                for i in range(denominator):
                    angle1 = i * 2 * np.pi / denominator - np.pi/2
                    angle2 = (i + 1) * 2 * np.pi / denominator - np.pi/2
                    
                    x1, y1 = np.cos(angle1), np.sin(angle1)
                    x2, y2 = np.cos(angle2), np.sin(angle2)
                    
                    points = [(0, 0), (x1, y1), (x2, y2)]
                    
                    if i < numerator:
                        triangle = Polygon(points, facecolor=color, 
                                         edgecolor='black', linewidth=2)
                    else:
                        triangle = Polygon(points, facecolor='white', 
                                         edgecolor='black', linewidth=2)
                    ax.add_patch(triangle)
        
        elif shape_type == "diamond":
            # Draw diamond (square rotated 45 degrees) divided into parts
            # Main diamond outline
            diamond_points = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            diamond = Polygon(diamond_points, facecolor='none', 
                            edgecolor='black', linewidth=3)
            ax.add_patch(diamond)
            
            if denominator == 4:
                # Special case for fourths - diamond quarters
                # Draw diagonal lines
                ax.plot([-1, 1], [0, 0], 'k-', linewidth=2)
                ax.plot([0, 0], [-1, 1], 'k-', linewidth=2)
                
                # Draw the four triangular sections
                sections = [
                    [(0, 0), (0, 1), (-1, 0)],  # Top left
                    [(0, 0), (0, 1), (1, 0)],   # Top right
                    [(0, 0), (1, 0), (0, -1)],  # Bottom right
                    [(0, 0), (0, -1), (-1, 0)]  # Bottom left
                ]
                
                for i, section_points in enumerate(sections):
                    if i < numerator:
                        triangle = Polygon(section_points, facecolor=color,
                                         edgecolor='black', linewidth=2, alpha=0.8)
                    else:
                        triangle = Polygon(section_points, facecolor='white',
                                         edgecolor='black', linewidth=2)
                    ax.add_patch(triangle)
            elif denominator == 5:
                # Special case for fifths - pentagon-like divisions
                # Draw lines from center to vertices and one additional point
                angles = [np.pi/2, np.pi/2 + 2*np.pi/5, np.pi/2 + 4*np.pi/5, 
                         np.pi/2 + 6*np.pi/5, np.pi/2 + 8*np.pi/5]
                
                # Map angles to diamond edges
                edge_points = []
                for angle in angles:
                    x, y = np.cos(angle), np.sin(angle)
                    # Find intersection with diamond edge
                    if abs(x) + abs(y) > 0:
                        scale = 1 / (abs(x) + abs(y))
                        edge_points.append((x * scale, y * scale))
                
                # Draw lines from center to edge points
                for point in edge_points:
                    ax.plot([0, point[0]], [0, point[1]], 'k-', linewidth=2)
                
                # Fill sections
                for i in range(denominator):
                    p1 = edge_points[i]
                    p2 = edge_points[(i + 1) % denominator]
                    section_points = [(0, 0), p1, p2]
                    
                    if i < numerator:
                        triangle = Polygon(section_points, facecolor=color,
                                         edgecolor='black', linewidth=2, alpha=0.8)
                    else:
                        triangle = Polygon(section_points, facecolor='white',
                                         edgecolor='black', linewidth=2)
                    ax.add_patch(triangle)
            else:
                # For other denominators, divide into equal triangular sections
                for i in range(denominator):
                    angle1 = i * 2 * np.pi / denominator
                    angle2 = (i + 1) * 2 * np.pi / denominator
                    
                    # Find points on diamond perimeter
                    x1, y1 = np.cos(angle1), np.sin(angle1)
                    x2, y2 = np.cos(angle2), np.sin(angle2)
                    
                    # Scale to diamond edge
                    scale1 = 1 / (abs(x1) + abs(y1)) if (abs(x1) + abs(y1)) > 0 else 1
                    scale2 = 1 / (abs(x2) + abs(y2)) if (abs(x2) + abs(y2)) > 0 else 1
                    
                    x1, y1 = x1 * scale1, y1 * scale1
                    x2, y2 = x2 * scale2, y2 * scale2
                    
                    points = [(0, 0), (x1, y1), (x2, y2)]
                    
                    if i < numerator:
                        triangle = Polygon(points, facecolor=color,
                                         edgecolor='black', linewidth=2, alpha=0.8)
                    else:
                        triangle = Polygon(points, facecolor='white',
                                         edgecolor='black', linewidth=2)
                    ax.add_patch(triangle)
        
        # Add fraction label above the shape
        ax.text(0, 1.3, f"{numerator}/{denominator}", 
                ha='center', va='bottom', fontsize=20, fontweight='bold')
    
    plt.tight_layout()
    return fig

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### {st.session_state.current_question}")
    
    # Create and display visual models
    fig = create_visual_models(data['fraction1'], data['fraction2'], data['shape_type'])
    st.pyplot(fig)
    plt.close()
    
    # Create fraction tiles for selection
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Use columns for side-by-side tiles
    col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1.5])
    
    frac1_str = f"{data['fraction1'][0]}/{data['fraction1'][1]}"
    frac2_str = f"{data['fraction2'][0]}/{data['fraction2'][1]}"
    
    with col2:
        # First fraction tile
        if st.button(
            frac1_str,
            key="frac1_button",
            use_container_width=True,
            type="secondary" if st.session_state.selected_fraction != frac1_str else "primary",
            help=f"Click to select {frac1_str}"
        ):
            st.session_state.selected_fraction = frac1_str
            st.rerun()
    
    with col3:
        # Second fraction tile
        if st.button(
            frac2_str,
            key="frac2_button",
            use_container_width=True,
            type="secondary" if st.session_state.selected_fraction != frac2_str else "primary",
            help=f"Click to select {frac2_str}"
        ):
            st.session_state.selected_fraction = frac2_str
            st.rerun()
    
    # Show selection status
    if st.session_state.selected_fraction is None and not st.session_state.answer_submitted:
        st.info("👆 Click on a fraction to select your answer")
    elif st.session_state.selected_fraction is not None and not st.session_state.answer_submitted:
        st.success(f"✔️ You selected: **{st.session_state.selected_fraction}**")
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        submit_disabled = st.session_state.selected_fraction is None or st.session_state.answer_submitted
        if st.button("Submit", type="primary", use_container_width=True, disabled=submit_disabled):
            # Parse the selected answer back to tuple format
            parts = st.session_state.selected_fraction.split('/')
            selected_tuple = (int(parts[0]), int(parts[1]))
            st.session_state.user_answer = selected_tuple
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.question_data["correct_answer"]
    comparison_type = st.session_state.question_data["comparison_type"]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Excellent work!**")
        
        # Quick explanation
        st.info(f"**{correct_answer[0]}/{correct_answer[1]}** has {correct_answer[0]} shaded parts out of {correct_answer[1]} total parts.")
        
        # Increase difficulty
        old_level = st.session_state.like_fractions_level
        st.session_state.like_fractions_level = min(st.session_state.like_fractions_level + 1, 3)
        
        if st.session_state.like_fractions_level > old_level:
            if st.session_state.like_fractions_level == 3:
                st.balloons()
    else:
        correct_str = f"{correct_answer[0]}/{correct_answer[1]}"
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_str}**.")
        
        # Decrease difficulty
        st.session_state.like_fractions_level = max(st.session_state.like_fractions_level - 1, 1)
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    frac1 = data["fraction1"]
    frac2 = data["fraction2"]
    comparison_type = data["comparison_type"]
    correct = data["correct_answer"]
    
    with st.expander("📖 **See explanation**", expanded=True):
        st.markdown(f"**Comparing:** {frac1[0]}/{frac1[1]} and {frac2[0]}/{frac2[1]}")
        
        # Key insight
        st.markdown("### Same denominators make it easy!")
        st.markdown(f"Both fractions have **{frac1[1]}** total parts")
        st.markdown("So we just compare the **numerators** (shaded parts):")
        
        # Comparison
        st.markdown(f"- {frac1[0]}/{frac1[1]} has **{frac1[0]}** shaded parts")
        st.markdown(f"- {frac2[0]}/{frac2[1]} has **{frac2[0]}** shaded parts")
        
        # Result
        if frac1[0] > frac2[0]:
            st.markdown(f"Since {frac1[0]} > {frac2[0]}, we know {frac1[0]}/{frac1[1]} > {frac2[0]}/{frac2[1]}")
        else:
            st.markdown(f"Since {frac1[0]} < {frac2[0]}, we know {frac1[0]}/{frac1[1]} < {frac2[0]}/{frac2[1]}")
        
        # Answer
        st.markdown("---")
        if comparison_type == "less":
            st.markdown(f"✓ **{correct[0]}/{correct[1]}** is the smaller fraction (fewer shaded parts)")
        else:
            st.markdown(f"✓ **{correct[0]}/{correct[1]}** is the larger fraction (more shaded parts)")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_fraction = None
    if "user_answer" in st.session_state:
        del st.session_state.user_answer