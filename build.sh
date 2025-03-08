#!/usr/bin/env bash
# команды для установки uv, зависимостей, сборки статики, применения миграций
make install
make collectstatic
make migrate