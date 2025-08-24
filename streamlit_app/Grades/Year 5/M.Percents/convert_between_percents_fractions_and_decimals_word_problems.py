import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Convert between percents, fractions and decimals: word problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/M. Percent/convert_between_percents_fractions_decimals_word_problems.py
    """
    # Initialize session state
    if "word_problem_difficulty" not in st.session_state:
        st.session_state.word_problem_difficulty = 1  # Start with easy conversions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answers = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.consecutive_correct = 0
        st.session_state.consecutive_incorrect = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > M. Percent**")
    st.title("📊 Convert Between Percents, Fractions and Decimals: Word Problems")
    st.markdown("*Apply conversion skills to real-world situations*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.word_problem_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic Word Problems",
            2: "Intermediate Scenarios", 
            3: "Complex Applications"
        }
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=difficulty_names[difficulty_level])
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Easy**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Medium**")
        else:
            st.markdown("**🔴 Hard**")
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new question if needed
    if st.session_state.current_question is None:
        generate_new_word_problem()
    
    # Display current question
    display_word_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve Word Problems:
        
        **Step 1: Identify the given value**
        - Look for fractions (like 1/2, 3/4)
        - Look for percents (like 25%, 50%)
        - Look for decimals (like 0.25, 0.5)
        
        **Step 2: Determine what conversions are needed**
        - Read carefully to see if you need fraction, decimal, or percent
        - Some problems ask for two conversions
        
        **Step 3: Apply conversion rules**
        - **Fraction → Decimal:** Divide top by bottom
        - **Fraction → Percent:** Multiply by 100
        - **Decimal → Percent:** Multiply by 100
        - **Decimal → Fraction:** Write over power of 10, simplify
        - **Percent → Decimal:** Divide by 100
        - **Percent → Fraction:** Write over 100, simplify
        
        ### Common Contexts:
        - **Money & Savings:** Interest rates, discounts, savings goals
        - **School & Sports:** Test scores, team statistics, completion rates
        - **Food & Nutrition:** Ingredients, nutritional values
        - **Technology:** Battery life, download progress, storage space
        
        ### Remember:
        - Always simplify fractions to lowest terms
        - Include % symbol for percents
        - Round decimals when appropriate
        """)

def generate_new_word_problem():
    """Generate a new word problem based on difficulty"""
    difficulty = st.session_state.word_problem_difficulty
    
    # Define scenario templates
    scenarios = {
        1: [  # Easy scenarios with common values
            {
                "context": "Diego is building a model car that is {value} the size of a normal car.",
                "given_type": "fraction",
                "given_values": [(1, 20), (1, 10), (1, 5), (1, 4), (1, 2)],
                "conversions": ["decimal", "percent"]
            },
            {
                "context": "Josie opens a savings account that earns {value}% interest per year.",
                "given_type": "percent",
                "given_values": [2, 5, 10, 15, 20, 25],
                "conversions": ["fraction", "decimal"]
            },
            {
                "context": "Tim has saved {value} of the money he needs for a new computer.",
                "given_type": "fraction",
                "given_values": [(1, 5), (2, 5), (3, 5), (4, 5), (1, 4), (3, 4)],
                "conversions": ["decimal", "percent"]
            },
            {
                "context": "Maya's phone battery is at {value}% charge.",
                "given_type": "percent",
                "given_values": [25, 50, 75, 80, 90, 100],
                "conversions": ["fraction", "decimal"]
            },
            {
                "context": "In the school basketball team, {value} of the players are in Year 5.",
                "given_type": "fraction",
                "given_values": [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)],
                "conversions": ["decimal", "percent"]
            },
            {
                "context": "About {value}% of the students in Alexandra's class have brown eyes.",
                "given_type": "percent",
                "given_values": [10, 20, 30, 40, 50, 60],
                "conversions": ["fraction", "decimal"]
            }
        ],
        2: [  # Medium scenarios with more complex values
            {
                "context": "Anita has finished {value} of her homework assignments.",
                "given_type": "fraction",
                "given_values": [(1, 8), (3, 8), (5, 8), (7, 8), (1, 6), (5, 6)],
                "conversions": ["decimal", "percent"]
            },
            {
                "context": "One serving of Toasty-O's cereal has {value}% of the recommended daily amount of iron.",
                "given_type": "percent",
                "given_values": [5, 12.5, 37.5, 62.5, 87.5],
                "conversions": ["fraction", "decimal"]
            },
            {
                "context": "In the school band, {value} of the students play percussion instruments.",
                "given_type": "fraction",
                "given_values": [(1, 12), (1, 15), (1, 20), (3, 20), (7, 20)],
                "conversions": ["decimal", "percent"]
            },
            {
                "context": "Mr Fisher asked his students to name their favourite season. {value} of the students said autumn.",
                "given_type": "fraction",
                "given_values": [(3, 10), (7, 10), (9, 10), (3, 20), (11, 20)],
                "conversions": ["decimal", "percent"]
            },
            {
                "context": "The local library reports that {value}% of borrowed books are returned late.",
                "given_type": "percent",
                "given_values": [2.5, 7.5, 12.5, 17.5, 22.5],
                "conversions": ["fraction", "decimal"]
            },
            {
                "context": "During the science experiment, {value} of the solution evaporated.",
                "given_type": "fraction",
                "given_values": [(2, 15), (4, 15), (7, 30), (11, 30), (13, 30)],
                "conversions": ["decimal", "percent"]
            }
        ],
        3: [  # Hard scenarios with challenging values
            {
                "context": "Beth helped her little brother with {value} of his homework problems.",
                "given_type": "fraction",
                "given_values": [(2, 9), (4, 9), (5, 9), (7, 9), (8, 9)],
                "conversions": ["decimal", "percent"]
            },
            {
                "context": "Dr Quinn's records show that {value} of her patients are children.",
                "given_type": "fraction",
                "given_values": [(2, 7), (3, 7), (4, 7), (5, 7), (6, 7)],
                "conversions": ["decimal", "percent"]
            },
            {
                "context": "The weather station recorded {value}% humidity yesterday.",
                "given_type": "percent",
                "given_values": [33.3, 66.7, 16.7, 83.3, 41.7],
                "conversions": ["fraction", "decimal"]
            },
            {
                "context": "In a survey, {value} of respondents preferred online shopping.",
                "given_type": "fraction",
                "given_values": [(5, 12), (7, 12), (11, 24), (13, 24), (17, 36)],
                "conversions": ["decimal", "percent"]
            },
            {
                "context": "The new energy-efficient light bulbs use {value}% of the power of regular bulbs.",
                "given_type": "percent",
                "given_values": [12.8, 23.6, 37.2, 64.8, 76.4],
                "conversions": ["fraction", "decimal"]
            },
            {
                "context": "During the charity drive, {value} of the goal was reached in the first week.",
                "given_type": "fraction",
                "given_values": [(3, 11), (5, 11), (7, 11), (9, 11), (4, 13)],
                "conversions": ["decimal", "percent"]
            }
        ]
    }
    
    # Select scenario based on difficulty
    scenario = random.choice(scenarios[difficulty])
    
    # Choose a specific value
    if scenario["given_type"] == "fraction":
        numerator, denominator = random.choice(scenario["given_values"])
        given_value = f"{numerator}/{denominator}"
        fraction_value = Fraction(numerator, denominator)
        decimal_value = numerator / denominator
        percent_value = (numerator / denominator) * 100
    elif scenario["given_type"] == "percent":
        percent = random.choice(scenario["given_values"])
        given_value = f"{percent}%"
        percent_value = percent
        decimal_value = percent / 100
        fraction_value = Fraction(str(decimal_value)).limit_denominator()
    else:  # decimal
        decimal = random.choice(scenario["given_values"])
        given_value = str(decimal)
        decimal_value = decimal
        percent_value = decimal * 100
        fraction_value = Fraction(str(decimal)).limit_denominator()
    
    # Create the word problem
    problem_text = scenario["context"].format(value=given_value)
    
    # Prepare correct answers
    correct_answers = {}
    
    if "fraction" in scenario["conversions"]:
        if fraction_value.denominator == 1:
            correct_answers["fraction"] = str(fraction_value.numerator)
        else:
            correct_answers["fraction"] = f"{fraction_value.numerator}/{fraction_value.denominator}"
    
    if "decimal" in scenario["conversions"]:
        # Handle repeating decimals
        if scenario["given_type"] == "fraction" and denominator in [3, 6, 7, 9, 11, 13]:
            if denominator == 3:
                if numerator == 1:
                    correct_answers["decimal"] = "0.333... or 0.3̄"
                else:
                    correct_answers["decimal"] = "0.666... or 0.6̄"
            elif denominator == 9:
                digit = str(numerator)
                correct_answers["decimal"] = f"0.{digit}{digit}{digit}... or 0.{digit}̄"
            else:
                # For other repeating decimals, show rounded version
                correct_answers["decimal"] = f"{decimal_value:.4f}"
        else:
            correct_answers["decimal"] = f"{decimal_value:.10g}".rstrip('0').rstrip('.')
    
    if "percent" in scenario["conversions"]:
        if percent_value == int(percent_value):
            correct_answers["percent"] = str(int(percent_value))
        else:
            correct_answers["percent"] = f"{percent_value:.10g}".rstrip('0').rstrip('.')
    
    st.session_state.question_data = {
        "problem_text": problem_text,
        "given_type": scenario["given_type"],
        "given_value": given_value,
        "conversions": scenario["conversions"],
        "fraction_value": fraction_value,
        "decimal_value": decimal_value,
        "percent_value": percent_value
    }
    st.session_state.correct_answers = correct_answers
    st.session_state.current_question = problem_text

def display_word_problem():
    """Display the current word problem interface"""
    data = st.session_state.question_data
    
    # Display the word problem
    st.markdown("### 📝 Problem:")
    st.markdown(f"**{data['problem_text']}**")
    st.markdown("---")
    
    # Create input fields for each conversion
    with st.form("answer_form", clear_on_submit=False):
        user_answers = {}
        
        for conversion in data["conversions"]:
            if conversion == "fraction":
                st.markdown(f"**Write {data['given_value']} as a fraction in simplest form.**")
                user_answers["fraction"] = st.text_input(
                    "Fraction:",
                    key="fraction_input",
                    placeholder="e.g., 1/2",
                    label_visibility="collapsed"
                )
            
            elif conversion == "decimal":
                st.markdown(f"**Write {data['given_value']} as a decimal.**")
                user_answers["decimal"] = st.text_input(
                    "Decimal:",
                    key="decimal_input",
                    placeholder="e.g., 0.5",
                    label_visibility="collapsed"
                )
            
            elif conversion == "percent":
                st.markdown(f"**Write {data['given_value']} as a percent.**")
                col1, col2 = st.columns([3, 1])
                with col1:
                    user_answers["percent"] = st.text_input(
                        "Percent:",
                        key="percent_input",
                        placeholder="Enter number only",
                        label_visibility="collapsed"
                    )
                with col2:
                    st.markdown("**%**")
        
        # Submit button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button:
            # Store user answers
            st.session_state.user_answers = user_answers
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def validate_answer(user_answer, correct_answer, conversion_type):
    """Validate user answer with flexibility for different formats"""
    if not user_answer:
        return False
    
    # Clean up user answer
    user_answer = user_answer.strip().replace(" ", "")
    
    # Handle fraction answers
    if conversion_type == "fraction":
        try:
            # Try to parse as fraction
            if '/' in user_answer:
                parts = user_answer.split('/')
                if len(parts) == 2:
                    user_num = int(parts[0])
                    user_den = int(parts[1])
                    user_frac = Fraction(user_num, user_den)
                    
                    # Parse correct answer
                    if '/' in correct_answer:
                        parts = correct_answer.split('/')
                        correct_num = int(parts[0])
                        correct_den = int(parts[1])
                        correct_frac = Fraction(correct_num, correct_den)
                    else:
                        correct_frac = Fraction(int(correct_answer))
                    
                    return user_frac == correct_frac
            else:
                # Whole number
                return int(user_answer) == int(correct_answer)
        except:
            return False
    
    # Handle decimal answers
    elif conversion_type == "decimal":
        # For repeating decimals, accept multiple formats
        if "..." in correct_answer or "̄" in correct_answer:
            # Check various representations
            acceptable_answers = correct_answer.split(" or ")
            user_lower = user_answer.lower()
            
            for acceptable in acceptable_answers:
                if user_lower == acceptable.lower():
                    return True
                # Also check without special characters
                clean_user = user_lower.replace("...", "").replace("̄", "")
                clean_acceptable = acceptable.lower().replace("...", "").replace("̄", "")
                if clean_user.startswith(clean_acceptable[:5]):  # Check first 5 chars
                    return True
            
            # Also accept rounded versions for repeating decimals
            try:
                user_float = float(user_answer)
                correct_float = st.session_state.question_data["decimal_value"]
                return abs(user_float - correct_float) < 0.0001
            except:
                return False
        else:
            try:
                return float(user_answer) == float(correct_answer)
            except:
                return False
    
    # Handle percent answers
    else:  # percent
        # Remove % sign if present
        user_answer = user_answer.rstrip('%')
        correct_answer = correct_answer.rstrip('%')
        
        try:
            return float(user_answer) == float(correct_answer)
        except:
            return False

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    if st.session_state.show_feedback:
        show_feedback()
    
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
    
    # Check all answers
    all_correct = True
    results = {}
    
    for conversion_type, user_answer in user_answers.items():
        if conversion_type in correct_answers:
            is_correct = validate_answer(user_answer, correct_answers[conversion_type], conversion_type)
            results[conversion_type] = is_correct
            if not is_correct:
                all_correct = False
    
    if all_correct:
        st.success("🎉 **Excellent! All answers are correct!**")
        st.session_state.consecutive_correct += 1
        st.session_state.consecutive_incorrect = 0
        
        # Increase difficulty after 3 consecutive correct
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.word_problem_difficulty
            st.session_state.word_problem_difficulty = min(
                st.session_state.word_problem_difficulty + 1, 3
            )
            
            if st.session_state.word_problem_difficulty > old_difficulty:
                st.info(f"⬆️ **Difficulty increased! Now tackling more complex word problems.**")
                st.session_state.consecutive_correct = 0
            elif st.session_state.word_problem_difficulty == 3:
                st.balloons()
                st.info("🏆 **Outstanding! You've mastered all word problem types!**")
    
    else:
        st.error("❌ **Not quite right. Check your answers below:**")
        
        # Show individual results
        for conversion_type in st.session_state.question_data["conversions"]:
            if conversion_type in results:
                if results[conversion_type]:
                    st.success(f"✅ {conversion_type.capitalize()}: Correct!")
                else:
                    user_answer = user_answers.get(conversion_type, "No answer")
                    correct_answer = correct_answers[conversion_type]
                    if conversion_type == "percent":
                        correct_answer += "%"
                    st.error(f"❌ {conversion_type.capitalize()}: Your answer '{user_answer}' → Correct answer: **{correct_answer}**")
        
        st.session_state.consecutive_incorrect += 1
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty after 3 consecutive incorrect
        if st.session_state.consecutive_incorrect >= 3:
            old_difficulty = st.session_state.word_problem_difficulty
            st.session_state.word_problem_difficulty = max(
                st.session_state.word_problem_difficulty - 1, 1
            )
            
            if old_difficulty > st.session_state.word_problem_difficulty:
                st.warning(f"⬇️ **Difficulty decreased to help you practice. Keep going!**")
                st.session_state.consecutive_incorrect = 0
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the conversions"""
    data = st.session_state.question_data
    
    with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
        st.markdown(f"### Problem: {data['problem_text']}")
        st.markdown(f"**Given value:** {data['given_value']}")
        st.markdown("---")
        
        # Show conversions based on given type
        if data["given_type"] == "fraction":
            st.markdown("### Starting with a fraction:")
            
            if "decimal" in data["conversions"]:
                st.markdown(f"""
                **To convert {data['given_value']} to decimal:**
                - Divide numerator by denominator
                - {data['fraction_value'].numerator} ÷ {data['fraction_value'].denominator} = **{st.session_state.correct_answers['decimal']}**
                """)
            
            if "percent" in data["conversions"]:
                st.markdown(f"""
                **To convert {data['given_value']} to percent:**
                - Method 1: Convert to decimal first ({data['decimal_value']:.6g}), then multiply by 100
                - Method 2: {data['given_value']} = x/100, solve for x
                - Answer: **{st.session_state.correct_answers['percent']}%**
                """)
        
        elif data["given_type"] == "percent":
            st.markdown("### Starting with a percent:")
            
            if "fraction" in data["conversions"]:
                st.markdown(f"""
                **To convert {data['given_value']} to fraction:**
                - Write as fraction over 100: {data['percent_value']}/100
                - Simplify to lowest terms: **{st.session_state.correct_answers['fraction']}**
                """)
            
            if "decimal" in data["conversions"]:
                st.markdown(f"""
                **To convert {data['given_value']} to decimal:**
                - Divide by 100 (or move decimal 2 places left)
                - {data['percent_value']} ÷ 100 = **{st.session_state.correct_answers['decimal']}**
                """)
        
        else:  # decimal
            st.markdown("### Starting with a decimal:")
            
            if "fraction" in data["conversions"]:
                st.markdown(f"""
                **To convert {data['given_value']} to fraction:**
                - Count decimal places and write over appropriate power of 10
                - Simplify to lowest terms: **{st.session_state.correct_answers['fraction']}**
                """)
            
            if "percent" in data["conversions"]:
                st.markdown(f"""
                **To convert {data['given_value']} to percent:**
                - Multiply by 100 (or move decimal 2 places right)
                - {data['decimal_value']} × 100 = **{st.session_state.correct_answers['percent']}%**
                """)
        
        # Add context-specific tips
        st.markdown("---")
        st.markdown("### 💡 Real-World Application:")
        
        if "savings" in data["problem_text"].lower() or "money" in data["problem_text"].lower():
            st.markdown("In finance, percents are commonly used for interest rates, while decimals are used in calculations.")
        elif "students" in data["problem_text"].lower() or "class" in data["problem_text"].lower():
            st.markdown("In statistics, fractions show parts of a whole, while percents make comparisons easier.")
        elif "battery" in data["problem_text"].lower() or "computer" in data["problem_text"].lower():
            st.markdown("Technology often displays percents for user-friendly reading, but uses decimals internally.")
        elif "homework" in data["problem_text"].lower() or "assignments" in data["problem_text"].lower():
            st.markdown("Progress is often shown as fractions (3/5 done) or percents (60% complete).")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answers = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answers" in st.session_state:
        del st.session_state.user_answers