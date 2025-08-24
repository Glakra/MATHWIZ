import streamlit as st
import random

def run():
    """
    Main function to run the What Percentage is Illustrated practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/what_percentage_is_illustrated.py
    """
    # Initialize session state
    if "percentage_difficulty" not in st.session_state:
        st.session_state.percentage_difficulty = 1  # Start with easy patterns
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🎨 What Percentage is Illustrated?")
    st.markdown("*Identify what percentage of the grid is colored*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.percentage_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {1: "Simple Patterns", 2: "Complex Patterns", 3: "Irregular Shapes"}
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=difficulty_names[difficulty_level])
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Easy**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Medium**")
        else:
            st.markdown("**🔴 Hard**")
    
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
        st.markdown("""
        ### How to Play:
        - **Count the colored squares** in the grid
        - **Calculate the percentage** of colored squares
        - **Enter your answer** with the % sign
        
        ### Tips for Success:
        - **Total squares:** The grid has 10×10 = 100 squares
        - **Easy calculation:** Number of colored squares = percentage
        - **Check your count:** Count by rows or patterns to avoid mistakes
        
        ### Examples:
        - **25 colored squares** = 25%
        - **50 colored squares** = 50%
        - **All 100 squares** = 100%
        
        ### Difficulty Levels:
        - **🟢 Easy:** Simple patterns (halves, quarters, full grid)
        - **🟡 Medium:** Complex patterns (checkerboards, borders, crosses)
        - **🔴 Hard:** Irregular shapes (diamonds, L-shapes, frames)
        """)

def generate_new_question():
    """Generate a new percentage question based on difficulty"""
    difficulty = st.session_state.percentage_difficulty
    
    # Define scenarios by difficulty
    easy_scenarios = [
        {
            "pattern": "all_filled",
            "colored_cells": [(i, j) for i in range(10) for j in range(10)],
            "color": "#9C27B0",
            "color_name": "purple",
            "correct_percentage": 100
        },
        {
            "pattern": "half_horizontal",
            "colored_cells": [(i, j) for i in range(5) for j in range(10)],
            "color": "#2196F3",
            "color_name": "blue",
            "correct_percentage": 50
        },
        {
            "pattern": "quarter",
            "colored_cells": [(i, j) for i in range(5) for j in range(5)],
            "color": "#FF5722",
            "color_name": "red",
            "correct_percentage": 25
        },
        {
            "pattern": "three_quarters",
            "colored_cells": [(i, j) for i in range(10) for j in range(10) if not (i >= 5 and j >= 5)],
            "color": "#4CAF50",
            "color_name": "green",
            "correct_percentage": 75
        },
        {
            "pattern": "twenty_percent",
            "colored_cells": [(i, j) for i in range(2) for j in range(10)],
            "color": "#FF9800",
            "color_name": "orange",
            "correct_percentage": 20
        }
    ]
    
    medium_scenarios = [
        {
            "pattern": "border",
            "colored_cells": [(i, j) for i in range(10) for j in range(10) 
                            if i == 0 or i == 9 or j == 0 or j == 9],
            "color": "#E91E63",
            "color_name": "pink",
            "correct_percentage": 36
        },
        {
            "pattern": "checkerboard",
            "colored_cells": [(i, j) for i in range(10) for j in range(10) if (i + j) % 2 == 0],
            "color": "#00BCD4",
            "color_name": "cyan",
            "correct_percentage": 50
        },
        {
            "pattern": "cross",
            "colored_cells": [(i, j) for i in range(10) for j in range(10) 
                            if i == 4 or i == 5 or j == 4 or j == 5],
            "color": "#795548",
            "color_name": "brown",
            "correct_percentage": 36
        },
        {
            "pattern": "diagonal_stripe",
            "colored_cells": [(i, j) for i in range(10) for j in range(10) if i == j],
            "color": "#3F51B5",
            "color_name": "indigo",
            "correct_percentage": 10
        }
    ]
    
    hard_scenarios = [
        {
            "pattern": "L_shape",
            "colored_cells": [(i, j) for i in range(7) for j in range(3)] + 
                           [(7, j) for j in range(7)] + [(8, j) for j in range(7)] + [(9, j) for j in range(7)],
            "color": "#8BC34A",
            "color_name": "light green",
            "correct_percentage": 42
        },
        {
            "pattern": "diamond",
            "colored_cells": [(i, j) for i in range(10) for j in range(10) 
                            if abs(i - 4.5) + abs(j - 4.5) <= 4],
            "color": "#FFC107",
            "color_name": "amber",
            "correct_percentage": 41
        },
        {
            "pattern": "frame_with_hole",
            "colored_cells": [(i, j) for i in range(10) for j in range(10) 
                            if not (2 <= i <= 7 and 2 <= j <= 7)],
            "color": "#9E9E9E",
            "color_name": "gray",
            "correct_percentage": 64
        }
    ]
    
    # Select scenario based on difficulty
    if difficulty == 1:
        scenario = random.choice(easy_scenarios)
    elif difficulty == 2:
        scenario = random.choice(medium_scenarios)
    else:
        scenario = random.choice(hard_scenarios)
    
    # Calculate percentage
    total_squares = 100
    colored_count = len(scenario["colored_cells"])
    
    st.session_state.question_data = {
        "colored_cells": scenario["colored_cells"],
        "color": scenario["color"],
        "color_name": scenario["color_name"],
        "colored_count": colored_count,
        "total_squares": total_squares
    }
    st.session_state.correct_answer = scenario["correct_percentage"]
    st.session_state.current_question = f"What percentage of the shape is {scenario['color_name']}?"

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📝 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Create SVG grid
    grid_size = 10
    cell_size = 30
    svg_width = grid_size * cell_size
    svg_height = grid_size * cell_size
    
    # Convert colored_cells list to a set for faster lookup
    colored_set = set(data["colored_cells"])
    
    svg_cells = ""
    for i in range(grid_size):
        for j in range(grid_size):
            x = j * cell_size
            y = i * cell_size
            if (i, j) in colored_set:
                fill_color = data["color"]
            else:
                fill_color = "white"
            
            svg_cells += f'''<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" 
                             fill="{fill_color}" stroke="#ccc" stroke-width="1"/>'''
    
    svg_html = f'''
    <div style="text-align: center; margin: 30px 0;">
        <svg width="{svg_width}" height="{svg_height}" style="border: 2px solid #333;">
            {svg_cells}
        </svg>
    </div>
    '''
    
    st.markdown(svg_html, unsafe_allow_html=True)
    
    # Answer input
    st.markdown("**Write your answer using a percent sign (%).**")
    
    with st.form("answer_form", clear_on_submit=False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            user_answer = st.text_input(
                "Your answer:",
                key="percentage_input",
                placeholder="e.g., 25%",
                label_visibility="collapsed"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            st.session_state.user_answer = user_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer.strip()
    correct_answer = st.session_state.correct_answer
    
    # Parse user answer
    try:
        if user_answer.endswith('%'):
            user_percentage = int(user_answer[:-1])
            valid_format = True
        else:
            valid_format = False
            st.warning("⚠️ Please include the % sign in your answer (e.g., 25%).")
    except:
        valid_format = False
        st.error("❌ Please enter a valid percentage (e.g., 25%).")
    
    if valid_format:
        if user_percentage == correct_answer:
            st.success("🎉 **Excellent! That's correct!**")
            
            # Increase difficulty
            old_difficulty = st.session_state.percentage_difficulty
            st.session_state.percentage_difficulty = min(
                st.session_state.percentage_difficulty + 1, 3
            )
            
            if st.session_state.percentage_difficulty > old_difficulty:
                st.info(f"⬆️ **Difficulty increased! Now working with more complex patterns.**")
            elif st.session_state.percentage_difficulty == 3:
                st.balloons()
                st.info("🏆 **Outstanding! You've mastered all pattern types!**")
        
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}%**.")
            
            # Decrease difficulty
            old_difficulty = st.session_state.percentage_difficulty
            st.session_state.percentage_difficulty = max(
                st.session_state.percentage_difficulty - 1, 1
            )
            
            if old_difficulty > st.session_state.percentage_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to simpler patterns. Keep practicing!**")
            
            # Show explanation
            show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    correct_answer = st.session_state.correct_answer
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"""
        ### How to calculate the percentage:
        
        **Step 1:** Count the {data['color_name']} squares
        - Number of {data['color_name']} squares = **{data['colored_count']}**
        
        **Step 2:** Count the total squares
        - Grid size = 10 × 10 = **{data['total_squares']}** squares
        
        **Step 3:** Calculate the percentage
        - Percentage = (Colored squares ÷ Total squares) × 100
        - Percentage = ({data['colored_count']} ÷ {data['total_squares']}) × 100
        - Percentage = **{correct_answer}%**
        
        **Answer:** **{correct_answer}%** of the grid is {data['color_name']}
        
        💡 **Remember:** In a 10×10 grid, each square represents 1%, 
        so you can count the colored squares to get the percentage directly!
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer