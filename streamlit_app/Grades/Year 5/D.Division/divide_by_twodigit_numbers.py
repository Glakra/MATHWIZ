import streamlit as st
import random

def run():
    """
    Main function to run the Divide by Two-Digit Numbers activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/D. Division/divide_by_two_digit_numbers.py
    """
    # Initialize session state
    if "two_digit_difficulty" not in st.session_state:
        st.session_state.two_digit_difficulty = 1
    
    if "current_two_digit_problem" not in st.session_state:
        st.session_state.current_two_digit_problem = None
        st.session_state.two_digit_quotient = None
        st.session_state.two_digit_remainder = None
        st.session_state.two_digit_feedback = False
        st.session_state.two_digit_submitted = False
        st.session_state.two_digit_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > D. Division**")
    st.title("🔢 Divide by Two-Digit Numbers")
    st.markdown("*Practice division with two-digit divisors and find quotients and remainders*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.two_digit_difficulty
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
    if st.session_state.current_two_digit_problem is None:
        generate_two_digit_problem()
    
    # Display current question
    display_two_digit_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Divide by Two-Digit Numbers:
        
        **Understanding Division:**
        - **Dividend** ÷ **Divisor** = **Quotient** R **Remainder**
        - Example: 52 ÷ 15 = 3 R 7
        
        **Long Division Steps:**
        1. **Estimate:** How many times does the divisor fit into the dividend?
        2. **Multiply:** Multiply your estimate by the divisor
        3. **Subtract:** Subtract from the dividend
        4. **Compare:** The remainder must be less than the divisor
        
        ### Example: 52 ÷ 15
        
        **Step 1:** How many times does 15 go into 52?
        - 15 × 3 = 45 (fits)
        - 15 × 4 = 60 (too big)
        - So quotient is 3
        
        **Step 2:** Find the remainder
        - 52 - 45 = 7
        - Since 7 < 15, our remainder is 7
        
        **Answer:** 52 ÷ 15 = 3 R 7
        
        ### Estimation Tips:
        - **Round the divisor:** 15 becomes 20, 23 becomes 20
        - **Round the dividend:** 52 becomes 50, 147 becomes 150
        - **Use multiplication facts** you know
        - **Check your work:** Quotient × Divisor + Remainder = Dividend
        
        ### Common Mistakes to Avoid:
        - **Remainder too large:** Remainder must be less than divisor
        - **Forgetting to check:** Always verify your answer
        - **Estimation errors:** Practice rounding to help estimate
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Two-digit ÷ two-digit (like 52÷15, 47÷15)
        - **🟠 Level 3:** Larger two-digit divisors (20s, 30s, 40s)
        - **🔴 Level 4-5:** Three-digit dividends with complex remainders
        """)

def generate_two_digit_problem():
    """Generate a two-digit division problem based on difficulty level"""
    difficulty = st.session_state.two_digit_difficulty
    
    # Define problems by difficulty level
    if difficulty == 1:
        # Level 1: Simple two-digit division like in the images
        problems = [
            {"dividend": 52, "divisor": 15},  # From your image: 52÷15 = 3 R 7
            {"dividend": 47, "divisor": 15},  # From your image: 47÷15 = 3 R 2
            {"dividend": 38, "divisor": 12},  # 38÷12 = 3 R 2
            {"dividend": 45, "divisor": 13},  # 45÷13 = 3 R 6
            {"dividend": 56, "divisor": 14},  # 56÷14 = 4 R 0
            {"dividend": 43, "divisor": 11},  # 43÷11 = 3 R 10
            {"dividend": 67, "divisor": 16},  # 67÷16 = 4 R 3
            {"dividend": 58, "divisor": 17},  # 58÷17 = 3 R 7
            {"dividend": 74, "divisor": 18},  # 74÷18 = 4 R 2
            {"dividend": 83, "divisor": 19},  # 83÷19 = 4 R 7
        ]
    elif difficulty == 2:
        # Level 2: Slightly larger numbers
        problems = [
            {"dividend": 89, "divisor": 12},  # 89÷12 = 7 R 5
            {"dividend": 95, "divisor": 14},  # 95÷14 = 6 R 11
            {"dividend": 78, "divisor": 13},  # 78÷13 = 6 R 0
            {"dividend": 91, "divisor": 15},  # 91÷15 = 6 R 1
            {"dividend": 84, "divisor": 16},  # 84÷16 = 5 R 4
            {"dividend": 97, "divisor": 17},  # 97÷17 = 5 R 12
            {"dividend": 85, "divisor": 18},  # 85÷18 = 4 R 13
            {"dividend": 93, "divisor": 19},  # 93÷19 = 4 R 17
            {"dividend": 76, "divisor": 11},  # 76÷11 = 6 R 10
            {"dividend": 88, "divisor": 20},  # 88÷20 = 4 R 8
        ]
    elif difficulty == 3:
        # Level 3: Larger two-digit divisors (20s, 30s, 40s)
        problems = [
            {"dividend": 127, "divisor": 23},  # 127÷23 = 5 R 12
            {"dividend": 145, "divisor": 24},  # 145÷24 = 6 R 1
            {"dividend": 156, "divisor": 25},  # 156÷25 = 6 R 6
            {"dividend": 167, "divisor": 26},  # 167÷26 = 6 R 11
            {"dividend": 189, "divisor": 27},  # 189÷27 = 7 R 0
            {"dividend": 134, "divisor": 32},  # 134÷32 = 4 R 6
            {"dividend": 178, "divisor": 35},  # 178÷35 = 5 R 3
            {"dividend": 195, "divisor": 38},  # 195÷38 = 5 R 5
            {"dividend": 216, "divisor": 41},  # 216÷41 = 5 R 11
            {"dividend": 187, "divisor": 44},  # 187÷44 = 4 R 11
        ]
    elif difficulty == 4:
        # Level 4: Three-digit dividends
        problems = [
            {"dividend": 234, "divisor": 15},  # 234÷15 = 15 R 9
            {"dividend": 287, "divisor": 18},  # 287÷18 = 15 R 17
            {"dividend": 345, "divisor": 23},  # 345÷23 = 15 R 0
            {"dividend": 298, "divisor": 26},  # 298÷26 = 11 R 12
            {"dividend": 367, "divisor": 29},  # 367÷29 = 12 R 19
            {"dividend": 412, "divisor": 32},  # 412÷32 = 12 R 28
            {"dividend": 456, "divisor": 35},  # 456÷35 = 13 R 1
            {"dividend": 523, "divisor": 38},  # 523÷38 = 13 R 29
            {"dividend": 487, "divisor": 41},  # 487÷41 = 11 R 36
            {"dividend": 534, "divisor": 44},  # 534÷44 = 12 R 6
        ]
    else:  # difficulty == 5
        # Level 5: Complex problems with larger numbers
        problems = [
            {"dividend": 567, "divisor": 47},  # 567÷47 = 12 R 3
            {"dividend": 623, "divisor": 52},  # 623÷52 = 11 R 51
            {"dividend": 698, "divisor": 56},  # 698÷56 = 12 R 26
            {"dividend": 745, "divisor": 59},  # 745÷59 = 12 R 37
            {"dividend": 812, "divisor": 63},  # 812÷63 = 12 R 56
            {"dividend": 876, "divisor": 67},  # 876÷67 = 13 R 5
            {"dividend": 934, "divisor": 71},  # 934÷71 = 13 R 11
            {"dividend": 987, "divisor": 74},  # 987÷74 = 13 R 25
            {"dividend": 856, "divisor": 78},  # 856÷78 = 10 R 76
            {"dividend": 923, "divisor": 82},  # 923÷82 = 11 R 21
        ]
    
    # Select a random problem
    problem = random.choice(problems)
    
    # Calculate quotient and remainder
    quotient = problem["dividend"] // problem["divisor"]
    remainder = problem["dividend"] % problem["divisor"]
    
    st.session_state.two_digit_data = problem
    st.session_state.two_digit_quotient = quotient
    st.session_state.two_digit_remainder = remainder
    st.session_state.current_two_digit_problem = f"Divide {problem['dividend']} by {problem['divisor']}"

def display_two_digit_problem():
    """Display the current two-digit division problem interface"""
    data = st.session_state.two_digit_data
    dividend = data["dividend"]
    divisor = data["divisor"]
    
    # Store format type in session state to keep it consistent
    if "division_format_type" not in st.session_state:
        st.session_state.division_format_type = random.choice(["horizontal", "long_division"])
    
    format_type = st.session_state.division_format_type
    
    st.markdown("### 🔢 Division Problem:")
    
    if format_type == "horizontal":
        # Horizontal format like "52 ÷ 15 = __ R __"
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 30px;
            background-color: #f8f9fa;
            border-radius: 10px;
            margin: 20px 0;
        ">
            <div style="font-size: 24px; margin-bottom: 10px;">
                <strong>Divide:</strong>
            </div>
            <div style="font-size: 28px; font-family: 'Courier New', monospace;">
                {dividend} ÷ {divisor} = <span style="color: #666;">__</span> R <span style="color: #666;">__</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Long division format with proper bracket notation
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 30px;
            background-color: #f8f9fa;
            border-radius: 10px;
            margin: 20px 0;
        ">
            <div style="font-size: 24px; margin-bottom: 20px;">
                <strong>Divide:</strong>
            </div>
            <div style="font-size: 24px; font-family: 'Courier New', monospace; line-height: 1.2;">
                <div style="display: inline-block; text-align: left;">
                    <div style="margin-left: 60px; border-bottom: 2px solid #333; padding: 5px 40px;">
                        <span style="color: #666; background-color: white; border: 1px solid #ccc; padding: 2px 8px; margin-right: 5px;">__</span>
                        <span style="font-size: 20px;">R</span>
                        <span style="color: #666; background-color: white; border: 1px solid #ccc; padding: 2px 8px; margin-left: 5px;">__</span>
                    </div>
                    <div style="margin-top: 5px;">
                        <span style="font-size: 20px;">{divisor}</span>
                        <span style="font-size: 28px; margin: 0 5px;">)</span>
                        <span style="font-size: 20px;">{dividend}</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Single form that handles both formats
    with st.form("division_form", clear_on_submit=False):
        if format_type == "horizontal":
            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
            
            with col1:
                st.markdown(f"<div style='text-align: center; font-size: 18px; margin-bottom: 10px;'>{dividend} ÷ {divisor} =</div>", unsafe_allow_html=True)
            
            with col2:
                quotient_input = st.text_input("Quotient", key="quotient_input", label_visibility="collapsed", placeholder="")
            
            with col3:
                st.markdown("<div style='text-align: center; padding-top: 8px; font-size: 18px;'>R</div>", unsafe_allow_html=True)
            
            with col4:
                remainder_input = st.text_input("Remainder", key="remainder_input", label_visibility="collapsed", placeholder="")
        
        else:
            col1, col2, col3, col4, col5 = st.columns([1, 1, 0.5, 1, 1])
            
            with col1:
                st.markdown("<div style='text-align: right; padding-top: 8px;'>Quotient:</div>", unsafe_allow_html=True)
            with col2:
                quotient_input = st.text_input("", key="quotient_input", label_visibility="collapsed", placeholder="")
            with col3:
                st.markdown("<div style='text-align: center; padding-top: 8px;'>R</div>", unsafe_allow_html=True)
            with col4:
                remainder_input = st.text_input("", key="remainder_input", label_visibility="collapsed", placeholder="")
            with col5:
                st.markdown("", unsafe_allow_html=True)  # Empty column for spacing
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        # Handle form submission
        if submit_button:
            if not quotient_input or not remainder_input:
                st.error("Please enter both quotient and remainder")
            elif quotient_input.strip() == "" or remainder_input.strip() == "":
                st.error("Please enter both quotient and remainder")
            else:
                try:
                    user_quotient = int(quotient_input.strip())
                    user_remainder = int(remainder_input.strip())
                    
                    # Store in session state
                    st.session_state.two_digit_user_quotient = user_quotient
                    st.session_state.two_digit_user_remainder = user_remainder
                    st.session_state.two_digit_feedback = True
                    st.session_state.two_digit_submitted = True
                    
                except ValueError:
                    st.error("Please enter valid numbers only")
                except Exception as e:
                    st.error(f"Please check your input: {str(e)}")
    
    # Show feedback and next button
    handle_two_digit_feedback()

def handle_two_digit_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.get("two_digit_feedback", False):
        show_two_digit_feedback()
    
    if st.session_state.get("two_digit_submitted", False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_two_digit_state()
                st.rerun()

def show_two_digit_feedback():
    """Display feedback for the two-digit division problem"""
    user_quotient = st.session_state.get("two_digit_user_quotient")
    user_remainder = st.session_state.get("two_digit_user_remainder")
    correct_quotient = st.session_state.get("two_digit_quotient")
    correct_remainder = st.session_state.get("two_digit_remainder")
    data = st.session_state.get("two_digit_data", {})
    
    # Safety check - ensure we have all the data we need
    if (user_quotient is None or user_remainder is None or 
        correct_quotient is None or correct_remainder is None or 
        not data):
        return
    
    if user_quotient == correct_quotient and user_remainder == correct_remainder:
        st.success(f"🎉 **Perfect!** {data['dividend']} ÷ {data['divisor']} = {correct_quotient} R {correct_remainder}")
        
        # Increase difficulty
        old_difficulty = st.session_state.two_digit_difficulty
        st.session_state.two_digit_difficulty = min(
            st.session_state.two_digit_difficulty + 1, 5
        )
        
        if st.session_state.two_digit_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered two-digit division!**")
        elif old_difficulty < st.session_state.two_digit_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.two_digit_difficulty}**")
        
        show_two_digit_explanation(correct=True)
    
    else:
        # Provide specific feedback about what's wrong
        feedback_parts = []
        if user_quotient != correct_quotient:
            feedback_parts.append(f"quotient should be {correct_quotient} (not {user_quotient})")
        if user_remainder != correct_remainder:
            feedback_parts.append(f"remainder should be {correct_remainder} (not {user_remainder})")
        
        feedback_text = " and ".join(feedback_parts)
        st.error(f"❌ **Not quite right.** The {feedback_text}.")
        
        # Check if remainder is too large
        if user_remainder >= data.get('divisor', 0):
            st.warning(f"⚠️ **Remember:** The remainder must be less than the divisor ({data['divisor']})")
        
        # Decrease difficulty
        old_difficulty = st.session_state.two_digit_difficulty
        st.session_state.two_digit_difficulty = max(
            st.session_state.two_digit_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.two_digit_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.two_digit_difficulty}. Keep practicing!**")
        
        show_two_digit_explanation(correct=False)

def show_two_digit_explanation(correct=True):
    """Show step-by-step explanation for the division problem"""
    data = st.session_state.get("two_digit_data", {})
    correct_quotient = st.session_state.get("two_digit_quotient")
    correct_remainder = st.session_state.get("two_digit_remainder")
    
    # Safety check - ensure we have all the data we need
    if (not data or correct_quotient is None or correct_remainder is None or
        'dividend' not in data or 'divisor' not in data):
        st.error("Unable to show explanation - missing problem data")
        return
        
    dividend = data["dividend"]
    divisor = data["divisor"]
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Step-by-Step Division:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        ### Problem: {dividend} ÷ {divisor}
        
        ### Step 1: Estimate the quotient
        - **Think:** How many times does {divisor} fit into {dividend}?
        - **Try multiples:** 
        """)
        
        # Show useful multiples
        multiples = []
        max_to_show = max(correct_quotient + 2, 5)  # Show at least 5 multiples
        for i in range(1, max_to_show + 1):
            product = divisor * i
            if i <= correct_quotient + 2:  # Show a couple extra for context
                if i == correct_quotient:
                    status = "✅ Perfect fit!"
                elif product > dividend:
                    status = "❌ Too big"
                else:
                    status = "✓ Fits, but not the best"
                multiples.append(f"  - {divisor} × {i} = {product} {status}")
        
        for multiple in multiples:
            st.markdown(multiple)
        
        st.markdown(f"""
        ### Step 2: Calculate the remainder
        - **Multiply:** {divisor} × {correct_quotient} = {divisor * correct_quotient}
        - **Subtract:** {dividend} - {divisor * correct_quotient} = {correct_remainder}
        - **Check:** Is {correct_remainder} < {divisor}? {"✅ Yes" if correct_remainder < divisor else "❌ No - need to adjust"}
        
        ### Final Answer:
        **{dividend} ÷ {divisor} = {correct_quotient} R {correct_remainder}**
        
        ### Verification:
        **Check:** {correct_quotient} × {divisor} + {correct_remainder} = {correct_quotient * divisor} + {correct_remainder} = {correct_quotient * divisor + correct_remainder} = {dividend} ✅
        """)

def reset_two_digit_state():
    """Reset the state for next problem"""
    st.session_state.current_two_digit_problem = None
    st.session_state.two_digit_quotient = None
    st.session_state.two_digit_remainder = None
    st.session_state.two_digit_feedback = False
    st.session_state.two_digit_submitted = False
    st.session_state.two_digit_data = {}
    
    # Clear format type so a new one is chosen for next question
    if "division_format_type" in st.session_state:
        del st.session_state.division_format_type
    
    # Clear user answers
    if "two_digit_user_quotient" in st.session_state:
        del st.session_state.two_digit_user_quotient
    if "two_digit_user_remainder" in st.session_state:
        del st.session_state.two_digit_user_remainder