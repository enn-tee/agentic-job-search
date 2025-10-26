# Recent Changes

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
