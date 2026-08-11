# AI Learning Research Platform

A research-oriented platform for studying how AI assistance affects programming learning, particularly students' ability to retain and transfer programming skills when working without AI.

## Research Question

> Does AI assistance change how well students retain and transfer programming skills when they later work without AI?

The study focuses on the relationship between students' immediate independent programming performance and their subsequent unaided learning outcomes, particularly:

- Delayed retention
- Transfer of programming knowledge and skills

## Research Motivation

Generative AI can improve students' immediate ability to complete programming tasks. However, stronger performance during AI-assisted learning does not necessarily mean that the underlying skill has been learned.

This project investigates that distinction by comparing learning under controlled AI-assisted and non-AI conditions and subsequently measuring performance without AI assistance.

The goal is not simply to build an AI tutor. The software is being developed as an experimental research platform whose features are driven by the study protocol.

## Current Research Design

The initial experimental design considers:

- A No-AI condition
- A Controlled-AI condition
- Immediate independent performance measurement
- Delayed unaided performance measurement
- Transfer measurement
- Standardized programming tasks
- Logged AI interactions
- Reproducible grading

The exact protocol is maintained separately in:

`research/protocol_v0.1.md`

Project boundaries and scope are documented in:

`research/SCOPE.md`

## Project Structure

```text
AI-Learning-Research/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── scripts/
│   └── requirements.txt
│
├── research/
│   ├── protocol_v0.1.md
│   └── SCOPE.md
│
├── frontend/
│
├── analysis/
│
├── docs/
│
├── .gitignore
└── README.md