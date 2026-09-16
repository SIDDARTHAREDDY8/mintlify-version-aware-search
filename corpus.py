"""Synthetic multi-version docs corpus for the version-aware search eval.

DISCLOSURE: This corpus is entirely synthetic. It was constructed to reproduce the
failure mode reported in mintlify discussion #5668 (old-version pages outranking
current-version equivalents on pure term relevance). It is NOT Mintlify's real index,
not scraped from docs.flowx.ai, and makes no claim about Mintlify's internal systems.
Page bodies use controlled term frequencies so the naive relevance-only ranker exhibits
the reported bug; see README.md.
"""

VERSIONS = ["4.0", "4.7.x", "5.1", "5.7"]

# Each page: version, url, title, body. Bodies deliberately use the vocabulary drift
# that happens across real versioned docs: old versions repeat the exact legacy term,
# new versions rename/restructure (e.g. "SSO setup" -> "Single sign-on", "Rate limits"
# -> "Rate limiting", "Error codes" -> "Errors and retries").
PAGES = [
    # ---- webhooks ----
    {"version": "4.7.x", "url": "/4.7.x/setup-guides/plugins-setup-guide/reporting-setup",
     "title": "Reporting setup",
     "body": ("webhook " * 6) + "without webhook reporting setup. Configure a webhook endpoint "
     "to receive event payloads. Each webhook delivery includes a signature header. "
     "Retry failed webhook deliveries from the dashboard. Webhook secrets rotate every 90 days."},
    {"version": "5.1", "url": "/5.1/docs/platform-deep-dive/integrations/incoming-webhooks",
     "title": "Incoming webhooks",
     "body": "incoming webhooks let external systems push events into the platform. "
     "Create an endpoint, verify the signature, and handle retries. "
     "See the webhook gateway for outbound delivery."},
    {"version": "5.1", "url": "/5.1/setup-guides/webhook-gateway-setup",
     "title": "Webhook gateway setup",
     "body": "the webhook gateway manages outbound event delivery. Configure destinations, "
     "set retry policies, and monitor delivery health from one place."},
    {"version": "5.7", "url": "/5.7/docs/integrations/webhooks-overview",
     "title": "Webhooks overview",
     "body": "webhooks deliver real-time event notifications to your infrastructure. "
     "Register endpoints, verify signatures with the shared secret, and use idempotency keys."},
    # ---- authentication ----
    {"version": "4.0", "url": "/4.0/guides/authentication",
     "title": "Authentication",
     "body": ("authentication " * 5) + "all api requests require authentication. "
     "Pass your api key in the authorization header for authentication."},
    {"version": "4.7.x", "url": "/4.7.x/guides/authentication",
     "title": "Authentication and API keys",
     "body": ("authentication " * 4) + "use api key authentication for server to server calls. "
     "Rotate keys regularly. Authentication failures return 401."},
    {"version": "5.1", "url": "/5.1/docs/authentication",
     "title": "Authentication",
     "body": "authenticate with an api key or a scoped token. Tokens expire after 30 days. "
     "Keep credentials out of client side code."},
    {"version": "5.7", "url": "/5.7/docs/security/oauth",
     "title": "Auth with OAuth 2.0",
     "body": "oauth 2.0 is the recommended auth flow. Register an application, complete the "
     "authorization code exchange, and refresh tokens before expiry."},
    # ---- rate limits ----
    {"version": "4.7.x", "url": "/4.7.x/api-reference/rate-limits",
     "title": "Rate limits",
     "body": ("rate limits " * 5) + "the api enforces rate limits per api key. "
     "Exceeding rate limits returns 429. Rate limits reset every minute."},
    {"version": "5.1", "url": "/5.1/docs/rate-limits",
     "title": "Rate limits and quotas",
     "body": "rate limits and quotas protect shared infrastructure. Default quota is 1000 "
     "requests per minute. Request an increase from support."},
    {"version": "5.7", "url": "/5.7/docs/platform/rate-limiting",
     "title": "Rate limiting",
     "body": "rate limiting uses a token bucket per workspace. Bursts up to 2x are allowed. "
     "Inspect remaining quota in response headers."},
    # ---- quickstart ----
    {"version": "4.0", "url": "/4.0/quickstart",
     "title": "Quickstart",
     "body": ("quickstart " * 4) + "this quickstart gets you running in five minutes. "
     "Install the package, set your api key, and make your first quickstart request."},
    {"version": "4.7.x", "url": "/4.7.x/quickstart",
     "title": "Quickstart guide",
     "body": ("quickstart " * 3) + "follow this quickstart guide to send your first api call. "
     "You need an account and an api key."},
    {"version": "5.1", "url": "/5.1/docs/quickstart",
     "title": "Quickstart",
     "body": "get started in minutes. Create a workspace, generate a token, and run the sample."},
    {"version": "5.7", "url": "/5.7/docs/quickstart",
     "title": "Quickstart",
     "body": "get started quickly with the interactive tutorial. No credit card required."},
    # ---- migration ----
    {"version": "5.1", "url": "/5.1/docs/migration/from-4x",
     "title": "Migrating from 4.x",
     "body": "migrating from 4.x to 5.1. Breaking changes: authentication headers renamed, "
     "webhook payload version bumped, pagination now cursor based."},
    {"version": "5.7", "url": "/5.7/docs/migration/from-51",
     "title": "Migrating from 5.1",
     "body": "migrating from 5.1 to 5.7. The oauth flow replaces api keys. "
     "Rate limiting headers changed names."},
    # ---- sso ----
    {"version": "4.7.x", "url": "/4.7.x/setup-guides/sso-setup",
     "title": "SSO setup",
     "body": ("sso " * 6) + "configure sso with your identity provider. "
     "Sso supports saml and oidc. Test the sso connection before enforcing it."},
    {"version": "5.1", "url": "/5.1/docs/security/sso",
     "title": "Single sign-on (SSO)",
     "body": "single sign-on lets team members authenticate with your identity provider. "
     "Supports saml 2.0 and oidc."},
    {"version": "5.7", "url": "/5.7/docs/security/sso-scim",
     "title": "SSO and SCIM",
     "body": "single sign-on plus scim provisioning keeps membership in sync automatically."},
    # ---- cli ----
    {"version": "4.0", "url": "/4.0/cli/install",
     "title": "CLI installation",
     "body": ("cli install " * 3) + "cli installation via npm or homebrew. "
     "Verify the cli install with the version command."},
    {"version": "5.1", "url": "/5.1/docs/cli/install",
     "title": "Install the CLI",
     "body": "install the command line tool with one command. Log in to link your workspace."},
    {"version": "5.7", "url": "/5.7/docs/cli/reference",
     "title": "CLI reference",
     "body": "command reference for the cli. Every command supports json output."},
    # ---- errors ----
    {"version": "4.7.x", "url": "/4.7.x/api-reference/errors",
     "title": "Error codes",
     "body": ("error codes " * 5) + "the api returns standard error codes. "
     "Common error codes are listed with their http status."},
    {"version": "5.1", "url": "/5.1/docs/api/errors",
     "title": "Error codes",
     "body": "error codes help you debug failed requests. Each error includes a code and message."},
    {"version": "5.7", "url": "/5.7/docs/api/errors-retries",
     "title": "Errors and retries",
     "body": "errors are returned with machine readable codes. Retry idempotent requests "
     "with exponential backoff."},
    # ---- pagination ----
    {"version": "4.7.x", "url": "/4.7.x/api-reference/pagination",
     "title": "Pagination",
     "body": ("pagination " * 5) + "list endpoints support pagination with page and per_page. "
     "Pagination metadata is in the response envelope."},
    {"version": "5.1", "url": "/5.1/docs/api/pagination",
     "title": "Pagination",
     "body": "paginate large collections with cursor based pagination for stable ordering."},
    {"version": "5.7", "url": "/5.7/docs/api/cursor-pagination",
     "title": "Cursor pagination",
     "body": "cursor pagination is the only supported mode. Pass the cursor from the "
     "previous response."},
]

# Queries with per-version ground truth: which page urls are the right answer
# when the reader is browsing that version. Only (query, version) pairs with at
# least one relevant page in that version are evaluated.
QUERIES = [
    {"q": "webhook", "relevant": {
        "4.7.x": ["/4.7.x/setup-guides/plugins-setup-guide/reporting-setup"],
        "5.1": ["/5.1/docs/platform-deep-dive/integrations/incoming-webhooks",
                "/5.1/setup-guides/webhook-gateway-setup"],
        "5.7": ["/5.7/docs/integrations/webhooks-overview"]}},
    {"q": "authentication", "relevant": {
        "4.0": ["/4.0/guides/authentication"],
        "4.7.x": ["/4.7.x/guides/authentication"],
        "5.1": ["/5.1/docs/authentication"],
        "5.7": ["/5.7/docs/security/oauth"]}},
    {"q": "rate limits", "relevant": {
        "4.7.x": ["/4.7.x/api-reference/rate-limits"],
        "5.1": ["/5.1/docs/rate-limits"],
        "5.7": ["/5.7/docs/platform/rate-limiting"]}},
    {"q": "quickstart", "relevant": {
        "4.0": ["/4.0/quickstart"],
        "4.7.x": ["/4.7.x/quickstart"],
        "5.1": ["/5.1/docs/quickstart"],
        "5.7": ["/5.7/docs/quickstart"]}},
    {"q": "migrating from 4.x", "relevant": {
        "5.1": ["/5.1/docs/migration/from-4x"]}},
    {"q": "migrating from 5.1", "relevant": {
        "5.7": ["/5.7/docs/migration/from-51"]}},
    {"q": "sso", "relevant": {
        "4.7.x": ["/4.7.x/setup-guides/sso-setup"],
        "5.1": ["/5.1/docs/security/sso"],
        "5.7": ["/5.7/docs/security/sso-scim"]}},
    {"q": "cli install", "relevant": {
        "4.0": ["/4.0/cli/install"],
        "5.1": ["/5.1/docs/cli/install"],
        "5.7": ["/5.7/docs/cli/reference"]}},
    {"q": "error codes", "relevant": {
        "4.7.x": ["/4.7.x/api-reference/errors"],
        "5.1": ["/5.1/docs/api/errors"],
        "5.7": ["/5.7/docs/api/errors-retries"]}},
    {"q": "pagination", "relevant": {
        "4.7.x": ["/4.7.x/api-reference/pagination"],
        "5.1": ["/5.1/docs/api/pagination"],
        "5.7": ["/5.7/docs/api/cursor-pagination"]}},
]


def eval_pairs():
    """Yield (query, browsing_version, relevant_urls) for every pair worth testing."""
    for item in QUERIES:
        for version, urls in item["relevant"].items():
            yield item["q"], version, urls
