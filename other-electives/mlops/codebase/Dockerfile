# M3 · Packaging: the model service as a container image.
# Build:  docker build -t deliverease-eta .
# Run:    docker run -p 8000:8000 -v $PWD/mlops_workdir:/app/mlops_workdir deliverease-eta
# The model file is NOT baked into the image: the registry folder is mounted, so a new model version
# goes live without rebuilding the image (code and model have separate release cycles).
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY deliverease/ deliverease/
ENV REGISTRY_DIR=/app/mlops_workdir/registry
EXPOSE 8000
CMD ["uvicorn", "deliverease.serve:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
