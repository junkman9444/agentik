<p align="center">
  <img src="assets/banner.png" alt="Agentik" width="100%">
</p>

# Agentik ☤
<p align="center">
  <a href="https://github.com/junkman9444/agentik">Agentik</a> — a <a href="https://sekuro.io">Sekuro</a> fork of <a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a>
</p>
<p align="center">
  <a href="https://github.com/junkman9444/agentik/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-GPLv2-green?style=for-the-badge" alt="License: GPLv2"></a>
  <a href="https://sekuro.io"><img src="https://img.shields.io/badge/Fork%20by-Sekuro-C6007E?style=for-the-badge" alt="Fork by Sekuro"></a>
  <a href="https://github.com/NousResearch/hermes-agent"><img src="https://img.shields.io/badge/Upstream-Hermes%20Agent-FFD700?style=for-the-badge" alt="Upstream: Hermes Agent"></a>
</p>

**The self-improving AI agent.** Agentik is a [Sekuro](https://sekuro.io)-branded fork of [Hermes Agent](https://github.com/NousResearch/hermes-agent) — the managed Nous Portal service layer (hosted OAuth login, billing, subscription tiers) has been removed in favor of bring-your-own-API-key providers only. It keeps the built-in learning loop from upstream — it creates skills from experience, improves them during use, nudges itself to persist knowledge, searches its own past conversations, and builds a deepening model of who you are across sessions. Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop — talk to it from Telegram while it works on a cloud VM.

Use any model you want — Anthropic, OpenAI, OpenRouter, your own endpoint, and many others. Switch with `hermes model` — no code changes, no lock-in, no managed portal.

<table>
<tr><td><b>A real terminal interface</b></td><td>Full TUI with multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output.</td></tr>
<tr><td><b>Lives where you do</b></td><td>Telegram, Discord, Slack, WhatsApp, Signal, and CLI — all from a single gateway process. Voice memo transcription, cross-platform conversation continuity.</td></tr>
<tr><td><b>A closed learning loop</b></td><td>Agent-curated memory with periodic nudges. Autonomous skill creation after complex tasks. Skills self-improve during use. FTS5 session search with LLM summarization for cross-session recall. <a href="https://github.com/plastic-labs/honcho">Honcho</a> dialectic user modeling. Compatible with the <a href="https://agentskills.io">agentskills.io</a> open standard.</td></tr>
<tr><td><b>Scheduled automations</b></td><td>Built-in cron scheduler with delivery to any platform. Daily reports, nightly backups, weekly audits — all in natural language, running unattended.</td></tr>
<tr><td><b>Delegates and parallelizes</b></td><td>Spawn isolated subagents for parallel workstreams. Write Python scripts that call tools via RPC, collapsing multi-step pipelines into zero-context-cost turns.</td></tr>
<tr><td><b>Runs anywhere, not just your laptop</b></td><td>Seven terminal backends — local, Docker, SSH, Singularity, Modal, Daytona, and Vercel Sandbox. Daytona and Modal offer serverless persistence — your agent's environment hibernates when idle and wakes on demand, costing nearly nothing between sessions. Run it on a $5 VPS or a GPU cluster.</td></tr>
<tr><td><b>Research-ready</b></td><td>Batch trajectory generation, trajectory compression for training the next generation of tool-calling models.</td></tr>
</table>

---

## Quick Install

> **Note:** This fork does not (yet) run its own install-script hosting. Clone and install with `uv`/`pip` directly until a hosted installer exists for Agentik.

### Linux, macOS, WSL2, Termux

```bash
git clone https://github.com/junkman9444/agentik.git
cd agentik
uv sync --all-extras   # or: pip install -e ".[all]"
```

### Windows (native, PowerShell)

> **Heads up:** Native Windows runs Agentik without WSL — CLI, gateway, TUI, and tools all work natively. If you'd rather use WSL2, the Linux/macOS commands above work there too. Found a bug? Please file issues on [this fork](https://github.com/junkman9444/agentik/issues).

```powershell
git clone https://github.com/junkman9444/agentik.git
cd agentik
uv sync --all-extras
```

The upstream project's installer handled bundling uv, Python 3.11, Node.js, ripgrep, ffmpeg, and a portable Git Bash automatically — this fork does not yet ship that installer. Install those dependencies manually, or restore upstream's `install.sh`/`install.ps1` scripts (see `NOTICE`) and re-host them under your own domain.

> **Android / Termux:** Follow upstream's [Termux guide](https://github.com/NousResearch/hermes-agent) for the manual path; the `.[termux]` extra applies the same way here.

After installation:

```bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
hermes              # start chatting!
```

### Troubleshooting

#### Windows Defender or antivirus flags `uv.exe` as malware

If your antivirus (Bitdefender, Windows Defender, etc.) quarantines `uv.exe` from the Hermes `bin` folder (`%LOCALAPPDATA%\hermes\bin\uv.exe`), this is a **false positive**. The file is Astral's `uv` — the Rust Python package manager Hermes bundles to manage its Python environment. ML-based antivirus engines commonly flag unsigned Rust binaries that download and install packages.

**To verify your copy is authentic:**

```powershell
# Install GitHub CLI if needed
winget install --id GitHub.cli

# Login to GitHub
gh auth login

# Run verification
$uv = "$env:LOCALAPPDATA\hermes\bin\uv.exe"
$ver = (& $uv --version).Split(' ')[1]
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$zip = "$env:TEMP\uv.zip"
Invoke-WebRequest "https://github.com/astral-sh/uv/releases/download/$ver/uv-x86_64-pc-windows-msvc.zip" -OutFile $zip -UseBasicParsing
gh attestation verify $zip --repo astral-sh/uv
Expand-Archive $zip "$env:TEMP\uv_x" -Force
(Get-FileHash "$env:TEMP\uv_x\uv.exe").Hash -eq (Get-FileHash $uv).Hash
```

If attestation says "Verification succeeded" and the last line prints `True`, you're good.

**To whitelist Hermes:**
- **Windows Defender:** Run PowerShell as Admin → `Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\hermes\bin"`
- **Bitdefender:** Add an exception in the Bitdefender console (Protection > Antivirus > Settings > Manage Exceptions)
- Whitelist the **folder**, not the file hash — Hermes updates `uv` and the hash changes every version

For more context, see the upstream Astral reports: [astral-sh/uv#13553](https://github.com/astral-sh/uv/issues/13553), [astral-sh/uv#15011](https://github.com/astral-sh/uv/issues/15011), [astral-sh/uv#10079](https://github.com/astral-sh/uv/issues/10079).

---

## Getting Started

```bash
hermes              # Interactive CLI — start a conversation
hermes model        # Choose your LLM provider and model
hermes tools        # Configure which tools are enabled
hermes config set   # Set individual config values
hermes config get   # Print individual config values
hermes gateway      # Start the messaging gateway (Telegram, Discord, etc.)
hermes setup        # Run the full setup wizard (configures everything at once)
hermes claw migrate # Migrate from OpenClaw (if coming from OpenClaw)
hermes update       # Update to the latest version
hermes doctor       # Diagnose any issues
```

📖 **[Upstream documentation →](https://hermes-agent.nousresearch.com/docs/)** (this fork does not host its own docs site; most content applies except the Nous Portal sections below)

---

## API keys (BYO-key only in this fork)

Agentik removed the managed Nous Portal service layer (hosted OAuth login, billing, subscription tiers, and the bundled Tool Gateway that routed web search / image gen / TTS / cloud browser through one subscription). Bring your own API key for whichever provider(s) you want — Anthropic, OpenAI, OpenRouter, a self-hosted endpoint, etc. — and configure per-tool credentials (Firecrawl, FAL, OpenAI TTS, Browser Use) individually if you use those tools.

---

## CLI vs Messaging Quick Reference

Hermes has two entry points: start the terminal UI with `hermes`, or run the gateway and talk to it from Telegram, Discord, Slack, WhatsApp, Signal, or Email. Once you're in a conversation, many slash commands are shared across both interfaces.

| Action                         | CLI                                           | Messaging platforms                                                              |
| ------------------------------ | --------------------------------------------- | -------------------------------------------------------------------------------- |
| Start chatting                 | `hermes`                                      | Run `hermes gateway setup` + `hermes gateway start`, then send the bot a message |
| Start fresh conversation       | `/new` or `/reset`                            | `/new` or `/reset`                                                               |
| Change model                   | `/model [provider:model]`                     | `/model [provider:model]`                                                        |
| Set a personality              | `/personality [name]`                         | `/personality [name]`                                                            |
| Retry or undo the last turn    | `/retry`, `/undo`                             | `/retry`, `/undo`                                                                |
| Compress context / check usage | `/compress`, `/usage`, `/insights [--days N]` | `/compress`, `/usage`, `/insights [days]`                                        |
| Browse skills                  | `/skills` or `/<skill-name>`                  | `/<skill-name>`                                                                  |
| Interrupt current work         | `Ctrl+C` or send a new message                | `/stop` or send a new message                                                    |
| Platform-specific status       | `/platforms`                                  | `/status`, `/sethome`                                                            |

For the full command lists, see the [CLI guide](https://hermes-agent.nousresearch.com/docs/user-guide/cli) and the [Messaging Gateway guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging).

---

## Documentation

This fork doesn't host its own docs site yet. **[Upstream Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/)** cover CLI usage, config, tools, skills, memory, MCP, cron, and architecture accurately for this fork too — everything except the Nous Portal / Tool Gateway / billing sections, which don't apply here.

---

## Migrating from OpenClaw

If you're coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys.

**During first-time setup:** The setup wizard (`hermes setup`) automatically detects `~/.openclaw` and offers to migrate before configuration begins.

**Anytime after install:**

```bash
hermes claw migrate              # Interactive migration (full preset)
hermes claw migrate --dry-run    # Preview what would be migrated
hermes claw migrate --preset user-data   # Migrate without secrets
hermes claw migrate --overwrite  # Overwrite existing conflicts
```

What gets imported:

- **SOUL.md** — persona file
- **Memories** — MEMORY.md and USER.md entries
- **Skills** — user-created skills → `~/.hermes/skills/openclaw-imports/`
- **Command allowlist** — approval patterns
- **Messaging settings** — platform configs, allowed users, working directory
- **API keys** — allowlisted secrets (Telegram, OpenRouter, OpenAI, Anthropic, ElevenLabs)
- **TTS assets** — workspace audio files
- **Workspace instructions** — AGENTS.md (with `--workspace-target`)

See `hermes claw migrate --help` for all options, or use the `openclaw-migration` skill for an interactive agent-guided migration with dry-run previews.

---

## Contributing

We welcome contributions! For upstream Hermes Agent's development conventions, see [its Contributing Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) — most of it applies here too.

Quick start for contributors — clone this fork and work from a normal git checkout:

```bash
git clone https://github.com/junkman9444/agentik.git
cd agentik
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

Create the venv outside the cloned source tree — a venv inside the directory
the agent operates from can be wiped by a relative-path command the agent runs
against its own checkout, destroying the running runtime mid-session.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv ~/.hermes/venvs/agentik-dev --python 3.11
source ~/.hermes/venvs/agentik-dev/bin/activate
uv pip install -e ".[all,dev]"
scripts/run_tests.sh
```

---

## Community

- 🐛 [Issues](https://github.com/junkman9444/agentik/issues)
- 📚 [Skills Hub](https://agentskills.io) (upstream, applies here too)

---

## License

GPLv2 — see [LICENSE](LICENSE). This is a fork of [Hermes Agent](https://github.com/NousResearch/hermes-agent) (MIT-licensed, © 2025 Nous Research) — see [NOTICE](NOTICE) for the original license terms.

Forked and rebranded by [Sekuro](https://sekuro.io).
