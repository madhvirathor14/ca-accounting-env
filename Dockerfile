# 1. Base image (Python 3.11 use karo, zyada stable hai)
FROM python:3.11-slim

# 2. Container ke andar folder banana
WORKDIR /app

# 3. Build tools install karna (pyproject.toml ke liye zaruri hai)
RUN pip install --no-cache-dir setuptools wheel

# 4. Pura code copy karna (pyproject.toml aur uv.lock ke saath)
COPY . .

# 5. Project ko "Editable" mode mein install karna
# Yahi wo step hai jo 'server' command ko register karega aur error fix karega!
RUN pip install -e .

# 6. Port set karna
ENV PORT=7860
EXPOSE 7860

# 7. Server chalu karne ki command
CMD ["python", "main.py"]