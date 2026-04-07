from data_generator import generate_variance_data

def get_task():
    data = generate_variance_data()
    return {
        "task_id": "budget_variance",
        "difficulty": "medium",
        "data": data,
        "question": f"Calculate Sales and Expense Variances. Budget Sales: {data['budget_sales']}, Actual Sales: {data['actual_sales']}, Budget Exp: {data['budget_expenses']}, Actual Exp: {data['actual_expenses']}. Also identify if Favorable (F) or Adverse (A)."
    }

def grade(data, action):
    # Logic: Sales Variance = Actual - Budget (Positive is Favorable)
    # Logic: Expense Variance = Budget - Actual (Positive is Favorable)
    correct_sales_var = data["actual_sales"] - data["budget_sales"]
    correct_exp_var = data["budget_expenses"] - data["actual_expenses"]

    agent_sv = action.get("sales_variance", 0)
    agent_ev = action.get("expense_variance", 0)
    agent_sfa = action.get("sales_fa", "").upper()
    agent_efa = action.get("expense_fa", "").upper()

    reward = 0.0
    tol_s = abs(correct_sales_var * 0.01)
    tol_e = abs(correct_exp_var * 0.01)

    # 0.34 for Sales Var
    if abs(agent_sv - correct_sales_var) <= tol_s:
        reward += 0.34
    
    # 0.33 for Exp Var
    if abs(agent_ev - correct_exp_var) <= tol_e:
        reward += 0.33

    # 0.33 for F/A check
    correct_sfa = "F" if correct_sales_var >= 0 else "A"
    correct_efa = "F" if correct_exp_var >= 0 else "A"
    if agent_sfa == correct_sfa and agent_efa == correct_efa:
        reward += 0.33

    return round(reward, 2)