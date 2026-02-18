# Building On-Device AI Memory with Qdrant Edge

A [DeepLearning.AI](https://www.deeplearning.ai) short course by [Qdrant](https://qdrant.tech).

Instructor: **Thierry Damiba**, Developer Advocate at Qdrant

<p align="center">
  <img src="assets/qdrant-edge-scheme.png" alt="Qdrant Edge Architecture" width="600">
</p>

## What you'll learn

- Store and retrieve vector embeddings on-device with Qdrant Edge, achieving sub-20ms query latency with no cloud dependency.
- Compile and run embedding models on Snapdragon hardware using AI Hub, then orchestrate memory across devices and cloud.
- Build three end-to-end applications: a photo memory you search with plain English, a product scout for cross-trip comparisons, and a robot memory agent.

## About this course

Today's AI interactions are fragmented across devices. Your AR glasses, phone, and laptop each hold separate context, with no shared memory. Relying on cloud-only retrieval adds latency that breaks real-time experiences. This course teaches you to build a **context hub**: a cross-device memory system where AI can subscribe to relevant information streams and deliver personalized experiences across all your devices.

Using **Qdrant Edge** for local vector storage and **AI Hub** for on-device inference, you'll store and query embeddings locally in under 20ms, design memory that works offline, and orchestrate context across multiple devices and the cloud.

In this course, you'll:

- Build a phone photo memory you search with natural language, a product scout that compares items across shopping trips, and a robot memory agent with spatial navigation.
- Configure Qdrant Edge for local vector storage on resource-constrained devices, with no server or network required.
- Generate embeddings on-device using models from AI Hub and store them in Qdrant Edge for fast local retrieval.
- Implement time and location-aware filtering using must (AND) and should (OR) conditions for contextual retrieval.
- Design cross-device memory orchestration with cascade queries: search locally first, fall back to cloud when needed.
- Compile the same model for multiple Snapdragon devices and sync memory between them.

All lessons use interactive Jupyter notebooks. An appendix covers deploying your context hub to a Snapdragon-powered Android phone or dev kit.

## Course outline

| # | Lesson | Format | Duration |
|---|--------|--------|----------|
| 1 | Introduction - The Context Hub Vision | Video | 5 mins |
| 2 | Edge Vector Memory with Qdrant | Video with code examples | 15 mins |
| 3 | On-Device Embeddings with AI Hub | Video with code examples | 15 mins |
| 4 | Contextual Retrieval and Filtering | Video with code examples | 12 mins |
| 5 | Cross-Device Memory Orchestration | Video with code examples | 15 mins |
| 6 | Lab - Phone Photo Memory | Video with code examples | 18 mins |
| 7 | Lab - Product Scout | Video with code examples | 15 mins |
| 8 | Lab - Robot Memory Agent | Video with code examples | 15 mins |
| 9 | Conclusion | Video | 1 min |
| - | Appendix - Deploying to a Snapdragon Device | Code examples | 1 min |

## Who should join?

Anyone with basic Python knowledge who wants to build AI applications that run on-device. If you've taken [Introduction to On-Device AI](https://www.deeplearning.ai/short-courses/introduction-to-on-device-ai/) with Krishna Sridhar, this is a great next step.

## Setup

```bash
pip install qdrant-edge-py qai-hub qai-hub-models torch transformers numpy
```

## Repository structure

```
L2/  Edge Vector Memory with Qdrant
L3/  On-Device Embeddings with AI Hub
L4/  Contextual Retrieval and Filtering
L5/  Cross-Device Memory Orchestration
L6/  Lab - Phone Photo Memory
L7/  Lab - Product Scout
L8/  Lab - Robot Memory Agent
Appendix/  Deploying to a Snapdragon Device
```
