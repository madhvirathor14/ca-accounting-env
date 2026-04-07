from data_generator import generate_pl_data

def get_task():
    data = generate_pl_data()
    return {
        "task_id": "profit_loss",
        "difficulty": "easy",
        "data": data,
        "question": f"Calculate Gross Profit and Net Profit. Sales: {data['sales']}, COGS: {data['cogs']}, Expenses: {data['expenses']}"
    }

def grade(data, action):
    # Sahi answers (Answer Key)
    correct_gp = data["sales"] - data["cogs"]
    correct_np = correct_gp - data["expenses"]

    # AI ne kya bheja (Action)
    # Hum .get() use kar rahe hain taaki agar AI galat key bheje toh crash na ho
    agent_gp = action.get("gross_profit", 0)
    agent_np = action.get("net_profit", 0)

    reward = 0.0
    tolerance_gp = abs(correct_gp * 0.01) # 1% tolerance
    tolerance_np = abs(correct_np * 0.01)

    # GP ke liye 0.5 marks
    if abs(agent_gp - correct_gp) <= tolerance_gp:
        reward += 0.5
    
    # NP ke liye 0.5 marks
    if abs(agent_np - correct_np) <= tolerance_np:
        reward += 0.5

    return round(reward, 2)