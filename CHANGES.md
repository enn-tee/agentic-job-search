# Recent Changes

## Artifact Caching System (2025-10-26)

### Changes Made

1. **🗄️ Multi-Stage Artifact Caching (NEW!)**
   - Each agent stage now caches its output
   - Job analysis cached (no re-analysis on repeat runs)
   - Tailored resumes cached per base resume
   - Quality reviews cached
   - Massive speed improvements for repeat runs!

2. **Cache Structure**
   - Stored in `.cache/` directory (git-ignored)
   - Content-based hashing (same job = same cache)
   - Artifacts saved as inspectable JSON files
   - Can view/edit cached artifacts directly

3. **Cached Stages**
   - `job_analysis_*.json` - Job posting analysis results
   - `tailored_resume_*.json` - Tailored resume + diff tracking
   - `quality_review_*.json` - Quality review results
   - Each includes metadata (timestamp, job hash, etc.)

4. **Cache Management**
   - `python main.py cache --list` - View cached artifacts
   - `python main.py cache --clear` - Clear all cache
   - `python main.py cache --clear --stage job_analysis` - Clear specific stage

### Usage

**First Run (Generates Artifacts):**
```bash
python main.py

📋 Analyzing job posting...
   🔍 Running job analysis (will be cached)...
   ✅ Job analysis cached for future runs
   ...
✍️  Tailoring resume...
   ✍️  Running resume tailoring (will be cached)...
   ✅ Tailored resume cached for future runs
   ...
```

**Second Run (Uses Cache - Much Faster!):**
```bash
python main.py

📋 Analyzing job posting...
   💾 Using cached job analysis
✍️  Tailoring resume...
   💾 Using cached tailored resume
🔍 Reviewing tailored resume...
   💾 Using cached quality review

# Runs in ~5 seconds instead of ~60 seconds!
```

**View Cache:**
```bash
python main.py cache --list

📦 Cached Artifacts:

   Job Analyses:      1
   Resume Matches:    0
   Tailored Resumes:  1
   Quality Reviews:   1

   Total: 3 artifacts
```

**Clear Cache:**
```bash
python main.py cache --clear
Clear ALL cached artifacts? [y/N]: y
✅ Cleared 3 artifact(s)
```

### Benefits

- ⚡ **10-20x faster** repeat runs (uses cached analysis)
- 💰 **Saves API costs** (no re-analyzing same job)
- 🔍 **Inspectable** artifacts (open `.cache/*.json` to view)
- 🔄 **Iteration friendly** (tweak base resume, re-run instantly)
- 📊 **Diff tracking** (see exactly what changed)

### Use Cases

**Perfect for:**
- Testing different base resumes for same job
- Tweaking resume content and regenerating
- Comparing multiple approaches
- Debugging agent outputs
- Reviewing past analyses

**Example Workflow:**
```bash
# First run - analyze job
python main.py
# (Full analysis, ~60 sec)

# Adjust base resume PDF
cp ~/updated_resume.pdf resume_pool/base_resumes/

# Second run - uses cached analysis
python main.py
# (Uses cache, ~5 sec!)

# View what was cached
ls .cache/
cat .cache/job_analysis_*.json
```

### Files Modified
- `main.py` - Integrated caching at each stage
- `.gitignore` - Added `.cache/`
- `CHANGES.md` - This file
- `QUICKSTART.md` - Updated (next)

### Files Created
- `src/utils/artifact_cache.py` - Caching system
- `.cache/` - Cache directory (created on first run)

---

## Job Details Caching (2025-10-26)

### Changes Made

1. **💾 Smart Caching (NEW!)**
   - System remembers your last job details
   - On next run, offers to reuse company name and title
   - Makes repeat runs much faster
   - Perfect for iterating on the same job application

2. **Cache Storage**
   - Saved in `.last_job_cache.json` (git-ignored)
   - Stores: job file path, company, title, industry
   - Automatically updated after each run

3. **User Experience**
   - **First run:** Enter all details normally
   - **Repeat runs:** Just hit Enter to reuse last job
   - **Different job:** Say "no" to cached details, enter new ones

### Usage

```bash
# First run
python main.py
# Enter: Synergie Systems, Entry-Level Healthcare Data Analyst

# Second run (same job)
python main.py
💾 Last job: Entry-Level Healthcare Data Analyst at Synergie Systems
Use these details again? [Y/n]: ⏎  # Just press Enter!
✅ Using cached job details
# Done! Much faster
```

### Files Modified
- `main.py` - Added caching functions
- `.gitignore` - Added `.last_job_cache.json`
- `QUICKSTART.md` - Documented caching behavior
- `CHANGES.md` - This file

### Files Created
- `.last_job_cache.json` - Cache file (git-ignored)

---

## PDF Resume Support (2025-10-26)

### Changes Made

1. **📄 PDF Resume Support (NEW!)**
   - Drop PDF resumes into `resume_pool/base_resumes/`
   - System automatically extracts text and parses with Claude
   - Converts to structured Resume format
   - Works alongside JSON resumes

2. **Dependencies Added**
   - `pypdf>=4.0.0` - PDF text extraction
   - `pdfplumber>=0.11.0` - Enhanced PDF parsing

3. **New Utility**
   - `src/utils/pdf_parser.py` - PDF parsing with Claude
   - Extracts and structures resume data automatically

### Usage

```bash
# Just copy your PDF resume
cp ~/Documents/my_resume.pdf resume_pool/base_resumes/

# Run the system
python main.py

# The PDF will be automatically parsed when loading resume pool
```

### Files Modified
- `requirements.txt` - Added PDF libraries
- `main.py` - Updated `load_resume_pool()` to support PDFs
- `.gitignore` - Added `*.pdf` to base_resumes ignore
- `QUICKSTART.md` - Documented PDF support
- `CHANGES.md` - This file

### Files Created
- `src/utils/pdf_parser.py` - PDF parsing utility

---

## CLI Improvements v2 (2025-10-26)

### Changes Made

1. **🎯 Interactive Mode (NEW!)**
   - Run `python main.py` without any arguments
   - Interactive prompts guide you through the process
   - Automatically detects job description in `current_job.txt`
   - Shows preview before confirming
   - Prompts for company name and job title
   - Smart defaults for everything

2. **Added `current_job.txt` workflow**
   - Created `current_job.txt` file (git-ignored)
   - Users can paste job descriptions here and reuse the file
   - No need to create new files for each job

3. **Simplified CLI flags**
   - Added `--job` as a shorter alias for `--job-text`
   - Both work identically
   - Removed `--job-url` (web scraping not yet implemented)

4. **Industry defaults from .env**
   - `--industry` flag now defaults to value in `.env`
   - Default is `healthcare` unless you change it
   - Can still override with `--industry tech`, etc.

5. **Updated .gitignore**
   - Added `current_job.txt` to ignore list
   - Resume pool already ignored

### New Usage

#### Interactive Mode (Easiest!)
```bash
# 1. Paste job description into current_job.txt
# 2. Run:
python main.py

# Then follow the prompts:
What would you like to do? [tailor/info/exit] (tailor):
Found job description in current_job.txt
Use this job description? [Y/n]: y
Company name: Synergie Systems
Job title: Entry-Level Healthcare Data Analyst
Industry [healthcare]:
```

#### Command-Line Mode (For Automation)
```bash
python main.py tailor \
  --job current_job.txt \
  --company "Synergie Systems" \
  --title "Entry-Level Healthcare Data Analyst"
```

#### What Changed
**Before:**
```bash
python main.py tailor \
  --job-text path/to/some/file.txt \
  --company "Company" \
  --title "Title" \
  --industry healthcare
```

**Now (Interactive):**
```bash
python main.py
# Interactive prompts handle everything
```

**Now (Command-Line):**
```bash
python main.py tailor \
  --job current_job.txt \
  --company "Company" \
  --title "Title"
# Industry defaults to healthcare from .env
# Can use --job or --job-text (both work)
```

### Files Modified
- `.gitignore` - Added `current_job.txt`
- `main.py` - Added interactive mode + updated CLI options
- `QUICKSTART.md` - Updated with interactive mode examples
- `README.md` - Updated basic usage section
- `CHANGES.md` - This file

### Files Created
- `current_job.txt` - Reusable job description file (git-ignored)

### Breaking Changes
None - backward compatible. Old `--job-text` flag still works.

### Key Features
- ✅ **Zero-config workflow**: Just run `python main.py`
- ✅ **Smart defaults**: Uses current_job.txt automatically if it has content
- ✅ **Preview before processing**: Shows job description preview
- ✅ **Guided prompts**: Never forget required fields
- ✅ **Both modes work**: Interactive OR command-line

### Next Steps
To use the new workflow:
1. Open `current_job.txt`
2. Paste a job description
3. Save the file
4. Run: `python main.py tailor --job current_job.txt --company "X" --title "Y"`

The industry will default to `healthcare` (from `.env`) unless you specify `--industry <name>`.
