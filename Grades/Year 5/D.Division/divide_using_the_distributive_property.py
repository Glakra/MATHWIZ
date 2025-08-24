import streamlit as st
import random

def run():
    """
    Main function to run the Divide using Distributive Property practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 3/L. Division/divide_using_the_distributive_property.py
    """
    # Initialize session state for difficulty and game state
    if "divide_distributive_difficulty" not in st.session_state:
        st.session_state.divide_distributive_difficulty = 1  # Start with basic problems
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answers = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 3 > L. Division**")
    st.title("📐 Divide Using the Distributive Property")
    st.markdown("*Break numbers apart to make division easier*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.divide_distributive_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {1: "2-digit ÷ 2-4", 2: "2-digit ÷ 3-6", 3: "3-digit ÷ 2-7"}
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 3 levels)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}/3")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 2:
            st.markdown("**🟠 Intermediate**")
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
        st.markdown("""
        ### How to Play:
        - **Break the number into friendly parts** that are easier to divide
        - **Fill in all the blanks** step by step
        - **Use the distributive property:** (a + b) ÷ c = (a ÷ c) + (b ÷ c)
        
        ### Understanding the Distributive Property:
        - **Split the dividend:** Break it into a "friendly" number + remainder
        - **Divide each part:** Divide both parts by the divisor
        - **Add the results:** Combine the quotients
        
        ### Example:
        **62 ÷ 2:**
        - **Step 1:** 62 = 60 + 2
        - **Step 2:** (60 ÷ 2) + (2 ÷ 2) = 30 + 1 = 31
        
        ### Strategy Tips:
        - **Choose friendly numbers:** Pick multiples that divide evenly
        - **Common splits:** 
          - For ÷2: Use multiples of 20, 40, 60, 80
          - For ÷3: Use multiples of 30, 60, 90
          - For ÷4: Use multiples of 40, 80
          - For ÷5: Use multiples of 50
        
        ### What Makes Numbers "Friendly":
        - **Even tens:** 20, 40, 60, 80 (easy to divide by 2, 4)
        - **Multiples of 30:** 30, 60, 90 (easy to divide by 3, 6)
        - **Multiples of 50:** 50, 100 (easy to divide by 5)
        
        ### Difficulty Levels:
        - **🟡 Level 1:** 2-digit numbers ÷ 2-4
        - **🟠 Level 2:** 2-digit numbers ÷ 3-6  
        - **🔴 Level 3:** 3-digit numbers ÷ 2-7
        
        ### Scoring:
        - ✅ **All correct:** Move to harder problems
        - ❌ **Any wrong:** Practice easier problems
        - 🎯 **Goal:** Master the distributive property for division!
        """)

def generate_new_question():
    """Generate a new distributive property division question"""
    difficulty = st.session_state.divide_distributive_difficulty
    
    # Set number ranges based on difficulty
    if difficulty == 1:
        # 2-digit ÷ 2-4
        divisors = [2, 3, 4]
        min_dividend = 20
        max_dividend = 99
    elif difficulty == 2:
        # 2-digit ÷ 3-6
        divisors = [3, 4, 5, 6]
        min_dividend = 30
        max_dividend = 99
    else:
        # 3-digit ÷ 2-7
        divisors = [2, 3, 4, 5, 6, 7]
        min_dividend = 100
        max_dividend = 300
    
    divisor = random.choice(divisors)
    
    # Generate a dividend that works well with distributive property
    # We want a number that can be split into a "friendly" part + small remainder
    
    # Choose a friendly base number (multiple of 10 or easy to divide)
    if divisor == 2:
        friendly_multiples = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
    elif divisor == 3:
        friendly_multiples = [30, 60, 90, 120, 150, 180, 210, 240, 270]
    elif divisor == 4:
        friendly_multiples = [40, 80, 120, 160, 200, 240, 280]
    elif divisor == 5:
        friendly_multiples = [50, 100, 150, 200, 250]
    elif divisor == 6:
        friendly_multiples = [60, 120, 180, 240]
    else:  # divisor == 7
        friendly_multiples = [70, 140, 210, 280]
    
    # Filter friendly multiples based on difficulty range
    valid_multiples = [m for m in friendly_multiples if min_dividend <= m <= max_dividend - 10]
    friendly_base = random.choice(valid_multiples)
    
    # Add a small remainder (less than the divisor, but not 0)
    remainder_part = random.randint(1, min(divisor - 1, max_dividend - friendly_base))
    remainder_part = max(1, remainder_part)  # Ensure at least 1
    
    dividend = friendly_base + remainder_part
    
    # Calculate all the answers
    final_answer = dividend // divisor
    friendly_quotient = friendly_base // divisor
    remainder_quotient = remainder_part // divisor
    
    # Store question data
    st.session_state.question_data = {
        "dividend": dividend,
        "divisor": divisor,
        "friendly_base": friendly_base,
        "remainder_part": remainder_part,
        "final_answer": final_answer,
        "friendly_quotient": friendly_quotient,
        "remainder_quotient": remainder_quotient
    }
    
    # Set up correct answers for validation
    st.session_state.correct_answers = {
        "remainder_part": remainder_part,
        "friendly_quotient": friendly_quotient,
        "sum_result": final_answer,
        "final_answer": final_answer
    }
    
    st.session_state.current_question = f"Find {dividend} ÷ {divisor}. Use the distributive property."

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question with larger, more prominent formatting
    st.markdown("### 📐 Question:")
    st.markdown(f"""
    <div style="
        font-size: 28px; 
        font-weight: bold; 
        color: #1f77b4; 
        background-color: #f0f8ff; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #1f77b4;
        margin: 20px 0;
        text-align: center;
    ">
        {st.session_state.current_question}
    </div>
    """, unsafe_allow_html=True)
    
    # Create the step-by-step breakdown with truly inline inputs
    with st.form("distributive_form", clear_on_submit=False):
        
        # Line 1: Break down the division with inline input
        st.markdown("### ")  # Add some space
        
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 2])
        
        with col1:
            st.markdown(f"""
            <div style="font-size: 24px; font-weight: bold; margin-top: 10px;">
                {data['dividend']} ÷ {data['divisor']} = ( {data['friendly_base']} ÷ {data['divisor']} ) + (
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            remainder_input = st.number_input(
                "missing",
                min_value=1,
                max_value=20,
                value=None,
                step=1,
                key="remainder_part",
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown(f"""
            <div style="font-size: 24px; font-weight: bold; margin-top: 10px;">
                ÷ {data['divisor']} )
            </div>
            """, unsafe_allow_html=True)
        
        # Line 2: Calculate each part with inline input
        st.markdown("### ")  # Add some space
        
        col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
        
        with col1:
            st.markdown("""
            <div style="font-size: 24px; font-weight: bold; margin-top: 10px;">
                =
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            friendly_quotient_input = st.number_input(
                "quotient",
                min_value=0,
                max_value=100,
                value=None,
                step=1,
                key="friendly_quotient",
                label_visibility="collapsed"
            )
        
        with col3:
            st.markdown(f"""
            <div style="font-size: 24px; font-weight: bold; margin-top: 10px;">
                + {data['remainder_quotient']}
            </div>
            """, unsafe_allow_html=True)
        
        # Line 3: Final result with inline input
        st.markdown("### ")  # Add some space
        
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            st.markdown("""
            <div style="font-size: 24px; font-weight: bold; margin-top: 10px;">
                =
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            final_answer_input = st.number_input(
                "answer",
                min_value=0,
                max_value=200,
                value=None,
                step=1,
                key="final_answer",
                label_visibility="collapsed"
            )
        
        # Submit button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit All Answers", type="primary", use_container_width=True)
        
        if submit_button:
            # Validate all answers
            user_answers = {
                "remainder_part": remainder_input,
                "friendly_quotient": friendly_quotient_input,
                "final_answer": final_answer_input
            }
            
            # Check if all fields are filled
            if any(answer is None for answer in user_answers.values()):
                st.error("❌ Please fill in all the blanks before submitting.")
                return
            
            st.session_state.user_answers = user_answers
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
    """Display feedback for the submitted answers"""
    user_answers = st.session_state.user_answers
    correct_answers = st.session_state.correct_answers
    data = st.session_state.question_data
    
    # Check each answer
    all_correct = True
    feedback_messages = []
    
    # Check remainder part
    if user_answers["remainder_part"] == correct_answers["remainder_part"]:
        feedback_messages.append("✅ Remainder part is correct!")
    else:
        all_correct = False
        feedback_messages.append(f"❌ Remainder part: Expected {correct_answers['remainder_part']}, got {user_answers['remainder_part']}")
    
    # Check friendly quotient
    if user_answers["friendly_quotient"] == correct_answers["friendly_quotient"]:
        feedback_messages.append("✅ Friendly quotient is correct!")
    else:
        all_correct = False
        feedback_messages.append(f"❌ Friendly quotient: Expected {correct_answers['friendly_quotient']}, got {user_answers['friendly_quotient']}")
    
    # Check final answer
    if user_answers["final_answer"] == correct_answers["final_answer"]:
        feedback_messages.append("✅ Final answer is correct!")
    else:
        all_correct = False
        feedback_messages.append(f"❌ Final answer: Expected {correct_answers['final_answer']}, got {user_answers['final_answer']}")
    
    # Display overall result
    if all_correct:
        st.success("🎉 **Perfect! All answers are correct!**")
        
        # Increase difficulty (max level 3)
        old_difficulty = st.session_state.divide_distributive_difficulty
        st.session_state.divide_distributive_difficulty = min(
            st.session_state.divide_distributive_difficulty + 1, 3
        )
        
        # Show encouragement based on difficulty
        if st.session_state.divide_distributive_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered the distributive property for division!**")
        elif old_difficulty < st.session_state.divide_distributive_difficulty:
            st.info(f"⬆️ **Level up! Now working with harder problems**")
    
    else:
        st.error("❌ **Some answers need correction. Let's review:**")
        
        # Decrease difficulty (min level 1)
        old_difficulty = st.session_state.divide_distributive_difficulty
        st.session_state.divide_distributive_difficulty = max(
            st.session_state.divide_distributive_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.divide_distributive_difficulty:
            st.warning(f"⬇️ **Let's practice easier problems first. Keep going!**")
    
    # Show detailed feedback
    for message in feedback_messages:
        if "✅" in message:
            st.success(message)
        else:
            st.error(message)
    
    # Always show explanation
    show_explanation()

def show_explanation():
    """Show explanation for the correct solution"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for detailed explanation**", expanded=True):
        st.markdown(f"""
        ### Complete Solution:
        
        **Problem:** {data['dividend']} ÷ {data['divisor']}
        
        ### Step-by-step breakdown:
        
        **Step 1: Break down the number**
        - We split {data['dividend']} into {data['friendly_base']} + {data['remainder_part']}
        - **Why {data['friendly_base']}?** It's a "friendly" number that divides evenly by {data['divisor']}
        - **Why {data['remainder_part']}?** It's what's left over: {data['dividend']} - {data['friendly_base']} = {data['remainder_part']}
        
        **Step 2: Apply the distributive property**
        - **{data['dividend']} ÷ {data['divisor']} = ({data['friendly_base']} + {data['remainder_part']}) ÷ {data['divisor']}**
        - **= ({data['friendly_base']} ÷ {data['divisor']}) + ({data['remainder_part']} ÷ {data['divisor']})**
        - **= {data['friendly_quotient']} + {data['remainder_quotient']}**
        
        **Step 3: Add the results**
        - **{data['friendly_quotient']} + {data['remainder_quotient']} = {data['final_answer']}**
        
        ### Why this works:
        - **Distributive Property:** (a + b) ÷ c = (a ÷ c) + (b ÷ c)
        - **Friendly numbers** make mental math easier
        - **Breaking apart** helps us avoid complex long division
        
        ### Check our work:
        - **{data['final_answer']} × {data['divisor']} = {data['final_answer'] * data['divisor']}**
        - **Does {data['final_answer'] * data['divisor']} = {data['dividend']}?** {"✅ Yes!" if data['final_answer'] * data['divisor'] == data['dividend'] else "❌ No"}
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answers = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answers" in st.session_state:
        del st.session_state.user_answers