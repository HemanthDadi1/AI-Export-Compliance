# CImEx Review Agent: build plan

What we build at the Buildathon city round. The submission promises it, so this plan keeps the scope small enough to finish in two days.

## The job

The agent reviews a plant's whole file set the way a verifier would. It then:

1. Lists what is wrong or missing, in plain words.
2. Asks the clerk only what it cannot resolve from the files.
3. Drafts the data request to the mill that matters most.
4. Hands over to the clerk, who approves. Then the report unlocks as it does today.

## Demo goal

On the sample plant (`Load sample documents`, then `Confirm all as read`), the agent:

- Finds the 4 open checks the dashboard shows today:
  - diesel: purchase invoices only, no stock log
  - lpg: purchase invoices only, no stock log
  - output: no monthly production log
  - Rayalaseema Steel Rolling: no verified data
- Ranks Rayalaseema first, because it is 63% of the steel and the biggest cost.
- Drafts the request email to Rayalaseema.
- Asks the clerk one question: "Do you keep monthly fuel stock records?" (it cannot know this from the files).
- Changes no figure. The number stays 4.38 tCO2/t until the clerk acts.

## Rules the agent must follow

- **It never sets a number.** It can only call read-only tools. The rule engine in `calc.py` stays the only place a figure is computed.
- **It never sends anything.** It drafts. The clerk copies or sends.
- **Every claim cites a tool result.** If no tool says it, the agent does not say it.
- **No private data leaves the plant's session.** It sees one plant's files only.

## Tools (all exist today; the agent wraps them)

Each tool calls `server.dispatch(...)`, the same router the website uses. Nothing new is computed.

| Tool | Calls | Returns |
|---|---|---|
| `get_readiness()` | `GET /api/readiness` | required items, done or not |
| `get_documents()` | `GET /api/docs` | each file, its fields, source line, issues, confirmed or not |
| `get_plant(year)` | `GET /api/state` | emissions per tonne, steel by mill, open checks (`plan.gaps`), heat conflicts, unmatched heats |
| `get_audit(year)` | `GET /api/audit` | every figure with its source file and any edits |
| `draft_mill_request(mill)` | new, text only | an email asking the mill for its verified value, built from the plant's heats and tonnes for that mill |

`draft_mill_request` is the only new code. It reads the plant and fills a fixed template. No model call.

## Build on Google

- **Agent Development Kit (Python, `google-adk`).** One `LlmAgent` with the five tools above as function tools.
- **Model:** Gemini 2.5 Flash first. Try Gemini 2.5 Pro on the same test if Flash misses checks or ranks badly.
- **Agent Skills:** one skill file with the CBAM review rules in plain words (what a verifier rejects, why fuel bought is not fuel used, why mill data matters most).
- **Hosting:** Cloud Run, next to the existing app. The website keeps working without the agent.
- **Antigravity:** use it to build and test the agent during the event.
- **AI Studio:** tune the agent's instructions against the sample plant before the event.

## Files

```
agent/
  __init__.py
  agent.py      LlmAgent: instructions, model, tools
  tools.py      the five tools, thin wrappers over server.dispatch
  skill.md      CBAM review rules for the agent
test_agent_tools.py   tools return the right facts on the sample plant (no model call)
```

## Tests (write first)

`test_agent_tools.py` runs without a model or key:

- On the sample plant, the tools report exactly the 4 open checks.
- Rayalaseema has the most steel on defaults (660 t, 63%).
- `draft_mill_request("Rayalaseema Steel Rolling")` names the mill, lists its heats and tonnes, and asks for a verified value per tonne.
- No tool changes state: `GET /api/state` is identical before and after every tool call.

The model run is checked by hand on the demo goal above. Record what it says.

## Two-day plan

**Before the event**
- Install `google-adk`. Get a Gemini key from AI Studio.
- Write `tools.py`, `draft_mill_request` and `test_agent_tools.py`. Make the tests pass.
- Draft `skill.md`.

**Day 1**
- Build `agent.py`. Run it on the sample plant from the command line.
- Fix the instructions until it finds all 4 checks and ranks Rayalaseema first.

**Day 2**
- Add an "Ask the review agent" panel to the dashboard that shows the agent's list, question and draft email.
- Deploy to Cloud Run.
- Rehearse the demo: load samples, confirm, run the agent, approve, open the report.

## Out of scope for the Buildathon

- The agent editing records or sending email.
- Shipping bills, ICEGATE or DGFT.
- More than one plant or user accounts.
