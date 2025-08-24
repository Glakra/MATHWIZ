import streamlit as st
import random

def run():
    """
    Main function to run the Prime and Composite Numbers activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Number theory/prime_and_composite_numbers.py
    """
    # Initialize session state
    if "prime_composite_difficulty" not in st.session_state:
        st.session_state.prime_composite_difficulty = 1
    
    if "current_prime_problem" not in st.session_state:
        st.session_state.current_prime_problem = None
        st.session_state.prime_answer = None
        st.session_state.prime_feedback = False
        st.session_state.prime_submitted = False
        st.session_state.prime_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Number theory**")
    st.title("🔢 Prime and Composite Numbers")
    st.markdown("*Identify whether numbers are prime or composite*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.prime_composite_difficulty
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
    if st.session_state.current_prime_problem is None:
        generate_prime_problem()
    
    # Display current question
    display_prime_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### What are Prime and Composite Numbers?
        
        **Prime Number:**
        - Has **exactly 2 factors**: 1 and itself
        - Cannot be divided evenly by any other numbers
        - Examples: 2, 3, 5, 7, 11, 13, 17, 19, 23...
        
        **Composite Number:**
        - Has **more than 2 factors**
        - Can be divided evenly by numbers other than 1 and itself
        - Examples: 4, 6, 8, 9, 10, 12, 14, 15, 16...
        
        ### Special Cases:
        - **1 is neither** prime nor composite (it only has 1 factor)
        - **2 is the only even prime number** (all other even numbers are composite)
        
        ### How to Check:
        
        **Example 1: Is 16 prime or composite?**
        - Find factors of 16: 1, 2, 4, 8, 16
        - 16 has more than 2 factors → **Composite**
        
        **Example 2: Is 17 prime or composite?**
        - Find factors of 17: 1, 17
        - 17 has exactly 2 factors → **Prime**
        
        ### Quick Checks:
        - **Even numbers** (except 2) are always composite
        - **Numbers ending in 5** (except 5) are always composite
        - **Try dividing** by small primes: 2, 3, 5, 7, 11...
        
        ### Strategy:
        1. **List the factors** of the number
        2. **Count the factors**
        3. **2 factors = Prime, More than 2 = Composite**
        
        ### Difficulty Levels:
        - **🟡 Level 1-2:** Small numbers (2-30)
        - **🟠 Level 3:** Medium numbers (30-60)
        - **🔴 Level 4-5:** Larger numbers (60-100)
        """)

def generate_prime_problem():
    """Generate a prime/composite problem based on difficulty level"""
    difficulty = st.session_state.prime_composite_difficulty
    
    # Define problems by difficulty level
    if difficulty == 1:
        # Level 1: Simple numbers, mix of obvious primes and composites
        numbers = [
            {"number": 16, "type": "composite", "factors": [1, 2, 4, 8, 16]},  # From your image
            {"number": 2, "type": "prime", "factors": [1, 2]},               # Smallest prime
            {"number": 4, "type": "composite", "factors": [1, 2, 4]},        # Small composite
            {"number": 3, "type": "prime", "factors": [1, 3]},               # Small prime
            {"number": 6, "type": "composite", "factors": [1, 2, 3, 6]},     # Small composite
            {"number": 5, "type": "prime", "factors": [1, 5]},               # Small prime
            {"number": 8, "type": "composite", "factors": [1, 2, 4, 8]},     # Power of 2
            {"number": 7, "type": "prime", "factors": [1, 7]},               # Small prime
            {"number": 9, "type": "composite", "factors": [1, 3, 9]},        # Perfect square
            {"number": 11, "type": "prime", "factors": [1, 11]},             # Two-digit prime
        ]
    elif difficulty == 2:
        # Level 2: Numbers 12-30
        numbers = [
            {"number": 12, "type": "composite", "factors": [1, 2, 3, 4, 6, 12]},
            {"number": 13, "type": "prime", "factors": [1, 13]},
            {"number": 15, "type": "composite", "factors": [1, 3, 5, 15]},
            {"number": 17, "type": "prime", "factors": [1, 17]},
            {"number": 18, "type": "composite", "factors": [1, 2, 3, 6, 9, 18]},
            {"number": 19, "type": "prime", "factors": [1, 19]},
            {"number": 20, "type": "composite", "factors": [1, 2, 4, 5, 10, 20]},
            {"number": 23, "type": "prime", "factors": [1, 23]},
            {"number": 24, "type": "composite", "factors": [1, 2, 3, 4, 6, 8, 12, 24]},
            {"number": 29, "type": "prime", "factors": [1, 29]},
        ]
    elif difficulty == 3:
        # Level 3: Numbers 30-60
        numbers = [
            {"number": 31, "type": "prime", "factors": [1, 31]},
            {"number": 32, "type": "composite", "factors": [1, 2, 4, 8, 16, 32]},
            {"number": 37, "type": "prime", "factors": [1, 37]},
            {"number": 39, "type": "composite", "factors": [1, 3, 13, 39]},
            {"number": 41, "type": "prime", "factors": [1, 41]},
            {"number": 42, "type": "composite", "factors": [1, 2, 3, 6, 7, 14, 21, 42]},
            {"number": 43, "type": "prime", "factors": [1, 43]},
            {"number": 45, "type": "composite", "factors": [1, 3, 5, 9, 15, 45]},
            {"number": 47, "type": "prime", "factors": [1, 47]},
            {"number": 49, "type": "composite", "factors": [1, 7, 49]},
        ]
    elif difficulty == 4:
        # Level 4: Numbers 60-80
        numbers = [
            {"number": 61, "type": "prime", "factors": [1, 61]},
            {"number": 63, "type": "composite", "factors": [1, 3, 7, 9, 21, 63]},
            {"number": 67, "type": "prime", "factors": [1, 67]},
            {"number": 69, "type": "composite", "factors": [1, 3, 23, 69]},
            {"number": 71, "type": "prime", "factors": [1, 71]},
            {"number": 72, "type": "composite", "factors": [1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 72]},
            {"number": 73, "type": "prime", "factors": [1, 73]},
            {"number": 75, "type": "composite", "factors": [1, 3, 5, 15, 25, 75]},
            {"number": 77, "type": "composite", "factors": [1, 7, 11, 77]},
            {"number": 79, "type": "prime", "factors": [1, 79]},
        ]
    else:  # difficulty == 5
        # Level 5: Numbers 80-100
        numbers = [
            {"number": 83, "type": "prime", "factors": [1, 83]},
            {"number": 84, "type": "composite", "factors": [1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84]},
            {"number": 89, "type": "prime", "factors": [1, 89]},
            {"number": 91, "type": "composite", "factors": [1, 7, 13, 91]},
            {"number": 93, "type": "composite", "factors": [1, 3, 31, 93]},
            {"number": 95, "type": "composite", "factors": [1, 5, 19, 95]},
            {"number": 97, "type": "prime", "factors": [1, 97]},
            {"number": 98, "type": "composite", "factors": [1, 2, 7, 14, 49, 98]},
            {"number": 99, "type": "composite", "factors": [1, 3, 9, 11, 33, 99]},
            {"number": 100, "type": "composite", "factors": [1, 2, 4, 5, 10, 20, 25, 50, 100]},
        ]
    
    # Select a random problem
    problem = random.choice(numbers)
    
    st.session_state.prime_data = problem
    st.session_state.prime_answer = problem["type"]
    st.session_state.current_prime_problem = f"Is {problem['number']} a prime number or a composite number?"

def display_prime_problem():
    """Display the current prime/composite problem interface"""
    data = st.session_state.prime_data
    number = data["number"]
    
    # Display the question
    st.markdown(f"### 🎯 {st.session_state.current_prime_problem}")
    
    # Display the two options in a clean layout matching the image
    with st.form("prime_composite_form", clear_on_submit=False):
        # Create two columns for the options
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="
                background-color: #e6f3ff;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                margin: 20px 10px;
                font-size: 18px;
                font-weight: bold;
                color: #333;
            ">
                prime number
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background-color: #e6f3ff;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                margin: 20px 10px;
                font-size: 18px;
                font-weight: bold;
                color: #333;
            ">
                composite number
            </div>
            """, unsafe_allow_html=True)
        
        # Radio button selection
        selected_option = st.radio(
            "Select your answer:",
            options=["prime number", "composite number"],
            key="prime_choice",
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        # Handle form submission
        if submit_button:
            if selected_option:
                st.session_state.prime_user_answer = selected_option
                st.session_state.prime_feedback = True
                st.session_state.prime_submitted = True
            else:
                st.error("Please select an answer")
    
    # Show feedback and next button
    handle_prime_feedback()

def handle_prime_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.get("prime_feedback", False):
        show_prime_feedback()
    
    if st.session_state.get("prime_submitted", False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_prime_state()
                st.rerun()

def show_prime_feedback():
    """Display feedback for the prime/composite problem"""
    user_answer = st.session_state.get("prime_user_answer")
    correct_answer = st.session_state.get("prime_answer")
    data = st.session_state.get("prime_data", {})
    
    if user_answer is None or correct_answer is None or not data:
        return
    
    number = data["number"]
    factors = data["factors"]
    
    # Fix: Convert answers to consistent format for comparison
    user_type = "prime" if user_answer == "prime number" else "composite"
    correct_type = correct_answer  # This is already "prime" or "composite"
    
    if user_type == correct_type:
        if correct_type == "prime":
            st.success(f"🎉 **Excellent!** {number} is a prime number because it has exactly 2 factors: 1 and {number}.")
        else:
            st.success(f"🎉 **Excellent!** {number} is a composite number because it has {len(factors)} factors: {', '.join(map(str, factors))}.")
        
        # Increase difficulty
        old_difficulty = st.session_state.prime_composite_difficulty
        st.session_state.prime_composite_difficulty = min(
            st.session_state.prime_composite_difficulty + 1, 5
        )
        
        if st.session_state.prime_composite_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered prime and composite numbers!**")
        elif old_difficulty < st.session_state.prime_composite_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.prime_composite_difficulty}**")
        
        show_prime_explanation(correct=True)
    
    else:
        if correct_type == "prime":
            st.error(f"❌ **Not quite.** {number} is actually a prime number, not composite.")
        else:
            st.error(f"❌ **Not quite.** {number} is actually a composite number, not prime.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.prime_composite_difficulty
        st.session_state.prime_composite_difficulty = max(
            st.session_state.prime_composite_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.prime_composite_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.prime_composite_difficulty}. Keep practicing!**")
        
        show_prime_explanation(correct=False)

def show_prime_explanation(correct=True):
    """Show explanation for the prime/composite problem"""
    data = st.session_state.get("prime_data", {})
    correct_answer = st.session_state.get("prime_answer")
    
    if not data or correct_answer is None:
        return
        
    number = data["number"]
    factors = data["factors"]
    
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
            <h4 style="color: {title_color}; margin-top: 0;">💡 Prime vs Composite Analysis:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        ### Number: {number}
        
        ### Step 1: Find all factors of {number}
        **Factors are numbers that divide evenly into {number}:**
        """)
        
        # Show how each factor works
        factor_explanations = []
        for factor in factors:
            quotient = number // factor
            factor_explanations.append(f"- **{factor}**: {number} ÷ {factor} = {quotient}")
        
        for explanation in factor_explanations:
            st.markdown(explanation)
        
        st.markdown(f"""
        ### Step 2: Count the factors
        **{number} has {len(factors)} factors: {', '.join(map(str, factors))}**
        
        ### Step 3: Apply the rule
        """)
        
        if correct_answer == "prime":
            st.markdown(f"""
            - **Prime numbers** have exactly 2 factors
            - {number} has {len(factors)} factors ✅
            - **Therefore, {number} is PRIME**
            
            ### Remember:
            - Prime numbers can only be divided by 1 and themselves
            - No other numbers divide evenly into {number}
            """)
        else:
            st.markdown(f"""
            - **Composite numbers** have more than 2 factors
            - {number} has {len(factors)} factors (more than 2) ✅
            - **Therefore, {number} is COMPOSITE**
            
            ### Why it's composite:
            - {number} can be divided by numbers other than 1 and {number}
            - For example: {number} ÷ {factors[1]} = {number // factors[1]}
            """)
        
        # Add some context about the number type
        if number == 1:
            st.markdown("### Special note: 1 is neither prime nor composite!")
        elif number == 2:
            st.markdown("### Special note: 2 is the only even prime number!")
        elif number % 2 == 0 and number > 2:
            st.markdown("### Quick tip: All even numbers greater than 2 are composite!")
        elif str(number).endswith('5') and number > 5:
            st.markdown("### Quick tip: All numbers ending in 5 (except 5) are composite!")

def reset_prime_state():
    """Reset the state for next problem"""
    st.session_state.current_prime_problem = None
    st.session_state.prime_answer = None
    st.session_state.prime_feedback = False
    st.session_state.prime_submitted = False
    st.session_state.prime_data = {}
    
    if "prime_user_answer" in st.session_state:
        del st.session_state.prime_user_answer