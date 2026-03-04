"""
Pipeline B: Onboarding Call Transcript -> Updated Memo + Agent Spec v2 + Changelog
"""

import os
import json
import re
import copy
from pathlib import Path
from datetime import datetime
from groq import Groq

# ── Config ──────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
MODEL = "llama-3.1-8b-instant"
OUTPUT_BASE = Path("outputs/accounts")
TRANSCRIPTS_DIR = Path("transcripts/onboarding")
CHANGELOG_DIR = Path("changelog")

ONBOARDING_MAP = {
    "onboarding_001": "ACE_001",
    "onboarding_002": "BSE_002",
    "onboarding_003": "GCR_003",
    "onboarding_004": "NHS_004",
    "onboarding_005": "RRR_005",
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
        temperature=0.1,
        max_tokens=3000,
    )
    return response.choices[0].message.content.strip()

# ── Load v1 ──────────────────────────────────────────────────────────────────
def load_v1(account_id: str) -> tuple[dict, dict]:
    v1_dir = OUTPUT_BASE / account_id / "v1"
    memo_path = v1_dir / "account_memo.json"
    agent_path = v1_dir / "agent_spec.json"
    
    if not memo_path.exists():
        raise FileNotFoundError(f"v1 memo not found: {memo_path}. Run pipeline_a.py first.")
    
    with open(memo_path) as f:
        memo = json.load(f)
    with open(agent_path) as f:
        agent = json.load(f)
    
    return memo, agent

# ── Extract Updates ──────────────────────────────────────────────────────────
UPDATE_SYSTEM = """You are a precise update extraction assistant for a phone answering service.
Extract ONLY the changes/updates mentioned in the onboarding call — things that DIFFER from the original setup.
Return only what changed. Do not repeat unchanged information.
Return valid JSON only."""

UPDATE_PROMPT = """This is an onboarding call transcript for an existing account.
The CURRENT account memo (v1) is provided below.
Extract ONLY the changes/updates mentioned in the onboarding transcript.

CURRENT v1 MEMO:
{v1_memo}

ONBOARDING TRANSCRIPT:
{transcript}

Return a JSON object describing ONLY what changed:
{{
  "changes": [
    {{
      "field": "<field name from memo, e.g. business_hours, emergency_routing_rules>",
      "old_value": "<what it was>",
      "new_value": "<what it is now>",
      "reason": "<why it changed, inferred from transcript>"
    }}
  ],
  "new_rules_added": ["<any brand new rules not in v1>"],
  "integration_constraint_updates": ["<any new software/integration constraints>"],
  "greeting_update": "<new greeting text if changed, else null>",
  "special_rules_updates": ["<new VIP rules, escalation rules, flags>"],
  "summary": "<1-2 sentence summary of what changed and why>"
}}"""

def extract_updates(client, transcript: str, v1_memo: dict) -> dict:
    prompt = UPDATE_PROMPT.format(
        v1_memo=json.dumps(v1_memo, indent=2),
        transcript=transcript
    )
    raw = call_llm(client, prompt, UPDATE_SYSTEM)
    _s = raw.find('{'); _e = raw.rfind('}')
    if _s != -1 and _e > _s: raw = raw[_s:_e+1]
    else:
        raw = re.sub(r"^```json\s*", "", raw.strip())
        raw = re.sub(r"^```\s*", "", raw.strip())
        raw = re.sub(r"```\s*$", "", raw.strip())
    
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ⚠ Update JSON parse error: {e}")
        raise

# ── Apply Patch ───────────────────────────────────────────────────────────────
PATCH_SYSTEM = """You are a precise data merging assistant. Apply updates to an existing JSON memo.
Return the complete updated JSON memo with all changes applied.
Return only valid JSON."""

PATCH_PROMPT = """Apply these updates to the existing account memo to produce the v2 memo.

CURRENT v1 MEMO:
{v1_memo}

UPDATES TO APPLY:
{updates}

Rules:
- Apply all changes listed
- Add all new rules
- Update integration constraints
- Update greeting if provided
- Update special rules
- Preserve all unchanged fields
- Update _meta to version v2 with updated_at timestamp
- Add a "v1_to_v2_changes" field summarizing what changed

Return the COMPLETE updated memo as valid JSON."""

def apply_patch(client, v1_memo: dict, updates: dict) -> dict:
    prompt = PATCH_PROMPT.format(
        v1_memo=json.dumps(v1_memo, indent=2),
        updates=json.dumps(updates, indent=2)
    )
    raw = call_llm(client, prompt, PATCH_SYSTEM)
    _s = raw.find('{'); _e = raw.rfind('}')
    if _s != -1 and _e > _s: raw = raw[_s:_e+1]
    else:
        raw = re.sub(r"^```json\s*", "", raw.strip())
        raw = re.sub(r"^```\s*", "", raw.strip())
        raw = re.sub(r"```\s*$", "", raw.strip())
    
    try:
        v2_memo = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ⚠ Patch JSON parse error: {e}")
        raise
    
    v2_memo["_meta"] = {
        "version": "v2",
        "created_at": v1_memo.get("_meta", {}).get("created_at", ""),
        "updated_at": datetime.utcnow().isoformat(),
        "source": "onboarding_call",
        "pipeline": "pipeline_b"
    }
    return v2_memo

# ── Regenerate Agent Spec v2 ──────────────────────────────────────────────────
AGENT_SYSTEM = """You are an expert voice AI agent designer for Clara Answers.
You write precise, natural-sounding system prompts for Retell AI voice agents.
Never mention function calls, tools, APIs, or internal software to callers.
Return only valid JSON."""

AGENT_PROMPT = """Using this UPDATED v2 account memo, generate the updated Retell Agent Spec v2.

V2 ACCOUNT MEMO:
{memo_json}

Return ONLY a valid JSON object:
{{
  "agent_name": "<CompanyName> - Clara Agent",
  "version": "v2",
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
  "system_prompt": "<FULL detailed system prompt>",
  "call_transfer_protocol": {{
    "during_hours": "<transfer steps>",
    "after_hours_emergency": "<transfer steps>",
    "after_hours_non_emergency": "<steps>"
  }},
  "transfer_fail_protocol": "<exact instructions if transfer fails>",
  "tool_invocation_placeholders": ["transfer_call", "send_message_notification"],
  "fallback_protocol": "<what to do if all else fails>",
  "updated_at": "{timestamp}"
}}

SYSTEM PROMPT MUST INCLUDE:
1. BUSINESS HOURS FLOW: greet with company name (use exact greeting from memo if specified), collect name and callback number, transfer to office, if transfer fails take message and confirm callback time, ask "anything else", close.
2. AFTER HOURS FLOW: greet, ask purpose, confirm emergency using exact triggers from memo, if emergency collect name+number+address immediately then transfer, if transfer fails give exact callback promise, if NOT emergency take message with callback promise, ask "anything else", close.
3. Apply all special rules (VIP clients, flags, escalation rules).
4. Never mention tools, software, or APIs to caller."""

def regenerate_agent_spec(client, v2_memo: dict) -> dict:
    prompt = AGENT_PROMPT.format(
        memo_json=json.dumps(v2_memo, indent=2),
        timestamp=datetime.utcnow().isoformat()
    )
    raw = call_llm(client, prompt, AGENT_SYSTEM)
    _s = raw.find('{'); _e = raw.rfind('}')
    if _s != -1 and _e > _s: raw = raw[_s:_e+1]
    else:
        raw = re.sub(r"^```json\s*", "", raw.strip())
        raw = re.sub(r"^```\s*", "", raw.strip())
        raw = re.sub(r"```\s*$", "", raw.strip())
    
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  ⚠ Agent v2 JSON parse error: {e}")
        raise

# ── Diff Generator ────────────────────────────────────────────────────────────
def generate_diff(v1_memo: dict, v2_memo: dict, v1_agent: dict, v2_agent: dict, updates: dict) -> dict:
    """Generate a structured diff/changelog between v1 and v2"""
    
    def compare_values(v1, v2, path=""):
        diffs = []
        if isinstance(v1, dict) and isinstance(v2, dict):
            all_keys = set(v1.keys()) | set(v2.keys())
            for k in sorted(all_keys):
                if k.startswith("_"):
                    continue
                child_path = f"{path}.{k}" if path else k
                if k not in v1:
                    diffs.append({"field": child_path, "change": "added", "new_value": v2[k]})
                elif k not in v2:
                    diffs.append({"field": child_path, "change": "removed", "old_value": v1[k]})
                elif v1[k] != v2[k]:
                    if isinstance(v1[k], (dict, list)):
                        diffs.extend(compare_values(v1[k], v2[k], child_path))
                    else:
                        diffs.append({
                            "field": child_path,
                            "change": "modified",
                            "old_value": v1[k],
                            "new_value": v2[k]
                        })
        elif isinstance(v1, list) and isinstance(v2, list):
            if v1 != v2:
                added = [x for x in v2 if x not in v1]
                removed = [x for x in v1 if x not in v2]
                if added:
                    diffs.append({"field": path, "change": "items_added", "new_items": added})
                if removed:
                    diffs.append({"field": path, "change": "items_removed", "removed_items": removed})
        return diffs
    
    memo_diffs = compare_values(v1_memo, v2_memo)
    
    # Compare system prompts
    v1_prompt = v1_agent.get("system_prompt", "")
    v2_prompt = v2_agent.get("system_prompt", "")
    prompt_changed = v1_prompt != v2_prompt
    
    changelog = {
        "account_id": v2_memo.get("account_id"),
        "company_name": v2_memo.get("company_name"),
        "changelog_generated_at": datetime.utcnow().isoformat(),
        "version_from": "v1",
        "version_to": "v2",
        "summary": updates.get("summary", "Onboarding updates applied"),
        "memo_field_changes": memo_diffs,
        "agent_prompt_updated": prompt_changed,
        "new_rules_added": updates.get("new_rules_added", []),
        "integration_updates": updates.get("integration_constraint_updates", []),
        "special_rules_updates": updates.get("special_rules_updates", []),
        "greeting_updated": updates.get("greeting_update") is not None,
        "greeting_new_value": updates.get("greeting_update"),
        "total_changes": len(memo_diffs),
    }
    return changelog

def save_changelog(account_id: str, changelog: dict):
    CHANGELOG_DIR.mkdir(parents=True, exist_ok=True)
    path = CHANGELOG_DIR / f"{account_id}_changes.json"
    with open(path, "w") as f:
        json.dump(changelog, f, indent=2)
    
    # Also write human-readable markdown
    md_path = CHANGELOG_DIR / f"{account_id}_changes.md"
    md = f"# Changelog: {changelog['company_name']} ({account_id})\n\n"
    md += f"**Version:** {changelog['version_from']} → {changelog['version_to']}\n\n"
    md += f"**Date:** {changelog['changelog_generated_at']}\n\n"
    md += f"**Summary:** {changelog['summary']}\n\n"
    md += f"## Changes ({changelog['total_changes']} field changes)\n\n"
    
    for diff in changelog.get("memo_field_changes", []):
        md += f"### `{diff['field']}`\n"
        change = diff.get("change", "")
        if change == "modified":
            md += f"- **Before:** `{diff.get('old_value')}`\n"
            md += f"- **After:** `{diff.get('new_value')}`\n\n"
        elif change in ("added", "items_added"):
            md += f"- **Added:** `{diff.get('new_value', diff.get('new_items'))}`\n\n"
        elif change in ("removed", "items_removed"):
            md += f"- **Removed:** `{diff.get('old_value', diff.get('removed_items'))}`\n\n"
    
    if changelog.get("new_rules_added"):
        md += "## New Rules Added\n"
        for r in changelog["new_rules_added"]:
            md += f"- {r}\n"
        md += "\n"
    
    if changelog.get("agent_prompt_updated"):
        md += "## Agent System Prompt\n- ✅ Updated to reflect all v2 changes\n\n"
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    
    print(f"  ✓ Changelog JSON: {path}")
    print(f"  ✓ Changelog MD:   {md_path}")

def save_v2_outputs(account_id: str, v2_memo: dict, v2_agent: dict):
    out_dir = OUTPUT_BASE / account_id / "v2"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    with open(out_dir / "account_memo.json", "w") as f:
        json.dump(v2_memo, f, indent=2)
    with open(out_dir / "agent_spec.json", "w") as f:
        json.dump(v2_agent, f, indent=2)
    
    print(f"  ✓ Saved: {out_dir}/account_memo.json")
    print(f"  ✓ Saved: {out_dir}/agent_spec.json")

# ── Task Tracker ──────────────────────────────────────────────────────────────
def create_task_tracker_item(account_id: str, company_name: str):
    tracker_dir = Path("outputs/task_tracker")
    tracker_dir.mkdir(parents=True, exist_ok=True)
    
    task = {
        "task_id": f"TASK-{account_id}-V2",
        "title": f"[V2] Agent updated after onboarding for {company_name}",
        "account_id": account_id,
        "status": "ready_for_review",
        "version": "v2",
        "created_at": datetime.utcnow().isoformat(),
        "outputs": [
            f"outputs/accounts/{account_id}/v2/account_memo.json",
            f"outputs/accounts/{account_id}/v2/agent_spec.json",
            f"changelog/{account_id}_changes.json",
            f"changelog/{account_id}_changes.md"
        ],
        "next_steps": [
            "Review v2 agent system prompt",
            "Compare with v1 using diff viewer",
            "Update agent in Retell UI",
            "Confirm with client before go-live"
        ]
    }
    
    path = tracker_dir / f"{account_id}_v2.json"
    with open(path, "w") as f:
        json.dump(task, f, indent=2)
    print(f"  ✓ Task tracker item: {path}")

# ── Main Pipeline B ───────────────────────────────────────────────────────────
def run_pipeline_b(transcript_file: Path, client) -> dict:
    filename = transcript_file.stem
    account_id = ONBOARDING_MAP.get(filename, filename.upper())
    
    print(f"\n{'='*60}")
    print(f"  Pipeline B | {filename} -> {account_id} v2")
    print(f"{'='*60}")
    
    # Step 1: Load v1
    print(f"  📂 Loading v1 assets...")
    v1_memo, v1_agent = load_v1(account_id)
    company = v1_memo.get("company_name", account_id)
    print(f"  ✓ Loaded v1 for {company}")
    
    # Step 2: Read onboarding transcript
    transcript = transcript_file.read_text()
    print(f"  📄 Loaded transcript ({len(transcript)} chars)")
    
    # Step 3: Extract updates
    print(f"  🔍 Extracting updates from onboarding...")
    updates = extract_updates(client, transcript, v1_memo)
    n_changes = len(updates.get("changes", []))
    print(f"  ✓ Found {n_changes} changes")
    
    # Step 4: Apply patch to produce v2 memo
    print(f"  🔧 Applying patch to memo...")
    v2_memo = apply_patch(client, v1_memo, updates)
    print(f"  ✓ v2 memo generated")
    
    # Step 5: Regenerate agent spec v2
    print(f"  🤖 Regenerating agent spec v2...")
    v2_agent = regenerate_agent_spec(client, v2_memo)
    print(f"  ✓ Agent spec v2 generated")
    
    # Step 6: Generate diff/changelog
    print(f"  📊 Generating changelog...")
    changelog = generate_diff(v1_memo, v2_memo, v1_agent, v2_agent, updates)
    save_changelog(account_id, changelog)
    
    # Step 7: Save v2 outputs
    print(f"  💾 Saving v2 outputs...")
    save_v2_outputs(account_id, v2_memo, v2_agent)
    
    # Step 8: Task tracker
    create_task_tracker_item(account_id, company)
    
    print(f"  ✅ Pipeline B complete for {company} ({account_id}) — {changelog['total_changes']} changes")
    return {
        "account_id": account_id,
        "company": company,
        "status": "success",
        "changes": changelog["total_changes"]
    }

def main():
    print("\n🚀 Clara Pipeline B — Onboarding -> Agent v2")
    print(f"   Model: {MODEL}")
    
    client = get_client()
    results = []
    
    transcript_files = sorted(TRANSCRIPTS_DIR.glob("*.txt"))
    if not transcript_files:
        print(f"❌ No onboarding transcripts in {TRANSCRIPTS_DIR}")
        return
    
    print(f"\n   Found {len(transcript_files)} onboarding transcripts")
    
    for tf in transcript_files:
        try:
            result = run_pipeline_b(tf, client)
            results.append(result)
        except Exception as e:
            print(f"  ❌ Failed for {tf.name}: {e}")
            import traceback; traceback.print_exc()
            results.append({"file": tf.name, "status": "failed", "error": str(e)})
    
    print(f"\n{'='*60}")
    print(f"  Pipeline B Summary")
    print(f"{'='*60}")
    success = sum(1 for r in results if r.get("status") == "success")
    print(f"  ✅ Succeeded: {success}/{len(results)}")
    for r in results:
        status = "✅" if r.get("status") == "success" else "❌"
        print(f"  {status} {r.get('company', r.get('file'))} — {r.get('changes', 0)} field changes")
    
    log_path = Path("outputs/pipeline_b_run.json")
    with open(log_path, "w") as f:
        json.dump({
            "run_at": datetime.utcnow().isoformat(),
            "model": MODEL,
            "results": results
        }, f, indent=2)
    print(f"\n  📋 Run log: {log_path}")

if __name__ == "__main__":
    main()
