FROM python:3.9-slim

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

RUN apt-get update || true

RUN apt-get install -y wget curl build-essential || true

# Manual BLAST install
RUN wget https://ftp.ncbi.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.15.0+-x64-linux.tar.gz \
    && tar -xzf ncbi-blast-2.15.0+-x64-linux.tar.gz \
    && mv ncbi-blast-2.15.0+/bin/* /usr/local/bin/

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app/dashboard.py"]
CMD ["--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
