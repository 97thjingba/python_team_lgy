#!/bin/bash

kubectl -n {{ k8s_namespace }} apply -f deployment.yaml
