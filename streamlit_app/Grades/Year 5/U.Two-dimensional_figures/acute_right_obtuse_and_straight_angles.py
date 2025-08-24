import streamlit as st
import streamlit.components.v1
import random
import math

def run():
    """
    Main function to run the Angle Classification practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year X/Geometry/acute_right_obtuse_straight_angles.py
    """
    # Initialize session state for difficulty and game state
    if "angle_difficulty" not in st.session_state:
        st.session_state.angle_difficulty = 1  # Start with level 1
    
    if "current_angle_question" not in st.session_state:
        st.session_state.current_angle_question = None
        st.session_state.angle_data = {}
        st.session_state.show_angle_feedback = False
        st.session_state.angle_answer_submitted = False
        st.session_state.consecutive_angle_correct = 0
        st.session_state.total_angle_attempts = 0
        st.session_state.selected_answer = None
    
    # Page header with breadcrumb
    st.markdown("**📐 Geometry > Angles**")
    st.title("📐 Acute, Right, Obtuse and Straight Angles")
    st.markdown("*Identify different types of angles by their measures*")
    st.markdown("---")
    
    # Difficulty and progress indicator
    difficulty_level = st.session_state.angle_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        level_names = {1: "🟢 Beginner", 2: "🟡 Intermediate", 3: "🔴 Advanced"}
        st.markdown(f"**Difficulty:** {level_names.get(difficulty_level, '🔴 Expert')}")
        
        # Progress bar (1 to 3 levels)
        progress = min((difficulty_level - 1) / 2, 1.0)
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if st.session_state.total_angle_attempts > 0:
            accuracy = (st.session_state.consecutive_angle_correct / st.session_state.total_angle_attempts) * 100
            st.metric("Accuracy", f"{accuracy:.0f}%")
        else:
            st.metric("Accuracy", "0%")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_angle_question is None:
        generate_new_angle_question()
    
    # Display current question
    display_angle_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Learn About Angles**", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 Angle Types:
            
            **🔸 Acute Angle**
            - **Less than 90°**
            - Sharp and pointed
            - Examples: 30°, 45°, 60°
            
            **🔸 Right Angle**  
            - **Exactly 90°**
            - Perfect corner shape
            - Forms an "L" shape
            
            **🔸 Obtuse Angle**
            - **Greater than 90° but less than 180°**
            - Wide and open
            - Examples: 120°, 135°, 150°
            
            **🔸 Straight Angle**
            - **Exactly 180°**
            - Forms a straight line
            - No bend or curve
            """)
        
        with col2:
            st.markdown("""
            ### 📏 How to Remember:
            
            **🔸 Acute = "A-cute"**
            - Think "small and cute"
            - Always less than a right angle
            
            **🔸 Right = "Right corner"**
            - Like the corner of a book
            - Square corner = 90°
            
            **🔸 Obtuse = "Obviously big"**
            - Bigger than a right angle
            - Wide and open
            
            **🔸 Straight = "Straight line"**
            - No angle at all, just a line
            - 180° = half a circle
            
            ### 🎯 Quick Tips:
            - Compare to a right angle (90°)
            - Look at how "open" the angle is
            - Practice makes perfect!
            """)

def generate_new_angle_question():
    """Generate a new angle classification question based on difficulty level"""
    difficulty = st.session_state.angle_difficulty
    
    # Define angle ranges for each difficulty level
    if difficulty == 1:
        # Level 1: Clear, obvious angles
        angle_options = [
            (30, "acute"), (45, "acute"), (60, "acute"),
            (90, "right"),
            (120, "obtuse"), (135, "obtuse"), (150, "obtuse"),
            (180, "straight")
        ]
    elif difficulty == 2:
        # Level 2: More varied angles
        angle_options = [
            (15, "acute"), (35, "acute"), (70, "acute"), (85, "acute"),
            (90, "right"),
            (95, "obtuse"), (110, "obtuse"), (140, "obtuse"), (165, "obtuse"),
            (180, "straight")
        ]
    else:
        # Level 3: Challenging angles near boundaries
        angle_options = [
            (10, "acute"), (25, "acute"), (75, "acute"), (89, "acute"),
            (90, "right"),
            (91, "obtuse"), (105, "obtuse"), (125, "obtuse"), (160, "obtuse"), (179, "obtuse"),
            (180, "straight")
        ]
    
    # Randomly select an angle
    angle_measure, correct_type = random.choice(angle_options)
    
    # Generate random orientation and styling
    orientations = [0, 30, 45, 60, 90, 120, 135, 180]
    base_rotation = random.choice(orientations)
    
    # Color options for the angle
    colors = ["#E91E63", "#9C27B0", "#3F51B5", "#2196F3", "#00BCD4", 
              "#4CAF50", "#FF9800", "#FF5722", "#795548"]
    angle_color = random.choice(colors)
    
    # Store question data
    st.session_state.angle_data = {
        "measure": angle_measure,
        "correct_type": correct_type,
        "base_rotation": base_rotation,
        "color": angle_color
    }
    st.session_state.current_angle_question = "Is this angle acute, right, obtuse, or straight?"
    st.session_state.selected_answer = None

def display_angle_question():
    """Display the current angle question interface"""
    data = st.session_state.angle_data
    
    # Display question
    st.markdown("### 📐 Question:")
    st.markdown(f"**{st.session_state.current_angle_question}**")
    
    # Create a large angle visualization
    display_angle_visual(data["measure"], data["color"])
    
    # Display clickable tile options
    display_clickable_tiles()
    
    # Submit button and feedback
    handle_answer_submission()

def display_angle_visual(angle_measure, color):
    """Create a large geometric representation of the angle"""
    
    st.markdown("---")
    
    # Create large SVG representation
    svg_code = create_large_angle_svg(angle_measure, color)
    
    # Display the visual with increased height
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        # Use st.components.v1.html to properly render large SVG
        st.components.v1.html(f"""
        <div style="text-align: center; margin: 20px 0;">
            {svg_code}
        </div>
        """, height=350)
        
        # Add description
        if angle_measure < 90:
            description = f"**Angle: {angle_measure}°** (Less than 90°)"
            type_desc = "Sharp & Pointed"
        elif angle_measure == 90:
            description = f"**Angle: {angle_measure}°** (Exactly 90°)"
            type_desc = "Perfect Corner"
        elif angle_measure < 180:
            description = f"**Angle: {angle_measure}°** (Between 90° and 180°)"
            type_desc = "Wide & Open"
        else:
            description = f"**Angle: {angle_measure}°** (Exactly 180°)"
            type_desc = "Straight Line"
            
        st.markdown(f"<div style='text-align: center; margin: 15px 0; font-size: 18px; color: {color}; font-weight: bold;'>{type_desc}</div>", 
                   unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center; margin: 10px 0; font-size: 16px;'>{description}</div>", 
                   unsafe_allow_html=True)

def create_large_angle_svg(angle_measure, color):
    """Create large SVG representation of angles"""
    
    if angle_measure == 180:
        # Straight angle - horizontal line with arrows
        return f"""
        <svg width="400" height="120" viewBox="0 0 400 120">
            <!-- Horizontal line -->
            <line x1="50" y1="60" x2="350" y2="60" stroke="{color}" stroke-width="4"/>
            <!-- Left arrow -->
            <polygon points="50,60 70,50 70,70" fill="{color}"/>
            <!-- Right arrow -->
            <polygon points="350,60 330,50 330,70" fill="{color}"/>
            <!-- Center point -->
            <circle cx="200" cy="60" r="5" fill="{color}"/>
            <!-- Angle marking -->
            <path d="M 170 45 L 170 75 M 230 45 L 230 75" stroke="{color}" stroke-width="3"/>
        </svg>
        """
    
    elif angle_measure == 90:
        # Right angle with square indicator
        return f"""
        <svg width="320" height="320" viewBox="0 0 320 320">
            <!-- Vertical ray -->
            <line x1="160" y1="160" x2="160" y2="40" stroke="{color}" stroke-width="4"/>
            <!-- Horizontal ray -->
            <line x1="160" y1="160" x2="280" y2="160" stroke="{color}" stroke-width="4"/>
            <!-- Right angle square indicator -->
            <rect x="160" y="130" width="30" height="30" fill="none" stroke="{color}" stroke-width="3"/>
            <!-- Center point -->
            <circle cx="160" cy="160" r="5" fill="{color}"/>
            <!-- Arrow on vertical ray -->
            <polygon points="160,40 150,60 170,60" fill="{color}"/>
            <!-- Arrow on horizontal ray -->
            <polygon points="280,160 260,150 260,170" fill="{color}"/>
        </svg>
        """
    
    elif angle_measure < 90:
        # Acute angle - sharp and pointed
        angle_rad = math.radians(angle_measure)
        end_x = 160 + 120 * math.cos(angle_rad)
        end_y = 160 - 120 * math.sin(angle_rad)
        
        return f"""
        <svg width="320" height="320" viewBox="0 0 320 320">
            <!-- First ray (horizontal) -->
            <line x1="160" y1="160" x2="280" y2="160" stroke="{color}" stroke-width="4"/>
            <!-- Second ray (at angle) -->
            <line x1="160" y1="160" x2="{end_x:.1f}" y2="{end_y:.1f}" stroke="{color}" stroke-width="4"/>
            <!-- Arc to show angle -->
            <path d="M 200 160 A 40 40 0 0 0 {160 + 40 * math.cos(angle_rad):.1f} {160 - 40 * math.sin(angle_rad):.1f}" 
                  fill="none" stroke="{color}" stroke-width="3"/>
            <!-- Center point -->
            <circle cx="160" cy="160" r="5" fill="{color}"/>
            <!-- Arrow on horizontal ray -->
            <polygon points="280,160 260,150 260,170" fill="{color}"/>
            <!-- Arrow on angled ray -->
            <polygon points="{end_x:.1f},{end_y:.1f} {end_x - 20:.1f},{end_y + 10:.1f} {end_x - 20:.1f},{end_y - 10:.1f}" fill="{color}"/>
        </svg>
        """
    
    else:
        # Obtuse angle - wide and open
        angle_rad = math.radians(angle_measure)
        end_x = 160 + 120 * math.cos(angle_rad)
        end_y = 160 - 120 * math.sin(angle_rad)
        
        return f"""
        <svg width="320" height="320" viewBox="0 0 320 320">
            <!-- First ray (horizontal) -->
            <line x1="160" y1="160" x2="280" y2="160" stroke="{color}" stroke-width="4"/>
            <!-- Second ray (at angle) -->
            <line x1="160" y1="160" x2="{end_x:.1f}" y2="{end_y:.1f}" stroke="{color}" stroke-width="4"/>
            <!-- Arc to show wide angle -->
            <path d="M 210 160 A 50 50 0 0 0 {160 + 50 * math.cos(angle_rad):.1f} {160 - 50 * math.sin(angle_rad):.1f}" 
                  fill="none" stroke="{color}" stroke-width="3"/>
            <!-- Center point -->
            <circle cx="160" cy="160" r="5" fill="{color}"/>
            <!-- Arrow on horizontal ray -->
            <polygon points="280,160 260,150 260,170" fill="{color}"/>
            <!-- Arrow on angled ray -->
            <polygon points="{end_x:.1f},{end_y:.1f} {end_x - 20:.1f},{end_y + 10:.1f} {end_x - 20:.1f},{end_y - 10:.1f}" fill="{color}"/>
        </svg>
        """

def display_clickable_tiles():
    """Display clickable answer tiles"""
    st.markdown("---")
    st.markdown("### Select the type of angle:")
    
    # Create 4 columns for the tiles
    cols = st.columns(4)
    
    # Define tile options
    options = [
        ("acute", "🔸 Acute", "#FF6B6B"),
        ("right", "🔸 Right", "#4ECDC4"), 
        ("obtuse", "🔸 Obtuse", "#45B7D1"),
        ("straight", "🔸 Straight", "#96CEB4")
    ]
    
    for i, (value, label, color) in enumerate(options):
        with cols[i]:
            # Check if this option is selected
            is_selected = st.session_state.selected_answer == value
            
            # Create tile using button
            button_style = "primary" if is_selected else "secondary"
            
            if st.button(
                label,
                key=f"tile_{value}",
                type=button_style,
                use_container_width=True,
                help=f"Select {value} angle"
            ):
                st.session_state.selected_answer = value
                st.rerun()

def handle_answer_submission():
    """Handle answer submission and feedback"""
    # Show selected answer
    if st.session_state.selected_answer:
        st.success(f"✅ **Selected:** {st.session_state.selected_answer.title()} angle")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Submit Answer", type="primary", use_container_width=True, 
                    disabled=not st.session_state.selected_answer):
            if st.session_state.selected_answer:
                st.session_state.show_angle_feedback = True
                st.session_state.angle_answer_submitted = True
                st.session_state.total_angle_attempts += 1
                st.rerun()
    
    # Show feedback and next button
    if st.session_state.show_angle_feedback:
        show_angle_feedback()
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_angle_question_state()
                st.rerun()

def show_angle_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.selected_answer
    correct_answer = st.session_state.angle_data["correct_type"]
    angle_measure = st.session_state.angle_data["measure"]
    
    st.markdown("---")
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        st.session_state.consecutive_angle_correct += 1
        
        # Check for difficulty progression
        if st.session_state.consecutive_angle_correct >= 3:
            old_difficulty = st.session_state.angle_difficulty
            st.session_state.angle_difficulty = min(st.session_state.angle_difficulty + 1, 3)
            
            if old_difficulty < st.session_state.angle_difficulty:
                st.balloons()
                st.info(f"🚀 **Level Up! Now at Level {st.session_state.angle_difficulty}**")
                st.session_state.consecutive_angle_correct = 0
    
    else:
        st.error(f"❌ **Not quite right.** This is a **{correct_answer}** angle.")
        st.session_state.consecutive_angle_correct = 0
        
        # Decrease difficulty if struggling
        if st.session_state.angle_difficulty > 1:
            st.session_state.angle_difficulty -= 1
            st.warning(f"⬇️ **Moving to Level {st.session_state.angle_difficulty} for more practice**")
        
        # Show explanation
        show_angle_explanation()

def show_angle_explanation():
    """Show detailed explanation for the correct answer"""
    correct_answer = st.session_state.angle_data["correct_type"]
    angle_measure = st.session_state.angle_data["measure"]
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### 📐 This angle measures **{angle_measure}°**
        
        **Why it's {correct_answer}:**
        """)
        
        if correct_answer == "acute":
            st.markdown(f"""
            - **Acute angles** are **less than 90°**
            - This angle is **{angle_measure}°**, which is less than 90°
            - ✅ **{angle_measure}° < 90°** → Acute angle
            
            **Remember:** Acute = "A-cute" = small and sharp! 🔸
            """)
        
        elif correct_answer == "right":
            st.markdown(f"""
            - **Right angles** are **exactly 90°**
            - This angle is **{angle_measure}°** = 90°
            - ✅ **{angle_measure}° = 90°** → Right angle
            
            **Remember:** Right angles form perfect corners, like the corner of a book! 📚
            """)
        
        elif correct_answer == "obtuse":
            st.markdown(f"""
            - **Obtuse angles** are **greater than 90° but less than 180°**
            - This angle is **{angle_measure}°**, which is greater than 90°
            - ✅ **90° < {angle_measure}° < 180°** → Obtuse angle
            
            **Remember:** Obtuse = "Obviously big" = wide and open! 🔸
            """)
        
        elif correct_answer == "straight":
            st.markdown(f"""
            - **Straight angles** are **exactly 180°**
            - This angle is **{angle_measure}°** = 180°
            - ✅ **{angle_measure}° = 180°** → Straight angle
            
            **Remember:** Straight angles form a perfectly straight line! ➡️
            """)
        
        # Add a visual reference
        st.markdown("""
        ### 📏 Quick Reference:
        - **0° to 89°** → 🔸 Acute (Sharp)
        - **90°** → 🔸 Right (Corner)
        - **91° to 179°** → 🔸 Obtuse (Wide)
        - **180°** → 🔸 Straight (Line)
        """)

def reset_angle_question_state():
    """Reset the question state for next question"""
    st.session_state.current_angle_question = None
    st.session_state.angle_data = {}
    st.session_state.show_angle_feedback = False
    st.session_state.angle_answer_submitted = False
    st.session_state.selected_answer = None