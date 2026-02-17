# Playwright CLI Evaluation — February 2026

**Date:** 2026-02-13
**Author:** Claude Code (Opus 4.6) + Human
**Test Target:** fwaptile-wordle (localhost:3011)
**Environment:** WSL2, Node 22.16.0, Chromium from `~/.cache/ms-playwright/`

---

## Test Environment

| Component | Version / Detail |
|-----------|-----------------|
| OS | WSL2 (Linux 6.6.87.1-microsoft-standard-WSL2) |
| Node.js | 22.16.0 |
| Playwright CLI | `@playwright/cli@latest` (installed 2026-02-13) |
| Playwright MCP | `@playwright/mcp@latest` (via .mcp.json) |
| Browser | Chrome (from `~/.cache/ms-playwright/`) |
| Test app | fwaptile-wordle — Express + WebSocket Wordle game |
| App URL | `http://localhost:3011` |

---

## Installation Experience

### Playwright CLI

```bash
npm install -g @playwright/cli@latest
# added 4 packages in 2s
```

**Time to install:** ~2 seconds. Minimal footprint (4 packages).

**Workspace init:**
```bash
cd ~/repos/your-project
playwright-cli install
# ✅ Workspace initialized at `/home/user/repos/your-project`.
# ✅ Found chrome, will use it as the default browser.
```

**Finding:** `playwright-cli install` does NOT install a SKILL.md into `.claude/skills/`. It initializes the workspace and detects the browser. The plan's assumption that it copies skill files was incorrect — the CLI works through the Bash tool, not Claude Code's skill system.

### Key Setup Differences

| Aspect | CLI | MCP |
|--------|-----|-----|
| Install | `npm install -g @playwright/cli` (2s) | Already configured in `.mcp.json` |
| Config | None needed (workspace init) | `.mcp.json` with args/flags |
| Browser | Auto-detects installed browsers | Auto-detects via npx |
| Skills | No SKILL.md — uses Bash tool | 28+ tool definitions loaded into context |

---

## Test Results (CLI)

### Test 1: Basic Navigation + Snapshot

```bash
playwright-cli open http://localhost:3011
```

**Result:** SUCCESS

Output (9 lines):
```
### Browser `default` opened with pid 1136815.
- default:
  - browser-type: chrome
  - user-data-dir: <in-memory>
  - headed: false
---
### Ran Playwright code
await page.goto('http://localhost:3011');
### Page
- Page URL: http://localhost:3011/
- Page Title: Wordle Battle - Fwaptile
- Console: 1 errors, 1 warnings
### Snapshot
- [Snapshot](.playwright-cli/page-2026-02-13T21-57-44-192Z.yml)
```

**Key finding:** Snapshot saved to `.playwright-cli/` directory as a YAML file. Only a file reference returned in the tool output. The actual snapshot (37 lines, 1,647 bytes) stays on disk and never enters the conversation context unless explicitly read.

**Screenshot:**
```bash
playwright-cli screenshot --filename wordle-home.png
```
**Result:** SUCCESS — 69KB PNG saved, file reference returned (8 lines output).

**WSL2 note:** `--no-sandbox` flag does NOT exist on the CLI. Running `playwright-cli open http://localhost:3011 --no-sandbox` errors with "unknown '--sandbox' option". The CLI handles sandboxing internally — no flag needed. This is a positive difference from MCP which requires `--no-sandbox` in WSL2.

### Test 2: Interaction (Click)

```bash
playwright-cli click e27    # Solo Practice button
```

**Result:** SUCCESS

Output (5 lines — snapshot saved to file, not inline):
```
### Ran Playwright code
await page.getByTestId('solo-practice').click();
### Page
- Page URL: http://localhost:3011/
- Page Title: Wordle Battle - Fwaptile
### Snapshot
- [Snapshot](.playwright-cli/page-2026-02-13T21-58-20-553Z.yml)
```

**Finding:** Element refs from the snapshot work reliably. The CLI resolves `e27` to `getByTestId('solo-practice')` — same selector strategy as MCP.

### Test 3: Form Input (Type + Submit)

```bash
playwright-cli type "CRANE"
playwright-cli press Enter
```

**Result:** SUCCESS — both commands worked. `type` uses `keyboard.type()` which works for non-input elements (game keyboard). 2 commands total for typing + submitting.

**Snapshot after submit** showed CRANE on the board (C, R, A, N, E in row 1) with `guessResult` in console confirming acceptance.

### Test 4: Multi-Page Flow

Full flow: home → click Solo Practice → click Start Game → wait for countdown → type + submit guess

| Step | Command | Result |
|------|---------|--------|
| Navigate | `playwright-cli open http://localhost:3011` | SUCCESS |
| View state | `playwright-cli snapshot` | File saved (37 lines) |
| Click | `playwright-cli click e27` | Solo Practice opened |
| Click | `playwright-cli click e85` | Game starting (countdown) |
| Wait | `sleep 4 && playwright-cli snapshot` | Game board visible |
| Type | `playwright-cli type "CRANE"` | Letters entered |
| Submit | `playwright-cli press Enter` | Guess accepted |

**Total commands:** 7 CLI commands for the full flow.

### Test 5: Console + Network Inspection

**Console:**
```bash
playwright-cli console
```
**Result:** File reference returned (3 lines output). Full console log (116 lines, 13,546 bytes) saved to `.playwright-cli/console-*.log`.

**Network:**
```bash
playwright-cli network
```
**Result:** File reference returned (3 lines output). Network log (558 bytes) saved to `.playwright-cli/network-*.log`.

**Finding:** Console and network output saved to files, not dumped into conversation. This is the biggest token savings vs MCP — a chatty app with 1-second timer syncs generated 116 console lines that stayed on disk.

### Test 6: Close

```bash
playwright-cli close
```
**Result:** SUCCESS — `Browser 'default' closed` (1 line).

---

## Comparison: CLI vs MCP

### Same Tasks Side-by-Side

#### Navigate + Snapshot

| Aspect | CLI | MCP |
|--------|-----|-----|
| Command | `playwright-cli open <url>` | `browser_navigate` tool |
| Snapshot delivery | File reference (3 lines) | Full YAML inline (~45 lines) |
| Console events | Not shown | ~5 truncated event lines appended |
| Total output | ~12 lines | ~50 lines |

#### Click

| Aspect | CLI | MCP |
|--------|-----|-----|
| Command | `playwright-cli click e27` | `browser_click` with ref + element params |
| Snapshot delivery | File reference | Full diff snapshot inline (~50 lines) |
| MCP advantage | — | Diff markers (`<changed>`, `[unchanged]`) reduce snapshot size |
| Total output | ~5 lines | ~55 lines |

#### Type a Word (CRANE = 5 chars + Enter)

| Aspect | CLI | MCP |
|--------|-----|-----|
| Commands | 2 (`type "CRANE"` + `press Enter`) | 7 (`browser_type` failed, then 5x `press_key` + 1x `press_key Enter`) |
| Notes | `type` uses `keyboard.type()` — works on any focused element | `browser_type` uses `fill()` — fails on non-input elements. Must fall back to `press_key` per character |
| Output per command | ~5 lines | ~20 lines (includes event stream) |
| Total output | ~10 lines | ~140 lines |

**CLI wins decisively here.** MCP's `browser_type` tool uses `locator.fill()` which only works on `<input>`, `<textarea>`, `<select>`, or `[contenteditable]` elements. For a game keyboard that uses `keydown` events, you must use `browser_press_key` once per character — 6 tool calls instead of CLI's 1 command.

#### Console Messages

| Aspect | CLI | MCP |
|--------|-----|-----|
| Command | `playwright-cli console` | `browser_console_messages` tool |
| Output | File ref (3 lines) | All 92 messages inline (~100 lines) |
| Data access | Read file if needed | Always in conversation |
| Token cost | ~12 tokens | ~1,200+ tokens |

#### Network Requests

| Aspect | CLI | MCP |
|--------|-----|-----|
| Command | `playwright-cli network` | `browser_network_requests` tool |
| Output | File ref (3 lines) | 4 requests + events inline (~15 lines) |
| Token cost | ~12 tokens | ~100 tokens |

### Summary Comparison Table

| Aspect | CLI | MCP | Winner |
|--------|-----|-----|--------|
| **Snapshot delivery** | File on disk (read on demand) | Inline in conversation | **CLI** (token savings) |
| **Commands for "type CRANE + Enter"** | 2 | 7 (type fails, press_key per char) | **CLI** (5x fewer) |
| **Console output** | File ref (3 lines) | 92 messages inline (~100 lines) | **CLI** (33x fewer tokens) |
| **Network output** | File ref (3 lines) | Inline (~15 lines) | **CLI** (5x fewer tokens) |
| **Snapshot diff support** | No (full snapshot each time) | Yes (`<changed>`, `[unchanged]` markers) | **MCP** |
| **WSL2 sandbox handling** | Automatic (no flag needed) | Requires `--no-sandbox` in config | **CLI** |
| **Setup complexity** | `npm i -g` + `install` | `.mcp.json` config (already done) | **Tie** |
| **Interaction reliability** | Refs work, click/type reliable | Refs work, click reliable, type has limitations | **CLI** |
| **Structured output** | Text + file refs | Structured tool results | **MCP** (for programmatic use) |
| **Error messages** | Clear shell errors | Structured error objects | **Tie** |
| **Browser management** | `close` / `kill-all` | Managed by MCP server | **Tie** |

---

## Token Usage Comparison

### CLI Session (Navigate → Click → Start Game → Type CRANE → Console → Network → Close)

| Step | Tool Calls | Output Lines | Est. Tokens |
|------|-----------|-------------|-------------|
| open | 1 | 12 | ~50 |
| snapshot (read file) | 1 + 1 Read | 3 + 37 | ~160 |
| click Solo Practice | 1 | 5 | ~25 |
| read snapshot | 1 Read | 50 | ~200 |
| click Start Game | 1 | 5 | ~25 |
| wait + snapshot | 1 | 3 | ~15 |
| read snapshot | 1 Read | 36 | ~150 |
| type CRANE | 1 | 5 | ~25 |
| press Enter | 1 | 5 | ~25 |
| read snapshot | 1 Read | 43 | ~180 |
| console | 1 | 3 | ~15 |
| network | 1 | 3 | ~15 |
| close | 1 | 1 | ~5 |
| **Total** | **13** | **211** | **~890** |

*Note: If you read ALL snapshot/console files, add ~500 more tokens. The point is you choose which to read.*

### MCP Session (Same Tasks)

| Step | Tool Calls | Output Lines | Est. Tokens |
|------|-----------|-------------|-------------|
| navigate | 1 | ~50 | ~350 |
| click Solo Practice | 1 | ~55 | ~380 |
| click Start Game | 1 | ~30 | ~200 |
| wait_for 4s | 1 | ~50 | ~350 |
| press_key c | 1 | ~20 | ~140 |
| press_key r | 1 | ~20 | ~140 |
| press_key a | 1 | ~20 | ~140 |
| press_key n | 1 | ~12 | ~80 |
| press_key e | 1 | ~12 | ~80 |
| press_key Enter | 1 | ~20 | ~140 |
| console_messages | 1 | ~100 | ~1,200 |
| network_requests | 1 | ~15 | ~100 |
| close | 1 | ~5 | ~30 |
| **Total** | **13** | **~409** | **~3,330** |

### Token Ratio

| Metric | CLI | MCP | Ratio |
|--------|-----|-----|-------|
| Estimated tokens (output) | ~890 | ~3,330 | **3.7x** |
| With selective file reads | ~1,400 | ~3,330 | **2.4x** |
| Tool calls | 13 (+ 4 Reads) | 13 | Equal |
| Lines returned to context | 211 | ~409 | 1.9x |

**Is it really 4x?** Close. Our measured ratio is **2.4x-3.7x** depending on how many files you read back. The 4x claim holds for scenarios where you don't need to read every snapshot — which is realistic in practice (you only read the ones where something unexpected happened).

The savings come from two mechanisms:
1. **Lazy loading:** Snapshots, console, network stay on disk. Only read what you need.
2. **No event stream:** MCP appends console events to every tool response. CLI doesn't.

---

## Findings and Gotchas

### CLI Positives
1. **No `--no-sandbox` needed** — handles WSL2 sandboxing internally
2. **`type` command uses `keyboard.type()`** — works for game keyboards, not just form inputs
3. **File-based output** — snapshots, console, network saved to `.playwright-cli/` dir
4. **Clean session management** — `open`, `close`, `list`, `kill-all` commands
5. **Storage commands** — cookies, localStorage, sessionStorage management built in
6. **Route mocking** — `route` command for network interception via CLI
7. **Tracing/video** — `tracing-start/stop`, `video-start/stop` available

### CLI Negatives
1. **No snapshot diffing** — full snapshot every time (MCP marks `<changed>`/`[unchanged]`)
2. **File management overhead** — `.playwright-cli/` directory accumulates files
3. **No `--no-sandbox` flag** — error message is confusing ("unknown '--sandbox' option")
4. **No skill file** — `playwright-cli install` doesn't create a SKILL.md for Claude Code
5. **Snapshot requires explicit read** — extra tool call to see what's on the page

### MCP Positives
1. **Snapshot diffing** — `<changed>` and `[unchanged]` markers reduce redundant data
2. **Structured tool definitions** — Claude knows exactly what parameters each tool accepts
3. **No file management** — everything inline, no cleanup needed
4. **Immediate visibility** — snapshots are always in context (no extra read step)

### MCP Negatives
1. **`browser_type` uses `fill()`** — fails on non-input elements (must fall back to `press_key`)
2. **Event stream noise** — console events appended to every response (timerSync spam)
3. **Console dump** — `browser_console_messages` returns ALL messages inline (92 lines in our test)
4. **Higher token cost** — ~3.3K tokens vs CLI's ~0.9K for the same workflow
5. **Requires `--no-sandbox`** in WSL2 config

### WSL2-Specific Notes
- Both CLI and MCP work fine in WSL2
- CLI auto-handles sandboxing; MCP requires `--no-sandbox` flag
- Headless mode is default for both (no display server needed)
- Chromium from `~/.cache/ms-playwright/` works for both

---

## Verdict

### When to Use CLI

- **CI/CD pipelines** where token cost matters
- **Batch automation** with many sequential tasks
- **Chatty apps** with high console output (game timers, WebSocket messages)
- **Simple navigation + screenshot** workflows
- **When you need `keyboard.type()`** instead of `fill()`

### When to Use MCP

- **Interactive exploration** where you need to see every page state
- **First-time debugging** where snapshot diffing helps spot changes
- **Form-heavy apps** where `browser_fill_form` is useful
- **When working in Claude Code** where MCP tools are already configured

### Recommendation: **Adopt CLI for targeted use cases, keep MCP as default**

The CLI delivers real token savings (2.4x-3.7x) but isn't a wholesale MCP replacement. The sweet spot:

1. **Keep MCP as default** for interactive development and debugging
2. **Use CLI for CI/CD** where token cost scales with volume
3. **Use CLI for chatty apps** where console/network output would blow up MCP context
4. **Use CLI when typing into non-form elements** (games, rich editors, custom inputs)

The "4x token savings" claim is **approximately correct** but depends on usage pattern. Selective file reading is the key — if you read every file, savings drop to ~2.4x.

---

## Raw Command Outputs

### CLI Snapshot File Sizes

| File | Lines | Bytes |
|------|-------|-------|
| Home page snapshot | 37 | 1,647 |
| Solo Practice config | 49 | 2,063 |
| Game starting (countdown) | 50 | 2,099 |
| Game board (keyboard) | 36 | 1,574 |
| After CRANE guess | 43 | 1,837 |
| **Total snapshots** | **215** | **9,220** |
| Console log (full session) | 116 | 13,546 |
| Network log | 4 | 558 |

### CLI .playwright-cli/ Directory

```
.playwright-cli/
├── console-*.log          # Console messages (per snapshot or explicit)
├── network-*.log          # Network requests
└── page-*.yml             # Accessibility snapshots (YAML)
```

Files are timestamped. No auto-cleanup — accumulates over sessions.

### MCP Inline Sizes (Estimated)

| Response | Approx Lines | Approx Tokens |
|----------|-------------|---------------|
| navigate (with snapshot) | 50 | 350 |
| click (with diff snapshot) | 55 | 380 |
| press_key (with events) | 20 | 140 |
| console_messages (all) | 100 | 1,200 |
| network_requests | 15 | 100 |

---

## See Also

- [BROWSER_AUTOMATION_LANDSCAPE_2026.md](./BROWSER_AUTOMATION_LANDSCAPE_2026.md) — Full landscape comparison (CLI is Approach 2)
- [Playwright MCP Guide](../../docs/mcp/playwright/README.md) — The MCP alternative evaluated here
- [COST_OPTIMIZATION_GUIDE.md](./COST_OPTIMIZATION_GUIDE.md) — Cost context and optimization strategies

---

*Last Updated: 2026-02-13*
