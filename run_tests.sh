#!/usr/bin/env bash

set -e

mypy koda tests examples
pytest
flake8

