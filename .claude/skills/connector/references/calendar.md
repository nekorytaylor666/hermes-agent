
# Google Calendar (via Higgsfield MCP proxy)

Google Calendar events, calendars, busy times, attendees. Exposes 15 tool(s).

## Prerequisites

Auth is wired automatically. Invoke via:

```bash
./bin/mcp2cli @calendar <command> [flags]
```

## Core workflow

```bash
./bin/mcp2cli @calendar --list                    # all 15 tools
./bin/mcp2cli @calendar google-calendar-update-following-instances --help   # inspect one
./bin/mcp2cli @calendar google-calendar-update-following-instances --flag value   # invoke
```

## Common patterns

- **Pretty JSON output**: `./bin/mcp2cli @calendar --pretty <cmd>` — `--pretty` goes AFTER `@calendar`, not before (parser requires `@<slug>` as first arg)
- **Truncate large arrays**: `./bin/mcp2cli @calendar --head N <cmd>` — `--head N` goes AFTER `@calendar`
- **JSON input via stdin**: pipe JSON to `... <cmd> --stdin` instead of typing every flag
- **JSON-valued flags** (filters, bodies, options): pass as single-quoted JSON strings

## Command reference

All 15 commands with their flags. `--stdin` (read JSON args from stdin) is available on every command and omitted from tables for brevity.

### `google-calendar-update-following-instances`

Update all instances of a recurring event following a specific

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |
| `--recurring-event-id RECURRING_EVENT_ID` | The ID of the recurring event You can use the "retrieve_options" tool using these parameters to get the values. key: ... |
| `--instance-id INSTANCE_ID` | The instance where the split will occur. All instances from this point forward will be updated with your changes, whi... |
| `--summary SUMMARY` | Enter a new title for all following instances |
| `--event-start-date EVENT_START_DATE` | For all-day events, enter the Event day in the format `yyyy-mm-dd`. For events with time, format according to [RFC333... |
| `--event-end-date EVENT_END_DATE` | For all-day events, enter the Event day in the format `yyyy-mm-dd`. For events with time, format according to [RFC333... |
| `--location LOCATION` | Specify a new location for all following instances |
| `--description DESCRIPTION` | Enter a new description for all following instances |
| `--attendees ATTENDEES` | Enter either an array or a comma separated list of email addresses of attendees |
| `--repeat-frequency {DAILY,WEEKLY,MONTHLY,YEARLY}` | Optionally change the repeat frequency for following instances |
| `--color-id COLOR_ID` | The color assigned to this event on your calendar. You can only select a color from the list of event colors provided... |
| `--time-zone TIME_ZONE` | Time zone used in the response. Optional. The default is the time zone of the calendar. You can use the "retrieve_opt... |
| `--send-updates {all,externalOnly,none}` | Configure whether to send notifications about the event |

### `google-calendar-update-event`

Update an event from Google Calendar. [See the

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |
| `--event-id EVENT_ID` | Select an event from Google Calendar. You can use the "retrieve_options" tool using these parameters to get the value... |
| `--summary SUMMARY` | Enter a title for the event, (e.g., `My event`) |
| `--event-start-date EVENT_START_DATE` | For all-day events, enter the Event day in the format `yyyy-mm-dd`. For events with time, format according to [RFC333... |
| `--event-end-date EVENT_END_DATE` | For all-day events, enter the Event day in the format `yyyy-mm-dd`. For events with time, format according to [RFC333... |
| `--location LOCATION` | Specify the location of the event |
| `--description DESCRIPTION` | Enter a description for the event |
| `--attendees ATTENDEES` | Enter either an array or a comma separated list of email addresses of attendees |
| `--repeat-frequency {DAILY,WEEKLY,MONTHLY,YEARLY}` | Select a frequency to make this event repeating |
| `--repeat-interval REPEAT_INTERVAL` | Enter 1 to "repeat every day", enter 2 to "repeat every other day", etc. Defaults to 1. |
| `--repeat-specific-days REPEAT_SPECIFIC_DAYS` | The event will repeat on these days of the week. Repeat Frequency must be `WEEKLY`. (JSON array) |
| `--repeat-until REPEAT_UNTIL` | The event will repeat only until this date, if set. Only one of `Repeat Until` or Repeat `How Many Times` may be ente... |
| `--repeat-times REPEAT_TIMES` | Limit the number of times this event will occur. Only one of `Repeat Until` or Repeat `How Many Times` may be entered. |
| `--time-zone TIME_ZONE` | Time zone used in the response. Optional. The default is the time zone of the calendar. You can use the "retrieve_opt... |
| `--send-updates {all,externalOnly,none}` | Configure whether to send notifications about the event |

### `google-calendar-update-event-instance`

Update a specific instance of a recurring event. Changes apply only

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |
| `--recurring-event-id RECURRING_EVENT_ID` | The ID of the recurring event You can use the "retrieve_options" tool using these parameters to get the values. key: ... |
| `--instance-id INSTANCE_ID` | The ID of the specific instance to update. Use List Event Instances action to get instance IDs. You can use the "retr... |
| `--summary SUMMARY` | Enter a new title for this instance |
| `--event-start-date EVENT_START_DATE` | For all-day events, enter the Event day in the format `yyyy-mm-dd`. For events with time, format according to [RFC333... |
| `--event-end-date EVENT_END_DATE` | For all-day events, enter the Event day in the format `yyyy-mm-dd`. For events with time, format according to [RFC333... |
| `--location LOCATION` | Specify a new location for this instance |
| `--description DESCRIPTION` | Enter a new description for this instance |
| `--attendees ATTENDEES` | Enter either an array or a comma separated list of email addresses of attendees |
| `--color-id COLOR_ID` | The color assigned to this event on your calendar. You can only select a color from the list of event colors provided... |
| `--time-zone TIME_ZONE` | Time zone used in the response. Optional. The default is the time zone of the calendar. You can use the "retrieve_opt... |
| `--send-updates {all,externalOnly,none}` | Configure whether to send notifications about the event |

### `google-calendar-quick-add-event`

Create a quick event to the Google Calendar. [See the

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |
| `--text TEXT` | Write a plain text description of event, and Google will parse this string to create the event. eg. 'Meet with Michae... |
| `--attendees ATTENDEES` | Enter either an array or a comma separated list of email addresses of attendees |

### `google-calendar-query-free-busy-calendars`

Retrieve free/busy calendar details from Google Calendar. [See the

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Select calendars to retrieve free/busy details You can use the "retrieve_options" tool using these parameters to get ... |
| `--time-min TIME_MIN` | Lower bound (exclusive) for an event's time to filter by. Must be an RFC3339 timestamp with mandatory time zone offse... |
| `--time-max TIME_MAX` | Upper bound (exclusive) for an event's time to filter by. Must be an RFC3339 timestamp with mandatory time zone offse... |
| `--time-zone TIME_ZONE` | Specify the preferred time zone to be used on the response You can use the "retrieve_options" tool using these parame... |

### `google-calendar-list-events`

Retrieve a list of event from the Google Calendar. [See the

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |
| `--i-cal-uid I_CAL_UID` | Specifies event ID in the iCalendar format to be included in the response. Optional. |
| `--max-attendees MAX_ATTENDEES` | The maximum number of attendees to include in the response. If there are more than the specified number of attendees,... |
| `--max-results MAX_RESULTS` | Maximum number of events returned on one result page. The number of events in the resulting page may be less than thi... |
| `--order-by {startTime,updated}` | The order of the events returned in the result. Optional. The default is an unspecified, stable order. Must set Singl... |
| `--private-extended-property PRIVATE_EXTENDED_PROPERTY` | Extended properties constraint specified as propertyName=value. Matches only private properties. This parameter might... |
| `--q Q` | Free text search terms to find events that match these terms in any field, except for extended properties. Optional. |
| `--shared-extended-property SHARED_EXTENDED_PROPERTY` | Extended properties constraint specified as propertyName=value. Matches only shared properties. This parameter might ... |
| `--show-deleted` | Whether to include deleted events (with status equals "cancelled") in the result. Cancelled instances of recurring ev... |
| `--show-hidden-invitations` | Whether to include hidden invitations in the result. Optional. The default is False. |
| `--single-events` | Whether to expand recurring events into instances and only return single one-off events and instances of recurring ev... |
| `--time-max TIME_MAX` | Upper bound (exclusive) for an event's time to filter by. Must be an RFC3339 timestamp with mandatory time zone offse... |
| `--time-min TIME_MIN` | Lower bound (exclusive) for an event's time to filter by. Must be an RFC3339 timestamp with mandatory time zone offse... |
| `--time-zone TIME_ZONE` | Time zone used in the response. Optional. The default is the time zone of the calendar. You can use the "retrieve_opt... |
| `--updated-min UPDATED_MIN` | Lower bound for an event's last modification time (as a RFC3339 timestamp) to filter by. When specified, entries dele... |
| `--event-types EVENT_TYPES` | Filter events by event type (JSON array) |

### `google-calendar-list-event-instances`

Retrieve instances of a recurring event. [See the

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |
| `--event-id EVENT_ID` | The recurring event identifier. Select an event from Google Calendar. You can use the "retrieve_options" tool using t... |
| `--max-attendees MAX_ATTENDEES` | The maximum number of attendees to include in the response. If there are more than the specified number of attendees,... |
| `--max-results MAX_RESULTS` | Maximum number of events returned on one result page. The number of events in the resulting page may be less than thi... |
| `--show-deleted` | Whether to include deleted events (with status equals "cancelled") in the result. Cancelled instances of recurring ev... |
| `--time-max TIME_MAX` | Upper bound (exclusive) for an event's time to filter by. Must be an RFC3339 timestamp with mandatory time zone offse... |
| `--time-min TIME_MIN` | Lower bound (exclusive) for an event's time to filter by. Must be an RFC3339 timestamp with mandatory time zone offse... |
| `--time-zone TIME_ZONE` | Time zone used in the response. Optional. The default is the time zone of the calendar. You can use the "retrieve_opt... |

### `google-calendar-list-calendars`

Retrieve a list of calendars from Google Calendar. [See the

_No flags._

### `google-calendar-get-event`

Retrieve event details from Google Calendar. [See the

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |
| `--event-id EVENT_ID` | Select an event from Google Calendar. You can use the "retrieve_options" tool using these parameters to get the value... |

### `google-calendar-get-date-time`

Get current date and time for use in Google Calendar actions. Useful

_No flags._

### `google-calendar-get-current-user`

Retrieve information about the authenticated Google Calendar account,

_No flags._

### `google-calendar-get-calendar`

Retrieve calendar details of a Google Calendar. [See the

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |

### `google-calendar-delete-event`

Delete an event from a Google Calendar. [See the

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |
| `--event-id EVENT_ID` | Select an event from Google Calendar. You can use the "retrieve_options" tool using these parameters to get the value... |

### `google-calendar-create-event`

Create an event in a Google Calendar. [See the

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |
| `--summary SUMMARY` | Enter a title for the event, (e.g., `My event`) |
| `--event-start-date EVENT_START_DATE` | For all-day events, enter the date in the format `yyyy-mm-dd` (e.g., `2025-01-15`). For events with time, format acco... |
| `--event-end-date EVENT_END_DATE` | For all-day events, enter the date in the format `yyyy-mm-dd` (e.g., `2025-01-15`). For events with time, format acco... |
| `--location LOCATION` | Specify the location of the event |
| `--description DESCRIPTION` | Enter a description for the event |
| `--attendees ATTENDEES` | An array of email addresses (e.g., `["alice@example.com", "bob@example.com"]`) (JSON array) |
| `--color-id COLOR_ID` | The color assigned to this event on your calendar. You can only select a color from the list of event colors provided... |
| `--time-zone TIME_ZONE` | Time zone used in the response. Optional. The default is the time zone of the calendar. You can use the "retrieve_opt... |
| `--send-updates {all,externalOnly,none}` | Configure whether to send notifications about the event |
| `--create-meet-room` | Whether to create a Google Meet room for this event. |
| `--visibility {default,public,private,confidential}` | Visibility of the event |
| `--repeat-frequency {DAILY,WEEKLY,MONTHLY,YEARLY}` | Select a frequency to make this event repeating |
| `--repeat-interval REPEAT_INTERVAL` | Enter 1 to "repeat every day", enter 2 to "repeat every other day", etc. Defaults to 1. |
| `--repeat-specific-days REPEAT_SPECIFIC_DAYS` | The event will repeat on these days of the week. Repeat Frequency must be `WEEKLY`. (JSON array) |
| `--repeat-until REPEAT_UNTIL` | The event will repeat only until this date, if set. Only one of `Repeat Until` or Repeat `How Many Times` may be ente... |
| `--repeat-times REPEAT_TIMES` | Limit the number of times this event will occur. Only one of `Repeat Until` or Repeat `How Many Times` may be entered. |

### `google-calendar-add-attendees-to-event`

Add attendees to an existing event. [See the

| Flag | Description |
|---|---|
| `--calendar-id CALENDAR_ID` | Optionally select the calendar, defaults to the primary calendar for the logged-in user You can use the "retrieve_opt... |
| `--event-id EVENT_ID` | Select an event from Google Calendar. You can use the "retrieve_options" tool using these parameters to get the value... |
| `--attendees ATTENDEES` | Enter either an array or a comma separated list of email addresses of attendees |
| `--send-updates {all,externalOnly,none}` | Configure whether to send notifications about the event |

## Security

- The JWT grants broad Higgsfield proxy access — rotate on compromise.

## Troubleshooting

- **`no baked tool named 'calendar'`** — re-run `make bake` from the mcp2cli project.
- **Stale schemas** — add `--refresh` before `@calendar` to bypass the 1h tool-list cache.
