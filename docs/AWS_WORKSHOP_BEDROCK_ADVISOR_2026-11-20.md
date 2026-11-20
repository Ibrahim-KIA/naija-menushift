# AWS Hack the Fork workshop — optional Bedrock adapter (20 November 2026)

## Access findings, not a permanent AWS account
The connected Workshop Studio event **HACK THE FORK ABUDJA** lists a 72-hour event starting on 19 November 2026, 17:00, and permits work in **us-east-1**. Its workshop covers Bedrock, SageMaker AI and S3, and provides a browser IDE and CLI/SDK access instructions. The account is temporary; AWS says the workshop resources and credentials are revoked/deleted after the event.

**The browser dashboard currently shows a team reassignment notice. Do not click Continue without confirming that no existing team resources need preserving.** Old team resources can become inaccessible. Never publish the workshop join code, AWS CLI credentials, AWS access keys, session tokens, signed IDE URLs or model output containing personal information in a public repository or site.

## Why Bedrock and what it actually does
Challenge 2 asks for an AI-enabled, explainable transformation of an existing menu item. The existing Python engine already filters hard constraints and ranks provisional formulations. Bedrock is a **complementary optional AI assistant**: it may select one to three already-feasible candidates for culinary *experimentation*, using a restaurant's short preference text and bounded cost/protein/time estimates.

It cannot invent an ingredient, change nutritional calculations, introduce an out-of-pool recipe, bypass a declared allergen/equipment constraint, certify food safety, produce patient diet recommendations or generate arbitrary user-facing recipe claims. Its response is strictly validated against the list of feasible IDs, and only fixed, code-defined follow-up questions are displayed.

This is a bounded *research-priority proposal*, not a validated taste model or evidence of improved ranking. The current AWS option is **not wired into either public web app** and AWS inference has **not yet been run against the team account**. The public Python/Next.js experiences stay deterministic, functional and unmodified.

## Code
- `src/menushift/bedrock_advisor.py`: one-shot Bedrock Converse call, schema and allowlist validation, optional Bedrock Guardrails configuration, failure fallback, capped token generation
- `tests/test_bedrock_advisor.py`: offline mock-client tests; zero AWS charges and no credentials
- `scripts/workshop_bedrock_demo.py`: manual, explicitly opted-in smoke test, called only in an authorised workshop IDE

## Authenticated workshop test procedure (only after team account is settled)
1. In Workshop Studio, verify the **current team** and its account. If the reassignment dialog is still shown, obtain the team's confirmation before accepting it. Do not proceed on a previous team's resources.
2. Open the provided AWS IDE or the AWS console using the authenticated workshop interface; check available Bedrock model access and approved per-team quotas for `us-east-1`. Do not assume a specific model ID is enabled or that all services are free forever.
3. In the authorised workshop terminal, pull the private repo using approved access. Do not put GitHub tokens or AWS credentials in code or command arguments.
4. Ensure Python 3.11+ is available, and install project dependencies plus the optional Bedrock client, for example `python -m pip install -e . boto3`. No new default production dependency is required.
5. Set `MENUSHIFT_BEDROCK_MODEL_ID` to a **verified model or inference profile ID** from the team account. If the team has configured and tested a Bedrock Guardrail, you may also set `MENUSHIFT_GUARDRAIL_ID` and `MENUSHIFT_GUARDRAIL_VERSION` together. These are IDs, not credentials.
6. From the repo root run `python scripts/workshop_bedrock_demo.py`. It makes at most **one** model inference call, with low output-token limit and no automatic retries. Verify that any returned IDs belong to the deterministic eligible set. On any rejection, model error or expired permission, the adapter returns `unavailable` and the deterministic engine remains authoritative.
7. Capture a redacted test result (status, allowed IDs, timestamp, model ID, whether optional service-side guardrail was configured). Do **not** retain raw prompts with personal data or secrets. Test an allergen-excluded/no-candidate case without an AWS call.

## Data, costs and permanence
- Use curated ingredient references only after review; no private patient data, precise personal information or unlicensed product data in prompts.
- AWS credits/permissions/available models need verification. The implementation **does not silently invoke or provision AWS resources**; every model call requires explicitly running the test, or a later gated integration.
- The workshop account is short-lived and should not become a production dependency. Do not store temporary workshop credentials in Vercel, Streamlit, source code, CI, Google Drive or messages.
- Keep the production application usable without AWS. Before a persistent release, obtain a separately controlled AWS account, deployment design, budget, rate limits, data privacy review and service-side guardrail evaluation.
- Even with Bedrock Guardrails configured, Python validation and human kitchen/food-safety review remain mandatory.

## AWS documentation
- Converse API: https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html
- Boto3 Converse client: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse.html
- Bedrock Guardrails: https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
