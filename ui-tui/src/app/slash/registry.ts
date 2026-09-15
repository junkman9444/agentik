import { coreCommands } from './commands/core.js'
import { debugCommands } from './commands/debug.js'
import { opsCommands } from './commands/ops.js'
import { sessionCommands } from './commands/session.js'
import { setupCommands } from './commands/setup.js'
import { wakeCommands } from './commands/wake.js'
import type { SlashCommand } from './types.js'

// topupCommands / subscriptionCommands (billing + subscription overlays, ./commands/topup.js and
// ./commands/subscription.js) are intentionally NOT registered in this fork: they authorize card
// charges to Nous Research and hand off to Nous's own subscription portal -- a Nous-specific paid
// feature, out of scope for Sage (Sekuro AGEnt). The overlay components (billingOverlay.tsx,
// subscriptionOverlay.tsx) still exist on disk but are now unreachable dead code (no slash command
// or keybind constructs the `billing`/`subscription` overlay-state shape that would render them).

export const SLASH_COMMANDS: SlashCommand[] = [
  ...coreCommands,
  ...sessionCommands,
  ...opsCommands,
  ...wakeCommands,
  ...setupCommands,
  ...debugCommands
]

const byName = new Map<string, SlashCommand>(
  SLASH_COMMANDS.flatMap(cmd => [cmd.name, ...(cmd.aliases ?? [])].map(name => [name, cmd] as const))
)

export const findSlashCommand = (name: string) => byName.get(name.toLowerCase())
