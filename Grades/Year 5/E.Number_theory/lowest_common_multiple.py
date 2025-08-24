import streamlit as st
import random
import math

def run():
    """
    Main function to run the Lowest Common Multiple activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Number theory/lowest_common_multiple.py
    """
    # Initialize session state
    if "lcm_difficulty" not in st.session_state:
        st.session_state.lcm_difficulty = 1
    
    if "current_lcm_problem" not in st.session_state:
        st.session_state.current_lcm_problem = None
        st.session_state.lcm_answer = None
        st.session_state.lcm_feedback = False
        st.session_state.lcm_submitted = False
        st.session_state.lcm_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Number theory**")
    st.title("🔗 Lowest Common Multiple")
    st.markdown("*Find the smallest number that both numbers divide into exactly*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.lcm_difficulty
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
    if st.session_state.current_lcm_problem is None:
        generate_lcm_problem()
    
    # Display current question
    display_lcm_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **How to Find Lowest Common Multiple (LCM)**", expanded=False):
        st.markdown("""
        ### What is Lowest Common Multiple?
        
        The **Lowest Common Multiple (LCM)** is the **smallest number** that two or more numbers can both divide into **exactly** (with no remainder).
        
        *Also known as Least Common Multiple*
        
        ### Method 1: Listing Multiples
        
        **Example: Find LCM of 6 and 8**
        
        **Step 1:** List multiples of each number
        - **Multiples of 6:** 6, 12, 18, **24**, 30, 36, 42, **48**, 54...
        - **Multiples of 8:** 8, 16, **24**, 32, 40, **48**, 56...
        
        **Step 2:** Find common multiples
        - **Common multiples:** 24, 48, 72...
        
        **Step 3:** Choose the smallest
        - **LCM = 24**
        
        ### Method 2: Prime Factorization
        
        **Example: Find LCM of 12 and 18**
        
        **Step 1:** Break into prime factors
        - **12 = 2² × 3¹**
        - **18 = 2¹ × 3²**
        
        **Step 2:** Take highest power of each prime
        - **2:** max(2,1) = 2 → 2²
        - **3:** max(1,2) = 2 → 3²
        
        **Step 3:** Multiply
        - **LCM = 2² × 3² = 4 × 9 = 36**
        
        ### Method 3: Using HCF Formula
        
        **For two numbers:** LCM(a,b) = (a × b) ÷ HCF(a,b)
        
        **Example: Find LCM of 15 and 20**
        - **HCF(15, 20) = 5**
        - **LCM = (15 × 20) ÷ 5 = 300 ÷ 5 = 60**
        
        ### Quick Tips:
        
        #### **Special Cases:**
        - **LCM of any number and 1 = the number**
        - **LCM of a number and itself = the number**
        - **If one number divides another, LCM = larger number**
        - **For coprime numbers (HCF=1), LCM = their product**
        
        #### **Shortcuts:**
        - **For consecutive numbers:** Usually LCM = their product
        - **For numbers ending in 0:** Often involves powers of 2, 5, 10
        - **Even + Odd:** LCM is always even
        
        ### Common Examples:
        - **LCM(4, 6) = 12** (both divide 12 exactly)
        - **LCM(5, 7) = 35** (coprime → multiply)
        - **LCM(9, 12) = 36** (9×4=36, 12×3=36)
        - **LCM(10, 15) = 30** (both divide 30)
        - **LCM(8, 12) = 24** (common factors reduce LCM)
        
        ### Step-by-Step Strategy:
        1. **Check if one divides the other** → If yes, LCM = larger number
        2. **Look for simple relationships** (multiples, factors)
        3. **Use listing method** for small numbers
        4. **Use prime factorization** for larger numbers
        5. **Verify by division** (both numbers should divide LCM exactly)
        
        ### Real-World Applications:
        - **Bus schedules:** When do buses arrive together?
        - **Gear systems:** When do gears align again?
        - **Patterns:** When do repeating patterns synchronize?
        - **Packaging:** Common package sizes for different items
        """)

def generate_lcm_problem():
    """Generate unlimited LCM problems using algorithmic generation"""
    difficulty = st.session_state.lcm_difficulty
    
    if difficulty == 1:
        # Level 1: Simple cases - small numbers, many coprime pairs
        problem_type = random.choice(['coprime', 'simple_multiple', 'small_common'])
        
        if problem_type == 'coprime':
            # Coprime numbers (LCM = product)
            pairs = [(2,3), (3,4), (4,5), (5,6), (3,5), (4,7), (5,7), (6,7), (7,8), (8,9)]
            num1, num2 = random.choice(pairs)
            lcm = num1 * num2
        elif problem_type == 'simple_multiple':
            # One number is multiple of another
            base = random.randint(2, 8)
            multiplier = random.randint(2, 4)
            num1 = base
            num2 = base * multiplier
            lcm = num2
        else:  # small_common
            # Small numbers with manageable LCM
            pairs = [(4,6), (6,8), (6,9), (8,10), (9,12), (10,12)]
            num1, num2 = random.choice(pairs)
            lcm = math.lcm(num1, num2)
        
        numbers = sorted([num1, num2])
    
    elif difficulty == 2:
        # Level 2: Medium numbers, mix of relationships
        problem_type = random.choice(['medium_coprime', 'medium_common', 'medium_multiple'])
        
        if problem_type == 'medium_coprime':
            # Medium coprime pairs
            primes = [7, 11, 13]
            composites = [8, 9, 10, 12, 14, 15, 16]
            num1 = random.choice(primes)
            num2 = random.choice([x for x in composites if math.gcd(num1, x) == 1])
            lcm = num1 * num2
        elif problem_type == 'medium_multiple':
            # Larger multiple relationships
            base = random.randint(6, 12)
            multiplier = random.randint(2, 5)
            num1 = base
            num2 = base * multiplier
            lcm = num2
        else:  # medium_common
            # Numbers with common factors
            pairs = [(12,15), (12,16), (12,18), (15,18), (15,20), (16,20), (18,20)]
            num1, num2 = random.choice(pairs)
            lcm = math.lcm(num1, num2)
        
        numbers = sorted([num1, num2])
    
    elif difficulty == 3:
        # Level 3: Larger numbers, more complex relationships
        problem_type = random.choice(['large_pairs', 'three_numbers', 'challenging_pairs'])
        
        if problem_type == 'three_numbers':
            # Three small numbers
            base_sets = [(2,3,4), (3,4,5), (4,5,6), (2,3,5), (3,5,7), (4,6,8)]
            numbers = list(random.choice(base_sets))
            lcm = math.lcm(*numbers)
        elif problem_type == 'challenging_pairs':
            # Larger two-number problems
            pairs = [(18,24), (20,24), (21,28), (24,30), (20,30), (24,36)]
            num1, num2 = random.choice(pairs)
            numbers = sorted([num1, num2])
            lcm = math.lcm(num1, num2)
        else:  # large_pairs
            # Generate larger numbers systematically
            base = random.randint(12, 20)
            factor1 = random.randint(2, 4)
            factor2 = random.randint(3, 5)
            num1 = base * factor1
            num2 = base * factor2
            numbers = sorted([num1, num2])
            lcm = math.lcm(num1, num2)
    
    elif difficulty == 4:
        # Level 4: Include three numbers or very challenging pairs
        problem_type = random.choice(['three_medium', 'large_pairs', 'coprime_large'])
        
        if problem_type == 'three_medium':
            # Three medium numbers
            base_sets = [(6,8,9), (6,9,12), (8,10,12), (9,12,15), (10,12,15)]
            numbers = list(random.choice(base_sets))
            lcm = math.lcm(*numbers)
        elif problem_type == 'coprime_large':
            # Large coprime numbers
            primes = [11, 13, 17, 19]
            composites = [15, 16, 18, 20, 21, 22, 24, 25]
            num1 = random.choice(primes)
            num2 = random.choice([x for x in composites if math.gcd(num1, x) == 1])
            numbers = sorted([num1, num2])
            lcm = num1 * num2
        else:  # large_pairs
            pairs = [(30,42), (36,48), (40,60), (45,60), (48,72)]
            num1, num2 = random.choice(pairs)
            numbers = sorted([num1, num2])
            lcm = math.lcm(num1, num2)
    
    else:  # difficulty == 5
        # Level 5: Very challenging problems
        problem_type = random.choice(['three_large', 'very_large_pairs', 'complex_relationships'])
        
        if problem_type == 'three_large':
            # Three larger numbers
            base_sets = [(12,15,18), (15,20,25), (18,24,30), (20,24,30)]
            numbers = list(random.choice(base_sets))
            lcm = math.lcm(*numbers)
        elif problem_type == 'complex_relationships':
            # Numbers with complex factor relationships
            pairs = [(54,72), (60,84), (72,96), (75,100), (84,108)]
            num1, num2 = random.choice(pairs)
            numbers = sorted([num1, num2])
            lcm = math.lcm(num1, num2)
        else:  # very_large_pairs
            # Generate very large systematic pairs
            base1 = random.randint(15, 25)
            base2 = random.randint(20, 30)
            # Ensure they have some common factor for interesting LCM
            common_factor = random.choice([2, 3, 4, 5])
            num1 = base1 * common_factor
            num2 = base2 * common_factor
            numbers = sorted([num1, num2])
            lcm = math.lcm(num1, num2)
    
    st.session_state.lcm_data = {"numbers": numbers, "lcm": lcm}
    st.session_state.lcm_answer = lcm
    
    # Create question text
    if len(numbers) == 2:
        st.session_state.current_lcm_problem = f"What is the lowest common multiple of {numbers[0]} and {numbers[1]}?"
    else:
        numbers_text = ", ".join(map(str, numbers[:-1])) + f" and {numbers[-1]}"
        st.session_state.current_lcm_problem = f"What is the lowest common multiple of {numbers_text}?"

def display_lcm_problem():
    """Display the current LCM problem with text input"""
    data = st.session_state.lcm_data
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
        {st.session_state.current_lcm_problem}
    </div>
    """, unsafe_allow_html=True)
    
    # Create input field with form
    with st.form("lcm_form", clear_on_submit=False):
        # Center the input field
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Text input for answer
            user_input = st.text_input(
                "Enter your answer:",
                key="lcm_input",
                placeholder="Type a number...",
                label_visibility="collapsed",
                help="Enter the lowest common multiple as a number"
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
                    st.session_state.lcm_user_answer = user_answer
                    st.session_state.lcm_feedback = True
                    st.session_state.lcm_submitted = True
                    st.rerun()
                except ValueError:
                    st.error("Please enter a valid number!")
            else:
                st.error("Please enter an answer!")
    
    # Show feedback and next button
    handle_lcm_feedback()

def handle_lcm_feedback():
    """Handle feedback display and next question button"""
    if st.session_state.get("lcm_feedback", False):
        show_lcm_feedback()
        
        # Show Next Question button immediately after feedback
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_lcm_state()
                st.rerun()

def show_lcm_feedback():
    """Display feedback for the LCM problem"""
    user_answer = st.session_state.get("lcm_user_answer")
    correct_answer = st.session_state.get("lcm_answer")
    data = st.session_state.get("lcm_data", {})
    
    if user_answer is None or correct_answer is None or not data:
        return
    
    numbers = data["numbers"]
    
    if user_answer == correct_answer:
        st.success(f"🎉 **Excellent!** The lowest common multiple is {correct_answer}.")
        
        # Increase difficulty
        old_difficulty = st.session_state.lcm_difficulty
        st.session_state.lcm_difficulty = min(
            st.session_state.lcm_difficulty + 1, 5
        )
        
        if st.session_state.lcm_difficulty == 5 and old_difficulty < 5:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered lowest common multiple!**")
        elif old_difficulty < st.session_state.lcm_difficulty:
            st.info(f"⬆️ **Level up! Now at Level {st.session_state.lcm_difficulty}**")
        
        show_lcm_explanation(correct=True)
    
    else:
        st.error(f"❌ **Not quite.** The correct lowest common multiple is **{correct_answer}**.")
        
        # Provide hints based on common mistakes
        if user_answer < correct_answer:
            # Check if it's a common multiple but not the lowest
            all_divide = all(user_answer % num == 0 for num in numbers)
            if all_divide:
                st.warning("💡 **Hint:** Your answer is a common multiple, but not the *lowest* one. Try finding a smaller multiple.")
            else:
                # Check which numbers don't divide the answer
                non_dividing = [num for num in numbers if user_answer % num != 0]
                if non_dividing:
                    st.warning(f"💡 **Hint:** {', '.join(map(str, non_dividing))} doesn't divide {user_answer} exactly.")
        elif user_answer > correct_answer:
            st.warning("💡 **Hint:** Your answer is too high. The LCM is the *smallest* common multiple.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.lcm_difficulty
        st.session_state.lcm_difficulty = max(
            st.session_state.lcm_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.lcm_difficulty:
            st.warning(f"⬇️ **Back to Level {st.session_state.lcm_difficulty}. Keep practicing!**")
        
        show_lcm_explanation(correct=False)

def show_lcm_explanation(correct=True):
    """Show explanation for the LCM problem"""
    data = st.session_state.get("lcm_data", {})
    correct_answer = st.session_state.get("lcm_answer")
    user_answer = st.session_state.get("lcm_user_answer")
    
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
            <h4 style="color: {title_color}; margin-top: 0;">💡 LCM Solution:</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if len(numbers) == 2:
            st.markdown(f"""
            ### Numbers: {numbers[0]} and {numbers[1]}
            ### LCM = {correct_answer}
            """)
        else:
            numbers_text = ", ".join(map(str, numbers[:-1])) + f" and {numbers[-1]}"
            st.markdown(f"""
            ### Numbers: {numbers_text}
            ### LCM = {correct_answer}
            """)
        
        # Method 1: Listing multiples (for 2 numbers)
        if len(numbers) == 2:
            st.markdown("### 📋 Method 1: Listing Multiples")
            
            num1, num2 = numbers
            
            # Generate multiples up to LCM + a bit more
            max_multiple = correct_answer + min(num1, num2)
            multiples1 = [num1 * i for i in range(1, (max_multiple // num1) + 2)]
            multiples2 = [num2 * i for i in range(1, (max_multiple // num2) + 2)]
            
            # Show first several multiples, highlighting common ones
            mult1_display = []
            for m in multiples1[:10]:  # Show first 10
                if m in multiples2:
                    mult1_display.append(f"**{m}**")  # Bold for common multiples
                else:
                    mult1_display.append(str(m))
            st.markdown(f"**Multiples of {num1}:** {', '.join(mult1_display)}")
            
            mult2_display = []
            for m in multiples2[:10]:
                if m in multiples1:
                    mult2_display.append(f"**{m}**")  # Bold for common multiples
                else:
                    mult2_display.append(str(m))
            st.markdown(f"**Multiples of {num2}:** {', '.join(mult2_display)}")
            
            # Find common multiples
            common_multiples = sorted(list(set(multiples1) & set(multiples2)))[:5]
            st.markdown(f"**Common multiples:** {', '.join(map(str, common_multiples))}...")
            st.markdown(f"**Lowest common multiple:** **{min(common_multiples)}** ✅")
        
        # Method 2: Prime factorization
        st.markdown("### 🧮 Method 2: Prime Factorization")
        
        factorizations = {}
        for num in numbers:
            factors = prime_factorization(num)
            factorizations[num] = factors
            factors_str = " × ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items()])
            st.markdown(f"- **{num} =** {factors_str}")
        
        # Find LCM using prime factorization
        all_primes = set()
        for factors in factorizations.values():
            all_primes.update(factors.keys())
        
        lcm_factors = {}
        for prime in all_primes:
            max_power = max(factorizations[num].get(prime, 0) for num in numbers)
            if max_power > 0:
                lcm_factors[prime] = max_power
        
        if lcm_factors:
            lcm_str = " × ".join([f"{p}^{e}" if e > 1 else str(p) for p, e in lcm_factors.items()])
            st.markdown(f"**Take highest power of each prime:**")
            for prime in sorted(lcm_factors.keys()):
                powers = [factorizations[num].get(prime, 0) for num in numbers]
                st.markdown(f"- **{prime}:** max({', '.join(map(str, powers))}) = {lcm_factors[prime]} → {prime}^{lcm_factors[prime]}")
            st.markdown(f"**LCM =** {lcm_str} = **{correct_answer}** ✅")
        
        # Method 3: Using HCF formula (for 2 numbers)
        if len(numbers) == 2:
            st.markdown("### ⚡ Method 3: Using HCF Formula")
            num1, num2 = numbers
            hcf = math.gcd(num1, num2)
            product = num1 * num2
            st.markdown(f"**Formula:** LCM(a,b) = (a × b) ÷ HCF(a,b)")
            st.markdown(f"**HCF({num1}, {num2}) = {hcf}**")
            st.markdown(f"**LCM = ({num1} × {num2}) ÷ {hcf} = {product} ÷ {hcf} = {correct_answer}** ✅")
        
        # Verification
        st.markdown("### ✅ Verification:")
        for num in numbers:
            quotient = correct_answer // num
            st.markdown(f"- **{correct_answer} ÷ {num} = {quotient}** (exactly, no remainder)")
        st.markdown(f"- **{correct_answer} is the smallest number that all given numbers divide into exactly** ✅")
        
        # Check user's answer if incorrect
        if user_answer != correct_answer and user_answer is not None:
            st.markdown(f"### ❌ Why {user_answer} is not correct:")
            can_divide_all = True
            for num in numbers:
                if user_answer % num == 0:
                    quotient = user_answer // num
                    st.markdown(f"- **{user_answer} ÷ {num} = {quotient}** ✅ (divides exactly)")
                else:
                    quotient = user_answer // num
                    remainder = user_answer % num
                    st.markdown(f"- **{user_answer} ÷ {num} = {quotient} remainder {remainder}** ❌ (doesn't divide exactly)")
                    can_divide_all = False
            
            if can_divide_all and user_answer > correct_answer:
                st.markdown(f"- **{user_answer} is a common multiple, but {correct_answer} is smaller and also works**")
            elif not can_divide_all:
                st.markdown(f"- **{user_answer} is not a common multiple because some numbers don't divide it exactly**")

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

def reset_lcm_state():
    """Reset the state for next problem"""
    st.session_state.current_lcm_problem = None
    st.session_state.lcm_answer = None
    st.session_state.lcm_feedback = False
    st.session_state.lcm_submitted = False
    st.session_state.lcm_data = {}
    
    if "lcm_user_answer" in st.session_state:
        del st.session_state.lcm_user_answer