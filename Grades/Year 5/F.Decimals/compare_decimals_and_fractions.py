import streamlit as st
import random
from fractions import Fraction
from decimal import Decimal

def run():
    """
    Main function to run the Compare Decimals and Fractions practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/compare_decimals_and_fractions.py
    """
    # Initialize session state for difficulty and game state
    if "compare_difficulty" not in st.session_state:
        st.session_state.compare_difficulty = 1  # Start with simple comparisons
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_answer = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("⚖️ Compare Decimals and Fractions")
    st.markdown("*Determine which is greater, less than, or equal*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.compare_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Basic", "Intermediate", "Advanced", "Expert"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level - 1]}")
        # Progress bar
        progress = (difficulty_level - 1) / 3
        st.progress(progress, text=f"Level {difficulty_level} of 4")
    
    with col2:
        if difficulty_level <= 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level <= 2:
            st.markdown("**🟡 Intermediate**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Advanced**")
        else:
            st.markdown("**🔴 Expert**")
    
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
        - **Look at the decimal and fraction**
        - **Choose the correct comparison sign**: >, <, or =
        - **Submit your answer** to check if you're correct
        
        ### Tips for Success:
        - **Convert to the same form:** 
          - Fraction → Decimal: Divide numerator by denominator
          - Decimal → Fraction: Use place values (0.5 = 5/10 = 1/2)
        - **Common equivalents to remember:**
          - 1/2 = 0.5
          - 1/4 = 0.25
          - 3/4 = 0.75
          - 1/5 = 0.2
          - 1/10 = 0.1
        
        ### Examples:
        - **0.5 = 1/2** (they are equal)
        - **0.3 < 1/2** (0.3 is less than 0.5)
        - **0.75 > 2/5** (0.75 is greater than 0.4)
        
        ### Difficulty Levels:
        - **🟢 Basic:** Simple fractions (halves, tenths, hundredths)
        - **🟡 Intermediate:** Mixed denominators (fifths, quarters)
        - **🟠 Advanced:** Complex fractions (thirds, sixths, eighths)
        - **🔴 Expert:** Challenging comparisons with mixed numbers
        """)

def generate_new_question():
    """Generate a new comparison question based on difficulty"""
    level = st.session_state.compare_difficulty
    
    if level == 1:  # Basic - simple fractions with denominators 10, 100
        questions = [
            {"decimal": 0.1, "fraction": (35, 100), "answer": ">"},
            {"decimal": 0.5, "fraction": (50, 100), "answer": "="},
            {"decimal": 0.25, "fraction": (1, 4), "answer": "="},
            {"decimal": 0.3, "fraction": (3, 10), "answer": "="},
            {"decimal": 0.7, "fraction": (65, 100), "answer": ">"},
            {"decimal": 0.4, "fraction": (45, 100), "answer": "<"},
            {"decimal": 0.2, "fraction": (2, 10), "answer": "="},
            {"decimal": 0.6, "fraction": (55, 100), "answer": ">"},
            {"decimal": 0.9, "fraction": (9, 10), "answer": "="},
            {"decimal": 0.15, "fraction": (2, 10), "answer": "<"},
        ]
    
    elif level == 2:  # Intermediate - add fifths and quarters
        questions = [
            {"decimal": 0.78, "fraction": (6, 10), "answer": ">"},
            {"decimal": 0.4, "fraction": (2, 5), "answer": "="},
            {"decimal": 0.25, "fraction": (1, 5), "answer": ">"},
            {"decimal": 0.8, "fraction": (4, 5), "answer": "="},
            {"decimal": 0.75, "fraction": (3, 4), "answer": "="},
            {"decimal": 0.6, "fraction": (3, 5), "answer": "="},
            {"decimal": 0.35, "fraction": (7, 20), "answer": "="},
            {"decimal": 0.45, "fraction": (2, 4), "answer": "<"},
            {"decimal": 0.85, "fraction": (17, 20), "answer": "="},
            {"decimal": 0.55, "fraction": (11, 20), "answer": "="},
        ]
    
    elif level == 3:  # Advanced - thirds, sixths, eighths
        questions = [
            {"decimal": 0.33, "fraction": (1, 3), "answer": "<"},
            {"decimal": 0.67, "fraction": (2, 3), "answer": ">"},
            {"decimal": 0.125, "fraction": (1, 8), "answer": "="},
            {"decimal": 0.375, "fraction": (3, 8), "answer": "="},
            {"decimal": 0.83, "fraction": (5, 6), "answer": "<"},
            {"decimal": 0.625, "fraction": (5, 8), "answer": "="},
            {"decimal": 0.16, "fraction": (1, 6), "answer": "<"},
            {"decimal": 0.88, "fraction": (7, 8), "answer": ">"},
            {"decimal": 0.42, "fraction": (5, 12), "answer": ">"},
            {"decimal": 0.72, "fraction": (18, 25), "answer": "="},
        ]
    
    else:  # Expert - complex comparisons
        questions = [
            {"decimal": 0.428, "fraction": (3, 7), "answer": "<"},
            {"decimal": 0.714, "fraction": (5, 7), "answer": "<"},
            {"decimal": 0.555, "fraction": (5, 9), "answer": "<"},
            {"decimal": 0.875, "fraction": (7, 8), "answer": "="},
            {"decimal": 0.416, "fraction": (5, 12), "answer": "<"},
            {"decimal": 0.636, "fraction": (7, 11), "answer": "<"},
            {"decimal": 0.385, "fraction": (5, 13), "answer": "<"},
            {"decimal": 0.923, "fraction": (12, 13), "answer": "<"},
            {"decimal": 0.454, "fraction": (5, 11), "answer": "<"},
            {"decimal": 0.286, "fraction": (2, 7), "answer": ">"},
        ]
    
    # Select a random question
    question = random.choice(questions)
    
    # Randomly decide which side to show first
    if random.choice([True, False]):
        # Show decimal first
        st.session_state.question_data = {
            "left_value": question["decimal"],
            "right_value": question["fraction"],
            "left_type": "decimal",
            "right_type": "fraction",
            "correct_answer": question["answer"]
        }
    else:
        # Show fraction first
        # Reverse the comparison operator
        reversed_answer = {"<": ">", ">": "<", "=": "="}[question["answer"]]
        st.session_state.question_data = {
            "left_value": question["fraction"],
            "right_value": question["decimal"],
            "left_type": "fraction",
            "right_type": "decimal",
            "correct_answer": reversed_answer
        }
    
    st.session_state.current_question = "Which sign makes the statement true?"
    st.session_state.selected_answer = None

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown("### 📊 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Format the values for display
    if data["left_type"] == "decimal":
        left_display = str(data["left_value"])
    else:
        left_display = f"{data['left_value'][0]}/{data['left_value'][1]}"
    
    if data["right_type"] == "decimal":
        right_display = str(data["right_value"])
    else:
        right_display = f"{data['right_value'][0]}/{data['right_value'][1]}"
    
    # Display the comparison in a nice format
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            {left_display}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background-color: #e0e0e0;
            padding: 20px;
            border-radius: 50%;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            height: 80px;
            width: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
        ">
            ?
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            {right_display}
        </div>
        """, unsafe_allow_html=True)
    
    # Answer selection buttons with better styling
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create a container for the buttons
    button_container = st.container()
    
    with button_container:
        # Use columns for button layout
        col1, col2, col3 = st.columns(3)
        
        # Define button style based on selection
        def get_button_style(symbol):
            if st.session_state.selected_answer == symbol:
                return "background-color: #1f77b4; color: white;"
            else:
                return "background-color: #f0f2f6; color: black;"
        
        with col1:
            st.markdown(f"""
            <style>
            .stButton > button {{
                width: 100%;
                height: 50px;
                font-size: 24px;
                font-weight: bold;
            }}
            </style>
            """, unsafe_allow_html=True)
            
            if st.button("&gt;", key="greater", use_container_width=True, 
                        help="Greater than"):
                st.session_state.selected_answer = ">"
                st.rerun()
        
        with col2:
            if st.button("&lt;", key="less", use_container_width=True,
                        help="Less than"):
                st.session_state.selected_answer = "<"
                st.rerun()
        
        with col3:
            if st.button("=", key="equal", use_container_width=True,
                        help="Equal to"):
                st.session_state.selected_answer = "="
                st.rerun()
    
    # Show selected answer feedback
    if st.session_state.selected_answer:
        st.info(f"Selected: **{st.session_state.selected_answer}**")
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True,
                    disabled=st.session_state.selected_answer is None or st.session_state.answer_submitted):
            if st.session_state.selected_answer:
                st.session_state.user_answer = st.session_state.selected_answer
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.question_data["correct_answer"]
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.compare_difficulty
        st.session_state.compare_difficulty = min(
            st.session_state.compare_difficulty + 1, 4
        )
        
        if st.session_state.compare_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Amazing! You've reached Expert level!**")
        elif old_difficulty < st.session_state.compare_difficulty:
            st.info(f"⬆️ **Level up! Now at {['Basic', 'Intermediate', 'Advanced', 'Expert'][st.session_state.compare_difficulty - 1]} level**")
    
    else:
        st.error(f"❌ **Not quite right.** The correct answer was **{correct_answer}**")
        
        # Decrease difficulty
        old_difficulty = st.session_state.compare_difficulty
        st.session_state.compare_difficulty = max(
            st.session_state.compare_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.compare_difficulty:
            st.warning(f"⬇️ **Level adjusted to {['Basic', 'Intermediate', 'Advanced', 'Expert'][st.session_state.compare_difficulty - 1]}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    
    # Calculate decimal values for both
    if data["left_type"] == "decimal":
        left_decimal = data["left_value"]
    else:
        left_decimal = data["left_value"][0] / data["left_value"][1]
    
    if data["right_type"] == "decimal":
        right_decimal = data["right_value"]
    else:
        right_decimal = data["right_value"][0] / data["right_value"][1]
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### Step-by-step conversion:")
        
        # Show left value conversion
        if data["left_type"] == "fraction":
            st.markdown(f"""
            **Left side:** {data["left_value"][0]}/{data["left_value"][1]}
            - Divide: {data["left_value"][0]} ÷ {data["left_value"][1]} = {left_decimal:.3f}
            """)
        else:
            st.markdown(f"""
            **Left side:** {data["left_value"]} (already in decimal form)
            """)
        
        # Show right value conversion
        if data["right_type"] == "fraction":
            st.markdown(f"""
            **Right side:** {data["right_value"][0]}/{data["right_value"][1]}
            - Divide: {data["right_value"][0]} ÷ {data["right_value"][1]} = {right_decimal:.3f}
            """)
        else:
            st.markdown(f"""
            **Right side:** {data["right_value"]} (already in decimal form)
            """)
        
        # Show comparison
        st.markdown(f"""
        ### Comparison:
        - {left_decimal:.3f} {data["correct_answer"]} {right_decimal:.3f}
        """)
        
        # Add visual representation if helpful
        if abs(left_decimal - right_decimal) < 0.01:
            st.info("💡 These values are equal (or very close)!")
        elif left_decimal > right_decimal:
            diff = left_decimal - right_decimal
            st.info(f"💡 The left value is larger by {diff:.3f}")
        else:
            diff = right_decimal - left_decimal
            st.info(f"💡 The right value is larger by {diff:.3f}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_answer = None
    if "user_answer" in st.session_state:
        del st.session_state.user_answer