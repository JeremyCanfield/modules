#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$project_dir/build"
jar -cf "$project_dir/build/hello.war" -C "$project_dir/web" .
jar -cf "$project_dir/build/hello-world.ear" -C "$project_dir/ear" META-INF/application.xml -C "$project_dir/build" hello.war
printf 'Created %s\n' "$project_dir/build/hello-world.ear"
