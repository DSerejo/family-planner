FROM python:3.12-slim

WORKDIR /app

RUN python -m venv /app/venv
SHELL ["/bin/bash", "-c"] 
RUN source /app/venv/bin/activate

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]