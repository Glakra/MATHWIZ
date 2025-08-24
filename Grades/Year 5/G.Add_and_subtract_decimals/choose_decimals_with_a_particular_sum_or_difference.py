import streamlit as st
import random

def run():
    """
    Main function to run the Choose decimals with a particular sum or difference activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/B. Addition and subtraction/choose_decimals_with_a_particular_sum_or_difference.py
    """
    # Initialize session state
    if "decimals_sum_diff_scenario" not in st.session_state:
        st.session_state.decimals_sum_diff_scenario = None
        st.session_state.decimals_answer_submitted = False
        st.session_state.selected_num1 = None
        st.session_state.selected_num2 = None
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > B. Addition and subtraction**")
    st.title("🎯 Choose Decimals with a Particular Sum or Difference")
    st.markdown("*Select two numbers that add to a target sum or have a target difference*")
    st.markdown("---")
    
    # Back button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new scenario if needed
    if st.session_state.decimals_sum_diff_scenario is None:
        st.session_state.decimals_sum_diff_scenario = generate_scenario()
        st.session_state.decimals_answer_submitted = False
    
    scenario = st.session_state.decimals_sum_diff_scenario
    
    # Display the question
    st.markdown(f"### 📝 {scenario['question']}")
    
    # Display the number box
    st.markdown("""
    <div style="
        background-color: #e3f2fd; 
        border: 2px solid #2196f3; 
        border-radius: 8px; 
        padding: 20px; 
        margin: 20px 0;
        text-align: center;
    ">
    """, unsafe_allow_html=True)
    
    # Create columns for the numbers
    cols = st.columns(4)
    for i, num in enumerate(scenario['numbers']):
        with cols[i]:
            st.markdown(f"""
            <div style="
                background-color: white; 
                border: 1px solid #90caf9;
                border-radius: 4px;
                padding: 12px;
                font-size: 20px;
                font-weight: bold;
                color: #1976d2;
                text-align: center;
            ">
                {num}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Create the sentence with dropdowns
    st.markdown("### Complete the sentence:")
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col1:
        num1 = st.selectbox(
            "First number",
            options=[''] + scenario['numbers'],
            key="dropdown1",
            label_visibility="collapsed",
            disabled=st.session_state.decimals_answer_submitted
        )
    
    if scenario['type'] == 'sum':
        with col2:
            st.markdown("<div style='text-align: center; padding-top: 5px;'>+</div>", unsafe_allow_html=True)
        with col3:
            num2 = st.selectbox(
                "Second number",
                options=[''] + scenario['numbers'],
                key="dropdown2",
                label_visibility="collapsed",
                disabled=st.session_state.decimals_answer_submitted
            )
        with col4:
            st.markdown(f"<div style='padding-top: 5px;'>= {scenario['target']}</div>", unsafe_allow_html=True)
    else:  # difference
        with col2:
            st.markdown("<div style='text-align: center; padding-top: 5px;'>and</div>", unsafe_allow_html=True)
        with col3:
            num2 = st.selectbox(
                "Second number",
                options=[''] + scenario['numbers'],
                key="dropdown2",
                label_visibility="collapsed",
                disabled=st.session_state.decimals_answer_submitted
            )
        with col4:
            st.markdown(f"<div style='padding-top: 5px;'>have a difference of {scenario['target']}.</div>", 
                       unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Submit Answer", type="primary", use_container_width=True,
                     disabled=st.session_state.decimals_answer_submitted):
            
            # Validate selection
            if num1 == '' or num2 == '':
                st.warning("⚠️ Please select two numbers.")
            elif num1 == num2:
                st.warning("⚠️ Please select two different numbers.")
            else:
                st.session_state.decimals_answer_submitted = True
                st.session_state.selected_num1 = num1
                st.session_state.selected_num2 = num2
                st.rerun()
    
    # Show feedback if answer was submitted
    if st.session_state.decimals_answer_submitted:
        show_feedback()
    
    # Next question button
    if st.session_state.decimals_answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                # Reset state for new question
                st.session_state.decimals_sum_diff_scenario = None
                st.session_state.decimals_answer_submitted = False
                st.session_state.selected_num1 = None
                st.session_state.selected_num2 = None
                st.rerun()
    
    # Instructions
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Look at the numbers** in the blue box
        - **Choose two numbers** that work together
        - **For addition:** Find two numbers that add up to the target
        - **For difference:** Find two numbers whose difference equals the target
        
        ### Tips for Success:
        - **Try different combinations** - there's only one correct pair
        - **For difference problems:** Remember it's the larger minus the smaller
        - **Check your math:** Add or subtract to verify your choice
        
        ### Examples:
        - **Addition:** If target is 6.5, you might need 3.3 + 3.2
        - **Difference:** If target is 0.6, you might need 8.7 - 8.1
        
        ### Remember:
        - Each number can only be used once
        - You must choose two different numbers
        - Work carefully with decimals!
        """)

def generate_scenario():
    """Generate a random sum or difference problem"""
    problem_type = random.choice(['sum', 'difference'])
    
    if problem_type == 'sum':
        # Generate a target sum between 3.0 and 12.0
        target = round(random.uniform(3.0, 12.0), 1)
        
        # Generate two correct numbers that sum to target
        num1 = round(random.uniform(0.5, target - 0.5), 1)
        num2 = round(target - num1, 1)
        
        # Generate distractors
        distractors = []
        while len(distractors) < 2:
            # Create numbers that are close but don't work
            d = round(random.uniform(0.1, target), 1)
            if d not in [num1, num2] and d not in distractors:
                # Check this doesn't accidentally work with another number
                works = False
                for existing in [num1, num2] + distractors:
                    if abs((d + existing) - target) < 0.01:
                        works = True
                        break
                if not works:
                    distractors.append(d)
        
        numbers = [num1, num2] + distractors
        random.shuffle(numbers)
        
        return {
            'type': 'sum',
            'numbers': numbers,
            'target': target,
            'correct_pair': sorted([num1, num2]),
            'question': 'Choose two numbers from the box to complete the addition number sentence.',
            'template': '__ + __ = {:.1f}'.format(target)
        }
    
    else:  # difference
        # Generate a target difference between 0.3 and 5.0
        target = round(random.uniform(0.3, 5.0), 1)
        
        # Generate two correct numbers with this difference
        smaller = round(random.uniform(0.1, 8.0), 1)
        larger = round(smaller + target, 1)
        
        # Generate distractors
        distractors = []
        while len(distractors) < 2:
            d = round(random.uniform(0.1, 10.0), 1)
            if d not in [smaller, larger] and d not in distractors:
                # Check this doesn't accidentally work
                works = False
                for existing in [smaller, larger] + distractors:
                    if abs(abs(d - existing) - target) < 0.01:
                        works = True
                        break
                if not works:
                    distractors.append(d)
        
        numbers = [smaller, larger] + distractors
        random.shuffle(numbers)
        
        return {
            'type': 'difference',
            'numbers': numbers,
            'target': target,
            'correct_pair': sorted([smaller, larger]),
            'question': 'Choose two numbers from the box to complete the sentence.',
            'template': '__ and __ have a difference of {:.1f}.'.format(target)
        }

def show_feedback():
    """Display feedback for the submitted answer"""
    scenario = st.session_state.decimals_sum_diff_scenario
    num1 = st.session_state.selected_num1
    num2 = st.session_state.selected_num2
    
    # Check if answer is correct
    correct = False
    
    if scenario['type'] == 'sum':
        if abs((num1 + num2) - scenario['target']) < 0.01:
            correct = True
    else:  # difference
        if abs(abs(num1 - num2) - scenario['target']) < 0.01:
            correct = True
    
    if correct:
        st.success("🎉 **Correct! Well done!**")
        
        if scenario['type'] == 'sum':
            st.info(f"✓ {num1} + {num2} = {scenario['target']}")
        else:
            st.info(f"✓ {max(num1, num2)} - {min(num1, num2)} = {scenario['target']}")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show what they calculated
        if scenario['type'] == 'sum':
            actual = round(num1 + num2, 1)
            st.warning(f"Your answer: {num1} + {num2} = {actual}")
            st.info(f"We need a sum of {scenario['target']}")
        else:
            actual = round(abs(num1 - num2), 1)
            st.warning(f"Your answer: The difference between {num1} and {num2} is {actual}")
            st.info(f"We need a difference of {scenario['target']}")
        
        # Show correct answer
        correct_nums = scenario['correct_pair']
        if scenario['type'] == 'sum':
            st.success(f"Correct answer: {correct_nums[0]} + {correct_nums[1]} = {scenario['target']}")
        else:
            st.success(f"Correct answer: {correct_nums[1]} - {correct_nums[0]} = {scenario['target']}")