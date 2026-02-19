# PharmaGuard Production Deployment Guide

## 📋 Pre-Deployment Verification

### 1. Code Quality Checks
```bash
# Run tests
pytest backend/ -v --cov=backend

# Lint code
flake8 backend/ --max-line-length=127

# Format check
black --check backend/

# Security scan
bandit -r backend/

# Dependency check
safety check -r requirements.txt
```

### 2. Environment Setup
```bash
# Copy and configure environment
cp .env.example .env

# Generate secure JWT secret
python -c "import secrets; print(secrets.token_hex(32))"

# Update .env with:
# - FLASK_ENV=production
# - FLASK_DEBUG=False
# - JWT_SECRET_KEY=<generated-key>
# - OpenAI API key (if using LLM)
```

## 🐳 Docker Deployment

### Build and Test Image
```bash
# Build image
docker build -t pharmaguard:latest .

# Test image locally
docker run --rm -p 5000:5000 \
  -e FLASK_ENV=production \
  -e LOG_FILE=/tmp/audit.log \
  pharmaguard:latest

# Test health endpoint
curl http://localhost:5000/health
```

### Push to Registry
```bash
# Tag image
docker tag pharmaguard:latest ghcr.io/yourusername/pharmaguard:latest
docker tag pharmaguard:latest ghcr.io/yourusername/pharmaguard:v1.0.0

# Login to registry
docker login ghcr.io

# Push image
docker push ghcr.io/yourusername/pharmaguard:latest
docker push ghcr.io/yourusername/pharmaguard:v1.0.0
```

## ☸️ Kubernetes Deployment

### Create ConfigMap and Secrets
```bash
# Create namespace
kubectl create namespace pharmaguard

# Create ConfigMap for non-sensitive config
kubectl create configmap pharmaguard-config \
  --from-literal=FLASK_ENV=production \
  --from-literal=API_WORKERS=4 \
  -n pharmaguard

# Create Secret for sensitive data
kubectl create secret generic pharmaguard-secrets \
  --from-literal=JWT_SECRET_KEY=$(openssl rand -hex 32) \
  --from-literal=OPENAI_API_KEY=sk-... \
  -n pharmaguard
```

### Deploy Application
```yaml
# Save as pharmaguard-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pharmaguard-api
  namespace: pharmaguard
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pharmaguard-api
  template:
    metadata:
      labels:
        app: pharmaguard-api
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      
      containers:
      - name: pharmaguard-api
        image: ghcr.io/yourusername/pharmaguard:latest
        imagePullPolicy: IfNotPresent
        
        ports:
        - containerPort: 5000
          name: http
        
        envFrom:
        - configMapRef:
            name: pharmaguard-config
        - secretRef:
            name: pharmaguard-secrets
        
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 30
        
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
        
        volumeMounts:
        - name: logs
          mountPath: /app/logs
        
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL
      
      volumes:
      - name: logs
        emptyDir: {}

---
apiVersion: v1
kind: Service
metadata:
  name: pharmaguard-api
  namespace: pharmaguard
spec:
  selector:
    app: pharmaguard-api
  type: ClusterIP
  ports:
  - port: 5000
    targetPort: 5000
    name: http

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: pharmaguard-api-hpa
  namespace: pharmaguard
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: pharmaguard-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Deploy to Kubernetes
```bash
# Apply deployment
kubectl apply -f pharmaguard-deployment.yaml

# Check deployment status
kubectl get deployments -n pharmaguard
kubectl get pods -n pharmaguard
kubectl logs -f deployment/pharmaguard-api -n pharmaguard

# Setup ingress (with TLS)
kubectl apply -f pharmaguard-ingress.yaml
```

## 🌍 Reverse Proxy Configuration (Nginx)

```nginx
upstream pharmaguard_backend {
    server 127.0.0.1:5000;
    keepalive 32;
}

server {
    listen 80;
    server_name api.pharmaguard.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.pharmaguard.com;
    
    # SSL Configuration
    ssl_certificate /etc/ssl/certs/api.pharmaguard.com.crt;
    ssl_certificate_key /etc/ssl/private/api.pharmaguard.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=50r/m;
    limit_req_zone $binary_remote_addr zone=analyze_limit:10m rate=20r/m;
    
    # Logging
    access_log /var/log/nginx/pharmaguard_access.log;
    error_log /var/log/nginx/pharmaguard_error.log;
    
    # Health check endpoint
    location /health {
        proxy_pass http://pharmaguard_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        limit_req zone=api_limit burst=10 nodelay;
    }
    
    # API endpoints
    location /analyze {
        proxy_pass http://pharmaguard_backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Rate limiting
        limit_req zone=analyze_limit burst=5 nodelay;
        
        # Timeout settings
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 120s;
    }
    
    # Block all other endpoints
    location / {
        return 404;
    }
}
```

## 📊 Monitoring & Logging

### Application Metrics
```bash
# Install monitoring
pip install prometheus-client prometheus-flask-exporter

# Metrics endpoint: /metrics
# Scrape interval: 30s recommended
```

### Log Aggregation
```bash
# Centralize logs (ELK Stack example)
# Filebeat collects logs
# Logstash processes them
# Elasticsearch stores them
# Kibana visualizes them

# Example Filebeat config
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /app/logs/audit.log

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
```

## 🔍 Health Checks & Alerts

```bash
# Setup monitoring alerts
# Alert on:
# - High error rate (>5%)
# - High latency (>1s)
# - Pod restart (>0/hour)
# - Disk space low (<10%)
# - Memory usage high (>80%)
```

## 🔄 Backup & Disaster Recovery

```bash
# Backup audit logs
0 2 * * * tar -czf /backup/pharmaguard-logs-$(date +%Y%m%d).tar.gz /app/logs/

# Database backup (if using MongoDB)
0 3 * * * mongodump --uri="mongodb://..." --out=/backup/mongodb-$(date +%Y%m%d)/

# Retention: Keep backups for 90 days
find /backup -type f -mtime +90 -delete
```

## ✅ Post-Deployment Verification

```bash
# Test all endpoints
curl -X GET https://api.pharmaguard.com/health

# Test with sample VCF
curl -X POST https://api.pharmaguard.com/analyze \
  -F "patient_id=P001" \
  -F "drug=CODEINE" \
  -F "vcf_file=@test.vcf"

# Check logs
kubectl logs deployment/pharmaguard-api -n pharmaguard

# Monitor metrics
# Access Prometheus dashboard
# Check error rates, latency, resource usage
```

## 🚨 Rollback Plan

```bash
# If deployment fails, rollback to previous version
kubectl rollout undo deployment/pharmaguard-api -n pharmaguard

# Check rollout history
kubectl rollout history deployment/pharmaguard-api -n pharmaguard

# Rollback to specific version
kubectl rollout undo deployment/pharmaguard-api --to-revision=2 -n pharmaguard
```

## 📝 Maintenance Schedule

- **Daily**: Monitor error rates, check health endpoints
- **Weekly**: Review audit logs, verify backups
- **Monthly**: Security updates, dependency updates
- **Quarterly**: Penetration testing, compliance review
- **Annually**: Disaster recovery drill, architecture review

## 🆘 Troubleshooting

### High Latency
```bash
# Check resource usage
kubectl top pods -n pharmaguard

# Check Flask worker count
# Increase workers in Dockerfile if needed
```

### High Error Rates
```bash
# Check logs
kubectl logs deployment/pharmaguard-api -n pharmaguard

# Check VCF file format
# Verify drug whitelist
```

### Pod Crashes
```bash
# Check events
kubectl describe pod <pod-name> -n pharmaguard

# Check resource limits
# Increase memory/CPU if needed
```

For more support, see [SECURITY.md](SECURITY.md) and [README.md](README.md).
