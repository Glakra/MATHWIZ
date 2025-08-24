import streamlit as st
import random
from fractions import Fraction

def run():
    """
    Main function to run the Put Fractions in Order activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A.Place values and number sense/put_fractions_in_order.py
    """
    # Initialize session state
    if "order_fractions_score" not in st.session_state:
        st.session_state.order_fractions_score = 0
        st.session_state.order_fractions_attempts = 0
        st.session_state.difficulty_level = 1  # Start with easier problems
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.selected_order = []  # Track the order of selection
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📊 Put Fractions in Order")
    st.markdown("*Arrange fractions from smallest to largest or largest to smallest*")
    st.markdown("---")
    
    # Score and difficulty display
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.session_state.order_fractions_attempts > 0:
            accuracy = (st.session_state.order_fractions_score / st.session_state.order_fractions_attempts) * 100
            st.metric("Score", f"{st.session_state.order_fractions_score}/{st.session_state.order_fractions_attempts}", 
                     f"{accuracy:.0f}%")
        else:
            st.metric("Score", "0/0", "Start practicing!")
    
    with col2:
        difficulty_names = {1: "🟢 Easy", 2: "🟡 Medium", 3: "🔴 Hard"}
        st.metric("Difficulty", difficulty_names[st.session_state.difficulty_level])
    
    with col3:
        # Back button
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_problem is None:
        generate_new_problem()
    
    # Display current problem
    display_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Read the instruction** - Order from smallest to largest OR largest to smallest
        - **Click fractions in order** - Start with the first one (smallest or largest)
        - **Continue selecting** - Pick the next fraction in the sequence
        - **Use Reset** if you want to start over
        - **Submit** when all fractions are selected
        
        ### Strategies for Ordering Fractions:
        
        **1. Same Denominators:**
        - Just compare the numerators
        - Example: 1/8 < 3/8 < 5/8 < 7/8
        
        **2. Same Numerators:**
        - Smaller denominator = larger fraction
        - Example: 1/2 > 1/3 > 1/4 > 1/5
        
        **3. Mixed Denominators:**
        - Find common denominators
        - Convert all fractions to the same denominator
        - Then compare numerators
        
        **4. Cross Multiplication:**
        - Compare pairs of fractions
        - For a/b vs c/d: compare a×d with b×c
        
        **5. Benchmark Strategy:**
        - Group by benchmarks: near 0, near 1/2, near 1
        - Compare within each group
        
        ### Quick Tips:
        - **Unit fractions:** 1/2 > 1/3 > 1/4 > 1/5...
        - **Near 0:** 1/10, 1/8, 1/6 (smaller fractions)
        - **Near 1/2:** 2/5, 3/7, 4/9 (middle fractions)
        - **Near 1:** 3/4, 5/6, 7/8 (larger fractions)
        
        ### Difficulty Levels:
        - **🟢 Easy:** Same denominators or simple comparisons
        - **🟡 Medium:** Mixed denominators, need conversions
        - **🔴 Hard:** Complex fractions, multiple strategies needed
        """)

def generate_new_problem():
    """Generate a new fraction ordering problem based on difficulty level"""
    
    difficulty = st.session_state.difficulty_level
    
    if difficulty == 1:  # Easy - same denominators or unit fractions
        problem_types = [
            # Same denominator problems
            {"fractions": [(2, 8), (5, 8), (1, 8), (7, 8)], "type": "same_denominator"},
            {"fractions": [(3, 10), (7, 10), (1, 10), (9, 10)], "type": "same_denominator"},
            {"fractions": [(4, 12), (11, 12), (7, 12), (2, 12)], "type": "same_denominator"},
            {"fractions": [(1, 6), (5, 6), (2, 6), (4, 6)], "type": "same_denominator"},
            # Unit fractions
            {"fractions": [(1, 2), (1, 5), (1, 3), (1, 8)], "type": "unit_fractions"},
            {"fractions": [(1, 4), (1, 7), (1, 3), (1, 10)], "type": "unit_fractions"},
            # Same numerators
            {"fractions": [(3, 4), (3, 8), (3, 5), (3, 10)], "type": "same_numerator"},
            {"fractions": [(2, 3), (2, 7), (2, 5), (2, 9)], "type": "same_numerator"},
        ]
    elif difficulty == 2:  # Medium - mixed but simpler
        problem_types = [
            {"fractions": [(1, 2), (3, 4), (1, 4), (5, 8)], "type": "mixed"},
            {"fractions": [(2, 3), (1, 2), (3, 6), (5, 6)], "type": "mixed"},
            {"fractions": [(3, 5), (1, 2), (7, 10), (2, 5)], "type": "mixed"},
            {"fractions": [(1, 3), (2, 6), (5, 6), (1, 2)], "type": "mixed"},
            {"fractions": [(3, 8), (1, 2), (5, 8), (1, 4)], "type": "mixed"},
            {"fractions": [(2, 5), (3, 10), (1, 2), (7, 10)], "type": "mixed"},
            {"fractions": [(1, 4), (3, 12), (5, 12), (2, 3)], "type": "mixed"},
            {"fractions": [(4, 5), (2, 3), (1, 2), (3, 10)], "type": "mixed"},
        ]
    else:  # difficulty == 3, Hard - complex mixed fractions
        problem_types = [
            {"fractions": [(5, 7), (3, 4), (2, 3), (7, 9)], "type": "complex"},
            {"fractions": [(4, 9), (3, 7), (5, 11), (2, 5)], "type": "complex"},
            {"fractions": [(7, 12), (5, 8), (3, 5), (11, 20)], "type": "complex"},
            {"fractions": [(5, 6), (7, 9), (4, 5), (11, 15)], "type": "complex"},
            {"fractions": [(3, 8), (5, 12), (7, 18), (4, 9)], "type": "complex"},
            {"fractions": [(8, 15), (7, 12), (9, 20), (11, 18)], "type": "complex"},
            {"fractions": [(4, 7), (5, 9), (7, 13), (3, 5)], "type": "complex"},
            {"fractions": [(9, 14), (5, 8), (7, 11), (4, 7)], "type": "complex"},
        ]
    
    # Select a random problem
    problem = random.choice(problem_types)
    fractions = problem["fractions"].copy()
    
    # Randomly decide ordering direction
    order_type = random.choice(["smallest to largest", "largest to smallest"])
    
    # Shuffle the fractions for display
    display_fractions = fractions.copy()
    random.shuffle(display_fractions)
    
    # Calculate correct order
    sorted_fractions = sorted(fractions, key=lambda x: Fraction(x[0], x[1]))
    if order_type == "largest to smallest":
        sorted_fractions.reverse()
    
    st.session_state.current_problem = {
        "fractions": display_fractions,
        "order_type": order_type,
        "correct_order": sorted_fractions,
        "problem_type": problem["type"]
    }
    st.session_state.selected_order = []
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False

def display_problem():
    """Display the current fraction ordering problem"""
    
    problem = st.session_state.current_problem
    
    # Display instruction
    st.markdown(f"### Put these fractions in order from **{problem['order_type']}**.")
    
    # Show selection progress
    selected_count = len(st.session_state.selected_order)
    if selected_count == 0:
        if problem['order_type'] == "smallest to largest":
            st.info("👆 Click on the **smallest** fraction first")
        else:
            st.info("👆 Click on the **largest** fraction first")
    elif selected_count < 4:
        st.info(f"👆 Now click on the **next** fraction in order ({selected_count}/4 selected)")
    else:
        st.success("✅ All fractions selected! Click Submit to check your answer")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display fractions as clickable tiles
    display_fraction_tiles()
    
    # Show selected order
    if st.session_state.selected_order:
        st.markdown("### Your order:")
        selected_str = " → ".join([f"{f[0]}/{f[1]}" for f in st.session_state.selected_order])
        st.markdown(f"**{selected_str}**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Reset button
        if st.button("🔄 Reset", type="secondary", use_container_width=True,
                    disabled=st.session_state.answer_submitted):
            st.session_state.selected_order = []
            st.rerun()
    
    with col2:
        # Submit button - only enabled when all fractions are selected
        submit_disabled = len(st.session_state.selected_order) < 4 or st.session_state.answer_submitted
        if st.button("✅ Submit", type="primary", use_container_width=True, 
                    disabled=submit_disabled):
            check_answer()
    
    # Show feedback
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                st.session_state.current_problem = None
                st.rerun()

def display_fraction_tiles():
    """Display fractions as clickable tiles"""
    
    problem = st.session_state.current_problem
    fractions = problem['fractions']
    selected = st.session_state.selected_order
    
    # Create 4 columns for the fractions
    cols = st.columns(4)
    
    for i, frac in enumerate(fractions):
        with cols[i]:
            # Check if this fraction is already selected
            is_selected = frac in selected
            
            # Determine the order number if selected
            order_number = ""
            if is_selected:
                order_number = str(selected.index(frac) + 1)
            
            # Create button with appropriate styling
            if is_selected:
                # Show as selected (disabled) with order number
                st.markdown(
                    f"""
                    <div style="
                        background-color: #4CAF50;
                        color: white;
                        padding: 20px;
                        border-radius: 8px;
                        text-align: center;
                        font-size: 24px;
                        font-weight: bold;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                        position: relative;
                        opacity: 0.7;
                    ">
                        <div style="
                            position: absolute;
                            top: -10px;
                            right: -10px;
                            background-color: #FF5722;
                            color: white;
                            border-radius: 50%;
                            width: 30px;
                            height: 30px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 16px;
                            font-weight: bold;
                        ">{order_number}</div>
                        {frac[0]}/{frac[1]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # Show as clickable if not submitted
                if not st.session_state.answer_submitted and len(selected) < 4:
                    if st.button(f"{frac[0]}/{frac[1]}", key=f"frac_{i}", 
                               use_container_width=True,
                               type="primary"):
                        st.session_state.selected_order.append(frac)
                        st.rerun()
                else:
                    # Show as disabled
                    st.markdown(
                        f"""
                        <div style="
                            background-color: #2196F3;
                            color: white;
                            padding: 20px;
                            border-radius: 8px;
                            text-align: center;
                            font-size: 24px;
                            font-weight: bold;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                            opacity: 0.5;
                        ">
                            {frac[0]}/{frac[1]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

def check_answer():
    """Check if the fraction order is correct"""
    
    problem = st.session_state.current_problem
    user_order = st.session_state.selected_order
    correct_order = problem['correct_order']
    
    st.session_state.answer_submitted = True
    st.session_state.order_fractions_attempts += 1
    
    # Check if user's order matches correct order
    is_correct = user_order == correct_order
    
    if is_correct:
        st.session_state.order_fractions_score += 1
        # Increase difficulty on success
        if st.session_state.difficulty_level < 3:
            st.session_state.difficulty_level += 1
    else:
        # Decrease difficulty on failure
        if st.session_state.difficulty_level > 1:
            st.session_state.difficulty_level -= 1
    
    st.session_state.show_feedback = True

def show_feedback():
    """Display feedback for the submitted answer"""
    
    problem = st.session_state.current_problem
    user_order = st.session_state.selected_order
    correct_order = problem['correct_order']
    
    is_correct = user_order == correct_order
    
    if is_correct:
        st.success("🎉 **Correct! Well done!**")
        
        # Show explanation based on problem type
        if problem['problem_type'] == 'same_denominator':
            st.info("💡 **Tip:** When denominators are the same, just compare the numerators!")
        elif problem['problem_type'] == 'unit_fractions':
            st.info("💡 **Tip:** For unit fractions (1/n), smaller denominator means larger fraction!")
        elif problem['problem_type'] == 'same_numerator':
            st.info("💡 **Tip:** When numerators are the same, smaller denominator means larger fraction!")
        else:
            st.info("💡 **Great job comparing mixed fractions!**")
        
        # Celebration for streaks
        if st.session_state.order_fractions_score % 5 == 0:
            st.balloons()
    else:
        st.error("❌ **Not quite right. Let's see the correct order:**")
        
        # Show correct order
        correct_order_str = " → ".join([f"{f[0]}/{f[1]}" for f in correct_order])
        st.info(f"**Correct order ({problem['order_type']}):**\n{correct_order_str}")
        
        # Show user's order for comparison
        user_order_str = " → ".join([f"{f[0]}/{f[1]}" for f in user_order])
        st.warning(f"**Your order:**\n{user_order_str}")
        
        # Provide specific feedback
        with st.expander("📚 **Learn from this problem**", expanded=True):
            st.markdown("### Let's compare these fractions step by step:")
            
            # Convert all fractions to common denominator or decimals
            st.markdown("**As decimals:**")
            for frac in correct_order:
                decimal = frac[0] / frac[1]
                st.markdown(f"- {frac[0]}/{frac[1]} = {decimal:.3f}")
            
            # Show comparison strategy
            if problem['problem_type'] == 'same_denominator':
                st.markdown("\n**Strategy:** Since all denominators are the same, compare numerators directly.")
            elif problem['problem_type'] == 'unit_fractions':
                st.markdown("\n**Strategy:** For unit fractions, remember: 1/2 > 1/3 > 1/4...")
            elif problem['problem_type'] == 'same_numerator':
                st.markdown("\n**Strategy:** When numerators are the same, smaller denominator = larger fraction.")
            else:
                st.markdown("\n**Strategy:** Convert to common denominators or decimals to compare.")