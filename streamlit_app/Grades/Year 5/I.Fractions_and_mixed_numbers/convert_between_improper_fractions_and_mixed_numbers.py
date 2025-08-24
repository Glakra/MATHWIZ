import streamlit as st
import random
import math

def run():
    """
    Main function to run the Convert Between Improper Fractions and Mixed Numbers practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A.Place values and number sense/convert_between_improper_fractions_and_mixed_numbers.py
    """
    # Initialize session state for difficulty and game state
    if "convert_fractions_difficulty" not in st.session_state:
        st.session_state.convert_fractions_difficulty = 1  # Start with simple conversions
    
    if "conversion_type" not in st.session_state:
        st.session_state.conversion_type = None  # "improper_to_mixed" or "mixed_to_improper"
        
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.correct_answer = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔄 Convert Between Improper Fractions and Mixed Numbers")
    st.markdown("*Convert improper fractions to mixed numbers and vice versa*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.convert_fractions_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic (denominators 2-6)",
            2: "Medium (denominators 2-10)",
            3: "Advanced (denominators 2-15)",
            4: "Expert (denominators 2-20)"
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
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### Two Types of Problems:
        
        **1. Improper Fraction → Mixed Number**
        - Example: 7/3 = 2 1/3
        - Divide numerator by denominator
        - Quotient = whole number
        - Remainder = new numerator
        - Keep same denominator
        
        **2. Mixed Number → Improper Fraction**
        - Example: 2 1/3 = 7/3
        - Multiply whole × denominator
        - Add the numerator
        - Keep same denominator
        
        ### Method 1: Improper to Mixed
        **Example: Convert 17/5**
        1. Divide: 17 ÷ 5 = 3 remainder 2
        2. Whole number = 3
        3. Fraction = 2/5
        4. Answer: 3 2/5
        
        ### Method 2: Mixed to Improper
        **Example: Convert 3 2/5**
        1. Multiply: 3 × 5 = 15
        2. Add: 15 + 2 = 17
        3. Answer: 17/5
        
        ### Quick Check:
        - **Improper fraction:** numerator ≥ denominator
        - **Mixed number:** whole number + proper fraction
        - **Proper fraction:** numerator < denominator
        
        ### Visual Method:
        - Draw circles/shapes divided into parts
        - Count complete shapes (whole number)
        - Count remaining parts (fraction)
        
        ### Common Mistakes to Avoid:
        - ❌ Forgetting to simplify the final fraction
        - ❌ Wrong order in multiplication for mixed→improper
        - ❌ Using wrong denominator
        
        ### Difficulty Levels:
        - **🟢 Basic:** Small denominators (2-6)
        - **🟡 Medium:** Medium denominators (2-10)
        - **🟠 Advanced:** Larger denominators (2-15)
        - **🔴 Expert:** All denominators (2-20)
        
        ### Goal:
        - Master both directions of conversion
        - Work quickly and accurately
        - Understand the relationship between forms
        """)

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b"""
    while b:
        a, b = b, a % b
    return a

def generate_new_problem():
    """Generate a new conversion problem"""
    difficulty = st.session_state.convert_fractions_difficulty
    
    # Define denominator ranges based on difficulty
    if difficulty == 1:  # Basic
        max_denominator = 6
    elif difficulty == 2:  # Medium
        max_denominator = 10
    elif difficulty == 3:  # Advanced
        max_denominator = 15
    else:  # Expert
        max_denominator = 20
    
    # Randomly choose conversion type
    conversion_type = random.choice(["improper_to_mixed", "mixed_to_improper"])
    st.session_state.conversion_type = conversion_type
    
    if conversion_type == "improper_to_mixed":
        # Generate an improper fraction
        denominator = random.randint(2, max_denominator)
        
        # Generate whole part (1-5 based on difficulty)
        whole_part = random.randint(1, min(5, difficulty + 1))
        
        # Generate fractional part (must be less than denominator)
        fraction_part = random.randint(1, denominator - 1)
        
        # Create improper fraction
        numerator = whole_part * denominator + fraction_part
        
        # Simplify the resulting mixed number fraction part
        gcf = gcd(fraction_part, denominator)
        simplified_num = fraction_part // gcf
        simplified_den = denominator // gcf
        
        # Store problem data
        st.session_state.problem_data = {
            "improper_numerator": numerator,
            "improper_denominator": denominator,
            "display_fraction": f"{numerator}/{denominator}"
        }
        
        st.session_state.correct_answer = {
            "whole": whole_part,
            "numerator": simplified_num,
            "denominator": simplified_den
        }
        
        st.session_state.current_problem = f"Write {numerator}/{denominator} as a mixed number:"
        
    else:  # mixed_to_improper
        # Generate a mixed number
        denominator = random.randint(2, max_denominator)
        whole = random.randint(1, min(5, difficulty + 1))
        numerator = random.randint(1, denominator - 1)
        
        # Simplify the fraction part first
        gcf = gcd(numerator, denominator)
        simplified_num = numerator // gcf
        simplified_den = denominator // gcf
        
        # Calculate the improper fraction
        improper_num = whole * simplified_den + simplified_num
        
        # Store problem data
        st.session_state.problem_data = {
            "mixed_whole": whole,
            "mixed_numerator": simplified_num,
            "mixed_denominator": simplified_den,
            "display_mixed": f"{whole} {simplified_num}/{simplified_den}"
        }
        
        st.session_state.correct_answer = {
            "numerator": improper_num,
            "denominator": simplified_den
        }
        
        st.session_state.current_problem = f"Write {whole} {simplified_num}/{simplified_den} as an improper fraction:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.problem_data
    conversion_type = st.session_state.conversion_type
    
    # Display question with nice formatting
    st.markdown("### 📝 Question:")
    
    if conversion_type == "improper_to_mixed":
        # Display improper fraction to convert
        st.markdown(f"""
        <div style="
            background-color: #e8f4fd;
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid #1f77b4;
            margin: 20px 0;
        ">
            <div style="font-size: 20px; margin-bottom: 15px;">
                <strong>Write <span style="font-size: 32px; color: #1f77b4;">
                    <sup>{data['improper_numerator']}</sup>⁄<sub>{data['improper_denominator']}</sub>
                </span> as a mixed number:</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer input form for mixed number
        with st.form("answer_form", clear_on_submit=False):
            col1, col2, col3, col4 = st.columns([1, 0.5, 1.5, 1])
            
            with col1:
                user_whole = st.number_input(
                    "Whole",
                    min_value=0,
                    max_value=20,
                    value=0,
                    step=1,
                    key="whole_input",
                    label_visibility="collapsed"
                )
            
            with col2:
                st.markdown("""
                <div style="text-align: center; margin-top: 5px; font-size: 20px;">
                    
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Fraction inputs
                user_numerator = st.number_input(
                    "Numerator",
                    min_value=0,
                    max_value=50,
                    value=0,
                    step=1,
                    key="num_input",
                    label_visibility="collapsed"
                )
                
                st.markdown("""
                <div style="margin: -15px 0;">
                    <hr style="border: none; border-top: 2px solid #333;">
                </div>
                """, unsafe_allow_html=True)
                
                user_denominator = st.number_input(
                    "Denominator",
                    min_value=1,
                    max_value=50,
                    value=1,
                    step=1,
                    key="den_input",
                    label_visibility="collapsed"
                )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
            
            if submit_button:
                st.session_state.submitted_answer = {
                    "whole": user_whole,
                    "numerator": user_numerator,
                    "denominator": user_denominator
                }
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
    
    else:  # mixed_to_improper
        # Display mixed number to convert
        st.markdown(f"""
        <div style="
            background-color: #f0e8ff;
            padding: 20px;
            border-radius: 15px;
            border-left: 5px solid #8b5cf6;
            margin: 20px 0;
        ">
            <div style="font-size: 20px; margin-bottom: 15px;">
                <strong>Write <span style="font-size: 32px; color: #8b5cf6;">
                    {data['mixed_whole']} <sup>{data['mixed_numerator']}</sup>⁄<sub>{data['mixed_denominator']}</sub>
                </span> as an improper fraction:</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer input form for improper fraction
        with st.form("answer_form", clear_on_submit=False):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                # Fraction inputs
                user_numerator = st.number_input(
                    "Numerator",
                    min_value=1,
                    max_value=200,
                    value=1,
                    step=1,
                    key="num_input_improper",
                    label_visibility="collapsed"
                )
                
                st.markdown("""
                <div style="margin: -15px 0;">
                    <hr style="border: none; border-top: 3px solid #333;">
                </div>
                """, unsafe_allow_html=True)
                
                user_denominator = st.number_input(
                    "Denominator",
                    min_value=1,
                    max_value=50,
                    value=1,
                    step=1,
                    key="den_input_improper",
                    label_visibility="collapsed"
                )
            
            # Submit button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
            
            if submit_button:
                st.session_state.submitted_answer = {
                    "numerator": user_numerator,
                    "denominator": user_denominator
                }
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
    submitted = st.session_state.submitted_answer
    correct = st.session_state.correct_answer
    conversion_type = st.session_state.conversion_type
    
    if conversion_type == "improper_to_mixed":
        # Check mixed number answer
        user_correct = (submitted["whole"] == correct["whole"] and
                       submitted["numerator"] == correct["numerator"] and
                       submitted["denominator"] == correct["denominator"])
        
        # Check if fraction is equivalent but not simplified
        fraction_equivalent = False
        if submitted["denominator"] != 0 and correct["denominator"] != 0:
            fraction_equivalent = (submitted["numerator"] * correct["denominator"] == 
                                 submitted["denominator"] * correct["numerator"])
        
        if user_correct:
            st.success("🎉 **Excellent! That's correct!**")
            increase_difficulty()
            
        elif submitted["whole"] == correct["whole"] and fraction_equivalent and submitted["numerator"] != correct["numerator"]:
            st.warning("🤔 **Almost there!** The fraction part should be in lowest terms.")
            st.info(f"The correct answer is **{correct['whole']} {correct['numerator']}/{correct['denominator']}**")
            show_explanation()
            
        else:
            st.error(f"❌ **Not quite right.**")
            st.info(f"The correct answer is **{correct['whole']} {correct['numerator']}/{correct['denominator']}**")
            decrease_difficulty()
            show_explanation()
    
    else:  # mixed_to_improper
        # Check improper fraction answer
        user_correct = (submitted["numerator"] == correct["numerator"] and
                       submitted["denominator"] == correct["denominator"])
        
        # Check if fraction is equivalent
        equivalent = False
        if submitted["denominator"] != 0 and correct["denominator"] != 0:
            equivalent = (submitted["numerator"] * correct["denominator"] == 
                         submitted["denominator"] * correct["numerator"])
        
        if user_correct:
            st.success("🎉 **Excellent! That's correct!**")
            increase_difficulty()
            
        elif equivalent:
            st.warning("🤔 **Almost there!** Your fraction is equivalent but not in the expected form.")
            st.info(f"The correct answer is **{correct['numerator']}/{correct['denominator']}**")
            show_explanation()
            
        else:
            st.error(f"❌ **Not quite right.**")
            st.info(f"The correct answer is **{correct['numerator']}/{correct['denominator']}**")
            decrease_difficulty()
            show_explanation()

def increase_difficulty():
    """Increase difficulty level"""
    old_difficulty = st.session_state.convert_fractions_difficulty
    st.session_state.convert_fractions_difficulty = min(
        st.session_state.convert_fractions_difficulty + 1, 4
    )
    
    if st.session_state.convert_fractions_difficulty == 4 and old_difficulty < 4:
        st.balloons()
        st.info("🏆 **Amazing! You've reached Expert level!**")
    elif old_difficulty < st.session_state.convert_fractions_difficulty:
        difficulty_names = {2: "Medium", 3: "Advanced", 4: "Expert"}
        st.info(f"⬆️ **Level up! Now at {difficulty_names[st.session_state.convert_fractions_difficulty]} level**")

def decrease_difficulty():
    """Decrease difficulty level"""
    old_difficulty = st.session_state.convert_fractions_difficulty
    st.session_state.convert_fractions_difficulty = max(
        st.session_state.convert_fractions_difficulty - 1, 1
    )
    
    if old_difficulty > st.session_state.convert_fractions_difficulty:
        difficulty_names = {1: "Basic", 2: "Medium", 3: "Advanced"}
        st.warning(f"⬇️ **Difficulty decreased to {difficulty_names[st.session_state.convert_fractions_difficulty]} level. Keep practicing!**")

def show_explanation():
    """Show detailed explanation for the correct answer"""
    data = st.session_state.problem_data
    conversion_type = st.session_state.conversion_type
    
    with st.expander("📖 **Click here for step-by-step explanation**", expanded=True):
        if conversion_type == "improper_to_mixed":
            numerator = data["improper_numerator"]
            denominator = data["improper_denominator"]
            
            st.markdown(f"""
            ### Converting {numerator}/{denominator} to a mixed number:
            
            **Step 1: Divide the numerator by the denominator**
            - {numerator} ÷ {denominator} = {numerator // denominator} remainder {numerator % denominator}
            
            **Step 2: Write the mixed number**
            - Whole number part = **{numerator // denominator}**
            - Fractional part = **{numerator % denominator}/{denominator}**
            """)
            
            # Check if fraction needs simplification
            remainder = numerator % denominator
            if remainder > 0:
                gcf = gcd(remainder, denominator)
                if gcf > 1:
                    st.markdown(f"""
            **Step 3: Simplify the fraction**
            - {remainder}/{denominator} = {remainder // gcf}/{denominator // gcf}
            
            **Final answer: {numerator // denominator} {remainder // gcf}/{denominator // gcf}**
            """)
                else:
                    st.markdown(f"""
            **Final answer: {numerator // denominator} {remainder}/{denominator}**
            """)
            
            # Visual representation
            st.markdown("**Visual representation:**")
            total_parts = numerator
            parts_per_whole = denominator
            wholes = numerator // denominator
            remaining = numerator % denominator
            
            visual = ""
            # Show whole shapes
            for i in range(wholes):
                visual += "[" + "█" * parts_per_whole + "] "
            # Show partial shape
            if remaining > 0:
                visual += "[" + "█" * remaining + "░" * (parts_per_whole - remaining) + "]"
            
            st.markdown(f"```\n{visual}\n```")
            st.markdown(f"= {wholes} whole{'s' if wholes > 1 else ''} and {remaining} out of {denominator} parts")
            
        else:  # mixed_to_improper
            whole = data["mixed_whole"]
            numerator = data["mixed_numerator"]
            denominator = data["mixed_denominator"]
            
            st.markdown(f"""
            ### Converting {whole} {numerator}/{denominator} to an improper fraction:
            
            **Step 1: Multiply whole number by denominator**
            - {whole} × {denominator} = {whole * denominator}
            
            **Step 2: Add the numerator**
            - {whole * denominator} + {numerator} = {whole * denominator + numerator}
            
            **Step 3: Keep the same denominator**
            - Improper fraction = **{whole * denominator + numerator}/{denominator}**
            
            **Verification:**
            - {whole * denominator + numerator} ÷ {denominator} = {whole} remainder {numerator} ✓
            """)
            
            # Visual representation
            st.markdown("**Visual representation:**")
            visual = ""
            # Show whole shapes
            for i in range(whole):
                visual += "[" + "█" * denominator + "] "
            # Show fractional part
            visual += "[" + "█" * numerator + "░" * (denominator - numerator) + "]"
            
            st.markdown(f"```\n{visual}\n```")
            st.markdown(f"Total parts = ({whole} × {denominator}) + {numerator} = {whole * denominator + numerator}")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_problem = None
    st.session_state.correct_answer = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    st.session_state.conversion_type = None
    if "submitted_answer" in st.session_state:
        del st.session_state.submitted_answer