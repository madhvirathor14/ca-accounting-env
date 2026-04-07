import random

# Task 1: Profit & Loss ke liye random data
def generate_pl_data():
    sales = random.randint(100000, 1000000)
    cogs_pc = random.uniform(0.4, 0.6)  # COGS is 40% to 60% of sales
    expenses_pc = random.uniform(0.1, 0.2) # Expenses are 10% to 20%
    
    return {
        "sales": round(sales, 2),
        "cogs": round(sales * cogs_pc, 2),
        "expenses": round(sales * expenses_pc, 2)
    }

# Task 2: Budget Variance ke liye random data
def generate_variance_data():
    budget_sales = random.randint(200000, 800000)
    # Actual sales variation +/- 25%
    actual_sales = budget_sales * random.uniform(0.75, 1.25) 
    
    budget_expenses = random.randint(50000, 300000)
    # Actual expense variation +/- 15%
    actual_expenses = budget_expenses * random.uniform(0.85, 1.15)
    
    return {
        "budget_sales": round(budget_sales, 2),
        "actual_sales": round(actual_sales, 2),
        "budget_expenses": round(budget_expenses, 2),
        "actual_expenses": round(actual_expenses, 2)
    }

# Task 3: Depreciation ke liye random data
def generate_depreciation_data():
    cost = random.randint(50000, 500000)
    useful_life = random.randint(3, 10)
    salvage = round(cost * 0.10, 2) # 10% scrap value
    rate = random.choice([10, 15, 20, 25])
    method = random.choice(["SLM", "WDV"])
    
    return {
        "cost": cost,
        "useful_life": useful_life,
        "salvage": salvage,
        "rate": rate,
        "method": method
    }