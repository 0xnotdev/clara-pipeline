"""
Pipeline A: Demo Call Transcript -> Account Memo JSON + Retell Agent Spec v1
"""

import os
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime
from groq import Groq

# ── Config ──────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
MODEL = "llama-3.3-70b-versatile"
OUTPUT_BASE = Path("outputs/accounts")
TRANSCRIPTS_DIR = Path("transcripts/demo")

ACCOUNT_ID_MAP = {
    "demo_001": "ACE_001",
    "demo_002": "BSE_002",
    "demo_003": "GCR_003",
    "demo_004": "NHS_004",
    "demo_005": "RRR_005",
}

# ── LLM Client ───────────────────────────────────────────────────────────────
def get_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set. Run: export GROQ_API_KEY=your_key")
    return Groq(api_key=GROQ_API_KEY)

def call_llm(client, prompt: str, system: str = "") -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.1,  # Low temp for consistent structured extraction
        max_tokens=3000,
    )
    return response.choices[0].message.content.strip()

# ── Extraction ───────────────────────────────────────────────────────────────
EXTRACTION_SYSTEM = """You are a precise data extraction assistant for a phone answering service company called Clara Answers.
Your job is to extract structured information from call transcripts.
CRITICAL RULES:
- Only extract information explicitly stated in the transcript
- Never invent or assume details not present
- If a field is not mentioned, use null or empty list
- Always return valid JSON only, no markdown, no explanation
- For questions_or_unknowns: only add if something critical for routing is genuinely missing"""

EXTRACTION_PROMPT = """Extract the following structured data from this demo call transcript.
Return ONLY a valid JSON object with exactly these fields:

{{
  "account_id": "{account_id}",
  "company_name": "<extracted>",
  "business_hours": {{
    "days": "<e.g. Monday-Friday>",
    "start": "<e.g. 7:00 AM>",
    "end": "<e.g. 6:00 PM>",
    "timezone": "<e.g. Central Time>"
  }},
  "office_address": "<full address or null>",
  "services_supported": ["<list of services>"],
  "emergency_definition": ["<list of what qualifies as emergency>"],
  "emergency_routing_rules": {{
    "step_1": {{
      "contact_name": "<name>",
      "phone": "<number>",
      "rings_before_next": <number or null>
    }},
    "step_2": {{
      "contact_name": "<name or null>",
      "phone": "<number or null>",
      "rings_before_next": <number or null>
    }},
    "fallback": "<what to do if all contacts fail>"
  }},
  "non_emergency_routing_rules": "<description of non-emergency handling>",
  "call_transfer_rules": {{
    "office_hours_transfer_to": "<name and number>",
    "timeout_rings": <number or null>,
    "if_no_answer": "<what to do>",
    "collect_before_transfer": ["<fields to collect>"]
  }},
  "integration_constraints": ["<list of software constraints>"],
  "after_hours_flow_summary": "<1-2 sentence summary>",
  "office_hours_flow_summary": "<1-2 sentence summary>",
  "special_rules": ["<any VIP clients, special flags, or escalation rules>"],
  "questions_or_unknowns": ["<only truly missing critical info>"],
  "notes": "<short summary note>"
}}

TRANSCRIPT:
{transcript}"""

def extract_account_memo(client, transcript: str, account_id: str) -> dict:
    prompt = EXTRACTION_PROMPT.format(account_id=account_id, transcript=transcript)
    raw = call_llm(client, prompt, EXTRACTION_SYSTEM)
    
    # Find the JSON object — extract everything between first { and last }
    start = raw.find('{')
    end = raw.rfind('}')
    if start != -1 and end != -1 and end > start:
        raw = raw[start:end+1]
    else:
        # Strip markdown fences as fallback
        raw = re.sub(r"^```json\s*", "", raw.strip())
        raw = re.sub(r"^```\s*", "", raw.strip())
        raw = re.sub(r"```\s*$", "", raw.strip())
    
    try:
        memo = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ⚠ JSON parse error: {e}")
        print(f"  Raw response: {raw[:300]}")
        raise
    
    memo["_meta"] = {
        "version": "v1",
        "created_at": datetime.utcnow().isoformat(),
        "source": "demo_call",
        "pipeline": "pipeline_a"
    }
    return memo

# ── Agent Spec Generator ──────────────────────────────────────────────────────
AGENT_SYSTEM = """You are an expert voice AI agent designer for Clara Answers, a phone answering service.
You write precise, natural-sounding system prompts for Retell AI voice agents.
CRITICAL RULES:
- Never mention "function calls", "tools", "APIs", or internal systems to the caller
- Agent must collect ONLY what's needed for routing — no unnecessary questions
- Prompts must be clear, warm, and professional
- Always include explicit transfer-fail fallback instructions
- Return only valid JSON"""

AGENT_PROMPT = """Using this account memo, generate a complete Retell Agent Draft Spec.

ACCOUNT MEMO:
{memo_json}

Return ONLY a valid JSON object:
{{
  "agent_name": "<CompanyName> - Clara Agent",
  "version": "v1",
  "voice_style": "professional, warm, concise",
  "language": "en-US",
  "key_variables": {{
    "company_name": "<value>",
    "timezone": "<value>",
    "business_hours": "<human readable>",
    "office_address": "<value>",
    "emergency_phone_1": "<value>",
    "emergency_phone_2": "<value or null>",
    "office_transfer_phone": "<value>"
  }},
  "system_prompt": "<FULL detailed system prompt — see requirements below>",
  "call_transfer_protocol": {{
    "during_hours": "<transfer steps>",
    "after_hours_emergency": "<transfer steps>",
    "after_hours_non_emergency": "<steps>"
  }},
  "transfer_fail_protocol": "<exact instructions if transfer fails>",
  "tool_invocation_placeholders": [
    "transfer_call",
    "send_message_notification"
  ],
  "fallback_protocol": "<what to do if all else fails>",
  "created_at": "{timestamp}"
}}

SYSTEM PROMPT MUST INCLUDE:
1. BUSINESS HOURS FLOW: greet with company name, state purpose, collect caller name and callback number, route/transfer, if transfer fails say sorry and confirm message taken, ask "is there anything else", close warmly.
2. AFTER HOURS FLOW: greet, ask purpose, confirm if emergency using the exact emergency triggers, if emergency: collect name + number + address immediately then attempt transfer, if transfer fails assure callback within [timeframe], if NOT emergency: collect name + number + issue summary, assure next-business-day callback, ask "anything else", close.
3. Must NOT mention tools, APIs, or software.
4. Must include exact wording for transfer failure.
5. Must include any special rules from the memo (VIP clients, special flags, etc.)."""

def generate_agent_spec(client, memo: dict) -> dict:
    memo_json = json.dumps(memo, indent=2)
    timestamp = datetime.utcnow().isoformat()
    prompt = AGENT_PROMPT.format(memo_json=memo_json, timestamp=timestamp)
    raw = call_llm(client, prompt, AGENT_SYSTEM)
    
    start = raw.find('{')
    end = raw.rfind('}')
    if start != -1 and end != -1 and end > start:
        raw = raw[start:end+1]
    else:
        raw = re.sub(r"^```json\s*", "", raw.strip())
        raw = re.sub(r"^```\s*", "", raw.strip())
        raw = re.sub(r"```\s*$", "", raw.strip())
    
    try:
        spec = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ⚠ Agent spec JSON parse error: {e}")
        raise
    
    return spec

# ── Storage ───────────────────────────────────────────────────────────────────
def save_outputs(account_id: str, memo: dict, agent_spec: dict, version: str = "v1"):
    out_dir = OUTPUT_BASE / account_id / version
    out_dir.mkdir(parents=True, exist_ok=True)
    
    memo_path = out_dir / "account_memo.json"
    agent_path = out_dir / "agent_spec.json"
    
    with open(memo_path, "w") as f:
        json.dump(memo, f, indent=2)
    
    with open(agent_path, "w") as f:
        json.dump(agent_spec, f, indent=2)
    
    print(f"  ✓ Saved: {memo_path}")
    print(f"  ✓ Saved: {agent_path}")
    return out_dir

# ── Task Tracker (GitHub Issues mock) ────────────────────────────────────────
def create_task_tracker_item(account_id: str, company_name: str, version: str):
    """Creates a local task tracker JSON (mocked GitHub/Asana item)"""
    tracker_dir = Path("outputs/task_tracker")
    tracker_dir.mkdir(parents=True, exist_ok=True)
    
    task = {
        "task_id": f"TASK-{account_id}-{version.upper()}",
        "title": f"[{version.upper()}] Agent configured for {company_name}",
        "account_id": account_id,
        "status": "ready_for_review",
        "version": version,
        "created_at": datetime.utcnow().isoformat(),
        "outputs": [
            f"outputs/accounts/{account_id}/{version}/account_memo.json",
            f"outputs/accounts/{account_id}/{version}/agent_spec.json"
        ],
        "next_steps": [
            "Review agent system prompt",
            "Paste into Retell UI or call Retell API",
            "Schedule onboarding call with client"
        ]
    }
    
    task_path = tracker_dir / f"{account_id}_{version}.json"
    with open(task_path, "w") as f:
        json.dump(task, f, indent=2)
    
    print(f"  ✓ Task tracker item: {task_path}")
    return task

# ── Main Pipeline A ───────────────────────────────────────────────────────────
def run_pipeline_a(transcript_file: Path, client) -> dict:
    filename = transcript_file.stem  # e.g. "demo_001"
    account_id = ACCOUNT_ID_MAP.get(filename, filename.upper())
    
    print(f"\n{'='*60}")
    print(f"  Pipeline A | {filename} -> {account_id}")
    print(f"{'='*60}")
    
    # Step 1: Read transcript
    transcript = transcript_file.read_text()
    print(f"  📄 Loaded transcript ({len(transcript)} chars)")
    
    # Step 2: Extract account memo
    print(f"  🔍 Extracting account memo...")
    memo = extract_account_memo(client, transcript, account_id)
    company = memo.get("company_name", account_id)
    print(f"  ✓ Extracted: {company}")
    
    # Step 3: Generate agent spec
    print(f"  🤖 Generating Retell agent spec v1...")
    agent_spec = generate_agent_spec(client, memo)
    print(f"  ✓ Agent spec generated")
    
    # Step 4: Save outputs
    print(f"  💾 Saving outputs...")
    save_outputs(account_id, memo, agent_spec, "v1")
    
    # Step 5: Create task tracker item
    create_task_tracker_item(account_id, company, "v1")
    
    print(f"  ✅ Pipeline A complete for {company} ({account_id})")
    return {"account_id": account_id, "company": company, "status": "success"}

def main():
    print("\n🚀 Clara Pipeline A — Demo Call -> Agent v1")
    print(f"   Model: {MODEL}")
    print(f"   Transcripts: {TRANSCRIPTS_DIR}")
    
    client = get_client()
    results = []
    
    transcript_files = sorted(TRANSCRIPTS_DIR.glob("*.txt"))
    if not transcript_files:
        print(f"❌ No transcripts found in {TRANSCRIPTS_DIR}")
        return
    
    print(f"\n   Found {len(transcript_files)} transcripts")
    
    for tf in transcript_files:
        try:
            result = run_pipeline_a(tf, client)
            results.append(result)
        except Exception as e:
            print(f"  ❌ Failed for {tf.name}: {e}")
            results.append({"file": tf.name, "status": "failed", "error": str(e)})
    
    # Summary
    print(f"\n{'='*60}")
    print(f"  Pipeline A Summary")
    print(f"{'='*60}")
    success = sum(1 for r in results if r.get("status") == "success")
    print(f"  ✅ Succeeded: {success}/{len(results)}")
    for r in results:
        status = "✅" if r.get("status") == "success" else "❌"
        name = r.get("company", r.get("file", "unknown"))
        print(f"  {status} {name} ({r.get('account_id', '?')})")
    
    # Save run log
    log_path = Path("outputs/pipeline_a_run.json")
    with open(log_path, "w") as f:
        json.dump({
            "run_at": datetime.utcnow().isoformat(),
            "model": MODEL,
            "results": results
        }, f, indent=2)
    print(f"\n  📋 Run log: {log_path}")

if __name__ == "__main__":
    main()
