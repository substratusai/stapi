#!/usr/bin/env bash
export API_KEY=${API_KEY:-""}
uvicorn main:app --host 0.0.0.0 --port $PORT