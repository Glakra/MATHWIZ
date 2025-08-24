import streamlit as st
import random

def run():
    """
    Main function to run the Compare Fractions with Unlike Denominators activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A.Place values and number sense/compare_fractions_with_unlike_denominators.py
    """
    # Initialize session state
    if "compare_fractions_direct_score" not in st.session_state:
        st.session_state.compare_fractions_direct_score = 0
        st.session_state.compare_fractions_direct_attempts = 0
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.selected_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("🔢 Compare Fractions with Unlike Denominators")
    st.markdown("*Compare fractions by finding common denominators or using other strategies*")
    st.markdown("---")
    
    # Score display
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.session_state.compare_fractions_direct_attempts > 0:
            accuracy = (st.session_state.compare_fractions_direct_score / st.session_state.compare_fractions_direct_attempts) * 100
            st.metric("Score", f"{st.session_state.compare_fractions_direct_score}/{st.session_state.compare_fractions_direct_attempts}", 
                     f"{accuracy:.0f}%")
        else:
            st.metric("Score", "0/0", "Start practicing!")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Read the question** - Which fraction is greater/less?
        - **Click on your answer** - Select the correct fraction
        - **Watch for equal fractions** - Sometimes they're the same!
        - **Submit your answer** to check if you're correct
        
        ### Strategies for Comparing Fractions:
        
        **1. Same Numerators:**
        - If tops are the same, smaller bottom = larger fraction
        - Example: 3/4 > 3/8 (fourths are bigger than eighths)
        
        **2. Same Denominators:**
        - If bottoms are the same, larger top = larger fraction
        - Example: 5/8 > 3/8 (5 parts is more than 3 parts)
        
        **3. Cross Multiplication:**
        - Multiply diagonally and compare
        - Example: 2/3 vs 3/4 → 2×4 = 8, 3×3 = 9 → 3/4 is larger
        
        **4. Common Denominators:**
        - Convert to same denominator
        - Example: 1/2 = 4/8, so 5/8 > 1/2
        
        **5. Benchmark to 1/2:**
        - Is each fraction more or less than 1/2?
        - Example: 2/5 < 1/2 < 3/5
        
        ### Quick Checks:
        - **Unit fractions:** 1/2 > 1/3 > 1/4 > 1/5...
        - **Close to 1:** 7/8 > 5/6 > 3/4
        - **Close to 0:** 1/8 < 1/4 < 1/3
        
        ### Remember:
        - Some fractions are **equivalent** (equal)
        - Examples: 1/2 = 2/4 = 3/6 = 4/8
        - Watch for the "neither; they are equal" option!
        """)

def generate_new_problem():
    """Generate a new fraction comparison problem"""
    
    problems = [
        # Problems with two different fractions
        {
            "fraction1": (3, 4),
            "fraction2": (1, 2),
            "question": "Which fraction is greater?",
            "correct_answer": (3, 4),
            "has_equal_option": False,
            "explanation": "3/4 is greater than 1/2. (3/4 = 6/8 and 1/2 = 4/8)"
        },
        {
            "fraction1": (1, 2),
            "fraction2": (1, 6),
            "question": "Which fraction is less?",
            "correct_answer": (1, 6),
            "has_equal_option": False,
            "explanation": "1/6 is less than 1/2. When numerators are the same, larger denominator means smaller fraction."
        },
        {
            "fraction1": (2, 3),
            "fraction2": (3, 4),
            "question": "Which fraction is less?",
            "correct_answer": (2, 3),
            "has_equal_option": False,
            "explanation": "2/3 is less than 3/4. (2/3 = 8/12 and 3/4 = 9/12)"
        },
        {
            "fraction1": (5, 8),
            "fraction2": (1, 2),
            "question": "Which fraction is greater?",
            "correct_answer": (5, 8),
            "has_equal_option": False,
            "explanation": "5/8 is greater than 1/2. (1/2 = 4/8, so 5/8 > 4/8)"
        },
        {
            "fraction1": (2, 5),
            "fraction2": (3, 10),
            "question": "Which fraction is greater?",
            "correct_answer": (2, 5),
            "has_equal_option": False,
            "explanation": "2/5 is greater than 3/10. (2/5 = 4/10, so 4/10 > 3/10)"
        },
        {
            "fraction1": (3, 5),
            "fraction2": (5, 8),
            "question": "Which fraction is less?",
            "correct_answer": (3, 5),
            "has_equal_option": False,
            "explanation": "3/5 is less than 5/8. (3/5 = 24/40 and 5/8 = 25/40)"
        },
        {
            "fraction1": (1, 3),
            "fraction2": (2, 7),
            "question": "Which fraction is greater?",
            "correct_answer": (1, 3),
            "has_equal_option": False,
            "explanation": "1/3 is greater than 2/7. (1/3 = 7/21 and 2/7 = 6/21)"
        },
        {
            "fraction1": (4, 9),
            "fraction2": (1, 2),
            "question": "Which fraction is less?",
            "correct_answer": (4, 9),
            "has_equal_option": False,
            "explanation": "4/9 is less than 1/2. (4/9 < 4.5/9 = 1/2)"
        },
        {
            "fraction1": (7, 10),
            "fraction2": (2, 3),
            "question": "Which fraction is greater?",
            "correct_answer": (7, 10),
            "has_equal_option": False,
            "explanation": "7/10 is greater than 2/3. (7/10 = 21/30 and 2/3 = 20/30)"
        },
        {
            "fraction1": (3, 8),
            "fraction2": (2, 5),
            "question": "Which fraction is less?",
            "correct_answer": (3, 8),
            "has_equal_option": False,
            "explanation": "3/8 is less than 2/5. (3/8 = 15/40 and 2/5 = 16/40)"
        },
        
        # Problems with equal fractions (has_equal_option = True)
        {
            "fraction1": (1, 2),
            "fraction2": (2, 4),
            "question": "Which fraction is greater?",
            "correct_answer": "equal",
            "has_equal_option": True,
            "explanation": "1/2 and 2/4 are equal. They represent the same amount."
        },
        {
            "fraction1": (2, 3),
            "fraction2": (4, 6),
            "question": "Which fraction is less?",
            "correct_answer": "equal",
            "has_equal_option": True,
            "explanation": "2/3 and 4/6 are equal. 4/6 simplifies to 2/3."
        },
        {
            "fraction1": (3, 4),
            "fraction2": (6, 8),
            "question": "Which fraction is greater?",
            "correct_answer": "equal",
            "has_equal_option": True,
            "explanation": "3/4 and 6/8 are equal. 6/8 simplifies to 3/4."
        },
        {
            "fraction1": (1, 5),
            "fraction2": (2, 10),
            "question": "Which fraction is less?",
            "correct_answer": "equal",
            "has_equal_option": True,
            "explanation": "1/5 and 2/10 are equal. They represent the same amount."
        },
        {
            "fraction1": (4, 5),
            "fraction2": (8, 10),
            "question": "Which fraction is greater?",
            "correct_answer": "equal",
            "has_equal_option": True,
            "explanation": "4/5 and 8/10 are equal. 8/10 simplifies to 4/5."
        },
        
        # More challenging comparisons
        {
            "fraction1": (5, 6),
            "fraction2": (7, 8),
            "question": "Which fraction is less?",
            "correct_answer": (5, 6),
            "has_equal_option": False,
            "explanation": "5/6 is less than 7/8. Both are close to 1, but 7/8 is closer."
        },
        {
            "fraction1": (4, 7),
            "fraction2": (5, 9),
            "question": "Which fraction is greater?",
            "correct_answer": (4, 7),
            "has_equal_option": False,
            "explanation": "4/7 is greater than 5/9. (4/7 = 36/63 and 5/9 = 35/63)"
        },
        {
            "fraction1": (3, 11),
            "fraction2": (2, 7),
            "question": "Which fraction is less?",
            "correct_answer": (3, 11),
            "has_equal_option": False,
            "explanation": "3/11 is less than 2/7. (3/11 = 21/77 and 2/7 = 22/77)"
        },
        {
            "fraction1": (5, 12),
            "fraction2": (3, 8),
            "question": "Which fraction is greater?",
            "correct_answer": (5, 12),
            "has_equal_option": False,
            "explanation": "5/12 is greater than 3/8. (5/12 = 10/24 and 3/8 = 9/24)"
        },
        {
            "fraction1": (7, 15),
            "fraction2": (1, 2),
            "question": "Which fraction is less?",
            "correct_answer": (7, 15),
            "has_equal_option": False,
            "explanation": "7/15 is less than 1/2. (7/15 < 7.5/15 = 1/2)"
        }
    ]
    
    st.session_state.current_problem = random.choice(problems)
    st.session_state.selected_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def display_problem():
    """Display the current fraction comparison problem"""
    
    problem = st.session_state.current_problem
    
    # Display question
    st.markdown(f"### {problem['question']}")
    
    # Get fractions
    frac1 = problem['fraction1']
    frac2 = problem['fraction2']
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create clickable options based on whether equal option exists
    if problem['has_equal_option']:
        # Three columns for three options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            frac1_text = f"{frac1[0]}/{frac1[1]}"
            if st.button(frac1_text, key="frac1_btn", 
                        type="primary" if st.session_state.selected_answer == frac1 else "secondary",
                        use_container_width=True):
                st.session_state.selected_answer = frac1
                st.rerun()
        
        with col2:
            frac2_text = f"{frac2[0]}/{frac2[1]}"
            if st.button(frac2_text, key="frac2_btn",
                        type="primary" if st.session_state.selected_answer == frac2 else "secondary",
                        use_container_width=True):
                st.session_state.selected_answer = frac2
                st.rerun()
        
        with col3:
            equal_text = "neither;\nthey are\nequal"
            if st.button(equal_text, key="equal_btn",
                        type="primary" if st.session_state.selected_answer == "equal" else "secondary",
                        use_container_width=True):
                st.session_state.selected_answer = "equal"
                st.rerun()
    else:
        # Two columns for two options
        col1, col2 = st.columns(2)
        
        with col1:
            frac1_text = f"{frac1[0]}/{frac1[1]}"
            if st.button(frac1_text, key="frac1_btn", 
                        type="primary" if st.session_state.selected_answer == frac1 else "secondary",
                        use_container_width=True):
                st.session_state.selected_answer = frac1
                st.rerun()
        
        with col2:
            frac2_text = f"{frac2[0]}/{frac2[1]}"
            if st.button(frac2_text, key="frac2_btn",
                        type="primary" if st.session_state.selected_answer == frac2 else "secondary",
                        use_container_width=True):
                st.session_state.selected_answer = frac2
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", type="primary", use_container_width=True, 
                    disabled=st.session_state.answer_submitted):
            if st.session_state.selected_answer:
                check_answer()
            else:
                st.warning("Please select an answer before submitting!")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                st.session_state.current_problem = None
                st.rerun()

def check_answer():
    """Check if the selected answer is correct"""
    
    problem = st.session_state.current_problem
    correct_answer = problem['correct_answer']
    
    st.session_state.answer_submitted = True
    st.session_state.compare_fractions_direct_attempts += 1
    
    if st.session_state.selected_answer == correct_answer:
        st.session_state.compare_fractions_direct_score += 1
    
    st.session_state.show_feedback = True

def show_feedback():
    """Display feedback for the submitted answer"""
    
    problem = st.session_state.current_problem
    correct_answer = problem['correct_answer']
    
    if st.session_state.selected_answer == correct_answer:
        st.success(f"🎉 **Correct! {problem['explanation']}**")
        
        # Add visual celebration for streaks
        if st.session_state.compare_fractions_direct_score % 5 == 0:
            st.balloons()
    else:
        if correct_answer == "equal":
            st.error(f"❌ **Not quite. The fractions are equal!**")
        else:
            st.error(f"❌ **Not quite. The correct answer is {correct_answer[0]}/{correct_answer[1]}**")
        st.info(f"💡 **{problem['explanation']}**")
        
        # Additional tips based on the type of error
        with st.expander("📚 **Learn More**", expanded=True):
            if correct_answer == "equal":
                st.markdown("""
                ### These fractions are equivalent!
                
                **How to recognize equivalent fractions:**
                - Multiply or divide both top and bottom by the same number
                - Simplify to lowest terms to check
                - Cross multiply: if products are equal, fractions are equal
                
                **Common equivalent fractions:**
                - 1/2 = 2/4 = 3/6 = 4/8 = 5/10
                - 1/3 = 2/6 = 3/9 = 4/12
                - 2/3 = 4/6 = 6/9 = 8/12
                - 1/4 = 2/8 = 3/12 = 4/16
                - 3/4 = 6/8 = 9/12 = 12/16
                """)
            else:
                st.markdown("""
                ### Strategy Review:
                
                **Method 1: Common Denominators**
                - Find the LCM of the denominators
                - Convert both fractions
                - Compare the numerators
                
                **Method 2: Cross Multiplication**
                - For a/b vs c/d: compare a×d with b×c
                - Larger product = larger fraction
                
                **Method 3: Decimal Conversion**
                - Divide numerator by denominator
                - Compare the decimal values
                
                **Quick Tricks:**
                - Same numerator? Smaller denominator wins
                - Compare to 1/2 as a benchmark
                - Think about how close each is to 0 or 1
                """)