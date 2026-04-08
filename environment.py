import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from tasks import task1_pl as pl_task
from tasks import task2_variance as var_task
from tasks import task3_depreciation as dep_task

class CAAccountingEnv:
    """
    Standard OpenEnv Environment for Financial Accounting Tasks.
    Strictly follows Phase 2 score validation: 0 < reward < 1 (exclusive bounds)
    """
    def __init__(self):
        self.registry = [pl_task, var_task, dep_task]
        self.current_module = None
        self.observation = None
        self.steps = 0
        self.is_active = False

    def reset(self):
        """Resets the environment for a new session."""
        self.current_module = random.choice(self.registry)
        self.observation = self.current_module.get_task()
        self.steps = 0
        self.is_active = True
        return self.observation

    def step(self, action):
        """
        Validates action and returns reward strictly between 0 and 1.
        CRITICAL: Score must be > 0.0 AND < 1.0 (NOT equal to 0.0 or 1.0)
        """
        if not self.is_active:
            raise Exception("Environment not initialized. Call reset() first.")

        # Get raw score from grader
        raw_reward = self.current_module.grade(
            self.observation["data"], 
            action
        )
        
        # CRITICAL FIX FOR PHASE 2:
        # Ensure score is STRICTLY between 0 and 1
        # Using 0.01 and 0.99 as safe bounds to avoid exact 0.0 or 1.0
        raw_float = float(raw_reward)
        
        # Clamp to valid range
        if raw_float <= 0.0:
            reward = 0.01
        elif raw_float >= 1.0:
            reward = 0.99
        else:
            reward = raw_float
        
        # Additional safeguard: round to avoid floating point issues
        reward = round(reward, 4)
        
        # Validate final score
        if not (0.0 < reward < 1.0):
            raise ValueError(
                f"Invalid reward score: {reward}. "
                f"Must be strictly between 0 and 1 (not equal to boundaries)"
            )
        
        self.steps += 1
        self.is_active = False 
        
        return {
            "observation": self.observation,
            "reward": reward,
            "done": True,
            "info": {
                "task_type": self.observation["task_id"],
                "raw_score": raw_float,
                "final_score": reward
            }
        }

    def state(self):
        """Returns the current environment state."""
        return {
            "current_task": self.observation["task_id"] if self.observation else None,
            "status": "active" if self.is_active else "completed",
            "steps": self.steps
        }
