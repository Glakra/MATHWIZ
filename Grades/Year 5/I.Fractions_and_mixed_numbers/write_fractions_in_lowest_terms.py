import streamlit as st
import random
import math

def run():
    """
    Main function to run the Write Fractions in Lowest Terms practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A.Place values and number sense/write_fractions_in_lowest_terms.py
    """
    # Initialize session state for difficulty and game state
    if "fractions_difficulty" not in st.session_state:
        st.session_state.fractions_difficulty = 1  # Start with simple fractions
    
    if "current_fraction" not in st.session_state:
        st.session_state.current_fraction = None
        st.session_state.correct_numerator = None
        st.session_state.correct_denominator = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.fraction_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Write Fractions in Lowest Terms")
    st.markdown("*Simplify fractions to their lowest form*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.fractions_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (2-20)",
            2: "Medium (10-50)",
            3: "Advanced (20-100)",
            4: "Expert (50-200)"
        }
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 4)
        progress = (difficulty_level - 1) / 3
        st.progress(progress, text=difficulty_names[difficulty_level])
    
    with col2:
        if difficulty_level <= 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level <= 2:
            st.markdown("**🟡 Medium**")
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
    if st.session_state.current_fraction is None:
        generate_new_fraction()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the fraction** shown
        - **Find the Greatest Common Factor (GCF)** of the numerator and denominator
        - **Divide both by the GCF** to get the lowest terms
        - **Enter your answer** in the boxes provided
        
        ### Tips for Success:
        - **Find the GCF:** List factors of both numbers and find the largest common one
        - **Divide both parts:** Whatever you divide the top by, divide the bottom by the same
        - **Check your work:** Can your answer be reduced further? If not, you're done!
        
        ### Examples:
        <table style="margin: 10px 0;">
        <tr>
            <td style="padding: 0 20px;">
                <div style="text-align: center;">
                    <strong>6</strong><br>
                    <hr style="margin: 2px 0; border-top: 2px solid black;">
                    <strong>8</strong>
                </div>
            </td>
            <td style="padding: 0 20px;">→</td>
            <td style="padding: 0 20px;">
                <div style="text-align: center;">
                    <strong>3</strong><br>
                    <hr style="margin: 2px 0; border-top: 2px solid black;">
                    <strong>4</strong>
                </div>
            </td>
            <td style="padding: 0 20px;">(GCF = 2)</td>
        </tr>
        <tr>
            <td style="padding: 0 20px;">
                <div style="text-align: center;">
                    <strong>12</strong><br>
                    <hr style="margin: 2px 0; border-top: 2px solid black;">
                    <strong>18</strong>
                </div>
            </td>
            <td style="padding: 0 20px;">→</td>
            <td style="padding: 0 20px;">
                <div style="text-align: center;">
                    <strong>2</strong><br>
                    <hr style="margin: 2px 0; border-top: 2px solid black;">
                    <strong>3</strong>
                </div>
            </td>
            <td style="padding: 0 20px;">(GCF = 6)</td>
        </tr>
        <tr>
            <td style="padding: 0 20px;">
                <div style="text-align: center;">
                    <strong>20</strong><br>
                    <hr style="margin: 2px 0; border-top: 2px solid black;">
                    <strong>25</strong>
                </div>
            </td>
            <td style="padding: 0 20px;">→</td>
            <td style="padding: 0 20px;">
                <div style="text-align: center;">
                    <strong>4</strong><br>
                    <hr style="margin: 2px 0; border-top: 2px solid black;">
                    <strong>5</strong>
                </div>
            </td>
            <td style="padding: 0 20px;">(GCF = 5)</td>
        </tr>
        </table>
        
        ### Finding GCF:
        1. **List all factors** of each number
        2. **Find common factors** that appear in both lists
        3. **Choose the largest** common factor
        
        ### Quick Checks:
        - If both numbers are **even**, divide by 2
        - If both end in **0 or 5**, divide by 5
        - If the sum of digits is divisible by **3**, both might be divisible by 3
        
        ### Difficulty Levels:
        - **🟢 Basic:** Small numbers (2-20)
        - **🟡 Medium:** Larger numbers (10-50)
        - **🟠 Advanced:** Big numbers (20-100)
        - **🔴 Expert:** Very large numbers (50-200)
        
        ### Scoring:
        - ✅ **Correct answer:** Move to harder fractions
        - ❌ **Wrong answer:** Practice with easier fractions
        - 🎯 **Goal:** Master simplifying any fraction!
        """)

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b"""
    while b:
        a, b = b, a % b
    return a

def generate_new_fraction():
    """Generate a new fraction that can be simplified"""
    difficulty = st.session_state.fractions_difficulty
    
    # Define ranges based on difficulty
    if difficulty == 1:  # Basic
        min_val, max_val = 2, 20
    elif difficulty == 2:  # Medium
        min_val, max_val = 10, 50
    elif difficulty == 3:  # Advanced
        min_val, max_val = 20, 100
    else:  # Expert
        min_val, max_val = 50, 200
    
    # Generate a fraction that's not already in lowest terms
    attempts = 0
    while attempts < 50:
        # First, generate the simplified fraction
        simplified_numerator = random.randint(1, max_val // 3)
        simplified_denominator = random.randint(simplified_numerator + 1, max_val // 2)
        
        # Make sure the simplified fraction is in lowest terms
        gcf = gcd(simplified_numerator, simplified_denominator)
        simplified_numerator //= gcf
        simplified_denominator //= gcf
        
        # Now multiply by a common factor to create the unsimplified fraction
        common_factors = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        if difficulty >= 3:
            common_factors.extend([11, 12, 13, 14, 15, 16, 18, 20])
        
        factor = random.choice(common_factors)
        
        # Create the unsimplified fraction
        unsimplified_numerator = simplified_numerator * factor
        unsimplified_denominator = simplified_denominator * factor
        
        # Make sure it's within our range
        if (min_val <= unsimplified_numerator <= max_val and 
            min_val <= unsimplified_denominator <= max_val and
            unsimplified_numerator < unsimplified_denominator):
            break
        
        attempts += 1
    
    # Store the question data
    st.session_state.fraction_data = {
        "numerator": unsimplified_numerator,
        "denominator": unsimplified_denominator,
        "gcf": gcd(unsimplified_numerator, unsimplified_denominator)
    }
    
    st.session_state.correct_numerator = simplified_numerator
    st.session_state.correct_denominator = simplified_denominator
    st.session_state.current_fraction = f"{unsimplified_numerator}/{unsimplified_denominator}"

def display_question():
    """Display the current question interface"""
    data = st.session_state.fraction_data
    
    # Display question with nice formatting
    st.markdown("### 📝 Question:")
    st.markdown("**Write this fraction in lowest terms:**")
    
    # Display the fraction in a highlighted box
    st.markdown(f"""
    <div style="
        background-color: #f0f2f6; 
        padding: 40px; 
        border-radius: 15px; 
        border-left: 5px solid #4CAF50;
        text-align: center;
        margin: 30px auto;
        width: 200px;
    ">
        <div style="
            font-size: 48px;
            font-weight: bold;
            color: #333;
            font-family: 'Courier New', monospace;
            line-height: 1;
        ">
            {data['numerator']}
        </div>
        <hr style="
            border: none;
            border-top: 4px solid #333;
            margin: 10px 0;
            width: 100%;
        ">
        <div style="
            font-size: 48px;
            font-weight: bold;
            color: #333;
            font-family: 'Courier New', monospace;
            line-height: 1;
        ">
            {data['denominator']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer input form
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Enter your answer in lowest terms:**")
        
        # Create a centered container for the fraction input
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Add custom CSS for centered number inputs
            st.markdown("""
            <style>
            div[data-testid="column"] input[type="number"] {
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Numerator input
            user_numerator = st.number_input(
                "Numerator",
                min_value=1,
                max_value=999,
                value=1,
                step=1,
                key="user_num",
                label_visibility="collapsed",
                placeholder="Numerator"
            )
            
            # Fraction bar
            st.markdown("""
            <div style="
                text-align: center; 
                margin: -20px 0 -20px 0;
                padding: 0;
            ">
                <hr style="
                    border: none;
                    border-top: 3px solid #333;
                    margin: 0;
                    width: 100%;
                ">
            </div>
            """, unsafe_allow_html=True)
            
            # Denominator input
            user_denominator = st.number_input(
                "Denominator",
                min_value=1,
                max_value=999,
                value=1,
                step=1,
                key="user_den",
                label_visibility="collapsed",
                placeholder="Denominator"
            )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_numerator = user_numerator
            st.session_state.user_denominator = user_denominator
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_num = st.session_state.user_numerator
    user_den = st.session_state.user_denominator
    correct_num = st.session_state.correct_numerator
    correct_den = st.session_state.correct_denominator
    
    # Check if the answer is correct
    user_correct = (user_num == correct_num and user_den == correct_den)
    
    # Also check if it's an equivalent fraction (same ratio)
    equivalent = False
    if user_den != 0 and correct_den != 0:
        equivalent = (user_num * correct_den == user_den * correct_num)
    
    if user_correct:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.fractions_difficulty
        st.session_state.fractions_difficulty = min(
            st.session_state.fractions_difficulty + 1, 4
        )
        
        # Show encouragement based on difficulty
        if st.session_state.fractions_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Amazing! You've reached Expert level!**")
        elif old_difficulty < st.session_state.fractions_difficulty:
            difficulty_names = {2: "Medium", 3: "Advanced", 4: "Expert"}
            st.info(f"⬆️ **Level up! Now at {difficulty_names[st.session_state.fractions_difficulty]} level**")
    
    elif equivalent and gcd(user_num, user_den) > 1:
        st.warning(f"🤔 **Almost there!** Your fraction is equivalent, but not in lowest terms.")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center;">
                <span style="font-size: 20px; font-weight: bold;">
                    {user_num}<br>
                    <hr style="margin: 2px 0; border-top: 2px solid black; width: 50px; display: inline-block;">
                    <br>{user_den}
                </span>
                <span style="margin: 0 20px;">→</span>
                <span style="font-size: 20px; font-weight: bold; color: green;">
                    {correct_num}<br>
                    <hr style="margin: 2px 0; border-top: 2px solid green; width: 50px; display: inline-block;">
                    <br>{correct_den}
                </span>
            </div>
            """, unsafe_allow_html=True)
        show_explanation()
        
        # Stay at same difficulty
        st.info("💪 **Keep practicing! You're getting close.**")
    
    else:
        st.error(f"❌ **Not quite right.**")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center;">
                <strong>The correct answer is:</strong><br>
                <span style="font-size: 24px; font-weight: bold; color: green;">
                    {correct_num}<br>
                    <hr style="margin: 2px 0; border-top: 3px solid green; width: 60px; display: inline-block;">
                    <br>{correct_den}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        # Decrease difficulty
        old_difficulty = st.session_state.fractions_difficulty
        st.session_state.fractions_difficulty = max(
            st.session_state.fractions_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.fractions_difficulty:
            difficulty_names = {1: "Basic", 2: "Medium", 3: "Advanced"}
            st.warning(f"⬇️ **Difficulty decreased to {difficulty_names[st.session_state.fractions_difficulty]} level. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show detailed explanation for the correct answer"""
    data = st.session_state.fraction_data
    numerator = data["numerator"]
    denominator = data["denominator"]
    gcf = data["gcf"]
    
    with st.expander("📖 **Click here for step-by-step explanation**", expanded=True):
        st.markdown(f"""
        ### How to simplify:
        """)
        
        # Show the fraction in vertical format
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center; font-size: 24px; font-weight: bold;">
                {numerator}<br>
                <hr style="margin: 2px 0; border-top: 3px solid black; width: 80px; display: inline-block;">
                <br>{denominator}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
        **Step 1: Find the GCF (Greatest Common Factor)**
        """)
        
        # Show factors
        num_factors = [i for i in range(1, numerator + 1) if numerator % i == 0]
        den_factors = [i for i in range(1, denominator + 1) if denominator % i == 0]
        common_factors = [i for i in num_factors if i in den_factors]
        
        st.markdown(f"""
        - Factors of {numerator}: {', '.join(map(str, num_factors))}
        - Factors of {denominator}: {', '.join(map(str, den_factors))}
        - **Common factors:** {', '.join(map(str, common_factors))}
        - **Greatest Common Factor (GCF):** {gcf}
        """)
        
        st.markdown(f"""
        **Step 2: Divide both numerator and denominator by the GCF**
        
        - Numerator: {numerator} ÷ {gcf} = **{numerator // gcf}**
        - Denominator: {denominator} ÷ {gcf} = **{denominator // gcf}**
        """)
        
        # Show the answer in vertical format
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center;">
                <strong>Answer:</strong><br>
                <span style="font-size: 24px; font-weight: bold; color: green;">
                    {numerator // gcf}<br>
                    <hr style="margin: 2px 0; border-top: 3px solid green; width: 60px; display: inline-block;">
                    <br>{denominator // gcf}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        # Show visual representation if numbers are small enough
        if numerator <= 24 and denominator <= 24 and gcf > 1:
            st.markdown("**Visual representation:**")
            
            # Create a simple visual grid
            cols = st.columns(2)
            with cols[0]:
                st.markdown(f"**Original:**")
                # Show blocks representing the fraction
                blocks = "🟦" * numerator + "⬜" * (denominator - numerator)
                st.markdown(f"<div style='font-size: 20px; line-height: 1.2; text-align: center;'>{blocks}</div>", unsafe_allow_html=True)
            
            with cols[1]:
                st.markdown(f"**Simplified:**")
                # Show grouped blocks
                simplified_blocks = "🟦" * (numerator // gcf) + "⬜" * (denominator // gcf - numerator // gcf)
                st.markdown(f"<div style='font-size: 20px; line-height: 1.2; text-align: center;'>{simplified_blocks}</div>", unsafe_allow_html=True)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_fraction = None
    st.session_state.correct_numerator = None
    st.session_state.correct_denominator = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.fraction_data = {}
    if "user_numerator" in st.session_state:
        del st.session_state.user_numerator
    if "user_denominator" in st.session_state:
        del st.session_state.user_denominator