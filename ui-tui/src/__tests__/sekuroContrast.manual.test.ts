import { describe, expect, it } from 'vitest'

import { contrastRatio } from '../lib/color.js'
import { fromSkin, skinIsLight } from '../theme.js'

// Manual verification test for the sekuro skin's real-world contrast, matching
// otter_space's exact reported bug: "text not visible. contrast sucks" with screenshots
// of washed-out pink text on both a light terminal and a dark maroon TUI panel.
const DARK_COLORS = {
  banner_border: '#FF4FB8', banner_title: '#FF4FB8', banner_accent: '#FF6BC4',
  banner_dim: '#FF8FCE', banner_text: '#FFFFFF', ui_accent: '#FF6BC4',
  ui_label: '#FF8FCE', ui_ok: '#6FDD6F', ui_error: '#FF5555', ui_warn: '#FFC24D',
  prompt: '#FFFFFF', input_rule: '#FF4FB8', response_border: '#FF4FB8',
  status_bar_bg: '#1E0C1A', status_bar_text: '#FFFFFF',
  status_bar_strong: '#FF4FB8', status_bar_dim: '#FF8FCE',
  status_bar_good: '#6FDD6F', status_bar_warn: '#FF4FB8', status_bar_bad: '#FF6B9D',
  status_bar_critical: '#FF5555', session_label: '#FF8FCE',
  session_border: '#FF8FCE', completion_menu_bg: '#1E0C1A',
  completion_menu_current_bg: '#3A1530', selection_bg: '#451A38',
  shell_dollar: '#4dabf7', voice_status_bg: '#1E0C1A'
}

const LIGHT_COLORS = {
  banner_title: '#C6007E', banner_accent: '#C6007E', banner_border: '#C6007E',
  banner_dim: '#A3006E', banner_text: '#000000', ui_accent: '#C6007E',
  ui_label: '#A3006E', ui_ok: '#157A15', ui_error: '#C62828', ui_warn: '#B45300',
  prompt: '#000000', input_rule: '#C6007E', response_border: '#C6007E',
  session_label: '#A3006E', status_bar_text: '#000000',
  status_bar_strong: '#C6007E', status_bar_dim: '#A3006E',
  status_bar_good: '#157A15', status_bar_warn: '#C6007E', status_bar_bad: '#C2185B',
  status_bar_critical: '#C62828', session_border: '#A3006E', shell_dollar: '#1E6FC0',
  completion_menu_bg: '#F5F5F5', completion_menu_current_bg: '#F0D9E8',
  selection_bg: '#D4E4F7', status_bar_bg: '#F5F5F5', voice_status_bg: '#F5F5F5'
}

describe('sekuro skin real-world contrast (otter_space: "text not visible")', () => {
  it('dark mode: text/border/muted all clear 4.5:1 against the observed maroon panel bg', () => {
    const isLight = skinIsLight(DARK_COLORS)

    expect(isLight).toBe(false)
    const t = fromSkin(DARK_COLORS, {}, '', '', '', '')
    const observedPanelBg = '#3D0F2E'

    for (const [name, value] of Object.entries({
      border: t.color.border,
      muted: t.color.muted,
      primary: t.color.primary,
      statusGood: t.color.statusGood,
      text: t.color.text
    })) {
      const ratio = contrastRatio(value, observedPanelBg)

      expect(ratio, `${name}=${value} vs panel bg ${observedPanelBg}: ${ratio.toFixed(2)}`).toBeGreaterThanOrEqual(
        4.5
      )
    }
  })

  it('light mode: text/border/muted all clear 4.5:1 against white', () => {
    const merged = { ...DARK_COLORS, ...LIGHT_COLORS }
    const t = fromSkin(merged, {}, '', '', '', '')

    for (const [name, value] of Object.entries({
      border: t.color.border,
      muted: t.color.muted,
      primary: t.color.primary,
      statusGood: t.color.statusGood,
      text: t.color.text
    })) {
      const ratio = contrastRatio(value, '#FFFFFF')

      expect(ratio, `${name}=${value} vs white: ${ratio.toFixed(2)}`).toBeGreaterThanOrEqual(4.5)
    }
  })
})
