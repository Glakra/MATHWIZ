import streamlit as st
import random
import html

def run():
    """
    Main function to run the Venn diagram problem solver.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/L.Problem_solving/use_venn_diagrams_to_solve_problems.py
    """
    # Initialize session state
    if "venn_difficulty" not in st.session_state:
        st.session_state.venn_difficulty = 1
    
    if "current_venn_problem" not in st.session_state:
        st.session_state.current_venn_problem = None
        st.session_state.venn_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.consecutive_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > L. Problem solving**")
    st.title("🔵🟡 Use Venn Diagrams to Solve Problems")
    st.markdown("*Learn to organize and analyze data using Venn diagrams*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.venn_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Basic", "Intermediate", "Advanced", "Complex", "Master"]
        st.markdown(f"**Current Level:** {difficulty_names[difficulty_level-1]}")
        progress = (difficulty_level - 1) / 4
        st.progress(progress, text=f"Level {difficulty_level} of 5")
    
    with col2:
        if difficulty_level <= 2:
            st.markdown("**🟢 Easy**")
        elif difficulty_level <= 3:
            st.markdown("**🟡 Medium**")
        else:
            st.markdown("**🔴 Hard**")
    
    with col3:
        if st.button("← Back", type="secondary"):
            if "subtopic" in st.query_params:
                del st.query_params["subtopic"]
            st.rerun()
    
    # Generate new problem if needed
    if st.session_state.current_venn_problem is None:
        generate_new_venn_problem()
    
    # Display current problem
    display_venn_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **How to Solve Venn Diagram Problems**", expanded=False):
        st.markdown("""
        ### Understanding Venn Diagrams:
        
        **What is a Venn Diagram?**
        - Two or more circles that overlap
        - Each circle represents a group
        - The overlap shows items in BOTH groups
        - Outside shows items in NEITHER group
        
        ### Key Areas in a Venn Diagram:
        
        **Two-Circle Diagram:**
        ```
        ┌─────────────────────────┐
        │    ┌─────┐ ┌─────┐     │
        │   │  A   │││  B   │    │
        │   │ only ││  only │    │
        │   └──────┘ └──────┘    │
        │      Both A & B         │
        │                         │
        │    Neither A nor B      │
        └─────────────────────────┘
        ```
        
        ### Problem-Solving Steps:
        
        **1. Read carefully** 📖
        - What are the two groups?
        - What numbers are given?
        - What are we finding?
        
        **2. Draw the diagram** ✏️
        - Label each circle
        - Fill in what you know
        - Start with the overlap!
        
        **3. Work from inside out** 🎯
        - FIRST: Put the "both" number in the middle
        - THEN: Calculate "only A" and "only B"
        - LAST: Find what the question asks
        
        ### Common Question Types:
        
        **"Only A" Questions:**
        - People who like A but NOT B
        - Formula: Total A - Both = Only A
        
        **"Both" Questions:**
        - People who like BOTH A and B
        - This is the overlap/intersection
        
        **"Either/Or" Questions:**
        - People who like A OR B (or both)
        - Formula: Only A + Only B + Both
        
        **"Neither" Questions:**
        - People who don't like A or B
        - Formula: Total - (A or B)
        
        ### Example Problem:
        
        **"10 kids like pizza, 8 like burgers, 3 like both. How many like only pizza?"**
        
        **Solution:**
        1. Pizza total = 10
        2. Both = 3
        3. Only pizza = 10 - 3 = 7 ✓
        
        ### Pro Tips:
        
        🎯 **Always start with the overlap** - Fill in "both" first
        
        🎯 **Check your work** - Numbers should add up correctly
        
        🎯 **Draw it out** - Visual helps avoid mistakes
        
        🎯 **Label everything** - Clear labels prevent confusion
        
        🎯 **Watch for "only"** - This means subtract the overlap!
        
        ### Common Mistakes to Avoid:
        
        ❌ **Don't add totals** - 10 + 8 ≠ 18 people (some counted twice!)
        
        ❌ **Don't forget overlap** - People in both groups count in each total
        
        ❌ **Read carefully** - "Only A" is different from "A"
        """)

def generate_venn_scenarios():
    """Generate diverse scenarios for Venn diagram problems"""
    return {
        "animals": [
            {"item1": "cats", "item2": "dogs", "context": "pets in the neighborhood"},
            {"item1": "whales", "item2": "polar bears", "context": "animals students like"},
            {"item1": "lions", "item2": "tigers", "context": "favorite zoo animals"},
            {"item1": "rabbits", "item2": "hamsters", "context": "classroom pets children want"},
            {"item1": "dolphins", "item2": "sharks", "context": "marine animals kids studied"},
        ],
        
        "activities": [
            {"item1": "swimming", "item2": "riding a horse", "context": "activities people know how to do"},
            {"item1": "playing on the jungle gym", "item2": "playing on the monkey bars", "context": "playground activities children like"},
            {"item1": "soccer", "item2": "basketball", "context": "sports students play"},
            {"item1": "painting", "item2": "drawing", "context": "art activities kids enjoy"},
            {"item1": "singing", "item2": "dancing", "context": "performance activities students do"},
        ],
        
        "food": [
            {"item1": "pizza", "item2": "hamburgers", "context": "favorite foods"},
            {"item1": "apples", "item2": "bananas", "context": "fruits children eat"},
            {"item1": "chocolate", "item2": "vanilla", "context": "ice cream flavors people like"},
            {"item1": "cookies", "item2": "cake", "context": "desserts kids want"},
            {"item1": "carrots", "item2": "broccoli", "context": "vegetables students eat"},
        ],
        
        "entertainment": [
            {"item1": "reading scary stories", "item2": "reading happy stories", "context": "types of stories people like"},
            {"item1": "watching movies", "item2": "playing video games", "context": "weekend activities"},
            {"item1": "board games", "item2": "card games", "context": "indoor games families play"},
            {"item1": "cartoons", "item2": "nature shows", "context": "TV programs children watch"},
            {"item1": "puzzles", "item2": "riddles", "context": "brain teasers students enjoy"},
        ],
        
        "places": [
            {"item1": "Portland", "item2": "San Diego", "context": "cities people have visited"},
            {"item1": "the beach", "item2": "the mountains", "context": "vacation spots families go to"},
            {"item1": "museums", "item2": "aquariums", "context": "field trip destinations"},
            {"item1": "Paris", "item2": "London", "context": "European cities tourists visited"},
            {"item1": "the library", "item2": "the park", "context": "places kids go after school"},
        ],
        
        "subjects": [
            {"item1": "math", "item2": "science", "context": "favorite school subjects"},
            {"item1": "history", "item2": "geography", "context": "social studies topics students like"},
            {"item1": "Spanish", "item2": "French", "context": "languages people are learning"},
            {"item1": "art", "item2": "music", "context": "creative subjects children enjoy"},
            {"item1": "reading", "item2": "writing", "context": "English activities students prefer"},
        ],
        
        "technology": [
            {"item1": "tablets", "item2": "laptops", "context": "devices students use"},
            {"item1": "email", "item2": "text messages", "context": "ways people communicate"},
            {"item1": "Instagram", "item2": "TikTok", "context": "social media apps teens use"},
            {"item1": "Minecraft", "item2": "Roblox", "context": "games children play"},
            {"item1": "YouTube", "item2": "Netflix", "context": "streaming services families have"},
        ],
        
        "collections": [
            {"item1": "stamps", "item2": "coins", "context": "items people collect"},
            {"item1": "baseball cards", "item2": "Pokemon cards", "context": "trading cards kids have"},
            {"item1": "seashells", "item2": "rocks", "context": "nature items children collect"},
            {"item1": "stickers", "item2": "badges", "context": "items students trade"},
            {"item1": "books", "item2": "magazines", "context": "reading materials people own"},
        ]
    }

def generate_new_venn_problem():
    """Generate a new Venn diagram problem"""
    difficulty = st.session_state.venn_difficulty
    scenarios = generate_venn_scenarios()
    
    # Choose scenario type based on difficulty
    if difficulty == 1:
        # Simple scenarios with small numbers
        scenario_types = ["animals", "food", "activities"]
        total_range = (8, 15)
        overlap_percentage = (0.1, 0.3)
    elif difficulty == 2:
        # Medium scenarios
        scenario_types = ["entertainment", "places", "subjects"]
        total_range = (12, 25)
        overlap_percentage = (0.2, 0.4)
    elif difficulty == 3:
        # Harder scenarios with larger numbers
        scenario_types = ["technology", "collections", "activities"]
        total_range = (20, 40)
        overlap_percentage = (0.3, 0.5)
    elif difficulty == 4:
        # Complex scenarios
        scenario_types = list(scenarios.keys())
        total_range = (30, 60)
        overlap_percentage = (0.2, 0.6)
    else:  # difficulty == 5
        # Master level - all scenarios, tricky numbers
        scenario_types = list(scenarios.keys())
        total_range = (40, 100)
        overlap_percentage = (0.1, 0.7)
    
    # Select random scenario
    scenario_type = random.choice(scenario_types)
    scenario = random.choice(scenarios[scenario_type])
    
    # Generate numbers
    total_people = random.randint(*total_range)
    
    # Calculate reasonable ranges for each group
    min_group = int(total_people * 0.3)
    max_group = int(total_people * 0.8)
    
    group1_total = random.randint(min_group, max_group)
    group2_total = random.randint(min_group, max_group)
    
    # Calculate overlap (both groups) - FIXED LOGIC
    max_possible_overlap = min(group1_total, group2_total)
    
    # Calculate min and max overlap based on percentages
    min_overlap = max(1, int(max_possible_overlap * overlap_percentage[0]))
    max_overlap_target = int(max_possible_overlap * overlap_percentage[1])
    
    # Ensure max_overlap is at least min_overlap + 1
    max_overlap = max(min_overlap + 1, max_overlap_target)
    
    # If max_overlap exceeds max_possible_overlap, adjust it
    if max_overlap > max_possible_overlap:
        max_overlap = max_possible_overlap
        # Also ensure min_overlap is valid
        min_overlap = min(min_overlap, max_overlap - 1)
        if min_overlap < 1:
            min_overlap = 1
    
    # Generate both_count
    if min_overlap >= max_overlap:
        both_count = min_overlap
    else:
        both_count = random.randint(min_overlap, max_overlap)
    
    # Calculate exclusive counts
    only_group1 = group1_total - both_count
    only_group2 = group2_total - both_count
    
    # Ensure we have valid numbers
    if only_group1 < 0 or only_group2 < 0:
        # Regenerate with safer numbers
        both_count = min(group1_total, group2_total) // 2
        only_group1 = group1_total - both_count
        only_group2 = group2_total - both_count
    
    # Ensure we don't exceed total
    people_in_diagram = only_group1 + only_group2 + both_count
    if people_in_diagram > total_people:
        total_people = people_in_diagram + random.randint(0, 5)
    
    # Choose question type based on difficulty
    if difficulty <= 2:
        question_types = ["only1", "only2"]
    elif difficulty <= 3:
        question_types = ["only1", "only2", "both", "either"]
    else:
        question_types = ["only1", "only2", "both", "either", "neither", "total_unique"]
    
    question_type = random.choice(question_types)
    
    # Generate question and answer
    context = scenario["context"]
    item1 = scenario["item1"]
    item2 = scenario["item2"]
    
    # Create the problem text
    problem_text = f"Of the {total_people} {context}, {group1_total} like {item1} and {group2_total} like {item2}. "
    problem_text += f"{both_count} {'person likes' if both_count == 1 else 'people like'} both {item1} and {item2}. "
    
    # Add specific question based on type
    if question_type == "only1":
        problem_text += f"How many people like {item1} but not {item2}?"
        correct_answer = only_group1
    elif question_type == "only2":
        problem_text += f"How many people like {item2} but not {item1}?"
        correct_answer = only_group2
    elif question_type == "both":
        problem_text += f"How many people like both {item1} and {item2}?"
        correct_answer = both_count
    elif question_type == "either":
        problem_text += f"How many people like either {item1} or {item2} (or both)?"
        correct_answer = only_group1 + only_group2 + both_count
    elif question_type == "neither":
        problem_text += f"How many people like neither {item1} nor {item2}?"
        correct_answer = total_people - (only_group1 + only_group2 + both_count)
    else:  # total_unique
        problem_text += f"How many different people like at least one of these?"
        correct_answer = only_group1 + only_group2 + both_count
    
    # Store problem data
    st.session_state.venn_data = {
        "total_people": total_people,
        "group1_total": group1_total,
        "group2_total": group2_total,
        "both_count": both_count,
        "only_group1": only_group1,
        "only_group2": only_group2,
        "neither": total_people - (only_group1 + only_group2 + both_count),
        "item1": item1,
        "item2": item2,
        "context": context,
        "question_type": question_type,
        "correct_answer": correct_answer,
        "problem_text": problem_text
    }
    st.session_state.current_venn_problem = problem_text

def display_venn_problem():
    """Display the current Venn diagram problem"""
    data = st.session_state.venn_data
    
    # Display problem text
    st.markdown(f"""
    <div style="
        background-color: #f0f8ff;
        border: 2px solid #4169e1;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        font-size: 18px;
        line-height: 1.6;
    ">
        {data['problem_text']}
    </div>
    """, unsafe_allow_html=True)
    
    # Hint section
    st.markdown("**Hint:** Copy and complete the Venn diagram below to help you solve the problem.")
    
    # Create interactive Venn diagram
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Draw Venn diagram using matplotlib (more reliable than SVG)
        draw_venn_diagram(data)
    
    with col2:
        # Answer input section
        st.markdown("### Your Answer:")
        
        # Create number input
        user_answer = st.number_input(
            "Enter your answer:",
            min_value=0,
            max_value=data['total_people'],
            step=1,
            key="venn_answer_input",
            disabled=st.session_state.answer_submitted
        )
        
        # Submit button
        if st.button("Submit", type="primary", disabled=st.session_state.answer_submitted):
            handle_venn_answer(user_answer)
    
    # Show feedback if answer submitted
    if st.session_state.show_feedback:
        show_venn_feedback()
        
        # Next problem button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Problem", type="secondary", use_container_width=True):
                reset_venn_problem_state()
                st.rerun()

def draw_venn_diagram(data):
    """Draw Venn diagram using matplotlib"""
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create circles
    circle1 = patches.Circle((0.35, 0.5), 0.25, fill=True, alpha=0.3, 
                            color='gold', edgecolor='orange', linewidth=2)
    circle2 = patches.Circle((0.65, 0.5), 0.25, fill=True, alpha=0.3, 
                            color='skyblue', edgecolor='blue', linewidth=2)
    
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    
    # Add labels
    ax.text(0.35, 0.85, f"I like {data['item1']}", ha='center', va='center', 
            fontsize=12, fontweight='bold')
    ax.text(0.65, 0.85, f"I like {data['item2']}", ha='center', va='center', 
            fontsize=12, fontweight='bold')
    
    # Add numbers if feedback is shown
    if st.session_state.show_feedback:
        ax.text(0.2, 0.5, str(data['only_group1']), ha='center', va='center', 
                fontsize=20, fontweight='bold')
        ax.text(0.5, 0.5, str(data['both_count']), ha='center', va='center', 
                fontsize=20, fontweight='bold')
        ax.text(0.8, 0.5, str(data['only_group2']), ha='center', va='center', 
                fontsize=20, fontweight='bold')
    
    # Add context label
    ax.text(0.5, 0.1, data['context'], ha='center', va='center', 
            fontsize=11, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black"))
    
    # Set axis properties
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Display the figure
    st.pyplot(fig)
    plt.close()

def handle_venn_answer(answer):
    """Handle user's answer submission"""
    st.session_state.user_answer = answer
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_venn_feedback():
    """Display feedback for the submitted answer"""
    data = st.session_state.venn_data
    user_answer = st.session_state.user_answer
    correct_answer = data['correct_answer']
    
    if user_answer == correct_answer:
        st.success("✅ **Correct! Excellent work with the Venn diagram!**")
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.venn_difficulty
            st.session_state.venn_difficulty = min(
                st.session_state.venn_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.venn_difficulty == 5 and old_difficulty < 5:
                st.balloons()
                st.info("🏆 **Amazing! You've mastered Venn diagram problems!**")
            elif old_difficulty < st.session_state.venn_difficulty:
                st.info(f"⬆️ **Level up! Now at Level {st.session_state.venn_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct answer is {correct_answer}.**")
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty
        old_difficulty = st.session_state.venn_difficulty
        st.session_state.venn_difficulty = max(
            st.session_state.venn_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.venn_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.venn_difficulty}. Keep practicing!**")
    
    # Show detailed explanation
    show_venn_explanation()

def show_venn_explanation():
    """Show detailed explanation of the Venn diagram solution"""
    data = st.session_state.venn_data
    
    with st.expander("📖 **See the complete solution**", expanded=True):
        st.markdown("### Let's solve this step by step:")
        
        st.markdown(f"""
        **Given information:**
        - Total {data['context']}: {data['total_people']}
        - Like {data['item1']}: {data['group1_total']}
        - Like {data['item2']}: {data['group2_total']}
        - Like both: {data['both_count']}
        
        **Step 1: Fill in the overlap**
        - The middle section (both) = {data['both_count']}
        
        **Step 2: Calculate "only" sections**
        - Only {data['item1']} = {data['group1_total']} - {data['both_count']} = {data['only_group1']}
        - Only {data['item2']} = {data['group2_total']} - {data['both_count']} = {data['only_group2']}
        
        **Step 3: Check the total**
        - In the diagram: {data['only_group1']} + {data['both_count']} + {data['only_group2']} = {data['only_group1'] + data['both_count'] + data['only_group2']}
        - Neither: {data['total_people']} - {data['only_group1'] + data['both_count'] + data['only_group2']} = {data['neither']}
        """)
        
        # Show answer based on question type
        question_explanations = {
            "only1": f"People who like {data['item1']} but NOT {data['item2']} = **{data['only_group1']}**",
            "only2": f"People who like {data['item2']} but NOT {data['item1']} = **{data['only_group2']}**",
            "both": f"People who like BOTH {data['item1']} and {data['item2']} = **{data['both_count']}**",
            "either": f"People who like either one (or both) = {data['only_group1']} + {data['both_count']} + {data['only_group2']} = **{data['only_group1'] + data['both_count'] + data['only_group2']}**",
            "neither": f"People who like neither = {data['total_people']} - {data['only_group1'] + data['both_count'] + data['only_group2']} = **{data['neither']}**",
            "total_unique": f"Total different people who like at least one = **{data['only_group1'] + data['both_count'] + data['only_group2']}**"
        }
        
        st.markdown(f"\n**Answer:** {question_explanations[data['question_type']]}")
        
        # Visual representation
        st.markdown("\n### Complete Venn Diagram:")
        st.markdown("""
        ```
        ┌─────────────────────────────┐
        │                             │
        │   ┌─────┐ ┌─────┐         │
        │  │  {}  │││  {}  │        │
        │  │      │{}│      │        │
        │  └──────┘ └──────┘        │
        │                             │
        │         Neither: {}         │
        └─────────────────────────────┘
        ```
        """.format(
            data['only_group1'],
            data['only_group2'],
            data['both_count'],
            data['neither']
        ))

def reset_venn_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_venn_problem = None
    st.session_state.venn_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = None