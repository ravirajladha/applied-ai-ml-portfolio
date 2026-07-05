# Hugging Face Docker Space: runs the two FastAPI services + the Streamlit UI.
FROM python:3.12-slim

# Non-root user (Hugging Face Spaces requirement).
RUN useradd -m -u 1000 user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    RECO_SERVICE=http://127.0.0.1:8001 \
    GATEWAY_URL=http://127.0.0.1:8000 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Create the app dir owned by the non-root user so it can write there.
RUN mkdir -p /home/user/app && chown user:user /home/user/app
WORKDIR /home/user/app

COPY --chown=user requirements-hf.txt .
USER user
RUN pip install --no-cache-dir --user -r requirements-hf.txt

COPY --chown=user . .

# Guard against CRLF line endings sneaking in from Windows checkouts.
RUN sed -i 's/\r$//' start.sh

EXPOSE 7860
CMD ["bash", "start.sh"]
