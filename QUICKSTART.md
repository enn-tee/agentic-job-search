# Quick Start Guide

Get up and running with the Agentic Resume Tailoring System in 5 minutes.

## Prerequisites

- Python 3.11 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Installation

### 1. Set up Python environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Anthropic API key
# ANTHROPIC_API_KEY=your_actual_api_key_here
```

## Usage

### Interactive Mode (Easiest!)

Simply run the CLI without any arguments for an interactive experience:

```bash
python main.py
```

You'll be prompted to:
1. Choose what you want to do (tailor, info, exit)
2. If tailoring:
   - Confirm use of `current_job.txt` (if it has content)
   - Enter company name
   - Enter job title
   - Confirm or change industry (defaults to healthcare)

**Example Interactive Session (First Time):**
```
🎯 Agentic Resume Tailoring System

What would you like to do? [tailor/info/exit] (tailor): tailor

📋 Let's tailor your resume!

Found job description in current_job.txt

Preview:
About the job
Job Title: Entry-Level Healthcare Data Analyst (Remote)
...

Use this job description? [Y/n]: y
Company name: Synergie Systems
Job title: Entry-Level Healthcare Data Analyst
Industry [healthcare]:
Use a specific base resume? [y/N]: n

============================================================
Starting resume tailoring...
============================================================
```

**Example Interactive Session (Repeat Run - Faster!):**
```
🎯 Agentic Resume Tailoring System

What would you like to do? [tailor/info/exit] (tailor): tailor

📋 Let's tailor your resume!

💾 Last job: Entry-Level Healthcare Data Analyst at Synergie Systems
Use these details again? [Y/n]: y
✅ Using cached job details

============================================================
Starting resume tailoring...
============================================================
```

**Note:** The system remembers your last job details, so re-running for the same position is instant!

### Command-Line Mode (Advanced)

You can also use direct commands for automation/scripting:

#### View Industry Information

```bash
python main.py info --industry healthcare
```

#### Tailor a Resume

##### Recommended Workflow: Using `current_job.txt`

The easiest way to tailor resumes is to use the `current_job.txt` file:

1. **Paste job description** into `current_job.txt` (this file is git-ignored)
2. **Run the tailor command:**

```bash
python main.py tailor \
  --job current_job.txt \
  --company "MedTech Solutions" \
  --title "Senior Healthcare Data Analyst"
```

**Note:**
- The `--industry` flag is optional and defaults to `healthcare` (from `.env`)
- You can use `--job` or `--job-text` (both work the same)
- The `current_job.txt` file won't be tracked by git, so you can reuse it for each new job

This will:
1. ✅ Analyze the job posting
2. ✅ Find the best matching base resume
3. ✅ Tailor the resume for the job
4. ✅ Review the tailored resume
5. ✅ Save the result to `resume_pool/tailored_resumes/`

#### Example: Using the sample job posting

```bash
python main.py tailor \
  --job examples/sample_job_posting.txt \
  --company "MedTech Solutions" \
  --title "Senior Healthcare Data Analyst"
```

#### Using a specific base resume

```bash
python main.py tailor \
  --job current_job.txt \
  --company "Company Name" \
  --title "Job Title" \
  --base-resume your_resume_id
```

#### Specifying a different industry

```bash
python main.py tailor \
  --job current_job.txt \
  --company "TechCorp" \
  --title "Software Engineer" \
  --industry tech
```

### Output

The system will generate:
- **Tailored Resume**: `resume_pool/tailored_resumes/YYYYMMDD_HHMMSS_company.json`
- **Metadata**: `resume_pool/metadata/YYYYMMDD_HHMMSS_company.json`

The output includes:
- Optimized professional summary
- Enhanced bullet points with metrics
- ATS-optimized keywords
- Aligned skills section
- Quality review score and feedback

## Creating Your Base Resume

### Option 1: Use a PDF (Easiest!)

Simply copy your existing resume PDF into `resume_pool/base_resumes/`:

```bash
cp ~/Documents/my_resume.pdf resume_pool/base_resumes/
```

The system will automatically:
- Extract text from the PDF
- Use Claude to parse it into structured format
- Load it into the resume pool

**Supported:** Any standard resume PDF with readable text.

### Option 2: Use the JSON template

Copy and modify `resume_pool/base_resumes/example_resume.json`:

```bash
cp resume_pool/base_resumes/example_resume.json resume_pool/base_resumes/my_resume.json
```

Then edit `my_resume.json` with your information.

### Option 3: Start from scratch

Create a new JSON file with this structure:

```json
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "phone": "(555) 123-4567",
  "professional_summary": "Your current professional summary...",
  "experience": [
    {
      "company": "Company Name",
      "title": "Job Title",
      "start_date": "2020-01",
      "end_date": null,
      "bullets": [
        "Achievement or responsibility 1",
        "Achievement or responsibility 2"
      ],
      "technologies": ["Tech1", "Tech2"]
    }
  ],
  "education": [
    {
      "institution": "University Name",
      "degree": "Degree Name",
      "field_of_study": "Major",
      "graduation_date": "2020-05"
    }
  ],
  "technical_skills": ["Skill 1", "Skill 2"],
  "certifications": ["Cert 1", "Cert 2"]
}
```

See `example_resume.json` for the complete schema.

## Tips for Best Results

### 1. Prepare Quality Base Resumes
- Include detailed bullet points with metrics
- List all relevant skills and technologies
- Keep multiple versions for different career paths

### 2. Provide Complete Job Descriptions
- Copy the entire job posting text
- Include requirements, responsibilities, and qualifications
- Don't abbreviate or summarize

### 3. Review and Refine
- The system provides suggestions - review them carefully
- Iterate based on quality review feedback
- Keep what works, refine what doesn't

## Interactive Skills Discovery

The system includes an **intelligent skills discovery process** that helps you identify transferable skills and experiences you might not realize are relevant.

### How It Works

After analyzing your resume against the job requirements, the system:

1. **Identifies Skill Gaps**
   - Compares job requirements to your resume
   - Finds missing required and preferred skills
   - Prioritizes the most important gaps

2. **Asks Targeted Questions**
   - Uses Claude to generate personalized questions
   - Explores adjacent and transferable experiences
   - Considers volunteer work, projects, hobbies, coursework

3. **Evaluates Your Responses**
   - Analyzes your answers for skill evidence
   - Identifies transferable experiences
   - Generates professional resume bullet points

4. **Multi-Round Exploration**
   - Up to 3 rounds of questions per skill
   - Follow-up questions based on your answers
   - Option to skip after each round

### Example Session

```
🔍 Analyzing skill gaps...
   Found 3 missing required skills
   Found 2 missing preferred skills

💡 Would you like to explore if you have transferable skills?
   This interactive process helps discover relevant experience you might have missed.
   Start skills discovery? [Y/n]: y

============================================================
🎯 Exploring skill 1/5: SQL Database Management
============================================================

📋 Why this matters: Database skills are critical for analyzing healthcare data
    and generating insights from electronic health records.

💭 Think about:
   • Academic projects or coursework
   • Volunteer work or community involvement
   • Personal projects or hobbies

❓ Question 1:
   Have you ever worked with spreadsheets to organize or analyze large amounts
   of data? This could be Excel, Google Sheets, or similar tools.

   Your answer (or 'skip' to move on): Yes, I managed a volunteer database
   for a local food bank using Google Sheets. I tracked donations, inventory,
   and distribution across 3 locations with about 5000 rows of data.

   ✅ Great! Found relevant experience!
   💡 Your experience with structured data management in Google Sheets demonstrates
   foundational database concepts like data organization, queries, and reporting.

   📝 Suggested resume bullets:
      1. Managed multi-location inventory database tracking 5,000+ donation records
         using structured data management principles
      2. Developed data tracking system for food bank operations, creating reports
         and queries to optimize distribution across 3 sites

   Add these bullets to your resume? [Y/n]: y

============================================================
📊 Discovery Summary
============================================================
✅ Discovered skills: SQL Database Management, Data Analysis
✅ New bullet points: 3

   ✅ Resume enhanced with discovered skills
```

### Configuration

You can customize the discovery process by modifying these settings in `run_skills_discovery()`:

```python
max_skills_to_explore = 5    # Number of missing skills to explore
max_rounds_per_skill = 3     # Question rounds before offering skip
```

### When Skills Discovery Runs

Skills discovery is **optional** and runs:
- After resume matching
- Before tailoring
- Only if skill gaps are detected
- Only if you choose to participate

You can skip the entire process or skip individual skills at any time.

### Tips for Best Results

**Be Specific:**
- Describe actual projects or situations
- Include numbers and outcomes when possible
- Mention tools, processes, or methodologies

**Think Broadly:**
- Consider non-work experiences
- Think about related or adjacent skills
- Don't dismiss "small" projects

**Examples to Consider:**
- **Academic:** Group projects, research, coursework
- **Volunteer:** Non-profit work, community projects
- **Personal:** Side projects, hobbies, online courses
- **Work:** Training, informal tasks, learning experiences

## Caching & Performance

The system includes **multi-layer intelligent caching** for blazing-fast repeat runs and significant API cost savings.

### What Gets Cached?

1. **Job Details Cache** (`.last_job_cache.json`)
   - Remembers your last job's company name and title
   - Instant re-runs for the same position
   - Just press Enter to reuse!

2. **Job Analysis Cache** (`.cache/job_analysis_*.json`)
   - Cached per job description (content-based hashing)
   - Repeat runs with same job = instant analysis
   - No re-analyzing the same posting

3. **Parsed PDF Resumes** (`.cache/resumes/`)
   - PDFs parsed once with Claude, then cached
   - File change detection (SHA256 hash)
   - Automatic re-parse when PDF modified
   - Massive speed improvement for loading resume pool

4. **Tailored Resumes** (`.cache/tailored_resume_*.json`)
   - Cached per job + base resume combination
   - Includes diff tracking
   - Iterate on different base resumes instantly

5. **Quality Reviews** (`.cache/quality_review_*.json`)
   - Cached per tailored resume
   - Instant feedback on repeat runs

### Cache Management

**View what's cached:**
```bash
python main.py cache --list
```

Output:
```
📦 Cached Artifacts:
   Job Analyses:      1
   Resume Matches:    0
   Tailored Resumes:  1
   Quality Reviews:   1
   Total: 3 artifacts

📄 Parsed PDF Resumes: 1
   • my_resume
     Cached: 2025-10-26T10:30:00
     Source: my_resume.pdf
```

**Clear all caches:**
```bash
python main.py cache --clear
```

**Clear specific cache:**
```bash
# Clear job analyses only
python main.py cache --clear --stage job_analysis

# Clear parsed PDF resumes only
python main.py cache --clear --stage resumes

# Clear tailored resumes only
python main.py cache --clear --stage tailored_resume

# Clear quality reviews only
python main.py cache --clear --stage quality_review
```

### Performance Impact

**First run (no cache):**
- Job analysis: ~15 seconds
- PDF parsing: ~20 seconds
- Resume tailoring: ~25 seconds
- Quality review: ~10 seconds
- **Total: ~70 seconds**

**Second run (with cache):**
- Job analysis: instant (cached)
- PDF parsing: instant (cached)
- Resume tailoring: instant (cached)
- Quality review: instant (cached)
- **Total: ~3 seconds**

**Result: 20x faster + saves API costs!**

### When Cache is Used

The system shows clear indicators:
- `💾 Using cached...` = Using cached data
- `🔍 Running... (will be cached)` = Generating and caching
- `📄 Using cached parse (file unchanged)` = PDF cache hit
- `🔍 Parsing PDF (will be cached)...` = Parsing PDF for first time

### Cache Invalidation

**Automatic invalidation:**
- PDF resumes: Detects file changes via hash
- Job analysis: Different job description = different cache
- Tailored resumes: Different job or base resume = new cache

**Manual invalidation:**
- Use `python main.py cache --clear` to force regeneration
- Delete `.cache/` directory to wipe everything
- Edit cached JSON files directly for quick tweaks

## Industry Support

Currently supported industries:

- **Healthcare** (`--industry healthcare`)
  - Clinical data analysis
  - Health informatics
  - Healthcare analytics

- **Technology** (`--industry tech`)
  - Software engineering
  - Data engineering
  - Full-stack development

### Adding a New Industry

1. Create `config/industries/your_industry.yaml`
2. Use `healthcare.yaml` or `tech.yaml` as a template
3. Define industry-specific:
   - Terminology and acronyms
   - Skills and categories
   - Keywords and action verbs
   - Certifications

## Troubleshooting

### "ANTHROPIC_API_KEY must be set"
- Make sure you created `.env` file
- Add your API key: `ANTHROPIC_API_KEY=sk-ant-...`

### "No base resumes found in pool"
- Add at least one resume JSON file to `resume_pool/base_resumes/`
- Don't use filenames starting with `example_`

### "Could not parse job analysis response"
- Check that your job description is complete
- Ensure the text file is readable
- Try with the sample job posting first

## What's Next?

- **Experiment** with different job postings
- **Refine** your base resumes based on feedback
- **Build** a library of tailored resumes
- **Track** what works for different roles

## Getting Help

- Check the main [README.md](README.md) for architecture details
- Review example files in `examples/`
- Open an issue for bugs or feature requests

Happy job hunting! 🎯
