#!/bin/bash

pytest -v -s --alluredir="${WORKSPACE}"/tests_logs/allure tests/
