# Helios — AI Career Ecosystem

> *Find jobs perfectly matched to your resume. Apply with a tailored resume in seconds.*

---

## What is Helios?

Helios is an AI-powered career platform that automates the most painful parts of job searching. Upload your resume, set your preferences, and Helios finds the best matching jobs, tailors your resume for each one, and shows you everything you need to decide whether to apply — company ratings, salary ranges, legitimacy scores, and more.

**Phase 1 turns a 2.5 hour job application process into 30 seconds.**

---

## The Problem

The average job seeker spends **2.5 hours per application**:

| Task | Time |
|---|---|
| Search for relevant jobs | 30 mins |
| Research the company | 20 mins |
| Tailor resume | 45 mins |
| Write cover letter | 30 mins |
| Check salary range | 15 mins |
| Verify legitimacy | 10 mins |
| Actually apply | 10 mins |

Most people send 100–200 applications to get one offer. That's **250–500 hours** of their life.

Helios does all of it in seconds.

---

## Phase 1 Features

### Resume Intelligence
- Upload your PDF resume
- AI parses it into structured data — experiences, skills, projects, education
- Resume stored as your master profile

### Smart Job Matching
- Set your preferences — role, job type, remote/onsite, location, industry
- Helios searches Adzuna, Remotive, and other job boards in real time
- AI scores every listing against your specific resume
- Get a ranked list of the jobs you're most qualified for

### Resume Tailoring
- For every job match, Helios generates a unique tailored resume
- Rewrites bullet points to mirror the job description language
- Surfaces hidden relevant experience
- Weaves in ATS keywords naturally
- Shows you WHY each change was made via tailoring notes
- ATS score so you know how likely you are to pass automated screening

### Company Intelligence (per job card)
- Company legitimacy score — is this job real?
- Glassdoor rating and review summary
- Salary range via Levels.fyi
- Company size and funding via Crunchbase
- Direct apply link

### Authentication
- Secure JWT based authentication
- Register, login, delete account
- All data tied to your account

---

## Tech Stack

### Backend
| Tool | Purpose |
|---|---|
| FastAPI | API framework |
| PostgreSQL | Primary database |
| SQLAlchemy | ORM |
| Asyncpg | Async Postgres driver |
| Alembic | Database migrations |
| JWT + OAuth2 | Authentication |
| PyMuPDF | PDF text extraction |
| OpenRouter API | AI inference (free models) |

### AI Models
| Model | Task |
|---|---|
| google/gemma-4-31b | Resume parsing |
| openai/gpt-oss-120b | Job analysis + tailoring |

### Integrations
| Service | Purpose |
|---|---|
| Adzuna API | Job discovery |
| Remotive API | Remote job discovery |
| Crunchbase API | Company data |
| Levels.fyi | Salary data |

### Frontend
| Tool | Purpose |
|---|---|
| Next.js | React framework |
| Shadcn/ui | Component library |
| Tailwind CSS | Styling |
| Vercel | Deployment |

---

## API Endpoints

### Auth
```
POST   /auth/register     → Create account
POST   /auth/login        → Login, get JWT token
DELETE /auth/delete       → Delete account
```

### Resume
```
POST   /resume/upload     → Upload PDF resume
POST   /resume/tailor     → Tailor resume to a job description
GET    /resume/tailored/{id} → Get a specific tailored resume
```

### Preferences
```
POST   /preferences/set   → Set job search preferences
GET    /preferences        → Get current preferences
```

### Jobs
```
GET    /jobs/match         → Find jobs matching your resume + preferences
GET    /jobs/{id}          → Get specific job details
GET    /jobs/{id}/legitimacy → See legitimacy report for a job
```

---

## Project Structure

```
helios/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py
│   │       ├── resume.py
│   │       ├── preferences.py
│   │       └── jobs.py
│   ├── models/
│   │   ├── user.py
│   │   ├── resume.py
│   │   ├── preferences.py
│   │   └── jobs.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── resume.py
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── resume_parser.py
│   │   ├── job_service.py
│   │   └── verification_service.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL
- OpenRouter API key (free at openrouter.ai)
- Adzuna API key (free at adzuna.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/helios.git
cd helios

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Fill in your keys in .env

# Create database
psql postgres -c "CREATE DATABASE helios;"

# Run the server
uvicorn app.main:app --reload
```

### Environment Variables

```
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost/helios
OPENROUTER_API_KEY=your_openrouter_key
BASE_URL=https://openrouter.ai/api/v1
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
```

---

## Roadmap

### Phase 1 — Job Finder (Current)
- [x] Resume upload and parsing
- [x] Resume tailoring with AI
- [x] JWT Authentication
- [ ] User preferences
- [ ] Job discovery via Adzuna
- [ ] AI match scoring
- [ ] Company intelligence
- [ ] Frontend (Next.js)
- [ ] Deploy

### Phase 2 — Auto Apply
- [ ] Email applications
- [ ] Playwright form filling (Greenhouse, Lever, Ashby)
- [ ] Application tracking dashboard

### Phase 3 — Full Automation
- [ ] Gmail inbox monitoring
- [ ] Auto follow-up emails
- [ ] Google Calendar interview scheduling
- [ ] Final round assignment breakdown

---

## The Vision

Phase 1 is a job finder. Phase 3 is a career agent that works while you sleep — finding jobs, applying with tailored resumes, following up on your behalf, scheduling interviews, and helping you ace final rounds.

The goal is to make job searching as passive as possible so candidates can focus on what actually matters — preparing for interviews and doing great work.

---

## License

MIT License — see LICENSE file for details.

---

Built by Siddharth S
