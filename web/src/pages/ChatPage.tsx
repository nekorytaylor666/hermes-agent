import { useMemo, useRef, useState, type FormEvent } from "react";
import { useChat } from "@ai-sdk/react";
import { DefaultChatTransport, type UIMessage } from "ai";
import {
  Send,
  Square,
  Wrench,
  Brain,
  Bot,
  User,
  ShieldAlert,
} from "lucide-react";
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
  const isUser = message.role === "user";
  return (
    <div className="flex gap-3">
      <div className="shrink-0 pt-0.5 opacity-70">
        {isUser ? (
          <User className="h-4 w-4" />
        ) : (
          <Bot className="h-4 w-4" />
        )}
      </div>
      <div className="flex-1 min-w-0 space-y-2">
        <div className="text-[0.65rem] uppercase tracking-[0.15em] opacity-50">
          {isUser ? "You" : "Hermes"}
        </div>
        {message.parts.map((part, i) => (
          <PartRenderer key={`${message.id}-${i}`} part={part} />
        ))}
      </div>
    </div>
  );
}

function PartRenderer({ part }: { part: UIMessage["parts"][number] }) {
  // Text — the most common part.
  if (part.type === "text") {
    return (
      <div className="whitespace-pre-wrap leading-relaxed text-sm">
        {part.text}
      </div>
    );
  }

  // Reasoning — model's chain-of-thought, shown as a muted block.
  if (part.type === "reasoning") {
    return (
      <details className="text-xs border border-current/15 pl-2">
        <summary className="cursor-pointer py-1 flex items-center gap-1.5 opacity-60">
          <Brain className="h-3 w-3" />
          Reasoning
        </summary>
        <div className="whitespace-pre-wrap opacity-70 pt-1 pb-2">
          {part.text}
        </div>
      </details>
    );
  }

  // Custom data parts.  The backend emits `data-status` with a StatusData
  // payload for lifecycle events (retries, fallbacks, interrupts).
  if (part.type === "data-status") {
    const data = (part as { data?: StatusData }).data;
    if (!data) return null;
    return (
      <div className="text-[0.65rem] uppercase tracking-[0.15em] opacity-50">
        {data.message}
      </div>
    );
  }

  // Dangerous-command approval — the user must click Once / Session /
  // Always / Deny to resolve it before the agent can proceed.  Mirrors
  // Telegram's inline-keyboard approval flow.
  if (part.type === "data-approval") {
    const data = (part as { data?: ApprovalData }).data;
    if (!data) return null;
    return <ApprovalCard data={data} />;
  }

  // Tool parts — in AI SDK v6 the part type is `tool-<name>` or
  // `dynamic-tool` (for dynamically-registered tools).  We render both
  // through a single card.
  if (part.type.startsWith("tool-") || part.type === "dynamic-tool") {
    const tp = part as unknown as {
      type: string;
      toolName?: string;
      toolCallId?: string;
      state?: string;
      input?: unknown;
      output?: unknown;
      errorText?: string;
    };
    const name = tp.toolName ?? tp.type.replace(/^tool-/, "");
    const state = tp.state ?? "input-streaming";
    return (
      <div className="border border-current/20 text-xs">
        <div className="flex items-center gap-2 px-2 py-1 bg-current/5">
          <Wrench className="h-3 w-3" />
          <span className="font-mondwest tracking-[0.1em]">{name}</span>
          <span className="ml-auto opacity-50 text-[0.65rem] tracking-[0.15em]">
            {state}
          </span>
        </div>
        {tp.input !== undefined && (
          <pre className="px-2 py-1 overflow-x-auto text-[0.7rem] opacity-75 border-t border-current/10">
            {safeStringify(tp.input)}
          </pre>
        )}
        {tp.output !== undefined && (
          <pre className="px-2 py-1 overflow-x-auto text-[0.7rem] border-t border-current/10 max-h-64">
            {safeStringify(tp.output)}
          </pre>
        )}
        {tp.errorText && (
          <div className="px-2 py-1 text-destructive border-t border-current/10">
            {tp.errorText}
          </div>
        )}
      </div>
    );
  }

  return null;
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
