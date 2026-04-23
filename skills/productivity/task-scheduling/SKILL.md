---
name: task-scheduling
description: Use when the user wants to schedule a recurring task, reminder, or periodic message to be posted into this chat. Creates, edits, or cancels scheduled jobs via higgsfieldcli cron commands.
---

# Task scheduling

## When to use this skill

Trigger when the user's message expresses intent to set up a **recurring
scheduled message** that will fire automatically at future times in this
chat. Examples:

- "Send me funny cat pictures every morning at 8."
- "Remind me every Monday to write my weekly update."
- "On the 1st of each month, post a summary of last month's news."
- Users may write in any language — detect intent, generate the schedule, and respond in the user's language.

Also trigger for **edit** intent ("change the time to 10am", "make it
weekdays only") and **cancel** intent ("stop the morning reminder",
"cancel the weekly update").

Do NOT trigger for:
- One-off reminders ("remind me tomorrow at 3pm" without recurrence).
  One-shot scheduling is not supported by this service.
- Questions about past scheduled jobs ("did the 8am reminder fire?").
- Changing the service behaviour (this skill only talks to the CRUD API).

## Hard rule: only `higgsfieldcli cron` creates schedules

**NEVER use any other scheduling tool to fulfill this skill.** This includes,
but is not limited to: `CronCreate`, `CronList`, `CronDelete`, `schedule`,
`ScheduleWakeup`, or any tool discovered via `ToolSearch`. Those are built-in
tools that create **session-local triggers** which expire within 7 days and
are invisible to the user's chat — they do NOT create real scheduled
messages.

Only `higgsfieldcli cron <subcommand>` calls the backend service that
persists jobs, dispatches them via the scheduler, and posts the message into
this chat.

If `higgsfieldcli cron` fails for ANY reason (unknown command, non-zero
exit, network error, unexpected output), STOP and report the exact error
text to the user. Do NOT attempt an alternative tool. Do NOT "try another
way". Failure of this CLI = failure of the task; the user needs to know so
they can fix the root cause.

## Core workflow

Every creation or edit follows these steps in order:

1. **Extract structured parameters** from the user's message:
   - `cron_expression` (standard 5-field Unix cron)
   - `timezone` (IANA name, e.g. `America/New_York`, `Europe/London`)
   - `title` (3–5 word human-readable label you generate — e.g. "Daily cat memes")
   - `prompt` (the message content to send on each run — see **step 2** for
     normalization rules before sending)
   - `start_at` **(optional)** — if the user said "starting from X" or "from
     next Monday at 9:35", compute the RFC3339 timestamp of that instant in
     the user's timezone and pass it. See the **Start-time** section below.

2. **Normalize the prompt.** Never forward the user's raw message as
   `prompt` verbatim. Rewrite it into a **clear, self-contained imperative**
   — the job will fire into the chat N times in the future, without the user
   present to clarify, so the text must stand on its own.
   - Fix grammar, typos, missing punctuation.
   - Expand vague verbs ("remind me" → "Remind me to review the Q2 roadmap").
   - Match the user's language in the final prompt (reply in the language the user wrote in).
   - Keep it short and direct — one or two sentences, no preamble.
   - If the user attached files/images, include their URLs inline in the prompt.
   - **Then show the normalized prompt to the user in the confirmation widget
     (step 4) and wait for their approval.** The user must see the exact text
     that will be stored and fired.

3. **Check against unsupported patterns** (see "What NOT to generate" below).
   If the user's request maps to an unsupported pattern, do NOT call the CLI.
   Instead, explain the limitation and offer an alternative.

4. **Resolve the timezone in this order — never guess:**
   - Read `$HF_USER_TIMEZONE`. If non-empty and a valid IANA name (contains `/` or equals `UTC`), use it silently — do not ask.
   - Otherwise, ask: "Which timezone should I use? (e.g. `America/New_York`)"
   - Do not default to UTC silently — 8:00 UTC is not what most users want.
   - **The resolved timezone applies to both `cron_expression` AND `start_at`**
     — they're interpreted in the same zone; pass the IANA name in `--timezone`
     and make sure the `start_at` RFC3339 string carries the correct offset.

5. **Show a confirmation widget** before executing. Display:
   - The **normalized prompt** (from step 2) — user must see final text
   - The parsed schedule in human-readable form ("Every hour at :35 starting Mon 2026-04-20 09:35, London time")
   - The title
   - A Confirm button and a Cancel button
   - Proceed only after the user confirms.

6. **Run the CLI command** (see "Commands" below), parse the JSON response,
   and reply to the user in the user's language with the outcome.

## Cron generation — common patterns

Produce the cron in the standard 5-field format: `minute hour dom month dow`.
DOW: `0` = Sunday, `1` = Monday, ..., `6` = Saturday. 3-letter abbreviations
(`MON`, `TUE`, ...) are also accepted by the server.

| User intent                                 | `cron_expression` |
|---------------------------------------------|-------------------|
| Every day at 8:00                           | `0 8 * * *`       |
| Every day at 8:30                           | `30 8 * * *`      |
| Every hour on the hour                      | `0 * * * *`       |
| Every 2 hours                               | `0 */2 * * *`     |
| Weekdays (Mon–Fri) at 9:00                  | `0 9 * * 1-5`     |
| Weekends at 10:00                           | `0 10 * * 0,6`    |
| Every Monday at 9:00                        | `0 9 * * 1`       |
| Mon, Wed, Fri at 9:00                       | `0 9 * * 1,3,5`   |
| 1st of each month at 12:00                  | `0 12 1 * *`      |
| 1st and 15th at 12:00                       | `0 12 1,15 * *`   |
| 3 times a day (9:00, 14:00, 20:00)          | `0 9,14,20 * * *` |
| 1 January at 00:00 (yearly)                 | `0 0 1 1 *`       |
| Every hour during business hours (Mon–Fri)  | `0 9-18 * * 1-5`  |

## Start-time ("starting from X") — the `start_at` parameter

Use `start_at` when the user anchors the first firing to a specific moment,
typically combined with an interval-style pattern:

- "every hour **starting Monday at 9:35**"
- "every 3 hours **from tomorrow 14:00**"
- "daily **from May 1** at 8am"

### How to generate `start_at`

1. Resolve the user's **absolute instant** for the first firing (date + time of
   day) in the user's timezone. E.g. today is Thursday 2026-04-17 London time;
   user says "starting Monday at 9:35" → Monday 2026-04-21 09:35 London.
2. Emit it as **RFC3339 with the timezone offset**, e.g. `2026-04-21T09:35:00+01:00`.
3. Construct `cron_expression` to match the **cadence** past the first firing.
   - "every hour starting 9:35" → `35 * * * *` (so subsequent firings at 10:35,
     11:35, ...). Don't pick `0 * * * *` here — it would fire at 10:00, not 10:35.
   - "daily from May 1 at 8am" → `0 8 * * *`.

### When NOT to use `start_at`

- "every day at 8am" — no start anchor, just omit `start_at`. Server
  defaults to the next natural cron match.
- "every Tuesday at 9:00" — cron already nails the phase; `start_at` adds nothing.

### Hard rules

- `start_at` **must be in the future** at the moment of the call. Past or
  present values return `400 start_at must be in the future`.
- Confirm with the user in step 5 by showing **absolute first-run time** in
  their timezone: "First firing: Mon 2026-04-21 09:35 London time".
- **Cannot be patched later.** If the user wants to move the start of an
  existing job, you must `delete` + `create` again. Spell this out if they
  ask to "reschedule the start".

## What NOT to generate (unsupported patterns)

The server will reject these. **Do not attempt them.** Recognize the intent,
tell the user it's not supported, and offer the closest workable alternative.

### Patterns the parser rejects

| User phrase                            | Why it fails                          | What to offer instead            |
|----------------------------------------|----------------------------------------|-----------------------------------|
| "last day of the month"                | No `L` support in standard 5-field    | "the 28th of each month" (or ask the user for a specific date) |
| "last Friday of the month"             | No `L` in DOW                         | "every Friday" or a specific date |
| "second Tuesday of each month"         | No `#` in DOW                         | "every Tuesday" or a date         |
| "nearest weekday to the 15th"          | No `W` support                        | Offer the 15th and note it may fall on a weekend |
| `@daily`, `@hourly` shortcuts          | Macros disabled in our parser         | Expand to `0 0 * * *`, `0 * * * *` etc. |
| Seconds precision ("every 30 seconds") | 5-field cron has no seconds field     | Not supportable. Decline.         |

### Schedules faster than once per hour

The server enforces a **1-hour minimum interval**. These will be rejected:

- `* * * * *` (every minute)
- `*/15 * * * *` (every 15 minutes)
- `*/30 * * * *` (every 30 minutes)
- `0,30 * * * *` (twice per hour)

If the user asks for sub-hourly frequency, reply: "This service only supports
schedules of once per hour or slower. Would you like to set it to once per hour?"

### DOM + DOW — OR, not AND (critical gotcha)

When both the day-of-month field and the day-of-week field are not `*`, cron
fires if **either** matches. You **cannot** express "Monday the 1st only" in
standard 5-field cron.

**Rule of thumb:** in every cron you generate, **at least one** of DOM / DOW
must be `*`. Never set both to specific values.

### One-shot ("run once and stop")

This service only supports **recurring** jobs. For "remind me on 2026-12-25
at 8am and never again":
- Tell the user one-off reminders aren't supported here.
- Alternative workaround: set a recurring yearly cron (`0 8 25 12 *`) and
  manually delete the job after the first firing — but confirm the user wants
  that, don't do it silently.

## Timezone rules

- The `timezone` field must be a **valid IANA timezone name** (e.g.
  `America/New_York`, `Europe/London`, `UTC`).
- Fixed offsets (`+05:00`, `UTC+5`) and abbreviations (`PST`, `EST`, `MSK`)
  are **not accepted** — the server will return an error.
- DST is handled correctly by the server because you provide an IANA name —
  never "translate" the user's local time into UTC yourself.

## Commands

All commands are run via `Bash` tool. Each outputs JSON to stdout.

`user_id` is handled automatically — the server extracts it from your JWT
token. You never pass it as a flag.

`--chat-id` is always required — pass the UUID of the current chat. The
server also reads chat_id from JWT as the source of truth, but the body
must not be empty.

### Create a scheduled job

```bash
higgsfieldcli cron create \
  --chat-id="<UUID of this chat>" \
  --title="Daily cat memes" \
  --prompt="Send me a funny cat picture" \
  --cron="0 8 * * *" \
  --timezone="America/New_York"
```

With an anchored start (`start_at`):
```bash
higgsfieldcli cron create \
  --chat-id="<UUID of this chat>" \
  --title="Hourly standup nudge" \
  --prompt="Drop your blocker for the day in this chat." \
  --cron="35 * * * *" \
  --timezone="Europe/London" \
  --start-at="2026-04-21T09:35:00+01:00"
```

If the user attached files, include their URLs in `--prompt`:
```bash
--prompt="Here is your daily wallpaper: https://cdn.higgsfield.ai/abc123.png"
```

Output on success:
```json
{"id":"...","chat_id":"...","status":"active","next_run_at":"2026-04-17T13:00:00Z",...}
```

Tell the user when the first firing will happen (use `next_run_at`,
convert to the user's timezone for display).

On error: the output is `{"error":"..."}`. Read the error, explain in
the user's language, offer a fix.

### List jobs for this chat

```bash
higgsfieldcli cron list --chat-id="<this chat UUID>"
```


Output: `{"jobs":[...]}`. Use this to answer "what scheduled jobs are
active in this chat?" or to look up an ID before editing/cancelling.

### Get a single job

```bash
higgsfieldcli cron get --id="<job UUID>"
```

### Edit a job (partial update)

```bash
higgsfieldcli cron patch --id="<job UUID>" --prompt="Updated text"
# Optional flags: --title, --cron, --timezone
# Only pass flags you want to change
```

When `--cron` or `--timezone` changes, the server recomputes `next_run_at`.
When only other fields change, the existing schedule is kept.

### Cancel a job

```bash
higgsfieldcli cron delete --id="<job UUID>"
```

Output: `{"status":"deleted"}`. Idempotent — safe to call again.

### Pause / resume

```bash
higgsfieldcli cron pause --id="<job UUID>"
higgsfieldcli cron resume --id="<job UUID>"
```

Useful when the user says "pause the reminders for a week". Idempotent.

### Trigger (manual, for testing)

```bash
higgsfieldcli cron trigger --id="<job UUID>"
```

Immediately queues the job for delivery, bypassing the scheduler. Does NOT
change the regular schedule. Use when asked to "send the reminder now" or
for testing.

## Error handling

On error, the CLI outputs `{"error":"..."}` to stderr and exits with
non-zero code. Map common errors for the user:

| Error contains                               | User-friendly explanation                                    |
|----------------------------------------------|--------------------------------------------------------------|
| `invalid cron expression`                    | "The schedule I came up with wasn't valid. Let me try again." |
| `invalid timezone`                           | "That timezone name isn't recognized. Do you mean X?"         |
| `schedule interval must be at least 1 hour`  | "This service supports minimum 1-hour intervals. Want hourly?"|
| `chat already has the maximum number`        | "You already have 10 scheduled tasks in this chat — that's the limit. Cancel one first?" |
| `required field is empty`                    | Ask the user for that field specifically.                    |
| `start_at must be in the future`             | Your computed start instant is past (often: timezone math slipped, or you picked "this Monday" when it's already past). Recompute and retry. |
| `CRON_BASE_URL environment variable is required` | Internal error — the CLI isn't configured. Not user-facing. |

## Per-chat limit

Each chat can have at most **10 active (or paused) scheduled jobs**. Deleted
jobs don't count. If the user tries to create an 11th, offer to list existing
jobs and help cancel ones they don't need.

## Reference flow — example dialogs

### Example 1 — daily, no start anchor

```
User: "Remind me every morning at 7:30 to read."
Agent:
  1. Parse cadence: cron="30 7 * * *", title="Morning reading".
  2. Normalize prompt: raw "Remind me every morning at 7:30 to read" →
     final "Time to read! Open your current book and read 10 pages."
     (imperative, self-contained).
  3. Timezone check — $HF_USER_TIMEZONE is "Europe/London". Use it.
  4. Confirm widget:
     ┌─────────────────────────────────────┐
     │ New schedule                        │
     │                                     │
     │ Title:  Morning reading             │
     │ Text:   "Time to read! Open your    │
     │          current book and read      │
     │          10 pages."                 │
     │ When:   Every day at 07:30          │
     │          (Europe/London)            │
     │ First:  Tomorrow 07:30              │
     │                                     │
     │ [Cancel]     [Confirm]              │
     └─────────────────────────────────────┘
  5. On Confirm:
     Bash("higgsfieldcli cron create --chat-id='<this chat UUID>' --title='Morning reading' --prompt='Time to read! Open your current book and read 10 pages.' --cron='30 7 * * *' --timezone='Europe/London'")
  6. "Done! The first reminder will arrive tomorrow at 07:30."
```

### Example 2 — anchored start via `start_at`

```
User: "Every hour starting Monday at 9:35, check the deploy status."
(Today is Thursday 2026-04-17.)

Agent:
  1. Parse cadence + anchor:
     cron="35 * * * *"        (hourly at :35 so subsequent firings are 10:35, 11:35…)
     start_at="2026-04-21T09:35:00-04:00"   (next Monday 09:35 New York)
     title="Deploy status check"
  2. Normalize prompt: "Check the current deploy status and list any red checks."
  3. Timezone: $HF_USER_TIMEZONE is "America/New_York". Use it.
  4. Confirm widget shows:
     Text:   "Check the current deploy status and list any red checks."
     When:   Every hour at :35
             (America/New_York)
     First:  Mon 2026-04-21 09:35
  5. On Confirm:
     Bash("higgsfieldcli cron create --chat-id='<UUID>' --title='Deploy status check' --prompt='Check the current deploy status and list any red checks.' --cron='35 * * * *' --timezone='America/New_York' --start-at='2026-04-21T09:35:00-04:00'")
  6. "Done. First check runs Monday 2026-04-21 at 09:35, then every hour."
```

## Self-checks before running the command

Run these mental checks on every generated payload:

1. Is `cron_expression` exactly 5 whitespace-separated fields?
2. Does **at least one** of DOM / DOW fields equal `*`? (Never both specific.)
3. Is `timezone` an IANA name (contains `/` like `Europe/London`, or is `UTC`)?
4. Will two consecutive firings be ≥ 1 hour apart?
5. Are `title` and `prompt` non-empty and under reasonable length (title ≤ 255, prompt ≤ 4000)?
6. Is `prompt` the **normalized** version (not the user's raw text), and did the user confirm it in the widget?
7. If user attached files — are their URLs included in the `--prompt` text?
8. If `--start-at` is passed:
   - Is it RFC3339 with a timezone offset (e.g. `-04:00`, not `Z` unless UTC)?
   - Is it strictly in the future relative to now?
   - Does its "minute" component match the minute field of `cron_expression`?
     (Mismatch = first firing at start_at, second firing at a different
     minute-of-hour — usually a cron-construction bug.)

If any check fails, fix locally — don't send a command you know will fail.
