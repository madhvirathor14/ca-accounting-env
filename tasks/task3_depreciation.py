from data_generator import generate_depreciation_data

def get_task():
    data = generate_depreciation_data()
    return {
        "task_id": "depreciation",
        "difficulty": "hard",
        "data": data,
        "question": f"Asset Cost: {data['cost']}, Useful Life: {data['useful_life']} years, Salvage Value: {data['salvage']}, Rate: {data['rate']}%, Method: {data['method']}. Calculate Year 1 Dep, Year 2 Dep, and Book Value at end of Year 2."
    }

def grade(data, action):
    cost = data["cost"]
    salvage = data["salvage"]
    life = data["useful_life"]
    rate = data["rate"]
    method = data["method"]

    # --- ANSWER KEY CALCULATION ---
    if method == "SLM":
        # Straight Line Method: (Cost - Salvage) / Life
        annual_dep = (cost - salvage) / life
        correct_y1_dep = annual_dep
        correct_y2_dep = annual_dep
        correct_book_val = cost - (2 * annual_dep)
    else:
        # Written Down Value (WDV) Method
        correct_y1_dep = cost * (rate / 100)
        book_val_y1 = cost - correct_y1_dep
        correct_y2_dep = book_val_y1 * (rate / 100)
        correct_book_val = book_val_y1 - correct_y2_dep

    # --- AGENT ANSWERS ---
    agent_y1 = action.get("year1_depreciation", 0)
    agent_y2 = action.get("year2_depreciation", 0)
    agent_bv = action.get("year2_book_value", 0)
    agent_method = action.get("method", "").upper()

    reward = 0.0
    tol = 0.01 # 1% Tolerance

    # 1. Method identification (0.25)
    if agent_method == method:
        reward += 0.25
    
    # 2. Year 1 Dep (0.25)
    if abs(agent_y1 - correct_y1_dep) <= (correct_y1_dep * tol):
        reward += 0.25
    
    # 3. Year 2 Dep (0.25)
    if abs(agent_y2 - correct_y2_dep) <= (correct_y2_dep * tol):
        reward += 0.25

    # 4. Final Book Value (0.25)
    if abs(agent_bv - correct_book_val) <= (correct_book_val * tol):
        reward += 0.25

    return round(reward, 2)