FROM python:3.10-slim

WORKDIR /ml_service

# Copy requirements
COPY requirements.txt .

# Install dependencies directly in this stage.
# We still use the CPU-only PyTorch to keep the image size drastically smaller (~200MB vs ~2.5GB).
RUN pip install --no-cache-dir torch==2.1.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir celery redis

# Copy app code
COPY . .

# Run the celery worker
CMD ["celery", "-A", "app.worker.tasks", "worker", "--loglevel=info"]
