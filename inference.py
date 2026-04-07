import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv  # Added this for local env support
from environment import CAAccountingEnv

# Setup professional logging for hackathon compliance
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AccountingAgent")

# 1. CLIENT INITIALIZATION
# loading .env here to ensure GROQ_API_KEY is available before client starts
load_dotenv() 

agent_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

def run_ca_baseline_eval():
    """
    Evaluates the environment using a high-precision LLM.
    Strictly follows the [START], [STEP], [END] protocol.
    """
    accounting_env = CAAccountingEnv()
    
    # Running 3 evaluation loops (Easy, Medium, Hard tasks)
    for run_idx in range(3):
        # 2. RESET PHASE - Starting a new task session
        current_obs = accounting_env.reset()
        task_id = current_obs["task_id"]
        
        # MANDATORY LOGGING: Marks the beginning of evaluation
        print(f"[START] task_id={task_id} seed={run_idx}")

        # Task Context & Prompting Logic
        system_instruction = (
            f"Context: {current_obs['question']}\n"
            f"Financial Data: {current_obs['data']}\n"
            f"Action: Solve the accounting problem and return ONLY a JSON object."
        )

        try:
            # 3. INFERENCE PHASE - Calling Groq Llama3
            inference_response = agent_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": system_instruction}],
                temperature=0.0, 
                response_format={"type": "json_object"}
            )

            # Parsing the LLM output
            ai_output = json.loads(inference_response.choices[0].message.content)
            
            # 4. STEP PHASE - Validation by the CA environment
            step_data = accounting_env.step(ai_output)
            
            # MANDATORY LOGGING: Outputting step metrics
            print(f"[STEP] step=1")
            print(f"  action: {ai_output}")
            print(f"  reward: {step_data['reward']}")
            print(f"  done: {str(step_data['done']).lower()}")

            # Task Completion Summary
            print(f"[END] task={task_id} total_reward={step_data['reward']} steps=1\n")

        except Exception as err:
            # Error handling for API or parsing issues
            logger.error(f"Critical error during task {task_id}: {err}")
            print(f"[END] task={task_id} status=CRASHED\n")

if __name__ == "__main__":
    # Starting the evaluation script
    run_ca_baseline_eval()