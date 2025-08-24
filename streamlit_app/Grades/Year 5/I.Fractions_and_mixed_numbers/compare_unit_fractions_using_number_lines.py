import streamlit as st
import random
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

def run():
    """
    Main function to run the Compare Unit Fractions Using Number Lines activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/compare_unit_fractions_using_number_lines.py
    """
    # Initialize session state
    if "fractions_difficulty" not in st.session_state:
        st.session_state.fractions_difficulty = 1  # Start with easier comparisons
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("📊 Compare Unit Fractions Using Number Lines")
    st.markdown("*Use number lines to compare unit fractions*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.fractions_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = ["Easy comparisons", "Medium comparisons", "Challenging comparisons"][min(difficulty_level-1, 2)]
        st.markdown(f"**Current Level:** {difficulty_text}")
        progress = min(difficulty_level / 3, 1.0)
        st.progress(progress, text=difficulty_text)
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Beginner**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
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
        st.markdown("### How to Play:")
        st.markdown("- **Look at the two number lines** showing unit fractions")
        st.markdown("- **Compare the positions** of the dots on the number lines")
        st.markdown("- **Choose which fraction is less or greater** based on the question")
        st.markdown("- **Remember:** Unit fractions have 1 as the numerator (top number)")
        
        st.markdown("### Tips for Success:")
        st.markdown("- **Closer to 0 = Smaller:** Fractions closer to 0 are smaller")
        st.markdown("- **Closer to 1 = Larger:** Fractions closer to 1 are larger")
        st.markdown("- **Bigger denominator = Smaller fraction:** For unit fractions, 1/8 < 1/4 < 1/2")
        st.markdown("- **Think of pizza slices:** 1/2 is bigger than 1/4 (half vs quarter of a pizza)")
        
        st.markdown("### Examples:")
        st.markdown("- **1/2 vs 1/4:** 1/2 is greater (halfway vs quarter way)")
        st.markdown("- **1/3 vs 1/6:** 1/3 is greater (thirds are bigger pieces than sixths)")
        st.markdown("- **1/5 vs 1/10:** 1/5 is greater (fifths are bigger pieces than tenths)")
        
        st.markdown("### Remember:")
        st.markdown("- The denominator tells you how many equal parts")
        st.markdown("- More parts = smaller pieces")
        st.markdown("- Unit fractions get smaller as denominators get bigger")

def generate_new_question():
    """Generate a new unit fractions comparison question"""
    difficulty = st.session_state.fractions_difficulty
    
    # Define denominator pools based on difficulty
    if difficulty == 1:
        # Easy: Common fractions with clear differences
        denominators = [2, 3, 4, 6]
    elif difficulty == 2:
        # Medium: Include more denominators
        denominators = [2, 3, 4, 5, 6, 8, 10]
    else:
        # Hard: Include all denominators up to 12
        denominators = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    
    # Select two different denominators
    denom1, denom2 = random.sample(denominators, 2)
    
    # Create the fractions (unit fractions have numerator 1)
    fraction1 = (1, denom1)
    fraction2 = (1, denom2)
    
    # Randomly decide whether to ask for less or greater
    comparison_type = random.choice(["less", "greater"])
    
    # Store question data
    st.session_state.question_data = {
        "fraction1": fraction1,
        "fraction2": fraction2,
        "comparison_type": comparison_type,
        "correct_answer": None
    }
    
    # Determine correct answer
    value1 = fraction1[0] / fraction1[1]
    value2 = fraction2[0] / fraction2[1]
    
    if comparison_type == "less":
        st.session_state.question_data["correct_answer"] = fraction1 if value1 < value2 else fraction2
        st.session_state.current_question = "Which fraction is less?"
    else:
        st.session_state.question_data["correct_answer"] = fraction1 if value1 > value2 else fraction2
        st.session_state.current_question = "Which fraction is greater?"

def create_number_line_figure(fraction1, fraction2):
    """Create a matplotlib figure with two number lines showing the fractions"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5), facecolor='white')
    plt.subplots_adjust(hspace=0.4)  # Add space between subplots
    
    # Configure both axes
    for ax, fraction in [(ax1, fraction1), (ax2, fraction2)]:
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.5, 0.5)
        ax.set_aspect('auto')
        
        # Remove y-axis
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_yticks([])
        
        # Remove x-axis tick labels (we'll add our own fraction labels)
        ax.set_xticks([])
        ax.spines['bottom'].set_visible(False)
        
        # Draw the number line
        ax.arrow(-0.05, 0, 1.1, 0, head_width=0.1, head_length=0.02, 
                 fc='black', ec='black', linewidth=2)
        
        # Add tick marks based on the fraction's denominator
        denom = fraction[1]
        for i in range(denom + 1):
            x = i / denom
            ax.plot([x, x], [-0.1, 0.1], 'k-', linewidth=1)
            
            # Add labels - show fractions instead of decimals
            if i == 0:
                ax.text(x, -0.25, '0', ha='center', va='top', fontsize=10)
            elif i == denom:
                ax.text(x, -0.25, '1', ha='center', va='top', fontsize=10)
            else:
                # Show fraction for all intermediate values
                # Simplify fraction if possible
                from fractions import Fraction
                frac = Fraction(i, denom)
                if frac.denominator == 1:
                    label = str(frac.numerator)
                else:
                    label = f'{frac.numerator}/{frac.denominator}'
                ax.text(x, -0.25, label, ha='center', va='top', fontsize=10)
        
        # Mark the fraction position with a dot
        fraction_value = fraction[0] / fraction[1]
        if ax == ax1:
            color = '#1f77b4'
        else:
            color = '#ff7f0e'
        ax.plot(fraction_value, 0, 'o', color=color, markersize=14, 
                markeredgewidth=3, markeredgecolor='darkred', fillstyle='full')
    
    # Don't use tight_layout as we've manually adjusted spacing
    return fig

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### 📝 {st.session_state.current_question}")
    
    # Create and display the number lines
    fig = create_number_line_figure(data['fraction1'], data['fraction2'])
    st.pyplot(fig)
    plt.close()
    
    # Create answer buttons
    with st.form("answer_form", clear_on_submit=False):
        # Format fractions for display
        frac1_str = f"{data['fraction1'][0]}/{data['fraction1'][1]}"
        frac2_str = f"{data['fraction2'][0]}/{data['fraction2'][1]}"
        
        # Radio button for answer selection
        user_answer = st.radio(
            "Select your answer:",
            options=[frac1_str, frac2_str],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit", type="primary", use_container_width=True)
        
        if submit_button and user_answer:
            # Parse the selected answer back to tuple format
            parts = user_answer.split('/')
            selected_fraction = (int(parts[0]), int(parts[1]))
            st.session_state.user_answer = selected_fraction
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

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
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.question_data["correct_answer"]
    comparison_type = st.session_state.question_data["comparison_type"]
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty
        old_difficulty = st.session_state.fractions_difficulty
        st.session_state.fractions_difficulty = min(st.session_state.fractions_difficulty + 1, 3)
        
        if st.session_state.fractions_difficulty > old_difficulty:
            if st.session_state.fractions_difficulty == 3:
                st.balloons()
                st.info("🏆 **Outstanding! You've reached the advanced level!**")
            else:
                st.info("⬆️ **Level up! Moving to more challenging comparisons.**")
    else:
        correct_str = f"{correct_answer[0]}/{correct_answer[1]}"
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_str}**.")
        
        # Decrease difficulty
        old_difficulty = st.session_state.fractions_difficulty
        st.session_state.fractions_difficulty = max(st.session_state.fractions_difficulty - 1, 1)
        
        if old_difficulty > st.session_state.fractions_difficulty:
            st.warning("⬇️ **Let's practice with easier comparisons. Keep trying!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    frac1 = data["fraction1"]
    frac2 = data["fraction2"]
    comparison_type = data["comparison_type"]
    correct = data["correct_answer"]
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        # Build explanation using multiple st.markdown calls to avoid string issues
        st.markdown("### Understanding the comparison:")
        st.markdown(f"**Fractions:** {frac1[0]}/{frac1[1]} and {frac2[0]}/{frac2[1]}")
        
        st.markdown("**Decimal values:**")
        st.markdown(f"- {frac1[0]}/{frac1[1]} = {frac1[0]/frac1[1]:.3f}")
        st.markdown(f"- {frac2[0]}/{frac2[1]} = {frac2[0]/frac2[1]:.3f}")
        
        st.markdown("### Key concept:")
        st.markdown("For unit fractions (fractions with 1 in the numerator):")
        st.markdown("- **Larger denominator = Smaller fraction**")
        st.markdown("- Think of it as dividing something into more pieces - each piece gets smaller!")
        
        st.markdown("### Visual understanding:")
        st.markdown(f"- Imagine a pizza divided into {frac1[1]} slices vs {frac2[1]} slices")
        if frac1[1] < frac2[1]:
            bigger_text = "bigger"
        else:
            bigger_text = "smaller"
        st.markdown(f"- One slice from the {frac1[1]}-slice pizza is {bigger_text} than one slice from the {frac2[1]}-slice pizza")
        
        st.markdown("### On the number line:")
        st.markdown("- Fractions closer to 0 are smaller")
        st.markdown("- Fractions closer to 1 are larger")
        if comparison_type == "less":
            smaller_text = "smaller"
            closer_text = "closer to 0"
        else:
            smaller_text = "larger"
            closer_text = "closer to 1"
        st.markdown(f"- {correct[0]}/{correct[1]} is the {smaller_text} fraction because it's {closer_text}")
        
        st.markdown(f"**Therefore:** {correct[0]}/{correct[1]} is the correct answer!")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer