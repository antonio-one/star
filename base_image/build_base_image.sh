#!/bin/bash
# USAGE: ./build_base_image.sh antonioone juby 0.0.5
# (TODO)Developer: Use git commit to trigger a new build in docker hub instead of pushing
docker_username=${1}
repo=${2}
version=${3}

docker build --no-cache --tag="${repo}:${version}" --tag="${repo}:latest" --file=base.Dockerfile .

docker tag "${repo}:${version}" "${docker_username}/${repo}:${version}"

docker tag "${repo}:latest" "${docker_username}/${repo}:latest"

docker push "${docker_username}/${repo}"
