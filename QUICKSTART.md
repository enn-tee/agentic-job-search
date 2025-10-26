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

### View Industry Information

See what the system knows about an industry:

```bash
python main.py info --industry healthcare
```

### Tailor a Resume

#### Example: Using the sample job posting

```bash
python main.py tailor \
  --job-text examples/sample_job_posting.txt \
  --company "MedTech Solutions" \
  --title "Senior Healthcare Data Analyst" \
  --industry healthcare
```

This will:
1. ✅ Analyze the job posting
2. ✅ Find the best matching base resume
3. ✅ Tailor the resume for the job
4. ✅ Review the tailored resume
5. ✅ Save the result to `resume_pool/tailored_resumes/`

#### Using your own resume

1. Create a JSON file in `resume_pool/base_resumes/` following the format in `example_resume.json`
2. Run the tailor command as shown above

#### Using a specific base resume

```bash
python main.py tailor \
  --job-text path/to/job.txt \
  --company "Company Name" \
  --title "Job Title" \
  --base-resume your_resume_id \
  --industry healthcare
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

### Option 1: Use the template

Copy and modify `resume_pool/base_resumes/example_resume.json`:

```bash
cp resume_pool/base_resumes/example_resume.json resume_pool/base_resumes/my_resume.json
```

Then edit `my_resume.json` with your information.

### Option 2: Start from scratch

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
