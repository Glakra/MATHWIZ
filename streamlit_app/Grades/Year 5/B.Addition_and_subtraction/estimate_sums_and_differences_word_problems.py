import streamlit as st
import random

def run():
    """
    Main function to run the Estimate Word Problems practice activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/B. Addition and subtraction/estimate_sums_and_differences_word_problems.py
    """
    # Initialize session state
    if "estimate_word_diff_difficulty" not in st.session_state:
        st.session_state.estimate_word_diff_difficulty = {"round_to": 100000}
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.problem_data = {}
        st.session_state.question_count = 0
        st.session_state.correct_count = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > B. Addition and subtraction**")
    st.title("📝 Estimate: Word Problems")
    st.markdown("*Practice estimation with real-world scenarios*")
    st.markdown("---")
    
    # Progress indicator
    round_to = st.session_state.estimate_word_diff_difficulty["round_to"]
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Rounding to:** Nearest {round_to:,}")
        if st.session_state.question_count > 0:
            accuracy = (st.session_state.correct_count / st.session_state.question_count) * 100
            st.markdown(f"**Score:** {st.session_state.correct_count}/{st.session_state.question_count} ({accuracy:.0f}%)")
        else:
            st.markdown("**Score:** Starting...")
    
    with col2:
        if round_to >= 100000:
            st.markdown("**🔴 Advanced**")
        elif round_to >= 10000:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🟡 Beginner**")
    
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
    with st.expander("💡 **Learn About Estimation in Word Problems**", expanded=False):
        st.markdown("""
        ### 🌍 Real-World Estimation
        
        **Estimation** helps us solve real-world problems quickly! We don't always need exact answers - sometimes a good approximation is perfect for making decisions.
        
        ### 📚 **Why Estimate in Word Problems?**
        - **Quick decisions:** Get answers fast for planning and choices
        - **Check reasonableness:** See if exact calculations make sense  
        - **Practical thinking:** Most real situations don't need perfect precision
        - **Mental math:** Calculate without calculators or paper
        
        ### 🎯 **Types of Estimation Problems:**
        
        #### **Addition Estimation:**
        - **Scenario:** Combining totals from different groups
        - **Examples:** 
          - Conference attendees from different countries
          - Animals counted in different regions
          - People arriving at different times
        - **Strategy:** Round both numbers, then add
        
        #### **Subtraction Estimation:**
        - **Scenario:** Finding the remaining amount or difference
        - **Examples:**
          - How many items are left after some are sold
          - How many are a different type from the total
          - How many people didn't participate
        - **Strategy:** Round both numbers, then subtract
        
        ### 🧮 **Steps for Word Problem Estimation:**
        
        1. **Read carefully:** What is the problem asking?
        2. **Identify the operation:** Do I add or subtract?
        3. **Find the numbers:** What are the important quantities?
        4. **Round the numbers:** To the specified place value
        5. **Calculate:** Perform the operation with rounded numbers
        6. **Check reasonableness:** Does the answer make sense?
        
        ### 💭 **Example Walkthrough:**
        
        **Problem:** "A factory produced 347,821 toys. Out of those, 189,456 were dolls and the rest were action figures. Estimate how many were action figures."
        
        **Step 1:** Understand the problem
        - Total toys = 347,821
        - Dolls = 189,456  
        - Need to find: Action figures = Total - Dolls
        
        **Step 2:** Round to nearest 100,000
        - 347,821 → 300,000
        - 189,456 → 200,000
        
        **Step 3:** Calculate
        - 300,000 - 200,000 = 100,000
        
        **Step 4:** Check reasonableness
        - About 1/3 of toys were dolls, so about 2/3 were action figures
        - 100,000 seems reasonable!
        
        ### 🎯 **Tips for Success:**
        
        **Reading Strategies:**
        - **Identify key numbers:** Look for quantities that need to be calculated
        - **Understand the scenario:** What's really happening in the story?
        - **Find the question:** What exactly is being asked?
        
        **Mathematical Strategies:**
        - **Round consistently:** Use the same place value for all numbers
        - **Choose operations wisely:** Addition for combining, subtraction for finding differences
        - **Estimate first:** Make a rough guess before calculating
        
        **Checking Strategies:**
        - **Compare to originals:** Is your estimate in the right ballpark?
        - **Use common sense:** Does the answer fit the real-world scenario?
        - **Think proportionally:** If half the items are one type, the estimate should reflect that
        
        ### 🌟 **Real-World Applications:**
        
        - **Business:** Estimating profits, costs, and sales
        - **Events:** Planning for attendees, food, and supplies  
        - **Sports:** Estimating scores, statistics, and attendance
        - **Travel:** Estimating distances, times, and costs
        - **Shopping:** Estimating total bills and budgets
        - **Science:** Making quick calculations in experiments
        
        ### 🔍 **Common Scenarios You'll See:**
        
        - **Technology:** Phone sales, app downloads, user registrations
        - **Events:** Conference attendees, festival visitors, concert goers
        - **Nature:** Animal populations, environmental data
        - **Manufacturing:** Product quantities, sales figures
        - **Education:** Student numbers, test scores, participation
        - **Entertainment:** Book sales, movie tickets, game players
        """)

def generate_new_question():
    """Generate a new estimation word problem"""
    
    # Define scenario pool
    scenarios = [
        {
            "text": "A high tech company just came out with a new mobile phone. A total of {total:,} customers bought them worldwide. Of those, {part:,} customers bought black phones and the rest bought white. About how many customers bought white phones?",
            "type": "subtraction"
        },
        {
            "text": "A large company is hosting a conference. So far, {a:,} attendees from Australia have registered, as well as {b:,} attendees from other countries. About how many total attendees have registered?",
            "type": "addition"
        },
        {
            "text": "A wildlife charity counted {a:,} penguins in one region and {b:,} in another. What is a good estimate of the total number of penguins?",
            "type": "addition"
        },
        {
            "text": "A factory produced {total:,} toys. Out of those, {part:,} were dolls and the rest were action figures. Estimate how many were action figures.",
            "type": "subtraction"
        },
        {
            "text": "During a festival, {a:,} people came in the morning and {b:,} came in the afternoon. Estimate the total number of people who attended.",
            "type": "addition"
        },
        {
            "text": "A bookstore sold {total:,} books. {part:,} of them were fiction. Estimate how many were non-fiction.",
            "type": "subtraction"
        },
        {
            "text": "An online streaming service gained {a:,} new subscribers in January and {b:,} new subscribers in February. About how many new subscribers did they gain in total?",
            "type": "addition"
        },
        {
            "text": "A sports stadium sold {total:,} tickets for a big game. {part:,} tickets were for the home team section and the rest were for visiting fans. About how many tickets were for visiting fans?",
            "type": "subtraction"
        },
        {
            "text": "A charity raised {a:,} dollars in donations and {b:,} dollars from a fundraising event. Estimate the total amount raised.",
            "type": "addition"
        },
        {
            "text": "A school district has {total:,} students. {part:,} are in elementary school and the rest are in middle and high school. About how many are in middle and high school?",
            "type": "subtraction"
        }
    ]
    
    # Choose random scenario
    scenario = random.choice(scenarios)
    round_to = st.session_state.estimate_word_diff_difficulty["round_to"]
    
    if scenario["type"] == "addition":
        # Generate two numbers for addition
        a = random.randint(100000, 900000)
        b = random.randint(100000, 900000)
        
        # Calculate correct estimate
        exact_answer = a + b
        correct_estimate = round(exact_answer / round_to) * round_to
        
        # Generate incorrect estimate
        wrong_offset = random.randint(50000, 200000)
        wrong_exact = exact_answer + wrong_offset
        wrong_estimate = round(wrong_exact / round_to) * round_to
        
        # Format the scenario text
        text = scenario["text"].format(a=a, b=b)
        
        # Store calculation details
        calculation_info = {
            "num1": a,
            "num2": b,
            "operation": "+",
            "exact_result": exact_answer
        }
        
    else:  # subtraction
        # Generate total and part for subtraction
        total = random.randint(500000, 999999)
        part = random.randint(100000, total - 100000)
        
        # Calculate correct estimate
        exact_answer = total - part
        correct_estimate = round(exact_answer / round_to) * round_to
        
        # Generate incorrect estimate
        wrong_offset = random.randint(30000, 100000)
        wrong_exact = exact_answer + wrong_offset
        wrong_estimate = round(wrong_exact / round_to) * round_to
        
        # Format the scenario text
        text = scenario["text"].format(total=total, part=part)
        
        # Store calculation details
        calculation_info = {
            "num1": total,
            "num2": part,
            "operation": "-",
            "exact_result": exact_answer
        }
    
    # Create choices and shuffle
    choices = [correct_estimate, wrong_estimate]
    random.shuffle(choices)
    
    st.session_state.problem_data = {
        "scenario_text": text,
        "scenario_type": scenario["type"],
        "correct_estimate": correct_estimate,
        "wrong_estimate": wrong_estimate,
        "choices": choices,
        "round_to": round_to,
        "calculation_info": calculation_info
    }
    
    st.session_state.correct_answer = correct_estimate
    st.session_state.current_question = "Choose the better estimate:"

def display_question():
    """Display the current question interface"""
    data = st.session_state.problem_data
    
    # Display the scenario in a story-like format
    st.markdown("### 📖 **Real-World Problem:**")
    
    st.markdown(f"""
    <div style="
        background-color: #f3f4f6; 
        padding: 25px; 
        border-radius: 15px; 
        border-left: 5px solid #6366f1;
        font-size: 18px;
        line-height: 1.6;
        margin: 20px 0;
        color: #374151;
    ">
        {data['scenario_text']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**{st.session_state.current_question}**")
    
    # Answer selection
    with st.form("estimation_word_form", clear_on_submit=False):
        st.markdown("**🤔 Which estimate makes more sense?**")
        
        user_answer = st.radio(
            "Choose your answer:",
            options=data["choices"],
            format_func=lambda x: f"**{x:,}**",
            key="word_estimate_choice"
        )
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("✅ Submit Estimate", type="primary", use_container_width=True)
        
        if submit_button:
            st.session_state.user_answer = user_answer
            st.session_state.show_feedback = True
            st.session_state.answer_submitted = True
    
    # Show feedback and next button
    handle_feedback_and_next()

def handle_feedback_and_next():
    """Handle feedback display and next question button"""
    # Show feedback if answer was submitted
    if st.session_state.show_feedback:
        show_feedback()
    
    # Next question button
    if st.session_state.answer_submitted:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Next Question", type="secondary", use_container_width=True):
                st.session_state.question_count += 1
                reset_question_state()
                st.rerun()

def show_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.problem_data
    user_answer = st.session_state.user_answer
    correct_answer = data["correct_estimate"]
    
    if user_answer == correct_answer:
        st.success("🎉 **Correct! Well estimated!**")
        st.session_state.correct_count += 1
        
        # Increase difficulty (make rounding more precise)
        old_round_to = st.session_state.estimate_word_diff_difficulty["round_to"]
        if old_round_to >= 100000:
            st.session_state.estimate_word_diff_difficulty["round_to"] = max(10000, old_round_to // 2)
        elif old_round_to >= 10000:
            st.session_state.estimate_word_diff_difficulty["round_to"] = max(1000, old_round_to // 2)
        else:
            st.session_state.estimate_word_diff_difficulty["round_to"] = max(100, old_round_to // 2)
        
        new_round_to = st.session_state.estimate_word_diff_difficulty["round_to"]
        if new_round_to < old_round_to:
            st.info(f"⬆️ **Great job! Now rounding to the nearest {new_round_to:,} for more precision**")
        
    else:
        st.error(f"❌ **Incorrect.** The correct estimate was **{correct_answer:,}**.")
        
        # Decrease difficulty (make rounding less precise)
        old_round_to = st.session_state.estimate_word_diff_difficulty["round_to"]
        st.session_state.estimate_word_diff_difficulty["round_to"] = min(100000, old_round_to * 2)
        
        new_round_to = st.session_state.estimate_word_diff_difficulty["round_to"]
        if new_round_to > old_round_to:
            st.warning(f"⬇️ **Let's practice with easier rounding. Now rounding to the nearest {new_round_to:,}**")
    
    show_solution_explanation()

def show_solution_explanation():
    """Show the complete solution with estimation steps"""
    data = st.session_state.problem_data
    calc_info = data["calculation_info"]
    
    with st.expander("📖 **See the estimation solution**", expanded=True):
        st.markdown("### 🧮 **Step-by-step estimation:**")
        
        # Step 1: Identify the problem type
        operation_name = "addition" if calc_info["operation"] == "+" else "subtraction"
        st.markdown(f"**Step 1: Identify the operation**")
        st.markdown(f"• This is a **{operation_name}** problem")
        st.markdown(f"• We need to {operation_name[:-3]} the numbers")
        
        # Step 2: Show the numbers and rounding
        st.markdown(f"**Step 2: Round to the nearest {data['round_to']:,}**")
        
        rounded_num1 = round(calc_info["num1"] / data["round_to"]) * data["round_to"]
        rounded_num2 = round(calc_info["num2"] / data["round_to"]) * data["round_to"]
        
        st.markdown(f"• **{calc_info['num1']:,}** rounds to **{rounded_num1:,}**")
        st.markdown(f"• **{calc_info['num2']:,}** rounds to **{rounded_num2:,}**")
        
        # Step 3: Show the calculation
        st.markdown(f"**Step 3: Calculate with rounded numbers**")
        if calc_info["operation"] == "+":
            estimated_result = rounded_num1 + rounded_num2
        else:
            estimated_result = rounded_num1 - rounded_num2
        
        calculation = f"{rounded_num1:,} {calc_info['operation']} {rounded_num2:,} = {estimated_result:,}"
        st.markdown(f"• **{calculation}**")
        
        # Step 4: Reasonableness check
        st.markdown(f"**Step 4: Check if the estimate makes sense**")
        st.markdown(f"• **Exact answer would be:** {calc_info['exact_result']:,}")
        st.markdown(f"• **Our estimate:** {estimated_result:,}")
        
        difference = abs(estimated_result - calc_info["exact_result"])
        percentage_error = (difference / calc_info["exact_result"]) * 100
        st.markdown(f"• **Difference:** {difference:,} ({percentage_error:.1f}% error)")
        st.markdown(f"• This is a good estimate for quick decision-making! ✓")
        
        # Explain why the wrong answer was wrong
        if "wrong_estimate" in data:
            st.markdown("### ❌ **Why the other choice was incorrect:**")
            wrong_diff = abs(data["wrong_estimate"] - calc_info["exact_result"])
            wrong_percentage = (wrong_diff / calc_info["exact_result"]) * 100
            st.markdown(f"• **Wrong estimate:** {data['wrong_estimate']:,}")
            st.markdown(f"• **Error:** {wrong_diff:,} ({wrong_percentage:.1f}% off)")
            st.markdown(f"• This estimate was too far from the actual numbers")

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = None
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.problem_data = {}
    if "user_answer" in st.session_state:
        del st.session_state.user_answer