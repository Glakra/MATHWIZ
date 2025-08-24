import streamlit as st
import random

def run():
    """
    Main function to run the Convert Decimals between Standard and Expanded Form using Fractions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Decimals/convert_decimals_between_standard_and_expanded_form_using_fractions.py
    """
    # Initialize session state
    if "expanded_form_difficulty" not in st.session_state:
        st.session_state.expanded_form_difficulty = 1  # Start with simple forms
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = "new"  # Start with new question needed
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Decimals**")
    st.title("🔢 Convert Decimals: Standard and Expanded Form using Fractions")
    st.markdown("*Convert expressions like 5 × 1/10 + 2 × 1/100 to standard decimal form*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.expanded_form_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "tenths & hundredths", 
            2: "ones, tenths & hundredths", 
            3: "tenths, hundredths & thousandths",
            4: "ones, tenths, hundredths & thousandths"
        }
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 4 levels)
        progress = (difficulty_level - 1) / 3  # Convert 1-4 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 2:
            st.markdown("**🟠 Intermediate**")
        elif difficulty_level == 3:
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
    if st.session_state.current_question == "new":
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Read the expanded form** with fractions
        - **Click the correct standard decimal form** from the options
        - **Think about place values** and what each fraction represents
        
        ### Key Concepts:
        - **1** = ones place
        - **1/10** = tenths place (0.1)
        - **1/100** = hundredths place (0.01)
        - **1/1000** = thousandths place (0.001)
        
        ### Conversion Process:
        1. **Multiply each coefficient** by its place value
        2. **Add all the results** together
        3. **Write as a decimal** number
        
        ### Examples:
        - **5 × 1/10 + 2 × 1/100** = 0.5 + 0.02 = **0.52**
        - **7 × 1 + 5 × 1/10** = 7 + 0.5 = **7.5**
        - **3 × 1/10 + 4 × 1/100** = 0.3 + 0.04 = **0.34**
        - **2 × 1 + 3 × 1/10 + 4 × 1/100** = 2 + 0.3 + 0.04 = **2.34**
        
        ### Place Value Breakdown:
        - **1/10 = 0.1** (one tenth)
        - **1/100 = 0.01** (one hundredth)  
        - **1/1000 = 0.001** (one thousandth)
        - **Multiply by the coefficient** to get the actual value
        
        ### Step-by-Step Method:
        1. **Identify each term**: 5 × 1/10 means 5 tenths
        2. **Convert to decimals**: 5 × 0.1 = 0.5
        3. **Add all terms**: 0.5 + 0.02 = 0.52
        4. **Check your answer**: Does it make sense?
        
        ### Common Mistakes:
        - **Don't confuse place values**: 1/10 ≠ 1/100
        - **Remember to add all terms** together
        - **Check decimal point placement**
        - **Be careful with zeros**: 0.02 not 0.2
        
        ### Difficulty Levels:
        - **🟡 Level 1:** Tenths & hundredths (0.34)
        - **🟠 Level 2:** Ones, tenths & hundredths (7.5)
        - **🟠 Level 3:** Tenths, hundredths & thousandths (0.467)
        - **🔴 Level 4:** All place values (5.594)
        
        ### Scoring:
        - ✅ **Correct answer:** Move to more complex expressions
        - ❌ **Wrong answer:** Practice with simpler expressions
        - 🎯 **Goal:** Master all four place values!
        """)

def generate_new_question():
    """Generate a new expanded form to standard form question"""
    difficulty = st.session_state.expanded_form_difficulty
    
    if difficulty == 1:
        generate_tenths_hundredths_question()
    elif difficulty == 2:
        generate_ones_tenths_hundredths_question()
    elif difficulty == 3:
        generate_tenths_hundredths_thousandths_question()
    else:
        generate_full_question()
    
    # Set current_question to "active" to prevent regeneration
    st.session_state.current_question = "active"

def generate_tenths_hundredths_question():
    """Generate questions with tenths and hundredths only"""
    # Generate random coefficients
    tenths = random.randint(1, 9)
    hundredths = random.randint(1, 9)
    
    # Create expanded form
    expanded_form = f"{tenths} × \\frac{{1}}{{10}} + {hundredths} × \\frac{{1}}{{100}}"
    
    # Calculate correct answer with proper rounding
    correct_answer = round(tenths * 0.1 + hundredths * 0.01, 4)
    
    # Generate distractors
    options = generate_distractors(correct_answer, "tenths_hundredths")
    
    st.session_state.question_data = {
        "expanded_form": expanded_form,
        "correct_answer": correct_answer,
        "options": options,
        "terms": [f"{tenths} × 1/10", f"{hundredths} × 1/100"],
        "calculations": [f"{tenths} × 0.1 = {round(tenths * 0.1, 4)}", f"{hundredths} × 0.01 = {round(hundredths * 0.01, 4)}"],
        "question_type": "tenths_hundredths"
    }

def generate_ones_tenths_hundredths_question():
    """Generate questions with ones, tenths, and hundredths"""
    # Generate random coefficients
    ones = random.randint(1, 9)
    tenths = random.randint(0, 9)
    hundredths = random.randint(0, 9)
    
    # Ensure at least one decimal place
    if tenths == 0 and hundredths == 0:
        tenths = random.randint(1, 9)
    
    # Create expanded form
    terms = []
    if ones > 0:
        terms.append(f"{ones} × 1")
    if tenths > 0:
        terms.append(f"{tenths} × \\frac{{1}}{{10}}")
    if hundredths > 0:
        terms.append(f"{hundredths} × \\frac{{1}}{{100}}")
    
    expanded_form = " + ".join(terms)
    
    # Calculate correct answer with proper rounding
    correct_answer = round(ones + tenths * 0.1 + hundredths * 0.01, 4)
    
    # Generate distractors
    options = generate_distractors(correct_answer, "ones_tenths_hundredths")
    
    calculation_terms = []
    if ones > 0:
        calculation_terms.append(f"{ones} × 1 = {ones}")
    if tenths > 0:
        calculation_terms.append(f"{tenths} × 0.1 = {round(tenths * 0.1, 4)}")
    if hundredths > 0:
        calculation_terms.append(f"{hundredths} × 0.01 = {round(hundredths * 0.01, 4)}")
    
    st.session_state.question_data = {
        "expanded_form": expanded_form,
        "correct_answer": correct_answer,
        "options": options,
        "terms": terms,
        "calculations": calculation_terms,
        "question_type": "ones_tenths_hundredths"
    }

def generate_tenths_hundredths_thousandths_question():
    """Generate questions with tenths, hundredths, and thousandths"""
    # Generate random coefficients
    tenths = random.randint(1, 9)
    hundredths = random.randint(0, 9)
    thousandths = random.randint(1, 9)
    
    # Create expanded form
    terms = []
    terms.append(f"{tenths} × \\frac{{1}}{{10}}")
    if hundredths > 0:
        terms.append(f"{hundredths} × \\frac{{1}}{{100}}")
    terms.append(f"{thousandths} × \\frac{{1}}{{1000}}")
    
    expanded_form = " + ".join(terms)
    
    # Calculate correct answer with proper rounding
    correct_answer = round(tenths * 0.1 + hundredths * 0.01 + thousandths * 0.001, 4)
    
    # Generate distractors
    options = generate_distractors(correct_answer, "tenths_hundredths_thousandths")
    
    calculation_terms = []
    calculation_terms.append(f"{tenths} × 0.1 = {round(tenths * 0.1, 4)}")
    if hundredths > 0:
        calculation_terms.append(f"{hundredths} × 0.01 = {round(hundredths * 0.01, 4)}")
    calculation_terms.append(f"{thousandths} × 0.001 = {round(thousandths * 0.001, 4)}")
    
    st.session_state.question_data = {
        "expanded_form": expanded_form,
        "correct_answer": correct_answer,
        "options": options,
        "terms": terms,
        "calculations": calculation_terms,
        "question_type": "tenths_hundredths_thousandths"
    }

def generate_full_question():
    """Generate questions with ones, tenths, hundredths, and thousandths"""
    # Generate random coefficients
    ones = random.randint(1, 9)
    tenths = random.randint(0, 9)
    hundredths = random.randint(0, 9)
    thousandths = random.randint(1, 9)
    
    # Ensure at least one decimal place
    if tenths == 0 and hundredths == 0:
        tenths = random.randint(1, 9)
    
    # Create expanded form
    terms = []
    if ones > 0:
        terms.append(f"{ones} × 1")
    if tenths > 0:
        terms.append(f"{tenths} × \\frac{{1}}{{10}}")
    if hundredths > 0:
        terms.append(f"{hundredths} × \\frac{{1}}{{100}}")
    if thousandths > 0:
        terms.append(f"{thousandths} × \\frac{{1}}{{1000}}")
    
    expanded_form = " + ".join(terms)
    
    # Calculate correct answer with proper rounding
    correct_answer = round(ones + tenths * 0.1 + hundredths * 0.01 + thousandths * 0.001, 4)
    
    # Generate distractors
    options = generate_distractors(correct_answer, "full")
    
    calculation_terms = []
    if ones > 0:
        calculation_terms.append(f"{ones} × 1 = {ones}")
    if tenths > 0:
        calculation_terms.append(f"{tenths} × 0.1 = {round(tenths * 0.1, 4)}")
    if hundredths > 0:
        calculation_terms.append(f"{hundredths} × 0.01 = {round(hundredths * 0.01, 4)}")
    if thousandths > 0:
        calculation_terms.append(f"{thousandths} × 0.001 = {round(thousandths * 0.001, 4)}")
    
    st.session_state.question_data = {
        "expanded_form": expanded_form,
        "correct_answer": correct_answer,
        "options": options,
        "terms": terms,
        "calculations": calculation_terms,
        "question_type": "full"
    }

def generate_distractors(correct_answer, question_type):
    """Generate 3 plausible wrong answers"""
    distractors = []
    
    # Common error patterns
    if question_type == "tenths_hundredths":
        # Errors like missing decimal point, wrong place values
        distractors.append(round(correct_answer * 10, 4))  # Missing decimal point
        distractors.append(round(correct_answer * 100, 4))  # Way off
        distractors.append(round(correct_answer + 0.1, 4))  # Small error
        
    elif question_type == "ones_tenths_hundredths":
        # Errors in ones/tenths confusion
        distractors.append(round(correct_answer * 10, 4))  # Decimal point error
        distractors.append(round(correct_answer - int(correct_answer), 4))  # Missing ones
        distractors.append(round(correct_answer + 0.05, 4))  # Small calculation error
        
    elif question_type == "tenths_hundredths_thousandths":
        # Errors in small decimal places
        distractors.append(round(correct_answer * 1000, 4))  # Major decimal error
        distractors.append(round(correct_answer * 10, 4))  # One decimal place off
        distractors.append(round(correct_answer + 0.001, 4))  # Small error
        
    else:  # full
        # Complex errors
        distractors.append(round(correct_answer * 10, 4))  # Decimal point error
        distractors.append(round(correct_answer / 10, 4))  # Reverse decimal error
        distractors.append(round(correct_answer + 0.1, 4))  # Calculation error
    
    # Remove duplicates and the correct answer
    unique_distractors = []
    for d in distractors:
        if abs(d - correct_answer) > 0.0001 and d not in unique_distractors and d > 0:
            unique_distractors.append(d)
    
    # Add more distractors if needed
    while len(unique_distractors) < 3:
        if correct_answer < 1:
            new_distractor = round(random.uniform(0.001, 0.999), 4)
        else:
            new_distractor = round(random.uniform(0.1, 99.9), 4)
        
        if abs(new_distractor - correct_answer) > 0.0001 and new_distractor not in unique_distractors:
            unique_distractors.append(new_distractor)
    
    # Take only 3 distractors
    options = [correct_answer] + unique_distractors[:3]
    
    # Shuffle the options
    random.shuffle(options)
    
    return options

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display the question
    st.markdown("### 🔢 Find the standard decimal form of:")
    
    # Display the expanded form using LaTeX
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 10px; 
        border: 2px solid #dee2e6;
        text-align: center;
        margin: 20px 0;
        font-size: 20px;
        color: #495057;
    ">
    """, unsafe_allow_html=True)
    
    st.latex(data['expanded_form'])
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display clickable options (like in the images)
    if not st.session_state.show_feedback:
        st.markdown("**Click on the correct answer:**")
        
        # Create a 2x2 grid of clickable tiles
        cols = st.columns(4)
        
        for i, option in enumerate(data['options']):
            with cols[i]:
                # Format the option nicely
                if option == int(option):
                    option_display = str(int(option))
                else:
                    option_display = str(option)
                
                if st.button(
                    option_display,
                    key=f"option_{i}",
                    use_container_width=True,
                    type="secondary"
                ):
                    st.session_state.selected_answer = option
                    st.session_state.user_answer = option
                    st.session_state.show_feedback = True
                    st.session_state.answer_submitted = True
                    st.rerun()
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
        
        # Only show next button after feedback is shown
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    if 'user_answer' not in st.session_state or 'question_data' not in st.session_state:
        st.error("Error: Missing answer or question data")
        return
    
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.question_data['correct_answer']
    
    # Check if answers match (with small tolerance for floating point errors)
    if abs(user_answer - correct_answer) < 0.0001:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 4 levels)
        old_difficulty = st.session_state.expanded_form_difficulty
        st.session_state.expanded_form_difficulty = min(st.session_state.expanded_form_difficulty + 1, 4)
        
        if st.session_state.expanded_form_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered all place values!**")
        elif old_difficulty < st.session_state.expanded_form_difficulty:
            st.info(f"⬆️ **Difficulty increased to Level {st.session_state.expanded_form_difficulty}!**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show correct answer
        if correct_answer == int(correct_answer):
            st.info(f"**Correct answer:** {int(correct_answer)}")
        else:
            st.info(f"**Correct answer:** {correct_answer}")
        
        # Decrease difficulty (min 1 level)
        old_difficulty = st.session_state.expanded_form_difficulty
        st.session_state.expanded_form_difficulty = max(st.session_state.expanded_form_difficulty - 1, 1)
        
        if old_difficulty > st.session_state.expanded_form_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to Level {st.session_state.expanded_form_difficulty}. Keep practicing!**")
    
    # Show explanation
    show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### Step-by-step solution:")
        
        # Show each calculation step
        for i, calculation in enumerate(data['calculations']):
            st.markdown(f"**Step {i+1}:** {calculation}")
        
        # Show the final addition
        if len(data['calculations']) > 1:
            terms_sum = " + ".join([calc.split(" = ")[1] for calc in data['calculations']])
            st.markdown(f"**Final step:** {terms_sum} = **{data['correct_answer']}**")
        
        st.markdown("---")
        
        # Show place value explanation
        st.markdown("### 💡 Place Value Reminder:")
        st.markdown("""
        - **1** = ones place
        - **1/10** = tenths place (0.1)
        - **1/100** = hundredths place (0.01)
        - **1/1000** = thousandths place (0.001)
        """)
        
        # Show conversion tip
        st.markdown("### 🎯 Quick Conversion:")
        st.markdown("""
        1. **Convert each fraction** to its decimal equivalent
        2. **Multiply by the coefficient** (the number in front)
        3. **Add all the results** together
        4. **The sum is your answer!**
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = "new"  # Reset to "new" so new question generates
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    
    # Clear answer-related session state
    keys_to_remove = ['user_answer', 'selected_answer']
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]