FROM ubuntu:24.04

# Install or copy over any environment dependencies here.
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root
# Copy the input file to /root/
COPY test_input.json /root/test_input.json
COPY calendar.pdf /root/calendar.pdf

# Copy skills to ALL agent paths (commented out for agent runs without skills)
COPY skills /root/.claude/skills
COPY skills /root/.codex/skills
COPY skills /root/.opencode/skill
COPY skills /root/.goose/skills
COPY skills /root/.factory/skills
COPY skills /root/.agents/skills
COPY skills /root/.gemini/skills

# Install Python dependencies for PDF skills
RUN pip3 install --break-system-packages \
    pypdf==5.1.0 \
    fillpdf==0.7.3 \
    pdfrw==0.4 \
    PyPDF2==3.0.1 \
    reportlab==4.2.5 \
    cryptography==43.0.3 \
    pdfplumber