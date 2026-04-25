#!/bin/sh
streamlit run app.py --server.port="${STREAMLIT_SERVER_PORT:-8501}" --server.address="${STREAMLIT_SERVER_ADDRESS:-0.0.0.0}"
