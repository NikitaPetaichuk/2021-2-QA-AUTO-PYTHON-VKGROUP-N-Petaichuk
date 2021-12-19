#!/bin/bash

cmd="pytest -v -s --alluredir=${WORKSPACE}/tests_logs/allure tests/"

if [ -n "${TESTS_KEYWORD}" ]; then
  cmd="$cmd -k ${TESTS_KEYWORD}"
fi

${cmd}
