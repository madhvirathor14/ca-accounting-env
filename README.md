
```yaml
---
title: Ca Accounting Agent
emoji: 🏦
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# 🏦 CA Accounting RL Environment
> **Empowering AI to solve Real-World Financial Challenges.** > Built for the **Meta PyTorch OpenEnv Hackathon 2026**

[![HuggingFace](https://img.shields.io/badge/🤗_Live_Demo-HuggingFace-orange)](https://huggingface.co/spaces/madhvirathor14/ca-accounting-agent)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![OpenEnv](https://img.shields.io/badge/Framework-OpenEnv_Core-green)](https://github.com/meta-pytorch/OpenEnv)

---

## 🌟 Overview & The Problem
Most Reinforcement Learning (RL) environments are based on physics simulations or games (like Atari or Chess). However, in the real world, some of the highest-stakes tasks happen in financial accounting, where a single miscalculation can cost a business heavily. 

This project transforms **CA-level Accounting** into a structured Reinforcement Learning environment. We have built a platform where an AI agent learns to process financial statements, handle data, and solve complex calculations—just like a Chartered Accountant would.

---

## 🎯 Mandatory Guidance: The OpenEnv Architecture

This project strictly adheres to the **OpenEnv API** standards. The environment interacts with the AI agent through the following core functions:

1. **`reset()`**: Initializes and provides the agent with a fresh, randomized accounting problem (using synthetic Indian financial data).
2. **`state()`**: Returns the current context of the financial problem (e.g., Sales, COGS, Asset values).
3. **`step(action)`**: The agent submits its calculated answer. The environment validates this answer and returns a continuous reward (ranging from `0.0` to `1.0`) along with a `done` flag.

---

## 📚 The Learning Curriculum (Task Breakdown)

The environment features a 3-tier curriculum designed to train the AI agent progressively. Each level has its own grading logic and reward system:

### 🟢 Level 1: Profit & Loss Statement (Easy)
- **Problem:** The agent receives a company's Sales, Cost of Goods Sold (COGS), and Operating Expenses.
- **Agent's Goal:** Calculate the `Gross Profit` and `Net Profit`.
- **Reward Breakdown (Total 1.0):**
  - +0.50 if Gross Profit is correct (Sales - COGS).
  - +0.50 if Net Profit is correct (Gross Profit - Expenses).

### 🟡 Level 2: Budget Variance Analysis (Medium)
- **Problem:** The agent is given Quarterly Budgeted figures versus Actual performance figures.
- **Agent's Goal:** Calculate the financial variance and identify whether it is **Favorable (F)** or **Adverse (A)** for the business.
- **Reward Breakdown (Total 1.0):**
  - +0.34 for exact Sales Variance calculation.
  - +0.33 for exact Expense Variance calculation.
  - +0.33 for correctly labeling both variances as "F" or "A".

### 🔴 Level 3: Depreciation & Asset Valuation (Hard)
- **Problem:** The agent receives an asset's Original Cost, Useful Life, Rate, and Salvage Value, along with a specified depreciation method (SLM or WDV).
- **Agent's Goal:** Identify the correct method, calculate Depreciation for Year 1 and Year 2, and determine the Book Value at the end of Year 2.
- **Reward Breakdown (Total 1.0):**
  - +0.25 for identifying the correct Method.
  - +0.25 for Year 1 Depreciation accuracy.
  - +0.25 for Year 2 Depreciation accuracy.
  - +0.25 for the final Book Value accuracy.

*(Note: In accordance with real-world accounting practices, a **1% rounding tolerance** is applied to all calculations).*

---

## 🚀 Complete Setup & Execution Guide

Follow these step-by-step instructions to run the project locally:

### **1. Local System Setup**
Run the following commands in your terminal:

```bash
# 1. Clone the repository and navigate into it
git clone [https://github.com/madhvirathor14/ca-accounting-env.git](https://github.com/madhvirathor14/ca-accounting-env.git)
cd ca-accounting-env

# 2. Create a fresh Virtual Environment
python -m venv venv

# 3. Activate the Virtual Environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install all necessary dependencies
pip install -r requirements.txt
```

### **2. Environment Variables (.env) Setup**
Before running the code, create a new file named `.env` in the root directory. Add your credentials like this:

```env
API_BASE_URL=[https://api.groq.com/openai/v1](https://api.groq.com/openai/v1)
MODEL_NAME=llama-3.3-70b-versatile
HF_TOKEN=your_huggingface_write_token_here
GROQ_API_KEY=your_groq_api_key_here
```

### **3. Running the Server & Baseline Agent**
You will need two separate terminal tabs to run the environment:

**Terminal 1 (Start the Backend API Server):**
```bash
uvicorn main:app --host 0.0.0.0 --port 7860
```
*(Wait until you see `Application startup complete` before moving to the next step).*

**Terminal 2 (Run the AI Agent Inference):**
```bash
python inference.py
```
*(This triggers the agent to call the environment, process the financial data, and return the answers to earn rewards).*

---

## 🐳 Docker Deployment Guide
To test the containerized version locally using Docker:

```bash
# Build the Docker Image
docker build -t ca-accounting-env .

# Run the Docker Container (Replace with your actual keys)
docker run -p 7860:7860 \
  -e API_BASE_URL=[https://api.groq.com/openai/v1](https://api.groq.com/openai/v1) \
  -e MODEL_NAME=llama-3.3-70b-versatile \
  -e GROQ_API_KEY=your_key_here \
  ca-accounting-env
```

---

## 🛠 Tech Stack Used
- **Language:** Python 3.11
- **API Framework:** FastAPI (Handling endpoints like `/reset` and `/step`)
- **RL Framework:** OpenEnv Core
- **Agent Intelligence:** Baseline validation performed using Groq's Llama-3.3-70b.
- **Containerization & Hosting:** Docker & Hugging Face Spaces

---

**Built with ❤️ by Madhvi Rathor**
```

