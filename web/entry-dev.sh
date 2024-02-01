#!/bin/bash

# The only reason to use a shell script wrapper is to generate the package-lock.json file
# Which seems impossible to do with COPY inside a Dockerfile since is a one direction copy from container to host
# It would be possible to do it with `docker cp` but that would require to execute in a script manually from the host
npm install --package-lock-only
npm run dev