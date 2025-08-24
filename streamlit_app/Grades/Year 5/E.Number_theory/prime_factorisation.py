import streamlit as st
import random

def run():
    """
    Main function to run the Prime Factorisation activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Number theory/prime_factorisation.py
    """
    # Initialize session state
    if "prime_fact_difficulty" not in st.session_state:
        st.session_state.prime_fact_difficulty = 1
    
    if "current_prime_fact_problem" not in st.session_state:
        st.session_state.current_prime_fact_problem = None
        st.session_state.prime_fact_answer = None
        st.session_state.prime_fact_feedback = False
        st.session_state.prime_fact_submitted = False
        st.session_state.prime_fact_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Number theory**")
    st.title("🔢 Prime Factorisation")
    st.markdown("*Break down numbers into their prime factors*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.prime_fact_difficulty
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
    if st.session_state.current_prime_fact_problem is None:
        generate_prime_fact_problem()
    
    # Display current question
    display_prime_fact_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### What is Prime Factorisation?
        
        **Prime factorisation** means breaking down a number into **prime numbers** that multiply together to give the original number.
        
        ### Key Rules:
        - Use **only prime numbers** (2, 3, 5, 7, 11, 13, 17, 19, 23...)
        - **All factors must be prime** - no composite numbers allowed!
        - The result should multiply back to the original number
        
        ### Example: Prime factorisation of 12
        
        **Step 1:** Start with the smallest prime (2)
        - 12 ÷ 2 = 6
        
        **Step 2:** Continue with 6
        - 6 ÷ 2 = 3
        
        **Step 3:** 3 is already prime
        - So we stop here
        
        **Answer:** 12 = 2 × 2 × 3
        
        ### Another Example: Prime factorisation of 10
        - 10 ÷ 2 = 5
        - 5 is prime, so we stop
        - **Answer:** 10 = 2 × 5
        
        ### Method - Factor Tree:
        ```
            12
           /  \\
          2    6
              / \\
             2   3
        ```
        **Result:** 2 × 2 × 3
        
        ### Quick Tips:
        - **Start with 2** (if the number is even)
        - **Then try 3, 5, 7, 11...** in order
        - **Stop when you reach prime numbers**
        - **Check your answer** by multiplying back
        
        ### Common Mistakes:
        - ❌ Using composite numbers (like 4, 6, 8, 9)
        - ❌ Not breaking down completely (stopping too early)
        - ❌ Including 1 in the factorisation
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Small numbers (6, 8, 10, 12, 15)
        - **🟠 Level 3:** Medium numbers (18, 20, 24, 30, 36)
        - **🔴 Level 4-5:** Larger numbers (42, 48, 60, 72, 84)
        """)

def generate_prime_fact_problem():
    """Generate a prime factorisation problem based on difficulty level"""
    difficulty = st.session_state.prime_fact_difficulty
    
    # Define problems by difficulty level
    if difficulty == 1:
        # Level 1: Simple numbers with clear factorisation
        problems = [
            {
                "number": 10,
                "correct": "2 × 5",
                "options": ["2 × 2 × 5", "2 × 5", "5", "2 × 10"],
                "factors": [2, 5]
            },
            {
                "number": 6,
                "correct": "2 × 3",
                "options": ["2 × 3", "6", "3 × 3", "2 × 6"],
                "factors": [2, 3]
            },
            {
                "number": 8,
                "correct": "2 × 2 × 2",
                "options": ["2 × 2 × 2", "2 × 4", "8", "4 × 2"],
                "factors": [2, 2, 2]
            },
            {
                "number": 9,
                "correct": "3 × 3",
                "options": ["3 × 3", "9", "3 × 6", "2 × 3"],
                "factors": [3, 3]
            },
            {
                "number": 12,
                "correct": "2 × 2 × 3",
                "options": ["2 × 2 × 3", "2 × 6", "3 × 4", "12"],
                "factors": [2, 2, 3]
            },
        ]
    elif difficulty == 2:
        # Level 2: Slightly more complex
        problems = [
            {
                "number": 14,
                "correct": "2 × 7",
                "options": ["2 × 7", "14", "7 × 7", "2 × 14"],
                "factors": [2, 7]
            },
            {
                "number": 15,
                "correct": "3 × 5",
                "options": ["3 × 5", "15", "5 × 5", "3 × 15"],
                "factors": [3, 5]
            },
            {
                "number": 16,
                "correct": "2 × 2 × 2 × 2",
                "options": ["2 × 2 × 2 × 2", "2 × 8", "4 × 4", "16"],
                "factors": [2, 2, 2, 2]
            },
            {
                "number": 18,
                "correct": "2 × 3 × 3",
                "options": ["2 × 3 × 3", "2 × 9", "3 × 6", "18"],
                "factors": [2, 3, 3]
            },
            {
                "number": 20,
                "correct": "2 × 2 × 5",
                "options": ["2 × 2 × 5", "2 × 10", "4 × 5", "20"],
                "factors": [2, 2, 5]
            },
        ]
    elif difficulty == 3:
        # Level 3: Medium complexity
        problems = [
            {
                "number": 24,
                "correct": "2 × 2 × 2 × 3",
                "options": ["2 × 2 × 2 × 3", "2 × 12", "4 × 6", "3 × 8"],
                "factors": [2, 2, 2, 3]
            },
            {
                "number": 30,
                "correct": "2 × 3 × 5",
                "options": ["2 × 3 × 5", "2 × 15", "5 × 6", "3 × 10"],
                "factors": [2, 3, 5]
            },
            {
                "number": 36,
                "correct": "2 × 2 × 3 × 3",
                "options": ["2 × 2 × 3 × 3", "2 × 18", "4 × 9", "6 × 6"],
                "factors": [2, 2, 3, 3]
            },
            {
                "number": 28,
                "correct": "2 × 2 × 7",
                "options": ["2 × 2 × 7", "2 × 14", "4 × 7", "28"],
                "factors": [2, 2, 7]
            },
            {
                "number": 32,
                "correct": "2 × 2 × 2 × 2 × 2",
                "options": ["2 × 2 × 2 × 2 × 2", "2 × 16", "4 × 8", "32"],
                "factors": [2, 2, 2, 2, 2]
            },
        ]
    elif difficulty == 4:
        # Level 4: More complex numbers
        problems = [
            {
                "number": 42,
                "correct": "2 × 3 × 7",
                "options": ["2 × 3 × 7", "2 × 21", "6 × 7", "3 × 14"],
                "factors": [2, 3, 7]
            },
            {
                "number": 48,
                "correct": "2 × 2 × 2 × 2 × 3",
                "options": ["2 × 2 × 2 × 2 × 3", "2 × 24", "16 × 3", "4 × 12"],
                "factors": [2, 2, 2, 2, 3]
            },
            {
                "number": 54,
                "correct": "2 × 3 × 3 × 3",
                "options": ["2 × 3 × 3 × 3", "2 × 27", "6 × 9", "18 × 3"],
                "factors": [2, 3, 3, 3]
            },
            {
                "number": 60,
                "correct": "2 × 2 × 3 × 5",
                "options": ["2 × 2 × 3 × 5", "2 × 30", "4 × 15", "6 × 10"],
                "factors": [2, 2, 3, 5]
            },
            {
                "number": 56,
                "correct": "2 × 2 × 2 × 7",
                "options": ["2 × 2 × 2 × 7", "2 × 28", "8 × 7", "4 × 14"],
                "factors": [2, 2, 2, 7]
            },
        ]
    else:  # difficulty == 5
        # Level 5: Complex numbers
        problems = [
            {
                "number": 72,
                "correct": "2 × 2 × 2 × 3 × 3",
                "options": ["2 × 2 × 2 × 3 × 3", "2 × 36", "8 × 9", "6 × 12"],
                "factors": [2, 2, 2, 3, 3]
            },
            {
                "number": 84,
                "correct": "2 × 2 × 3 × 7",
                "options": ["2 × 2 × 3 × 7", "2 × 42", "4 × 21", "12 × 7"],
                "factors": [2, 2, 3, 7]
            },
            {
                "number": 90,
                "correct": "2 × 3 × 3 × 5",
                "options": ["2 × 3 × 3 × 5", "2 × 45", "9 × 10", "18 × 5"],
                "factors": [2, 3, 3, 5]
            },
            {
                "number": 96,
                "correct": "2 × 2 × 2 × 2 × 2 × 3",
                "options": ["2 × 2 × 2 × 2 × 2 × 3", "2 × 48", "32 × 3", "16 × 6"],
                "factors": [2, 2, 2, 2, 2, 3]
            },
            {
                "number": 105,
                "correct": "3 × 5 × 7",
                "options": ["3 × 5 × 7", "3 × 35", "5 × 21", "15 × 7"],
                "factors": [3, 5, 7]
            },
        ]
    
    # Select a random problem
    problem = random.choice(problems)
    
    st.session_state.prime_fact_data = problem
    st.session_state.prime_fact_answer = problem["correct"]
    st.session_state.current_prime_fact_problem = f"What is the prime factorisation of {problem['number']}?"

def display_prime_fact_problem():
    """Display the current prime factorisation problem interface with clickable tiles"""
    data = st.session_state.prime_fact_data
    number = data["number"]
    options = data["options"]
    
    # Initialize selected option in session state if not exists
    if "prime_fact_selected_option" not in st.session_state:
        st.session_state.prime_fact_selected_option = None
    
    # Display the question
    st.markdown(f"### 🎯 {st.session_state.current_prime_fact_problem}")
    
    # Add some spacing
    st.markdown("")
    
    # Create clickable tiles in a 2x2 grid
    row1_col1, row1_col2 = st.columns(2, gap="medium")
    row2_col1, row2_col2 = st.columns(2, gap="medium")
    columns = [row1_col1, row1_col2, row2_col1, row2_col2]
    
    # Display each option as a clickable tile
    for i, option in enumerate(options):
        with columns[i]:
            # Determine if this tile is selected
            is_selected = st.session_state.prime_fact_selected_option == option
            
            # Create button with conditional styling
            button_type = "primary" if is_selected else "secondary"
            button_text = f"✅ {option}" if is_selected else option
            
            if st.button(
                button_text,
                key=f"tile_{i}",
                use_container_width=True,
                type=button_type,
                help=f"Click to select: {option}"
            ):
                st.session_state.prime_fact_selected_option = option
                st.rerun()
    
    # Show current selection status
    st.markdown("")
    if st.session_state.prime_fact_selected_option:
        st.success(f"**Selected:** {st.session_state.prime_fact_selected_option}")
    else:
        st.info("👆 **Click on one of the options above to select your answer**")
    
    # Submit section
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.button(
            "✅ Submit Answer", 
            type="primary", 
            use_container_width=True,
            disabled=st.session_state.prime_fact_selected_option is None
        )
    
    # Handle submission
    if submit_button and st.session_state.prime_fact_selected_option:
        st.session_state.prime_fact_user_answer = st.session_state.prime_fact_selected_option
        st.session_state.prime_fact_feedback = True
        st.session_state.prime_fact_submitted = True
        st.rerun()
    
    # Show feedback and next button
    handle_prime_fact_feedback()

def handle_prime_fact_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.get("prime_fact_feedback", False):
        show_prime_fact_feedback()
    
    if st.session_state.get("prime_fact_submitted", False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_prime_fact_state()
                st.rerun()

def show_prime_fact_feedback():
    """Display feedback for the prime factorisation problem"""
    user_answer = st.session_state.get("prime_fact_user_answer")
    correct_answer = st.session_state.get("prime_fact_answer")
    data = st.session_state.get("prime_fact_data", {})
    
    if user_answer is None or correct_answer is None or not data:
        return
    
    number = data["number"]
    factors = data["factors"]
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent!** The prime factorisation of {number} is {correct_answer}.")
        
        # Increase difficulty
        old_difficulty = st.session_state.prime_fact_difficulty
        st.session_state.prime_fact_difficulty = min(
            st.session_state.prime_fact_difficulty + 1, 5
        )
        
        if st.session_state.prime_fact_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered prime factorisation!**")
        elif old_difficulty < st.session_state.prime_fact_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.prime_fact_difficulty}**")
        
        show_prime_fact_explanation(correct=True)
    
    else:
        st.error(f"❌ **Not quite.** The correct prime factorisation of {number} is **{correct_answer}**.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.prime_fact_difficulty
        st.session_state.prime_fact_difficulty = max(
            st.session_state.prime_fact_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.prime_fact_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.prime_fact_difficulty}. Keep practicing!**")
        
        show_prime_fact_explanation(correct=False)

def show_prime_fact_explanation(correct=True):
    """Show explanation for the prime factorisation problem"""
    data = st.session_state.get("prime_fact_data", {})
    correct_answer = st.session_state.get("prime_fact_answer")
    user_answer = st.session_state.get("prime_fact_user_answer")
    
    if not data or correct_answer is None:
        return
        
    number = data["number"]
    factors = data["factors"]
    options = data["options"]
    
    color = "#e8f5e8" if correct else "#ffe8e8"
    border_color = "#4CAF50" if correct else "#f44336"
    title_color = "#2e7d2e" if correct else "#c62828"
    
    with st.expander("📖 **Click here for step-by-step explanation**", expanded=not correct):
        st.markdown(f"""
        <div style="
            background-color: {color}; 
            border-left: 4px solid {border_color}; 
            padding: 15px; 
            border-radius: 5px;
        ">
            <h4 style="color: {title_color}; margin-top: 0;">💡 Prime Factorisation Breakdown:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        ### Number: {number}
        
        ### Step-by-step factorisation:
        """)
        
        # Show the factor tree process
        current = number
        steps = []
        remaining_factors = factors.copy()
        
        while len(remaining_factors) > 0:
            prime = remaining_factors[0]
            quotient = current // prime
            steps.append(f"**{current} ÷ {prime} = {quotient}**")
            current = quotient
            remaining_factors.remove(prime)
        
        for step in steps:
            st.markdown(f"- {step}")
        
        st.markdown(f"""
        ### Prime factorisation: {correct_answer}
        
        ### Verification:
        **Check:** {' × '.join(map(str, factors))} = {number} ✅
        
        ### Why each option is right or wrong:
        """)
        
        # Analyze each option
        for option in options:
            if option == correct_answer:
                st.markdown(f"- **{option}** ✅ **CORRECT** - All factors are prime")
            else:
                # Analyze why this option is wrong
                if '×' not in option:
                    # Single number
                    if option == str(number):
                        st.markdown(f"- **{option}** ❌ This is the original number, not its prime factors")
                    else:
                        st.markdown(f"- **{option}** ❌ This is just one factor, not the complete factorisation")
                else:
                    # Check if contains non-prime factors
                    option_parts = [int(x.strip()) for x in option.split('×')]
                    non_primes = []
                    for part in option_parts:
                        if part > 1 and not is_prime(part):
                            non_primes.append(str(part))
                    
                    if non_primes:
                        st.markdown(f"- **{option}** ❌ Contains composite numbers: {', '.join(non_primes)}")
                    else:
                        # Check if it equals the original number
                        product = 1
                        for part in option_parts:
                            product *= part
                        if product != number:
                            st.markdown(f"- **{option}** ❌ This equals {product}, not {number}")
                        else:
                            st.markdown(f"- **{option}** ❌ Check the prime factors again")
        
        st.markdown(f"""
        ### Remember:
        - **Prime factorisation** uses only prime numbers
        - **All prime factors** must multiply to give the original number
        - **No composite numbers** allowed in the factorisation
        """)

def is_prime(n):
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def reset_prime_fact_state():
    """Reset the state for next problem"""
    st.session_state.current_prime_fact_problem = None
    st.session_state.prime_fact_answer = None
    st.session_state.prime_fact_feedback = False
    st.session_state.prime_fact_submitted = False
    st.session_state.prime_fact_data = {}
    st.session_state.prime_fact_selected_option = None  # Reset selection
    
    if "prime_fact_user_answer" in st.session_state:
        del st.session_state.prime_fact_user_answer