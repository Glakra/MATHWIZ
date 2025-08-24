import streamlit as st
import random
import math

def run():
    """
    Main function to run the Highest Common Factor activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Number theory/highest_common_factor.py
    """
    # Initialize session state
    if "hcf_difficulty" not in st.session_state:
        st.session_state.hcf_difficulty = 1
    
    if "current_hcf_problem" not in st.session_state:
        st.session_state.current_hcf_problem = None
        st.session_state.hcf_answer = None
        st.session_state.hcf_feedback = False
        st.session_state.hcf_submitted = False
        st.session_state.hcf_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Number theory**")
    st.title("🔗 Highest Common Factor")
    st.markdown("*Find the largest number that divides both numbers exactly*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.hcf_difficulty
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
    if st.session_state.current_hcf_problem is None:
        generate_hcf_problem()
    
    # Display current question
    display_hcf_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **How to Find Highest Common Factor (HCF)**", expanded=False):
        st.markdown("""
        ### What is Highest Common Factor?
        
        The **Highest Common Factor (HCF)** is the **largest number** that divides two or more numbers **exactly** (with no remainder).
        
        *Also known as Greatest Common Divisor (GCD)*
        
        ### Method 1: Listing Factors
        
        **Example: Find HCF of 12 and 18**
        
        **Step 1:** List all factors of each number
        - **Factors of 12:** 1, 2, 3, 4, 6, 12
        - **Factors of 18:** 1, 2, 3, 6, 9, 18
        
        **Step 2:** Find common factors
        - **Common factors:** 1, 2, 3, 6
        
        **Step 3:** Choose the highest
        - **HCF = 6**
        
        ### Method 2: Prime Factorization
        
        **Example: Find HCF of 24 and 36**
        
        **Step 1:** Break into prime factors
        - **24 = 2³ × 3¹**
        - **36 = 2² × 3²**
        
        **Step 2:** Take lowest power of common primes
        - **Common primes:** 2 and 3
        - **2:** min(3,2) = 2 → 2²
        - **3:** min(1,2) = 1 → 3¹
        
        **Step 3:** Multiply
        - **HCF = 2² × 3¹ = 4 × 3 = 12**
        
        ### Method 3: Euclidean Algorithm (Advanced)
        
        **Example: Find HCF of 48 and 18**
        
        ```
        48 = 18 × 2 + 12
        18 = 12 × 1 + 6  
        12 = 6 × 2 + 0
        ```
        **HCF = 6** (last non-zero remainder)
        
        ### Quick Tips:
        
        #### **Special Cases:**
        - **HCF of any number and 1 = 1**
        - **HCF of a number and itself = the number**
        - **If one number divides another, HCF = smaller number**
        
        #### **Shortcuts:**
        - **Even numbers:** Always have HCF ≥ 2
        - **Both odd:** HCF is odd
        - **One even, one odd:** HCF is odd
        - **Consecutive numbers:** HCF = 1
        
        ### Common Examples:
        - **HCF(4, 10) = 2** (both even, both divisible by 2)
        - **HCF(6, 9) = 3** (both divisible by 3)
        - **HCF(8, 12) = 4** (both divisible by 4)
        - **HCF(15, 25) = 5** (both divisible by 5)
        - **HCF(7, 11) = 1** (both prime, no common factors)
        
        ### Step-by-Step Strategy:
        1. **Start with smaller number**
        2. **Check if it divides the larger number**
        3. **If yes, that's your HCF**
        4. **If no, try factors of the smaller number**
        5. **Work downward until you find a common factor**
        """)

def generate_hcf_problem():
    """Generate an unlimited HCF problem based on difficulty level using algorithmic generation"""
    difficulty = st.session_state.hcf_difficulty
    
    # Generate problems algorithmically based on difficulty
    if difficulty == 1:
        # Level 1: Small HCF (2-5), simple multiples (2-8)
        hcf = random.choice([2, 3, 4, 5])
        multiplier1 = random.randint(2, 6)
        multiplier2 = random.randint(2, 8)
        # Ensure different multipliers for variety
        while multiplier2 == multiplier1:
            multiplier2 = random.randint(2, 8)
        
        num1 = hcf * multiplier1
        num2 = hcf * multiplier2
        numbers = sorted([num1, num2])
    
    elif difficulty == 2:
        # Level 2: Medium HCF (3-12), moderate multiples (2-10)
        hcf = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        multiplier1 = random.randint(2, 8)
        multiplier2 = random.randint(2, 10)
        while multiplier2 == multiplier1:
            multiplier2 = random.randint(2, 10)
        
        num1 = hcf * multiplier1
        num2 = hcf * multiplier2
        numbers = sorted([num1, num2])
    
    elif difficulty == 3:
        # Level 3: Larger HCF (6-25), bigger multiples (3-12)
        hcf = random.choice([6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 25])
        multiplier1 = random.randint(3, 10)
        multiplier2 = random.randint(3, 12)
        while multiplier2 == multiplier1:
            multiplier2 = random.randint(3, 12)
        
        num1 = hcf * multiplier1
        num2 = hcf * multiplier2
        numbers = sorted([num1, num2])
    
    elif difficulty == 4:
        # Level 4: Include 3-number problems or challenging 2-number problems
        if random.choice([True, False]):  # 50% chance of 3 numbers
            hcf = random.choice([4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 20])
            multiplier1 = random.randint(2, 8)
            multiplier2 = random.randint(2, 8)
            multiplier3 = random.randint(2, 8)
            # Ensure all different
            while multiplier2 == multiplier1:
                multiplier2 = random.randint(2, 8)
            while multiplier3 == multiplier1 or multiplier3 == multiplier2:
                multiplier3 = random.randint(2, 8)
            
            num1 = hcf * multiplier1
            num2 = hcf * multiplier2
            num3 = hcf * multiplier3
            numbers = sorted([num1, num2, num3])
        else:
            # Challenging 2-number problems
            hcf = random.choice([12, 14, 15, 16, 18, 20, 21, 24, 28, 30, 35, 36])
            multiplier1 = random.randint(3, 10)
            multiplier2 = random.randint(3, 12)
            while multiplier2 == multiplier1:
                multiplier2 = random.randint(3, 12)
            
            num1 = hcf * multiplier1
            num2 = hcf * multiplier2
            numbers = sorted([num1, num2])
    
    else:  # difficulty == 5
        # Level 5: Very challenging numbers
        if random.choice([True, False]):  # 50% chance of 3 numbers
            hcf = random.choice([12, 15, 18, 20, 24, 30, 36, 40, 45])
            multiplier1 = random.randint(2, 8)
            multiplier2 = random.randint(2, 8)
            multiplier3 = random.randint(2, 8)
            while multiplier2 == multiplier1:
                multiplier2 = random.randint(2, 8)
            while multiplier3 == multiplier1 or multiplier3 == multiplier2:
                multiplier3 = random.randint(2, 8)
            
            num1 = hcf * multiplier1
            num2 = hcf * multiplier2
            num3 = hcf * multiplier3
            numbers = sorted([num1, num2, num3])
        else:
            # Large 2-number problems
            hcf = random.choice([24, 28, 30, 32, 36, 40, 42, 45, 48, 54, 60, 72])
            multiplier1 = random.randint(3, 12)
            multiplier2 = random.randint(3, 15)
            while multiplier2 == multiplier1:
                multiplier2 = random.randint(3, 15)
            
            num1 = hcf * multiplier1
            num2 = hcf * multiplier2
            numbers = sorted([num1, num2])
    
    # Create the problem data
    problem = {"numbers": numbers, "hcf": hcf}
    
    st.session_state.hcf_data = problem
    st.session_state.hcf_answer = problem["hcf"]
    
    # Create question text
    if len(problem["numbers"]) == 2:
        st.session_state.current_hcf_problem = f"What is the highest common factor of {problem['numbers'][0]} and {problem['numbers'][1]}?"
    else:
        numbers_text = ", ".join(map(str, problem["numbers"][:-1])) + f" and {problem['numbers'][-1]}"
        st.session_state.current_hcf_problem = f"What is the highest common factor of {numbers_text}?"

def display_hcf_problem():
    """Display the current HCF problem with text input"""
    data = st.session_state.hcf_data
    numbers = data["numbers"]
    
    # Display the question with clear formatting
    st.markdown("### 🎯 Question:")
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #4CAF50;
        font-size: 18px;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        color: #2c3e50;
    ">
        {st.session_state.current_hcf_problem}
    </div>
    """, unsafe_allow_html=True)
    
    # Create input field with form
    with st.form("hcf_form", clear_on_submit=False):
        # Center the input field
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Text input for answer
            user_input = st.text_input(
                "Enter your answer:",
                key="hcf_input",
                placeholder="Type a number...",
                label_visibility="collapsed",
                help="Enter the highest common factor as a number"
            )
            
            # Add some spacing
            st.markdown("")
            
            # Submit button
            submit_button = st.form_submit_button(
                "✅ Submit", 
                type="primary", 
                use_container_width=True
            )
        
        # Handle form submission
        if submit_button:
            if user_input.strip():
                try:
                    user_answer = int(user_input.strip())
                    st.session_state.hcf_user_answer = user_answer
                    st.session_state.hcf_feedback = True
                    st.session_state.hcf_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("Please enter a valid number!")
            else:
                st.error("Please enter an answer!")
    
    # Show feedback and next button
    handle_hcf_feedback()

def handle_hcf_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.get("hcf_feedback", False):
        show_hcf_feedback()
    
    if st.session_state.get("hcf_submitted", False):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_hcf_state()
                st.rerun()

def show_hcf_feedback():
    """Display feedback for the HCF problem"""
    user_answer = st.session_state.get("hcf_user_answer")
    correct_answer = st.session_state.get("hcf_answer")
    data = st.session_state.get("hcf_data", {})
    
    if user_answer is None or correct_answer is None or not data:
        return
    
    numbers = data["numbers"]
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent!** The highest common factor is {correct_answer}.")
        
        # Increase difficulty
        old_difficulty = st.session_state.hcf_difficulty
        st.session_state.hcf_difficulty = min(
            st.session_state.hcf_difficulty + 1, 5
        )
        
        if st.session_state.hcf_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered highest common factor!**")
        elif old_difficulty < st.session_state.hcf_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.hcf_difficulty}**")
        
        show_hcf_explanation(correct=True)
    
    else:
        st.error(f"❌ **Not quite.** The correct highest common factor is **{correct_answer}**.")
        
        # Provide hints based on common mistakes
        if user_answer > correct_answer:
            st.warning("💡 **Hint:** Your answer is too high. The HCF cannot be larger than the smallest number.")
        elif user_answer < correct_answer:
            st.warning("💡 **Hint:** Your answer is too low. Try checking if there are larger common factors.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.hcf_difficulty
        st.session_state.hcf_difficulty = max(
            st.session_state.hcf_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.hcf_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.hcf_difficulty}. Keep practicing!**")
        
        show_hcf_explanation(correct=False)

def show_hcf_explanation(correct=True):
    """Show explanation for the HCF problem"""
    data = st.session_state.get("hcf_data", {})
    correct_answer = st.session_state.get("hcf_answer")
    user_answer = st.session_state.get("hcf_user_answer")
    
    if not data or correct_answer is None:
        return
        
    numbers = data["numbers"]
    
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
            <h4 style="color: {title_color}; margin-top: 0;">💡 HCF Solution:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if len(numbers) == 2:
            st.markdown(f"""
            ### Numbers: {numbers[0]} and {numbers[1]}
            ### HCF = {correct_answer}
            """)
        else:
            numbers_text = ", ".join(map(str, numbers[:-1])) + f" and {numbers[-1]}"
            st.markdown(f"""
            ### Numbers: {numbers_text}
            ### HCF = {correct_answer}
            """)
        
        # Method 1: Listing factors
        st.markdown("### 📋 Method 1: Listing Factors")
        
        all_factors = {}
        for num in numbers:
            factors = get_factors(num)
            all_factors[num] = factors
            st.markdown(f"- **Factors of {num}:** {', '.join(map(str, sorted(factors)))}")
        
        # Find common factors
        common_factors = set(all_factors[numbers[0]])
        for num in numbers[1:]:
            common_factors = common_factors.intersection(all_factors[num])
        
        common_factors_list = sorted(list(common_factors), reverse=True)
        st.markdown(f"- **Common factors:** {', '.join(map(str, common_factors_list))}")
        st.markdown(f"- **Highest common factor:** **{max(common_factors_list)}** ✅")
        
        # Method 2: Prime factorization (for 2 numbers)
        if len(numbers) == 2:
            st.markdown("### 🧮 Method 2: Prime Factorization")
            
            factorizations = {}
            for num in numbers:
                factors = prime_factorization(num)
                factorizations[num] = factors
                factors_str = " × ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()])
                st.markdown(f"- **{num} =** {factors_str}")
            
            # Find HCF using prime factorization
            all_primes = set()
            for factors in factorizations.values():
                all_primes.update(factors.keys())
            
            hcf_factors = {}
            for prime in all_primes:
                min_power = min(factorizations[num].get(prime, 0) for num in numbers)
                if min_power > 0:
                    hcf_factors[prime] = min_power
            
            if hcf_factors:
                hcf_str = " × ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in hcf_factors.items()])
                st.markdown(f"- **HCF =** {hcf_str} = **{correct_answer}** ✅")
            else:
                st.markdown(f"- **HCF =** **1** (no common prime factors)")
        
        # Verification
        st.markdown("### ✅ Verification:")
        for num in numbers:
            quotient = num // correct_answer
            st.markdown(f"- **{num} ÷ {correct_answer} = {quotient}** (exactly, no remainder)")
        
        # Check if user's answer divides the numbers
        if user_answer != correct_answer and user_answer is not None:
            st.markdown(f"### ❌ Why {user_answer} is not correct:")
            can_divide_all = True
            for num in numbers:
                if num % user_answer == 0:
                    quotient = num // user_answer
                    st.markdown(f"- **{num} ÷ {user_answer} = {quotient}** ✅ (divides exactly)")
                else:
                    quotient = num // user_answer
                    remainder = num % user_answer
                    st.markdown(f"- **{num} ÷ {user_answer} = {quotient} remainder {remainder}** ❌ (doesn't divide exactly)")
                    can_divide_all = False
            
            if can_divide_all and user_answer < correct_answer:
                st.markdown(f"- **{user_answer} does divide all numbers, but {correct_answer} is larger and also divides all numbers**")

def get_factors(n):
    """Get all factors of a number"""
    factors = set()
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
    return factors

def prime_factorization(n):
    """Get prime factorization as a dictionary {prime: power}"""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            if d not in factors:
                factors[d] = 0
            factors[d] += 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = 1
    return factors

def reset_hcf_state():
    """Reset the state for next problem"""
    st.session_state.current_hcf_problem = None
    st.session_state.hcf_answer = None
    st.session_state.hcf_feedback = False
    st.session_state.hcf_submitted = False
    st.session_state.hcf_data = {}
    
    if "hcf_user_answer" in st.session_state:
        del st.session_state.hcf_user_answer