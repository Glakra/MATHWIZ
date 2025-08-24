import streamlit as st
import random
import pandas as pd

def run():
    """
    Main function to run the Compare, Order and Round Decimals Word Problems activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/A. Place values and number sense/compare_order_and_round_decimals_word_problems.py
    """
    # Initialize session state
    if "decimals_difficulty" not in st.session_state:
        st.session_state.decimals_difficulty = 1  # Start with 1 decimal place
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = "new"  # Start with new question needed
        st.session_state.correct_answer = None
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.question_data = {}
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > A. Place values and number sense**")
    st.title("📊 Compare, Order and Round Decimals: Word Problems")
    st.markdown("*Solve real-world problems involving decimal comparisons, ordering, and rounding*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.decimals_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**Current Difficulty:** {difficulty_level} decimal place{'s' if difficulty_level > 1 else ''}")
        # Progress bar (1 to 3 decimal places)
        progress = (difficulty_level - 1) / 2  # Convert 1-3 to 0-1
        st.progress(progress, text=f"{difficulty_level} decimal place{'s' if difficulty_level > 1 else ''}")
    
    with col2:
        if difficulty_level == 1:
            st.markdown("**🟡 Beginner**")
        elif difficulty_level == 2:
            st.markdown("**🟠 Intermediate**")
        else:
            st.markdown("**🔴 Advanced**")
    
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
    
    # Debug section (can be removed later)
    with st.expander("🔧 Debug Info (For Testing)", expanded=False):
        st.write(f"**Current Question State:** {st.session_state.current_question}")
        st.write(f"**Show Feedback:** {st.session_state.show_feedback}")
        st.write(f"**Answer Submitted:** {st.session_state.answer_submitted}")
        st.write(f"**Selected Answer:** {st.session_state.get('selected_answer', 'None')}")
        st.write(f"**User Answer:** {st.session_state.get('user_answer', 'None')}")
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Instructions & Tips**", expanded=False):
        st.markdown("""
        ### How to Play:
        - **Read the word problem carefully**
        - **Identify what you need to compare, order, or round**
        - **Click the correct answer** from the options
        - **Think about place values** - tenths, hundredths, thousandths
        
        ### Tips for Success:
        - **Line up decimal points** when comparing
        - **Add zeros** if needed: 0.3 = 0.30 = 0.300
        - **For ordering:** Start from the left and compare digit by digit
        - **For rounding:** Look at the digit after the rounding place
        
        ### Comparing Examples:
        - **0.7 vs 0.65:** 0.7 = 0.70, so 0.7 > 0.65
        - **0.24 vs 0.3:** 0.3 = 0.30, so 0.3 > 0.24
        
        ### Ordering Examples:
        - **Order: 0.8, 0.75, 0.9** → 0.75, 0.8, 0.9
        - **Order: 1.2, 1.25, 1.02** → 1.02, 1.2, 1.25
        
        ### Rounding Examples:
        - **Round 0.67 to 1 decimal place:** 0.7 (7 ≥ 5, round up)
        - **Round 0.23 to 1 decimal place:** 0.2 (3 < 5, round down)
        
        ### Difficulty Levels:
        - **🟡 1 decimal place:** Basic comparisons (0.3 vs 0.7)
        - **🟠 2 decimal places:** More precision (0.45 vs 0.47)
        - **🔴 3 decimal places:** Advanced (0.234 vs 0.237)
        
        ### Scoring:
        - ✅ **Correct answer:** Advance to more decimal places
        - ❌ **Wrong answer:** Practice with fewer decimal places
        - 🎯 **Goal:** Master 3 decimal places!
        """)

def generate_new_question():
    """Generate a new decimal word problem"""
    difficulty = st.session_state.decimals_difficulty
    
    # Question types
    question_types = [
        "compare_weights",
        "compare_scores", 
        "compare_measurements",
        "order_prices",
        "order_distances",
        "round_measurement",
        "round_score",
        "highest_lowest",
        "compare_times",
        "order_weights"
    ]
    
    question_type = random.choice(question_types)
    
    if question_type == "compare_weights":
        generate_compare_weights_question()
    elif question_type == "compare_scores":
        generate_compare_scores_question()
    elif question_type == "compare_measurements":
        generate_compare_measurements_question()
    elif question_type == "order_prices":
        generate_order_prices_question()
    elif question_type == "order_distances":
        generate_order_distances_question()
    elif question_type == "round_measurement":
        generate_round_measurement_question()
    elif question_type == "round_score":
        generate_round_score_question()
    elif question_type == "highest_lowest":
        generate_highest_lowest_question()
    elif question_type == "compare_times":
        generate_compare_times_question()
    elif question_type == "order_weights":
        generate_order_weights_question()
    
    # CRITICAL FIX: Set current_question to "active" to prevent regeneration
    st.session_state.current_question = "active"

def generate_order_distances_question():
    """Generate a question about ordering distances"""
    difficulty = st.session_state.decimals_difficulty
    
    routes = ["Route A", "Route B", "Route C", "Path 1", "Path 2", "Path 3", "Trail X", "Trail Y", "Trail Z"]
    selected_routes = random.sample(routes, 3)
    
    # Generate distances
    distances = [generate_decimal(difficulty) for _ in range(3)]
    
    # Ensure no ties
    while len(set(distances)) != 3:
        distances = [generate_decimal(difficulty) for _ in range(3)]
    
    story = f"Three hiking routes were measured. {selected_routes[0]} is {distances[0]} kilometers long, {selected_routes[1]} is {distances[1]} kilometers long, and {selected_routes[2]} is {distances[2]} kilometers long."
    
    # Create ordering options
    routes_distances = list(zip(selected_routes, distances))
    
    # Sort by distance (ascending - shortest to longest)
    sorted_routes = sorted(routes_distances, key=lambda x: x[1])
    correct_order = [route[0] for route in sorted_routes]
    
    # Create different ordering options
    import itertools
    all_perms = list(itertools.permutations(selected_routes))
    
    # Include the correct answer and 3 random wrong answers
    options = [correct_order]
    
    # Add some specific wrong answers
    wrong_options = [
        [correct_order[2], correct_order[1], correct_order[0]],  # Reverse order
        [correct_order[1], correct_order[0], correct_order[2]],  # Swap first two
        [correct_order[0], correct_order[2], correct_order[1]],  # Swap last two
    ]
    
    for wrong_option in wrong_options:
        if wrong_option not in options and len(options) < 4:
            options.append(wrong_option)
    
    # Fill remaining slots with random permutations
    for perm in all_perms:
        if list(perm) not in options and len(options) < 4:
            options.append(list(perm))
    
    st.session_state.question_data = {
        "story": story,
        "question": "Order the routes from shortest to longest:",
        "options": options[:4],
        "correct_answer": correct_order,
        "explanation": f"Ordering by distance: {', '.join([f'{route} ({distance} km)' for route, distance in sorted_routes])}",
        "question_type": "order_distances"
    }

def generate_round_score_question():
    """Generate a rounding question with scores"""
    difficulty = st.session_state.decimals_difficulty
    
    # Only round if we have enough decimal places
    if difficulty == 1:
        generate_compare_scores_question()
        return  # FIXED: Added return to prevent continuing execution
    
    competitions = [
        ("gymnastics", "Maria"),
        ("diving", "Alex"),
        ("figure skating", "Emma"),
        ("dance", "Jordan"),
        ("spelling bee", "Taylor")
    ]
    
    competition, person = random.choice(competitions)
    
    # Generate a score with more decimal places than we want to round to
    if difficulty == 2:
        original_score = round(random.uniform(85.0, 99.9), 2)
        round_to = 1
    else:
        original_score = round(random.uniform(85.0, 99.99), 3)
        round_to = 2
    
    story = f"In the {competition} competition, {person} scored {original_score} points."
    
    # Calculate correct rounded value
    correct_rounded = round(original_score, round_to)
    
    # Generate distractors
    options = [correct_rounded]
    
    # Add common rounding errors
    if round_to == 1:
        # Round up/down errors
        wrong1 = round(original_score + 0.1, 1)
        wrong2 = round(original_score - 0.1, 1)
        wrong3 = round(original_score, 0)  # Wrong decimal places
    else:
        wrong1 = round(original_score + 0.01, 2)
        wrong2 = round(original_score - 0.01, 2)
        wrong3 = round(original_score, 1)  # Wrong decimal places
    
    # Filter out invalid options and duplicates
    for option in [wrong1, wrong2, wrong3]:
        if option > 0 and option not in options:
            options.append(option)
    
    # Ensure we have enough options
    while len(options) < 4:
        new_option = round(random.uniform(85.0, 99.9), round_to)
        if new_option not in options:
            options.append(new_option)
    
    options = sorted(list(set(options)))[:4]
    
    st.session_state.question_data = {
        "story": story,
        "question": f"Round {original_score} points to {round_to} decimal place{'s' if round_to > 1 else ''}.",
        "options": options,
        "correct_answer": correct_rounded,
        "explanation": f"To round {original_score} to {round_to} decimal place{'s' if round_to > 1 else ''}, look at the digit after the rounding place. The answer is {correct_rounded}.",
        "question_type": "round_score"
    }

def generate_decimal(difficulty):
    """Generate a decimal with specified number of places"""
    if difficulty == 1:
        return round(random.uniform(0.1, 9.9), 1)
    elif difficulty == 2:
        return round(random.uniform(0.01, 9.99), 2)
    else:
        return round(random.uniform(0.001, 9.999), 3)

def generate_compare_weights_question():
    """Generate a question comparing weights of animals/objects"""
    difficulty = st.session_state.decimals_difficulty
    
    animals = ["Snowball", "Meadow", "Whiskers", "Fluffy", "Shadow", "Cookie", "Bella", "Max", "Luna", "Charlie"]
    objects = ["baby rabbit", "kitten", "puppy", "guinea pig", "hamster", "bird", "turtle", "mouse"]
    
    # Pick two items to compare
    if random.choice([True, False]):
        # Use animal names
        name1, name2 = random.sample(animals, 2)
        item_type = random.choice(["puppies", "kittens", "bunnies", "guinea pigs"])
        weight1 = generate_decimal(difficulty)
        weight2 = generate_decimal(difficulty)
        
        # Ensure weights are different
        while weight1 == weight2:
            weight2 = generate_decimal(difficulty)
        
        story = f"The {random.choice(['Johnson', 'Smith', 'Brown', 'Davis'])} family has two new {item_type}! {name1} weighs {weight1} kilograms and {name2} weighs {weight2} kilograms."
    else:
        # Use object descriptions
        obj1, obj2 = random.sample(objects, 2)
        weight1 = generate_decimal(difficulty)
        weight2 = generate_decimal(difficulty)
        
        # Ensure weights are different
        while weight1 == weight2:
            weight2 = generate_decimal(difficulty)
        
        # Handle articles properly
        article1 = "an" if obj1[0].lower() in 'aeiou' else "a"
        article2 = "an" if obj2[0].lower() in 'aeiou' else "a"
        
        story = f"At the pet store, there are two animals for adoption. The {obj1} weighs {weight1} kilograms and the {obj2} weighs {weight2} kilograms."
        name1, name2 = obj1, obj2
    
    if weight1 > weight2:
        correct_answer = name1
        explanation = f"{name1} weighs {weight1} kg and {name2} weighs {weight2} kg. Since {weight1} > {weight2}, {name1} weighs more."
    else:
        correct_answer = name2
        explanation = f"{name1} weighs {weight1} kg and {name2} weighs {weight2} kg. Since {weight2} > {weight1}, {name2} weighs more."
    
    st.session_state.question_data = {
        "story": story,
        "question": "Which one weighs more?",
        "options": [name1, name2],
        "correct_answer": correct_answer,
        "explanation": explanation,
        "question_type": "compare_weights"
    }

def generate_compare_scores_question():
    """Generate a question comparing test scores or competition scores"""
    difficulty = st.session_state.decimals_difficulty
    
    names = ["Maria", "Janet", "Felicia", "Alex", "Sam", "Jordan", "Taylor", "Casey", "Riley", "Avery"]
    
    # Choose 3 people
    selected_names = random.sample(names, 3)
    
    # Generate scores
    scores = [generate_decimal(difficulty) for _ in range(3)]
    
    # Ensure no ties
    while len(set(scores)) != 3:
        scores = [generate_decimal(difficulty) for _ in range(3)]
    
    # Choose competition type
    competitions = [
        ("gymnastics", "all-around competition"),
        ("diving", "competition"),
        ("figure skating", "competition"),
        ("dance", "competition"),
        ("science fair", "judging"),
        ("spelling bee", "competition"),
        ("art contest", "judging"),
        ("music competition", "performance")
    ]
    
    sport, event = random.choice(competitions)
    
    # Create story
    story = f"{', '.join(selected_names[:-1])} and {selected_names[-1]} compete in {sport}. In the {event}, their scores were very close!"
    
    # Create table data
    table_data = list(zip(selected_names, scores))
    
    # Find highest score
    max_score = max(scores)
    winner = selected_names[scores.index(max_score)]
    
    st.session_state.question_data = {
        "story": story,
        "table_data": table_data,
        "question": "Who had the highest score?",
        "options": selected_names,
        "correct_answer": winner,
        "explanation": f"{winner} had the highest score with {max_score}. Comparing all scores: {', '.join([f'{name}: {score}' for name, score in table_data])}",
        "question_type": "compare_scores"
    }

def generate_compare_measurements_question():
    """Generate a question comparing measurements"""
    difficulty = st.session_state.decimals_difficulty
    
    measurements = [
        ("height", "meters", ["Emma", "Liam"]),
        ("length", "meters", ["rope A", "rope B"]),
        ("distance", "kilometers", ["path A", "path B"]),
        ("width", "meters", ["table A", "table B"]),
        ("thickness", "centimeters", ["book A", "book B"])
    ]
    
    measure_type, unit, items = random.choice(measurements)
    
    # Generate two different measurements
    val1 = generate_decimal(difficulty)
    val2 = generate_decimal(difficulty)
    
    # Ensure they're different
    while val1 == val2:
        val2 = generate_decimal(difficulty)
    
    # Handle articles properly for the first item
    article1 = "an" if items[0][0].lower() in 'aeiou' else "a"
    article2 = "an" if items[1][0].lower() in 'aeiou' else "a"
    
    # For names like "Emma", don't use articles
    if items[0][0].isupper():
        story = f"Two items were measured. {items[0]} has a {measure_type} of {val1} {unit}, and {items[1]} has a {measure_type} of {val2} {unit}."
    else:
        story = f"Two items were measured. {items[0]} has a {measure_type} of {val1} {unit}, and {items[1]} has a {measure_type} of {val2} {unit}."
    
    if val1 > val2:
        correct_answer = items[0]
        explanation = f"{items[0]} has a {measure_type} of {val1} {unit} and {items[1]} has a {measure_type} of {val2} {unit}. Since {val1} > {val2}, {items[0]} has the greater {measure_type}."
    else:
        correct_answer = items[1]
        explanation = f"{items[0]} has a {measure_type} of {val1} {unit} and {items[1]} has a {measure_type} of {val2} {unit}. Since {val2} > {val1}, {items[1]} has the greater {measure_type}."
    
    st.session_state.question_data = {
        "story": story,
        "question": f"Which has the greater {measure_type}?",
        "options": items,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "question_type": "compare_measurements"
    }

def generate_order_prices_question():
    """Generate a question about ordering prices"""
    difficulty = st.session_state.decimals_difficulty
    
    items = ["apple", "banana", "orange", "grape", "pear", "peach", "plum", "cherry"]
    selected_items = random.sample(items, 3)
    
    # Generate prices
    prices = [generate_decimal(difficulty) for _ in range(3)]
    
    # Ensure no ties
    while len(set(prices)) != 3:
        prices = [generate_decimal(difficulty) for _ in range(3)]
    
    # Fix the article usage and formatting
    articles = []
    for item in selected_items:
        if item[0].lower() in 'aeiou':
            articles.append("an")
        else:
            articles.append("a")
    
    story = f"At the fruit stand, {articles[0]} {selected_items[0]} costs ${prices[0]}, {articles[1]} {selected_items[1]} costs ${prices[1]}, and {articles[2]} {selected_items[2]} costs ${prices[2]}."
    
    # Create ordering options
    items_prices = list(zip(selected_items, prices))
    
    # Sort by price (ascending)
    sorted_items = sorted(items_prices, key=lambda x: x[1])
    correct_order = [item[0] for item in sorted_items]
    
    # Create different ordering options
    options = [
        correct_order,
        [correct_order[1], correct_order[0], correct_order[2]],
        [correct_order[2], correct_order[1], correct_order[0]],
        [correct_order[0], correct_order[2], correct_order[1]]
    ]
    
    # Remove duplicates and ensure correct answer is included
    unique_options = []
    for opt in options:
        if opt not in unique_options:
            unique_options.append(opt)
    
    if len(unique_options) < 3:
        # Add more random permutations
        import itertools
        all_perms = list(itertools.permutations(selected_items))
        for perm in all_perms:
            if list(perm) not in unique_options and len(unique_options) < 4:
                unique_options.append(list(perm))
    
    st.session_state.question_data = {
        "story": story,
        "question": "Order the fruits from least expensive to most expensive:",
        "options": unique_options[:4],
        "correct_answer": correct_order,
        "explanation": f"Ordering by price: {', '.join([f'{item} (${price})' for item, price in sorted_items])}",
        "question_type": "order_prices"
    }

def generate_round_measurement_question():
    """Generate a rounding question with measurements"""
    difficulty = st.session_state.decimals_difficulty
    
    # Only round if we have enough decimal places
    if difficulty == 1:
        generate_compare_weights_question()
        return  # FIXED: Added return to prevent continuing execution
    
    measurements = [
        ("height", "meters", "The tree"),
        ("distance", "kilometers", "The hiking trail"),
        ("weight", "kilograms", "The package"),
        ("length", "meters", "The rope"),
        ("width", "centimeters", "The book")
    ]
    
    measure_type, unit, subject = random.choice(measurements)
    
    # Generate a number with more decimal places than we want to round to
    if difficulty == 2:
        original_value = round(random.uniform(1.0, 99.9), 2)
        round_to = 1
    else:
        original_value = round(random.uniform(1.0, 99.99), 3)
        round_to = 2
    
    story = f"{subject} has a {measure_type} of {original_value} {unit}."
    
    # Calculate correct rounded value
    correct_rounded = round(original_value, round_to)
    
    # Generate distractors
    options = [correct_rounded]
    
    # Add common rounding errors
    if round_to == 1:
        # Round up/down errors
        wrong1 = round(original_value + 0.1, 1)
        wrong2 = round(original_value - 0.1, 1)
        wrong3 = round(original_value, 0)  # Wrong decimal places
    else:
        wrong1 = round(original_value + 0.01, 2)
        wrong2 = round(original_value - 0.01, 2)
        wrong3 = round(original_value, 1)  # Wrong decimal places
    
    # Filter out invalid options and duplicates
    for option in [wrong1, wrong2, wrong3]:
        if option > 0 and option not in options:
            options.append(option)
    
    # Ensure we have enough options
    while len(options) < 4:
        new_option = round(random.uniform(1.0, 99.9), round_to)
        if new_option not in options:
            options.append(new_option)
    
    options = sorted(list(set(options)))[:4]
    
    st.session_state.question_data = {
        "story": story,
        "question": f"Round {original_value} {unit} to {round_to} decimal place{'s' if round_to > 1 else ''}.",
        "options": options,
        "correct_answer": correct_rounded,
        "explanation": f"To round {original_value} to {round_to} decimal place{'s' if round_to > 1 else ''}, look at the digit after the rounding place. The answer is {correct_rounded}.",
        "question_type": "round_measurement"
    }

def generate_highest_lowest_question():
    """Generate a question about finding highest/lowest values"""
    difficulty = st.session_state.decimals_difficulty
    
    contexts = [
        ("rainfall", "millimeters", "Monday", "Tuesday", "Wednesday", "Thursday"),
        ("temperature", "degrees", "City A", "City B", "City C", "City D"),
        ("plant growth", "centimeters", "Plant 1", "Plant 2", "Plant 3", "Plant 4"),
        ("race times", "seconds", "Runner A", "Runner B", "Runner C", "Runner D")
    ]
    
    measure_type, unit, *items = random.choice(contexts)
    selected_items = random.sample(items, 4)
    
    # Generate values
    values = [generate_decimal(difficulty) for _ in range(4)]
    
    # Ensure no ties
    while len(set(values)) != 4:
        values = [generate_decimal(difficulty) for _ in range(4)]
    
    # Choose whether to ask for highest or lowest
    ask_for_highest = random.choice([True, False])
    
    # Create table data
    table_data = list(zip(selected_items, values))
    
    if ask_for_highest:
        if measure_type == "race times":
            # For race times, lowest is best (fastest)
            best_value = min(values)
            answer = selected_items[values.index(best_value)]
            question = "Who had the fastest time?"
            explanation = f"{answer} had the fastest time with {best_value} {unit}."
        else:
            best_value = max(values)
            answer = selected_items[values.index(best_value)]
            question = f"Which had the highest {measure_type}?"
            explanation = f"{answer} had the highest {measure_type} with {best_value} {unit}."
    else:
        if measure_type == "race times":
            # For race times, highest is worst (slowest)
            worst_value = max(values)
            answer = selected_items[values.index(worst_value)]
            question = "Who had the slowest time?"
            explanation = f"{answer} had the slowest time with {worst_value} {unit}."
        else:
            worst_value = min(values)
            answer = selected_items[values.index(worst_value)]
            question = f"Which had the lowest {measure_type}?"
            explanation = f"{answer} had the lowest {measure_type} with {worst_value} {unit}."
    
    story = f"Here are the {measure_type} measurements:"
    
    st.session_state.question_data = {
        "story": story,
        "table_data": table_data,
        "question": question,
        "options": selected_items,
        "correct_answer": answer,
        "explanation": explanation,
        "question_type": "highest_lowest"
    }

def generate_compare_times_question():
    """Generate a question comparing times"""
    difficulty = st.session_state.decimals_difficulty
    
    activities = [
        ("swimming", "seconds", "Maria", "Emma"),
        ("running", "seconds", "Jake", "Tom"),
        ("cycling", "minutes", "Anna", "Lisa"),
        ("solving a puzzle", "minutes", "Alex", "Jordan")
    ]
    
    activity, unit, person1, person2 = random.choice(activities)
    
    # Generate times
    time1 = generate_decimal(difficulty)
    time2 = generate_decimal(difficulty)
    
    # Ensure they're different
    while time1 == time2:
        time2 = generate_decimal(difficulty)
    
    story = f"{person1} and {person2} are {activity}. {person1} took {time1} {unit} and {person2} took {time2} {unit}."
    
    # For times, lower is better
    if time1 < time2:
        correct_answer = person1
        explanation = f"{person1} was faster with {time1} {unit} compared to {person2}'s {time2} {unit}. Since {time1} < {time2}, {person1} was faster."
    else:
        correct_answer = person2
        explanation = f"{person2} was faster with {time2} {unit} compared to {person1}'s {time1} {unit}. Since {time2} < {time1}, {person2} was faster."
    
    st.session_state.question_data = {
        "story": story,
        "question": "Who was faster?",
        "options": [person1, person2],
        "correct_answer": correct_answer,
        "explanation": explanation,
        "question_type": "compare_times"
    }

def generate_order_weights_question():
    """Generate a question about ordering weights"""
    difficulty = st.session_state.decimals_difficulty
    
    objects = ["box A", "box B", "box C", "package 1", "package 2", "package 3", "bag X", "bag Y", "bag Z"]
    selected_objects = random.sample(objects, 3)
    
    # Generate weights
    weights = [generate_decimal(difficulty) for _ in range(3)]
    
    # Ensure no ties
    while len(set(weights)) != 3:
        weights = [generate_decimal(difficulty) for _ in range(3)]
    
    story = f"Three items were weighed. {selected_objects[0]} weighs {weights[0]} kg, {selected_objects[1]} weighs {weights[1]} kg, and {selected_objects[2]} weighs {weights[2]} kg."
    
    # Create ordering options
    objects_weights = list(zip(selected_objects, weights))
    
    # Sort by weight (ascending - lightest to heaviest)
    sorted_objects = sorted(objects_weights, key=lambda x: x[1])
    correct_order = [obj[0] for obj in sorted_objects]
    
    # Create different ordering options
    import itertools
    all_perms = list(itertools.permutations(selected_objects))
    
    # Include the correct answer and 3 random wrong answers
    options = [correct_order]
    
    # Add some specific wrong answers
    wrong_options = [
        [correct_order[2], correct_order[1], correct_order[0]],  # Reverse order
        [correct_order[1], correct_order[0], correct_order[2]],  # Swap first two
        [correct_order[0], correct_order[2], correct_order[1]],  # Swap last two
    ]
    
    for wrong_option in wrong_options:
        if wrong_option not in options and len(options) < 4:
            options.append(wrong_option)
    
    # Fill remaining slots with random permutations
    for perm in all_perms:
        if list(perm) not in options and len(options) < 4:
            options.append(list(perm))
    
    st.session_state.question_data = {
        "story": story,
        "question": "Order the items from lightest to heaviest:",
        "options": options[:4],
        "correct_answer": correct_order,
        "explanation": f"Ordering by weight: {', '.join([f'{obj} ({weight} kg)' for obj, weight in sorted_objects])}",
        "question_type": "order_weights"
    }

def display_question():
    """Display the current question interface"""
    data = st.session_state.question_data
    
    # Display story
    st.markdown("### 📖 Story:")
    st.markdown(f"{data['story']}")
    
    # Display table if it exists
    if 'table_data' in data:
        st.markdown("### 📊 Data:")
        
        # Create a proper DataFrame table instead of HTML
        import pandas as pd
        
        # Create DataFrame from table data
        df = pd.DataFrame(data['table_data'], columns=['Person/Item', 'Value'])
        
        # Display as a nice streamlit table
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Display question with better highlighting
    st.markdown("### ❓ Question:")
    st.markdown(f"""
    <div style="
        background-color: #fff3cd; 
        padding: 20px; 
        border-radius: 10px; 
        border-left: 5px solid #ffc107;
        font-size: 18px;
        font-weight: bold;
        margin: 20px 0;
        color: #856404;
    ">
        {data['question']}
    </div>
    """, unsafe_allow_html=True)
    
    # Answer selection OUTSIDE of form
    st.markdown("**Choose your answer:**")
    
    # Handle different answer types with clickable tiles
    if data['question_type'] in ['order_prices', 'order_weights', 'order_distances']:
        # Create clickable tiles for ordering
        st.markdown("**Click on the correct order:**")
        
        for i, option in enumerate(data['options']):
            if isinstance(option, list):
                option_display = ' → '.join(option)
            else:
                option_display = str(option)
            
            # Create a clickable tile
            tile_key = f"order_option_{i}"
            if st.button(
                option_display,
                key=tile_key,
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.selected_answer = option
                # REMOVED: st.rerun() - This was causing the issue
    else:
        # Create clickable tiles for other question types
        cols = st.columns(min(len(data['options']), 4))
        
        for i, option in enumerate(data['options']):
            col_index = i % len(cols)
            with cols[col_index]:
                if st.button(
                    str(option),
                    key=f"option_{i}",
                    use_container_width=True,
                    type="secondary"
                ):
                    st.session_state.selected_answer = option
                    # REMOVED: st.rerun() - This was causing the issue
    
    # Show selected answer
    if 'selected_answer' in st.session_state:
        st.success(f"**Selected:** {st.session_state.selected_answer}")
    
    # Submit button appears only when answer is selected AND feedback is not shown
    if ('selected_answer' in st.session_state and 
        not st.session_state.show_feedback and 
        not st.session_state.answer_submitted):
        
        with st.form("submit_form", clear_on_submit=False):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("✅ Submit Answer", type="primary", use_container_width=True)
            
            if submit_button:
                st.session_state.user_answer = st.session_state.selected_answer
                st.session_state.show_feedback = True
                st.session_state.answer_submitted = True
                if 'selected_answer' in st.session_state:
                    del st.session_state.selected_answer
                st.rerun()
    
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
    # Check if we have the necessary data
    if 'user_answer' not in st.session_state or 'question_data' not in st.session_state:
        st.error("Error: Missing answer or question data")
        return
    
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.question_data['correct_answer']
    
    if user_answer == correct_answer:
        st.success("🎉 **Excellent! That's correct!**")
        
        # Increase difficulty (max 3 decimal places)
        old_difficulty = st.session_state.decimals_difficulty
        st.session_state.decimals_difficulty = min(st.session_state.decimals_difficulty + 1, 3)
        
        if st.session_state.decimals_difficulty == 3 and old_difficulty < 3:
            st.balloons()
            st.info("🏆 **Outstanding! You've mastered 3 decimal places!**")
        elif old_difficulty < st.session_state.decimals_difficulty:
            st.info(f"⬆️ **Difficulty increased! Now working with {st.session_state.decimals_difficulty} decimal places**")
    
    else:
        st.error("❌ **Not quite right.**")
        
        # Show correct answer
        st.info(f"**Correct answer:** {correct_answer}")
        
        # Decrease difficulty (min 1 decimal place)
        old_difficulty = st.session_state.decimals_difficulty
        st.session_state.decimals_difficulty = max(st.session_state.decimals_difficulty - 1, 1)
        
        if old_difficulty > st.session_state.decimals_difficulty:
            st.warning(f"⬇️ **Difficulty decreased to {st.session_state.decimals_difficulty} decimal place{'s' if st.session_state.decimals_difficulty > 1 else ''}. Keep practicing!**")
    
    # Show explanation
    show_explanation()

def show_explanation():
    """Show explanation for the correct answer"""
    explanation = st.session_state.question_data['explanation']
    
    with st.expander("📖 **Click here for explanation**", expanded=True):
        st.markdown(f"### {explanation}")
        
        # Add additional tips based on question type
        question_type = st.session_state.question_data['question_type']
        
        if question_type in ['compare_weights', 'compare_measurements', 'compare_times']:
            st.markdown("""
            ### 💡 Comparison Tips:
            - **Line up decimal points** when comparing
            - **Add zeros** to make the same number of decimal places
            - **Compare from left to right**, digit by digit
            - **Remember**: 0.7 = 0.70 = 0.700
            """)
        
        elif question_type in ['order_prices', 'order_weights', 'order_distances']:
            st.markdown("""
            ### 💡 Ordering Tips:
            - **Compare pairs** of numbers first
            - **Line up decimal points** and compare digit by digit
            - **Start with the leftmost digit** and work right
            - **Use number lines** to visualize the order
            """)
        
        elif question_type in ['round_measurement', 'round_score']:
            st.markdown("""
            ### 💡 Rounding Tips:
            - **Find the rounding place** (tenths, hundredths, etc.)
            - **Look at the digit to the right** of the rounding place
            - **If it's 5 or greater**, round up
            - **If it's less than 5**, round down
            """)

def reset_question_state():
    """Reset the question state for next question"""
    st.session_state.current_question = "new"  # Reset to "new" so new question generates
    st.session_state.correct_answer = None
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.question_data = {}
    
    # Clear answer-related session state
    keys_to_remove = ['user_answer', 'selected_answer']
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]