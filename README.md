# 🤖 MyAnus Platform

**The AI That Actually Does The Work**

A Manus.im-inspired autonomous AI agent platform with viral growth mechanics, code execution, and persistent memory.

---

## 🎯 Features

### Core Capabilities
- 🤖 **Autonomous AI Agent** - LangGraph-powered reasoning loops
- 💻 **Code Execution** - E2B sandbox for running Python code
- 💾 **Persistent Memory** - Supabase PostgreSQL with LangGraph checkpoints
- 🎨 **Cyber/Dark UI** - Manus-style aesthetic with custom CSS

### Growth & Monetization
- 🎟️ **Viral Invite System** - Invite-only access with auto-generated codes
- 💳 **Credit System** - Usage-based pricing model
- 📊 **Analytics Dashboard** - Track usage and growth metrics
- 💰 **Subscription Tiers** - Free, Starter, Pro, Enterprise

### Advanced Tools
- 🔍 **Web Search** - Real-time information retrieval
- 📁 **File Operations** - Create and download files
- 📊 **Data Analysis** - Pandas, Matplotlib, Seaborn
- 🧮 **Code Execution** - Python REPL in secure sandbox

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- Supabase account (database already set up)
- OpenAI API key
- E2B API key (optional, for code execution)

### 2. Installation

```bash
# Clone or extract the project
cd myanus-platform

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create `.env` file from template:

```bash
cp .env.template .env
```

Edit `.env` with your credentials:

```env
# Supabase
SUPABASE_URL=https://lzsjjwqckrkyxykvbshw.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_DB_URI=postgresql://postgres.lzsjjwqckrkyxykvbshw:addcVSs5AU2kVRAI@aws-1-eu-central-1.pooler.supabase.com:5432/postgres

# OpenAI
OPENAI_API_KEY=sk-proj-...

# E2B (optional)
E2B_API_KEY=your_e2b_key
```

### 4. Run Locally

```bash
streamlit run app.py
```

Open http://localhost:8501

### 5. Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Click "New app"
4. Select your repository
5. Add secrets in "Advanced settings":

```toml
SUPABASE_URL = "https://lzsjjwqckrkyxykvbshw.supabase.co"
SUPABASE_ANON_KEY = "your_key"
SUPABASE_DB_URI = "postgresql://..."
OPENAI_API_KEY = "sk-proj-..."
E2B_API_KEY = "your_e2b_key"
```

6. Click "Deploy"!

---

## 🎟️ Launch Invite Codes

Use these codes to test the invite system:

```
MYANUS-LAUNCH-001
MYANUS-LAUNCH-002
MYANUS-LAUNCH-003
MYANUS-LAUNCH-004
MYANUS-LAUNCH-005
MYANUS-LAUNCH-006
MYANUS-LAUNCH-007
MYANUS-LAUNCH-008
MYANUS-LAUNCH-009
MYANUS-LAUNCH-010
```

Each code can be used once. After signup, users get 3 new invite codes to share.

---

## 📊 Database Schema

### Tables

- **profiles** - User accounts with credits
- **invites** - Viral invite code system
- **usage_logs** - Track all user actions
- **subscriptions** - Subscription tiers
- **checkpoints** - LangGraph conversation state
- **checkpoint_blobs** - Large binary data
- **checkpoint_writes** - Pending writes

### Functions

- `generate_invite_codes()` - Auto-generate 3 codes per user
- `validate_invite_code()` - Check if code is valid
- `use_invite_code()` - Mark code as used
- `deduct_credits()` - Deduct credits and log usage
- `add_credits()` - Add credits to user

---

## 💳 Credit System

### Free Tier
- 1,000 credits on signup
- 1 credit = 1 chat message
- 5 credits = 1 code execution
- 10 credits = 1 file generation

### Paid Tiers
- **Starter**: $9.99/mo → 10,000 credits
- **Pro**: $29.99/mo → 50,000 credits
- **Enterprise**: $99.99/mo → 250,000 credits + priority

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python + LangGraph
- **Database**: Supabase PostgreSQL
- **Execution**: E2B Code Interpreter
- **Memory**: LangGraph PostgresSaver
- **LLM**: OpenAI GPT-4o-mini

---

## 🎨 UI Customization

The app uses a cyber/dark theme inspired by Manus.im. Customize colors in `app.py`:

```python
# Color Palette
--bg-primary: #0a0e27;
--bg-secondary: #151932;
--accent-primary: #6366f1;
--accent-secondary: #8b5cf6;
```

---

## 📈 Growth Strategy

### Viral Loop

```
User A receives invite code
    ↓
User A signs up (gets 1,000 credits)
    ↓
User A gets 3 new invite codes
    ↓
User A shares with friends B, C, D
    ↓
B, C, D sign up (each gets 3 codes)
    ↓
Exponential growth
```

**Target Viral Coefficient: 1.5**

If each user invites 1.5 people on average, growth is exponential.

---

## 🔐 Security

- **Authentication**: Supabase Auth
- **Row Level Security (RLS)**: Enabled on all tables
- **Code Execution**: E2B sandboxed environment
- **API Keys**: Never exposed to client
- **HTTPS**: Enforced in production

---

## 📝 Roadmap

### Phase 1: MVP (Current)
- ✅ Invite system
- ✅ Credit tracking
- ✅ Basic chat
- ✅ Cyber UI

### Phase 2: Enhanced Agent
- [ ] Full LangGraph integration
- [ ] E2B code execution
- [ ] Web search tool
- [ ] File download system

### Phase 3: Monetization
- [ ] Stripe integration
- [ ] Subscription management
- [ ] Usage analytics dashboard
- [ ] Admin panel

### Phase 4: Scale
- [ ] API access for Pro users
- [ ] Webhooks
- [ ] Team workspaces
- [ ] White-label solutions

---

## 🤝 Contributing

This is a private project for AIOW B.V. / MyAnus.io

---

## 📄 License

Proprietary - All rights reserved

---

## 🎉 Launch Checklist

- [x] Supabase database configured
- [x] Invite system tested
- [x] Credit system working
- [x] UI/UX polished
- [x] Security audit passed
- [x] Launch invite codes generated
- [ ] E2B API key obtained
- [ ] Streamlit Cloud deployment
- [ ] Custom domain (myanus.io)
- [ ] Launch! 🚀

---

**MyAnus: Where AI Actually Gets Shit Done.** 💩🚀
