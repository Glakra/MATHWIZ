import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the arithmetic sequences with fractions activity.
    This gets called when the subtopic is loaded from:
    Grades/Year X/Number Sequences/arithmetic_sequences_fractions.py
    """
    # Initialize session state
    if "fraction_seq_difficulty" not in st.session_state:
        st.session_state.fraction_seq_difficulty = 1
    
    if "current_fraction_problem" not in st.session_state:
        st.session_state.current_fraction_problem = None
        st.session_state.fraction_problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.consecutive_correct = 0
        st.session_state.total_attempted = 0
        st.session_state.total_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > Number Sequences**")
    st.title("🔢 Arithmetic Sequences with Fractions")
    st.markdown("*Find the next fraction in the sequence*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.fraction_seq_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = {
            1: "Basic fractions (same denominator, +1 or -1)",
            2: "Larger denominators (up to 20)",
            3: "Skip counting (±2, ±3)",
            4: "Mixed patterns",
            5: "Complex sequences"
        }
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level}/5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Beginner**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_fraction_problem is None:
        generate_new_fraction_problem()
    
    # Display current problem
    display_fraction_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Solve:
        1. **Look at the fractions** in the sequence
        2. **Check what's changing** - usually the numerator (top number)
        3. **Find the pattern** - is it adding or subtracting?
        4. **Apply the pattern** to find the next fraction
        
        ### Fraction Patterns:
        - **Same denominator** - bottom number stays the same
        - **Changing numerator** - top number goes up or down
        - **Common patterns:**
          - Add 1: 2/8 → 3/8 → 4/8 → 5/8
          - Subtract 1: 9/11 → 8/11 → 7/11 → 6/11
          - Add 2: 1/10 → 3/10 → 5/10 → 7/10
        
        ### Writing Fractions:
        - Type the numerator (top number)
        - Type "/" 
        - Type the denominator (bottom number)
        - Example: Type "5/8" for five-eighths
        
        ### Tips:
        - **Keep the same denominator** in your answer
        - **Check the pattern** with at least two pairs
        - **Simplify only if** the sequence shows simplified fractions
        
        ### Difficulty Levels:
        - **🟢 Level 1-2:** Add/subtract 1, small denominators
        - **🟡 Level 3:** Skip counting patterns
        - **🔴 Level 4-5:** Complex patterns, larger numbers
        """)

def generate_new_fraction_problem():
    """Generate a new fraction sequence problem"""
    difficulty = st.session_state.fraction_seq_difficulty
    
    if difficulty == 1:
        # Basic fractions (denominators 8-12, step ±1)
        denominator = random.randint(8, 12)
        step = random.choice([-1, 1])
        length = 5  # Show 4, ask for 5th
        
        # Choose starting numerator to avoid going negative or over denominator
        if step == 1:
            start_num = random.randint(2, denominator - length)
        else:
            start_num = random.randint(length + 1, denominator - 2)
    
    elif difficulty == 2:
        # Larger denominators (13-20, step ±1)
        denominator = random.randint(13, 20)
        step = random.choice([-1, 1])
        length = 5
        
        if step == 1:
            start_num = random.randint(2, denominator - length)
        else:
            start_num = random.randint(length + 1, denominator - 2)
    
    elif difficulty == 3:
        # Skip counting (±2, ±3)
        denominator = random.randint(10, 25)
        step = random.choice([-3, -2, 2, 3])
        length = 5
        
        if step > 0:
            start_num = random.randint(2, max(2, denominator - length * abs(step)))
        else:
            start_num = random.randint(min(denominator - 2, length * abs(step) + 2), denominator - 2)
    
    elif difficulty == 4:
        # Mixed patterns (various steps and denominators)
        denominator = random.randint(12, 30)
        step = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        length = random.choice([5, 6])
        
        if step > 0:
            start_num = random.randint(1, max(1, denominator - length * abs(step)))
        else:
            start_num = random.randint(min(denominator - 1, length * abs(step) + 1), denominator - 1)
    
    else:  # difficulty == 5
        # Complex sequences (larger numbers, various patterns)
        pattern_type = random.choice(['arithmetic', 'alternating', 'fibonacci-like'])
        
        if pattern_type == 'arithmetic':
            denominator = random.randint(20, 50)
            step = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            length = 6
            
            if step > 0:
                start_num = random.randint(1, max(1, denominator - length * abs(step)))
            else:
                start_num = random.randint(min(denominator - 1, length * abs(step) + 1), denominator - 1)
        
        elif pattern_type == 'alternating':
            # Alternating add/subtract
            denominator = random.randint(15, 30)
            step1 = random.randint(1, 3)
            step2 = random.randint(-3, -1)
            length = 6
            start_num = random.randint(5, denominator - 10)
            
            # Generate alternating pattern
            step = (step1, step2)  # Will handle in generation
        
        else:  # fibonacci-like
            # Each numerator is sum of previous two
            denominator = random.randint(20, 40)
            start_num = random.randint(1, 3)
            second_num = random.randint(1, 3)
            length = 5
            step = 'fibonacci'
    
    # Generate the sequence
    sequence = []
    
    if isinstance(step, tuple):  # Alternating pattern
        current = start_num
        for i in range(length - 1):
            sequence.append(Fraction(current, denominator))
            if i % 2 == 0:
                current += step[0]
            else:
                current += step[1]
    elif step == 'fibonacci':  # Fibonacci-like
        sequence.append(Fraction(start_num, denominator))
        sequence.append(Fraction(second_num, denominator))
        for i in range(2, length - 1):
            next_num = sequence[i-1].numerator + sequence[i-2].numerator
            if next_num < denominator:
                sequence.append(Fraction(next_num, denominator))
            else:
                # If too large, use a different pattern
                step = 1
                sequence = []
                for j in range(length - 1):
                    sequence.append(Fraction(start_num + step * j, denominator))
                break
    else:  # Regular arithmetic
        for i in range(length - 1):
            numerator = start_num + step * i
            if 0 < numerator < denominator:
                sequence.append(Fraction(numerator, denominator))
    
    # Calculate the next fraction
    if isinstance(step, tuple):
        if (len(sequence) - 1) % 2 == 0:
            next_fraction = Fraction(sequence[-1].numerator + step[0], denominator)
        else:
            next_fraction = Fraction(sequence[-1].numerator + step[1], denominator)
    elif step == 'fibonacci' and len(sequence) >= 2:
        next_num = sequence[-1].numerator + sequence[-2].numerator
        next_fraction = Fraction(next_num, denominator)
    else:
        next_fraction = Fraction(sequence[-1].numerator + step, sequence[-1].denominator)
    
    st.session_state.fraction_problem_data = {
        'sequence': sequence,
        'next_fraction': next_fraction,
        'step': step,
        'pattern_type': pattern_type if difficulty == 5 else 'arithmetic',
        'difficulty': difficulty
    }
    st.session_state.current_fraction_problem = True

def display_fraction_problem():
    """Display the fraction sequence problem"""
    data = st.session_state.fraction_problem_data
    
    # Display instruction
    st.markdown("### What is the next fraction in this sequence?")
    
    # Display the sequence
    sequence_str = ""
    for i, frac in enumerate(data['sequence']):
        # Display as improper fraction (don't simplify to maintain pattern)
        sequence_str += f"<span style='font-size: 24px; font-weight: bold;'>{frac.numerator}/{frac.denominator}</span>"
        if i < len(data['sequence']) - 1:
            sequence_str += " , "
        else:
            sequence_str += " , ... "
    
    st.markdown(f"<div style='text-align: center; margin: 30px 0;'>{sequence_str}</div>", unsafe_allow_html=True)
    
    # Input field for answer
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_answer = st.text_input(
            "",
            key="fraction_answer",
            placeholder="Enter fraction (e.g., 5/8)",
            label_visibility="collapsed"
        )
    
    # Style the input
    st.markdown("""
    <style>
    input[type="text"] {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        height: 45px;
        border: 2px solid #4CAF50;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Submit", type="primary", use_container_width=True, disabled=st.session_state.answer_submitted):
            if user_answer:
                validate_fraction_answer(user_answer)
            else:
                st.warning("Please enter a fraction!")
    
    # Show feedback
    if st.session_state.show_feedback:
        show_fraction_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next Question", type="secondary", use_container_width=True):
                reset_fraction_problem_state()
                st.rerun()

def validate_fraction_answer(user_answer):
    """Validate the user's fraction answer"""
    data = st.session_state.fraction_problem_data
    
    try:
        # Parse user input as fraction
        if '/' in user_answer:
            parts = user_answer.strip().split('/')
            if len(parts) == 2:
                num = int(parts[0].strip())
                den = int(parts[1].strip())
                user_fraction = Fraction(num, den)
            else:
                st.error("Please enter a valid fraction (e.g., 5/8)")
                return
        else:
            st.error("Please enter a fraction with / (e.g., 5/8)")
            return
        
        st.session_state.total_attempted += 1
        
        # Check if answer is correct
        correct_fraction = data['next_fraction']
        
        # Compare fractions (they should have same numerator and denominator)
        if user_fraction.numerator == correct_fraction.numerator and user_fraction.denominator == correct_fraction.denominator:
            st.session_state.total_correct += 1
            st.session_state.consecutive_correct += 1
            st.session_state.user_correct = True
            
            # Increase difficulty after 3 consecutive correct
            if st.session_state.consecutive_correct >= 3:
                if st.session_state.fraction_seq_difficulty < 5:
                    st.session_state.fraction_seq_difficulty += 1
                st.session_state.consecutive_correct = 0
        else:
            st.session_state.consecutive_correct = 0
            st.session_state.user_correct = False
            st.session_state.user_answer = user_fraction
            
            # Decrease difficulty after poor performance
            if st.session_state.total_attempted % 3 == 0:
                accuracy = st.session_state.total_correct / st.session_state.total_attempted
                if accuracy < 0.5 and st.session_state.fraction_seq_difficulty > 1:
                    st.session_state.fraction_seq_difficulty -= 1
        
        st.session_state.show_feedback = True
        st.session_state.answer_submitted = True
        
    except ValueError:
        st.error("Please enter a valid fraction (e.g., 5/8)")
    except Exception as e:
        st.error("Invalid input. Please enter a fraction like 5/8")

def show_fraction_feedback():
    """Display feedback for fraction problems"""
    data = st.session_state.fraction_problem_data
    
    if st.session_state.user_correct:
        st.success("✅ **Correct! Well done!**")
        
        # Show celebration for level up
        if st.session_state.consecutive_correct == 0 and st.session_state.fraction_seq_difficulty > 1:
            st.markdown("""
            <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; 
                        border: 2px solid #4CAF50; text-align: center; margin: 10px 0;'>
                <h3 style='color: #2e7d32; margin: 0;'>🎉 Level Up! 🎉</h3>
                <p style='color: #388e3c; margin: 5px 0;'>You've advanced to Level {}</p>
            </div>
            """.format(st.session_state.fraction_seq_difficulty), unsafe_allow_html=True)
    else:
        correct = data['next_fraction']
        st.error(f"❌ **Not quite. The correct answer is {correct.numerator}/{correct.denominator}**")
        
        # Show explanation
        show_fraction_explanation()

def show_fraction_explanation():
    """Show step-by-step solution for fraction sequences"""
    data = st.session_state.fraction_problem_data
    
    with st.expander("📖 **See how to solve this**", expanded=True):
        st.markdown("### Step-by-Step Solution:")
        
        # Show the sequence
        seq_display = [f"{frac.numerator}/{frac.denominator}" for frac in data['sequence']]
        st.markdown(f"**Sequence:** {', '.join(seq_display)}, ...")
        
        # Explain the pattern
        st.markdown("**Step 1: Look at the pattern**")
        
        if data['pattern_type'] == 'arithmetic' or data['difficulty'] <= 4:
            # Show how numerators change
            st.markdown("Let's look at the numerators (top numbers):")
            numerators = [frac.numerator for frac in data['sequence']]
            st.code(f"Numerators: {', '.join(map(str, numerators))}")
            
            # Find the difference
            if isinstance(data['step'], tuple):
                st.markdown("This is an **alternating pattern**")
                st.markdown(f"- First step: +{data['step'][0]}")
                st.markdown(f"- Second step: {data['step'][1]}")
            else:
                if len(data['sequence']) >= 2:
                    diff = data['sequence'][1].numerator - data['sequence'][0].numerator
                    st.code(f"{data['sequence'][1].numerator} - {data['sequence'][0].numerator} = {diff}")
                    
                    if data['difficulty'] <= 3:
                        st.markdown(f"The numerator is {'increasing' if diff > 0 else 'decreasing'} by **{abs(diff)}** each time")
            
            st.markdown(f"The denominator stays **{data['sequence'][0].denominator}**")
        
        elif data['pattern_type'] == 'fibonacci-like':
            st.markdown("This is a **Fibonacci-like pattern**")
            st.markdown("Each numerator is the sum of the previous two:")
            for i in range(2, len(data['sequence'])):
                prev1 = data['sequence'][i-1].numerator
                prev2 = data['sequence'][i-2].numerator
                current = data['sequence'][i].numerator
                st.code(f"{prev2} + {prev1} = {current}")
        
        # Show the calculation
        st.markdown("**Step 2: Find the next fraction**")
        
        if isinstance(data['step'], tuple):
            # Alternating pattern
            last_num = data['sequence'][-1].numerator
            if (len(data['sequence']) - 1) % 2 == 0:
                st.code(f"{last_num} + {data['step'][0]} = {data['next_fraction'].numerator}")
            else:
                st.code(f"{last_num} + ({data['step'][1]}) = {data['next_fraction'].numerator}")
        elif data['pattern_type'] == 'fibonacci-like':
            prev1 = data['sequence'][-1].numerator
            prev2 = data['sequence'][-2].numerator
            st.code(f"{prev2} + {prev1} = {data['next_fraction'].numerator}")
        else:
            last_num = data['sequence'][-1].numerator
            next_num = data['next_fraction'].numerator
            if hasattr(data['step'], '__iter__'):
                step = data['step'] if not isinstance(data['step'], tuple) else data['step'][0]
            else:
                step = data['step']
            st.code(f"{last_num} + ({step}) = {next_num}")
        
        st.markdown(f"**Answer:** {data['next_fraction'].numerator}/{data['next_fraction'].denominator}")
        
        # Pattern summary
        if data['difficulty'] <= 2:
            st.info("💡 **Remember:** In these sequences, the denominator (bottom) stays the same, only the numerator (top) changes!")
        
        # Show accuracy
        if st.session_state.total_attempted > 0:
            accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100, 1)
            st.markdown(f"**Your accuracy:** {st.session_state.total_correct}/{st.session_state.total_attempted} ({accuracy}%)")

def reset_fraction_problem_state():
    """Reset for next problem"""
    st.session_state.current_fraction_problem = None
    st.session_state.fraction_problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    if "user_answer" in st.session_state:
        del st.session_state.user_answer
    if "user_correct" in st.session_state:
        del st.session_state.user_correct