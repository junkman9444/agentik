import type { BillingBlock } from '@hermes/shared/billing'

export interface BillingDialogCopy {
  cancelLabel: string
  confirmLabel: string
  detail: string
  title: string
}

/**
 * Copy for the out-of-credits confirm dialog (the TUI's billing wall). The
 * dialog is the actionable layer — the full provider guidance already lands in
 * the transcript — so `detail` stays to one concise, non-truncating line and the
 * confirm button carries the recovery: the provider's billing page (or `/model`
 * to switch when we have no URL). Pure + exported so the wording is unit-tested
 * without driving the gateway.
 *
 * Nous Portal billing (the `block.is_nous` branch) is intentionally not handled
 * here: this fork has no Nous provider in its credential pool
 * (sage_cli/auth.py's PROVIDER_REGISTRY), so a billing event can never carry
 * is_nous: true in a live session. If block.is_nous is somehow set anyway, it
 * falls through to the generic provider-billing copy below rather than
 * recommending the removed /topup flow.
 */
export function billingDialogCopy(block: BillingBlock): BillingDialogCopy {
  const label = block.provider_label || 'your provider'

  return {
    cancelLabel: 'Dismiss',
    confirmLabel: block.billing_url ? 'Open billing page' : 'Switch provider',
    detail: `${label} reports your credits or billing are exhausted.`,
    title: `Out of credits · ${label}`
  }
}
