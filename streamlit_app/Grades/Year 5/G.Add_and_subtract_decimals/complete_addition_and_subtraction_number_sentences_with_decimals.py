import streamlit as st
import random

def run():
    """
    Main function to run the Complete addition and subtraction number sentences with decimals activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/G. Add and subtract decimals/complete_addition_and_subtraction_number_sentences_with_decimals.py
    """
    # Initialize session state
    if "decimal_sentences_problem" not in st.session_state:
        st.session_state.decimal_sentences_problem = None
        st.session_state.decimal_answer_submitted = False
        st.session_state.user_answer = ""
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > G. Add and subtract decimals**")
    st.title("✏️ Complete Addition and Subtraction Number Sentences")
    st.markdown("*Fill in the missing number to complete the equation*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.decimal_sentences_problem is None:
        st.session_state.decimal_sentences_problem = generate_problem()
        st.session_state.decimal_answer_submitted = False
        st.session_state.user_answer = ""
    
    problem = st.session_state.decimal_sentences_problem
    
    # Display the question
    st.markdown("### 📝 Fill in the missing number:")
    
    # Create the equation display with input box
    equation_html = create_equation_display(problem)
    st.markdown(equation_html, unsafe_allow_html=True)
    
    # Create columns for better layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Input field for answer
        if not st.session_state.decimal_answer_submitted:
            user_input = st.text_input(
                "Your answer:",
                value=st.session_state.user_answer,
                key="answer_input",
                label_visibility="collapsed",
                placeholder="Enter decimal"
            )
            st.session_state.user_answer = user_input
        
        # Submit button
        if st.button("✅ Submit", type="primary", use_container_width=True,
                     disabled=st.session_state.decimal_answer_submitted):
            
            if st.session_state.user_answer.strip() == "":
                st.warning("⚠️ Please enter a number.")
            else:
                try:
                    # Validate the input is a valid number
                    float(st.session_state.user_answer)
                    st.session_state.decimal_answer_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("❌ Please enter a valid decimal number.")
    
    # Show feedback if answer was submitted
    if st.session_state.decimal_answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.decimal_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.decimal_sentences_problem = None
                st.session_state.decimal_answer_submitted = False
                st.session_state.user_answer = ""
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the equation** with a missing number
        - **Figure out** what number makes the equation true
        - **Type your answer** in the box
        - **Click Submit** to check your answer
        
        ### Types of Problems:
        1. **Missing difference:** `a - ? = c` (What do I subtract from a to get c?)
        2. **Missing subtrahend:** `? - b = c` (What number minus b equals c?)
        3. **Missing addend:** `? + b = c` (What plus b equals c?)
        4. **Missing sum:** `a + ? = c` (What do I add to a to get c?)
        
        ### Tips for Success:
        - **Use inverse operations:**
          - For `a - ? = c`, think: `? = a - c`
          - For `? - b = c`, think: `? = c + b`
          - For `? + b = c`, think: `? = c - b`
          - For `a + ? = c`, think: `? = c - a`
        
        ### Examples:
        - `0.6 - ? = 0.4` → `? = 0.6 - 0.4 = 0.2`
        - `? + 0.3 = 0.8` → `? = 0.8 - 0.3 = 0.5`
        - `? - 0.2 = 0.7` → `? = 0.7 + 0.2 = 0.9`
        
        ### Remember:
        - Check your answer by substituting it back
        - Work carefully with decimal places
        - Think about the relationship between addition and subtraction
        """)

def generate_problem():
    """Generate a random addition or subtraction problem with a missing number"""
    problem_types = [
        'subtract_missing_subtrahend',  # a - ? = c
        'subtract_missing_minuend',     # ? - b = c  
        'add_missing_first',            # ? + b = c
        'add_missing_second'            # a + ? = c
    ]
    
    problem_type = random.choice(problem_types)
    
    if problem_type == 'subtract_missing_subtrahend':
        # a - ? = c format
        # Generate a and c such that a > c
        a = round(random.uniform(0.5, 2.0), 1)
        c = round(random.uniform(0.1, a - 0.1), 1)
        missing = round(a - c, 1)
        
        return {
            'type': problem_type,
            'equation': f"{a} - ? = {c}",
            'display_parts': {
                'before_box': f"{a} - ",
                'after_box': f" = {c}"
            },
            'answer': missing,
            'explanation': f"Since {a} - ? = {c}, we need to find what number subtracted from {a} gives {c}. That's {a} - {c} = {missing}."
        }
    
    elif problem_type == 'subtract_missing_minuend':
        # ? - b = c format
        b = round(random.uniform(0.1, 1.5), 1)
        c = round(random.uniform(0.1, 1.5), 1)
        missing = round(b + c, 1)
        
        return {
            'type': problem_type,
            'equation': f"? - {b} = {c}",
            'display_parts': {
                'before_box': "",
                'after_box': f" - {b} = {c}"
            },
            'answer': missing,
            'explanation': f"Since ? - {b} = {c}, we need to find what number minus {b} equals {c}. That's {c} + {b} = {missing}."
        }
    
    elif problem_type == 'add_missing_first':
        # ? + b = c format
        b = round(random.uniform(0.1, 1.5), 1)
        c = round(random.uniform(b + 0.1, 3.0), 1)
        missing = round(c - b, 1)
        
        return {
            'type': problem_type,
            'equation': f"? + {b} = {c}",
            'display_parts': {
                'before_box': "",
                'after_box': f" + {b} = {c}"
            },
            'answer': missing,
            'explanation': f"Since ? + {b} = {c}, we need to find what number plus {b} equals {c}. That's {c} - {b} = {missing}."
        }
    
    else:  # add_missing_second
        # a + ? = c format
        a = round(random.uniform(0.1, 1.5), 1)
        c = round(random.uniform(a + 0.1, 3.0), 1)
        missing = round(c - a, 1)
        
        return {
            'type': problem_type,
            'equation': f"{a} + ? = {c}",
            'display_parts': {
                'before_box': f"{a} + ",
                'after_box': f" = {c}"
            },
            'answer': missing,
            'explanation': f"Since {a} + ? = {c}, we need to find what number added to {a} equals {c}. That's {c} - {a} = {missing}."
        }

def create_equation_display(problem):
    """Create HTML for the equation display with input box styling"""
    if st.session_state.decimal_answer_submitted:
        # Show the completed equation with the user's answer
        user_answer = st.session_state.user_answer
        is_correct = abs(float(user_answer) - problem['answer']) < 0.01
        box_color = "#4CAF50" if is_correct else "#f44336"
        
        equation_html = f"""
        <div style="
            text-align: center;
            margin: 40px 0;
            font-size: 36px;
            font-family: monospace;
        ">
            <span>{problem['display_parts']['before_box']}</span>
            <span style="
                display: inline-block;
                background-color: {box_color}20;
                border: 2px solid {box_color};
                border-radius: 8px;
                padding: 8px 20px;
                min-width: 80px;
                color: {box_color};
                font-weight: bold;
            ">{user_answer}</span>
            <span>{problem['display_parts']['after_box']}</span>
        </div>
        """
    else:
        # Show empty box for input
        equation_html = f"""
        <div style="
            text-align: center;
            margin: 40px 0;
            font-size: 36px;
            font-family: monospace;
        ">
            <span>{problem['display_parts']['before_box']}</span>
            <span style="
                display: inline-block;
                background-color: #f0f0f0;
                border: 2px dashed #999;
                border-radius: 8px;
                padding: 8px 20px;
                min-width: 80px;
                color: #666;
            ">?</span>
            <span>{problem['display_parts']['after_box']}</span>
        </div>
        """
    
    return equation_html

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.decimal_sentences_problem
    
    try:
        user_answer = float(st.session_state.user_answer)
        
        # Check if answer is correct (within small tolerance for decimal precision)
        if abs(user_answer - problem['answer']) < 0.01:
            st.success("🎉 **Excellent! That's correct!**")
            
            # Show the complete equation
            complete_equation = problem['equation'].replace('?', str(problem['answer']))
            st.info(f"✓ {complete_equation}")
            
        else:
            st.error(f"❌ **Not quite right.** The correct answer is **{problem['answer']}**")
            
            # Show explanation
            with st.expander("📖 **See explanation**", expanded=True):
                st.markdown(problem['explanation'])
                
                # Show verification
                complete_equation = problem['equation'].replace('?', str(problem['answer']))
                st.markdown(f"**Check:** {complete_equation} ✓")
                
                # Show what the user's answer gives
                user_equation = problem['equation'].replace('?', str(user_answer))
                st.markdown(f"**Your answer:** {user_equation} ✗")
                
    except ValueError:
        st.error("❌ Invalid number format.")