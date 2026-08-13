# 📧 Smart Email Processing System — README

---

## 📁 Project Structure

```
email-processing-system/
│
├── app.py                          # Flask web application (main entry point)
├── classifier.py                   # Message classification logic
├── data_processor.py               # Main processing pipeline
├── task_extractor.py               # Task & event extraction
├── sensitive_detector.py           # Sensitive info detection
├── generate_demo_report.py         # Demo report generator
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (if any)
├── .gitignore                      # Git ignore file
├── README.md                       # Complete documentation
├── MANDATORY_DEMO_REPORT.md        # Report for 15 mandatory IDs
├── FIXES_REPORT.md                 # Documentation of fixes made
│
├── templates/
│   └── index.html                  # Web dashboard HTML
│
├── static/
│   └── style.css                   # Dashboard styling
│
├── uploads/                        # Temporary CSV uploads
│   └── (uploaded files go here)
│
├── output/                         # Generated JSON output files
│   ├── classifications.json        # All 900 classifications
│   ├── tasks.json                  # 330 tasks + 130 events
│   ├── sensitive.json              # 30 sensitive items detected
│   └── statistics.json             # Processing statistics
```

---

## 📊 How Message Classification Works

Classification is handled by `MessageClassifier` in `classifier.py`, using a **rule-based regex pattern matching approach** with confidence scoring (an optional ML path via `TfidfVectorizer` + `LogisticRegression` exists but is only used if a pre-trained model is found in `models/`; otherwise the system falls back to rules).

### Categories
The system classifies every message into one of **6 categories**:

| Category | Description |
|----------|-------------|
| **Action Required** | Messages needing user action |
| **Meeting or Event** | Calendar-related messages |
| **Personal Information** | Messages with personal data |
| **Promotional** | Marketing and sales messages |
| **Sensitive Information** | Messages with sensitive data |
| **General Information** | Default category when nothing else matches |

### Processing Steps

1. **Preprocessing** — the message is lowercased.
2. **Pattern Matching** — each category has its own list of regex patterns; every pattern is checked against the message and matches are counted per category.
3. **Category Selection**
   - If any `sensitive` pattern matched, that category wins outright — **sensitive detection always takes priority** over every other category.
   - Otherwise, if no pattern matched at all, the category defaults to **General Information**.
   - Otherwise, the category with the highest match count is chosen.
4. **Confidence Calculation**
   ```
   confidence = matches_in_winning_category / total_matches_across_all_categories
   if matches_in_winning_category > 1:
       confidence += 0.1        # boost for multiple matches
   confidence = min(confidence, 0.95)   # capped at 95%
   # if there were no matches at all → confidence = 0.50
   ```
5. **Reason Generation** — a template explanation is chosen for the winning category (e.g. *"The message contains action words like 'please', 'submit', or 'complete'"*) and appended with `(found N matching patterns)`.

### Confidence Examples

| Pattern Matches | Confidence |
|------------------|------------|
| 0 (default) | 0.50 |
| 1 | 0.50 |
| 2 | 0.77 |
| 3+ | 0.85–0.95 |

### Example

**Input:**
```
From: manager@company.com
Message: Please submit your Q3 report by Friday. It's urgent!
```

**Output:**
```json
{
  "message_id": "MSG_001",
  "category": "Action Required",
  "confidence": 0.91,
  "reason": "The message contains action words like \"please\", \"submit\", or \"complete\" (found 3 matching patterns)"
}
```

---

## 📅 How Tasks and Events Are Extracted

Extraction is handled by `TaskExtractor` in `task_extractor.py`. **Every message** is checked (not just those classified as "Action Required" or "Meeting or Event") — the extractor runs its own independent keyword check.

### Detection Keywords

**Task keywords:** `submit`, `complete`, `finish`, `provide`, `update`, `review`, `approve`, `send`, `please`, `kindly`, `need`, `must`, `should`

**Event keywords:** `meeting`, `event`, `call`, `zoom`, `teams`, `webinar`, `appointment`, `schedule`, `calendar`

If a message matches **neither** list, no task or event is extracted for it (returns `null`). If it matches **both**, it is classified as an **event** (events take priority over tasks).

### Extraction Process

1. **Title**
   - Task titles: text following phrases like "please", "kindly", "submit", "complete", etc., up to a stop point (`by`, `before`, `.`, `?`, or end of string).
   - Event titles: text around event keywords ("meeting", "call", "webinar", etc.).
   - Fallback for either: the first 50 characters of the message.
   - Titles are capped at 100 characters.
2. **Deadline** — supports `YYYY-MM-DD`, `MM/DD/YYYY`, `MM-DD-YYYY`, and `by/on/before Month DD, YYYY`. Parsed and normalized to `YYYY-MM-DD` where possible. **If no date is present, stored as `null` — never guessed.**
3. **Time** — supports `HH:MM` and `HH:MM AM/PM` formats. **If missing, stored as `null`.**
4. **Person** — looks for a capitalized name immediately following "with", "from", or "by". **If missing, stored as `null`.**
5. **Priority**
   - **High:** urgent, important, asap, immediately, critical, high priority
   - **Medium (default):** please, need, should, required
   - **Low:** when possible, if you can, eventually, low priority

**Core principle:** the system **never invents information**. Deadline, time, and person are only populated when the pattern is explicitly present in the text — otherwise they are `null`.

### Example

**Input:**
```
Meeting with Sarah about project timeline on 2026-08-20 at 3:00 PM.
```

**Output:**
```json
{
  "item_id": "EVENT_MSG_042",
  "type": "event",
  "title": "project timeline",
  "description": "Meeting with Sarah about project timeline on 2026-08-20 at 3:00 PM.",
  "deadline": "2026-08-20",
  "time": "3:00 PM",
  "person": "Sarah",
  "priority": "high",
  "source_message_id": "MSG_042"
}
```

---

## 🔒 How Sensitive Information Is Detected and Masked

Detection is handled by `SensitiveDetector` in `sensitive_detector.py` using **regular expressions only** — no data is sent to any external service.

### Detection Categories

| Type | Example Trigger | Risk | Recommended Action |
|------|------------------|------|---------------------|
| Password / OTP / verification code | `password: [value]`, `otp: [digits]` | 🔴 High | Do Not Store |
| Bank details (card, account, expiry) | `card number: [16 digits]`, `account number: [8-12 digits]` | 🔴 High | Do Not Send External |
| Personal ID (SSN, phone, email) | `ssn: [xxx-xx-xxxx]`, `phone: [10-15 digits]`, `email: [user@domain]` | 🟡 Medium | Ask for Confirmation |
| API token / access / auth token | `api key: [16-40 chars]` | 🔴 High | Do Not Store |

### Process

1. **Pattern Matching** — the raw message is scanned case-insensitively against every pattern in every category.
2. **Value Extraction** — when a pattern matches, the actual sensitive value is captured (e.g. *"Your OTP is 847291"* → captures `847291`).
3. **Risk Assessment** — each category carries a fixed risk level (High or Medium).
4. **Masking** — the captured value is replaced with asterisks (`*` × length) everywhere it appears in the message, plus a secondary pass masks near-adjacent partial matches for values longer than 4 characters.

**Security guarantee:** only the **masked** message is stored in `sensitive.json` — the raw sensitive value itself is never written to disk in plain text (only a truncated `original_partial`, e.g. `"84***"`, is kept for internal reference).

> **Note:** the detector currently returns only the **first** sensitive item found per message. If a single message contains multiple distinct sensitive items (e.g. both a password and a phone number), only the first match is recorded in the output.

### Example

**Input:**
```
Your one-time password is 847291. Please use it within 5 minutes.
```

**Output:**
```json
{
  "message_id": "MSG_204",
  "sensitivity_type": "password",
  "risk": "high",
  "masked_text": "Your one-time password is ******. Please use it within 5 minutes.",
  "recommended_action": "do_not_store"
}
```

---

## ⚠️ Assumptions and Limitations

### Assumptions

**Data format**
- The CSV follows the expected columns: `message_id`, `sender`, `message`, `timestamp`.
- Messages are in English.
- Dates follow standard formats (`YYYY-MM-DD`, `MM/DD/YYYY`, etc.).

**Classification**
- Keyword/regex patterns are sufficient signal for categorization — no deep semantic understanding is attempted.
- Each message is assigned exactly one primary category, with sensitive content always taking priority.

**Extraction**
- Tasks are only recognized when they contain an expected action verb; events only when they contain an expected meeting/calendar keyword.

**Security**
- All processing happens locally; no message content is sent to any external API.

### Limitations

| Limitation | Description |
|------------|--------------|
| Rule-based only | No trained ML model is used by default — the classifier can miss context, sarcasm, or unusual phrasing that doesn't match a known pattern. |
| Language | English only. |
| Date parsing | Some complex or ambiguous date formats may not be recognized and will fall through to `null`. |
| Relative dates | Expressions like "tomorrow" or "next week" are not resolved — stored as `null`. |
| Person extraction | Limited to simple `with/from/by <Capitalized Name>` patterns; multi-part names, titles, or unusual capitalization may be missed. |
| Single sensitive finding | Only the first sensitive-data match per message is captured; additional distinct sensitive items in the same message are not reported. |
| Path portability | The default CSV input path is currently hardcoded to a local machine path rather than a portable/relative one, unless a file is explicitly uploaded through the `/api/process` endpoint. |

---

## 🤖 AI-Tool Usage Declaration

| Tool | Purpose | Data Sent? |
|------|---------|------------|
| GitHub Copilot | Code suggestions & autocompletion | ❌ No sensitive data |
| ChatGPT (GPT-4) | Architecture brainstorming & debugging | ❌ No sensitive data |
| Stack Overflow | Error resolution & best practices | ❌ No |

### Important Disclosures

**No external API processing**
- All message processing (classification, extraction, detection) happens locally using regex, `scikit-learn`, `dateutil`, and `pandas`.
- No message content is sent to any external AI or third-party service at runtime.
- Sensitive data never leaves the system.

**Code understanding**
- Every line of code was reviewed and is understood by the developer.
- AI-assisted suggestions were reviewed and modified before inclusion — no unreviewed black-box components.

**Compliance**
- ✅ No dataset uploaded to public repositories.
- ✅ Sensitive data masked in all output files.
- ✅ No raw/unmasked sensitive values written to disk.
