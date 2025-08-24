import streamlit as st
import random
from fractions import Fraction
from math import gcd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def run():
    """
    Main function to run the Subtract Fractions with Unlike Denominators practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/J. Add and subtract fractions/subtract_fractions_with_unlike_denominators_using_models.py
    """
    # Initialize session state
    if "frac_subtract_problem" not in st.session_state:
        st.session_state.frac_subtract_problem = None
        st.session_state.frac_subtract_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > J. Add and subtract fractions**")
    st.title("➖ Subtract Fractions with Unlike Denominators Using Models")
    st.markdown("*Use visual models to subtract fractions with different denominators*")
    st.markdown("---")
    
    # Generate new problem if needed
    if st.session_state.frac_subtract_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Subtract Fractions with Unlike Denominators:
        
        **Step 1:** Look at the visual models
        - The top row shows the first fraction as individual blocks
        - The bottom bar shows the fraction being subtracted
        
        **Step 2:** Find a common denominator
        - Think: What number do both denominators divide into evenly?
        - The visual model helps you see equivalent fractions
        
        **Step 3:** Convert to equivalent fractions
        - Make both fractions have the same denominator
        - Count how many pieces remain after subtraction
        
        ### Example:
        **4/6 - 1/2 = ?**
        - Common denominator: 6
        - 1/2 = 3/6 (the bar shows this visually)
        - 4/6 - 3/6 = 1/6
        
        ### Tips:
        - 🔍 Use the visual model to understand the fractions
        - 🎯 Find the least common denominator (LCD)
        - ✅ Always simplify your final answer
        - 📊 Check if your answer makes sense visually
        """)

def generate_new_problem():
    """Generate a new fraction subtraction problem with unlike denominators"""
    # Common denominators that work well visually
    denominators = [2, 3, 4, 5, 6, 8, 10, 12]
    
    # Generate two fractions where first > second
    while True:
        denom1 = random.choice(denominators)
        denom2 = random.choice([d for d in denominators if d != denom1])
        
        # Ensure different denominators
        if denom1 == denom2:
            continue
            
        # Generate numerators
        num1 = random.randint(1, denom1 - 1)
        num2 = random.randint(1, denom2 - 1)
        
        # Create fractions
        frac1 = Fraction(num1, denom1)
        frac2 = Fraction(num2, denom2)
        
        # Ensure first fraction is larger and result is positive
        if frac1 > frac2:
            result = frac1 - frac2
            if result.numerator > 0:  # Ensure positive result
                break
    
    st.session_state.frac_subtract_problem = {
        "frac1": frac1,
        "frac2": frac2,
        "num1": num1,
        "denom1": denom1,
        "num2": num2,
        "denom2": denom2,
        "result": result
    }
    st.session_state.frac_subtract_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def create_fraction_blocks(numerator, denominator):
    """Create a visual representation of fraction blocks"""
    fig, ax = plt.subplots(1, 1, figsize=(8, 2))
    ax.set_xlim(0, numerator * 1.2)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Create individual blocks
    for i in range(numerator):
        rect = patches.Rectangle((i * 1.1, 0.2), 1, 0.6, 
                                linewidth=2, edgecolor='black', 
                                facecolor='#5DD5D5')
        ax.add_patch(rect)
        ax.text(i * 1.1 + 0.5, 0.5, f'1/{denominator}', 
                ha='center', va='center', fontsize=12, weight='bold')
    
    return fig

def create_fraction_bar(numerator, denominator):
    """Create a bar representation of a fraction"""
    fig, ax = plt.subplots(1, 1, figsize=(8, 2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Background bar
    bg_rect = patches.Rectangle((0, 0.3), 1, 0.4, 
                               linewidth=2, edgecolor='black', 
                               facecolor='#f0f0f0')
    ax.add_patch(bg_rect)
    
    # Filled portion
    fill_width = numerator / denominator
    fill_rect = patches.Rectangle((0, 0.3), fill_width, 0.4, 
                                 linewidth=2, edgecolor='black', 
                                 facecolor='#FF69B4')
    ax.add_patch(fill_rect)
    
    # Add dividing lines
    for i in range(1, denominator):
        x_pos = i / denominator
        ax.plot([x_pos, x_pos], [0.3, 0.7], 'k--', linewidth=1)
    
    # Add fraction label
    ax.text(fill_width/2, 0.5, f'{numerator}/{denominator}', 
            ha='center', va='center', fontsize=14, weight='bold', color='white')
    
    return fig

def display_problem():
    """Display the current fraction subtraction problem"""
    problem = st.session_state.frac_subtract_problem
    
    # Display the problem
    st.markdown("### 📝 Subtract:")
    
    col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1, 0.5, 1])
    with col1:
        st.markdown(f"### {problem['num1']}/{problem['denom1']}")
    with col2:
        st.markdown("### −")
    with col3:
        st.markdown(f"### {problem['num2']}/{problem['denom2']}")
    with col4:
        st.markdown("### =")
    with col5:
        st.markdown("### ?")
    
    # Display visual model
    st.markdown("### 📊 Use the model to help you:")
    
    # First fraction as blocks
    st.markdown("**First fraction:**")
    fig1 = create_fraction_blocks(problem['num1'], problem['denom1'])
    st.pyplot(fig1)
    plt.close(fig1)
    
    # Minus sign
    st.markdown("**Subtract:**")
    
    # Second fraction as bar
    fig2 = create_fraction_bar(problem['num2'], problem['denom2'])
    st.pyplot(fig2)
    plt.close(fig2)
    
    # Divider line
    st.markdown("---")
    
    # Answer input
    with st.form("answer_form", clear_on_submit=False):
        st.markdown("**Enter your answer:**")
        
        col1, col2, col3 = st.columns([1, 0.2, 1])
        with col1:
            numerator = st.number_input("Numerator:", min_value=0, max_value=100, step=1, key="num_input")
        with col2:
            st.markdown("<div style='text-align: center; font-size: 24px; margin-top: 25px;'>—</div>", unsafe_allow_html=True)
        with col3:
            denominator = st.number_input("Denominator:", min_value=1, max_value=100, step=1, key="denom_input")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
        
        if submit_button:
            if denominator > 0:  # Valid denominator
                user_answer = Fraction(numerator, denominator)
                st.session_state.frac_subtract_answer = user_answer
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                st.rerun()
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next problem button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Problem", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    problem = st.session_state.frac_subtract_problem
    user_answer = st.session_state.frac_subtract_answer
    correct_answer = problem['result']
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        st.balloons()
        
        # Show the work
        with st.expander("✅ **See the solution**", expanded=True):
            show_solution(problem)
    else:
        st.error(f"❌ **Not quite right.** The correct answer is **{correct_answer}**")
        
        # Show detailed explanation
        with st.expander("📖 **Click here for step-by-step solution**", expanded=True):
            show_solution(problem)
            
            # Additional feedback on common mistakes
            if user_answer.denominator != correct_answer.denominator:
                st.warning("💡 **Tip:** Make sure to simplify your answer to lowest terms!")
            
            # Check if they forgot to find common denominator
            if user_answer == Fraction(problem['num1'] - problem['num2'], problem['denom1']):
                st.warning("⚠️ **Remember:** You can't subtract fractions with different denominators directly. Find a common denominator first!")

def show_solution(problem):
    """Show step-by-step solution"""
    frac1 = problem['frac1']
    frac2 = problem['frac2']
    result = problem['result']
    
    # Find LCD
    lcd = abs(frac1.denominator * frac2.denominator) // gcd(frac1.denominator, frac2.denominator)
    
    st.markdown(f"""
    ### Step-by-step solution:
    
    **1. Original problem:**
    {frac1} − {frac2} = ?
    
    **2. Find the least common denominator (LCD):**
    - Denominators: {frac1.denominator} and {frac2.denominator}
    - LCD = {lcd}
    
    **3. Convert to equivalent fractions:**
    - {frac1} = {frac1.numerator * (lcd // frac1.denominator)}/{lcd}
    - {frac2} = {frac2.numerator * (lcd // frac2.denominator)}/{lcd}
    
    **4. Subtract the fractions:**
    {frac1.numerator * (lcd // frac1.denominator)}/{lcd} − {frac2.numerator * (lcd // frac2.denominator)}/{lcd} = {(frac1.numerator * (lcd // frac1.denominator)) - (frac2.numerator * (lcd // frac2.denominator))}/{lcd}
    
    **5. Simplify if needed:**
    {(frac1.numerator * (lcd // frac1.denominator)) - (frac2.numerator * (lcd // frac2.denominator))}/{lcd} = **{result}**
    """)
    
    # Visual representation of the solution
    st.markdown("### Visual representation:")
    
    # Show equivalent fractions visually
    equiv1_blocks = (frac1.numerator * (lcd // frac1.denominator))
    equiv2_blocks = (frac2.numerator * (lcd // frac2.denominator))
    
    st.markdown(f"**{frac1} = {equiv1_blocks}/{lcd}** (shown as {equiv1_blocks} blocks of 1/{lcd})")
    fig3 = create_fraction_blocks(equiv1_blocks, lcd)
    st.pyplot(fig3)
    plt.close(fig3)
    
    st.markdown(f"**{frac2} = {equiv2_blocks}/{lcd}** (taking away {equiv2_blocks} blocks)")
    fig4 = create_fraction_bar(equiv2_blocks, lcd)
    st.pyplot(fig4)
    plt.close(fig4)
    
    st.markdown(f"**Result: {equiv1_blocks - equiv2_blocks} blocks of 1/{lcd} = {result}**")

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.frac_subtract_problem = None
    st.session_state.frac_subtract_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False