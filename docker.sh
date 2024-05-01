#!/bin/bash

case "$1" in
  rebuild)
    docker compose up --build
    ;;
  dev)
    docker compose up
    ;;
  nuxt-bash)
    docker exec -it nuxt-docker /bin/bash
    ;;
  scraper-bash)
    docker exec -it scraper-docker /bin/bash
    ;;
  *)
    echo "Usage: $0 {rebuild|dev|nuxt}"
    exit 1
esac