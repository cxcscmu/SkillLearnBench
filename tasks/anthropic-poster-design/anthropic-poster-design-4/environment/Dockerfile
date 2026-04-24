FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3 python3-pip

RUN python3 -m pip install --break-system-packages pytest

WORKDIR /root

# Copy skills to agent-specific locations
COPY skills /root/.claude/skills
COPY skills /root/.codex/skills
COPY skills /root/.opencode/skills
COPY skills /root/.goose/skills
COPY skills /root/.agents/skills
# Gemini
COPY skills /root/.gemini/skills
COPY skills /root/.factory/skills