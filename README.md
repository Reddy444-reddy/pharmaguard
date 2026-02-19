# 🧬 PharmaGuard - AI Clinical Pharmacogenomics Engine

Enterprise-grade pharmacogenomic analysis platform powered by CPIC guidelines, built with Flask and designed for production deployment.

## 🌟 Features

- **Clinical Intelligence**: CPIC-aligned risk assessment with evidence levels
- **Genomic Analysis**: VCF file parsing with target gene filtering (CYP2D6, CYP2C19, CYP2C9, SLCO1B1, TPMT, DPYD)
- **Risk Scoring**: Numeric risk assessment (0-100 scale)
- **Audit Trail**: Complete request tracing with UUID correlation IDs
- **Rate Limiting**: DDoS protection with configurable limits
- **Production Ready**: Docker containerized, Kubernetes deployable
- **Security Hardened**: Path traversal protection, input validation, secure error handling

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask dev server
export FLASK_ENV=development
python -m backend.api

# Server runs at http://localhost:5000
```

### Docker

```bash
# Build image
docker build -t pharmaguard:latest .

# Run container
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e JWT_SECRET_KEY=$(openssl rand -hex 32) \
  pharmaguard:latest

# Test health endpoint
curl http://localhost:5000/health
```

### Render Deployment (Recommended for Cloud)

```bash
# Push to GitHub
git push origin main

# Go to https://render.com
# 1. Create New Web Service
# 2. Connect your GitHub repo
# 3. Set environment variables (see RENDER_QUICK_START.md)
# 4. Deploy!

# Your API will be live at: https://pharmaguard-api-xxxx.onrender.com
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [RENDER_QUICK_START.md](RENDER_QUICK_START.md) | 5-minute Render deployment guide |
| [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) | Detailed Render setup instructions |
| [SECURITY.md](SECURITY.md) | Security guidelines & best practices |
| [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) | K8s, Docker, Nginx configuration |
| [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md) | Enhancement tracking |

## 🔧 API Endpoints

### Health Check
```bash
GET /health
```
Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-19T10:30:45.123456"
}
```

### Analyze Pharmacogenomics
```bash
POST /analyze
Content-Type: multipart/form-data

Parameters:
- patient_id (string): Patient identifier
- drug (string): Drug name (CODEINE, WARFARIN, CLOPIDOGREL, SIMVASTATIN, AZATHIOPRINE, FLUOROURACIL)
- vcf_file (file): VCF format genomic file
```

Response:
```json
{
  "analysis_id": "550e8400-e29b-41d4-a716-446655440000",
  "patient_id": "P001",
  "drug": "CODEINE",
  "timestamp": "2026-02-19T10:30:45.123456",
  "risk_assessment": {
    "risk_label": "Safe",
    "risk_score": 0.0,
    "severity": "none",
    "evidence_level": "A",
    "guideline_version": "2023.1"
  },
  "pharmacogenomic_profile": {
    "primary_gene": "CYP2D6",
    "diplotype": "*1/*1",
    "phenotype": "NM",
    "detected_variants": [...]
  },
  "clinical_recommendation": {
    "recommendation_text": "Standard dosing recommended.",
    "guideline_source": "CPIC",
    "evidence_level": "A",
    "cpic_version": "2023.1"
  }
}
```

## 📊 Supported Genes & Drugs

### Genes
- CYP2D6 (codeine metabolism)
- CYP2C19 (clopidogrel metabolism)
- CYP2C9 (warfarin metabolism)
- SLCO1B1 (statin metabolism)
- TPMT (azathioprine metabolism)
- DPYD (fluorouracil metabolism)

### Drugs
- **CODEINE** - Opioid analgesic
- **WARFARIN** - Anticoagulant
- **CLOPIDOGREL** - Antiplatelet
- **SIMVASTATIN** - Statin
- **AZATHIOPRINE** - Immunosuppressant
- **FLUOROURACIL** - Chemotherapy agent

## 🔐 Security Features

- ✅ Path traversal protection (werkzeug.secure_filename)
- ✅ Rate limiting (50/hour global, 20/hour on /analyze)
- ✅ Request ID tracing (UUID correlation)
- ✅ Input validation & sanitization
- ✅ Secure error responses (no stack trace leakage)
- ✅ HTTPS ready (TLS support)
- ✅ Audit logging with patient privacy

## 📈 Production Deployment Options

### Option 1: Render (Recommended for Quick Setup)
See [RENDER_QUICK_START.md](RENDER_QUICK_START.md)
- Zero infrastructure management
- Free tier available
- Auto-scaling
- GitHub integration

### Option 2: Kubernetes
See [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)
- Enterprise-grade orchestration
- Auto-scaling (HPA: 3-10 replicas)
- Load balancing
- Health checks

### Option 3: Docker Compose
```bash
docker-compose up
```
Perfect for development and small deployments.

## 🧪 Testing

```bash
# Run unit tests
pytest backend/test_backend.py -v

# Security scanning
bandit -r backend/

# Dependency check
safety check -r requirements.txt

# Code quality
flake8 backend/
black --check backend/
```

## 📦 Dependencies

```
Flask==3.0.0              # Web framework
Flask-CORS==4.0.0         # Cross-origin support
Flask-Limiter==3.5.0      # Rate limiting
pyvcf3==1.0.1             # VCF parsing
requests==2.31.0          # HTTP client
gunicorn==21.2.0          # WSGI server
python-dotenv==1.0.0      # Environment management
```

## 🏗️ Architecture

```
Request → Validators → VCF Parser → Phenotype Mapper → PGx Rules → Response Builder → Client
           ↓
     (Security checks)
           ↓
     (Input validation)
           ↓
     (Error handling)
           ↓
     (Request tracing)
```

## 🎯 Configuration

Set environment variables in `.env` or Render dashboard:

```env
FLASK_ENV=production
FLASK_DEBUG=false
PYTHONUNBUFFERED=true
LOG_FILE=audit.log
JWT_SECRET_KEY=<your-secret-key>
MAX_CONTENT_LENGTH=5242880
RATE_LIMIT_ENABLED=true
OPENAI_API_KEY=<optional-for-llm>
```

See [.env.example](.env.example) for complete configuration.

## 📝 Logging

All requests are logged to `audit.log` with:
- Request ID (UUID)
- Timestamp
- Patient ID (hashed for privacy)
- Drug name
- Risk assessment
- Error information (if any)

## 🔄 CI/CD Pipeline

GitHub Actions automatically:
- Runs unit tests
- Scans for security vulnerabilities
- Checks code quality
- Builds Docker image
- Pushes to registry
- Deploys to production

See `.github/workflows/ci-cd.yml`

## 🆘 Troubleshooting

### Health Check Fails
```bash
# Check if service is running
curl -v http://localhost:5000/health

# Check logs
tail -f audit.log
```

### Rate Limiting Error
```
HTTP 429 - Too Many Requests
```
Rate limit is 20 requests/hour per IP on /analyze endpoint.

### VCF Parsing Error
- Ensure VCF file format is valid
- Check that file contains target genes (CYP2D6, etc.)
- Maximum file size: 5MB

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Verify Flask-Limiter is installed
pip install Flask-Limiter==3.5.0
```

## 📊 Performance

- **Response Time**: < 500ms average
- **Throughput**: 50+ requests/hour per instance
- **Uptime**: 99.9% (with proper deployment)
- **Scalability**: Horizontal scaling with Kubernetes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and security checks
5. Submit a pull request

## 📜 License

This project is provided as-is for educational and clinical research purposes.

## ⚖️ Medical Disclaimer

This software is for clinical decision support only. All pharmacogenomic recommendations should be reviewed by qualified healthcare professionals before clinical implementation. Always follow your institution's protocols and regulatory guidelines.

## 🔗 Resources

- [CPIC Guidelines](https://cpicpgx.org/)
- [OWASP Security](https://owasp.org/)
- [Render Documentation](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 📞 Support

For issues or questions:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) (if exists)
2. Review [SECURITY.md](SECURITY.md)
3. See [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md)
4. Open an issue on GitHub

---

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: February 19, 2026

🚀 Ready to deploy? Start with [RENDER_QUICK_START.md](RENDER_QUICK_START.md)
