FROM python:3.11-slim

WORKDIR /app

COPY requirements_urban_planning.txt .
RUN pip install --no-cache-dir -r requirements_urban_planning.txt

COPY . .

CMD ["python", "urban_planning_agent.py"]