apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: {{ project_dns_name }}
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: {{ project_dns_name }}
    spec:
      containers:
      - name: {{ project_dns_name }}
        image: registry.shafayouxi.org/kevinanew/{{ project }}:{{ docker_tag }}
        imagePullPolicy: Always
        env:
        - name: STAGE
          value: {{stage}}
        ports:
        - containerPort: 80
        resources:
          requests:
            cpu: 100m
      imagePullSecrets:
      - name: docker-registry-secret
---
apiVersion: v1
kind: Service
metadata:
  name: {{ project_dns_name }}
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: {{ project_dns_name }}
