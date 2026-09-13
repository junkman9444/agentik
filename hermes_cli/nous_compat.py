"""Safe stand-ins for the deleted Nous Portal ``nous_account`` / ``nous_subscription`` modules.

The Nous Portal core-path subsystem (auth_nous.py, nous_account.py, nous_auth_keepalive.py,
nous_billing.py, nous_subscription.py, portal_cli.py, proxy/adapters/nous_portal.py) has been
removed from this fork. This module exists so every consumer that used to import entitlement /
managed-tool-gateway data from those modules keeps working: every account is reported "not logged
in" / "no managed tools", never crashes, and every managed-tool code path degrades to the direct
(BYO credentials) path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Literal, Optional

NousAccountInfoSource = Literal["jwt", "account_api", "inference_key", "none", "error"]

TOOL_COVERAGE_CATEGORIES = ("firecrawl", "fal", "fal-video", "openai-audio", "browser-use", "modal")

FREE_TIER_NEEDS_ACCOUNT = "This needs a Nous account. Run `hermes auth upgrade`."
FREE_TIER_NEEDS_ACCOUNT_CHAT = "This needs a Nous account. Use /login to sign in."

_REMOVED_MESSAGE = "Nous Portal support has been removed from this fork."

# Plugin-compat stand-ins for names external code imported from ``hermes_cli.auth_nous``.
_NOUS_SHARED_STORE_FILENAME_STUB = "nous_auth.json"


def _refresh_nous_oauth_pure_stub(*args, **kwargs):  # noqa: ARG001
    raise RuntimeError(_REMOVED_MESSAGE)


@dataclass(frozen=True)
class NousPortalSubscriptionInfo:
    plan: Optional[str] = None
    tier: Optional[int] = None
    monthly_charge: Optional[float] = None
    monthly_credits: Optional[float] = None
    current_period_end: Optional[str] = None
    credits_remaining: Optional[float] = None
    rollover_credits: Optional[float] = None


@dataclass(frozen=True)
class NousPaidServiceAccessInfo:
    allowed: Optional[bool] = None
    paid_access: Optional[bool] = None
    reason: Optional[str] = None
    organisation_id: Optional[str] = None
    effective_at_ms: Optional[int] = None
    has_active_subscription: Optional[bool] = None
    active_subscription_is_paid: Optional[bool] = None
    subscription_tier: Optional[int] = None
    subscription_monthly_charge: Optional[float] = None
    subscription_credits_remaining: Optional[float] = None
    purchased_credits_remaining: Optional[float] = None
    total_usable_credits: Optional[float] = None
    member_spend_cap_exceeded: Optional[bool] = None
    member_spend_cap_usd: Optional[float] = None
    member_spend_usd: Optional[float] = None
    member_spend_cap_remaining_usd: Optional[float] = None


@dataclass(frozen=True)
class NousToolAccessInfo:
    enabled: bool = False
    coverage: dict = field(default_factory=dict)


@dataclass(frozen=True)
class NousPortalAccountInfo:
    """Always a logged-out / not-entitled snapshot in this fork."""

    logged_in: bool = False
    source: NousAccountInfoSource = "none"
    fresh: bool = True
    user_id: Optional[str] = None
    org_id: Optional[str] = None
    org_slug: Optional[str] = None
    org_name: Optional[str] = None
    client_id: Optional[str] = None
    product_id: Optional[str] = None
    nous_client: Optional[str] = None
    portal_base_url: Optional[str] = None
    inference_base_url: Optional[str] = None
    inference_credential_present: bool = False
    credential_source: Optional[str] = None
    expires_at: Optional[Any] = None
    email: Optional[str] = None
    privy_did: Optional[str] = None
    subscription: Optional[NousPortalSubscriptionInfo] = None
    paid_service_access: Optional[bool] = None
    paid_service_access_info: Optional[NousPaidServiceAccessInfo] = None
    tool_access: Optional[NousToolAccessInfo] = None
    raw_claims: Optional[dict] = None
    raw_account: Optional[dict] = None
    error: Optional[str] = _REMOVED_MESSAGE
    account_tier: Optional[str] = None

    @property
    def is_paid(self) -> bool:
        return False

    @property
    def is_anonymous_tier(self) -> bool:
        return False

    @property
    def is_free_tier(self) -> bool:
        return False

    @property
    def tool_gateway_entitled(self) -> bool:
        return False

    def tool_gateway_entitled_for(self, category: str) -> bool:  # noqa: ARG002
        return False


def get_nous_portal_account_info(*, force_fresh: bool = False, min_jwt_ttl_seconds: int = 60) -> NousPortalAccountInfo:  # noqa: ARG001
    return NousPortalAccountInfo()


def reset_nous_portal_account_info_cache() -> None:
    return None


def nous_policy_present() -> Optional[bool]:
    return None


def nous_policy_notice(*, removed: bool) -> str:  # noqa: ARG001
    return ""


def nous_policy_allowed_ids(*, force_refresh: bool = False) -> Optional[set]:  # noqa: ARG001
    return None


def nous_portal_billing_url(account_info: Optional[NousPortalAccountInfo] = None) -> str:  # noqa: ARG001
    return "https://portal.nousresearch.com/billing"


def nous_portal_topup_url(account_info: Optional[NousPortalAccountInfo] = None) -> str:  # noqa: ARG001
    return "https://portal.nousresearch.com/billing"


def format_nous_portal_entitlement_message(
    account_info: Optional[NousPortalAccountInfo] = None, *, capability: str = "this feature",
    include_refresh_hint: bool = True, coverage_category: Optional[str] = None, in_chat: bool = False,
) -> Optional[str]:  # noqa: ARG001
    return f"{capability} is not available: {_REMOVED_MESSAGE}"


def nous_policy_notice_removed() -> str:
    return ""


# --- nous_subscription.py stand-ins --------------------------------------------------------------

_FEATURE_KEYS = ("web", "image_gen", "video_gen", "tts", "stt", "browser", "modal")
_FEATURE_LABELS = {
    "web": "Web tools", "image_gen": "Image generation", "video_gen": "Video generation",
    "tts": "OpenAI TTS", "stt": "Speech-to-text", "browser": "Browser automation",
    "modal": "Modal execution",
}
MANAGED_FEATURE_COVERAGE_CATEGORY: Dict[str, str] = {
    "web": "firecrawl", "image_gen": "fal", "video_gen": "fal-video", "tts": "openai-audio",
    "stt": "openai-audio", "browser": "browser-use", "modal": "modal",
}


@dataclass(frozen=True)
class NousFeatureState:
    key: str
    label: str
    included_by_default: bool = False
    available: bool = False
    active: bool = False
    managed_by_nous: bool = False
    direct_override: bool = False
    toolset_enabled: bool = False
    current_provider: str = ""
    explicit_configured: bool = False


@dataclass(frozen=True)
class NousSubscriptionFeatures:
    subscribed: bool = False
    nous_auth_present: bool = False
    provider_is_nous: bool = False
    features: Dict[str, NousFeatureState] = field(default_factory=dict)
    account_info: Optional[NousPortalAccountInfo] = None

    def __getattr__(self, name: str) -> NousFeatureState:
        if name in _FEATURE_KEYS:
            return self.features[name]
        raise AttributeError(name)

    def items(self) -> Iterable[NousFeatureState]:
        return (self.features[key] for key in _FEATURE_KEYS)


def _default_features() -> Dict[str, NousFeatureState]:
    return {key: NousFeatureState(key, _FEATURE_LABELS[key]) for key in _FEATURE_KEYS}


def get_nous_subscription_features(config: Optional[dict] = None, *, force_fresh: bool = False) -> NousSubscriptionFeatures:  # noqa: ARG001
    """Never-managed features: every category reports "not available via Nous subscription", so
    callers fall through to their direct/BYO-credential branch."""
    return NousSubscriptionFeatures(features=_default_features(), account_info=NousPortalAccountInfo())


def apply_nous_managed_defaults(config: dict, *, enabled_toolsets: Optional[Iterable[str]] = None, force_fresh: bool = False) -> set:  # noqa: ARG001
    return set()


def get_gateway_eligible_tools(config: Optional[dict] = None, *, force_fresh: bool = False) -> tuple:  # noqa: ARG001
    return [], [], [], []


def apply_gateway_defaults(config: dict, tool_keys: list) -> set:  # noqa: ARG001
    return set()


def prompt_enable_tool_gateway(config: dict, *, force_fresh: bool = True) -> set:  # noqa: ARG001
    return set()


def ensure_nous_portal_access(*, capability: str = "the Nous Tool Gateway", coverage_category: Optional[str] = None) -> bool:  # noqa: ARG001
    print(f"  {capability} requires the Nous Portal, which is not available in this fork.")
    return False


def managed_nous_tools_enabled(*, force_fresh: bool = False) -> bool:  # noqa: ARG001
    return False


def _local_browser_runnable() -> bool:
    """Mirrors ``nous_subscription._local_browser_runnable`` for post-setup install checks that
    used to import it: the agent-browser CLI plus a usable engine (Chromium or Lightpanda)."""
    try:
        from tools.browser_tool_install import _chromium_installed
        from tools.browser_tool_lightpanda_fallback import _using_lightpanda_engine
    except Exception:
        return _has_agent_browser()
    if not _has_agent_browser():
        return False
    return _using_lightpanda_engine() or _chromium_installed()


def _has_agent_browser() -> bool:
    """Mirrors ``nous_subscription._has_agent_browser``: is the agent-browser CLI on PATH/installed."""
    import shutil

    try:
        from tools.browser_tool_install import _find_agent_browser, _requires_real_termux_browser_install
    except Exception:
        from hermes_constants import with_hermes_node_path
        from pathlib import Path

        local_bin_dir = Path(__file__).parent.parent / "node_modules" / ".bin"
        search_paths = [None, with_hermes_node_path().get("PATH", ""), str(local_bin_dir) if local_bin_dir.is_dir() else ""]
        return any(
            shutil.which("agent-browser", **({} if path is None else {"path": path}))
            for path in search_paths if path != "")
    try:
        browser_cmd = _find_agent_browser(validate=False)
    except FileNotFoundError:
        return False
    return not _requires_real_termux_browser_install(browser_cmd)
