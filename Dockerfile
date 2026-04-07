# 1. Base image (Python ka environment)
FROM python:3.10-slim

# 2. Container ke andar folder banana
WORKDIR /app

# 3. Pehle requirements copy karke install karna
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Pura code copy karna
COPY . .

# 5. Port set karna (Hugging Face ke liye 7860 standard hai)
ENV PORT=7860
EXPOSE 7860

# 6. Server chalu karne ki command
CMD ["python", "main.py"]