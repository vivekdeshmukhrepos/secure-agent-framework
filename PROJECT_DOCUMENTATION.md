# 🛡️ Secure AI Defense Lab - Project Documentation

## Overview

**Secure AI Defense Lab** is an interactive web application built with Streamlit that demonstrates security vulnerabilities in AI systems and how to defend against them. It provides hands-on attack simulation scenarios and shows real-time mitigation strategies for various AI security threats.

### Purpose
This project educates developers and security professionals about:
- Common AI system attack vectors
- Security filter implementation techniques
- Multi-layer protection pipelines
- Safe AI agent design patterns

---



## File-by-File Documentation

### 📄 **Root Level Files**

#### `app.py` (Main Application )
**Purpose:** Streamlit web UI for the entire application  
**Key Components:**
- 6 interactive tabs for different attack scenarios
- Session state management for attack logs
- Real-time user input capture
- File upload handling for document summarizer
- Attack report generation

**Flow:**
1. User selects an attack category from tabs
2. Enters malicious input or uploads a file
3. App calls `agent.process()` or `agent.plan_and_execute()`
4. Returns sanitized/filtered output
5. Logs are stored in session state and displayed in the Report tab

#### `requirements.txt`
**Purpose:** Python package dependencies  
**Contents:**
- `streamlit` - Web UI framework
- `openai` - OpenAI API client for LLM calls

#### `Readme.md`
**Purpose:** Quick overview and feature summary  
**Contents:** Project description, feature list, and basic structure

#### `TestCases.txt`
**Purpose:** Comprehensive testing scenarios (90+ test cases)  
**Categories:**
1. Prompt Injection Tests (4 scenarios)
2. Data Leakage Tests (5 scenarios)
3. Model Inversion Tests (3 scenarios)
4. Harmful/Biased Output Tests (3 scenarios)
5. Secure Summarizer Tests (5 scenarios)
6. Report Module Tests (3 scenarios)
7. UI/UX Tests (4 scenarios)
8. Performance Tests (3 scenarios)
9. Security Tests (3 scenarios)
10. Negative/Edge Case Tests (4 scenarios)

#### `malicious_input.txt`
**Purpose:** Pre-written attack examples for testing

#### `sample_report.txt`
**Purpose:** Example of application output/report format

---

### 🤖 **agent/ Directory** - Core Security Logic

#### `agent/__init__.py`
**Purpose:** Package initialization and public API exports  
**Exports:**
- `agent` - Global SecureAgent instance
- `SecureAgent` - The main class

**Usage:** Other modules import via `from agent import agent`

#### `agent/secure_agent.py` (~120 lines)
**Purpose:** Main security agent class with all defense mechanisms  

**Class: SecureAgent**
- **Constructor:** Initializes `last_log` for tracking operations

**Security Filter Methods:**

1. **`sanitize_prompt_injection(text: str) -> str`**
   - Detects phrases: "ignore previous", "override", "ignore instructions"
   - Returns: `[BLOCKED: Prompt Injection Attempt Detected]` if match found
   - Case-insensitive comparison

2. **`sanitize_data_leakage(text: str) -> str`**
   - Uses regex patterns to detect:
     - Emails: `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}`
     - Phone numbers (10-digit): `\b(?:\+91[-\s]?)?[0-9]{10}\b`
   - Masks with: `[EMAIL_MASKED]`, `[PHONE_MASKED]`
   - Returns: `[BLOCKED]: {sanitized_text}` if any masking occurred

3. **`sanitize_model_inversion(text: str) -> str`**
   - Detects queries for: "salary", "internal policy"
   - Returns: `[BLOCKED: Model Inversion Attempt]` if match found

4. **`sanitize_harmful_output(text: str) -> str`**
   - Filters banned terms: "violence", "hate", "kill"
   - Returns: `[FILTERED: Harmful Content Blocked]` if match found

**Pipeline Methods:**

5. **`apply_security(category: str, text: str) -> (str, list)`**
   - Routes text through appropriate security filter based on category
   - Returns sanitized text + step-by-step log
   - Categories: "Prompt Injection", "Data Leakage", "Model Inversion", "Harmful / Biased Output", "Secure Summarizer"
   - "Secure Summarizer" applies multi-layer protection (Data Leakage + Prompt Injection)

6. **`process(category: str, user_text: str) -> str`**
   - Direct processing pipeline for attack tabs
   - If blocked, returns block message immediately
   - Otherwise, sends sanitized text to LLM for processing
   - Stores complete flow in `self.last_log`

7. **`plan_and_execute(category: str, prompt: str) -> str`**
   - Advanced pipeline for the Secure Summarizer
   - Sanitizes input, then calls LLM with planning message
   - Used for document summarization
   - Returns formatted summary

---

### ⚙️ **config/ Directory** - Configuration Management

#### `config/__init__.py`
**Purpose:** Configuration loader with fallback mechanism  
**Exports:** `settings` - Global configuration dict  
**Feature:** Tries to load from `config.py`, falls back to inline defaults if missing

#### `config/config.py`
**Purpose:** Global application settings  
**Contains:**
```python
CONFIG = {
    "OPENAI_API_KEY": "sk-proj-...",  # OpenAI API key
    "OPENAI_MODEL": "gpt-4o-mini",     # LLM model to use
    "TEMPERATURE": 0.3                 # LLM creativity level (0-1)
}
```

**Notes:**
- API key should be updated with real credentials
- Lower temperature (0.3) = more deterministic, safer responses

---

### 🧠 **llm/ Directory** - LLM Integration

#### `llm/__init__.py`
**Purpose:** Package exports  
**Exports:**
- `call_llm` - Main function to query OpenAI

#### `llm/agent_llm.py` (~80 lines)
**Purpose:** OpenAI API wrapper with fallback support  

**Functions:**

1. **`_call_with_new_client(system_prompt, user_prompt) -> str`**
   - Uses modern OpenAI client (`openai>=1.0.0`)
   - Creates chat completion with system + user prompts
   - Extracts response content from `response.choices[0].message.content`
   - Error handling returns `[LLM ERROR] {error_message}`

2. **`_call_with_legacy(system_prompt, user_prompt) -> str`**
   - Fallback for older OpenAI library versions
   - Uses legacy `openai.ChatCompletion.create()` API
   - Similar flow but handles different response format

3. **`call_llm(system_prompt: str, user_prompt: str) -> str`**
   - Public entry point for LLM calls
   - Automatically chooses modern or legacy implementation
   - Called by `SecureAgent` after sanitization
   - Example usage:
     ```python
     result = call_llm(
         system_prompt="You are a secure AI agent...",
         user_prompt=sanitized_text
     )
     ```

**Configuration Used:**
- Model: `CONFIG["OPENAI_MODEL"]` (default: "gpt-4o-mini")
- Temperature: `CONFIG["TEMPERATURE"]` (default: 0.3)
- API Key: `CONFIG["OPENAI_API_KEY"]`

---

## Data Flow & Execution Paths

### Path 1: Attack Tab Processing (Prompt Injection, Data Leakage, etc.)

```
User Input in UI
       ↓
app.py: agent.process(category, user_input)
       ↓
secure_agent.apply_security(category, text)
       ↓
Appropriate sanitization filter (e.g., sanitize_prompt_injection)
       ↓
Is blocked? → YES → Return [BLOCKED: ...] message
       ↓ NO
       ↓
call_llm(system_prompt, sanitized_text)
       ↓
agent_llm.call_llm() → OpenAI API call
       ↓
Return LLM response to UI
       ↓
Store in session_state.report
```

### Path 2: Secure Summarizer (Document Upload)

```
User uploads .txt file
       ↓
app.py: Read file content
       ↓
agent.plan_and_execute("Secure Summarizer", file_content)
       ↓
apply_security() → Multi-layer: sanitize_data_leakage + sanitize_prompt_injection
       ↓
call_llm() with summarization system prompt
       ↓
Return safe summary to UI
       ↓
Store in session_state.report
```

---

## Security Mechanisms Explained

### 1. **Prompt Injection Defense**
- **How:** Pattern matching for injection keywords
- **When:** Before sending user input to LLM
- **Example:** Input "Ignore previous instructions" → Blocked immediately

### 2. **Data Leakage Prevention**
- **How:** Regex-based email/phone detection + masking
- **When:** Sanitizes user input and model output
- **Example:** Input with "john@example.com" → Replaced with "[EMAIL_MASKED]"

### 3. **Model Inversion Blocking**
- **How:** Detects queries about sensitive internal data
- **When:** Before LLM processing
- **Example:** Input "What's the salary?" → Blocked as model inversion attempt

### 4. **Harmful Content Filtering**
- **How:** Keyword detection for violence/hate speech
- **When:** On both input and LLM output
- **Example:** Input "How to kill..." → Filtered immediately

### 5. **Multi-Layer Protection (Summarizer)**
- **How:** Applies multiple sanitization layers sequentially
- **When:** For document uploads
- **Steps:** Mask data → Check injection → LLM → Return safe summary

---

## Key Design Patterns

### 1. **Pipeline Architecture**
- Sequential processing: Input → Sanitization → LLM → Output
- Each layer can block at any stage
- Logging at each step for transparency

### 2. **Defense in Depth**
- Multiple independent filters (prompt injection, data leakage, etc.)
- Multi-layer sanitization for sensitive operations
- Both input and output validation

### 3. **Graceful Degradation**
- LLM fallback: Modern → Legacy OpenAI client
- Comprehensive error handling
- All errors returned as formatted messages

### 4. **Session Management**
- Streamlit session state maintains attack history
- Reports are built chronologically
- Allows demo of multiple attacks in one session

---

## Configuration & Setup

### Environment Variables
The application reads from `config/config.py`:
- `OPENAI_API_KEY` - Required for LLM functionality
- `OPENAI_MODEL` - Model selection (default: "gpt-4o-mini")
- `TEMPERATURE` - Response randomness (0.3 for safety)

### Dependencies
```bash
pip install streamlit openai
```

### Running the Application
```bash
streamlit run app.py
```

---

## Testing

**Test Coverage:** See `TestCases.txt` (90+ scenarios)

**Test Categories:**
1. Prompt Injection (4 tests)
2. Data Leakage (5 tests)
3. Model Inversion (3 tests)
4. Harmful Output (3 tests)
5. Summarizer (5 tests)
6. Reports (3 tests)
7. UI/UX (4 tests)
8. Performance (3 tests)
9. Security (3 tests)
10. Negative Cases (4 tests)

---

## Security Considerations

### Current Implementation
- ✅ Pattern-based injection detection
- ✅ Regex-based sensitive data masking
- ✅ Keyword-based harmful content filtering
- ✅ Temperature-controlled LLM responses (0.3 = safe)

### Limitations
- ⚠️ Keyword matching can be bypassed with variations
- ⚠️ Regex patterns may miss edge cases (unicode, spacing)
- ⚠️ No advanced NLP-based semantic attack detection
- ⚠️ API key exposed in config file (should use environment variables in production)

### Production Recommendations
1. Use environment variables for secrets
2. Implement more sophisticated NLP-based detection
3. Add rate limiting and request throttling
4. Use secure logging without exposing sensitive data
5. Implement audit trails for all security events
6. Add authentication and authorization layers

---

## Extension Points

### Adding New Security Filters
Add method to `SecureAgent`:
```python
def sanitize_new_threat(self, text: str) -> str:
    # Your detection logic
    return text  # or [BLOCKED: ...]
```

Then add case in `apply_security()`:
```python
elif category == "New Threat":
    text = self.sanitize_new_threat(text)
    steps.append(f"[New Filter] → {text}")
```

### Adding New Attack Scenarios
Add tab in `app.py`:
```python
with tabs[6]:  # New tab
    st.subheader("New Attack Type")
    user_input = st.text_area("Enter input:")
    if st.button("Run"):
        output = agent.process("New Attack Type", user_input)
        st.text_area("Output:", output)
```

---

## Related Documentation

- **Readme.md** - Quick feature overview
- **TestCases.txt** - 90+ test scenarios with expected outcomes
- **malicious_input.txt** - Pre-made attack examples
- **sample_report.txt** - Example output format

---

## Summary

The Secure AI Defense Lab demonstrates a **layered security approach** for AI systems:

| Layer | Component | Method |
|-------|-----------|--------|
| 1. Input Validation | SecureAgent filters | Pattern matching |
| 2. Sanitization | Data masking | Regex replacement |
| 3. Safe Processing | Temperature control | LLM config |
| 4. Output Verification | Logging & transparency | Step-by-step traces |

This project is ideal for **learning AI security**, **training teams**, and **prototyping security controls** before production deployment.
