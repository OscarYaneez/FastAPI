FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --create-home appuser

COPY --chown=appuser:appgroup first_project/__init__.py first_project/first_api.py ./first_project/
COPY --chown=appuser:appgroup first_project/models ./first_project/models/

USER appuser

EXPOSE 8000

CMD ["uvicorn", "first_project.first_api:app", "--host", "0.0.0.0", "--port", "8000"]