import { useMemo, useRef, useState, type FormEvent } from "react";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport, type UIMessage } from "ai";
import { Send, Square, ShieldAlert } from "lucide-react";
import { H2 } from "@nous-research/ui";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

// Custom data part shapes emitted by the Python backend.  See
// hermes_cli/web_chat.py (on_status / on_approval_request).
type StatusData = { lifecycle: string; message: string };
type ApprovalData = {
  approvalId: string;
  command: string;
  description: string;
  patternKeys?: string[];
  choices?: string[];
};
type ApprovalChoice = "once" | "session" | "always" | "deny";

function getToken(): string | null {
  return typeof window !== "undefined"
    ? (window.__HERMES_SESSION_TOKEN__ ?? null)
    : null;
}

export default function ChatPage() {
  const chatId = useMemo(() => crypto.randomUUID(), []);
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement | null>(null);

  const transport = useMemo(
    () =>
      new DefaultChatTransport({
        api: "/api/chat",
        headers: (): Record<string, string> => {
          const t = getToken();
          return t ? { Authorization: `Bearer ${t}` } : {};
        },
      }),
    [],
  );

  const { messages, sendMessage, status, stop, error } = useChat({
    id: chatId,
    transport,
  });

  const isStreaming = status === "streaming" || status === "submitted";

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || isStreaming) return;
    setInput("");
    sendMessage({ text });
    // Scroll to bottom shortly after React commits the new message.
    requestAnimationFrame(() => {
      scrollRef.current?.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    });
  };

  return (
    <div className="flex h-[calc(100vh-10rem)] flex-col">
      <div className="flex items-baseline justify-between pb-3">
        <H2>Chat</H2>
        <span className="text-[0.7rem] opacity-50 tracking-[0.15em]">
          session {chatId.slice(0, 8)}
        </span>
      </div>

      <div
        ref={scrollRef}
        className={cn(
          "flex-1 overflow-y-auto",
          "border border-current/20 bg-background-base/50",
          "px-3 sm:px-5 py-4",
          "space-y-5",
        )}
      >
        {messages.length === 0 && !isStreaming && (
          <div className="opacity-50 text-sm">
            No messages yet. Send one below.
          </div>
        )}

        {messages.map((m) => (
          <MessageBlock key={m.id} message={m} />
        ))}

        {isStreaming && messages.at(-1)?.role !== "assistant" && (
          <div className="opacity-60 text-xs tracking-[0.15em] animate-pulse">
            · · ·
          </div>
        )}

        {error && (
          <div className="text-destructive text-sm border border-destructive/40 p-2">
            {String(error.message ?? error)}
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2 pt-3">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Hermes..."
          disabled={isStreaming}
          className="flex-1"
          autoFocus
        />
        {isStreaming ? (
          <Button
            type="button"
            variant="destructive"
            onClick={() => stop()}
            className="gap-2"
          >
            <Square className="h-3.5 w-3.5" />
            Stop
          </Button>
        ) : (
          <Button type="submit" disabled={!input.trim()} className="gap-2">
            <Send className="h-3.5 w-3.5" />
            Send
          </Button>
        )}
      </form>
    </div>
  );
}

function MessageBlock({ message }: { message: UIMessage }) {
  const m = message as unknown as Record<string, unknown>;
  const { id, role, parts, ...rest } = m;
  const partsArr = (parts as unknown[]) ?? [];
  return (
    <section className="border border-current/25">
      <header className="flex flex-wrap items-baseline gap-x-3 gap-y-1 px-2 py-1 bg-current/5 text-[0.7rem] font-mono">
        <span className="uppercase tracking-[0.15em] opacity-80">
          {String(role)}
        </span>
        <span className="opacity-60">id=</span>
        <code className="break-all">{String(id)}</code>
        <span className="opacity-60">parts={partsArr.length}</span>
        {Object.keys(rest).length > 0 && (
          <details className="basis-full">
            <summary className="cursor-pointer opacity-60">
              message meta ({Object.keys(rest).length})
            </summary>
            <Json value={rest} />
          </details>
        )}
      </header>
      <div className="p-2 space-y-2">
        {partsArr.length === 0 && (
          <div className="opacity-50 text-xs italic">(no parts)</div>
        )}
        {partsArr.map((part, i) => (
          <PartRenderer key={`${String(id)}-${i}`} part={part} index={i} />
        ))}
      </div>
    </section>
  );
}

function PartRenderer({ part, index }: { part: unknown; index: number }) {
  const p = (part ?? {}) as Record<string, unknown>;
  const type = String(p.type ?? "(unknown)");

  // ── Text ────────────────────────────────────────────────────────────
  if (type === "text") {
    const { type: _t, text, state, ...rest } = p;
    void _t;
    return (
      <PartFrame index={index} type={type} extras={{ state }} rest={rest}>
        <pre className="whitespace-pre-wrap text-sm font-sans">
          {String(text ?? "")}
        </pre>
      </PartFrame>
    );
  }

  // ── Reasoning — <details> accordion per spec ────────────────────────
  if (type === "reasoning") {
    const { type: _t, text, state, ...rest } = p;
    void _t;
    return (
      <PartFrame index={index} type={type} extras={{ state }} rest={rest}>
        <details>
          <summary className="cursor-pointer text-xs opacity-70">
            reasoning text ({String(text ?? "").length} chars)
          </summary>
          <pre className="whitespace-pre-wrap text-xs opacity-80 pt-1">
            {String(text ?? "")}
          </pre>
        </details>
      </PartFrame>
    );
  }

  // ── Tools + any dynamic-* part — tabs for input / output / rest ────
  if (type.startsWith("tool-") || type.startsWith("dynamic-")) {
    return <ToolPart part={p} type={type} index={index} />;
  }

  // ── data-approval — keep the approval UX actionable ─────────────────
  if (type === "data-approval") {
    const data = (p.data as ApprovalData | undefined) ?? undefined;
    const { type: _t, data: _d, ...rest } = p;
    void _t;
    void _d;
    return (
      <PartFrame index={index} type={type} rest={rest}>
        {data ? (
          <>
            <div className="text-[0.65rem] font-mono opacity-70 mb-1">
              approvalId=<code>{data.approvalId}</code>
            </div>
            <ApprovalCard data={data} />
          </>
        ) : (
          <div className="opacity-50 text-xs italic">(no data)</div>
        )}
      </PartFrame>
    );
  }

  // ── data-status ─────────────────────────────────────────────────────
  if (type === "data-status") {
    const data = (p.data as StatusData | undefined) ?? undefined;
    const { type: _t, data: _d, ...rest } = p;
    void _t;
    void _d;
    return (
      <PartFrame index={index} type={type} rest={rest}>
        {data ? (
          <div className="text-xs font-mono">
            <span className="opacity-60">lifecycle=</span>
            {data.lifecycle}
            <span className="opacity-60"> · message=</span>
            {data.message}
          </div>
        ) : (
          <div className="opacity-50 text-xs italic">(no data)</div>
        )}
      </PartFrame>
    );
  }

  // ── Any other data-* — surface `.data` + `id` prominently ───────────
  if (type.startsWith("data-")) {
    const { type: _t, data, id, ...rest } = p;
    void _t;
    const extras: Record<string, unknown> = {};
    if (id !== undefined) extras.id = id;
    return (
      <PartFrame index={index} type={type} extras={extras} rest={rest}>
        {data === undefined ? (
          <div className="opacity-50 text-xs italic">(no data payload)</div>
        ) : (
          <Json value={data} />
        )}
      </PartFrame>
    );
  }

  // ── file / source-* ─────────────────────────────────────────────────
  if (type === "file" || type.startsWith("source-")) {
    const { type: _t, ...rest } = p;
    void _t;
    return (
      <PartFrame index={index} type={type} rest={rest}>
        <Json value={rest} />
      </PartFrame>
    );
  }

  // ── Fallback: dump every field verbatim ─────────────────────────────
  const { type: _t, ...rest } = p;
  void _t;
  return (
    <PartFrame index={index} type={type} rest={rest}>
      <Json value={rest} />
    </PartFrame>
  );
}

// Wraps every part with a consistent debug header: index, type, any
// caller-supplied extras (e.g. state), and a collapsible raw-JSON dump.
function PartFrame({
  index,
  type,
  extras,
  rest,
  children,
}: {
  index: number;
  type: string;
  extras?: Record<string, unknown>;
  rest?: Record<string, unknown>;
  children: React.ReactNode;
}) {
  return (
    <div className="border border-current/20">
      <header className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5 px-2 py-1 bg-current/[.03] text-[0.7rem] font-mono">
        <span className="opacity-50">#{index}</span>
        <code className="font-semibold">{type}</code>
        {extras &&
          Object.entries(extras)
            .filter(([, v]) => v !== undefined && v !== null)
            .map(([k, v]) => (
              <span key={k}>
                <span className="opacity-60">{k}=</span>
                <code>{String(v)}</code>
              </span>
            ))}
      </header>
      <div className="p-2">{children}</div>
      {rest && Object.keys(rest).length > 0 && (
        <details className="border-t border-current/10">
          <summary className="cursor-pointer px-2 py-1 text-[0.65rem] font-mono opacity-60">
            part raw ({Object.keys(rest).length} fields)
          </summary>
          <div className="p-2 border-t border-current/10">
            <Json value={rest} />
          </div>
        </details>
      )}
    </div>
  );
}

// Tool part with input / output / rest tabs.
function ToolPart({
  part,
  type,
  index,
}: {
  part: Record<string, unknown>;
  type: string;
  index: number;
}) {
  type Tab = "input" | "output" | "rest";
  const [tab, setTab] = useState<Tab>("input");

  const toolName =
    (part.toolName as string | undefined) ??
    (type.startsWith("tool-") ? type.slice("tool-".length) : type);
  const toolCallId = part.toolCallId as string | undefined;
  const state = part.state as string | undefined;
  const input = part.input;
  const output = part.output;
  const errorText = part.errorText as string | undefined;

  const rest: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(part)) {
    if (
      k !== "type" &&
      k !== "toolName" &&
      k !== "toolCallId" &&
      k !== "state" &&
      k !== "input" &&
      k !== "output" &&
      k !== "errorText"
    ) {
      rest[k] = v;
    }
  }

  return (
    <div className="border border-current/20">
      <header className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5 px-2 py-1 bg-current/[.03] text-[0.7rem] font-mono">
        <span className="opacity-50">#{index}</span>
        <code className="font-semibold">{type}</code>
        <span>
          <span className="opacity-60">toolName=</span>
          <code>{toolName}</code>
        </span>
        {toolCallId && (
          <span>
            <span className="opacity-60">toolCallId=</span>
            <code className="break-all">{toolCallId}</code>
          </span>
        )}
        {state && (
          <span>
            <span className="opacity-60">state=</span>
            <code>{state}</code>
          </span>
        )}
      </header>
      <nav
        role="tablist"
        className="flex gap-0 border-t border-current/10 text-[0.7rem] font-mono"
      >
        {(["input", "output", "rest"] as const).map((t) => (
          <button
            key={t}
            role="tab"
            aria-selected={tab === t}
            onClick={() => setTab(t)}
            className={cn(
              "px-2 py-1 border-r border-current/10 cursor-pointer",
              tab === t ? "bg-current/10" : "opacity-60 hover:opacity-100",
            )}
          >
            {t}
          </button>
        ))}
      </nav>
      <div className="p-2 border-t border-current/10">
        {tab === "input" &&
          (input === undefined ? (
            <div className="opacity-50 text-xs italic">(no input yet)</div>
          ) : (
            <Json value={input} />
          ))}
        {tab === "output" && (
          <>
            {errorText && (
              <pre className="whitespace-pre-wrap text-xs text-destructive mb-1">
                {errorText}
              </pre>
            )}
            {output === undefined && !errorText ? (
              <div className="opacity-50 text-xs italic">(no output yet)</div>
            ) : output !== undefined ? (
              <Json value={output} />
            ) : null}
          </>
        )}
        {tab === "rest" &&
          (Object.keys(rest).length === 0 ? (
            <div className="opacity-50 text-xs italic">(no other fields)</div>
          ) : (
            <Json value={rest} />
          ))}
      </div>
    </div>
  );
}

function Json({ value }: { value: unknown }) {
  return (
    <pre className="whitespace-pre-wrap break-words text-[0.7rem] font-mono leading-snug overflow-x-auto">
      {safeStringify(value)}
    </pre>
  );
}

function safeStringify(v: unknown): string {
  if (typeof v === "string") return v;
  try {
    return JSON.stringify(v, null, 2);
  } catch {
    return String(v);
  }
}

const APPROVAL_CHOICES: Array<{
  choice: ApprovalChoice;
  label: string;
  variant: "default" | "outline" | "destructive";
}> = [
  { choice: "once", label: "Allow Once", variant: "default" },
  { choice: "session", label: "Session", variant: "outline" },
  { choice: "always", label: "Always", variant: "outline" },
  { choice: "deny", label: "Deny", variant: "destructive" },
];

function ApprovalCard({ data }: { data: ApprovalData }) {
  const [resolved, setResolved] = useState<ApprovalChoice | null>(null);
  const [pending, setPending] = useState<ApprovalChoice | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function respond(choice: ApprovalChoice) {
    if (resolved || pending) return;
    setPending(choice);
    setError(null);
    try {
      const token = getToken();
      const res = await fetch("/api/chat/approve", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ approvalId: data.approvalId, choice }),
      });
      if (!res.ok) {
        const body = await res.text();
        throw new Error(`${res.status}: ${body}`);
      }
      setResolved(choice);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setPending(null);
    }
  }

  return (
    <div className="border border-warning/50 bg-warning/5">
      <div className="flex items-center gap-2 px-2.5 py-1.5 border-b border-current/15">
        <ShieldAlert className="h-3.5 w-3.5 text-warning" />
        <span className="font-mondwest tracking-[0.1em] text-xs">
          Approval required
        </span>
        <span className="ml-auto opacity-60 text-[0.65rem]">
          {data.description}
        </span>
      </div>
      <pre className="px-2.5 py-2 overflow-x-auto text-[0.75rem] whitespace-pre-wrap break-words">
        {data.command}
      </pre>
      <div className="flex flex-wrap gap-1.5 px-2.5 py-2 border-t border-current/15">
        {APPROVAL_CHOICES.map(({ choice, label, variant }) => {
          const isResolved = resolved === choice;
          return (
            <Button
              key={choice}
              variant={isResolved ? "default" : variant}
              size="sm"
              disabled={resolved !== null || pending !== null}
              onClick={() => respond(choice)}
            >
              {pending === choice ? "…" : label}
              {isResolved && " ✓"}
            </Button>
          );
        })}
      </div>
      {resolved && (
        <div className="px-2.5 py-1 text-[0.65rem] opacity-70 uppercase tracking-[0.15em] border-t border-current/15">
          Resolved · {resolved}
        </div>
      )}
      {error && (
        <div className="px-2.5 py-1 text-destructive text-xs border-t border-current/15">
          {error}
        </div>
      )}
    </div>
  );
}
