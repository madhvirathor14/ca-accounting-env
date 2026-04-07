import random
# Humne modules ko 'as' use karke rename kiya hai taaki code padhne mein professional lage
from tasks import task1_pl as pl_task
from tasks import task2_variance as var_task
from tasks import task3_depreciation as dep_task

class CAAccountingEnv:
    """
    Standard OpenEnv Environment for Financial Accounting Tasks.
    Yeh class AI Agent ke liye 'Exam Hall' ka kaam karti hai.
    """
    def __init__(self):
        # Registering all available accounting modules
        self.registry = [pl_task, var_task, dep_task]
        self.current_module = None
        self.observation = None
        self.steps = 0
        self.is_active = False

    def reset(self):
        """
        MANDATORY: Har naye session ke liye environment ko clean karta hai.
        """
        # Ek random accounting area select karna
        self.current_module = random.choice(self.registry)
        
        # Task data generate karwana
        self.observation = self.current_module.get_task()
        
        # State reset
        self.steps = 0
        self.is_active = True
        
        return self.observation

    def step(self, action):
        """
        MANDATORY: AI ke answer ko validate karke reward return karta hai.
        """
        if not self.is_active:
            raise Exception("Environment not initialized. Call reset() first.")

        # Task-specific grader se marks (reward) nikalna
        reward = self.current_module.grade(
            self.observation["data"], 
            action
        )
        
        self.steps += 1
        self.is_active = False # Single-turn logic for accounting
        
        return {
            "observation": self.observation,
            "reward": reward,
            "done": True,
            "info": {"task_type": self.observation["task_id"]}
        }

    def state(self):
        """MANDATORY: Current context return karta hai."""
        return {
            "current_task": self.observation["task_id"] if self.observation else None,
            "status": "active" if self.is_active else "completed",
            "usage": f"Steps taken: {self.steps}"
        }