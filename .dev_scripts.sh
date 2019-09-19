#!/bin/bash
export BANKEN_REPO="/absolute/path/to/infra-dashboard"
alias start-banken='docker-compose -f $BANKEN_REPO/docker-compose.yml up -d'
alias stop-banken='docker-compose -f $BANKEN_REPO/docker-compose.yml stop'
alias restart='stop-banken && start-banken'