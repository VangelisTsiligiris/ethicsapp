# FinTech AI Ethics & Governance Toolkit

A comprehensive Streamlit application for identifying ethical and responsible use of AI in financial technology. Built on the latest global regulations (EU AI Act, NIST AI RMF, UK FCA, Singapore MAS FEAT) with interactive tools for risk identification, governance framework building, and ethical assessment.

## 🎯 Purpose

This toolkit helps finance professionals and students:
- Understand global AI regulations affecting financial services
- Identify and assess AI-related risks
- Build customized governance frameworks
- Complete comprehensive ethical assessments
- Learn from real-world case studies
- Generate compliance documentation

## 🌟 Features

### 📜 Regulatory Framework Reference
- **EU AI Act**: Full implementation timeline, risk classifications, penalties
- **US Frameworks**: NIST AI RMF, CFPB guidance, agency-specific requirements
- **UK FCA**: Consumer Duty implications, five principles approach
- **Singapore MAS**: FEAT principles, Veritas toolkit integration
- **Comparison Matrix**: Side-by-side regulatory comparison

### ⚠️ Risk Identification Tool
- Interactive questionnaire across 6 risk categories
- Weighted scoring based on regulatory priorities
- Visual risk dashboards
- Jurisdiction-specific alerts
- Automated mitigation recommendations

### 🔧 Governance Framework Builder
- Organization profile customization
- Policy and procedure status tracking
- Three lines of defense structure
- Risk appetite definition
- Lifecycle controls mapping
- Monitoring and reporting framework

### ✅ Ethical Assessment Checklist
- 64 assessment items across 8 categories
- Priority-weighted scoring
- Compliance gap identification
- Exportable assessment reports

### 📊 Case Studies & Scenarios
- Credit scoring bias case study
- Chatbot failure analysis
- Algorithmic trading incident
- Interactive decision-making scenario

### 📚 Resources & Documentation
- Official regulatory document links
- Framework and guideline references
- Learning resources
- Technical tools and templates

### 💾 Export & Reports
- JSON and Markdown export formats
- Comprehensive report generation
- Audit-ready documentation

## 🚀 Deployment Instructions

### Local Development

1. **Clone or download the application files**

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the application**
Open your browser to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/fintech-ai-ethics-tool.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the `app.py` file as the main file
   - Click "Deploy"

### Docker Deployment

1. **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and run**
```bash
docker build -t fintech-ai-ethics-tool .
docker run -p 8501:8501 fintech-ai-ethics-tool
```

### Heroku Deployment

1. **Create Procfile**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Create setup.sh**
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

3. **Deploy**
```bash
heroku create your-app-name
git push heroku main
```

## 📁 Project Structure

```
fintech_ai_ethics_tool/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── Dockerfile            # For Docker deployment (optional)
├── Procfile              # For Heroku deployment (optional)
└── setup.sh              # For Heroku deployment (optional)
```

## 🔧 Configuration Options

The application can be configured via Streamlit's configuration system:

**Create `.streamlit/config.toml`:**
```toml
[theme]
primaryColor = "#3182ce"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f7fafc"
textColor = "#1a365d"
font = "sans serif"

[server]
maxUploadSize = 50

[browser]
gatherUsageStats = false
```

## 📋 Regulatory Frameworks Covered

| Framework | Jurisdiction | Status |
|-----------|--------------|--------|
| EU AI Act (2024/1689) | European Union | Phased implementation 2024-2027 |
| NIST AI RMF 1.0/2.0 | United States | Voluntary, widely adopted |
| CFPB AI Guidance | United States | Active enforcement |
| FCA AI Update | United Kingdom | Principles-based approach |
| MAS FEAT Principles | Singapore | Industry-led implementation |

## 🎓 Educational Use

This toolkit is designed for:
- University finance and technology courses
- Professional development programs
- Corporate training initiatives
- Self-directed learning

### Suggested Learning Path

1. **Week 1**: Review Regulatory Framework section
2. **Week 2**: Complete Risk Identification for a sample use case
3. **Week 3**: Build a governance framework using the builder
4. **Week 4**: Run through ethical assessment checklist
5. **Week 5**: Study case studies and complete interactive scenario
6. **Week 6**: Generate comprehensive report

## 📊 Assessment Categories

The toolkit assesses AI systems across 8 dimensions:

1. **Fairness & Non-Discrimination**
2. **Transparency & Explainability**
3. **Accountability & Governance**
4. **Data Quality & Privacy**
5. **Security & Robustness**
6. **Human Oversight**
7. **Consumer Protection**
8. **Regulatory Compliance**

## 🔄 Keeping Current

AI regulations evolve rapidly. This toolkit reflects regulations as of November 2025. Users should:

- Monitor official regulatory sources for updates
- Check for toolkit updates regularly
- Supplement with legal/compliance professional advice
- Participate in regulatory consultations where possible

## ⚖️ Disclaimer

This tool is for educational and informational purposes only. It does not constitute legal advice. Organizations should consult with qualified legal and compliance professionals for specific regulatory requirements and compliance strategies.

## 📝 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

Contributions welcome! Please submit issues and pull requests via GitHub.

## 📧 Contact

For questions or feedback, please open a GitHub issue.

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Regulatory Coverage**: EU AI Act, NIST AI RMF, UK FCA, Singapore MAS FEAT
