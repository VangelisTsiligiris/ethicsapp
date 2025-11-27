"""
FinTech AI Ethics & Governance Toolkit
A comprehensive tool for identifying ethical and responsible use of AI in financial technology.
Reflects latest regulations (EU AI Act, NIST AI RMF, UK FCA, Singapore MAS FEAT) and includes
risk identification, governance frameworks, and assessment tools.

Developed by: Vangelis Tsiligkiris | Nottingham Trent University
Version: 1.0.0
Last Updated: November 2025
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import subprocess
import os

# Page configuration
st.set_page_config(
    page_title="FinTech AI Ethics & Governance Toolkit",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling with section backgrounds
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
    
    .main-header {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a365d;
        margin-bottom: 0.5rem;
        border-bottom: 3px solid #2b6cb0;
        padding-bottom: 0.5rem;
    }
    
    .sub-header {
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Section backgrounds with different colors */
    .section-blue {
        background: linear-gradient(135deg, #ebf8ff 0%, #bee3f8 100%);
        border-left: 4px solid #3182ce;
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .section-green {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        border-left: 4px solid #38a169;
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .section-purple {
        background: linear-gradient(135deg, #faf5ff 0%, #e9d8fd 100%);
        border-left: 4px solid #805ad5;
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .section-orange {
        background: linear-gradient(135deg, #fffaf0 0%, #feebc8 100%);
        border-left: 4px solid #dd6b20;
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .section-teal {
        background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
        border-left: 4px solid #319795;
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .section-pink {
        background: linear-gradient(135deg, #fff5f7 0%, #fed7e2 100%);
        border-left: 4px solid #d53f8c;
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .section-gray {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-left: 4px solid #718096;
        padding: 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fffaf0 0%, #feebc8 100%);
        border-left: 4px solid #dd6b20;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        border-left: 4px solid #38a169;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    .risk-high { background: #fed7d7; color: #c53030; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600; }
    .risk-medium { background: #feebc8; color: #c05621; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600; }
    .risk-low { background: #c6f6d5; color: #276749; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 600; }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    
    .regulation-badge { display: inline-block; padding: 0.35rem 0.75rem; border-radius: 6px; font-size: 0.8rem; font-weight: 600; margin: 0.25rem; }
    .eu-badge { background: #3182ce; color: white; }
    .us-badge { background: #805ad5; color: white; }
    .uk-badge { background: #d53f8c; color: white; }
    .sg-badge { background: #38a169; color: white; }
    
    .footer {
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #1a365d 0%, #2a4365 100%);
        color: white;
        border-radius: 12px;
        text-align: center;
    }
    
    .footer a { color: #90cdf4; text-decoration: none; font-weight: 600; }
    .footer a:hover { color: #bee3f8; text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'risk_assessment' not in st.session_state:
    st.session_state.risk_assessment = {}
if 'governance_plan' not in st.session_state:
    st.session_state.governance_plan = {}
if 'completed_assessments' not in st.session_state:
    st.session_state.completed_assessments = []

# Helper function to generate DOCX report
def generate_docx_report(report_data, filename="report.docx"):
    js_code = '''
const { Document, Packer, Paragraph, TextRun, Header, Footer, AlignmentType, HeadingLevel, PageNumber, LevelFormat } = require('docx');
const fs = require('fs');

const reportData = ''' + json.dumps(report_data, default=str) + ''';

const doc = new Document({
    styles: {
        default: { document: { run: { font: "Arial", size: 22 } } },
        paragraphStyles: [
            { id: "Title", name: "Title", basedOn: "Normal", run: { size: 48, bold: true, color: "1a365d", font: "Arial" }, paragraph: { spacing: { before: 240, after: 240 }, alignment: AlignmentType.CENTER } },
            { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, color: "1a365d", font: "Arial" }, paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 } },
            { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, color: "2d3748", font: "Arial" }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
            { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 24, bold: true, color: "4a5568", font: "Arial" }, paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2 } }
        ]
    },
    numbering: { config: [{ reference: "bullet-list", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
    sections: [{
        properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
        headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "FinTech AI Ethics & Governance Report", italics: true, size: 20, color: "718096" })] })] }) },
        footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Developed by Vangelis Tsiligkiris | Nottingham Trent University — Page ", size: 18, color: "718096" }), new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "718096" }), new TextRun({ text: " of ", size: 18, color: "718096" }), new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18, color: "718096" })] })] }) },
        children: [
            new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("AI Ethics & Governance Report")] }),
            new Paragraph({ children: [new TextRun({ text: "Generated: ", bold: true }), new TextRun(reportData.report_metadata?.generated_at || new Date().toISOString())] }),
            new Paragraph({ children: [new TextRun({ text: "Tool Version: ", bold: true }), new TextRun(reportData.report_metadata?.tool_version || "1.0.0")] }),
            new Paragraph({ spacing: { after: 240 }, children: [] }),
            new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Executive Summary")] }),
            new Paragraph({ children: [new TextRun("This report summarizes the AI ethics and governance assessment conducted using the FinTech AI Ethics & Governance Toolkit. The assessment evaluates compliance with major regulatory frameworks including the EU AI Act, NIST AI RMF, UK FCA guidance, and Singapore MAS FEAT principles.")] }),
            new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Regulatory Framework References")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("EU AI Act (Regulation 2024/1689) - https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("NIST AI RMF 1.0 - https://www.nist.gov/itl/ai-risk-management-framework")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("UK FCA AI Update 2024 - https://www.fca.org.uk/firms/innovation/ai-approach")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Singapore MAS FEAT Principles - https://www.mas.gov.sg/schemes-and-initiatives/veritas")] }),
            new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Risk Assessment Summary")] }),
            ...(reportData.risk_assessment && reportData.risk_assessment.overall_score ? [
                new Paragraph({ children: [new TextRun({ text: "Overall Risk Score: ", bold: true }), new TextRun(String(Math.round(reportData.risk_assessment.overall_score)) + "%")] }),
                new Paragraph({ children: [new TextRun({ text: "Risk Level: ", bold: true }), new TextRun(reportData.risk_assessment.risk_level || "Not Assessed")] }),
                new Paragraph({ children: [new TextRun({ text: "Use Case: ", bold: true }), new TextRun(reportData.risk_assessment.use_case || "Not Specified")] }),
                new Paragraph({ children: [new TextRun({ text: "Jurisdictions: ", bold: true }), new TextRun(Array.isArray(reportData.risk_assessment.jurisdictions) ? reportData.risk_assessment.jurisdictions.join(", ") : "Not Specified")] }),
                new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Category Scores")] }),
                ...(reportData.risk_assessment.category_scores ? Object.entries(reportData.risk_assessment.category_scores).map(([cat, score]) => new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: cat + ": ", bold: true }), new TextRun(String(Math.round(score)) + "%")] })) : [])
            ] : [new Paragraph({ children: [new TextRun("Risk assessment not completed.")] })]),
            new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Governance Framework")] }),
            ...(reportData.governance_framework && Object.keys(reportData.governance_framework).length > 0 ? [
                ...(reportData.governance_framework.structure ? [
                    new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Governance Structure")] }),
                    new Paragraph({ children: [new TextRun({ text: "AI Officer: ", bold: true }), new TextRun(reportData.governance_framework.structure.ai_officer || "Not Assigned")] }),
                    new Paragraph({ children: [new TextRun({ text: "Executive Sponsor: ", bold: true }), new TextRun(reportData.governance_framework.structure.ai_sponsor || "Not Assigned")] }),
                    new Paragraph({ children: [new TextRun({ text: "AI Ethics Committee: ", bold: true }), new TextRun(reportData.governance_framework.structure.has_ai_committee ? "Established" : "Not Established")] })
                ] : []),
                ...(reportData.governance_framework.policies ? [
                    new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Policy Status")] }),
                    ...Object.entries(reportData.governance_framework.policies).map(([policy, status]) => new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun({ text: policy + ": ", bold: true }), new TextRun(String(status))] }))
                ] : [])
            ] : [new Paragraph({ children: [new TextRun("Governance framework not created.")] })]),
            new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Ethical Assessments")] }),
            ...(reportData.ethical_assessments && reportData.ethical_assessments.length > 0 ? 
                reportData.ethical_assessments.flatMap((assessment, idx) => [
                    new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Assessment " + (idx + 1) + ": " + (assessment.system_name || "Unnamed System"))] }),
                    new Paragraph({ children: [new TextRun({ text: "Overall Score: ", bold: true }), new TextRun(String(Math.round(assessment.overall_score || 0)) + "%")] }),
                    new Paragraph({ children: [new TextRun({ text: "Assessor: ", bold: true }), new TextRun(assessment.assessor || "Not Specified")] }),
                    new Paragraph({ children: [new TextRun({ text: "Date: ", bold: true }), new TextRun(assessment.timestamp ? assessment.timestamp.split("T")[0] : "Not Specified")] })
                ])
            : [new Paragraph({ children: [new TextRun("No ethical assessments completed.")] })]),
            new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Recommendations")] }),
            new Paragraph({ children: [new TextRun("Based on the assessments conducted, the following actions are recommended:")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Address any identified high-priority risks immediately")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Complete missing governance framework elements")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Conduct regular re-assessments as regulations evolve")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Maintain documentation for audit and compliance purposes")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Engage legal and compliance professionals for specific regulatory requirements")] }),
            new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Key Regulatory Sources")] }),
            new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("European Union")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("EU AI Act: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("EC AI Strategy: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai")] }),
            new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("United States")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("CFPB Advanced Technology: https://www.consumerfinance.gov/rules-policy/advanced-technology/")] }),
            new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("United Kingdom")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("FCA AI Approach: https://www.fca.org.uk/firms/innovation/ai-approach")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Bank of England AI Survey: https://www.bankofengland.co.uk/report/2024/artificial-intelligence-in-uk-financial-services-2024")] }),
            new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Singapore")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("MAS Veritas Initiative: https://www.mas.gov.sg/schemes-and-initiatives/veritas")] }),
            new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("Veritas Toolkit: https://github.com/veritas-toolkit/")] }),
            new Paragraph({ spacing: { before: 480 }, children: [] }),
            new Paragraph({ children: [new TextRun({ text: "Disclaimer: ", bold: true, size: 20 }), new TextRun({ text: "This report is for educational and informational purposes only. It does not constitute legal advice. Organizations should consult with qualified legal and compliance professionals for specific regulatory requirements.", size: 20, italics: true })] })
        ]
    }]
});

Packer.toBuffer(doc).then(buffer => {
    fs.writeFileSync("''' + filename + '''", buffer);
    console.log("Document created successfully");
}).catch(err => { console.error("Error:", err); process.exit(1); });
'''
    return js_code

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
st.sidebar.markdown("## 🏛️ **Navigation**")

pages = {
    "🏠 Home & Overview": "home",
    "📜 Regulatory Framework": "regulations",
    "⚠️ Risk Identification Tool": "risk_tool",
    "🔧 Governance Framework Builder": "governance",
    "✅ Ethical Assessment Checklist": "assessment",
    "📊 Case Studies & Scenarios": "cases",
    "📚 Resources & Documentation": "resources",
    "💾 Export & Reports": "export"
}

selected_page = st.sidebar.radio("Select a section:", list(pages.keys()), label_visibility="collapsed")
current_page = pages[selected_page]

# ============================================
# HOME PAGE
# ============================================
if current_page == "home":
    st.markdown('<h1 class="main-header">⚖️ FinTech AI Ethics & Governance Toolkit</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="section-blue">
        <h3 style="font-weight: 700; color: #1a365d; margin-top: 0;">🎯 Purpose</h3>
        <p>This comprehensive toolkit helps finance professionals and students identify, assess, and govern 
        the <strong>ethical and responsible use of AI</strong> and technology in financial services. Built on the latest 
        global regulations and best practices, this tool provides practical frameworks for real-world application.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""<div class="metric-container"><h2 style="color: #3182ce; margin: 0; font-weight: 700;">4+</h2><p style="color: #718096; margin: 0;"><strong>Major Regulatory Frameworks</strong></p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-container"><h2 style="color: #38a169; margin: 0; font-weight: 700;">50+</h2><p style="color: #718096; margin: 0;"><strong>Risk Categories Covered</strong></p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-container"><h2 style="color: #805ad5; margin: 0; font-weight: 700;">100+</h2><p style="color: #718096; margin: 0;"><strong>Assessment Questions</strong></p></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="metric-container"><h2 style="color: #dd6b20; margin: 0; font-weight: 700;">2025</h2><p style="color: #718096; margin: 0;"><strong>Regulations Updated</strong></p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<h2 class="sub-header">🌟 Core Ethical Principles in FinTech AI</h2>', unsafe_allow_html=True)
    
    principles_col1, principles_col2 = st.columns(2)
    
    with principles_col1:
        st.markdown("""<div class="section-green"><h4 style="font-weight: 700; color: #276749; margin-top: 0;">🎯 Fairness</h4><p>AI systems must not discriminate against individuals or groups based on protected characteristics.</p><p><strong>Key Considerations:</strong> Demographic parity, Equal opportunity, Bias detection, Regular audits</p></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="section-purple"><h4 style="font-weight: 700; color: #553c9a; margin-top: 0;">🔍 Transparency</h4><p>Financial institutions must be able to explain how AI systems make decisions.</p><p><strong>Key Considerations:</strong> Explainable AI (XAI), Clear adverse action notices, Model documentation</p></div>""", unsafe_allow_html=True)
    
    with principles_col2:
        st.markdown("""<div class="section-orange"><h4 style="font-weight: 700; color: #c05621; margin-top: 0;">👤 Accountability</h4><p>Clear lines of responsibility must exist for AI system outcomes.</p><p><strong>Key Considerations:</strong> Senior management oversight, Audit trails, Incident response procedures</p></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="section-teal"><h4 style="font-weight: 700; color: #285e61; margin-top: 0;">🔒 Privacy & Security</h4><p>AI systems must protect personal data and maintain robust security measures.</p><p><strong>Key Considerations:</strong> Data minimization, Consent management, Secure data handling</p></div>""", unsafe_allow_html=True)

# ============================================
# REGULATORY FRAMEWORK PAGE
# ============================================
elif current_page == "regulations":
    st.markdown('<h1 class="main-header">📜 Global Regulatory Framework</h1>', unsafe_allow_html=True)
    
    st.markdown("""<div class="section-blue"><p>This section provides a comprehensive overview of the <strong>major AI regulations affecting financial technology</strong> globally. Understanding these frameworks is essential for ensuring compliance and ethical AI deployment.</p></div>""", unsafe_allow_html=True)
    
    reg_tabs = st.tabs(["🇪🇺 EU AI Act", "🇺🇸 US Frameworks", "🇬🇧 UK FCA", "🇸🇬 Singapore MAS", "📋 Comparison"])
    
    with reg_tabs[0]:
        st.markdown('<h2 class="sub-header">European Union AI Act</h2>', unsafe_allow_html=True)
        st.markdown("""<span class="regulation-badge eu-badge">Effective: August 2024 - Full Compliance: August 2026</span>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="section-blue">The EU AI Act is the <strong>world's first comprehensive legal framework</strong> on artificial intelligence.<br><br><strong>🔗 Official Source:</strong> <a href="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689" target="_blank">EUR-Lex - Regulation (EU) 2024/1689</a><br><strong>🔗 EC AI Strategy:</strong> <a href="https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai" target="_blank">European Commission Digital Strategy</a></div>""", unsafe_allow_html=True)
        
        st.markdown("#### **📅 Implementation Timeline**")
        timeline_data = {"Date": ["February 2, 2025", "August 2, 2025", "August 2, 2026", "August 2, 2027"], "Milestone": ["Prohibited AI practices & AI literacy", "GPAI model rules apply", "Full high-risk AI requirements", "Extended transition for legacy systems"], "Impact": ["Ban on social scoring, emotion recognition", "Transparency rules for GenAI", "Credit scoring, risk assessment compliance", "Legacy financial products comply"]}
        st.dataframe(pd.DataFrame(timeline_data), use_container_width=True, hide_index=True)
        
        st.markdown("#### **⚠️ Penalties for Non-Compliance**")
        penalty_data = {"Violation Type": ["Prohibited AI practices", "Non-compliance with high-risk requirements", "Incorrect information to authorities"], "Maximum Fine": ["€35 million or 7% global turnover", "€15 million or 3% global turnover", "€7.5 million or 1% global turnover"]}
        st.dataframe(pd.DataFrame(penalty_data), use_container_width=True, hide_index=True)
    
    with reg_tabs[1]:
        st.markdown('<h2 class="sub-header">United States AI Regulatory Framework</h2>', unsafe_allow_html=True)
        st.markdown("""<span class="regulation-badge us-badge">Voluntary Framework with Sector-Specific Enforcement</span>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="section-purple">The US takes a <strong>sector-specific approach</strong> to AI regulation.<br><br><strong>🔗 NIST AI RMF:</strong> <a href="https://www.nist.gov/itl/ai-risk-management-framework" target="_blank">NIST AI Risk Management Framework</a><br><strong>🔗 NIST Playbook:</strong> <a href="https://airc.nist.gov/airmf-resources/airmf/" target="_blank">AI RMF Implementation Resources</a><br><strong>🔗 CFPB:</strong> <a href="https://www.consumerfinance.gov/rules-policy/advanced-technology/" target="_blank">CFPB Advanced Technology</a></div>""", unsafe_allow_html=True)
        
        st.markdown("#### **📊 NIST AI RMF Core Functions**")
        nist_col1, nist_col2 = st.columns(2)
        with nist_col1:
            st.markdown("""<div class="section-blue"><h5 style="font-weight: 700;">🏛️ GOVERN</h5><p>Establish AI governance structures, define roles, create policies</p></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="section-teal"><h5 style="font-weight: 700;">🗺️ MAP</h5><p>Context definition, stakeholder identification, risk framing</p></div>""", unsafe_allow_html=True)
        with nist_col2:
            st.markdown("""<div class="section-orange"><h5 style="font-weight: 700;">📏 MEASURE</h5><p>Metrics, testing, bias assessment, performance monitoring</p></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="section-green"><h5 style="font-weight: 700;">🔧 MANAGE</h5><p>Risk treatment, continuous monitoring, incident response</p></div>""", unsafe_allow_html=True)
    
    with reg_tabs[2]:
        st.markdown('<h2 class="sub-header">UK Financial Conduct Authority (FCA)</h2>', unsafe_allow_html=True)
        st.markdown("""<span class="regulation-badge uk-badge">Principles-Based, Outcomes-Focused Regulation</span>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="section-pink">The UK adopts a <strong>principles-based approach</strong> relying on existing frameworks.<br><br><strong>🔗 FCA AI Approach:</strong> <a href="https://www.fca.org.uk/firms/innovation/ai-approach" target="_blank">FCA AI and the FCA</a><br><strong>🔗 FCA AI Update:</strong> <a href="https://www.fca.org.uk/publication/corporate/ai-update.pdf" target="_blank">AI Update 2024 (PDF)</a><br><strong>🔗 AI Survey 2024:</strong> <a href="https://www.bankofengland.co.uk/report/2024/artificial-intelligence-in-uk-financial-services-2024" target="_blank">Bank of England AI Survey</a></div>""", unsafe_allow_html=True)
        
        st.markdown("#### **🎯 UK Government's Five AI Principles**")
        principles_data = {"Principle": ["Safety, Security & Robustness", "Transparency & Explainability", "Fairness", "Accountability & Governance", "Contestability & Redress"], "FCA Application": ["Threshold Conditions, SMCR, operational resilience", "Consumer Duty fair value, disclosure obligations", "Consumer Duty, Principles for Business", "Senior Managers Regime, governance arrangements", "Complaints handling, vulnerable customer guidance"]}
        st.dataframe(pd.DataFrame(principles_data), use_container_width=True, hide_index=True)
    
    with reg_tabs[3]:
        st.markdown('<h2 class="sub-header">Singapore Monetary Authority (MAS)</h2>', unsafe_allow_html=True)
        st.markdown("""<span class="regulation-badge sg-badge">FEAT Principles & Veritas Framework</span>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="section-green">Singapore has pioneered a <strong>collaborative, principles-based approach</strong> through FEAT and Veritas.<br><br><strong>🔗 MAS Veritas Initiative:</strong> <a href="https://www.mas.gov.sg/schemes-and-initiatives/veritas" target="_blank">MAS Veritas</a><br><strong>🔗 Veritas Toolkit:</strong> <a href="https://github.com/veritas-toolkit/" target="_blank">GitHub - Veritas Toolkit</a><br><strong>🔗 Project MindForge:</strong> <a href="https://www.mas.gov.sg/schemes-and-initiatives/project-mindforge" target="_blank">MAS Project MindForge (GenAI)</a></div>""", unsafe_allow_html=True)
        
        st.markdown("#### **🎯 FEAT Principles**")
        feat_col1, feat_col2 = st.columns(2)
        with feat_col1:
            st.markdown("""<div class="section-green"><h5 style="font-weight: 700;">F - Fairness</h5><p>No systematic disadvantage, regular bias assessment, fairness metrics</p></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="section-purple"><h5 style="font-weight: 700;">E - Ethics</h5><p>AI aligned with organizational values, ethical review processes</p></div>""", unsafe_allow_html=True)
        with feat_col2:
            st.markdown("""<div class="section-orange"><h5 style="font-weight: 700;">A - Accountability</h5><p>Clear ownership, documented processes, audit trails</p></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="section-teal"><h5 style="font-weight: 700;">T - Transparency</h5><p>Appropriate explainability, clear communication, documentation</p></div>""", unsafe_allow_html=True)
    
    with reg_tabs[4]:
        st.markdown('<h2 class="sub-header">Regulatory Comparison Matrix</h2>', unsafe_allow_html=True)
        comparison_data = {"Aspect": ["Approach", "Legal Status", "Explainability", "Penalties", "Scope"], "EU AI Act": ["Prescriptive, risk-based", "Binding regulation", "Mandatory for high-risk", "Up to €35M or 7%", "All in EU"], "US (NIST)": ["Sector-specific, voluntary", "Voluntary + enforcement", "ECOA for credit", "Varies by agency", "Sector-specific"], "UK FCA": ["Principles-based", "Existing rules", "Consumer Duty", "FCA regime", "FCA-regulated"], "Singapore MAS": ["Principles-based", "Voluntary", "FEAT principle", "MAS powers", "FIs in Singapore"]}
        st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

# ============================================
# RISK IDENTIFICATION TOOL
# ============================================
elif current_page == "risk_tool":
    st.markdown('<h1 class="main-header">⚠️ AI Risk Identification Tool</h1>', unsafe_allow_html=True)
    
    st.markdown("""<div class="section-orange"><p>Use this interactive tool to <strong>identify and assess AI-related risks</strong> in your FinTech application.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("### **Step 1: Define Your AI Use Case**")
    
    use_case_col1, use_case_col2 = st.columns(2)
    with use_case_col1:
        use_case_type = st.selectbox("**AI Application Type:**", ["Credit Scoring/Underwriting", "Fraud Detection", "Customer Service Chatbot", "Investment Advisory (Robo-Advisor)", "Anti-Money Laundering (AML)", "Insurance Underwriting/Pricing", "Marketing/Personalization", "Other"])
        deployment_stage = st.selectbox("**Deployment Stage:**", ["Planning/Design", "Development", "Testing", "Production", "Legacy System Review"])
    with use_case_col2:
        jurisdictions = st.multiselect("**Operating Jurisdictions:**", ["European Union", "United States", "United Kingdom", "Singapore", "Other"])
        customer_type = st.multiselect("**Customer Types:**", ["Retail Consumers", "Small Business", "Corporate/Institutional", "High Net Worth"])
    
    st.markdown("---")
    st.markdown("### **Step 2: Risk Assessment Questionnaire**")
    
    risk_categories = {
        "Fairness & Discrimination": [("Does the AI make decisions impacting credit access?", 3), ("Is training data representative?", 2), ("Have you conducted disparate impact testing?", 3)],
        "Transparency & Explainability": [("Can you explain individual decisions?", 3), ("Do you provide adverse action notices?", 3), ("Is model logic documented?", 2)],
        "Data Quality & Privacy": [("Is personal data collected with consent?", 3), ("Are data retention policies enforced?", 2), ("Is training data validated?", 2)],
        "Accountability & Governance": [("Is there a designated senior manager accountable?", 3), ("Are escalation procedures established?", 2), ("Is there board reporting on AI risks?", 2)]
    }
    
    responses = {}
    risk_scores = {}
    
    for category, questions in risk_categories.items():
        with st.expander(f"📋 **{category}**", expanded=False):
            responses[category] = {}
            category_score = 0
            max_score = 0
            for i, (question, weight) in enumerate(questions):
                response = st.radio(question, ["Yes - Fully Implemented", "Partial - In Progress", "No - Not Addressed", "N/A"], key=f"{category}_{i}", horizontal=True)
                responses[category][question] = response
                max_score += weight
                if response == "Yes - Fully Implemented": category_score += weight
                elif response == "Partial - In Progress": category_score += weight * 0.5
                elif response == "N/A": max_score -= weight
            risk_scores[category] = {"score": (category_score / max_score) * 100 if max_score > 0 else 100, "weight": 1.0}
    
    st.markdown("---")
    
    if st.button("🔍 **Generate Risk Analysis**", type="primary"):
        overall_score = sum(s["score"] for s in risk_scores.values()) / len(risk_scores) if risk_scores else 0
        risk_level = "Low" if overall_score >= 80 else "Medium" if overall_score >= 60 else "High"
        risk_color = "#38a169" if overall_score >= 80 else "#dd6b20" if overall_score >= 60 else "#c53030"
        
        st.markdown("### **Step 3: Risk Analysis Results**")
        
        fig = go.Figure(go.Indicator(mode="gauge+number", value=overall_score, domain={'x': [0, 1], 'y': [0, 1]}, title={'text': "Overall Risk Readiness Score"}, gauge={'axis': {'range': [0, 100]}, 'bar': {'color': risk_color}, 'steps': [{'range': [0, 60], 'color': "#fed7d7"}, {'range': [60, 80], 'color': "#feebc8"}, {'range': [80, 100], 'color': "#c6f6d5"}]}))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""<div style="text-align: center; margin: 1rem 0;"><span class="risk-{'low' if risk_level == 'Low' else 'medium' if risk_level == 'Medium' else 'high'}" style="font-size: 1.25rem;"><strong>Risk Level: {risk_level}</strong></span></div>""", unsafe_allow_html=True)
        
        st.session_state.risk_assessment = {"timestamp": datetime.now().isoformat(), "use_case": use_case_type, "jurisdictions": jurisdictions, "overall_score": overall_score, "risk_level": risk_level, "category_scores": {cat: data["score"] for cat, data in risk_scores.items()}, "responses": responses}
        st.success("✅ Risk assessment saved! Export from the Export & Reports section.")

# ============================================
# GOVERNANCE FRAMEWORK BUILDER
# ============================================
elif current_page == "governance":
    st.markdown('<h1 class="main-header">🔧 Governance Framework Builder</h1>', unsafe_allow_html=True)
    
    st.markdown("""<div class="section-purple"><p>Build a <strong>customized AI governance framework</strong> for your organization.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("### **📋 Organization Profile**")
    org_col1, org_col2 = st.columns(2)
    with org_col1:
        org_size = st.selectbox("**Organization Size:**", ["Startup (<50)", "SME (50-250)", "Mid-size (250-1000)", "Large Enterprise (1000+)"])
        primary_business = st.selectbox("**Primary Business:**", ["Retail Banking", "Commercial Banking", "Investment Banking", "Asset Management", "Insurance", "Payments/FinTech", "Lending Platform", "Other"])
    with org_col2:
        regulatory_status = st.selectbox("**Regulatory Status:**", ["Fully Regulated (Bank License)", "Regulated (Other License)", "Registered/Authorized", "Unregulated", "Seeking Authorization"])
        ai_maturity = st.selectbox("**AI Maturity Level:**", ["Exploring", "Emerging (1-2 Production)", "Established (Multiple)", "Advanced (AI-First)"])
    
    st.markdown("---")
    st.markdown("### **🏗️ Governance Framework Components**")
    
    framework_tabs = st.tabs(["1️⃣ Structure", "2️⃣ Policies", "3️⃣ Risk Management"])
    
    governance_plan = {}
    
    with framework_tabs[0]:
        st.markdown("#### **👤 Accountability Framework**")
        acc_col1, acc_col2 = st.columns(2)
        with acc_col1:
            ai_officer = st.text_input("**Chief AI/Data Officer:**", placeholder="Name and title")
            ai_sponsor = st.text_input("**Executive Sponsor:**", placeholder="Board/C-suite member")
        with acc_col2:
            ai_risk_owner = st.text_input("**AI Risk Owner:**", placeholder="Head of Risk/CRO")
            ai_ethics_owner = st.text_input("**AI Ethics/Compliance Owner:**", placeholder="CCO/Ethics Officer")
        has_ai_committee = st.checkbox("AI Ethics/Governance Committee established")
        has_model_committee = st.checkbox("Model Risk Committee established")
        governance_plan["structure"] = {"ai_officer": ai_officer, "ai_sponsor": ai_sponsor, "ai_risk_owner": ai_risk_owner, "ai_ethics_owner": ai_ethics_owner, "has_ai_committee": has_ai_committee, "has_model_committee": has_model_committee}
    
    with framework_tabs[1]:
        st.markdown("#### **Core AI Policies**")
        policy_status = {}
        core_policies = [("AI Ethics Policy", "Defines ethical principles"), ("AI Risk Management Policy", "Framework for AI risks"), ("Model Risk Management Policy", "SR 11-7 aligned"), ("Data Governance Policy", "Data quality and privacy"), ("Third-Party AI Policy", "Vendor oversight"), ("AI Transparency Policy", "Explainability requirements"), ("AI Fairness Policy", "Bias prevention"), ("AI Incident Management Policy", "Failure response")]
        for policy, description in core_policies:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{policy}**")
                st.caption(description)
            with col2:
                policy_status[policy] = st.selectbox("Status", ["Not Started", "In Development", "Under Review", "Approved", "N/A"], key=f"policy_{policy}")
        governance_plan["policies"] = policy_status
    
    with framework_tabs[2]:
        st.markdown("#### **📊 Risk Taxonomy**")
        risk_taxonomy = st.multiselect("**Risk Categories to Address:**", ["Model Risk", "Fairness/Discrimination Risk", "Data Quality Risk", "Privacy Risk", "Cybersecurity Risk", "Operational Risk", "Regulatory Risk", "Reputational Risk", "Third-Party Risk"], default=["Model Risk", "Fairness/Discrimination Risk", "Regulatory Risk"])
        governance_plan["risk_management"] = {"taxonomy": risk_taxonomy}
    
    st.markdown("---")
    
    if st.button("📄 **Generate Governance Framework**", type="primary"):
        st.session_state.governance_plan = governance_plan
        st.markdown("""<div class="success-card"><h4 style="font-weight: 700;">✅ Framework Generated Successfully</h4><p>Export from the <strong>Export & Reports</strong> section as DOCX.</p></div>""", unsafe_allow_html=True)

# ============================================
# ETHICAL ASSESSMENT CHECKLIST
# ============================================
elif current_page == "assessment":
    st.markdown('<h1 class="main-header">✅ Ethical Assessment Checklist</h1>', unsafe_allow_html=True)
    
    st.markdown("""<div class="section-green"><p>Complete this comprehensive checklist to assess the <strong>ethical readiness</strong> of your AI system.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("### **📝 System Information**")
    sys_col1, sys_col2 = st.columns(2)
    with sys_col1:
        system_name = st.text_input("**AI System Name:**", placeholder="e.g., Credit Decision Engine v2.0")
        system_owner = st.text_input("**System Owner:**", placeholder="Name and department")
    with sys_col2:
        assessment_date = st.date_input("**Assessment Date:**", value=datetime.now())
        assessor_name = st.text_input("**Assessor:**", placeholder="Your name")
    
    st.markdown("---")
    
    assessment_sections = {
        "1. Fairness & Non-Discrimination": [("1.1", "Protected characteristics are not used as direct inputs", "Critical"), ("1.2", "Disparate impact testing has been conducted", "Critical"), ("1.3", "Human override is available for edge cases", "High")],
        "2. Transparency & Explainability": [("2.1", "Individual decisions can be explained to consumers", "Critical"), ("2.2", "Adverse action notices include specific reasons", "Critical"), ("2.3", "Model logic and features are documented", "High")],
        "3. Accountability & Governance": [("3.1", "Senior manager designated as accountable", "Critical"), ("3.2", "Audit trails capture all AI decisions", "Critical"), ("3.3", "Escalation procedures are established", "High")],
        "4. Data Quality & Privacy": [("4.1", "Personal data collected with appropriate consent", "Critical"), ("4.2", "Data quality has been validated", "High"), ("4.3", "Privacy impact assessment conducted", "High")]
    }
    
    assessment_results = {}
    section_scores = {}
    
    for section, items in assessment_sections.items():
        with st.expander(f"📋 **{section}**", expanded=False):
            section_results = {}
            compliant_count = 0
            total = len(items)
            for item_id, item_text, priority in items:
                col1, col2, col3 = st.columns([0.5, 3, 1.5])
                with col1: st.markdown(f"**{item_id}**")
                with col2: st.markdown(f"{item_text} {'🔴 *Critical*' if priority == 'Critical' else '🟠 *High*'}")
                with col3:
                    status = st.selectbox("Status", ["Not Assessed", "Compliant", "Partial", "Non-Compliant", "N/A"], key=f"check_{item_id}", label_visibility="collapsed")
                    section_results[item_id] = {"text": item_text, "priority": priority, "status": status}
                    if status == "Compliant": compliant_count += 1
                    elif status == "Partial": compliant_count += 0.5
                    elif status == "N/A": total -= 1
            assessment_results[section] = section_results
            section_scores[section] = (compliant_count / total * 100) if total > 0 else 100
    
    st.markdown("---")
    
    if st.button("📊 **Generate Assessment Report**", type="primary"):
        overall_score = sum(section_scores.values()) / len(section_scores) if section_scores else 0
        status_color = "#38a169" if overall_score >= 80 else "#dd6b20" if overall_score >= 60 else "#c53030"
        overall_status = "Ready for Production" if overall_score >= 80 else "Needs Improvement" if overall_score >= 60 else "Not Ready"
        
        st.markdown("### **📊 Assessment Results**")
        st.markdown(f"""<div class="metric-container" style="margin: 1rem auto; max-width: 400px;"><h2 style="color: {status_color}; margin: 0; font-weight: 700;">{overall_score:.1f}%</h2><p style="color: #718096; margin: 0;"><strong>Overall Compliance Score</strong></p><p style="color: {status_color}; margin-top: 0.5rem;"><strong>{overall_status}</strong></p></div>""", unsafe_allow_html=True)
        
        st.session_state.completed_assessments.append({"timestamp": datetime.now().isoformat(), "system_name": system_name, "assessor": assessor_name, "overall_score": overall_score, "section_scores": section_scores, "results": assessment_results})
        st.success("✅ Assessment saved! Export from the Export & Reports section.")

# ============================================
# CASE STUDIES & SCENARIOS
# ============================================
elif current_page == "cases":
    st.markdown('<h1 class="main-header">📊 Case Studies & Scenarios</h1>', unsafe_allow_html=True)
    
    st.markdown("""<div class="section-teal"><p>Learn from <strong>real-world scenarios and case studies</strong> involving AI ethics in financial services.</p></div>""", unsafe_allow_html=True)
    
    case_tabs = st.tabs(["📊 Credit Scoring Bias", "🤖 Chatbot Failure", "📈 Algorithmic Trading"])
    
    with case_tabs[0]:
        st.markdown("### **Case Study: Discriminatory Credit Scoring Model**")
        st.markdown("""<div class="warning-card"><h4 style="font-weight: 700;">⚠️ Scenario Overview</h4><p>A fintech lender's AI model showed <strong>23% lower approval rates</strong> for minority applicants with similar credit profiles.</p></div>""", unsafe_allow_html=True)
        st.markdown("""
#### **⚠️ What Went Wrong**
| **Feature** | **Issue** | **Impact** |
|---------|-------|--------|
| ZIP code stability | Correlated with racial composition | Disparate impact |
| University attended | Proxy for socioeconomic status | Disparate impact |
| Social media sentiment | Biased training data | Algorithmic bias |

#### **🔧 Key Lessons**
- Alternative data requires extra scrutiny
- Fairness testing must be proactive
- Diverse teams catch more issues
- Continuous monitoring is essential

**🔗 Relevant Regulation:** [CFPB Fair Lending Guidance](https://www.consumerfinance.gov/rules-policy/regulations/1002/)
        """)
    
    with case_tabs[1]:
        st.markdown("### **Case Study: Customer Service Chatbot Failure**")
        st.markdown("""<div class="warning-card"><h4 style="font-weight: 700;">⚠️ Scenario Overview</h4><p>A bank's AI chatbot provided <strong>incorrect dispute rights information</strong> and failed to recognize statutory protections.</p></div>""", unsafe_allow_html=True)
        st.markdown("""
#### **🔧 Key Lessons**
- Regulatory content requires special handling
- Escalation triggers must be comprehensive
- Chatbots cannot replace required disclosures

**🔗 Relevant Guidance:** [CFPB Chatbot Guidance](https://www.consumerfinance.gov/about-us/blog/chatbots-in-consumer-finance/)
        """)
    
    with case_tabs[2]:
        st.markdown("### **Case Study: AI Trading System Malfunction**")
        st.markdown("""<div class="warning-card"><h4 style="font-weight: 700;">⚠️ Scenario Overview</h4><p>An AI trading system caused <strong>$180M client losses</strong> during market volatility.</p></div>""", unsafe_allow_html=True)
        st.markdown("""
#### **🔧 Key Lessons**
- Historical data has limits
- Speed requires automated safeguards
- Uncertainty estimation is crucial
- Stress testing must go beyond history
        """)

# ============================================
# RESOURCES & DOCUMENTATION
# ============================================
elif current_page == "resources":
    st.markdown('<h1 class="main-header">📚 Resources & Documentation</h1>', unsafe_allow_html=True)
    
    st.markdown("""<div class="section-blue"><p>Access comprehensive resources and <strong>official documentation</strong> for AI ethics in financial services.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("### **📜 Official Regulatory Documents**")
    
    st.markdown("""
<div class="section-blue">
<h4 style="font-weight: 700; margin-top: 0;">🇪🇺 European Union</h4>

| **Document** | **Description** | **Link** |
|----------|-------------|------|
| EU AI Act (2024/1689) | Comprehensive AI regulation | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689) |
| GDPR (2016/679) | Data protection framework | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679) |
| AI Office Guidelines | Implementation guidance | [EC Digital Strategy](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) |
</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
<div class="section-purple">
<h4 style="font-weight: 700; margin-top: 0;">🇺🇸 United States</h4>

| **Document** | **Description** | **Link** |
|----------|-------------|------|
| NIST AI RMF 1.0 | AI Risk Management Framework | [NIST](https://www.nist.gov/itl/ai-risk-management-framework) |
| NIST AI RMF Playbook | Implementation guidance | [NIST Playbook](https://airc.nist.gov/airmf-resources/airmf/) |
| CFPB AI Guidance | Consumer protection in AI | [CFPB](https://www.consumerfinance.gov/rules-policy/advanced-technology/) |
</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
<div class="section-pink">
<h4 style="font-weight: 700; margin-top: 0;">🇬🇧 United Kingdom</h4>

| **Document** | **Description** | **Link** |
|----------|-------------|------|
| FCA AI Approach | FCA approach to AI | [FCA](https://www.fca.org.uk/firms/innovation/ai-approach) |
| FCA AI Update (2024) | AI regulatory update | [FCA PDF](https://www.fca.org.uk/publication/corporate/ai-update.pdf) |
| AI Survey 2024 | AI usage in UK FS | [Bank of England](https://www.bankofengland.co.uk/report/2024/artificial-intelligence-in-uk-financial-services-2024) |
</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
<div class="section-green">
<h4 style="font-weight: 700; margin-top: 0;">🇸🇬 Singapore</h4>

| **Document** | **Description** | **Link** |
|----------|-------------|------|
| FEAT Principles | Fairness, Ethics, Accountability, Transparency | [MAS](https://www.mas.gov.sg/publications/monographs-or-information-paper/2018/feat) |
| Veritas Initiative | FEAT implementation | [MAS Veritas](https://www.mas.gov.sg/schemes-and-initiatives/veritas) |
| Veritas Toolkit | Open-source tools | [GitHub](https://github.com/veritas-toolkit/) |
| Project MindForge | GenAI in finance | [MAS MindForge](https://www.mas.gov.sg/schemes-and-initiatives/project-mindforge) |
</div>
    """, unsafe_allow_html=True)
    
    st.markdown("### **🔧 Technical Tools**")
    st.markdown("""
<div class="section-gray">

| **Tool** | **Purpose** | **Source** |
|------|---------|--------|
| Veritas Toolkit | FEAT assessment | [GitHub](https://github.com/veritas-toolkit/) |
| AI Fairness 360 | Bias detection | [IBM](https://aif360.mybluemix.net/) |
| Fairlearn | Fairness assessment | [Microsoft](https://fairlearn.org/) |
| SHAP | Explainability | [GitHub](https://github.com/shap/shap) |
| LIME | Local explanations | [GitHub](https://github.com/marcotcr/lime) |
</div>
    """, unsafe_allow_html=True)

# ============================================
# EXPORT & REPORTS
# ============================================
elif current_page == "export":
    st.markdown('<h1 class="main-header">💾 Export & Reports</h1>', unsafe_allow_html=True)
    
    st.markdown("""<div class="section-gray"><p>Generate and export reports in <strong>DOCX format</strong> for documentation, audit, and compliance purposes.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("### **📤 Available Data**")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        st.markdown("#### **📊 Risk Assessment**")
        if st.session_state.risk_assessment:
            st.markdown("""<div class="success-card"><p>✅ <strong>Risk assessment data available</strong></p></div>""", unsafe_allow_html=True)
            st.write(f"**Use Case:** {st.session_state.risk_assessment.get('use_case', 'N/A')}")
            st.write(f"**Risk Level:** {st.session_state.risk_assessment.get('risk_level', 'N/A')}")
            st.write(f"**Score:** {st.session_state.risk_assessment.get('overall_score', 0):.1f}%")
        else:
            st.markdown("""<div class="warning-card"><p>⚠️ No risk assessment completed.</p></div>""", unsafe_allow_html=True)
    
    with export_col2:
        st.markdown("#### **🔧 Governance Framework**")
        if st.session_state.governance_plan:
            st.markdown("""<div class="success-card"><p>✅ <strong>Governance framework data available</strong></p></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="warning-card"><p>⚠️ No governance framework created.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### **📋 Generate Comprehensive DOCX Report**")
    st.markdown("Generate a professional Word document combining all assessment data, suitable for compliance documentation and audit purposes.")
    
    if st.button("📄 **Generate DOCX Report**", type="primary"):
        report_data = {
            "report_metadata": {"generated_at": datetime.now().isoformat(), "tool_version": "1.0.0", "framework_references": ["EU AI Act (2024/1689)", "NIST AI RMF 1.0", "UK FCA AI Update 2024", "Singapore MAS FEAT"]},
            "risk_assessment": st.session_state.risk_assessment if st.session_state.risk_assessment else None,
            "governance_framework": st.session_state.governance_plan if st.session_state.governance_plan else None,
            "ethical_assessments": st.session_state.completed_assessments if st.session_state.completed_assessments else None
        }
        
        js_code = generate_docx_report(report_data, "/tmp/ai_ethics_report.docx")
        
        with open("/tmp/generate_report.js", "w") as f:
            f.write(js_code)
        
        try:
            result = subprocess.run(["node", "/tmp/generate_report.js"], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists("/tmp/ai_ethics_report.docx"):
                with open("/tmp/ai_ethics_report.docx", "rb") as f:
                    docx_data = f.read()
                
                st.download_button(label="📥 **Download DOCX Report**", data=docx_data, file_name=f"AI_Ethics_Governance_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                st.success("✅ DOCX report generated successfully!")
            else:
                st.error(f"Error generating DOCX: {result.stderr}")
                report_json = json.dumps(report_data, indent=2, default=str)
                st.download_button(label="📥 Download JSON (Fallback)", data=report_json, file_name=f"ai_ethics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", mime="application/json")
        except Exception as e:
            st.error(f"Error: {str(e)}")
            report_json = json.dumps(report_data, indent=2, default=str)
            st.download_button(label="📥 Download JSON (Fallback)", data=report_json, file_name=f"ai_ethics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", mime="application/json")

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <h4 style="font-weight: 700; margin-top: 0;">⚖️ FinTech AI Ethics & Governance Toolkit</h4>
    <p><strong>Version 1.0.0</strong> | Last Updated: November 2025</p>
    <p style="margin-top: 1rem;">
        Developed by <a href="https://www.ntu.ac.uk/staff-profiles/business/vangelis-tsiligkiris" target="_blank"><strong>Vangelis Tsiligkiris</strong> | Nottingham Trent University</a>
    </p>
    <p style="font-size: 0.85rem; margin-top: 1.5rem; opacity: 0.9;">
        This tool is for educational purposes. Always consult with legal and compliance professionals for specific regulatory requirements.
    </p>
</div>
""", unsafe_allow_html=True)
