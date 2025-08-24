import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Put Numbers in Order practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/E. Decimals/put_assorted_decimals_fractions_and_mixed_numbers_in_order.py
    """
    # Initialize session state
    if "order_difficulty" not in st.session_state:
        st.session_state.order_difficulty = 1  # Start with 3 numbers
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_order = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.user_selections = []  # Track order of selections
        st.session_state.tile_positions = {}  # Track position of each tile
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > E. Decimals**")
    st.title("🔢 Put Numbers in Order")
    st.markdown("*Order decimals, fractions and mixed numbers from largest to smallest*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.order_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        num_items = difficulty_level + 2  # 3, 4, 5, or 6 items
        st.markdown(f"**Current Level:** {num_items} numbers")
        # Progress bar
        progress = (difficulty_level - 1) / 3
        st.progress(progress, text=f"Level {difficulty_level} of 4")
    
    with col2:
        if difficulty_level <= 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level <= 2:
            st.markdown("**🟡 Intermediate**")
        elif difficulty_level <= 3:
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
    if st.session_state.current_question is None:
        generate_new_question()
    
    # Display current question
    display_question()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Click the numbers in order from largest to smallest**
        - **Each clicked number will be marked with its position**
        - **Use the Reset button to start over if needed**
        - **Submit your answer when all numbers are ordered**
        
        ### Tips for Success:
        - **Convert to the same form** to compare easily:
          - Fraction → Decimal: Divide numerator by denominator
          - Mixed number → Decimal: Convert whole part + fraction part
        - **Common conversions:**
          - 1/2 = 0.5
          - 1/4 = 0.25
          - 3/4 = 0.75
          - 1/5 = 0.2
          - 1/3 ≈ 0.333...
          - 2/3 ≈ 0.667...
        
        ### Examples:
        - **Order:** 2½, 0.75, 1/3 → **Answer:** 2½ (2.5), 0.75, 1/3 (0.333...)
        - **Order:** 1.2, 5/4, 0.9 → **Answer:** 5/4 (1.25), 1.2, 0.9
        
        ### Difficulty Levels:
        - **🟢 Basic:** 3 numbers with simple conversions
        - **🟡 Intermediate:** 4 numbers with mixed types
        - **🟠 Advanced:** 5 numbers including mixed numbers
        - **🔴 Expert:** 6 numbers with complex fractions
        """)

def generate_number_value():
    """Generate a random number in decimal, fraction, or mixed number format"""
    number_type = random.choice(['decimal', 'fraction', 'mixed'])
    
    if number_type == 'decimal':
        # Generate decimal between 0.1 and 3.9
        value = round(random.uniform(0.1, 3.9), 2)
        display = str(value)
        return {'value': value, 'display': display, 'type': 'decimal'}
    
    elif number_type == 'fraction':
        # Generate proper fraction
        denominators = [2, 3, 4, 5, 6, 8, 10]
        denominator = random.choice(denominators)
        numerator = random.randint(1, denominator - 1)
        value = numerator / denominator
        display = f"{numerator}/{denominator}"
        return {'value': value, 'display': display, 'type': 'fraction'}
    
    else:  # mixed number
        # Generate mixed number
        whole = random.randint(1, 3)
        denominators = [2, 3, 4, 5, 6, 8]
        denominator = random.choice(denominators)
        numerator = random.randint(1, denominator - 1)
        value = whole + (numerator / denominator)
        # Store as tuple for easier display
        display = f"{whole} {numerator}/{denominator}"
        return {'value': value, 'display': display, 'type': 'mixed', 
                'whole': whole, 'numerator': numerator, 'denominator': denominator}

def generate_new_question():
    """Generate a new ordering question based on difficulty"""
    num_items = st.session_state.order_difficulty + 2  # 3, 4, 5, or 6 items
    
    # Generate unique numbers
    numbers = []
    values_used = set()
    
    while len(numbers) < num_items:
        num = generate_number_value()
        # Ensure uniqueness (within 0.01 tolerance)
        is_unique = True
        for used_val in values_used:
            if abs(num['value'] - used_val) < 0.01:
                is_unique = False
                break
        
        if is_unique:
            numbers.append(num)
            values_used.add(num['value'])
    
    # Sort by value (largest to smallest)
    correct_order = sorted(numbers, key=lambda x: x['value'], reverse=True)
    
    # Shuffle for display
    display_order = numbers.copy()
    random.shuffle(display_order)
    
    st.session_state.question_data = {
        'numbers': display_order,
        'correct_order': correct_order
    }
    st.session_state.user_selections = []
    st.session_state.tile_positions = {}
    st.session_state.current_question = "Put these numbers in order from largest to smallest."

def get_position_label(position, total):
    """Get the label for a position"""
    if position == 1:
        return "1st (Largest)"
    elif position == 2:
        return "2nd"
    elif position == 3:
        return "3rd"
    elif position == total:
        return f"{position}th (Smallest)"
    else:
        return f"{position}th"

def display_question():
    """Display the current question interface"""
    # Display question
    st.markdown("### 📊 Question:")
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Instruction
    st.info("💡 **Click the numbers in order from largest to smallest**")
    
    # Show current selection status
    num_items = len(st.session_state.question_data['numbers'])
    selections_made = len(st.session_state.user_selections)
    
    if selections_made > 0:
        st.markdown(f"**Progress:** {selections_made} of {num_items} numbers selected")
    
    # Reset button (only show if selections have been made)
    if selections_made > 0 and selections_made < num_items:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Reset Order", type="secondary", use_container_width=True):
                st.session_state.user_selections = []
                st.session_state.tile_positions = {}
                st.rerun()
    
    # Display tiles
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(num_items)
    
    for i, (col, num) in enumerate(zip(cols, st.session_state.question_data['numbers'])):
        with col:
            # Check if this number has been selected
            position = st.session_state.tile_positions.get(i)
            
            if position is not None:
                # Already selected - show position
                button_type = "primary"
                help_text = get_position_label(position, num_items)
                disabled = True
                
                # Show position label above tile
                st.markdown(f"<div style='text-align: center; color: #1976d2; font-weight: bold; margin-bottom: 5px;'>{help_text}</div>", 
                           unsafe_allow_html=True)
            else:
                # Not selected yet
                button_type = "secondary"
                help_text = "Click to select this number"
                disabled = False
                
                # Empty space for alignment
                st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
            
            # Create button
            if st.button(num['display'], 
                        key=f"tile_{i}",
                        type=button_type,
                        use_container_width=True,
                        help=help_text,
                        disabled=disabled):
                
                # Add this selection
                st.session_state.user_selections.append(i)
                st.session_state.tile_positions[i] = len(st.session_state.user_selections)
                st.rerun()
    
    # Show message based on selection status
    if selections_made == num_items:
        st.success("✅ **All numbers selected! Click Submit to check your answer.**")
    elif selections_made > 0:
        next_position = get_position_label(selections_made + 1, num_items)
        st.info(f"👆 **Now select the {next_position} number**")
    
    # Submit button (only enabled when all selections made)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit", 
                    type="primary", 
                    use_container_width=True,
                    disabled=(selections_made < num_items or st.session_state.answer_submitted)):
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next question button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="primary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    correct_order = st.session_state.question_data['correct_order']
    user_order = [st.session_state.question_data['numbers'][i] for i in st.session_state.user_selections]
    
    # Check if order is correct
    is_correct = all(user['value'] == correct['value'] 
                    for user, correct in zip(user_order, correct_order))
    
    if is_correct:
        st.success("🎉 **Excellent! That's the correct order!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.order_difficulty
        st.session_state.order_difficulty = min(
            st.session_state.order_difficulty + 1, 4
        )
        
        if st.session_state.order_difficulty == 4 and old_difficulty < 4:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered ordering 6 numbers!**")
        elif old_difficulty < st.session_state.order_difficulty:
            new_num = st.session_state.order_difficulty + 2
            st.info(f"⬆️ **Level up! Now ordering {new_num} numbers**")
    
    else:
        st.error("❌ **Not quite right. Here's the correct order:**")
        
        # Show correct order
        correct_display = " > ".join([num['display'] for num in correct_order])
        st.markdown(f"**Correct order:** {correct_display}")
        
        # Show user's order for comparison
        user_display = " > ".join([num['display'] for num in user_order])
        st.markdown(f"**Your order:** {user_display}")
        
        # Decrease difficulty
        old_difficulty = st.session_state.order_difficulty
        st.session_state.order_difficulty = max(
            st.session_state.order_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.order_difficulty:
            new_num = st.session_state.order_difficulty + 2
            st.warning(f"⬇️ **Level adjusted to {new_num} numbers. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation with decimal conversions"""
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown("### Converting to decimals for comparison:")
        
        correct_order = st.session_state.question_data['correct_order']
        
        for i, num in enumerate(correct_order):
            if num['type'] == 'decimal':
                st.markdown(f"{i+1}. **{num['display']}** = {num['value']} (already decimal)")
            elif num['type'] == 'fraction':
                parts = num['display'].split('/')
                if len(parts) == 2:
                    st.markdown(f"{i+1}. **{num['display']}** = {parts[0]} ÷ {parts[1]} = {num['value']:.3f}")
            else:  # mixed number
                if 'whole' in num:
                    whole = num['whole']
                    numerator = num['numerator']
                    denominator = num['denominator']
                    frac_value = numerator / denominator
                    st.markdown(f"{i+1}. **{whole} {numerator}/{denominator}** = {whole} + {numerator}/{denominator} = {whole} + {frac_value:.3f} = {num['value']:.3f}")
                else:
                    st.markdown(f"{i+1}. **{num['display']}** = {num['value']:.3f}")
        
        st.markdown("### Order from largest to smallest:")
        order_display = " > ".join([f"{num['value']:.3f}" for num in correct_order])
        st.markdown(f"**{order_display}**")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_order = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.user_selections = []
    st.session_state.tile_positions = {}