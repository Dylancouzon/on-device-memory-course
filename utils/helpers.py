"""Shared helper functions for the course notebooks."""

import os
import random
import time
from pathlib import Path

from qdrant_edge import (
    EdgeShard, EdgeConfig, VectorDataConfig, Distance,
    Point, UpdateOperation, Query, QueryRequest,
)


# AI Hub device list (Snapdragon-powered)
DEVICES = [
    "Samsung Galaxy S22 Ultra 5G",
    "Samsung Galaxy S22 5G",
    "Samsung Galaxy S22+ 5G",
    "Samsung Galaxy Tab S8",
    "Xiaomi 12",
    "Xiaomi 12 Pro",
    "Samsung Galaxy S23",
    "Samsung Galaxy S23+",
    "Samsung Galaxy S23 Ultra",
    "Samsung Galaxy S24",
    "Samsung Galaxy S24 Ultra",
    "Samsung Galaxy S24+",
]


def get_ai_hub_api_token():
    """Get AI Hub API token from environment."""
    token = os.environ.get("QAI_HUB_API_TOKEN", "")
    if not token:
        from dotenv import load_dotenv
        load_dotenv()
        token = os.environ.get("QAI_HUB_API_TOKEN", "")
    return token


def get_random_device():
    """Select a random device to spread load across AI Hub fleet."""
    device = random.choice(DEVICES)
    print(f"Selected device: {device}")
    return device


def create_shard(directory, vector_name, dimension, distance=Distance.Cosine):
    """Create an EdgeShard with a single vector configuration."""
    Path(directory).mkdir(parents=True, exist_ok=True)
    config = EdgeConfig(
        vector_data={
            vector_name: VectorDataConfig(
                size=dimension,
                distance=distance,
            )
        }
    )
    return EdgeShard(directory, config)


def make_point(point_id, vector_name, embedding, payload=None):
    """Create a Point from an embedding and optional payload."""
    if payload is None:
        payload = {}
    payload.setdefault("timestamp", time.time())
    vec = embedding if isinstance(embedding, list) else embedding.tolist()
    return Point(
        id=point_id,
        vector={vector_name: vec},
        payload=payload,
    )


def cleanup_shard(shard, directory):
    """Close a shard and remove its directory."""
    import shutil
    shard.close()
    shutil.rmtree(directory, ignore_errors=True)
