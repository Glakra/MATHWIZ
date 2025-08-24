import streamlit as st
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from fractions import Fraction

def run():
    """
    Main function to run the Compare Fractions with Like Denominators Using Number Lines activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/I. Fractions and mixed numbers/compare_fractions_with_like_denominators_using_number_lines.py
    """
    # Initialize session state
    if "like_fractions_nl_level" not in st.session_state:
        st.session_state.like_fractions_nl_level = 1
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
        st.session_state.selected_fraction = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > I. Fractions and mixed numbers**")
    st.title("📈 Compare Fractions with Like Denominators Using Number Lines")
    st.markdown("*Use number lines to compare fractions with the same denominator*")
    st.markdown("---")
    
    # Add custom CSS for button styling
    st.markdown("""
    <style>
    /* Style for fraction buttons */
    .stButton > button {
        min-height: 60px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        border: 2px solid #c3c7cf !important;
    }
    
    /* Selected button style */
    .stButton > button[kind="primary"] {
        background-color: #d1e7ff !important;
        border: 2px solid #0066cc !important;
        color: #0066cc !important;
    }
    
    /* Hover effect */
    .stButton > button:hover {
        transform: scale(1.02);
        transition: transform 0.2s;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Difficulty indicator
    difficulty_level = st.session_state.like_fractions_nl_level
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_text = ["Basic fractions", "Standard fractions", "Advanced fractions"][min(difficulty_level-1, 2)]
        st.markdown(f"**Current Level:** {difficulty_text}")
        progress = min(difficulty_level / 3, 1.0)
        st.progress(progress, text=difficulty_text)
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟢 Basic**")
        elif difficulty_level == 2:
            st.markdown("**🟡 Standard**")
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
        st.markdown("- **Look at the two number lines** showing fractions")
        st.markdown("- **Compare the positions** of the dots on the number lines")
        st.markdown("- **Choose which fraction is less or greater** based on the question")
        st.markdown("- Both fractions have the **same denominator** (bottom number)")
        
        st.markdown("### Key Strategy:")
        st.markdown("For fractions with the **same denominator:**")
        st.markdown("- **Just compare the numerators** (top numbers)")
        st.markdown("- **Bigger numerator = Bigger fraction**")
        st.markdown("- The dot **farther right** on the number line is the larger fraction")
        
        st.markdown("### Examples:")
        st.markdown("- **3/5 vs 1/5:** 3/5 is greater (3 > 1)")
        st.markdown("- **2/8 vs 5/8:** 2/8 is less (2 < 5)")
        st.markdown("- **4/6 vs 6/6:** 4/6 is less (4 < 6)")
        
        st.markdown("### Visual Tip:")
        st.markdown("- **Closer to 0 = Smaller fraction**")
        st.markdown("- **Closer to 1 = Larger fraction**")
        st.markdown("- When denominators are the same, it's easy!")

def generate_new_question():
    """Generate a new like denominators comparison question"""
    difficulty = st.session_state.like_fractions_nl_level
    
    # Define denominator ranges based on difficulty
    if difficulty == 1:
        # Basic: Smaller denominators
        denominators = [3, 4, 5, 6]
    elif difficulty == 2:
        # Standard: Medium denominators
        denominators = [5, 6, 8, 10]
    else:
        # Advanced: Larger denominators with closer numerators
        denominators = [8, 10, 12, 15]
    
    # Select a denominator
    denominator = random.choice(denominators)
    
    # Generate two different numerators
    if difficulty == 1:
        # Basic: Clear differences between numerators
        possible_numerators = list(range(1, denominator))
        if len(possible_numerators) >= 2:
            num1, num2 = random.sample(possible_numerators, 2)
            # Ensure reasonable difference for beginners
            while abs(num1 - num2) < 2 and len(possible_numerators) > 2:
                num1, num2 = random.sample(possible_numerators, 2)
    else:
        # Standard and Advanced: Any valid numerators
        possible_numerators = list(range(1, denominator))
        num1, num2 = random.sample(possible_numerators, 2)
    
    # Create the fractions
    fraction1 = (num1, denominator)
    fraction2 = (num2, denominator)
    
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
    if comparison_type == "less":
        st.session_state.question_data["correct_answer"] = fraction1 if num1 < num2 else fraction2
        st.session_state.current_question = "Which fraction is less?"
    else:
        st.session_state.question_data["correct_answer"] = fraction1 if num1 > num2 else fraction2
        st.session_state.current_question = "Which fraction is greater?"
    
    # Reset selection
    st.session_state.selected_fraction = None

def create_number_line_figure(fraction1, fraction2):
    """Create a matplotlib figure with two number lines showing the fractions"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5), facecolor='white')
    plt.subplots_adjust(hspace=0.4)
    
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
        
        # Draw the number line with arrows on both ends
        ax.annotate('', xy=(1.05, 0), xytext=(-0.05, 0),
                    arrowprops=dict(arrowstyle='<->', color='black', lw=2))
        
        # Add tick marks based on the fraction's denominator
        denom = fraction[1]
        numerator = fraction[0]
        
        # Determine label frequency based on denominator size
        if denom <= 6:
            label_freq = 1  # Show every fraction
        elif denom <= 10:
            label_freq = 2  # Show every other fraction
        else:
            label_freq = 3  # Show every third fraction
        
        for i in range(denom + 1):
            x = i / denom
            ax.plot([x, x], [-0.1, 0.1], 'k-', linewidth=1.5)
            
            # Add labels - show fractions WITHOUT simplifying
            if i == 0:
                ax.text(x, -0.3, '0', ha='center', va='top', fontsize=10, fontweight='bold')
            elif i == denom:
                ax.text(x, -0.3, '1', ha='center', va='top', fontsize=10, fontweight='bold')
            elif i == numerator:  # Always show the fraction being compared
                label = f'{i}/{denom}'
                ax.text(x, -0.3, label, ha='center', va='top', fontsize=9, fontweight='bold', color='red')
            elif i % label_freq == 0:  # Show other labels based on frequency
                # Show fraction WITHOUT simplifying - keep original denominator
                label = f'{i}/{denom}'
                fontsize = 8 if denom <= 10 else 7  # Smaller font for larger denominators
                ax.text(x, -0.3, label, ha='center', va='top', fontsize=fontsize)
        
        # Mark the fraction position with a colored dot
        fraction_value = fraction[0] / fraction[1]
        if ax == ax1:
            color = '#1f77b4'  # Blue (similar to reference)
        else:
            color = '#2ca02c'  # Green (similar to reference)
        
        # Draw a larger, more visible dot
        ax.plot(fraction_value, 0, 'o', color=color, markersize=12, 
                markeredgewidth=2, markeredgecolor='black', fillstyle='full')
    
    return fig

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display question
    st.markdown(f"### {st.session_state.current_question}")
    
    # Create and display the number lines
    fig = create_number_line_figure(data['fraction1'], data['fraction2'])
    st.pyplot(fig)
    plt.close()
    
    # Create fraction tiles for selection
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Use columns for side-by-side tiles
    col1, col2, col3, col4 = st.columns([1.5, 1.5, 1.5, 1.5])
    
    frac1_str = f"{data['fraction1'][0]}/{data['fraction1'][1]}"
    frac2_str = f"{data['fraction2'][0]}/{data['fraction2'][1]}"
    
    with col2:
        # First fraction tile
        if st.button(
            frac1_str,
            key="frac1_button",
            use_container_width=True,
            type="secondary" if st.session_state.selected_fraction != frac1_str else "primary",
            help=f"Click to select {frac1_str}"
        ):
            st.session_state.selected_fraction = frac1_str
            st.rerun()
    
    with col3:
        # Second fraction tile
        if st.button(
            frac2_str,
            key="frac2_button",
            use_container_width=True,
            type="secondary" if st.session_state.selected_fraction != frac2_str else "primary",
            help=f"Click to select {frac2_str}"
        ):
            st.session_state.selected_fraction = frac2_str
            st.rerun()
    
    # Show selection status
    if st.session_state.selected_fraction is None and not st.session_state.answer_submitted:
        st.info("👆 Click on a fraction to select your answer")
    elif st.session_state.selected_fraction is not None and not st.session_state.answer_submitted:
        st.success(f"✔️ You selected: **{st.session_state.selected_fraction}**")
    
    # Submit button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        submit_disabled = st.session_state.selected_fraction is None or st.session_state.answer_submitted
        if st.button("Submit", type="primary", use_container_width=True, disabled=submit_disabled):
            # Parse the selected answer back to tuple format
            parts = st.session_state.selected_fraction.split('/')
            selected_tuple = (int(parts[0]), int(parts[1]))
            st.session_state.user_answer = selected_tuple
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
            st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 2, 2])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.question_data["correct_answer"]
    comparison_type = st.session_state.question_data["comparison_type"]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Great job!**")
        
        # Quick explanation
        frac1 = st.session_state.question_data["fraction1"]
        frac2 = st.session_state.question_data["fraction2"]
        st.info(f"Since both fractions have denominator {correct_answer[1]}, we just compare {frac1[0]} and {frac2[0]}. "
                f"{correct_answer[0]}/{correct_answer[1]} is {'less' if comparison_type == 'less' else 'greater'}!")
        
        # Increase difficulty
        old_level = st.session_state.like_fractions_nl_level
        st.session_state.like_fractions_nl_level = min(st.session_state.like_fractions_nl_level + 1, 3)
        
        if st.session_state.like_fractions_nl_level > old_level:
            if st.session_state.like_fractions_nl_level == 3:
                st.balloons()
    else:
        correct_str = f"{correct_answer[0]}/{correct_answer[1]}"
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_str}**.")
        
        # Decrease difficulty
        st.session_state.like_fractions_nl_level = max(st.session_state.like_fractions_nl_level - 1, 1)
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    data = st.session_state.question_data
    frac1 = data["fraction1"]
    frac2 = data["fraction2"]
    comparison_type = data["comparison_type"]
    correct = data["correct_answer"]
    
    with st.expander("📖 **See explanation**", expanded=True):
        st.markdown(f"**Comparing:** {frac1[0]}/{frac1[1]} and {frac2[0]}/{frac2[1]}")
        
        # Key rule
        st.markdown("### The Rule:")
        st.markdown(f"When denominators are the same ({frac1[1]}), just compare numerators!")
        
        # Show the comparison
        st.markdown("### Compare the numerators:")
        st.markdown(f"- {frac1[0]}/{frac1[1]} → numerator is **{frac1[0]}**")
        st.markdown(f"- {frac2[0]}/{frac2[1]} → numerator is **{frac2[0]}**")
        
        # Which is bigger/smaller
        if frac1[0] > frac2[0]:
            st.markdown(f"Since **{frac1[0]} > {frac2[0]}**, we know **{frac1[0]}/{frac1[1]} > {frac2[0]}/{frac2[1]}**")
        else:
            st.markdown(f"Since **{frac1[0]} < {frac2[0]}**, we know **{frac1[0]}/{frac1[1]} < {frac2[0]}/{frac2[1]}**")
        
        # Number line explanation
        st.markdown("### On the number line:")
        if comparison_type == "less":
            st.markdown(f"- The smaller fraction ({correct[0]}/{correct[1]}) is **closer to 0**")
        else:
            st.markdown(f"- The larger fraction ({correct[0]}/{correct[1]}) is **closer to 1**")
        
        # Answer
        st.markdown("---")
        if comparison_type == "less":
            st.markdown(f"✓ **{correct[0]}/{correct[1]}** is the smaller fraction")
        else:
            st.markdown(f"✓ **{correct[0]}/{correct[1]}** is the larger fraction")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    st.session_state.selected_fraction = None
    if "user_answer" in st.session_state:
        del st.session_state.user_answer