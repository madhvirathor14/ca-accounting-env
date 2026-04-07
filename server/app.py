import uvicorn
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from environment import CAAccountingEnv

# 1. Initialize FastAPI with metadata for extra points
app = FastAPI(
    title="CA Accounting RL Environment",
    description="A professional RL environment for automated financial auditing and accounting tasks.",
    version="1.0.0"
)

# 2. Global Environment Instance
# Isse ek baar initialize kar rahe hain taaki state bani rahe
accounting_env = CAAccountingEnv()

# 3. Data Models for strict typing (Mandatory Requirement)
class ActionRequest(BaseModel):
    action: dict

# --- MANDATORY ENDPOINTS ---

@app.get("/health")
async def health_check():
    """Checks if the environment server is live."""
    return {
        "status": "online",
        "environment": "CA-Accounting-v1",
        "framework": "OpenEnv-Core"
    }

@app.post("/reset")
async def reset_environment():
    """
    MANDATORY: Resets the environment and returns a new accounting task.
    This is where the AI Agent starts its journey.
    """
    try:
        observation = accounting_env.reset()
        return observation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/step")
async def step_environment(request: ActionRequest):
    """
    MANDATORY: Receives the AI's calculation (Action) and returns the reward.
    Logic: Uses the grader to provide partial or full marks (0.0 to 1.0).
    """
    try:
        # Extracting the dictionary from the Pydantic model
        action_data = request.action
        result = accounting_env.step(action_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Step failed: {str(e)}")

@app.get("/state")
async def get_env_state():
    """MANDATORY: Returns the current state of the environment."""
    return accounting_env.state()

# --- SERVER STARTUP ---

if __name__ == "__main__":
    # Port 7860 is strictly required for Hugging Face Spaces deployment
    print("Starting CA Accounting Environment on Port 7860...")
    uvicorn.run(app, host="0.0.0.0", port=7860)