import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Convert Fractions and Mixed Numbers to Decimals activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Decimals/convert_fractions_and_mixed_numbers_to_decimals.py
    """
    # Initialize session state
    if "fractions_difficulty" not in st.session_state:
        st.session_state.fractions_difficulty = 1  # Start with simple fractions
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = "new"  # Start with new question needed
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Decimals**")
    st.title("🔢 Convert Fractions and Mixed Numbers to Decimals")
    st.markdown("*Convert fractions like 17/100 to decimal numbers like 0.17*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.fractions_difficulty
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
        - **Read the fraction or mixed number**
        - **Type the decimal equivalent** in the text box
        - **Click Submit** to check your answer
        - **Remember**: Use a decimal point (.) not a comma
        
        ### Key Concepts:
        - **Tenths**: 1/10 = 0.1, 3/10 = 0.3
        - **Hundredths**: 1/100 = 0.01, 25/100 = 0.25
        - **Thousandths**: 1/1000 = 0.001, 375/1000 = 0.375
        - **Mixed numbers**: 2 3/4 = 2.75
        
        ### Conversion Tips:
        - **Tenths (÷10)**: 7/10 = 7 ÷ 10 = 0.7
        - **Hundredths (÷100)**: 43/100 = 43 ÷ 100 = 0.43
        - **Thousandths (÷1000)**: 256/1000 = 256 ÷ 1000 = 0.256
        - **Mixed numbers**: Add whole + fraction: 1 + 0.5 = 1.5
        
        ### Examples:
        - **9/10** = 0.9
        - **17/100** = 0.17
        - **771/1000** = 0.771
        - **2 1/4** = 2.25
        - **3 3/5** = 3.6
        
        ### Common Mistakes:
        - **Don't forget the zero**: 5/100 = 0.05 (not .5)
        - **Count decimal places**: 1000 = 3 decimal places
        - **Mixed numbers**: Convert fraction first, then add
        
        ### Difficulty Levels:
        - **🟡 Tenths:** Simple fractions like 3/10
        - **🟠 Hundredths:** Fractions like 25/100
        - **🟠 Thousandths:** Fractions like 375/1000
        - **🔴 Mixed Numbers:** Like 2 3/4 = 2.75
        
        ### Scoring:
        - ✅ **Correct answer:** Move to harder fractions
        - ❌ **Wrong answer:** Practice with easier fractions
        - 🎯 **Goal:** Master mixed numbers!
        """)

def generate_new_question():
    """Generate a new fraction to decimal conversion question"""
    difficulty = st.session_state.fractions_difficulty
    
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
    """Generate a question with tenths (denominators of 10)"""
    # Generate a random numerator from 1-9 (avoiding 0 and 10)
    numerator = random.randint(1, 9)
    denominator = 10
    
    # Create the question
    fraction_str = f"{numerator}/{denominator}"
    correct_decimal = numerator / denominator
    
    st.session_state.question_data = {
        "fraction_display": fraction_str,
        "numerator": numerator,
        "denominator": denominator,
        "correct_answer": correct_decimal,
        "question_type": "tenths"
    }

def generate_hundredths_question():
    """Generate a question with hundredths (denominators of 100)"""
    # Generate a random numerator from 1-99 (avoiding 0 and 100)
    numerator = random.randint(1, 99)
    denominator = 100
    
    # Create the question
    fraction_str = f"{numerator}/{denominator}"
    correct_decimal = numerator / denominator
    
    st.session_state.question_data = {
        "fraction_display": fraction_str,
        "numerator": numerator,
        "denominator": denominator,
        "correct_answer": correct_decimal,
        "question_type": "hundredths"
    }

def generate_thousandths_question():
    """Generate a question with thousandths (denominators of 1000)"""
    # Generate a random numerator from 1-999 (avoiding 0 and 1000)
    numerator = random.randint(1, 999)
    denominator = 1000
    
    # Create the question
    fraction_str = f"{numerator}/{denominator}"
    correct_decimal = numerator / denominator
    
    st.session_state.question_data = {
        "fraction_display": fraction_str,
        "numerator": numerator,
        "denominator": denominator,
        "correct_answer": correct_decimal,
        "question_type": "thousandths"
    }

def generate_mixed_number_question():
    """Generate a question with mixed numbers"""
    # Generate whole number part
    whole_part = random.randint(1, 5)
    
    # Generate fraction part - use common fractions
    fraction_options = [
        (1, 2),   # 1/2 = 0.5
        (1, 4),   # 1/4 = 0.25
        (3, 4),   # 3/4 = 0.75
        (1, 5),   # 1/5 = 0.2
        (2, 5),   # 2/5 = 0.4
        (3, 5),   # 3/5 = 0.6
        (4, 5),   # 4/5 = 0.8
        (1, 8),   # 1/8 = 0.125
        (3, 8),   # 3/8 = 0.375
        (5, 8),   # 5/8 = 0.625
        (7, 8),   # 7/8 = 0.875
        (1, 10),  # 1/10 = 0.1
        (3, 10),  # 3/10 = 0.3
        (7, 10),  # 7/10 = 0.7
        (9, 10),  # 9/10 = 0.9
    ]
    
    frac_num, frac_den = random.choice(fraction_options)
    
    # Create the mixed number display
    mixed_number_str = f"{whole_part} {frac_num}/{frac_den}"
    
    # Calculate correct decimal
    fraction_decimal = frac_num / frac_den
    correct_decimal = whole_part + fraction_decimal
    
    st.session_state.question_data = {
        "fraction_display": mixed_number_str,
        "whole_part": whole_part,
        "frac_numerator": frac_num,
        "frac_denominator": frac_den,
        "correct_answer": correct_decimal,
        "question_type": "mixed_number"
    }

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display the question with nice formatting
    st.markdown("### 🔢 Convert to Decimal:")
    
    # Display the fraction in a highlighted box like the images
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
        Write <strong style="font-size: 32px; color: #007bff;">{data['fraction_display']}</strong> as a decimal number.
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
                    placeholder="0.0",
                    key="decimal_input",
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
                        user_answer = float(user_input.strip())
                        st.session_state.user_answer = user_answer
                        st.session_state.show_feedback = True
                        st.session_state.answer_submitted = True
                        st.rerun()
                    except ValueError:
                        st.error("❌ Please enter a valid decimal number (e.g., 0.25)")
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
    correct_answer = st.session_state.question_data['correct_answer']
    
    # Check if answers match (with small tolerance for floating point errors)
    if abs(user_answer - correct_answer) < 0.0001:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 4 levels)
        old_difficulty = st.session_state.fractions_difficulty
        st.session_state.fractions_difficulty = min(st.session_state.fractions_difficulty + 1, 4)
        
        if st.session_state.fractions_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered mixed numbers!**")
        elif old_difficulty < st.session_state.fractions_difficulty:
            level_names = {1: "tenths", 2: "hundredths", 3: "thousandths", 4: "mixed numbers"}
            st.info(f"⬆️ **Difficulty increased! Now working with {level_names[st.session_state.fractions_difficulty]}**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show correct answer
        st.info(f"**Correct answer:** {correct_answer}")
        
        # Decrease difficulty (min 1 level)
        old_difficulty = st.session_state.fractions_difficulty
        st.session_state.fractions_difficulty = max(st.session_state.fractions_difficulty - 1, 1)
        
        if old_difficulty > st.session_state.fractions_difficulty:
            level_names = {1: "tenths", 2: "hundredths", 3: "thousandths", 4: "mixed numbers"}
            st.warning(f"⬇️ **Difficulty decreased to {level_names[st.session_state.fractions_difficulty]}. Keep practicing!**")
    
    # Show explanation
    show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    question_type = data['question_type']
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        if question_type == "tenths":
            st.markdown(f"""
            ### Step-by-step conversion:
            
            **Fraction:** {data['fraction_display']}
            **Decimal:** {data['correct_answer']}
            
            ### Method:
            1. **Divide numerator by denominator:** {data['numerator']} ÷ {data['denominator']} = {data['correct_answer']}
            2. **Think of place values:** {data['numerator']} tenths = 0.{data['numerator']}
            3. **Remember:** Tenths have 1 decimal place
            
            ### Quick tip:
            For tenths, just put the numerator after the decimal point: {data['numerator']}/10 = 0.{data['numerator']}
            """)
        
        elif question_type == "hundredths":
            st.markdown(f"""
            ### Step-by-step conversion:
            
            **Fraction:** {data['fraction_display']}
            **Decimal:** {data['correct_answer']}
            
            ### Method:
            1. **Divide numerator by denominator:** {data['numerator']} ÷ {data['denominator']} = {data['correct_answer']}
            2. **Think of place values:** {data['numerator']} hundredths = 0.{data['numerator']:02d}
            3. **Remember:** Hundredths have 2 decimal places
            
            ### Quick tip:
            For hundredths, put the numerator after the decimal point with 2 places: {data['numerator']}/100 = 0.{data['numerator']:02d}
            """)
        
        elif question_type == "thousandths":
            st.markdown(f"""
            ### Step-by-step conversion:
            
            **Fraction:** {data['fraction_display']}
            **Decimal:** {data['correct_answer']}
            
            ### Method:
            1. **Divide numerator by denominator:** {data['numerator']} ÷ {data['denominator']} = {data['correct_answer']}
            2. **Think of place values:** {data['numerator']} thousandths = 0.{data['numerator']:03d}
            3. **Remember:** Thousandths have 3 decimal places
            
            ### Quick tip:
            For thousandths, put the numerator after the decimal point with 3 places: {data['numerator']}/1000 = 0.{data['numerator']:03d}
            """)
        
        elif question_type == "mixed_number":
            fraction_decimal = data['frac_numerator'] / data['frac_denominator']
            st.markdown(f"""
            ### Step-by-step conversion:
            
            **Mixed Number:** {data['fraction_display']}
            **Decimal:** {data['correct_answer']}
            
            ### Method:
            1. **Separate whole and fraction:** {data['whole_part']} + {data['frac_numerator']}/{data['frac_denominator']}
            2. **Convert fraction to decimal:** {data['frac_numerator']} ÷ {data['frac_denominator']} = {fraction_decimal}
            3. **Add whole number:** {data['whole_part']} + {fraction_decimal} = {data['correct_answer']}
            
            ### Quick tip:
            Mixed numbers: Keep the whole number, convert the fraction, then add them together!
            """)
        
        # Add general tips based on difficulty
        if question_type in ["tenths", "hundredths", "thousandths"]:
            st.markdown("""
            ### 💡 General Tips:
            - **Count the zeros** in the denominator to know decimal places
            - **10 = 1 decimal place, 100 = 2 places, 1000 = 3 places**
            - **Add leading zeros** if needed: 5/100 = 0.05 (not 0.5)
            - **Practice with division** if you're unsure
            """)
        else:
            st.markdown("""
            ### 💡 Mixed Number Tips:
            - **Always keep the whole number** part
            - **Convert only the fraction** part to decimal
            - **Add them together** for the final answer
            - **Common fractions:** 1/2=0.5, 1/4=0.25, 3/4=0.75
            """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = "new"  # Reset to "new" so new question generates
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    
    # Clear answer-related session state
    keys_to_remove = ['user_answer', 'decimal_input']
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]