FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r backend/requirement.txt
ENV PYTHONPATH=/app
EXPOSE 8080
CMD ["sh", "-c", "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"] 