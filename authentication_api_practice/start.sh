#!/usr/bin/env bash
set -e


python3 -m uvicorn auth_prac.main:app --host "0.0.0.0" --port 8000
