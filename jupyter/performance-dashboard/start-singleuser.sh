#!/bin/bash
set -e

notebook_arg=""
cp -rn /notebooks/*  /home/jovyan/work

exec jupyterhub-singleuser \
  --port=8888 \
  --ip=0.0.0.0 \
  --user=$JPY_USER \
  --cookie-name=$JPY_COOKIE_NAME \
  --base-url=$JPY_BASE_URL \
  --hub-prefix=$JPY_HUB_PREFIX \
  --hub-api-url=$JPY_HUB_API_URL \
  ${notebook_arg} \
  $@ 2>&1 | tee /var/log/jupyter.log
