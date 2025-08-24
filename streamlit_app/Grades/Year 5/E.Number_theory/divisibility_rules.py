import streamlit as st
import random

def run():
    """
    Main function to run the Divisibility Rules activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Number theory/divisibility_rules.py
    """
    # Initialize session state
    if "div_rules_difficulty" not in st.session_state:
        st.session_state.div_rules_difficulty = 1
    
    if "current_div_problem" not in st.session_state:
        st.session_state.current_div_problem = None
        st.session_state.div_answer = None
        st.session_state.div_feedback = False
        st.session_state.div_submitted = False
        st.session_state.div_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Number theory**")
    st.title("🧮 Divisibility Rules")
    st.markdown("*Determine if numbers are divisible without doing division*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.div_rules_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Level:** {difficulty_level}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_div_problem is None:
        generate_div_problem()
    
    # Display current question
    display_div_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Divisibility Rules Reference**", expanded=False):
        st.markdown("""
        ### Quick Divisibility Rules:
        
        #### **Divisibility by 2:**
        - Number ends in **0, 2, 4, 6, or 8**
        - Example: 1,234 ✅ (ends in 4)
        
        #### **Divisibility by 3:**
        - **Sum of digits** is divisible by 3
        - Example: 123 → 1+2+3 = 6 → 6÷3 = 2 ✅
        
        #### **Divisibility by 4:**
        - **Last two digits** are divisible by 4
        - Example: 1,236 → 36÷4 = 9 ✅
        
        #### **Divisibility by 5:**
        - Number ends in **0 or 5**
        - Example: 1,235 ✅ (ends in 5)
        
        #### **Divisibility by 6:**
        - Divisible by **both 2 AND 3**
        - Example: 126 → even ✅ AND 1+2+6=9, 9÷3=3 ✅
        
        #### **Divisibility by 8:**
        - **Last three digits** are divisible by 8
        - Example: 1,248 → 248÷8 = 31 ✅
        
        #### **Divisibility by 9:**
        - **Sum of digits** is divisible by 9
        - Example: 1,539 → 1+5+3+9 = 18 → 18÷9 = 2 ✅
        
        #### **Divisibility by 10:**
        - Number ends in **0**
        - Example: 1,230 ✅ (ends in 0)
        
        #### **Divisibility by 11:**
        - **Alternating sum** of digits is divisible by 11
        - Example: 1,331 → 1-3+3-1 = 0 → 0÷11 = 0 ✅
        
        #### **Divisibility by 12:**
        - Divisible by **both 3 AND 4**
        - Example: 144 → 1+4+4=9 (÷3) ✅ AND 44÷4=11 ✅
        
        ### Strategy Tips:
        - **Start with easy rules** (2, 5, 10) first
        - **Check digit sums** for 3 and 9
        - **Look at last few digits** for 4 and 8
        - **Combine rules** for 6 and 12
        
        ### Common Mistakes:
        - ❌ Forgetting to add ALL digits for sum rules
        - ❌ Checking wrong number of digits at the end
        - ❌ Missing that 6 and 12 need BOTH conditions
        """)

def generate_div_problem():
    """Generate a divisibility rules problem based on difficulty level"""
    difficulty = st.session_state.div_rules_difficulty
    
    # Define problems by difficulty level
    if difficulty == 1:
        # Level 1: Simple rules (2, 5, 10)
        problems = [
            # Divisibility by 2
            {"number": 1234, "divisor": 2, "correct": True, "rule": "ends in even digit"},
            {"number": 5673, "divisor": 2, "correct": False, "rule": "ends in odd digit"},
            {"number": 8746, "divisor": 2, "correct": True, "rule": "ends in even digit"},
            {"number": 9357, "divisor": 2, "correct": False, "rule": "ends in odd digit"},
            
            # Divisibility by 5
            {"number": 1235, "divisor": 5, "correct": True, "rule": "ends in 5"},
            {"number": 6840, "divisor": 5, "correct": True, "rule": "ends in 0"},
            {"number": 4572, "divisor": 5, "correct": False, "rule": "ends in 2"},
            {"number": 9863, "divisor": 5, "correct": False, "rule": "ends in 3"},
            
            # Divisibility by 10
            {"number": 4560, "divisor": 10, "correct": True, "rule": "ends in 0"},
            {"number": 7280, "divisor": 10, "correct": True, "rule": "ends in 0"},
            {"number": 3425, "divisor": 10, "correct": False, "rule": "ends in 5"},
            {"number": 6714, "divisor": 10, "correct": False, "rule": "ends in 4"},
        ]
    
    elif difficulty == 2:
        # Level 2: Medium rules (3, 4, 9)
        problems = [
            # Divisibility by 3
            {"number": 123, "divisor": 3, "correct": True, "rule": "sum of digits: 1+2+3=6, 6÷3=2"},
            {"number": 4578, "divisor": 3, "correct": True, "rule": "sum of digits: 4+5+7+8=24, 24÷3=8"},
            {"number": 1357, "divisor": 3, "correct": False, "rule": "sum of digits: 1+3+5+7=16, 16÷3=5⅓"},
            {"number": 2468, "divisor": 3, "correct": False, "rule": "sum of digits: 2+4+6+8=20, 20÷3=6⅔"},
            
            # Divisibility by 4
            {"number": 1236, "divisor": 4, "correct": True, "rule": "last two digits: 36÷4=9"},
            {"number": 5628, "divisor": 4, "correct": True, "rule": "last two digits: 28÷4=7"},
            {"number": 4573, "divisor": 4, "correct": False, "rule": "last two digits: 73÷4=18¼"},
            {"number": 6947, "divisor": 4, "correct": False, "rule": "last two digits: 47÷4=11¾"},
            
            # Divisibility by 9
            {"number": 1539, "divisor": 9, "correct": True, "rule": "sum of digits: 1+5+3+9=18, 18÷9=2"},
            {"number": 4698, "divisor": 9, "correct": True, "rule": "sum of digits: 4+6+9+8=27, 27÷9=3"},
            {"number": 2468, "divisor": 9, "correct": False, "rule": "sum of digits: 2+4+6+8=20, 20÷9=2⅔"},
            {"number": 5731, "divisor": 9, "correct": False, "rule": "sum of digits: 5+7+3+1=16, 16÷9=1⅞"},
        ]
    
    elif difficulty == 3:
        # Level 3: Complex rules (6, 8)
        problems = [
            # Divisibility by 6 (must be divisible by both 2 and 3)
            {"number": 126, "divisor": 6, "correct": True, "rule": "even AND sum 1+2+6=9 (÷3)"},
            {"number": 4578, "divisor": 6, "correct": True, "rule": "even AND sum 4+5+7+8=24 (÷3)"},
            {"number": 135, "divisor": 6, "correct": False, "rule": "odd (not divisible by 2)"},
            {"number": 158, "divisor": 6, "correct": False, "rule": "even but sum 1+5+8=14 (not ÷3)"},
            
            # Divisibility by 8
            {"number": 1248, "divisor": 8, "correct": True, "rule": "last three digits: 248÷8=31"},
            {"number": 5632, "divisor": 8, "correct": True, "rule": "last three digits: 632÷8=79"},
            {"number": 4573, "divisor": 8, "correct": False, "rule": "last three digits: 573÷8=71⅝"},
            {"number": 6947, "divisor": 8, "correct": False, "rule": "last three digits: 947÷8=118⅜"},
        ]
    
    elif difficulty == 4:
        # Level 4: Advanced rules (11, 12)
        problems = [
            # Divisibility by 11
            {"number": 1331, "divisor": 11, "correct": True, "rule": "alternating sum: 1-3+3-1=0, 0÷11=0"},
            {"number": 2552, "divisor": 11, "correct": True, "rule": "alternating sum: 2-5+5-2=0, 0÷11=0"},
            {"number": 1234, "divisor": 11, "correct": False, "rule": "alternating sum: 1-2+3-4=-2, not divisible by 11"},
            {"number": 5678, "divisor": 11, "correct": False, "rule": "alternating sum: 5-6+7-8=-2, not divisible by 11"},
            
            # Divisibility by 12 (must be divisible by both 3 and 4)
            {"number": 144, "divisor": 12, "correct": True, "rule": "sum 1+4+4=9 (÷3) AND 44÷4=11"},
            {"number": 2436, "divisor": 12, "correct": True, "rule": "sum 2+4+3+6=15 (÷3) AND 36÷4=9"},
            {"number": 158, "divisor": 12, "correct": False, "rule": "sum 1+5+8=14 (not ÷3)"},
            {"number": 246, "divisor": 12, "correct": False, "rule": "sum 2+4+6=12 (÷3) but 46÷4=11.5"},
        ]
    
    else:  # difficulty == 5
        # Level 5: Mixed challenging problems
        problems = [
            {"number": 69645, "divisor": 5, "correct": True, "rule": "ends in 5"},
            {"number": 87432, "divisor": 8, "correct": True, "rule": "last three digits: 432÷8=54"},
            {"number": 123456, "divisor": 6, "correct": True, "rule": "even AND sum 1+2+3+4+5+6=21 (÷3)"},
            {"number": 98765, "divisor": 9, "correct": False, "rule": "sum 9+8+7+6+5=35, 35÷9=3⅞"},
            {"number": 54321, "divisor": 11, "correct": False, "rule": "alternating sum: 5-4+3-2+1=3, not divisible by 11"},
            {"number": 147258, "divisor": 12, "correct": False, "rule": "even, sum=27 (÷3) but 58÷4=14.5"},
        ]
    
    # Select a random problem
    problem = random.choice(problems)
    
    st.session_state.div_data = problem
    st.session_state.div_answer = "yes" if problem["correct"] else "no"
    st.session_state.current_div_problem = f"Is {problem['number']:,} divisible by {problem['divisor']}?"

def display_div_problem():
    """Display the current divisibility problem with yes/no clickable tiles"""
    data = st.session_state.div_data
    number = data["number"]
    divisor = data["divisor"]
    
    # Initialize selected option in session state if not exists
    if "div_selected_option" not in st.session_state:
        st.session_state.div_selected_option = None
    
    # Display the question with large, clear formatting
    st.markdown("### 🎯 Question:")
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 5px solid #4CAF50;
        font-size: 24px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #2c3e50;
    ">
        Is {number:,} divisible by {divisor}?
    </div>
    """, unsafe_allow_html=True)
    
    # Create yes/no clickable tiles
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        pass  # Empty column for spacing
    
    with col2:
        # Create a sub-grid for yes/no options
        yes_col, no_col = st.columns(2, gap="medium")
        
        with yes_col:
            # Determine if "yes" is selected
            is_yes_selected = st.session_state.div_selected_option == "yes"
            button_type = "primary" if is_yes_selected else "secondary"
            button_text = "✅ yes" if is_yes_selected else "yes"
            
            if st.button(
                button_text,
                key="yes_tile",
                use_container_width=True,
                type=button_type,
                help="Click to select: yes"
            ):
                st.session_state.div_selected_option = "yes"
                st.rerun()
        
        with no_col:
            # Determine if "no" is selected
            is_no_selected = st.session_state.div_selected_option == "no"
            button_type = "primary" if is_no_selected else "secondary"
            button_text = "✅ no" if is_no_selected else "no"
            
            if st.button(
                button_text,
                key="no_tile",
                use_container_width=True,
                type=button_type,
                help="Click to select: no"
            ):
                st.session_state.div_selected_option = "no"
                st.rerun()
    
    with col3:
        pass  # Empty column for spacing
    
    # Show current selection status
    st.markdown("")
    if st.session_state.div_selected_option:
        st.success(f"**Selected:** {st.session_state.div_selected_option}")
    else:
        st.info("👆 **Click 'yes' or 'no' to select your answer**")
    
    # Submit section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.button(
            "✅ Submit", 
            type="primary", 
            use_container_width=True,
            disabled=st.session_state.div_selected_option is None
        )
    
    # Handle submission
    if submit_button and st.session_state.div_selected_option:
        st.session_state.div_user_answer = st.session_state.div_selected_option
        st.session_state.div_feedback = True
        st.session_state.div_submitted = True
        st.rerun()
    
    # Show feedback and next button
    handle_div_feedback()

def handle_div_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.get("div_feedback", False):
        show_div_feedback()
    
    if st.session_state.get("div_submitted", False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_div_state()
                st.rerun()

def show_div_feedback():
    """Display feedback for the divisibility problem"""
    user_answer = st.session_state.get("div_user_answer")
    correct_answer = st.session_state.get("div_answer")
    data = st.session_state.get("div_data", {})
    
    if user_answer is None or correct_answer is None or not data:
        return
    
    number = data["number"]
    divisor = data["divisor"]
    rule = data["rule"]
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Correct!** {number:,} {'is' if correct_answer == 'yes' else 'is not'} divisible by {divisor}.")
        
        # Increase difficulty
        old_difficulty = st.session_state.div_rules_difficulty
        st.session_state.div_rules_difficulty = min(
            st.session_state.div_rules_difficulty + 1, 5
        )
        
        if st.session_state.div_rules_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered divisibility rules!**")
        elif old_difficulty < st.session_state.div_rules_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.div_rules_difficulty}**")
        
        show_div_explanation(correct=True)
    
    else:
        st.error(f"❌ **Not quite.** {number:,} {'is' if correct_answer == 'yes' else 'is not'} divisible by {divisor}.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.div_rules_difficulty
        st.session_state.div_rules_difficulty = max(
            st.session_state.div_rules_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.div_rules_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.div_rules_difficulty}. Keep practicing!**")
        
        show_div_explanation(correct=False)

def show_div_explanation(correct=True):
    """Show explanation for the divisibility problem"""
    data = st.session_state.get("div_data", {})
    correct_answer = st.session_state.get("div_answer")
    
    if not data or correct_answer is None:
        return
        
    number = data["number"]
    divisor = data["divisor"]
    rule = data["rule"]
    is_divisible = data["correct"]
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click here for detailed explanation**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Divisibility Rule Explanation:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        ### Number: {number:,}
        ### Divisor: {divisor}
        ### Answer: **{'Yes' if is_divisible else 'No'}** - {number:,} {'is' if is_divisible else 'is not'} divisible by {divisor}
        
        ### Rule Applied:
        **{rule}**
        
        ### Step-by-step check:
        """)
        
        # Show detailed rule application
        if divisor == 2:
            last_digit = number % 10
            st.markdown(f"""
            - **Rule for 2:** Number must end in 0, 2, 4, 6, or 8
            - **Last digit:** {last_digit}
            - **Result:** {last_digit} is {'even' if last_digit % 2 == 0 else 'odd'} → {'✅ Divisible' if last_digit % 2 == 0 else '❌ Not divisible'}
            """)
            
        elif divisor == 3:
            digit_sum = sum(int(d) for d in str(number))
            st.markdown(f"""
            - **Rule for 3:** Sum of digits must be divisible by 3
            - **Digits:** {' + '.join(str(number))} = {digit_sum}
            - **Check:** {digit_sum} ÷ 3 = {digit_sum / 3}
            - **Result:** {'✅ Divisible' if digit_sum % 3 == 0 else '❌ Not divisible'}
            """)
            
        elif divisor == 4:
            last_two = number % 100
            st.markdown(f"""
            - **Rule for 4:** Last two digits must be divisible by 4
            - **Last two digits:** {last_two:02d}
            - **Check:** {last_two} ÷ 4 = {last_two / 4}
            - **Result:** {'✅ Divisible' if last_two % 4 == 0 else '❌ Not divisible'}
            """)
            
        elif divisor == 5:
            last_digit = number % 10
            st.markdown(f"""
            - **Rule for 5:** Number must end in 0 or 5
            - **Last digit:** {last_digit}
            - **Result:** {'✅ Divisible' if last_digit in [0, 5] else '❌ Not divisible'}
            """)
            
        elif divisor == 6:
            is_even = number % 2 == 0
            digit_sum = sum(int(d) for d in str(number))
            div_by_3 = digit_sum % 3 == 0
            st.markdown(f"""
            - **Rule for 6:** Must be divisible by BOTH 2 and 3
            - **Divisible by 2:** {'✅ Yes' if is_even else '❌ No'} (ends in {number % 10})
            - **Divisible by 3:** {'✅ Yes' if div_by_3 else '❌ No'} (digit sum = {digit_sum})
            - **Result:** {'✅ Divisible' if is_even and div_by_3 else '❌ Not divisible'}
            """)
            
        elif divisor == 8:
            last_three = number % 1000
            st.markdown(f"""
            - **Rule for 8:** Last three digits must be divisible by 8
            - **Last three digits:** {last_three:03d}
            - **Check:** {last_three} ÷ 8 = {last_three / 8}
            - **Result:** {'✅ Divisible' if last_three % 8 == 0 else '❌ Not divisible'}
            """)
            
        elif divisor == 9:
            digit_sum = sum(int(d) for d in str(number))
            st.markdown(f"""
            - **Rule for 9:** Sum of digits must be divisible by 9
            - **Digits:** {' + '.join(str(number))} = {digit_sum}
            - **Check:** {digit_sum} ÷ 9 = {digit_sum / 9}
            - **Result:** {'✅ Divisible' if digit_sum % 9 == 0 else '❌ Not divisible'}
            """)
            
        elif divisor == 10:
            last_digit = number % 10
            st.markdown(f"""
            - **Rule for 10:** Number must end in 0
            - **Last digit:** {last_digit}
            - **Result:** {'✅ Divisible' if last_digit == 0 else '❌ Not divisible'}
            """)
            
        elif divisor == 11:
            digits = [int(d) for d in str(number)]
            alt_sum = sum(digits[i] * (-1)**i for i in range(len(digits)))
            st.markdown(f"""
            - **Rule for 11:** Alternating sum of digits must be divisible by 11
            - **Calculation:** {' - '.join([str(d) if i % 2 == 0 else f'({d})' for i, d in enumerate(digits)])} = {alt_sum}
            - **Check:** {alt_sum} ÷ 11 = {alt_sum / 11 if alt_sum != 0 else 0}
            - **Result:** {'✅ Divisible' if alt_sum % 11 == 0 else '❌ Not divisible'}
            """)
            
        elif divisor == 12:
            is_div_3 = sum(int(d) for d in str(number)) % 3 == 0
            is_div_4 = (number % 100) % 4 == 0
            st.markdown(f"""
            - **Rule for 12:** Must be divisible by BOTH 3 and 4
            - **Divisible by 3:** {'✅ Yes' if is_div_3 else '❌ No'}
            - **Divisible by 4:** {'✅ Yes' if is_div_4 else '❌ No'}
            - **Result:** {'✅ Divisible' if is_div_3 and is_div_4 else '❌ Not divisible'}
            """)
        
        # Verification
        if is_divisible:
            quotient = number // divisor
            st.markdown(f"""
            ### ✅ Verification:
            **{number:,} ÷ {divisor} = {quotient:,}** (exactly, no remainder)
            """)
        else:
            quotient = number // divisor
            remainder = number % divisor
            st.markdown(f"""
            ### ❌ Verification:
            **{number:,} ÷ {divisor} = {quotient:,} remainder {remainder}** (not exact)
            """)

def reset_div_state():
    """Reset the state for next problem"""
    st.session_state.current_div_problem = None
    st.session_state.div_answer = None
    st.session_state.div_feedback = False
    st.session_state.div_submitted = False
    st.session_state.div_data = {}
    st.session_state.div_selected_option = None  # Reset selection
    
    if "div_user_answer" in st.session_state:
        del st.session_state.div_user_answer