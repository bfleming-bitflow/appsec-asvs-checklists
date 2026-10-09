# Laravel verification checklist

<!-- Generated from checklists/laravel.yml by tools/checklist.py. Do not edit by hand. -->

Verification checklist for Laravel applications (Laravel 11 and later, PHP 8.2 and later), covering server-rendered Blade applications and JSON APIs authenticated with sessions, Laravel Sanctum, Laravel Passport or third-party JWT packages.

| Property | Value |
| --- | --- |
| Standard | [OWASP ASVS 5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0_release/5.0) |
| API risks | [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) |
| Scope | all levels |
| Items | 56 (L1: 28, L2: 27, L3: 1) |

Requirement summaries are paraphrased. The official ASVS text is authoritative; consult it before recording a result.

## Contents

- [Authentication](#authentication) (11)
- [Session management](#session-management) (10)
- [Access control](#access-control) (8)
- [API tokens](#api-tokens) (5)
- [Input validation and output encoding](#input-validation-and-output-encoding) (13)
- [API and web service configuration](#api-and-web-service-configuration) (9)

## Summary

| ID | Title | ASVS | Level | API Top 10 |
| --- | --- | --- | --- | --- |
| [LAR-AUTHN-001](#lar-authn-001-minimum-password-length-is-enforced-server-side) | Minimum password length is enforced server-side | V6.2.1 | L1 | API2:2023 |
| [LAR-AUTHN-002](#lar-authn-002-no-character-composition-rules-are-imposed) | No character composition rules are imposed | V6.2.5 | L1 | API2:2023 |
| [LAR-AUTHN-003](#lar-authn-003-new-passwords-are-checked-against-breached-password-data) | New passwords are checked against breached password data | V6.2.12 | L2 | API2:2023 |
| [LAR-AUTHN-004](#lar-authn-004-long-passwords-are-accepted-and-verified-without-truncation) | Long passwords are accepted and verified without truncation | V6.2.9 | L2 | API2:2023 |
| [LAR-AUTHN-005](#lar-authn-005-passwords-are-stored-with-an-approved-password-hashing-function) | Passwords are stored with an approved password hashing function | V11.4.2 | L2 | - |
| [LAR-AUTHN-006](#lar-authn-006-login-is-protected-against-brute-force-and-credential-stuffing) | Login is protected against brute force and credential stuffing | V6.3.1 | L1 | API2:2023, API4:2023 |
| [LAR-AUTHN-007](#lar-authn-007-authentication-responses-do-not-reveal-whether-an-account-exists) | Authentication responses do not reveal whether an account exists | V6.3.8 | L3 | API2:2023 |
| [LAR-AUTHN-008](#lar-authn-008-no-default-or-seeded-accounts-exist-in-production) | No default or seeded accounts exist in production | V6.3.2 | L1 | - |
| [LAR-AUTHN-009](#lar-authn-009-password-reset-does-not-bypass-multi-factor-authentication) | Password reset does not bypass multi-factor authentication | V6.4.3 | L2 | API2:2023 |
| [LAR-AUTHN-010](#lar-authn-010-one-time-passwords-cannot-be-replayed) | One-time passwords cannot be replayed | V6.5.1 | L2 | API2:2023 |
| [LAR-AUTHN-011](#lar-authn-011-authentication-events-are-logged) | Authentication events are logged | V16.3.1 | L2 | - |
| [LAR-SESS-001](#lar-sess-001-session-identifier-is-regenerated-on-authentication) | Session identifier is regenerated on authentication | V7.2.4 | L1 | API2:2023 |
| [LAR-SESS-002](#lar-sess-002-logout-invalidates-the-session-on-the-server) | Logout invalidates the session on the server | V7.4.1 | L1 | API2:2023 |
| [LAR-SESS-003](#lar-sess-003-session-cookie-has-the-secure-attribute-and-a-secure-prefix) | Session cookie has the Secure attribute and a secure prefix | V3.3.1 | L1 | - |
| [LAR-SESS-004](#lar-sess-004-session-cookie-is-not-readable-by-client-side-scripts) | Session cookie is not readable by client-side scripts | V3.3.4 | L2 | - |
| [LAR-SESS-005](#lar-sess-005-samesite-is-set-according-to-cookie-purpose) | SameSite is set according to cookie purpose | V3.3.2 | L2 | - |
| [LAR-SESS-006](#lar-sess-006-inactivity-timeout-enforces-re-authentication) | Inactivity timeout enforces re-authentication | V7.3.1 | L2 | - |
| [LAR-SESS-007](#lar-sess-007-absolute-session-lifetime-is-enforced) | Absolute session lifetime is enforced | V7.3.2 | L2 | - |
| [LAR-SESS-008](#lar-sess-008-other-sessions-can-be-terminated-after-a-credential-change) | Other sessions can be terminated after a credential change | V7.4.3 | L2 | - |
| [LAR-SESS-009](#lar-sess-009-sensitive-account-changes-require-re-authentication) | Sensitive account changes require re-authentication | V7.5.1 | L2 | API2:2023 |
| [LAR-SESS-010](#lar-sess-010-disabling-an-account-terminates-its-sessions-and-tokens) | Disabling an account terminates its sessions and tokens | V7.4.2 | L1 | API2:2023 |
| [LAR-AUTHZ-001](#lar-authz-001-function-level-access-requires-explicit-permission) | Function-level access requires explicit permission | V8.2.1 | L1 | API5:2023 |
| [LAR-AUTHZ-002](#lar-authz-002-object-level-access-is-checked-for-every-record) | Object-level access is checked for every record | V8.2.2 | L1 | API1:2023 |
| [LAR-AUTHZ-003](#lar-authz-003-field-level-write-access-is-restricted) | Field-level write access is restricted | V8.2.3 | L2 | API3:2023 |
| [LAR-AUTHZ-004](#lar-authz-004-mass-assignment-is-limited-to-intended-fields) | Mass assignment is limited to intended fields | V15.3.3 | L2 | API3:2023 |
| [LAR-AUTHZ-005](#lar-authz-005-responses-return-only-the-fields-the-consumer-needs) | Responses return only the fields the consumer needs | V15.3.1 | L1 | API3:2023 |
| [LAR-AUTHZ-006](#lar-authz-006-authorization-is-enforced-on-the-server-not-the-client) | Authorization is enforced on the server, not the client | V8.3.1 | L1 | API5:2023 |
| [LAR-AUTHZ-007](#lar-authz-007-tenant-isolation-is-enforced-on-every-query) | Tenant isolation is enforced on every query | V8.4.1 | L2 | API1:2023 |
| [LAR-AUTHZ-008](#lar-authz-008-failed-authorization-attempts-are-logged) | Failed authorization attempts are logged | V16.3.2 | L2 | - |
| [LAR-TOKEN-001](#lar-token-001-reference-tokens-are-random-unique-and-stored-hashed) | Reference tokens are random, unique and stored hashed | V7.2.3 | L1 | API2:2023 |
| [LAR-TOKEN-002](#lar-token-002-self-contained-tokens-are-verified-before-use) | Self-contained tokens are verified before use | V9.1.1 | L1 | API2:2023 |
| [LAR-TOKEN-003](#lar-token-003-token-algorithms-are-restricted-to-an-allowlist) | Token algorithms are restricted to an allowlist | V9.1.2 | L1 | API2:2023 |
| [LAR-TOKEN-004](#lar-token-004-token-validity-period-is-enforced) | Token validity period is enforced | V9.2.1 | L1 | API2:2023 |
| [LAR-TOKEN-005](#lar-token-005-tokens-are-accepted-only-by-their-intended-audience) | Tokens are accepted only by their intended audience | V9.2.3 | L2 | API2:2023 |
| [LAR-INPUT-001](#lar-input-001-request-input-is-validated-against-positive-rules) | Request input is validated against positive rules | V2.2.1 | L1 | - |
| [LAR-INPUT-002](#lar-input-002-only-validated-input-reaches-business-logic) | Only validated input reaches business logic | V2.2.2 | L1 | - |
| [LAR-INPUT-003](#lar-input-003-blade-output-is-encoded-for-its-context) | Blade output is encoded for its context | V1.2.1 | L1 | - |
| [LAR-INPUT-004](#lar-input-004-data-embedded-in-javascript-is-json-encoded) | Data embedded in JavaScript is JSON-encoded | V1.2.3 | L1 | - |
| [LAR-INPUT-005](#lar-input-005-database-queries-are-parameterized) | Database queries are parameterized | V1.2.4 | L1 | - |
| [LAR-INPUT-006](#lar-input-006-operating-system-commands-are-not-built-from-input) | Operating system commands are not built from input | V1.2.5 | L1 | - |
| [LAR-INPUT-007](#lar-input-007-rich-text-html-is-sanitized-with-a-maintained-library) | Rich-text HTML is sanitized with a maintained library | V1.3.1 | L1 | - |
| [LAR-INPUT-008](#lar-input-008-dynamic-code-execution-is-not-used-with-input) | Dynamic code execution is not used with input | V1.3.2 | L1 | - |
| [LAR-INPUT-009](#lar-input-009-untrusted-data-is-not-deserialized-with-unserialize) | Untrusted data is not deserialized with unserialize() | V1.5.2 | L2 | - |
| [LAR-INPUT-010](#lar-input-010-xml-parsers-do-not-resolve-external-entities) | XML parsers do not resolve external entities | V1.5.1 | L1 | - |
| [LAR-INPUT-011](#lar-input-011-comparisons-are-type-strict) | Comparisons are type-strict | V15.3.5 | L2 | - |
| [LAR-INPUT-012](#lar-input-012-templates-are-never-compiled-from-user-input) | Templates are never compiled from user input | V1.3.7 | L2 | - |
| [LAR-INPUT-013](#lar-input-013-outbound-requests-to-user-supplied-urls-are-restricted) | Outbound requests to user-supplied URLs are restricted | V1.3.6 | L2 | API7:2023, API10:2023 |
| [LAR-API-001](#lar-api-001-endpoints-are-rate-limited-per-consumer) | Endpoints are rate limited per consumer | V2.4.1 | L2 | API4:2023, API6:2023 |
| [LAR-API-002](#lar-api-002-cors-allows-only-trusted-origins) | CORS allows only trusted origins | V3.4.2 | L1 | API8:2023 |
| [LAR-API-003](#lar-api-003-responses-declare-an-accurate-content-type) | Responses declare an accurate Content-Type | V4.1.1 | L1 | API8:2023 |
| [LAR-API-004](#lar-api-004-errors-return-generic-messages-in-production) | Errors return generic messages in production | V16.5.1 | L2 | API8:2023 |
| [LAR-API-005](#lar-api-005-documentation-and-monitoring-endpoints-are-not-publicly-exposed) | Documentation and monitoring endpoints are not publicly exposed | V13.4.5 | L2 | API9:2023 |
| [LAR-API-006](#lar-api-006-client-ip-and-scheme-are-derived-from-trusted-proxies-only) | Client IP and scheme are derived from trusted proxies only | V15.3.4 | L2 | API8:2023 |
| [LAR-API-007](#lar-api-007-source-control-metadata-and-environment-files-are-not-served) | Source control metadata and environment files are not served | V13.4.1 | L1 | API8:2023 |
| [LAR-API-008](#lar-api-008-graphql-queries-are-limited-in-depth-and-cost) | GraphQL queries are limited in depth and cost | V4.3.1 | L2 | API4:2023 |
| [LAR-API-009](#lar-api-009-websocket-handshakes-validate-the-origin-header) | WebSocket handshakes validate the Origin header | V4.4.2 | L2 | API8:2023 |

## Authentication

Covers password policy, credential storage, brute-force resistance and account lifecycle. Starter kits (Breeze, Jetstream, Fortify) implement part of this; verify the code that is actually deployed rather than the starter kit defaults.

### LAR-AUTHN-001 Minimum password length is enforced server-side

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.2.1 (L1), V6 Authentication / V6.2 Password Security |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** User-chosen passwords must be at least 8 characters; 15 or more is strongly recommended.

**How to verify in Laravel.**

- Locate the password rule used by registration, password change and password reset
  (FormRequest classes, `Validator::make` calls, Fortify `PasswordValidationRules`).
- Prefer defining the policy once with `Password::defaults(fn () => ...)` in a service
  provider and referencing it with `Password::defaults()` in every rule set, so the
  three flows cannot drift apart.
- Confirm the effective minimum is `Password::min(8)` or higher.
- Submit a 7-character password to each flow and confirm a 422 response.

**Evidence.** Path and line of the `Password::defaults()` definition and of each rule set that uses it; request/response pair showing rejection of a short password.

### LAR-AUTHN-002 No character composition rules are imposed

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.2.5 (L1), V6 Authentication / V6.2 Password Security |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Passwords of any composition are accepted; there is no requirement for upper or lower case letters, digits or special characters.

**How to verify in Laravel.**

- Search for `->mixedCase()`, `->letters()`, `->numbers()` and `->symbols()` on
  `Password` rules, and for custom `regex:` rules applied to password fields.
- Any of these imposes a composition rule and fails this requirement. Length and
  breached-password checks are the intended replacement.

**Evidence.** Search output (`grep -rn "mixedCase\|symbols()\|numbers()" app/`) showing no composition rules, or the rule set that was changed.

### LAR-AUTHN-003 New passwords are checked against breached password data

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.2.12 (L2), V6 Authentication / V6.2 Password Security |
| Related ASVS | V6.2.4 |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Passwords submitted at registration or change are checked against a set of breached passwords.

**How to verify in Laravel.**

- Confirm the password rule includes `->uncompromised()`. Laravel implements it with the
  Have I Been Pwned range API using k-anonymity; only a hash prefix leaves the server.
- Decide and document the behaviour when the range API is unreachable. The default
  verifier treats a failed lookup as not compromised (fail open).
- Confirm outbound HTTPS to `api.pwnedpasswords.com` is allowed from production, or
  that an offline breached-password list is used instead.

**Evidence.** Rule definition including `uncompromised()`; test or manual request showing a known breached password (for example `password123456`) is rejected.

### LAR-AUTHN-004 Long passwords are accepted and verified without truncation

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.2.9 (L2), V6 Authentication / V6.2 Password Security |
| Related ASVS | V6.2.8 |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Passwords of at least 64 characters are permitted and are verified exactly as received.

**How to verify in Laravel.**

- Check that no `max:` rule below 64 is applied to password fields.
- Laravel's default hasher is bcrypt, which only processes the first 72 bytes of input.
  A 73-byte password and its first 72 bytes produce the same hash. Either switch the
  driver to `argon2id` in `config/hashing.php`, or reject inputs longer than 72 bytes
  with an explicit error instead of silently truncating.
- Confirm no middleware or mutator trims, lowercases or otherwise transforms the
  password before hashing (`TrimStrings` excludes `password` and
  `password_confirmation` by default; check that custom field names are excluded too).

**Evidence.** `config/hashing.php` driver setting; test showing a 64-character password can be set and used to log in; `TrimStrings` exclusion list.

### LAR-AUTHN-005 Passwords are stored with an approved password hashing function

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V11.4.2 (L2), V11 Cryptography / V11.4 Hashing and Hash-based Functions |

**Requirement summary.** Passwords are stored using a computationally intensive key derivation function with parameters set according to current guidance.

**How to verify in Laravel.**

- Confirm passwords are written through `Hash::make()` or the `hashed` model cast, never
  with `md5()`, `sha1()`, `hash()` or reversible encryption.
- Review `config/hashing.php`: bcrypt cost (`BCRYPT_ROUNDS`, default 12) or Argon2id
  memory, time and thread parameters. Compare them with the OWASP Password Storage
  Cheat Sheet.
- Confirm `Hash::needsRehash()` or Laravel's automatic rehash on login is active so that
  parameter increases apply to existing users.

**Evidence.** `config/hashing.php`; the user model cast or the write path; a sample stored hash prefix (`$2y$12$` or `$argon2id$`) from a non-production database.

### LAR-AUTHN-006 Login is protected against brute force and credential stuffing

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.3.1 (L1), V6 Authentication / V6.3 General Authentication Security |
| Related ASVS | V6.1.1 |
| API Top 10 | API2:2023 Broken Authentication, API4:2023 Unrestricted Resource Consumption |

**Requirement summary.** Controls against credential stuffing and password brute force are implemented as defined in the application's security documentation.

**How to verify in Laravel.**

- Identify every credential-accepting endpoint: web login, API token issuance, password
  confirmation, two-factor challenge and password reset.
- Confirm each is rate limited. Breeze uses `LoginRequest::ensureIsNotRateLimited()`;
  Fortify uses the `login` and `two-factor` limiters; custom endpoints need
  `throttle:` middleware or `RateLimiter::attempt()`.
- The throttle key should combine the account identifier and client IP so that one
  account cannot be locked by a single source and many accounts cannot be sprayed
  from one source without limit.
- Confirm the client IP used by the limiter is correct behind proxies (see the trusted
  proxy item).

**Evidence.** Limiter definitions and route middleware; output of repeated failed logins showing HTTP 429 after the documented threshold.

### LAR-AUTHN-007 Authentication responses do not reveal whether an account exists

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.3.8 (L3), V6 Authentication / V6.3 General Authentication Security |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Valid users cannot be inferred from error messages, status codes or response timing in login, registration and password reset.

**How to verify in Laravel.**

- Login: the default message `auth.failed` is generic. Check that custom code does not
  return different messages for unknown user and wrong password.
- Password reset: `Password::sendResetLink()` returns `Password::INVALID_USER` for
  unknown addresses, and Breeze displays it as a validation error. Return the same
  response for every submitted address.
- Registration: a `unique:users,email` rule discloses existing accounts. Where this
  matters, accept the request and notify the existing account owner by email instead.
- Compare response times for existing and non-existing accounts; a missing user must
  not skip the password hash computation.

**Evidence.** Side-by-side responses (status, body, timing over repeated requests) for an existing and a non-existing account in each flow.

### LAR-AUTHN-008 No default or seeded accounts exist in production

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.3.2 (L1), V6 Authentication / V6.3 General Authentication Security |

**Requirement summary.** Default accounts such as "admin" or "root" are not present or are disabled.

**How to verify in Laravel.**

- Review `database/seeders`. The default `DatabaseSeeder` creates `test@example.com`
  and `UserFactory` uses the password `password`.
- Confirm seeders that create users are not run in production deployment scripts
  (`php artisan db:seed --force`) or are guarded by `app()->environment()` checks.
- Query the production user table for well-known addresses and names (`admin`,
  `test@example.com`, `*@example.com`).

**Evidence.** Seeder code review notes; deployment script; result of the production query (counts only, no personal data).

### LAR-AUTHN-009 Password reset does not bypass multi-factor authentication

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.4.3 (L2), V6 Authentication / V6.4 Authentication Factor Lifecycle and Recovery |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Forgotten-password recovery is secure and does not bypass any enabled multi-factor authentication.

**How to verify in Laravel.**

- Check whether the reset flow logs the user in. The `ResetsPasswords` trait from
  `laravel/ui` calls `guard()->login()` after reset; Breeze and Fortify redirect to
  the login page instead.
- If the user is logged in after reset, confirm the second factor is still required
  before an authenticated session is established.
- Confirm reset tokens expire (`auth.passwords.*.expire`, default 60 minutes) and are
  single use, and that throttling (`auth.passwords.*.throttle`) is configured.

**Evidence.** Reset controller code; recorded flow for an MFA-enabled test account showing the second factor prompt after reset.

### LAR-AUTHN-010 One-time passwords cannot be replayed

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.5.1 (L2), V6 Authentication / V6.5 General Multi-factor authentication requirements |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Lookup secrets (recovery codes), out-of-band codes and TOTP values can be used successfully only once.

**How to verify in Laravel.**

- For TOTP, submit the same valid code twice within its time window. The second
  attempt must fail. With `pragmarx/google2fa` this requires `verifyKeyNewer()` and
  persisting the last accepted timestamp; plain `verifyKey()` accepts replays.
- For recovery codes, confirm the used code is removed or replaced. Fortify replaces a
  used recovery code via `replaceRecoveryCode()`.
- For email or SMS codes, confirm the stored code is deleted on first successful use.

**Evidence.** Code path for each factor; request log showing the replayed code being rejected.

### LAR-AUTHN-011 Authentication events are logged

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V16.3.1 (L2), V16 Security Logging and Error Handling / V16.3 Security Events |

**Requirement summary.** All authentication operations, successful and unsuccessful, are logged with relevant metadata such as authentication type or factors used.

**How to verify in Laravel.**

- Confirm listeners exist for `Illuminate\Auth\Events\Login`, `Failed`, `Lockout`,
  `Logout`, `PasswordReset` and, where used, two-factor events.
- Each record should include timestamp, user identifier (or attempted identifier),
  client IP, user agent and outcome.
- Confirm passwords, tokens and session identifiers are never logged; the `Failed`
  event carries the submitted credentials array, so log only the identifier field.

**Evidence.** Listener registration and a sample log entry for a successful and a failed login from a non-production environment.

## Session management

Applies to cookie-based sessions (`web` guard and Sanctum SPA authentication). Token-based API authentication is covered in the Tokens section.

### LAR-SESS-001 Session identifier is regenerated on authentication

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.2.4 (L1), V7 Session Management / V7.2 Fundamental Session Management Security |
| API Top 10 | API2:2023 Broken Authentication |
| ZAP alerts | [40013 Session Fixation](https://www.zaproxy.org/docs/alerts/40013/) |

**Requirement summary.** A new session token is generated on authentication and re-authentication, and the previous token is terminated.

**How to verify in Laravel.**

- `SessionGuard::login()` migrates the session ID, so `Auth::attempt()` and
  `Auth::login()` comply. Breeze and Fortify additionally call
  `$request->session()->regenerate()`.
- Review custom login paths (social login callbacks, impersonation, magic links,
  `Auth::loginUsingId()`, manual `session()->put('user_id', ...)`) and confirm each
  results in a regenerated session ID.
- Test: record the session cookie before login, authenticate, confirm the value
  changed and the old value no longer authenticates.

**Evidence.** Cookie values before and after login; list of reviewed custom login paths.

### LAR-SESS-002 Logout invalidates the session on the server

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.4.1 (L1), V7 Session Management / V7.4 Session Termination |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** When a session is terminated by logout or expiry, it cannot be used again.

**How to verify in Laravel.**

- Confirm logout calls `Auth::guard('web')->logout()`,
  `$request->session()->invalidate()` and `$request->session()->regenerateToken()`.
- For Sanctum personal access tokens, confirm logout deletes the token with
  `$request->user()->currentAccessToken()->delete()`.
- Test: copy the session cookie, log out, replay a request with the copied cookie and
  confirm it is unauthenticated.

**Evidence.** Logout controller code; replay request and response after logout.

### LAR-SESS-003 Session cookie has the Secure attribute and a secure prefix

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V3.3.1 (L1), V3 Web Frontend Security / V3.3 Cookie Setup |
| Related ASVS | V3.3.3 |
| ZAP alerts | [10011 Cookie Without Secure Flag](https://www.zaproxy.org/docs/alerts/10011/) |

**Requirement summary.** Cookies have the Secure attribute; if the `__Host-` prefix is not used, the `__Secure-` prefix is used.

**How to verify in Laravel.**

- `config/session.php`: `secure` must be `true` in production (`SESSION_SECURE_COOKIE`).
- Set the cookie name (`SESSION_COOKIE`) to start with `__Host-`, which also requires
  `path` `/` and no `domain`. Use `__Secure-` only if the cookie must be shared across
  subdomains.
- Apply the same to the `XSRF-TOKEN` cookie if the frontend does not read it from a
  renamed cookie, and to any application cookies set with `cookie()`.

**Evidence.** `Set-Cookie` response headers captured from production or staging.

### LAR-SESS-004 Session cookie is not readable by client-side scripts

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V3.3.4 (L2), V3 Web Frontend Security / V3.3 Cookie Setup |
| ZAP alerts | [10010 Cookie No HttpOnly Flag](https://www.zaproxy.org/docs/alerts/10010/) |

**Requirement summary.** Cookies that client-side scripts do not need, such as session tokens, have the HttpOnly attribute.

**How to verify in Laravel.**

- `config/session.php`: `http_only` is `true` (the default).
- Confirm the session identifier is not also exposed in a response body, a JavaScript
  variable or a non-HttpOnly cookie.
- The `XSRF-TOKEN` cookie is intentionally readable; it is not a session token.

**Evidence.** `Set-Cookie` header for the session cookie showing `httponly`.

### LAR-SESS-005 SameSite is set according to cookie purpose

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V3.3.2 (L2), V3 Web Frontend Security / V3.3 Cookie Setup |
| ZAP alerts | [10054 Cookie without SameSite Attribute](https://www.zaproxy.org/docs/alerts/10054/) |

**Requirement summary.** Each cookie's SameSite value fits its purpose, limiting cross-site request forgery and UI redress exposure.

**How to verify in Laravel.**

- `config/session.php`: `same_site` defaults to `lax`. Use `strict` if no cross-site
  top-level navigation needs an authenticated session.
- `none` requires a documented reason (for example embedded third-party flows) and
  must be combined with `Secure`.
- Confirm CSRF protection (`VerifyCsrfToken` / `ValidateCsrfToken`) remains enabled
  regardless of SameSite, and review the `except` list.

**Evidence.** `Set-Cookie` headers; CSRF middleware exception list.

### LAR-SESS-006 Inactivity timeout enforces re-authentication

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.3.1 (L2), V7 Session Management / V7.3 Session Timeout |
| Related ASVS | V7.1.1 |

**Requirement summary.** An inactivity timeout forces re-authentication according to documented risk decisions.

**How to verify in Laravel.**

- `config/session.php`: `lifetime` (minutes, `SESSION_LIFETIME`) is an idle timeout;
  each request extends it. Confirm the value matches the documented decision.
- Confirm "remember me" is either disabled or its lifetime is documented, because the
  remember-me cookie re-authenticates silently after the session expires.
- Test: authenticate, stay idle beyond the configured lifetime, confirm the next
  request requires login.

**Evidence.** Configuration value; documented decision; test result.

### LAR-SESS-007 Absolute session lifetime is enforced

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.3.2 (L2), V7 Session Management / V7.3 Session Timeout |
| Related ASVS | V7.1.1 |

**Requirement summary.** An absolute maximum session lifetime forces re-authentication regardless of activity.

**How to verify in Laravel.**

- Laravel has no built-in absolute timeout. Confirm a middleware stores the
  authentication time in the session at login and logs the user out once the
  documented maximum is exceeded.
- Confirm the same limit applies to "remember me" re-authentication and to Sanctum
  tokens (`sanctum.expiration`, in minutes; `null` means tokens never expire).

**Evidence.** Middleware code and registration; `config/sanctum.php` expiration value.

### LAR-SESS-008 Other sessions can be terminated after a credential change

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.4.3 (L2), V7 Session Management / V7.4 Session Termination |

**Requirement summary.** After changing or removing an authentication factor, the user is offered the option to terminate all other active sessions.

**How to verify in Laravel.**

- `Auth::logoutOtherDevices($password)` invalidates other sessions only when the
  `AuthenticateSession` middleware (`auth.session`) is applied to authenticated routes.
  Confirm it is.
- Confirm Sanctum tokens other than the current one are revoked when requested
  (`$user->tokens()->where('id', '!=', $currentId)->delete()`).
- Confirm the `remember_token` is cycled so remembered devices are also signed out.

**Evidence.** Password change controller; middleware configuration; test with two browser sessions.

### LAR-SESS-009 Sensitive account changes require re-authentication

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.5.1 (L2), V7 Session Management / V7.5 Defenses Against Session Abuse |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Full re-authentication is required before changing attributes that affect authentication, such as email, phone, MFA configuration or recovery data.

**How to verify in Laravel.**

- Confirm routes that change email, password, MFA settings and recovery codes use the
  `password.confirm` middleware or an equivalent challenge.
- Review `auth.password_timeout` (seconds, default 10800). A three-hour window may be
  too long for high-risk changes; document the chosen value.
- For APIs, confirm the endpoint requires the current password or a fresh second
  factor in the request.

**Evidence.** Route list (`php artisan route:list -v`) showing middleware; configuration value.

### LAR-SESS-010 Disabling an account terminates its sessions and tokens

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.4.2 (L1), V7 Session Management / V7.4 Session Termination |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** All active sessions are terminated when a user account is disabled or deleted.

**How to verify in Laravel.**

- With `SESSION_DRIVER=database`, confirm the disable or delete action removes rows
  from the `sessions` table for that `user_id`. Other drivers need an equivalent
  mechanism or a per-request check of the account status.
- Confirm Sanctum tokens (`$user->tokens()->delete()`) and Passport tokens are revoked.
- Confirm the remember token is cycled.

**Evidence.** Code of the disable/delete action; test showing an existing session is rejected after the account is disabled.

## Access control

Laravel provides gates, policies and middleware, but none of them is applied implicitly. Every route and every query that returns user-scoped data needs an explicit decision.

### LAR-AUTHZ-001 Function-level access requires explicit permission

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V8.2.1 (L1), V8 Authorization / V8.2 General Authorization Design |
| API Top 10 | API5:2023 Broken Function Level Authorization |

**Requirement summary.** Access to functions is restricted to consumers with explicit permissions.

**How to verify in Laravel.**

- Export the route table (`php artisan route:list --json`) and confirm every non-public
  route has authentication middleware and an authorization check (`can:` middleware,
  `Gate::authorize()`, `$this->authorize()` or a FormRequest `authorize()` method).
- FormRequest `authorize()` returning `true` unconditionally is not an authorization
  check.
- Test administrative routes with a low-privilege account and expect HTTP 403.

**Evidence.** Route table with middleware column; list of routes intentionally public; 403 responses.

### LAR-AUTHZ-002 Object-level access is checked for every record

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V8.2.2 (L1), V8 Authorization / V8.2 General Authorization Design |
| API Top 10 | API1:2023 Broken Object Level Authorization |

**Requirement summary.** Data-specific access is restricted to consumers with explicit permissions to each data item, preventing IDOR and broken object level authorization.

**How to verify in Laravel.**

- Route model binding (`/orders/{order}`) loads any record by key. Confirm a policy
  check follows (`$this->authorize('view', $order)`) or the binding is scoped
  (`->scopeBindings()`, or querying through the relationship
  `$request->user()->orders()->findOrFail($id)`).
- Review `find()`, `findOrFail()` and `where('id', ...)` calls that take request input.
- Test with two accounts: request the other account's record identifiers and expect
  403 or 404.

**Evidence.** Policy classes and controller calls; cross-account test results.

### LAR-AUTHZ-003 Field-level write access is restricted

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V8.2.3 (L2), V8 Authorization / V8.2 General Authorization Design |
| Related ASVS | V8.1.2 |
| API Top 10 | API3:2023 Broken Object Property Level Authorization |

**Requirement summary.** Access to individual fields is restricted to consumers with explicit permissions, mitigating broken object property level authorization.

**How to verify in Laravel.**

- Identify fields that only some roles may change (`role`, `is_admin`, `status`,
  `tenant_id`, `price`, `email_verified_at`).
- Confirm validation rules for each update action list only the fields the current
  role may set, for example with conditional rules based on `$this->user()->can()`.
- Submit an update with a restricted field as a low-privilege user and confirm the
  stored value is unchanged.

**Evidence.** FormRequest rules per action; request and database state before and after the test.

### LAR-AUTHZ-004 Mass assignment is limited to intended fields

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V15.3.3 (L2), V15 Secure Coding and Architecture / V15.3 Defensive Coding |
| API Top 10 | API3:2023 Broken Object Property Level Authorization |

**Requirement summary.** Countermeasures prevent setting fields that are not intended for the given controller action.

**How to verify in Laravel.**

- Search for `$request->all()`, `$request->input()` without keys and `$request->except()`
  passed to `create()`, `update()`, `fill()` or `forceFill()`. Use
  `$request->validated()` or `$request->safe()->only([...])` instead.
- Review models with `protected $guarded = [];` or `Model::unguard()`.
- Consider `Model::preventSilentlyDiscardingAttributes()` (part of
  `Model::shouldBeStrict()`) in non-production environments to surface unexpected
  attributes during testing.

**Evidence.** Search output for the patterns above; model `$fillable` / `$guarded` definitions.

### LAR-AUTHZ-005 Responses return only the fields the consumer needs

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V15.3.1 (L1), V15 Secure Coding and Architecture / V15.3 Defensive Coding |
| API Top 10 | API3:2023 Broken Object Property Level Authorization |

**Requirement summary.** The application returns only the required subset of fields from a data object rather than the entire object.

**How to verify in Laravel.**

- Search for controllers returning models or collections directly
  (`return $user;`, `return User::all();`, `response()->json($model)`), which
  serialize every attribute not listed in `$hidden`.
- Prefer API Resources (`JsonResource`) with explicit fields, using `when()` or
  `$this->when($request->user()->can(...))` for role-dependent fields.
- Inspect responses for `password`, `remember_token`, `two_factor_secret`,
  `two_factor_recovery_codes`, internal flags and other users' data.

**Evidence.** List of API resources; sample responses from key endpoints.

### LAR-AUTHZ-006 Authorization is enforced on the server, not the client

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V8.3.1 (L1), V8 Authorization / V8.3 Operation Level Authorization |
| API Top 10 | API5:2023 Broken Function Level Authorization |

**Requirement summary.** Authorization rules are enforced at a trusted service layer and do not rely on controls the client can manipulate.

**How to verify in Laravel.**

- Hiding buttons with `@can` in Blade or with Inertia/Vue/React props is presentation
  only. Confirm every corresponding route performs its own check.
- Confirm no authorization decision uses request-supplied values such as
  `role`, `is_admin` or `user_id` from the body, query string, headers or cookies.

**Evidence.** Mapping of UI-gated actions to server-side checks; direct requests to the hidden actions with an unprivileged account.

### LAR-AUTHZ-007 Tenant isolation is enforced on every query

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V8.4.1 (L2), V8 Authorization / V8.4 Other Authorization Considerations |
| API Top 10 | API1:2023 Broken Object Level Authorization |

**Requirement summary.** In multi-tenant applications, cross-tenant controls ensure operations never affect tenants the consumer is not permitted to access.

**How to verify in Laravel.**

- Confirm tenant scoping is applied centrally, for example with a global scope on
  tenant-owned models, and that `withoutGlobalScope()` / `withoutGlobalScopes()` calls
  are reviewed and justified.
- Confirm raw queries, queued jobs, scheduled commands and exports apply the tenant
  filter, since they run outside the HTTP request context.
- Confirm `tenant_id` is never taken from request input on write.

**Evidence.** Scope implementation; search results for scope bypasses; cross-tenant test results.

### LAR-AUTHZ-008 Failed authorization attempts are logged

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V16.3.2 (L2), V16 Security Logging and Error Handling / V16.3 Security Events |

**Requirement summary.** Failed authorization attempts are logged; at L3 all authorization decisions are logged, including access to sensitive data.

**How to verify in Laravel.**

- Confirm `AuthorizationException` (rendered as 403) is reported with user, route,
  policy ability and target identifier. Laravel does not report it by default because
  it is in the internal "do not report" list, so explicit logging is needed (for
  example a `Gate::after()` callback or an exception reporting callback).
- Confirm the log entry does not contain the protected data itself.

**Evidence.** Logging code; sample log entry for a denied request.

## API tokens

Sanctum personal access tokens are reference tokens stored hashed in the database. Passport access tokens and tokens from JWT packages are self-contained and must be validated cryptographically on every request.

### LAR-TOKEN-001 Reference tokens are random, unique and stored hashed

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.2.3 (L1), V7 Session Management / V7.2 Fundamental Session Management Security |
| Related ASVS | V7.2.2 |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Reference tokens are unique, generated with a CSPRNG and have at least 128 bits of entropy.

**How to verify in Laravel.**

- Sanctum `createToken()` generates the secret with `Str::random(40)` (backed by
  `random_bytes()`) and stores only its SHA-256 hash. Confirm tokens are not created
  by custom code with `uniqid()`, `rand()`, `mt_rand()` or predictable values.
- Confirm no static, shared API keys are used in place of per-user tokens.
- Confirm the plain-text token is shown once and not stored or logged.

**Evidence.** Token creation code; `personal_access_tokens` table schema showing a hashed token column.

### LAR-TOKEN-002 Self-contained tokens are verified before use

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V9.1.1 (L1), V9 Self-contained Tokens / V9.1 Token source and integrity |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Self-contained tokens are validated using their digital signature or MAC before their contents are accepted.

**How to verify in Laravel.**

- Passport validates its access tokens in `TokenGuard`. Confirm no code decodes a JWT
  payload with `base64_decode()` or `explode('.', $token)` to read claims.
- With `firebase/php-jwt`, confirm claims are only read from the result of
  `JWT::decode()`.
- Test: alter one character of the payload and expect HTTP 401.

**Evidence.** Token verification code path; response to a tampered token.

### LAR-TOKEN-003 Token algorithms are restricted to an allowlist

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V9.1.2 (L1), V9 Self-contained Tokens / V9.1 Token source and integrity |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Only allowlisted algorithms can be used to create and verify self-contained tokens, and the `none` algorithm is never accepted.

**How to verify in Laravel.**

- `firebase/php-jwt` 6.x requires a `Key` object that binds a key to one algorithm
  (`new Key($publicKey, 'RS256')`). Confirm the algorithm is a constant, not a value
  read from the token header.
- For `php-open-source-saver/jwt-auth` or `tymon/jwt-auth`, confirm `JWT_ALGO` is set
  explicitly and that symmetric and asymmetric keys are not mixed.
- Test: submit a token with `alg` set to `none` and to `HS256` signed with the public
  key; both must be rejected.

**Evidence.** Configuration and verification code; responses to the two test tokens.

### LAR-TOKEN-004 Token validity period is enforced

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V9.2.1 (L1), V9 Self-contained Tokens / V9.2 Token content |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** If a token carries a validity period, it is accepted only while the verification time falls within it.

**How to verify in Laravel.**

- Confirm issued tokens include `exp` and that verification rejects expired tokens.
  `firebase/php-jwt` enforces `exp` and `nbf` when present; check `JWT::$leeway` is a
  small value.
- Passport: review `Passport::tokensExpireIn()` and `refreshTokensExpireIn()`; the
  defaults are long-lived.
- Sanctum (reference tokens): set `sanctum.expiration` or per-token `expires_at`.

**Evidence.** Configured lifetimes; response to an expired test token.

### LAR-TOKEN-005 Tokens are accepted only by their intended audience

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V9.2.3 (L2), V9 Self-contained Tokens / V9.2 Token content |
| Related ASVS | V9.2.2 |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** A service accepts only tokens intended for it, for example by validating the JWT `aud` claim against an allowlist.

**How to verify in Laravel.**

- If several services trust the same issuer or key, confirm each validates `aud`
  (and `iss`) explicitly. `firebase/php-jwt` does not check `aud`; compare it in
  application code after decoding.
- For Passport, confirm client scopes are checked with the `scopes` / `scope`
  middleware so a token issued for one client purpose cannot call unrelated routes.

**Evidence.** Audience and issuer checks in code; response to a token minted for another audience.

## Input validation and output encoding

Validation enforces expected structure; encoding and parameterization prevent injection. Neither replaces the other.

### LAR-INPUT-001 Request input is validated against positive rules

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V2.2.1 (L1), V2 Validation and Business Logic / V2.2 Input Validation |
| Related ASVS | V2.1.1 |

**Requirement summary.** Input is validated against business expectations using allowlists of values, patterns and ranges, or against expected structure and logical limits.

**How to verify in Laravel.**

- Confirm each state-changing endpoint uses a FormRequest or `$request->validate()`
  with rules covering type, length and format for every accepted field.
- Prefer `Rule::in()`, `Rule::enum()`, `integer`, `uuid`, `date_format` and `max:` over
  free-form `string` rules.
- Confirm validation also covers array input (`items.*.quantity`) and nested JSON.

**Evidence.** List of FormRequest classes per endpoint; examples of rejected invalid payloads.

### LAR-INPUT-002 Only validated input reaches business logic

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V2.2.2 (L1), V2 Validation and Business Logic / V2.2 Input Validation |

**Requirement summary.** Input validation is enforced at a trusted service layer; client-side validation is not relied upon.

**How to verify in Laravel.**

- Confirm controllers pass `$request->validated()` or `$request->safe()` to services,
  not `$request->all()` or `$request->input()`.
- Confirm HTML5 attributes and frontend validation (Livewire, Inertia, Vue) are
  mirrored by server-side rules. Livewire public properties are client-modifiable and
  need `#[Validate]` rules or explicit checks.

**Evidence.** Search results for `$request->all()`; Livewire component rules.

### LAR-INPUT-003 Blade output is encoded for its context

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.2.1 (L1), V1 Encoding and Sanitization / V1.2 Injection Prevention |
| ZAP alerts | [40012 Cross Site Scripting (Reflected)](https://www.zaproxy.org/docs/alerts/40012/), [40014 Cross Site Scripting (Persistent)](https://www.zaproxy.org/docs/alerts/40014/) |

**Requirement summary.** Output encoding for HTML elements, attributes, comments, CSS and HTTP headers matches the context in which the data is placed.

**How to verify in Laravel.**

- `{{ }}` applies `htmlspecialchars` and is safe for HTML element content and quoted
  attributes. Search for raw output `{!! !!}` and `@php echo` and confirm each value is
  trusted or sanitized.
- `{{ }}` is not sufficient in unquoted attributes, `href`/`src` (use a scheme
  allowlist to block `javascript:` URLs), inline event handlers or `<style>` blocks.
- Review `HtmlString` and `new HtmlString()` usages, which bypass escaping.

**Evidence.** `grep -rn "{!!" resources/views` output with a justification per occurrence.

### LAR-INPUT-004 Data embedded in JavaScript is JSON-encoded

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.2.3 (L1), V1 Encoding and Sanitization / V1.2 Injection Prevention |
| ZAP alerts | [40012 Cross Site Scripting (Reflected)](https://www.zaproxy.org/docs/alerts/40012/) |

**Requirement summary.** Output encoding is used when building JavaScript or JSON content so that data cannot change the structure of the script.

**How to verify in Laravel.**

- Confirm data passed to inline scripts uses `@json($value)` or `Js::from($value)`,
  which escape characters such as `<`, `>` and quotes.
- Search for `var x = '{{ $value }}'` and `{!! json_encode(...) !!}` patterns;
  HTML-escaping does not protect JavaScript string contexts.

**Evidence.** Search results for inline script blocks in `resources/views`.

### LAR-INPUT-005 Database queries are parameterized

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.2.4 (L1), V1 Encoding and Sanitization / V1.2 Injection Prevention |
| ZAP alerts | [40018 SQL Injection](https://www.zaproxy.org/docs/alerts/40018/) |

**Requirement summary.** Database queries use parameterized queries or an ORM, and are protected from SQL and other database injection.

**How to verify in Laravel.**

- Eloquent and the query builder bind values. Review raw expressions: `DB::raw()`,
  `whereRaw()`, `selectRaw()`, `orderByRaw()`, `havingRaw()`, `DB::statement()`,
  `DB::select()`. Each must use `?` bindings, never string interpolation.
- Column and direction names cannot be bound. Confirm `orderBy($request->sort)` and
  similar calls validate against an allowlist.
- Confirm JSON path arguments (`where('meta->' . $key, ...)`) are allowlisted.

**Evidence.** Search output for `Raw(` and `DB::` calls with review notes.

### LAR-INPUT-006 Operating system commands are not built from input

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.2.5 (L1), V1 Encoding and Sanitization / V1.2 Injection Prevention |
| ZAP alerts | [90020 Remote OS Command Injection](https://www.zaproxy.org/docs/alerts/90020/) |

**Requirement summary.** The application protects against OS command injection by using parameterized OS calls or contextual command-line encoding.

**How to verify in Laravel.**

- Search for `exec`, `shell_exec`, `system`, `passthru`, `proc_open`, `popen` and
  backticks.
- Prefer `Process::run([...])` or Symfony `Process` with an argument array, which does
  not invoke a shell. A string command passed to `Process::run()` is interpreted by
  the shell.
- Where a shell string is unavoidable, confirm each argument goes through
  `escapeshellarg()` and that option injection (`--`) is prevented.

**Evidence.** Search output with review notes per call site.

### LAR-INPUT-007 Rich-text HTML is sanitized with a maintained library

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.3.1 (L1), V1 Encoding and Sanitization / V1.3 Sanitization |
| ZAP alerts | [40014 Cross Site Scripting (Persistent)](https://www.zaproxy.org/docs/alerts/40014/) |

**Requirement summary.** Untrusted HTML from WYSIWYG editors or similar is sanitized with a well-known sanitization library or framework feature.

**How to verify in Laravel.**

- Confirm stored rich text is sanitized with an allowlist-based library such as
  `symfony/html-sanitizer` or HTML Purifier (`mews/purifier`), either on input or
  immediately before output with `{!! !!}`.
- Regex-based or `strip_tags()`-based filtering does not meet this requirement;
  `strip_tags()` with an allowed-tags list keeps dangerous attributes.

**Evidence.** Sanitizer configuration and call sites; test payloads that are neutralized.

### LAR-INPUT-008 Dynamic code execution is not used with input

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.3.2 (L1), V1 Encoding and Sanitization / V1.3 Sanitization |
| ZAP alerts | [90019 Server Side Code Injection](https://www.zaproxy.org/docs/alerts/90019/) |

**Requirement summary.** The application avoids `eval()` and other dynamic code execution; where unavoidable, input is sanitized first.

**How to verify in Laravel.**

- Search for `eval(`, `assert(` with string arguments, `create_function`,
  `call_user_func` / `call_user_func_array` and variable functions (`$fn()`) whose
  name comes from input, and `include` / `require` with input-derived paths.
- Confirm dynamic dispatch uses an explicit allowlist mapping.

**Evidence.** Search output with review notes.

### LAR-INPUT-009 Untrusted data is not deserialized with unserialize()

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.5.2 (L2), V1 Encoding and Sanitization / V1.5 Safe Deserialization |

**Requirement summary.** Deserialization of untrusted data restricts object types to prevent deserialization attacks.

**How to verify in Laravel.**

- Search for `unserialize(` on any value an attacker can influence (cookies, request
  data, cache entries shared with other systems). Use `json_decode()`, or pass
  `['allowed_classes' => false]`.
- `Crypt::decrypt()` unserializes by default; use `Crypt::decryptString()` for string
  payloads. A leaked `APP_KEY` turns any `decrypt()` sink into object injection, so
  confirm the key is not in the repository and is rotated if it was ever exposed.
- Review `phar://` handling in file operations on user-supplied paths.

**Evidence.** Search output; confirmation of `APP_KEY` storage location.

### LAR-INPUT-010 XML parsers do not resolve external entities

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.5.1 (L1), V1 Encoding and Sanitization / V1.5 Safe Deserialization |
| ZAP alerts | [90023 XML External Entity Attack](https://www.zaproxy.org/docs/alerts/90023/) |

**Requirement summary.** XML parsers use a restrictive configuration with external entity resolution disabled, preventing XXE.

**How to verify in Laravel.**

- With PHP 8 and libxml2 2.9 or later, external entity loading is disabled by default.
  Search for `LIBXML_NOENT`, `LIBXML_DTDLOAD` and `LIBXML_DTDATTR` passed to
  `simplexml_load_string()`, `DOMDocument::loadXML()` or `XMLReader`, which re-enable
  entity processing.
- Confirm third-party XML, SVG, SAML and spreadsheet libraries in use do not enable
  these flags.

**Evidence.** Search output; libxml version (`php -i | grep -i libxml`).

### LAR-INPUT-011 Comparisons are type-strict

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V15.3.5 (L2), V15 Secure Coding and Architecture / V15.3 Defensive Coding |

**Requirement summary.** Variables are checked for the correct type and comparisons use strict equality, avoiding type juggling.

**How to verify in Laravel.**

- Search for `==` and `!=` comparisons involving tokens, hashes, roles or identifiers.
  Loose comparison treats numeric strings such as `"0e123"` and `"0e456"` as equal.
- Confirm secrets are compared with `hash_equals()`, and `in_array()` /
  `array_search()` use the strict third argument where types matter.
- Consider `declare(strict_types=1);` and a static analyser (PHPStan or Psalm) rule
  set that flags loose comparisons.

**Evidence.** Search output with review notes; static analysis configuration.

### LAR-INPUT-012 Templates are never compiled from user input

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.3.7 (L2), V1 Encoding and Sanitization / V1.3 Sanitization |
| ZAP alerts | [90035 Server Side Template Injection](https://www.zaproxy.org/docs/alerts/90035/) |

**Requirement summary.** Templates are not built from untrusted input; where unavoidable, input is sanitized or sandboxed.

**How to verify in Laravel.**

- Search for `Blade::render()`, `Blade::compileString()` and `view()->make()` with
  input-derived template content or names. Blade compiles to PHP, so user-controlled
  template strings lead to code execution.
- User-editable templates (emails, notifications) should use a logic-less engine with
  a fixed variable set instead of Blade.

**Evidence.** Search output; description of how user-editable templates are rendered.

### LAR-INPUT-013 Outbound requests to user-supplied URLs are restricted

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.3.6 (L2), V1 Encoding and Sanitization / V1.3 Sanitization |
| Related ASVS | V15.3.2 |
| API Top 10 | API7:2023 Server Side Request Forgery, API10:2023 Unsafe Consumption of APIs |
| ZAP alerts | [40046 Server Side Request Forgery](https://www.zaproxy.org/docs/alerts/40046/) |

**Requirement summary.** The application protects against SSRF by validating untrusted data against an allowlist of protocols, domains, paths and ports.

**How to verify in Laravel.**

- Locate `Http::` calls, Guzzle clients, `file_get_contents()` and `fopen()` whose URL
  includes input (webhooks, URL previews, imports, avatar fetching).
- Confirm the scheme is limited to `https`, the host is allowlisted or resolved and
  checked against private, loopback and link-local ranges (including
  `169.254.169.254`), and the check uses the resolved address that is actually
  connected to.
- Confirm redirects are disabled (`Http::withOptions(['allow_redirects' => false])`)
  or each hop is re-validated.

**Evidence.** Call sites and validation code; test results against internal addresses.

## API and web service configuration

Configuration items that apply to JSON APIs and to the HTTP surface of the application.

### LAR-API-001 Endpoints are rate limited per consumer

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V2.4.1 (L2), V2 Validation and Business Logic / V2.4 Anti-automation |
| API Top 10 | API4:2023 Unrestricted Resource Consumption, API6:2023 Unrestricted Access to Sensitive Business Flows |

**Requirement summary.** Anti-automation controls protect against excessive calls that could cause data exfiltration, garbage data, quota exhaustion or denial of service.

**How to verify in Laravel.**

- Confirm a limiter is defined (`RateLimiter::for('api', ...)`) keyed by user ID for
  authenticated requests and by IP otherwise, and applied with `throttle:api`.
- Confirm stricter, dedicated limiters exist for expensive or abusable flows: exports,
  search, SMS or email sending, checkout, invitation and signup.
- Confirm the cache store backing the limiter is shared across application instances
  (Redis or database, not `array` or per-node `file`).

**Evidence.** Limiter definitions; route middleware; 429 response with `Retry-After` header.

### LAR-API-002 CORS allows only trusted origins

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V3.4.2 (L1), V3 Web Frontend Security / V3.4 Browser Security Mechanism Headers |
| API Top 10 | API8:2023 Security Misconfiguration |
| ZAP alerts | [40040 CORS Header](https://www.zaproxy.org/docs/alerts/40040/), [10098 Cross-Domain Misconfiguration](https://www.zaproxy.org/docs/alerts/10098/) |

**Requirement summary.** The `Access-Control-Allow-Origin` header is a fixed value, or the request Origin is validated against an allowlist of trusted origins.

**How to verify in Laravel.**

- Review `config/cors.php` (publish it with `php artisan config:publish cors` if it is
  absent). `allowed_origins` should list explicit origins; `*` must not be combined
  with `supports_credentials` set to `true`.
- Review `allowed_origins_patterns` regular expressions for missing anchors or
  unescaped dots.
- Test: send `Origin: https://attacker.invalid` and confirm the origin is not echoed.

**Evidence.** `config/cors.php`; response headers for allowed and disallowed origins.

### LAR-API-003 Responses declare an accurate Content-Type

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V4.1.1 (L1), V4 API and Web Service / V4.1 Generic Web Service Security |
| API Top 10 | API8:2023 Security Misconfiguration |

**Requirement summary.** Every response with a body has a Content-Type that matches the content, with a safe character encoding.

**How to verify in Laravel.**

- `response()->json()` and API Resources send `application/json`. RFC 8259 defines no
  charset parameter for JSON and requires UTF-8, so its absence is acceptable there.
- Confirm endpoints that return strings or files set the type explicitly; a plain
  string response defaults to `text/html; charset=UTF-8`, which allows reflected
  content to be rendered as HTML.
- Confirm downloads use `response()->download()` or set `Content-Type` and
  `Content-Disposition: attachment` together with `X-Content-Type-Options: nosniff`.

**Evidence.** Response headers for JSON, text and download endpoints.

### LAR-API-004 Errors return generic messages in production

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V16.5.1 (L2), V16 Security Logging and Error Handling / V16.5 Error Handling |
| Related ASVS | V13.4.2 |
| API Top 10 | API8:2023 Security Misconfiguration |
| ZAP alerts | [10023 Information Disclosure - Debug Error Messages](https://www.zaproxy.org/docs/alerts/10023/), [90022 Application Error Disclosure](https://www.zaproxy.org/docs/alerts/90022/) |

**Requirement summary.** A generic message is returned when an unexpected or security-sensitive error occurs, without stack traces, queries, keys or tokens.

**How to verify in Laravel.**

- Confirm `APP_DEBUG=false` and `APP_ENV=production` in the deployed environment.
  With debug enabled, the error page and JSON responses include the stack trace,
  file paths and request data.
- Confirm custom exception rendering does not return `$e->getMessage()` for
  database or third-party exceptions.
- Trigger an error (for example a malformed route parameter that reaches the database)
  and inspect the response.

**Evidence.** Environment configuration (values only for `APP_DEBUG` and `APP_ENV`); sample error response.

### LAR-API-005 Documentation and monitoring endpoints are not publicly exposed

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V13.4.5 (L2), V13 Configuration / V13.4 Unintended Information Leakage |
| Related ASVS | V15.2.3 |
| API Top 10 | API9:2023 Improper Inventory Management |

**Requirement summary.** Documentation (such as internal API docs) and monitoring endpoints are not exposed unless explicitly intended.

**How to verify in Laravel.**

- Check for Telescope (`/telescope`), Horizon (`/horizon`), Pulse (`/pulse`), Log
  Viewer, generated API docs (l5-swagger, Scramble) and debug bars. Confirm each is
  not installed in production or is protected by its authorization gate
  (`viewTelescope`, `viewHorizon`, `viewPulse`).
- Confirm dev dependencies are excluded from production builds
  (`composer install --no-dev`).
- Request each path unauthenticated against the production host.

**Evidence.** Composer production install command; HTTP responses for each path.

### LAR-API-006 Client IP and scheme are derived from trusted proxies only

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V15.3.4 (L2), V15 Secure Coding and Architecture / V15.3 Defensive Coding |
| Related ASVS | V4.1.3 |
| API Top 10 | API8:2023 Security Misconfiguration |

**Requirement summary.** Proxies and middleware transfer the original client IP using trusted fields that the end user cannot manipulate, and that value is used for logging and security decisions.

**How to verify in Laravel.**

- Review `trustProxies(at: ...)` in `bootstrap/app.php` (or the `TrustProxies`
  middleware in older applications). Trusting `*` is only acceptable if the
  application is reachable exclusively through the proxy.
- Test: send `X-Forwarded-For: 203.0.113.10` directly to the application and confirm
  `$request->ip()`, logs and rate limit keys do not use the spoofed value.

**Evidence.** Proxy configuration; log entry or debug output from the spoofing test.

### LAR-API-007 Source control metadata and environment files are not served

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V13.4.1 (L1), V13 Configuration / V13.4 Unintended Information Leakage |
| API Top 10 | API8:2023 Security Misconfiguration |
| ZAP alerts | [40035 Hidden File Found](https://www.zaproxy.org/docs/alerts/40035/), [40034 .env Information Leak](https://www.zaproxy.org/docs/alerts/40034/) |

**Requirement summary.** The application is deployed without source control metadata such as `.git`, or that metadata is inaccessible externally and to the application.

**How to verify in Laravel.**

- Confirm the web server document root is `public/`, not the project root. Serving
  the project root exposes `.env`, `.git`, `composer.json` and `storage/`.
- Request `/.git/HEAD`, `/.env` and `/storage/logs/laravel.log` and expect 404.
- Prefer build artifacts that exclude `.git` entirely.

**Evidence.** Web server configuration (document root); HTTP responses for the paths above.

### LAR-API-008 GraphQL queries are limited in depth and cost

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V4.3.1 (L2), V4 API and Web Service / V4.3 GraphQL |
| Related ASVS | V4.3.2 |
| API Top 10 | API4:2023 Unrestricted Resource Consumption |

**Requirement summary.** Query allowlisting, depth limiting, amount limiting or cost analysis prevents denial of service through expensive nested GraphQL queries.

**How to verify in Laravel.**

- Applies when Lighthouse or another GraphQL server is used.
- Lighthouse: review `security.max_query_depth`, `security.max_query_complexity` and
  `security.disable_introspection` in `config/lighthouse.php`, and pagination
  `max_count` limits.
- Test a deeply nested query and confirm it is rejected before execution.

**Evidence.** GraphQL configuration; response to an over-limit query.

### LAR-API-009 WebSocket handshakes validate the Origin header

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V4.4.2 (L2), V4 API and Web Service / V4.4 WebSocket |
| API Top 10 | API8:2023 Security Misconfiguration |

**Requirement summary.** During the WebSocket handshake, the Origin header is checked against the origins allowed for the application.

**How to verify in Laravel.**

- Applies when Laravel Reverb or another WebSocket server is used.
- Reverb: confirm `allowed_origins` in `config/reverb.php` lists explicit hosts rather
  than `*`.
- Confirm private and presence channels are authorized in `routes/channels.php` with
  per-channel checks, not `return true;`.

**Evidence.** WebSocket server configuration; channel authorization callbacks.
