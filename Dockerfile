FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .
RUN mkdir -p data/chromadb_data

EXPOSE 8501

CMD ["sh", "-c", "streamlit run app2.py --server.address 0.0.0.0 --server.port ${PORT:-8501} --server.headless true"]