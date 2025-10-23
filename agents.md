We have the following YAML structure for the types of vulnerabilities that we want to implement to test our proposal application security tool that we want to submit to YC startup accelerator.

# Vulnerable test app manifest for YC demo
# Purpose: seed a sandbox web app with toggleable vulnerabilities (technical and business-logic)
# WARNING: implement only in an isolated test environment.

meta:
  app_name: vulnerable-shop-demo
  version: 1.0
  author: "Generated for YC prep"
  created: 2025-10-23
  notes: |
    Each entry below describes a vulnerable endpoint or workflow. Implement as toggleable modules
    (feature flags) and use seeded data in `seed_data:` to create realistic test cases.

vulnerabilities:
  - id: TECH-001
    title: SQL Injection (Login/Search)
    category: technical
    route: /login
    method: POST
    description: "Login endpoint concatenates user input into SQL query without parameterization."
    bug_pattern: "db.query(\"SELECT * FROM users WHERE email = '" + email + "' AND password = '" + pwd + "'\")"
    seed_data:
      users:
        - id: 1
          email: alice@example.com
          password: password123
        - id: 2
          email: bob@example.com
          password: hunter2
    severity: high
    detection_hints:
      - look for unsanitized parameters in SQL strings
      - abnormal query shapes in logs
    remediation: "Use parameterized queries / prepared statements; ORM with safe bindings."
    notes: "Provide a search endpoint variant (/search?q=) that demonstrates reflected behavior as well."

  - id: TECH-002
    title: Stored XSS (Comments)
    category: technical
    route: /posts/{id}/comments
    method: POST
    description: "User-submitted comments are stored and later rendered in HTML without proper escaping."
    bug_pattern: "res.render('post', {comments: post.comments}) // no escaping"
    seed_data:
      posts:
        - id: 100
          title: 'Welcome'
          comments: []
    severity: medium
    detection_hints:
      - outputs that include unescaped user-input in HTML
      - lack of Content-Security-Policy header
    remediation: "Escape HTML on render; apply CSP; mark cookies HttpOnly."

  - id: TECH-003
    title: Insecure Direct Object Reference (IDOR) - Invoices
    category: technical
    route: /invoices/{invoice_id}
    method: GET
    description: "Server returns invoice by ID with no ownership check."
    bug_pattern: "SELECT * FROM invoices WHERE id = :id // no owner check"
    seed_data:
      invoices:
        - id: 9001
          owner_user_id: 1
          amount: 499.99
        - id: 9002
          owner_user_id: 2
          amount: 29.99
    severity: high
    detection_hints:
      - endpoints that use raw numeric IDs
      - ability to access other users' resources by guessing IDs
    remediation: "Enforce authorization: verify current_user.id == invoice.owner_user_id."

  - id: TECH-004
    title: CSRF on Account Transfer
    category: technical
    route: /account/transfer
    method: POST
    description: "State-changing transfer endpoint accepts cookie auth and lacks CSRF token validation."
    bug_pattern: "POST /account/transfer from authenticated cookie-based session with no anti-CSRF"
    seed_data:
      users:
        - id: 1
          balance: 1000.0
        - id: 2
          balance: 10.0
    severity: high
    detection_hints:
      - POST endpoints that change state without CSRF protections
    remediation: "Require same-site cookies or CSRF tokens; validate Origin/Referer."

  - id: TECH-005
    title: SSRF via URL Preview
    category: technical
    route: /preview?url={url}
    method: GET
    description: "Server-side previewer fetches arbitrary URLs provided by users without allowlist."
    bug_pattern: "httpClient.get(request.query.url) // no validation"
    seed_data: {}
    severity: high
    detection_hints:
      - server issues HTTP requests to user-supplied URLs in logs
      - access to internal metadata endpoints (e.g., 169.254.169.254)
    remediation: "Allowlist remote hosts, restrict schemes, enforce timeouts; sanitize/validate URLs."

  - id: TECH-006
    title: Insecure File Upload (Path Traversal)
    category: technical
    route: /upload
    method: POST
    description: "Uploads saved using original filename with no normalization, enabling ../ traversal."
    bug_pattern: "fs.writeFile('uploads/' + req.file.name, data)"
    seed_data: {}
    severity: high
    detection_hints:
      - uploaded filenames containing ../ or absolute paths
      - files written outside upload directory in server logs
    remediation: "Sanitize filenames, generate server-side unique names, restrict allowed file types and storage paths."

  - id: TECH-007
    title: Missing Security Headers
    category: technical
    route: any
    method: ANY
    description: "App responds without CSP, HSTS, X-Frame-Options."
    bug_pattern: "no security headers in response"
    seed_data: {}
    severity: low
    detection_hints:
      - missing standard headers in HTTP responses
    remediation: "Ensure secure headers configured on app / reverse proxy."  - id: BL-001
    title: Price Manipulation by Client (Parameter Tampering)
    category: business_logic
    route: /checkout
    method: POST
    description: "Server trusts client-sent price or discount instead of using authoritative server pricing."
    bug: "Server accepts `total`/`price`/`discount` fields from client payload and records that as charged amount."
    scenario: |
      Checkout form includes a hidden `total` input. A user modifies the form (or API request) to set `total` to 0.00
      and the server charges that amount and grants access to paid features.
    impact: "Users can purchase items for free or at incorrect prices, causing revenue loss and abuse of paid features."
    seed: "Create a cart page that posts `items` and `total`. Server-side code should (in this vulnerable lab) accept the submitted `total`."
    seed_data:
      products:
        - id: 10
          name: 'Pro Plan'
          price: 199.00
    severity: critical
    detection_hints:
      - orders with totals that don't match product sums
      - client-supplied price fields in request logs
    remediation: "Always calculate totals server-side from product prices, tax and shipping."

  - id: BL-002
    title: Promo Stacking / Coupon Abuse
    category: business_logic
    route: /apply-coupon
    method: POST
    description: "Multiple coupons can be applied and combine multiplicatively; no per-account or per-order limits."
    bug: "No rules preventing stacking, reuse across accounts, or enforcing per-order caps."
    scenario: |
      A user applies two or more coupons (WELCOME10 and BLACKFRI50). The system applies both discounts multiplicatively
      (e.g. price * 0.9 * 0.5) and the user gets a very large discount or free product.
    impact: "Excessive discounts, revenue loss, and possible inventory drain when coupons enable free acquisition."
    seed: "Implement an `applyCoupon` endpoint that accepts coupon codes and naively applies them to the cart without checks."
    seed_data:
      coupons:
        - code: WELCOME10
          discount_percent: 10
        - code: BLACKFRI50
          discount_percent: 50
    severity: high
    detection_hints:
      - multiple coupons applied to single order
      - repeated coupon usage from same accounts or IPs
    remediation: "Enforce non-stackable flags, usage limits per account, and validate coupons at checkout server-side."

  - id: BL-003
    title: Subscription / Billing Bypass (Grace Period Abuse)
    category: business_logic
    route: /entitlements, /billing/webhook
    method: MIXED
    description: "Access is based on stale client/local state or delayed sync between billing and entitlement services."
    bug: "Entitlement service trusts cached or client-supplied subscription status and does not revalidate with billing immediately."
    scenario: |
      A user cancels subscription in billing but the entitlement cache still shows active access for the grace period; the user
      toggles plan or exploits delayed reconciliation to access premium features after cancellation or without payment.
    impact: "Users retain premium access without paying, or downgrade to cheaper plans while still consuming higher-tier benefits."
    seed: "Create separate mock billing and entitlement services; intentionally delay webhook sync so entitlement remains active after cancellation."
    severity: high
    detection_hints:
      - entitlements that do not match billing records
      - webhook delivery lag events
    remediation: "Design strong sync protocols, require server-side authoritative checks against billing for critical gating."

  - id: BL-004
    title: Race Condition: Inventory / Checkout Double-spend
    category: business_logic
    route: /checkout
    method: POST
    description: "Concurrent checkouts can both succeed and decrement stock below zero due to lack of atomic operations."
    bug: "No transactional locking or atomic check-and-decrement when reserving inventory."
    scenario: |
      Two users (or two concurrent requests) attempt to purchase the last unit of an item. Both requests read `qty=1` available
      and both decrement, resulting in negative stock and overselling.
    impact: "Overselling, logistical headaches, customer service issues and potential financial loss."
    seed: "Provide an item with low stock (1) and allow concurrent requests to /checkout to simulate race conditions."
    severity: high
    detection_hints:
      - stock levels going negative
      - multiple confirmed orders for the same last unit
    remediation: "Use database transactions, row locking, or atomic decrement operations; implement reservation and timeout."

  - id: BL-005
    title: Refund / Chargeback Logic Flaw
    category: business_logic
    route: /refund
    method: POST
    description: "Refund endpoint allows arbitrary amounts or multiple refunds because it lacks state checks and idempotency."
    bug: "No validation on refund amounts relative to order total and no check preventing duplicate refunds."
    scenario: |
      An attacker calls `POST /refund {order_id: 5001, amount: 199.00}` repeatedly before the refunded state is updated,
      causing multiple payouts or credits for a single order.
    impact: "Monetary loss, accounting inconsistencies and potential exploitation at scale."
    seed: "Implement a refund endpoint that accepts `order_id` and `amount` and immediately processes refunds without checking `refunded_amount` or locking the order."
    seed_data:
      orders:
        - id: 5001
          user_id: 1
          total: 199.00
          status: paid
          refunded_amount: 0.0
    severity: critical
    detection_hints:
      - many refund transactions for same order_id
      - refunded_amount exceeding order total
    remediation: "Lock order state during refund processing, check existing `refunded_amount`, and make refunds idempotent."

  - id: BL-006
    title: Account Enumeration via Password Reset Flow
    category: business_logic
    route: /forgot-password
    method: POST
    description: "Password reset responses or timings reveal whether an email is registered."
    bug: "Distinct messages or timing differences for registered vs non-registered emails."
    scenario: |
      The `POST /forgot-password` endpoint responds with "Email sent" for existing users and "No account found" for others,
      enabling attackers to enumerate valid emails.
    impact: "User privacy loss and targeted phishing or brute-force attacks using discovered accounts."
    seed: "Implement naive reset flow returning different messages or HTTP codes for existing vs non-existing emails."
    seed_data:
      users:
        - id: 1
          email: alice@example.com
    severity: medium
    detection_hints:
      - many reset requests followed by confirmed account discoveries
      - differing response payloads or timing for emails
    remediation: "Use uniform responses, constant timing, and rate-limit reset operations."

  - id: BL-007
    title: Insecure Role Escalation via Client-side Role Flags
    category: business_logic
    route: /profile, /admin-actions
    method: POST
    description: "User role is stored client-side (in JWT or hidden field) and the server trusts it for authorization."
    bug: "Server directly trusts client-provided `role` claim or header rather than validating against server-side records."
    scenario: |
      A user alters the `role` claim in a JWT or a hidden form field to `admin`, then calls admin endpoints that the server
      grants because it trusts the client-supplied role.
    impact: "Unauthorized access to admin functionality, data exfiltration, or privilege escalation."
    seed: "Issue JWTs that contain a `role` claim and implement server endpoints that read the claim without verifying DB role."
    severity: critical
    detection_hints:
      - mismatches between JWT claims and server-side user roles
      - non-admin accounts performing admin actions
    remediation: "Validate roles server-side and never trust client-provided authorization claims."

  - id: BL-008
    title: Loyalty Points / Credit Abuse
    category: business_logic
    route: /apply-credits, /reward
    method: POST
    description: "Server accepts client-supplied credit/points adjustments or lacks anti-fraud checks on reward issuance."
    bug: "API accepts `points` or `credit` values from client and applies them without validation or thresholds."
    scenario: |
      A user sends `POST /apply-credits {user_id: 2, points: 100000}` and the server adds those points to the account,
      enabling free purchases.
    impact: "Fraudulent purchases, accounting anomalies, and financial loss."
    seed: "Create a reward endpoint that accepts `points` in the request and immediately updates the user's balance."
    severity: high
    detection_hints:
      - sudden large increases in account credits
      - credits applied from unfamiliar IPs or devices
    remediation: "Require server-side validation, signed requests for credit changes, and manual review thresholds."

  - id: BL-009
    title: KYC / Identity Bypass (Weak Verification)
    category: business_logic
    route: /kyc/submit
    method: POST
    description: "KYC acceptance is trivial (e.g., any uploaded file or only filename checks), permitting fraudulent approvals."
    bug: "System marks KYC as complete upon any file upload or simple flag without document validation or liveness checks."
    scenario: |
      A user uploads a placeholder image or text file and the system marks them KYC-complete, granting access to high-value features.
    impact: "Fraud, money laundering risk, regulatory exposure and reputational damage."
    seed: "Implement a KYC endpoint that sets `kyc_status=approved` upon any file without OCR, metadata, or manual review."
    severity: critical
    detection_hints:
      - many approvals with low-quality documents
      - KYC completions tied to suspicious accounts or IPs
    remediation: "Use automated document validation (OCR), liveness detection, and manual review for higher-risk cases."

  - id: BL-010
    title: Order Cancellation / Return Race (Re-sell Attack)
    category: business_logic
    route: /cancel-order, /refund
    method: POST
    description: "Cancel and refund flows are independent and not state-locked, allowing refunds before courier pickup is verified."
    bug: "Refunds processed without verifying courier pickup or locking order state during cancellation/refund."
    scenario: |
      A fraudster cancels an order (or triggers a refund) while the merchant still ships the item; the merchant refunds the money
      and ships, causing financial loss when the item is delivered to the attacker.
    impact: "Monetary loss, inventory loss, and increased fraud rates."
    seed: "Create independent `cancel` and `refund` endpoints and do not check courier pickup or order fulfillment status before refunding."
    severity: high
    detection_hints:
      - refunds issued while courier shows item as 'in transit'
      - frequent cancels/refunds tied to same shipping addresses
    remediation: "Coordinate order state, require courier confirmation for refunds in certain windows, and lock orders during refund processing."

  - id: BL-011
    title: Vendor / Marketplace Payout Manipulation
    category: business_logic
    route: /webhooks/vendor/sale
    method: POST
    description: "Vendor sales webhooks accepted without signature verification or authentication, triggering payouts."
    bug: "Webhook endpoint processes sale events and credits vendor accounts without verifying payload authenticity."
    scenario: |
      An attacker POSTs `{vendor_id: 77, sale_amount: 1000}` to the vendor webhook and the system credits vendor 77's balance,
      causing payout of fake sales.
    impact: "Direct financial losses via fraudulent payouts and erosion of trust in marketplace accounting."
    seed: "Expose a webhook endpoint that accepts sale events and immediately credits vendor balances without verifying HMAC or source IP."
    seed_data:
      vendors:
        - id: 77
          name: 'Acme Supplies'
          balance: 0
    severity: critical
    detection_hints:
      - webhook calls from unexpected IPs
      - vendor balances increasing without corresponding orders
    remediation: "Sign webhooks with HMAC secrets, verify source IPs, and reconcile events with order records."

  - id: BL-012
    title: Coupon Brute-force (Predictable Codes)
    category: business_logic
    route: /apply-coupon
    method: POST
    description: "Short or sequential coupon codes combined with lack of rate-limiting enable brute-force discovery."
    bug: "System accepts predictable coupon patterns and does not throttle attempts."
    scenario: |
      An attacker scripts requests trying sequential codes (SAVE10, SAVE11, ...) and discovers valid coupons at scale.
    impact: "Large-scale coupon exploitation leading to revenue loss."
    seed: "Create a coupon generator that uses short, sequential codes and provide an apply endpoint without rate limiting."
    severity: medium
    detection_hints:
      - high rate of coupon checks from same IPs
      - many failed attempts followed by occasional success
    remediation: "Use long, random coupon codes, CAPTCHAs for attempts, and rate-limiting."

  - id: BL-013
    title: Improper Authorization on Admin/Support Tools
    category: business_logic
    route: /support/adjust_balance
    method: POST
    description: "Support/admin APIs lack backend role checks and can be called by any authenticated user."
    bug: "No server-side enforcement of staff-only permissions on support endpoints."
    scenario: |
      A normal user calls `/support/adjust_balance {user_id: 2, delta: 100}` and their request succeeds because the API
      only checks for authentication, not specific staff roles.
    impact: "Account manipulation, fraudulent balance changes, and internal abuse."
    seed: "Implement support endpoints accessible to authenticated users but omit role validation logic."
    severity: critical
    detection_hints:
      - privileged actions performed by non-privileged accounts
      - lack of role checks in request logs
    remediation: "Enforce RBAC on backend and audit all support actions."

  - id: BL-014
    title: Refund-to-Alternate-Payment (Payment Instrument Swap)
    category: business_logic
    route: /refund
    method: POST
    description: "Refund destination is accepted from request and honored without verifying original payment instrument."
    bug: "Server processes refunds to `refund_account` provided by the client instead of the original payment method."
    scenario: |
      An attacker requests a refund and supplies their own payment account as `refund_account`. The system sends funds to the attacker
      rather than the original payer.
    impact: "Funds diverted to attacker-controlled accounts, resulting in direct financial loss."
    seed: "Allow `refund_account` parameter on refund endpoint and process it without validating against the original transaction."
    severity: critical
    detection_hints:
      - refunds sent to accounts not matching original payment records
      - addition of many new refund destinations
    remediation: "Restrict refunds to original payment instruments or require strong verification for changes."

  - id: BL-015
    title: Abuse of Trial Periods / Multi-accounting
    category: business_logic
    route: /trial/activate, /signup
    method: POST
    description: "Trial activations are easy to repeat using disposable emails and cleared cookies; no device or payment checks."
    bug: "No throttling, device fingerprinting, or payment-card binding on trial activation."
    scenario: |
      Attackers create many disposable-email accounts to repeatedly claim trials, stacking free usage over long periods.
    impact: "Sustained unauthorized free access to paid features and inflated user metrics."
    seed: "Allow trial signups with email-only verification, no rate-limiting, and no device fingerprinting."
    severity: medium
    detection_hints:
      - many trials from same IP ranges or device fingerprints
      - rapid account churn for trial accounts
    remediation: "Bind trials to phone or card verification, use device fingerprinting, and apply throttling and fraud scoring."

  - id: BL-016
    title: Insecure Shipping / Address Change after Dispatch
    category: business_logic
    route: /orders/{order_id}/change_address
    method: POST
    description: "Address changes are permitted after dispatch without verification, enabling interception of shipments."
    bug: "Server accepts address changes for dispatched orders with no MFA, support approval, or courier verification."
    scenario: |
      A user changes the shipping address after dispatch and redirects delivery to an address they control, enabling theft of goods.
    impact: "Order theft, chargebacks, and customer disputes."
    seed: "Expose `/orders/{id}/change_address` that accepts a new address and updates orders regardless of dispatch status."
    severity: high
    detection_hints:
      - address changes on dispatched orders
      - multiple address changes from new devices or IPs
    remediation: "Disallow or require multi-party verification for post-dispatch address changes; tie changes to courier tracking."

  - id: BL-017
    title: Reward for Referrals That Can Be Self-Referred
    category: business_logic
    route: /signup?ref=<code>
    method: POST
    description: "Referral credits awarded based solely on presence of code; no uniqueness or anti-abuse checks."
    bug: "System credits both referrer and referee immediately without validating uniqueness or preventing self-referral."
    scenario: |
      A user creates multiple fake accounts and uses their referral code to self-refer, collecting referral credits repeatedly.
    impact: "Fraudulent credit accumulation and abuse of referral incentives."
    seed: "Implement referral signup that credits both accounts on signup without checking device/IP uniqueness or requiring first purchase."
    severity: medium
    detection_hints:
      - many referrals credited from same IP/device
      - rapid sequence of referrals for same referrer
    remediation: "Require first purchase for reward, limit referrals per device/IP, and add fraud scoring."

  - id: BL-018
    title: Mix-up of Test & Production Flags
    category: business_logic
    route: any
    method: ANY
    description: "Production honors client-sent test flags (e.g., `X-Test-Mode`) allowing test-only behavior in prod."
    bug: "Server accepts and acts on client-provided test flags to enable discounted or free flows."
    scenario: |
      An attacker sends `X-Test-Mode: true` header to production endpoints and receives test discounts or free access reserved for QA. 
    impact: "Free access or discounted transactions in production, leading to revenue loss and policy confusion."
    seed: "Implement endpoints that check `X-Test-Mode` and grant test benefits when present."
    severity: critical
    detection_hints:
      - production logs containing test headers
      - unusual transactions with test metadata
    remediation: "Ignore client-sent test flags in production; control features via server-side flags."

  - id: BL-019
    title: Lack of Financial Reconciliation Checks
    category: business_logic
    route: /webhooks/payment
    method: POST
    description: "Payment webhooks are accepted without signature verification or reconciliation with the payment provider."
    bug: "System marks orders paid based solely on incoming webhook payload with no signature verification or cross-check."
    scenario: |
      An attacker crafts a fake `POST /webhooks/payment` payload marking `order_id` as paid, and the system fulfills the order without
      verifying with the payment provider.
    impact: "Fake payments accepted, leading to fulfillment without real funds and potential chargebacks."
    seed: "Create a webhook endpoint that marks orders paid on receipt of payload without verifying provider signatures or reconciling records."
    severity: critical
    detection_hints:
      - webhooks from unexpected IPs
      - orders marked paid with no record in payment provider dashboard
    remediation: "Verify webhook signatures, reconcile with provider APIs, and use idempotency and replay protection."

  - id: BL-020
    title: Escrow / Marketplace Release Logic Flaw
    category: business_logic
    route: /orders/{order_id}/confirm-delivery
    method: POST
    description: "Funds are released to sellers when buyer calls confirm-delivery endpoint; confirmations can be spoofed."
    bug: "System releases escrow solely on buyer-sent confirmation without independent verification."
    scenario: |
      An attacker or malicious seller triggers a buyer-like confirmation request (or forces a buyer to click) and the system releases
      funds to the seller even though goods were not delivered.
    impact: "Sellers receive funds without delivering goods; marketplace faces fraud and disputes."
    seed: "Implement a buyer confirmation endpoint that triggers escrow release immediately upon receiving a POST."
    severity: high
    detection_hints:
      - escrow releases without delivery tracking events
      - confirmations coming from unusual IPs/devices
    remediation: "Require courier/webhook verification, time locks, or hold funds until independent delivery proofs are available."

## Architecture

# Core structure
app/
├── routes/
│   ├── technical/
│   │   ├── tech_001_sq.py
│   │   ├── tech_002_xs.py
│   │   ├── tech_003_id.py
│   │   └── ...
│   ├── business_logic/
│   │   ├── price_manipulation.py
│   │   ├── coupon_abuse.py
│   │   └── ...
│   └── admin/
├── middleware/
│   ├── feature_flags.py
│   └── security_headers.py
├── database/
│   ├── models.py
│   └── seed_data.py
└── config/
    ├── vulnerabilities.py
    └── feature_flags.py

## Seed Data Management:

It is good to use a database file as a seed to create a sqlite db:

```
# database/seed_data.py
def create_test_data():
    users = [
        {"id": 1, "email": "alice@example.com", "password": "password123", "role": "user"},
        {"id": 2, "email": "bob@example.com", "password": "hunter2", "role": "user"},
        {"id": 3, "email": "admin@example.com", "password": "admin123", "role": "admin"}
    ]
    # ... all other seed data from your manifest
```

