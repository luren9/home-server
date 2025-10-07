# ------------------------------------------------------------------------------------
# Stage: Base - Shared configs and libraries used across stages ----------------------
# ------------------------------------------------------------------------------------
FROM alpine:3.20 AS base

# Install necessary packages needed across all stages
RUN apk add --no-cache python3 py3-pip tzdata
COPY requirements.base.txt /requirements.base.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /requirements.base.txt

# Env variables
ENV PYTHONUNBUFFERED=1
ENV TZ="Europe/Stockholm"

# Setup filesystem
RUN mkdir /docker/
WORKDIR /docker/

# Create a non-root user and give it permission to the docker directory
RUN addgroup -g 1005 appgroup && \
    adduser -u 1005 -G appgroup -S appuser && \
    chown -R appuser:appgroup /docker

# Copy application code
COPY app /docker/app

# ------------------------------------------------------------------------------------
# Stage: kubernetes - production specific configs ------------------------------------
# ------------------------------------------------------------------------------------
FROM base AS kubernetes

# Insert entrypoint shell file into container
COPY container-entrypoints/entrypoint-k8s.sh /entrypoint-k8s.sh
RUN chmod +x /entrypoint-k8s.sh

# Run container as non-root user
USER appuser
ENTRYPOINT ["/entrypoint-k8s.sh"]


# -----------------------------------------------------------------------------------
# Stage: Local Development stage ----------------------------------------------------
# -----------------------------------------------------------------------------------
FROM base AS local

# Insert entrypoint shell file into container
COPY container-entrypoints/entrypoint-local.sh /entrypoint-local.sh
RUN chmod +x /entrypoint-local.sh

# Run container as non-root user
USER appuser
ENTRYPOINT ["/entrypoint-local.sh"]





