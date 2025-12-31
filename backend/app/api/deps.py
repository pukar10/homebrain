"""
app/api/deps.py
"""
from typing import Any
from fastapi import Request

def get_graph(request: Request) -> Any:
    return request.app.state.graph

def get_runtime(request: Request) -> Any:
    return request.app.state.runtime

def get_settings(request: Request) -> Any:
    return request.app.state.settings
