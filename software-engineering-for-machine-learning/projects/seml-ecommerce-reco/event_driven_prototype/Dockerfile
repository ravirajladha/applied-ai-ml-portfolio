# Hugging Face Docker Space: runs the two FastAPI services + the Streamlit UI.
FROM python:3.12-slim

# Non-root user (Hugging Face Spaces requirement).
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    RECO_SERVICE=http://127.0.0.1:8001 \
    GATEWAY_URL=http://127.0.0.1:8000 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /home/user/app

COPY --chown=user requirements-hf.txt .
USER user
RUN pip install --no-cache-dir --user -r requirements-hf.txt

COPY --chown=user . .

EXPOSE 7860
CMD ["bash", "start.sh"]
