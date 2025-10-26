# Product Enhancement TODO

Track features, improvements, and questions for the Agentic Resume Tailoring System.

---

## 🔥 High Priority

### Architecture Decisions

- [ ] **Evaluate orchestration frameworks**
  - [ ] Research LangGraph integration
    - Pros: State management, conditional flows, graph-based
    - Cons: Added complexity
    - Effort: Medium (2-3 days)
  - [ ] Research CrewAI integration
    - Pros: Agent collaboration, built-in patterns
    - Cons: Opinionated, heavier
    - Effort: Medium (2-3 days)
  - [ ] Decide: Keep custom orchestration vs adopt framework
  - **Question**: Do we need parallel agent execution? Complex workflows?
  - **Notes**: Current custom approach works well for sequential pipeline

- [ ] **Agent parallelization**
  - Current: Sequential execution (analyzer → matcher → tailoring → review)
  - Enhancement: Run multiple tailoring strategies in parallel
  - Would LangGraph/CrewAI help here?

### Core Features

- [ ] **Web scraping for job postings**
  - [ ] Implement Beautiful Soup + Playwright job scraper
  - [ ] Support LinkedIn job URLs
  - [ ] Support Indeed job URLs
  - [ ] Support company career pages
  - [ ] Handle authentication/paywalls
  - Priority: HIGH
  - Effort: 1-2 weeks

- [ ] **Resume format conversion**
  - [ ] JSON → PDF export (using reportlab or weasyprint)
  - [ ] JSON → DOCX export (using python-docx)
  - [ ] Template system for different resume styles
  - [ ] ATS-friendly formatting rules
  - Priority: HIGH
  - Effort: 1 week

- [ ] **MCP Server Integration**
  - [ ] Implement Google Jobs MCP server integration
    - Requires: SerpAPI key
    - Benefit: Automated job discovery
  - [ ] Test OMOP MCP for healthcare terminology
  - [ ] Test FHIR MCP for health data standards
  - [ ] Create abstraction for MCP client management
  - Priority: MEDIUM
  - Effort: 1-2 weeks
  - **Question**: Which MCP servers provide most value?

---

## 📊 Medium Priority

### User Experience

- [ ] **Interactive resume builder**
  - [ ] CLI wizard to create base resume JSON
  - [ ] Guided prompts for each section
  - [ ] Validation and formatting help
  - Priority: MEDIUM
  - Effort: 3-5 days

- [ ] **Resume pool management**
  - [ ] List all resumes in pool (CLI command)
  - [ ] Search/filter by tags, skills, industry
  - [ ] View resume details
  - [ ] Delete/archive old resumes
  - Priority: MEDIUM
  - Effort: 2-3 days

- [ ] **Multi-variant generation**
  - [ ] Generate 2-3 resume variations per job:
    - Impact-focused (metrics heavy)
    - Technical-focused (tech stack emphasis)
    - Leadership-focused (management emphasis)
  - [ ] Let user select best variant
  - Priority: MEDIUM
  - Effort: 1 week

- [ ] **Diff visualization**
  - [ ] Show before/after comparison
  - [ ] Highlight changes in summary, bullets, skills
  - [ ] Export diff as HTML or PDF
  - Priority: MEDIUM
  - Effort: 3-5 days

### Analytics & Learning

- [ ] **Success tracking**
  - [ ] Mark resumes that got interviews
  - [ ] Track which modifications work best
  - [ ] Learn from patterns over time
  - [ ] Dashboard showing success metrics
  - Priority: MEDIUM
  - Effort: 1 week
  - **Question**: How to measure success? Interview rate? Callback rate?

- [ ] **Memory/Learning system**
  - [ ] Integrate Memory MCP server
  - [ ] Store successful patterns
  - [ ] Learn which keywords/phrases work
  - [ ] Improve matching over time
  - Priority: MEDIUM
  - Effort: 1-2 weeks
  - Depends on: MCP integration

---

## 🔧 Low Priority / Nice to Have

### Additional Features

- [ ] **Batch processing**
  - [ ] Process multiple jobs at once
  - [ ] Generate tailored resumes for 5-10 jobs
  - [ ] Compare job matches across batch
  - Priority: LOW
  - Effort: 3-5 days

- [ ] **Cover letter generation**
  - [ ] New agent: CoverLetterWriter
  - [ ] Use job analysis + resume
  - [ ] Industry-specific templates
  - Priority: LOW
  - Effort: 1 week

- [ ] **Job monitoring**
  - [ ] Monitor job boards for new postings
  - [ ] Alert when matching jobs appear
  - [ ] Auto-generate tailored resume
  - Priority: LOW
  - Effort: 2 weeks
  - Depends on: Web scraping, MCP Google Jobs

- [ ] **LinkedIn profile optimizer**
  - [ ] Similar to resume tailoring
  - [ ] Optimize headline, summary, experience
  - [ ] Export to LinkedIn format
  - Priority: LOW
  - Effort: 1 week

### UI/UX Improvements

- [ ] **Web UI (Streamlit or Gradio)**
  - [ ] Upload resume via web form
  - [ ] Paste job posting or URL
  - [ ] View tailored resume in browser
  - [ ] Download PDF/DOCX
  - Priority: LOW
  - Effort: 2-3 weeks

- [ ] **Rich CLI output**
  - [ ] Better formatting with Rich library
  - [ ] Progress bars for agent execution
  - [ ] Colored output for different stages
  - [ ] Tables for resume comparisons
  - Priority: LOW
  - Effort: 2-3 days

---

## 🌍 Industry Expansion

- [ ] **Finance industry**
  - [ ] Create finance.yaml configuration
  - [ ] Research finance terminology (trading, compliance, etc.)
  - [ ] Add finance-specific keywords
  - [ ] Finance certifications (CFA, FRM, etc.)
  - Priority: MEDIUM
  - Effort: 2-3 days

- [ ] **Education industry**
  - [ ] Create education.yaml
  - [ ] Teaching certifications
  - [ ] Educational technology
  - Priority: LOW
  - Effort: 2-3 days

- [ ] **Non-profit sector**
  - [ ] Create nonprofit.yaml
  - [ ] Grant writing, fundraising terms
  - [ ] Non-profit specific keywords
  - Priority: LOW
  - Effort: 2-3 days

- [ ] **Marketing/Sales**
  - [ ] Create marketing.yaml
  - [ ] Marketing tools (HubSpot, Salesforce, etc.)
  - [ ] Growth metrics and KPIs
  - Priority: LOW
  - Effort: 2-3 days

---

## 🐛 Bug Fixes / Technical Debt

- [ ] **Error handling improvements**
  - [ ] Better error messages for API failures
  - [ ] Retry logic for Claude API calls
  - [ ] Graceful degradation when agents fail
  - Priority: MEDIUM
  - Effort: 2-3 days

- [ ] **Input validation**
  - [ ] Validate resume JSON schema
  - [ ] Check for required fields
  - [ ] Helpful error messages
  - Priority: MEDIUM
  - Effort: 1-2 days

- [ ] **Logging improvements**
  - [ ] Structured logging (JSON format)
  - [ ] Log levels (DEBUG, INFO, WARN, ERROR)
  - [ ] Save logs to files
  - Priority: LOW
  - Effort: 1 day

- [ ] **Unit test coverage**
  - [ ] Tests for each agent
  - [ ] Tests for industry adapters
  - [ ] Tests for services
  - [ ] Integration tests for full workflow
  - Priority: MEDIUM
  - Effort: 1 week

---

## ❓ Open Questions

### Architecture
- [ ] Should we adopt LangGraph or CrewAI?
  - **Pros**: Better state management, conditional flows
  - **Cons**: Added complexity, learning curve
  - **Decision needed by**: [Date]

- [ ] How to handle agent failures?
  - Retry? Skip? Fail entire pipeline?
  - Current: Fails entire pipeline
  - Better approach?

- [ ] Should agents run in parallel where possible?
  - Example: Generate multiple resume variants simultaneously
  - Would require async/await or threading

### Product
- [ ] What metrics define a "successful" tailored resume?
  - Interview requests received?
  - Callback rate?
  - User satisfaction?

- [ ] Should we support multiple resume formats in the pool?
  - Currently: JSON only
  - Support PDF/DOCX as input?

- [ ] How to price this if commercialized?
  - Per resume generated?
  - Subscription?
  - Free tier?

### MCP Integration
- [ ] Which MCP servers provide the most value?
  - Google Jobs (job discovery) - HIGH VALUE
  - OMOP/FHIR (healthcare only) - NICHE VALUE
  - Memory (learning) - MEDIUM VALUE

- [ ] Should MCP be opt-in or opt-out?
  - Current: Opt-in (disabled by default)
  - Keep this approach?

### Healthcare Specific
- [ ] Should we add more healthcare sub-domains?
  - Clinical research
  - Pharmacy
  - Medical devices
  - Health IT vs Clinical analytics

- [ ] Partner with healthcare job boards?
  - Health eCareers API integration?
  - HIMSS JobMine access?

---

## 💡 Ideas / Future Vision

### Advanced Features (6+ months)
- [ ] **AI-powered interview prep**
  - Based on job posting + tailored resume
  - Generate likely interview questions
  - Practice answers with AI interviewer

- [ ] **Salary negotiation assistant**
  - Research market rates for role
  - Suggest negotiation strategies
  - Generate counter-offer language

- [ ] **Career path advisor**
  - Analyze job market trends
  - Suggest skills to learn
  - Recommend career transitions

- [ ] **Network optimization**
  - Identify key people at target companies
  - Suggest LinkedIn connections
  - Generate personalized outreach messages

### Platform Evolution
- [ ] **Resume marketplace**
  - Users share anonymized success patterns
  - Community-driven improvements
  - Best practices database

- [ ] **Employer version**
  - Reverse matching (jobs → candidates)
  - Candidate screening assistance
  - Interview question generation

---

## 📅 Sprint Planning

### Sprint 1 (Week 1-2): Foundation Solidification
- [ ] Add comprehensive unit tests
- [ ] Improve error handling
- [ ] Add input validation
- [ ] Document all agent prompts

### Sprint 2 (Week 3-4): Core Features
- [ ] Web scraping implementation
- [ ] Resume format conversion (PDF/DOCX)
- [ ] Resume pool management commands

### Sprint 3 (Week 5-6): MCP Integration
- [ ] Decide on LangGraph/CrewAI vs custom
- [ ] Google Jobs MCP integration
- [ ] Test OMOP/FHIR MCP servers

### Sprint 4 (Week 7-8): UX & Polish
- [ ] Interactive resume builder
- [ ] Multi-variant generation
- [ ] Rich CLI improvements
- [ ] Diff visualization

---

## 📝 Notes

### Research Needed
- Competitive analysis: What do Kickresume, Resume.io, Rezi.ai do?
- ATS systems: How do they actually parse resumes?
- Market research: What do job seekers struggle with most?

### Technical Considerations
- Token usage optimization (Claude API costs)
- Rate limiting and caching strategies
- Data privacy and security (resume data is sensitive)

### Community Feedback
- [ ] Get feedback from healthcare data analysts
- [ ] Test with real job postings
- [ ] Measure actual interview callback improvements

---

## ✅ Completed (from initial build)
- [x] Core project structure
- [x] Industry abstraction layer (plugin system)
- [x] Healthcare industry configuration (comprehensive)
- [x] Tech industry configuration (basic)
- [x] 4 AI agents (analyzer, matcher, tailoring, reviewer)
- [x] Data models (JobPosting, Resume, Industry)
- [x] Service layer (terminology, keywords, skills)
- [x] CLI interface
- [x] Example resume + job posting
- [x] Documentation (README, QUICKSTART, PROJECT_SUMMARY)
- [x] Basic tests (setup verification)

---

**Last Updated**: 2025-10-26
**Version**: 0.1.0 MVP

---

## How to Use This TODO

1. **Review regularly** - Weekly check-ins on progress
2. **Prioritize** - Focus on HIGH priority items first
3. **Update dates** - Add target completion dates
4. **Track effort** - Estimate time for planning
5. **Close items** - Move completed items to bottom
6. **Add notes** - Document decisions and learnings
