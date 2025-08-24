import streamlit as st
import random

def run():
    """
    Main function to run the Multi-step word problems: identify reasonable answers activity.
    This gets called when the subtopic is loaded from:
    Grades/Year 5/L.Problem_solving/multistep_word_problems_identify_reasonable_answers.py
    """
    # Initialize session state
    if "reasonable_difficulty" not in st.session_state:
        st.session_state.reasonable_difficulty = 1
    
    if "current_problem" not in st.session_state:
        st.session_state.current_problem = None
        st.session_state.problem_data = {}
        st.session_state.show_feedback = False
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.consecutive_correct = 0
    
    # Page header with breadcrumb
    st.markdown("**📚 Year 5 > L. Problem solving**")
    st.title("🎯 Identify Reasonable Answers")
    st.markdown("*Estimate to check if answers make sense*")
    st.markdown("---")
    
    # Difficulty indicator
    difficulty_level = st.session_state.reasonable_difficulty
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        difficulty_names = ["Basic Estimation", "Multi-Step", "Complex Scenarios", "Advanced", "Master"]
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
    if st.session_state.current_problem is None:
        generate_new_reasonable_problem()
    
    # Display current problem
    display_reasonable_problem()
    
    # Instructions section
    st.markdown("---")
    with st.expander("💡 **Estimation Strategies Guide**", expanded=False):
        st.markdown("""
        ### How to Check if Estimates are Reasonable:
        
        **1. Round Numbers** 🔄
        - Round to nearest 10, 100, or easy number
        - $798 → $800, 38 people → 40 people
        
        **2. Use Compatible Numbers** 🎯
        - Change to numbers that work well together
        - 19 × 4 → 20 × 4 = 80
        
        **3. Front-End Estimation** 📊
        - Focus on the largest place values
        - 467 + 382 → 400 + 300 = 700
        
        **4. Benchmark Numbers** 📏
        - Use familiar amounts as reference
        - Is $100/week reasonable for rent?
        - Think: 4 weeks × $100 = $400/month
        
        ### Common Estimation Checks:
        
        **Too High:**
        - Overestimated quantities
        - Used larger rounding
        - Forgot to divide/share
        
        **Too Low:**
        - Underestimated quantities
        - Missed some items
        - Forgot to multiply
        
        **Just Right:**
        - Close to actual calculation
        - Makes sense in context
        - Reasonable for the situation
        
        ### Quick Mental Math Tips:
        
        **Weekly ↔ Monthly:**
        - Week to month: × 4 (approximately)
        - Month to week: ÷ 4
        
        **Daily ↔ Yearly:**
        - School year ≈ 180 days
        - Full year = 365 days
        - Work year ≈ 250 days
        
        **Groups and Sets:**
        - Dozen = 12
        - Score = 20
        - Pairs/couples = × 2
        
        ### Example:
        "Rent is $798/month, split between 2 people"
        - $798 ÷ 2 ≈ $800 ÷ 2 = $400 per person
        - $400 ÷ 4 weeks = $100/week
        - Estimate of $100/week is reasonable ✓
        """)

def generate_reasonable_scenarios():
    """Generate diverse scenarios for reasonable answer problems"""
    return {
        "housing_costs": [
            {
                "template": "{name} and {pronoun_poss} roommate rent an apartment for ${rent} a month. Each of them pays half.\n\n{image_placeholder}\n\nBecause there are about 4 weeks in a month, {name} estimates {pronoun_poss} share of the rent is about ${estimate} a week. Is that a good estimate?",
                "names": [
                    ("Michelle", "her", "her"),
                    ("David", "his", "his"),
                    ("Jordan", "their", "their")
                ],
                "calculation": "rent_split_weekly",
                "factors": ["rent", "weeks_per_month"]
            },
            {
                "template": "The {family} family's mortgage is ${mortgage} per month. They budget ${estimate} per day for housing costs. Is this a reasonable estimate?",
                "families": ["Johnson", "Patel", "Martinez", "Chen"],
                "calculation": "monthly_to_daily",
                "factors": ["mortgage", "days_per_month"]
            }
        ],
        
        "collection_drives": [
            {
                "template": "{name}'s youth group is collecting {items} to take to the {location}. There are {people} people in the group, and they each gave {per_person} {items}. They got an additional {extra} by asking door-to-door. They set up boxes at schools and got another {school_extra}. {name} works out that they have collected a total of {estimate} {items}. Does that sound about right?",
                "names": ["Greg", "Lisa", "Sam"],
                "items": ["blankets", "canned goods", "books", "toys"],
                "locations": ["animal shelter", "food bank", "library", "children's hospital"],
                "calculation": "collection_total",
                "factors": ["people", "per_person", "extra", "school_extra"]
            },
            {
                "template": "The school is collecting {items} for charity. {class1} collected {qty1}, {class2} collected {qty2}, and {class3} collected {qty3}. The principal estimates they have about {estimate} {items} total. Is this a good estimate?",
                "items": ["box tops", "aluminum cans", "plastic bottles", "newspapers"],
                "classes": ["Grade 3", "Grade 4", "Grade 5", "Grade 6"],
                "calculation": "simple_sum",
                "factors": ["qty1", "qty2", "qty3"]
            }
        ],
        
        "family_outings": [
            {
                "template": "Zoo tickets cost ${child_price} for a child and ${adult_price} for an adult.\n\n{image_placeholder}\n\nMr {last_name}, Mrs {last_name}, and their kids estimate it will cost roughly ${estimate} for their family of {family_size} to visit the zoo. Is that a good estimate?",
                "last_names": ["Carter", "Wilson", "Anderson", "Thompson"],
                "calculation": "family_tickets",
                "factors": ["child_price", "adult_price", "children", "adults"]
            },
            {
                "template": "A family of {family_size} is going to the movies. Tickets are ${ticket_price} each, and they plan to buy {snack_sets} combo meals at ${snack_price} each. They estimate the total cost will be about ${estimate}. Is this reasonable?",
                "calculation": "movies_total",
                "factors": ["family_size", "ticket_price", "snack_sets", "snack_price"]
            }
        ],
        
        "school_supplies": [
            {
                "template": "Ms {name} is a teacher with {students} students. Every school day, Ms {name} prints out {pages} pages of worksheets for each of them. There are {school_days} school days left in this school year. Ms {name} works out that she will need to print a total of {estimate} pages in this time. Does that sound about right?",
                "names": ["Miller", "Garcia", "Davis", "Rodriguez"],
                "calculation": "teacher_printing",
                "factors": ["students", "pages", "school_days"]
            },
            {
                "template": "The art teacher needs to order supplies for {students} students. Each student needs {brushes} paintbrushes at ${brush_price} each and {paint_sets} paint sets at ${paint_price} each. The teacher estimates the total cost will be about ${estimate}. Is this a reasonable estimate?",
                "calculation": "art_supplies",
                "factors": ["students", "brushes", "brush_price", "paint_sets", "paint_price"]
            }
        ],
        
        "shopping": [
            {
                "template": "{name} is shopping for a party. {pronoun_cap} buys {qty1} {item1} at ${price1} each, {qty2} {item2} at ${price2} each, and {qty3} {item3} at ${price3} each. {pronoun_cap} estimates the total will be about ${estimate}. Is this a good estimate?",
                "names": [
                    ("Sarah", "She", "she"),
                    ("Mike", "He", "he"),
                    ("Alex", "They", "they")
                ],
                "items": [
                    ("pizzas", "bottles of soda", "bags of chips"),
                    ("cakes", "ice cream tubs", "cookie packs"),
                    ("sandwich platters", "fruit trays", "veggie trays")
                ],
                "calculation": "shopping_total",
                "factors": ["qty1", "price1", "qty2", "price2", "qty3", "price3"]
            }
        ],
        
        "travel": [
            {
                "template": "The {family} family is driving to visit relatives {distance} miles away. Their car gets about {mpg} miles per gallon, and gas costs ${gas_price} per gallon. They estimate the round trip will cost about ${estimate} in gas. Is this reasonable?",
                "families": ["Smith", "Brown", "Taylor", "White"],
                "calculation": "gas_cost",
                "factors": ["distance", "mpg", "gas_price"]
            },
            {
                "template": "A school bus holds {capacity} students. The school has {total_students} students going on a field trip. The principal estimates they need {estimate} buses. Is this a good estimate?",
                "calculation": "buses_needed",
                "factors": ["total_students", "capacity"]
            }
        ],
        
        "time_based": [
            {
                "template": "{name} practices piano {minutes} minutes every day. Over a {time_period}, {pronoun} estimates {pronoun} will practice for about {estimate} hours total. Is this a reasonable estimate?",
                "names": [
                    ("Emma", "she", "she"),
                    ("Noah", "he", "he"),
                    ("Casey", "they", "they")
                ],
                "time_periods": ["week", "month", "semester"],
                "calculation": "practice_time",
                "factors": ["minutes", "days"]
            },
            {
                "template": "The cafeteria serves about {meals_per_day} meals each school day. With {school_days} days left in the school year, they estimate they'll serve about {estimate} more meals this year. Does this sound right?",
                "calculation": "cafeteria_meals",
                "factors": ["meals_per_day", "school_days"]
            }
        ],
        
        "production": [
            {
                "template": "A bakery makes {batches} batches of cookies each day. Each batch has {per_batch} cookies. In a {day_period}-day work week, they estimate they make about {estimate} cookies. Is this a good estimate?",
                "calculation": "production_total",
                "factors": ["batches", "per_batch", "day_period"]
            },
            {
                "template": "A factory produces {per_hour} widgets per hour. Running {hours} hours a day for {days} days, they estimate production of about {estimate} widgets. Is this reasonable?",
                "calculation": "factory_production",
                "factors": ["per_hour", "hours", "days"]
            }
        ]
    }

def generate_new_reasonable_problem():
    """Generate a new reasonable answer problem based on difficulty"""
    difficulty = st.session_state.reasonable_difficulty
    scenarios = generate_reasonable_scenarios()
    
    # Choose scenario types based on difficulty
    if difficulty == 1:
        scenario_types = ["housing_costs", "family_outings", "school_supplies"]
    elif difficulty == 2:
        scenario_types = ["collection_drives", "shopping", "time_based"]
    elif difficulty == 3:
        scenario_types = ["shopping", "travel", "production"]
    elif difficulty == 4:
        scenario_types = ["travel", "time_based", "production", "collection_drives"]
    else:  # difficulty == 5
        scenario_types = list(scenarios.keys())
    
    scenario_type = random.choice(scenario_types)
    scenario = random.choice(scenarios[scenario_type])
    
    # Generate numbers and calculate actual vs estimate
    problem_text = scenario["template"]
    calculation_type = scenario["calculation"]
    
    # Initialize correct_answer to avoid undefined variable error
    correct_answer = "Yes."
    
    # Generate appropriate numbers based on calculation type and difficulty
    if calculation_type == "rent_split_weekly":
        rent = random.randint(600, 1200) if difficulty <= 2 else random.randint(1200, 2400)
        actual_weekly = (rent / 2) / 4
        
        # Generate estimate that could be reasonable, too high, or too low
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_weekly / 10) * 10
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_weekly * random.uniform(1.5, 2.0) / 10) * 10
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_weekly * random.uniform(0.4, 0.6) / 10) * 10
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{rent}", str(rent))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "monthly_to_daily":
        mortgage = random.randint(1200, 2400) if difficulty <= 2 else random.randint(2000, 4000)
        actual_daily = mortgage / 30
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_daily)
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_daily * random.uniform(1.5, 2.5))
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_daily * random.uniform(0.3, 0.6))
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{mortgage}", str(mortgage))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "collection_total":
        people = random.randint(30, 50) if difficulty <= 3 else random.randint(40, 80)
        per_person = random.randint(2, 4)
        extra = random.randint(20, 40)
        school_extra = random.randint(40, 80)
        
        actual_total = (people * per_person) + extra + school_extra
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_total / 10) * 10
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_total * random.uniform(1.3, 1.8) / 10) * 10
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_total * random.uniform(0.5, 0.7) / 10) * 10
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{people}", str(people))
        problem_text = problem_text.replace("{per_person}", str(per_person))
        problem_text = problem_text.replace("{extra}", str(extra))
        problem_text = problem_text.replace("{school_extra}", str(school_extra))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "simple_sum":
        qty1 = random.randint(100, 300)
        qty2 = random.randint(150, 350)
        qty3 = random.randint(200, 400)
        
        actual_total = qty1 + qty2 + qty3
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_total / 50) * 50
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_total * random.uniform(1.3, 1.8) / 50) * 50
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_total * random.uniform(0.4, 0.7) / 50) * 50
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{qty1}", str(qty1))
        problem_text = problem_text.replace("{qty2}", str(qty2))
        problem_text = problem_text.replace("{qty3}", str(qty3))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "family_tickets":
        child_price = random.randint(15, 25) if difficulty <= 3 else random.randint(20, 35)
        adult_price = random.randint(25, 40) if difficulty <= 3 else random.randint(35, 55)
        family_size = random.randint(4, 6)
        adults = 2
        children = family_size - adults
        
        actual_total = (adults * adult_price) + (children * child_price)
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_total / 10) * 10
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_total * random.uniform(1.4, 1.9) / 10) * 10
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_total * random.uniform(0.4, 0.7) / 10) * 10
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{child_price}", str(child_price))
        problem_text = problem_text.replace("{adult_price}", str(adult_price))
        problem_text = problem_text.replace("{family_size}", str(family_size))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "movies_total":
        family_size = random.randint(3, 6)
        ticket_price = random.randint(8, 15)
        snack_sets = random.randint(2, family_size)
        snack_price = random.randint(12, 20)
        
        actual_total = (family_size * ticket_price) + (snack_sets * snack_price)
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_total / 10) * 10
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_total * random.uniform(1.4, 2.0) / 10) * 10
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_total * random.uniform(0.4, 0.7) / 10) * 10
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{family_size}", str(family_size))
        problem_text = problem_text.replace("{ticket_price}", str(ticket_price))
        problem_text = problem_text.replace("{snack_sets}", str(snack_sets))
        problem_text = problem_text.replace("{snack_price}", str(snack_price))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "teacher_printing":
        students = random.randint(20, 35)
        pages = random.randint(2, 4)
        school_days = random.randint(60, 100) if difficulty <= 3 else random.randint(100, 180)
        
        actual_total = students * pages * school_days
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            # For larger numbers, round more loosely
            if actual_total > 5000:
                estimate = round(actual_total / 1000) * 1000
            else:
                estimate = round(actual_total / 100) * 100
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_total * random.uniform(1.5, 2.5) / 100) * 100
            correct_answer = "No, it is much too high."
        else:
            # Make it clearly too low
            estimate = round(actual_total * random.uniform(0.2, 0.5) / 100) * 100
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{students}", str(students))
        problem_text = problem_text.replace("{pages}", str(pages))
        problem_text = problem_text.replace("{school_days}", str(school_days))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "art_supplies":
        students = random.randint(20, 35)
        brushes = random.randint(2, 4)
        brush_price = random.randint(2, 5)
        paint_sets = 1
        paint_price = random.randint(8, 15)
        
        actual_total = students * ((brushes * brush_price) + (paint_sets * paint_price))
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_total / 50) * 50
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_total * random.uniform(1.5, 2.2) / 50) * 50
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_total * random.uniform(0.3, 0.6) / 50) * 50
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{students}", str(students))
        problem_text = problem_text.replace("{brushes}", str(brushes))
        problem_text = problem_text.replace("{brush_price}", str(brush_price))
        problem_text = problem_text.replace("{paint_sets}", str(paint_sets))
        problem_text = problem_text.replace("{paint_price}", str(paint_price))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "shopping_total":
        qty1 = random.randint(3, 8)
        price1 = random.randint(8, 20)
        qty2 = random.randint(4, 10)
        price2 = random.randint(3, 8)
        qty3 = random.randint(2, 6)
        price3 = random.randint(5, 15)
        
        actual_total = (qty1 * price1) + (qty2 * price2) + (qty3 * price3)
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_total / 10) * 10
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_total * random.uniform(1.4, 2.0) / 10) * 10
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_total * random.uniform(0.4, 0.7) / 10) * 10
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{qty1}", str(qty1))
        problem_text = problem_text.replace("{price1}", str(price1))
        problem_text = problem_text.replace("{qty2}", str(qty2))
        problem_text = problem_text.replace("{price2}", str(price2))
        problem_text = problem_text.replace("{qty3}", str(qty3))
        problem_text = problem_text.replace("{price3}", str(price3))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "gas_cost":
        distance = random.randint(200, 500)
        mpg = random.randint(20, 35)
        gas_price = round(random.uniform(3.0, 4.5), 2)
        
        actual_cost = (distance * 2 / mpg) * gas_price  # Round trip
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_cost / 5) * 5
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_cost * random.uniform(1.8, 2.5) / 5) * 5
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_cost * random.uniform(0.3, 0.6) / 5) * 5
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{distance}", str(distance))
        problem_text = problem_text.replace("{mpg}", str(mpg))
        problem_text = problem_text.replace("{gas_price}", f"{gas_price:.2f}")
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "buses_needed":
        capacity = random.randint(40, 60)
        total_students = random.randint(150, 400)
        
        actual_buses = (total_students + capacity - 1) // capacity  # Ceiling division
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = actual_buses
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = actual_buses + random.randint(2, 4)
            correct_answer = "No, it is much too high."
        else:
            estimate = max(1, actual_buses - random.randint(1, 3))
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{capacity}", str(capacity))
        problem_text = problem_text.replace("{total_students}", str(total_students))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "practice_time":
        minutes = random.randint(20, 45)
        time_period = random.choice(scenario.get("time_periods", ["week"]))
        
        if time_period == "week":
            days = 7
        elif time_period == "month":
            days = 30
        else:  # semester
            days = 120
            
        actual_hours = (minutes * days) / 60
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_hours)
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_hours * random.uniform(1.5, 2.5))
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_hours * random.uniform(0.3, 0.6))
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{minutes}", str(minutes))
        problem_text = problem_text.replace("{time_period}", time_period)
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "cafeteria_meals":
        meals_per_day = random.randint(200, 500)
        school_days = random.randint(60, 120)
        
        actual_total = meals_per_day * school_days
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            if actual_total > 10000:
                estimate = round(actual_total / 1000) * 1000
            else:
                estimate = round(actual_total / 500) * 500
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_total * random.uniform(1.5, 2.0) / 1000) * 1000
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_total * random.uniform(0.3, 0.6) / 1000) * 1000
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{meals_per_day}", str(meals_per_day))
        problem_text = problem_text.replace("{school_days}", str(school_days))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "production_total":
        batches = random.randint(10, 30)
        per_batch = random.randint(12, 48)  # Dozens
        day_period = 5
        
        actual_total = batches * per_batch * day_period
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            estimate = round(actual_total / 100) * 100
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_total * random.uniform(1.5, 2.5) / 100) * 100
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_total * random.uniform(0.3, 0.6) / 100) * 100
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{batches}", str(batches))
        problem_text = problem_text.replace("{per_batch}", str(per_batch))
        problem_text = problem_text.replace("{day_period}", str(day_period))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
        
    elif calculation_type == "factory_production":
        per_hour = random.randint(50, 200)
        hours = random.randint(8, 12)
        days = random.randint(5, 20)
        
        actual_total = per_hour * hours * days
        
        estimate_type = random.choice(["reasonable", "too_high", "too_low"])
        if estimate_type == "reasonable":
            if actual_total > 10000:
                estimate = round(actual_total / 1000) * 1000
            else:
                estimate = round(actual_total / 500) * 500
            correct_answer = "Yes."
        elif estimate_type == "too_high":
            estimate = round(actual_total * random.uniform(1.8, 2.5) / 1000) * 1000
            correct_answer = "No, it is much too high."
        else:
            estimate = round(actual_total * random.uniform(0.2, 0.5) / 1000) * 1000
            correct_answer = "No, it is much too low."
        
        problem_text = problem_text.replace("{per_hour}", str(per_hour))
        problem_text = problem_text.replace("{hours}", str(hours))
        problem_text = problem_text.replace("{days}", str(days))
        problem_text = problem_text.replace("{estimate}", str(int(estimate)))
    
    # Replace template placeholders
    if "names" in scenario:
        name_data = random.choice(scenario["names"])
        if isinstance(name_data, tuple):
            problem_text = problem_text.replace("{name}", name_data[0])
            if len(name_data) > 1:
                problem_text = problem_text.replace("{pronoun_poss}", name_data[1])
            if len(name_data) > 2:
                problem_text = problem_text.replace("{pronoun}", name_data[2])
                problem_text = problem_text.replace("{pronoun_cap}", name_data[2].capitalize())
        else:
            problem_text = problem_text.replace("{name}", name_data)
    
    # Replace other placeholders
    for key in ["families", "items", "locations", "classes", "last_names"]:
        if key in scenario:
            if key == "items" and isinstance(scenario["items"][0], tuple):
                item_set = random.choice(scenario["items"])
                problem_text = problem_text.replace("{item1}", item_set[0])
                problem_text = problem_text.replace("{item2}", item_set[1])
                problem_text = problem_text.replace("{item3}", item_set[2])
            else:
                value = random.choice(scenario[key])
                problem_text = problem_text.replace(f"{{{key[:-1]}}}", value)
                problem_text = problem_text.replace(f"{{{key}}}", value)
    
    # Replace specific values
    if "{family}" in problem_text:
        problem_text = problem_text.replace("{family}", random.choice(["Johnson", "Patel", "Garcia", "Chen"]))
    
    if "{last_name}" in problem_text:
        last_name = random.choice(["Carter", "Wilson", "Anderson", "Thompson"])
        problem_text = problem_text.replace("{last_name}", last_name)
    
    # Handle class replacements
    if "{class1}" in problem_text and "{class2}" in problem_text and "{class3}" in problem_text:
        classes = ["Grade 3", "Grade 4", "Grade 5", "Grade 6"]
        selected_classes = random.sample(classes, 3)
        problem_text = problem_text.replace("{class1}", selected_classes[0])
        problem_text = problem_text.replace("{class2}", selected_classes[1])
        problem_text = problem_text.replace("{class3}", selected_classes[2])
    
    # Add image placeholder
    problem_text = problem_text.replace("{image_placeholder}", "")
    
    # Store problem data
    st.session_state.problem_data = {
        "problem_text": problem_text,
        "correct_answer": correct_answer,
        "scenario_type": scenario_type,
        "calculation_type": calculation_type,
        "actual_value": locals().get('actual_total', locals().get('actual_weekly', locals().get('actual_cost', locals().get('actual_buses', locals().get('actual_hours', locals().get('actual_daily', 0))))))
    }
    st.session_state.current_problem = problem_text

def display_reasonable_problem():
    """Display the current reasonable answer problem"""
    problem_data = st.session_state.problem_data
    
    # Display problem with optional image
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(f"""
        <div style="
            background-color: #f8f9fa;
            border: 2px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            font-size: 16px;
            line-height: 1.8;
        ">
            {problem_data['problem_text']}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Scenario-specific image/emoji
        emoji = get_scenario_image(problem_data['scenario_type'])
        st.markdown(f"""
        <div style="
            background-color: #e3f2fd;
            border: 2px solid #90caf9;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <span style="font-size: 64px;">
                {emoji}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Answer buttons
    st.markdown("### Is this estimate reasonable?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Yes.", key="yes_btn", use_container_width=True):
            handle_answer("Yes.")
    
    with col2:
        if st.button("No, it is much too high.", key="high_btn", use_container_width=True):
            handle_answer("No, it is much too high.")
    
    with col3:
        if st.button("No, it is much too low.", key="low_btn", use_container_width=True):
            handle_answer("No, it is much too low.")
    
    # Show feedback if answer submitted
    if st.session_state.show_feedback:
        show_feedback()
        
        # Next problem button
        st.markdown("")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Next Problem", type="secondary", use_container_width=True):
                reset_problem_state()
                st.rerun()

def get_scenario_image(scenario_type):
    """Get emoji for different scenario types"""
    emoji_map = {
        "housing_costs": "🏠",
        "collection_drives": "📦",
        "family_outings": "🎢",
        "school_supplies": "📚",
        "shopping": "🛒",
        "travel": "🚗",
        "time_based": "⏰",
        "production": "🏭"
    }
    return emoji_map.get(scenario_type, "🔢")

def handle_answer(answer):
    """Handle user's answer selection"""
    st.session_state.user_answer = answer
    st.session_state.show_feedback = True
    st.session_state.answer_submitted = True

def show_feedback():
    """Display feedback for the submitted answer"""
    user_answer = st.session_state.user_answer
    correct_answer = st.session_state.problem_data["correct_answer"]
    
    if user_answer == correct_answer:
        st.success("✅ **Correct! Well done!**")
        st.session_state.consecutive_correct += 1
        
        # Increase difficulty after 3 consecutive correct answers
        if st.session_state.consecutive_correct >= 3:
            old_difficulty = st.session_state.reasonable_difficulty
            st.session_state.reasonable_difficulty = min(
                st.session_state.reasonable_difficulty + 1, 5
            )
            st.session_state.consecutive_correct = 0
            
            if st.session_state.reasonable_difficulty == 5 and old_difficulty < 5:
                st.balloons()
                st.info("🏆 **Fantastic! You've mastered estimation!**")
            elif old_difficulty < st.session_state.reasonable_difficulty:
                st.info(f"⬆️ **Level up! Now at Level {st.session_state.reasonable_difficulty}**")
    
    else:
        st.error(f"❌ **Not quite. The correct answer is: {correct_answer}**")
        st.session_state.consecutive_correct = 0
        
        # Decrease difficulty
        old_difficulty = st.session_state.reasonable_difficulty
        st.session_state.reasonable_difficulty = max(
            st.session_state.reasonable_difficulty - 1, 1
        )
        
        if old_difficulty > st.session_state.reasonable_difficulty:
            st.warning(f"⬇️ **Level decreased to {st.session_state.reasonable_difficulty}. Keep practicing!**")
        
        # Show explanation
        show_explanation()

def show_explanation():
    """Show detailed explanation of why the estimate is reasonable or not"""
    problem_data = st.session_state.problem_data
    correct_answer = problem_data["correct_answer"]
    
    with st.expander("📖 **See why**", expanded=True):
        st.markdown("### Let's check the estimate:")
        
        calculation_type = problem_data["calculation_type"]
        
        if calculation_type == "rent_split_weekly":
            st.markdown("""
            **Steps:**
            1. Monthly rent ÷ 2 people = each person's share
            2. Monthly share ÷ 4 weeks = weekly cost
            
            **Quick estimation:**
            - Round the rent to an easier number
            - Divide by 2, then by 4 (or divide by 8)
            """)
            
        elif calculation_type == "monthly_to_daily":
            st.markdown("""
            **Steps:**
            1. Monthly amount ÷ 30 days = daily cost
            
            **Quick estimation:**
            - Round to nearest hundred
            - Divide by 30 (or by 3, then by 10)
            """)
            
        elif calculation_type == "collection_total":
            st.markdown("""
            **Steps:**
            1. People × items per person = group collection
            2. Add door-to-door collection
            3. Add school collection
            4. Find total
            
            **Quick estimation:**
            - Round each number before calculating
            - Add the rounded numbers
            """)
            
        elif calculation_type == "simple_sum":
            st.markdown("""
            **Steps:**
            1. Add all quantities together
            
            **Quick estimation:**
            - Round each number to nearest 50 or 100
            - Add the rounded numbers
            """)
            
        elif calculation_type == "family_tickets":
            st.markdown("""
            **Steps:**
            1. Count adults and children
            2. Adults × adult price
            3. Children × child price
            4. Add both totals
            
            **Quick estimation:**
            - Round prices to nearest $5 or $10
            - Multiply and add
            """)
            
        elif calculation_type == "movies_total":
            st.markdown("""
            **Steps:**
            1. Family size × ticket price = ticket total
            2. Snack sets × snack price = snack total
            3. Add both totals
            
            **Quick estimation:**
            - Round prices to nearest $5 or $10
            - Calculate each part and add
            """)
            
        elif calculation_type == "teacher_printing":
            st.markdown("""
            **Steps:**
            1. Students × pages per day = daily total
            2. Daily total × school days = grand total
            
            **Quick estimation:**
            - Round to compatible numbers
            - For large results, estimate to nearest hundred or thousand
            """)
            
        elif calculation_type == "art_supplies":
            st.markdown("""
            **Steps:**
            1. Calculate cost per student: (brushes × price) + (paint × price)
            2. Multiply by number of students
            
            **Quick estimation:**
            - Round prices and calculate per-student cost
            - Multiply by student count
            """)
            
        elif calculation_type == "shopping_total":
            st.markdown("""
            **Steps:**
            1. Item 1: quantity × price
            2. Item 2: quantity × price
            3. Item 3: quantity × price
            4. Add all totals
            
            **Quick estimation:**
            - Round each price
            - Multiply and add
            """)
            
        elif calculation_type == "gas_cost":
            st.markdown("""
            **Steps:**
            1. Round trip distance = distance × 2
            2. Gallons needed = distance ÷ miles per gallon
            3. Total cost = gallons × price per gallon
            
            **Quick estimation:**
            - Round distance and mpg to easy numbers
            - Calculate gallons, then multiply by price
            """)
            
        elif calculation_type == "buses_needed":
            st.markdown("""
            **Steps:**
            1. Total students ÷ bus capacity = buses needed
            2. Round UP to next whole number (can't have partial buses!)
            
            **Quick estimation:**
            - Divide and round up
            - Remember: always need whole buses
            """)
            
        elif calculation_type == "practice_time":
            st.markdown("""
            **Steps:**
            1. Minutes per day × number of days = total minutes
            2. Total minutes ÷ 60 = hours
            
            **Quick estimation:**
            - Calculate total minutes
            - Divide by 60 for hours
            """)
            
        elif calculation_type == "cafeteria_meals":
            st.markdown("""
            **Steps:**
            1. Meals per day × school days = total meals
            
            **Quick estimation:**
            - Round to easy numbers
            - Multiply
            """)
            
        elif calculation_type == "production_total":
            st.markdown("""
            **Steps:**
            1. Batches per day × items per batch = daily production
            2. Daily production × work days = total production
            
            **Quick estimation:**
            - Calculate daily amount first
            - Multiply by days
            """)
            
        elif calculation_type == "factory_production":
            st.markdown("""
            **Steps:**
            1. Widgets per hour × hours per day = daily production
            2. Daily production × days = total production
            
            **Quick estimation:**
            - Calculate daily production
            - Multiply by number of days
            """)
        
        # Explain why the answer is correct
        if correct_answer == "Yes.":
            st.markdown("\n**Why it's reasonable:**")
            st.markdown("The estimate is close to the actual calculation. Good estimation!")
        elif "too high" in correct_answer:
            st.markdown("\n**Why it's too high:**")
            st.markdown("The estimate is significantly larger than the actual amount. Check if numbers were overestimated or if there was an error in calculation.")
        else:
            st.markdown("\n**Why it's too low:**")
            st.markdown("The estimate is significantly smaller than the actual amount. Some values might have been underestimated or missed.")

def reset_problem_state():
    """Reset the problem state for next question"""
    st.session_state.current_problem = None
    st.session_state.problem_data = {}
    st.session_state.show_feedback = False
    st.session_state.answer_submitted = False
    st.session_state.user_answer = None