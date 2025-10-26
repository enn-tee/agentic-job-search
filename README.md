# Agentic Resume Tailoring System

An intelligent, agent-based system for tailoring resumes to specific job postings with industry-specific optimization.

## 🎯 Features

- **Multi-Agent Architecture**: Specialized agents for job analysis, resume matching, tailoring, and quality review
- **Industry-Agnostic Design**: Plugin-based architecture supporting multiple industries (Healthcare, Tech, Finance, etc.)
- **Resume Pool Management**: Versioned resume storage with intelligent tagging and search
- **ATS Optimization**: Natural keyword integration for Applicant Tracking Systems
- **Optional MCP Integration**: Extensible support for Model Context Protocol servers

## 📁 Project Structure

```
agentic-job-search/
├── src/
│   ├── agents/              # Specialized AI agents
│   ├── core/                # Core abstractions and interfaces
│   ├── services/            # Business logic services
│   ├── models/              # Data models
│   └── utils/               # Utility functions
├── config/
│   ├── industries/          # Industry-specific configurations
│   └── prompts/             # Agent prompt templates
├── resume_pool/
│   ├── base_resumes/        # Base resume templates
│   ├── tailored_resumes/    # Generated tailored resumes
│   ├── metadata/            # Resume metadata and index
│   └── job_postings/        # Archived job postings
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
└── scripts/                 # Utility scripts
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Anthropic API key

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd agentic-job-search

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Basic Usage

```bash
# Tailor resume for a job posting
python main.py --job-url "https://example.com/job-posting"

# Use a specific base resume
python main.py --job-url "..." --base-resume "healthcare_analyst_base"

# Specify industry
python main.py --job-url "..." --industry healthcare
```

## 🏗️ Architecture

### Agent Pipeline

```
Job URL Input
    ↓
Job Posting Analyzer Agent
    ↓
Resume Matcher Agent
    ↓
Tailoring Orchestrator Agent
    ├── Summary Optimizer
    ├── Bullet Point Enhancer
    ├── ATS Keyword Optimizer
    └── Skills Alignment Agent
    ↓
Quality Reviewer Agent
    ↓
Tailored Resume Output
```

### Industry Abstraction Layer

The system uses a plugin-based architecture to support multiple industries:

- **Industry Adapters**: Define industry-specific behavior
- **YAML Configurations**: Industry terminology, keywords, job boards
- **Optional MCP Servers**: Industry-specific data sources and tools

## 🔧 Configuration

### Industry Profiles

Industries are configured via YAML files in `config/industries/`:

```yaml
# config/industries/healthcare.yaml
industry: healthcare
display_name: "Healthcare & Life Sciences"

terminology:
  acronyms:
    EHR: "Electronic Health Records"
    FHIR: "Fast Healthcare Interoperability Resources"

skill_categories:
  clinical_knowledge:
    - Medical terminology
    - HIPAA compliance
  technical_skills:
    - SQL (healthcare databases)
    - Python/R (clinical analytics)
```

### Adding a New Industry

1. Create `config/industries/{industry_name}.yaml`
2. Define terminology, skills, and job boards
3. Optionally create a custom `IndustryAdapter` in `src/core/adapters.py`

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test suite
pytest tests/unit/test_agents.py
```

## 📋 Roadmap

### Phase 1: MVP (Current)
- [x] Core project structure
- [x] Industry abstraction layer
- [ ] Basic agent implementations
- [ ] Healthcare industry configuration
- [ ] CLI interface

### Phase 2: Job Automation
- [ ] MCP integration layer
- [ ] Google Jobs MCP server integration
- [ ] Web scraping for job postings
- [ ] Automated job monitoring

### Phase 3: Advanced Features
- [ ] OMOP/FHIR MCP for healthcare terminology
- [ ] Memory MCP for learning patterns
- [ ] Multi-variant resume generation
- [ ] Web UI

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [Anthropic Claude](https://www.anthropic.com/claude)
- Inspired by the Model Context Protocol (MCP)
