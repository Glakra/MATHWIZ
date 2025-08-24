import streamlit as st
import random
from fractions import Fraction
import re

def run():
    """
    Main function to run the Convert Decimals to Fractions and Mixed Numbers activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Decimals/convert_decimals_to_fractions_and_mixed_numbers.py
    """
    # Initialize session state
    if "decimals_to_fractions_difficulty" not in st.session_state:
        st.session_state.decimals_to_fractions_difficulty = 1  # Start with simple decimals
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = "new"  # Start with new question needed
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Decimals**")
    st.title("🔢 Convert Decimals to Fractions and Mixed Numbers")
    st.markdown("*Convert decimals like 0.32 to fractions like 32/100 or 8/25*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimals_to_fractions_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {1: "tenths", 2: "hundredths", 3: "thousandths", 4: "mixed numbers"}
        st.markdown(f"**Current Difficulty:** {difficulty_names[difficulty_level]}")
        # Progress bar (1 to 4 levels)
        progress = (difficulty_level - 1) / 3  # Convert 1-4 to 0-1
        st.progress(progress, text=f"Level {difficulty_level}: {difficulty_names[difficulty_level]}")
    
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
        - **Read the decimal number**
        - **Type the fraction equivalent** in the text box
        - **Use the format a/b** (like 1/2 or 32/100)
        - **For mixed numbers use the format a b/c** (like 1 1/4)
        - **Click Submit** to check your answer
        
        ### Key Concepts:
        - **Tenths**: 0.3 = 3/10
        - **Hundredths**: 0.25 = 25/100 = 1/4 (simplified)
        - **Thousandths**: 0.125 = 125/1000 = 1/8 (simplified)
        - **Mixed numbers**: 1.5 = 1 1/2
        
        ### Conversion Tips:
        - **Count decimal places** to find denominator
        - **1 decimal place** → denominator 10
        - **2 decimal places** → denominator 100  
        - **3 decimal places** → denominator 1000
        - **Simplify when possible**: 50/100 = 1/2
        
        ### Examples:
        - **0.5** = 5/10 = 1/2
        - **0.32** = 32/100 = 8/25
        - **0.04** = 4/100 = 1/25
        - **0.125** = 125/1000 = 1/8
        - **1.75** = 1 3/4
        
        ### Input Format:
        - **Simple fractions**: 1/2, 3/4, 5/8
        - **Mixed numbers**: 2 1/4, 1 1/2, 3 2/5
        - **Both simplified and unsimplified forms accepted**
        
        ### Common Conversions:
        - **0.5** = 1/2
        - **0.25** = 1/4
        - **0.75** = 3/4
        - **0.2** = 1/5
        - **0.125** = 1/8
        
        ### Difficulty Levels:
        - **🟡 Tenths:** 0.3, 0.7, 0.9
        - **🟠 Hundredths:** 0.25, 0.32, 0.04
        - **🟠 Thousandths:** 0.125, 0.375, 0.008
        - **🔴 Mixed Numbers:** 1.5, 2.25, 1.125
        
        ### Scoring:
        - ✅ **Correct answer:** Move to harder decimals
        - ❌ **Wrong answer:** Practice with easier decimals
        - 🎯 **Goal:** Master mixed numbers!
        """)

def generate_new_question():
    """Generate a new decimal to fraction conversion question"""
    difficulty = st.session_state.decimals_to_fractions_difficulty
    
    if difficulty == 1:
        generate_tenths_question()
    elif difficulty == 2:
        generate_hundredths_question()
    elif difficulty == 3:
        generate_thousandths_question()
    else:
        generate_mixed_number_question()
    
    # Set current_question to "active" to prevent regeneration
    st.session_state.current_question = "active"

def generate_tenths_question():
    """Generate a question with tenths (1 decimal place)"""
    # Generate a random decimal with 1 decimal place
    options = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    decimal = random.choice(options)
    
    # Convert to fraction
    fraction = Fraction(decimal).limit_denominator()
    
    st.session_state.question_data = {
        "decimal": decimal,
        "correct_fraction": fraction,
        "question_type": "tenths",
        "decimal_places": 1
    }

def generate_hundredths_question():
    """Generate a question with hundredths (2 decimal places)"""
    # Generate a random decimal with 2 decimal places
    numerator = random.randint(1, 99)
    decimal = numerator / 100
    
    # Convert to fraction
    fraction = Fraction(decimal).limit_denominator()
    
    st.session_state.question_data = {
        "decimal": decimal,
        "correct_fraction": fraction,
        "question_type": "hundredths",
        "decimal_places": 2
    }

def generate_thousandths_question():
    """Generate a question with thousandths (3 decimal places)"""
    # Generate a random decimal with 3 decimal places
    numerator = random.randint(1, 999)
    decimal = numerator / 1000
    
    # Convert to fraction
    fraction = Fraction(decimal).limit_denominator()
    
    st.session_state.question_data = {
        "decimal": decimal,
        "correct_fraction": fraction,
        "question_type": "thousandths",
        "decimal_places": 3
    }

def generate_mixed_number_question():
    """Generate a question with mixed numbers (decimals > 1)"""
    # Generate a mixed number
    whole_part = random.randint(1, 4)
    
    # Common decimal fractions
    fraction_options = [0.25, 0.5, 0.75, 0.125, 0.375, 0.625, 0.875, 0.2, 0.4, 0.6, 0.8]
    fraction_part = random.choice(fraction_options)
    
    decimal = whole_part + fraction_part
    
    # Convert to mixed number fraction
    fraction = Fraction(decimal).limit_denominator()
    
    st.session_state.question_data = {
        "decimal": decimal,
        "correct_fraction": fraction,
        "question_type": "mixed_number",
        "decimal_places": len(str(fraction_part).split('.')[1]) if '.' in str(fraction_part) else 1
    }

def parse_user_fraction(user_input):
    """Parse user input and return a Fraction object"""
    user_input = user_input.strip()
    
    # Handle mixed numbers (e.g., "1 1/2", "2 3/4")
    mixed_pattern = r'^(\d+)\s+(\d+)/(\d+)$'
    mixed_match = re.match(mixed_pattern, user_input)
    
    if mixed_match:
        whole = int(mixed_match.group(1))
        numerator = int(mixed_match.group(2))
        denominator = int(mixed_match.group(3))
        
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        
        # Convert to improper fraction
        total_numerator = whole * denominator + numerator
        return Fraction(total_numerator, denominator)
    
    # Handle simple fractions (e.g., "1/2", "3/4")
    fraction_pattern = r'^(\d+)/(\d+)$'
    fraction_match = re.match(fraction_pattern, user_input)
    
    if fraction_match:
        numerator = int(fraction_match.group(1))
        denominator = int(fraction_match.group(2))
        
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        
        return Fraction(numerator, denominator)
    
    # Handle whole numbers
    if user_input.isdigit():
        return Fraction(int(user_input))
    
    raise ValueError("Invalid fraction format")

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display the question with nice formatting (matching the images)
    st.markdown("### 🔢 Convert to Fraction:")
    
    # Display the decimal in a highlighted box like the images
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa; 
        padding: 30px; 
        border-radius: 15px; 
        border: 2px solid #dee2e6;
        text-align: center;
        margin: 30px 0;
        font-size: 24px;
        color: #495057;
    ">
        Write <strong style="font-size: 32px; color: #007bff;">{data['decimal']}</strong> as a fraction.
    </div>
    """, unsafe_allow_html=True)
    
    # Text input for the answer (similar to the images)
    if not st.session_state.show_feedback:
        with st.form("answer_form", clear_on_submit=False):
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                # Text input field
                user_input = st.text_input(
                    "Enter your answer:",
                    placeholder="1/2 or 1 1/2",
                    key="fraction_input",
                    label_visibility="collapsed"
                )
                
                # Submit button (green like in the images)
                submit_button = st.form_submit_button(
                    "Submit", 
                    type="primary", 
                    use_container_width=True
                )
            
            if submit_button:
                if user_input.strip():
                    try:
                        # Parse the user input
                        user_fraction = parse_user_fraction(user_input)
                        st.session_state.user_answer = user_fraction
                        st.session_state.show_feedback = True
                        st.session_state.answer_submitted = True
                        st.rerun()
                    except ValueError as e:
                        st.error(f"❌ Please enter a valid fraction (e.g., 1/2 or 2 1/4)")
                else:
                    st.error("❌ Please enter an answer before submitting")
    
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
    correct_answer = st.session_state.question_data['correct_fraction']
    
    # Check if answers are equivalent
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 4 levels)
        old_difficulty = st.session_state.decimals_to_fractions_difficulty
        st.session_state.decimals_to_fractions_difficulty = min(st.session_state.decimals_to_fractions_difficulty + 1, 4)
        
        if st.session_state.decimals_to_fractions_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered mixed numbers!**")
        elif old_difficulty < st.session_state.decimals_to_fractions_difficulty:
            level_names = {1: "tenths", 2: "hundredths", 3: "thousandths", 4: "mixed numbers"}
            st.info(f"⬆️ **Difficulty increased! Now working with {level_names[st.session_state.decimals_to_fractions_difficulty]}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show correct answer
        if correct_answer.denominator == 1:
            st.info(f"**Correct answer:** {correct_answer.numerator}")
        else:
            # Show as mixed number if appropriate
            if correct_answer > 1:
                whole_part = correct_answer.numerator // correct_answer.denominator
                remainder = correct_answer.numerator % correct_answer.denominator
                if remainder == 0:
                    st.info(f"**Correct answer:** {whole_part}")
                else:
                    st.info(f"**Correct answer:** {whole_part} {remainder}/{correct_answer.denominator}")
            else:
                st.info(f"**Correct answer:** {correct_answer.numerator}/{correct_answer.denominator}")
        
        # Decrease difficulty (min 1 level)
        old_difficulty = st.session_state.decimals_to_fractions_difficulty
        st.session_state.decimals_to_fractions_difficulty = max(st.session_state.decimals_to_fractions_difficulty - 1, 1)
        
        if old_difficulty > st.session_state.decimals_to_fractions_difficulty:
            level_names = {1: "tenths", 2: "hundredths", 3: "thousandths", 4: "mixed numbers"}
            st.warning(f"⬇️ **Difficulty decreased to {level_names[st.session_state.decimals_to_fractions_difficulty]}. Keep practicing!**")
    
    # Show explanation
    show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    decimal = data['decimal']
    correct_fraction = data['correct_fraction']
    question_type = data['question_type']
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        if question_type == "tenths":
            st.markdown(f"""
            ### Step-by-step conversion:
            
            **Decimal:** {decimal}
            **Fraction:** {correct_fraction}
            
            ### Method:
            1. **Count decimal places:** {decimal} has 1 decimal place
            2. **Write as fraction:** {decimal} = {int(decimal * 10)}/10
            3. **Simplify if possible:** {int(decimal * 10)}/10 = {correct_fraction}
            
            ### Quick tip:
            For tenths, put the digit after the decimal over 10: 0.{int(decimal * 10)} = {int(decimal * 10)}/10
            """)
        
        elif question_type == "hundredths":
            original_fraction = Fraction(int(decimal * 100), 100)
            st.markdown(f"""
            ### Step-by-step conversion:
            
            **Decimal:** {decimal}
            **Fraction:** {correct_fraction}
            
            ### Method:
            1. **Count decimal places:** {decimal} has 2 decimal places
            2. **Write as fraction:** {decimal} = {int(decimal * 100)}/100
            3. **Simplify if possible:** {original_fraction} = {correct_fraction}
            
            ### Quick tip:
            For hundredths, put the digits after the decimal over 100: 0.{int(decimal * 100):02d} = {int(decimal * 100)}/100
            """)
        
        elif question_type == "thousandths":
            original_fraction = Fraction(int(decimal * 1000), 1000)
            st.markdown(f"""
            ### Step-by-step conversion:
            
            **Decimal:** {decimal}
            **Fraction:** {correct_fraction}
            
            ### Method:
            1. **Count decimal places:** {decimal} has 3 decimal places
            2. **Write as fraction:** {decimal} = {int(decimal * 1000)}/1000
            3. **Simplify if possible:** {original_fraction} = {correct_fraction}
            
            ### Quick tip:
            For thousandths, put the digits after the decimal over 1000: 0.{int(decimal * 1000):03d} = {int(decimal * 1000)}/1000
            """)
        
        elif question_type == "mixed_number":
            whole_part = int(decimal)
            decimal_part = decimal - whole_part
            
            st.markdown(f"""
            ### Step-by-step conversion:
            
            **Decimal:** {decimal}
            **Mixed Number:** {correct_fraction}
            
            ### Method:
            1. **Separate whole and decimal parts:** {whole_part} + {decimal_part}
            2. **Convert decimal part to fraction:** {decimal_part} = {Fraction(decimal_part).limit_denominator()}
            3. **Combine:** {whole_part} + {Fraction(decimal_part).limit_denominator()} = {correct_fraction}
            
            ### Quick tip:
            For mixed numbers: Keep the whole number, convert the decimal part to a fraction!
            """)
        
        # Add general tips
        st.markdown("""
        ### 💡 General Tips:
        - **Count decimal places** to find the denominator
        - **Always simplify** fractions when possible
        - **Check your work** by converting back to decimal
        - **Common equivalents:** 0.5=1/2, 0.25=1/4, 0.75=3/4
        """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = "new"  # Reset to "new" so new question generates
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    
    # Clear answer-related session state
    keys_to_remove = ['user_answer', 'fraction_input']
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]