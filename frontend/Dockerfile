FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 3012
CMD ["streamlit", "run", "app.py"]
