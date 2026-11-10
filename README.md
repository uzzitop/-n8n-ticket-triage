# n8n ticket triage

An n8n workflow that reads a support message, classifies it with a local LLM (Ollama) and creates a ticket in Jira with the category, urgency, a short summary and a suggested reply.

## The problem

In support, every incoming message has to be read, sorted and turned into a ticket before anyone can work on it. At the IoT startup where I worked, writing tickets from messy notes was one of the most repetitive parts of the day. This workflow does that first pass automatically, so a person only reviews the ticket instead of writing it.

## How it works

![Workflow](flujo.png)

1. **Message**: the support message comes in (for testing, it is set by hand in the `mensaje` node).
2. **Ollama**: an HTTP request sends the message to a local model (`qwen3.5:9b`) with a prompt that asks for a JSON with 4 keys.
3. **Collect Data**: the JSON answer is split into fields.
4. **Jira**: a new issue is created with those fields.

What the model returns for each message:

| Field | Values |
|---|---|
| `categoria` | pago (payment), conectividad (connectivity), hardware, otro (other) |
| `urgencia` | alta, media, baja (high, medium, low) |
| `resumen` | one short sentence |
| `respuesta` | a short, polite suggested reply in Spanish |

## Results

I tested it with 15 sample messages from a vending machine support context and compared the model's category with the one I expected.

**13 of 15 correct (87%).** Full list in [`tests/results.csv`](tests/results.csv); the score is calculated by [`tests/score.py`](tests/score.py).

The 2 misses:

| # | Message | Expected | Model | Why it probably failed |
|---|---|---|---|---|
| 3 | "El lector de tarjetas dice «error de comunicación»." | pago | hardware | A card reader is physical hardware, so the label is ambiguous. The prompt doesn't say that card readers count as payment. |
| 11 | "Necesito una factura del mes pasado." | otro | pago | An invoice sounds like money, but it's an admin request, not a payment problem. |

Both misses come from category boundaries, not from the model reading the message wrong. The next step is to add one-line definitions of each category to the prompt and run the same 15 messages again.

## Stack

- n8n (self-hosted, runs on my own computer)
- Ollama with `qwen3.5:9b` (runs locally, no data leaves the machine)
- Jira Software Cloud (free plan)

## How to run it

1. Install [n8n](https://docs.n8n.io/hosting/) and [Ollama](https://ollama.com/), then run `ollama pull qwen3.5:9b`.
2. In n8n, import `workflow.json` (Workflows → Import from file).
3. Add your own Jira credentials in the **Create an issue** node and pick your project.
4. Write a message in the `mensaje` node and click **Execute workflow**.

`workflow.json` contains no credentials.

## Next steps

- Category definitions in the prompt, then re-test (target: 15/15).
- Replace the manual trigger with a webhook or email trigger so messages come in on their own.
- Log every run to compare the model's urgency with the urgency a person would set.
