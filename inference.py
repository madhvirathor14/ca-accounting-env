import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
from environment import CAAccountingEnv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AccountingAgent")

load_dotenv()

agent_client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("HF_TOKEN")
)

def run_ca_baseline_eval():
    accounting_env = CAAccountingEnv()
    
    for run_idx in range(3):
        current_obs = accounting_env.reset()
        task_id = current_obs["task_id"]
        
        print(f"[START] task_id={task_id} seed={run_idx}")

        system_instruction = (
            f"Context: {current_obs['question']}\n"
            f"Financial Data: {current_obs['data']}\n"
            f"Action: Solve the accounting problem and return ONLY a JSON object."
        )

        try:
            inference_response = agent_client.chat.completions.create(
                model=os.environ.get("MODEL_NAME"),
                messages=[{"role": "user", "content": system_instruction}],
                temperature=0.0,
                response_format={"type": "json_object"}
            )

            ai_output = json.loads(inference_response.choices[0].message.content)
            step_data = accounting_env.step(ai_output)

            print(f"[STEP] step=1")
            print(f"  observation: {current_obs['data']}")
            print(f"  action: {ai_output}")
            print(f"  reward: {step_data['reward']}")
            print(f"  done: {str(step_data['done']).lower()}")
            print(f"[END] task={task_id} total_reward={step_data['reward']} steps=1\n")

        except Exception as err:
            logger.error(f"Critical error during task {task_id}: {err}")
            print(f"[END] task={task_id} status=CRASHED\n")

if __name__ == "__main__":
    run_ca_baseline_eval()