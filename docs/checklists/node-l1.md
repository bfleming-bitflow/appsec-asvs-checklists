# Node.js (Express and NestJS) verification checklist

<!-- Generated from checklists/node.yml by tools/checklist.py. Do not edit by hand. -->

Verification checklist for Node.js services built with Express 4/5 or NestJS 10 and later, covering server-rendered applications and JSON or GraphQL APIs authenticated with cookie sessions (express-session, Passport) or bearer tokens (JWT).

| Property | Value |
| --- | --- |
| Standard | [OWASP ASVS 5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0_release/5.0) |
| API risks | [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/) |
| Scope | levels up to L1 |
| Items | 27 (L1: 27) |

Requirement summaries are paraphrased. The official ASVS text is authoritative; consult it before recording a result.

## Contents

- [Authentication](#authentication) (4)
- [Session management](#session-management) (5)
- [Access control](#access-control) (4)
- [Self-contained tokens (JWT)](#self-contained-tokens-jwt) (4)
- [Input validation and output encoding](#input-validation-and-output-encoding) (7)
- [API and web service configuration](#api-and-web-service-configuration) (3)

## Summary

| ID | Title | ASVS | Level | API Top 10 |
| --- | --- | --- | --- | --- |
| [NODE-AUTHN-001](#node-authn-001-minimum-password-length-is-enforced-server-side) | Minimum password length is enforced server-side | V6.2.1 | L1 | API2:2023 |
| [NODE-AUTHN-002](#node-authn-002-no-character-composition-rules-are-imposed) | No character composition rules are imposed | V6.2.5 | L1 | API2:2023 |
| [NODE-AUTHN-006](#node-authn-006-login-is-protected-against-brute-force-and-credential-stuffing) | Login is protected against brute force and credential stuffing | V6.3.1 | L1 | API2:2023, API4:2023 |
| [NODE-AUTHN-008](#node-authn-008-no-default-or-seeded-accounts-exist-in-production) | No default or seeded accounts exist in production | V6.3.2 | L1 | - |
| [NODE-SESS-001](#node-sess-001-session-identifier-is-regenerated-on-authentication) | Session identifier is regenerated on authentication | V7.2.4 | L1 | API2:2023 |
| [NODE-SESS-002](#node-sess-002-logout-invalidates-the-session-on-the-server) | Logout invalidates the session on the server | V7.4.1 | L1 | API2:2023 |
| [NODE-SESS-003](#node-sess-003-session-cookie-has-the-secure-attribute-and-a-secure-prefix) | Session cookie has the Secure attribute and a secure prefix | V3.3.1 | L1 | - |
| [NODE-SESS-006](#node-sess-006-session-identifiers-have-sufficient-entropy) | Session identifiers have sufficient entropy | V7.2.3 | L1 | API2:2023 |
| [NODE-SESS-011](#node-sess-011-disabling-an-account-terminates-its-sessions-and-tokens) | Disabling an account terminates its sessions and tokens | V7.4.2 | L1 | API2:2023 |
| [NODE-AUTHZ-001](#node-authz-001-function-level-access-requires-explicit-permission) | Function-level access requires explicit permission | V8.2.1 | L1 | API5:2023 |
| [NODE-AUTHZ-002](#node-authz-002-object-level-access-is-checked-for-every-record) | Object-level access is checked for every record | V8.2.2 | L1 | API1:2023 |
| [NODE-AUTHZ-005](#node-authz-005-responses-return-only-the-fields-the-consumer-needs) | Responses return only the fields the consumer needs | V15.3.1 | L1 | API3:2023 |
| [NODE-AUTHZ-006](#node-authz-006-authorization-is-enforced-on-the-server-not-the-client) | Authorization is enforced on the server, not the client | V8.3.1 | L1 | API5:2023 |
| [NODE-TOKEN-001](#node-token-001-tokens-are-verified-before-their-claims-are-used) | Tokens are verified before their claims are used | V9.1.1 | L1 | API2:2023 |
| [NODE-TOKEN-002](#node-token-002-token-algorithms-are-restricted-to-an-allowlist) | Token algorithms are restricted to an allowlist | V9.1.2 | L1 | API2:2023 |
| [NODE-TOKEN-003](#node-token-003-verification-keys-come-from-trusted-configuration) | Verification keys come from trusted configuration | V9.1.3 | L1 | API2:2023 |
| [NODE-TOKEN-004](#node-token-004-token-validity-period-is-enforced) | Token validity period is enforced | V9.2.1 | L1 | API2:2023 |
| [NODE-INPUT-001](#node-input-001-request-input-is-validated-against-positive-rules) | Request input is validated against positive rules | V2.2.1 | L1 | - |
| [NODE-INPUT-002](#node-input-002-only-validated-input-reaches-business-logic) | Only validated input reaches business logic | V2.2.2 | L1 | - |
| [NODE-INPUT-003](#node-input-003-template-output-is-encoded-for-its-context) | Template output is encoded for its context | V1.2.1 | L1 | - |
| [NODE-INPUT-004](#node-input-004-database-queries-are-parameterized) | Database queries are parameterized | V1.2.4 | L1 | - |
| [NODE-INPUT-005](#node-input-005-operating-system-commands-are-not-built-from-input) | Operating system commands are not built from input | V1.2.5 | L1 | - |
| [NODE-INPUT-006](#node-input-006-rich-text-html-is-sanitized-with-a-maintained-library) | Rich-text HTML is sanitized with a maintained library | V1.3.1 | L1 | - |
| [NODE-INPUT-007](#node-input-007-dynamic-code-execution-is-not-used-with-input) | Dynamic code execution is not used with input | V1.3.2 | L1 | - |
| [NODE-API-002](#node-api-002-cors-allows-only-trusted-origins) | CORS allows only trusted origins | V3.4.2 | L1 | API8:2023 |
| [NODE-API-003](#node-api-003-responses-declare-an-accurate-content-type) | Responses declare an accurate Content-Type | V4.1.1 | L1 | API8:2023 |
| [NODE-API-007](#node-api-007-source-control-metadata-and-environment-files-are-not-served) | Source control metadata and environment files are not served | V13.4.1 | L1 | API8:2023 |

## Authentication

Express and NestJS provide no authentication by default. Every control below depends on application code or on libraries such as Passport, so review the code that is deployed.

### NODE-AUTHN-001 Minimum password length is enforced server-side

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.2.1 (L1), V6 Authentication / V6.2 Password Security |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** User-chosen passwords must be at least 8 characters; 15 or more is strongly recommended.

**How to verify in Node.js (Express and NestJS).**

- Locate the schema for registration, password change and password reset (zod, joi,
  class-validator DTOs) and confirm a minimum of 8 or more, for example
  `z.string().min(8)` or `@MinLength(8)`.
- Define the policy once and reuse it in all three flows.
- Submit a 7-character password to each flow and confirm a 400 or 422 response.

**Evidence.** Schema definitions with file paths; request/response pair showing rejection.

### NODE-AUTHN-002 No character composition rules are imposed

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.2.5 (L1), V6 Authentication / V6.2 Password Security |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Passwords of any composition are accepted; there is no requirement for upper or lower case letters, digits or special characters.

**How to verify in Node.js (Express and NestJS).**

- class-validator `@IsStrongPassword()` with default options requires at least one
  lowercase, uppercase, digit and symbol, which fails this requirement. Search for it
  and for password regular expressions (`.regex(` in zod, `.pattern(` in joi).
- Length and breached-password checks are the intended replacement.

**Evidence.** Search output showing no composition rules, or the change that removed them.

### NODE-AUTHN-006 Login is protected against brute force and credential stuffing

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.3.1 (L1), V6 Authentication / V6.3 General Authentication Security |
| Related ASVS | V6.1.1 |
| API Top 10 | API2:2023 Broken Authentication, API4:2023 Unrestricted Resource Consumption |

**Requirement summary.** Controls against credential stuffing and password brute force are implemented as defined in the application's security documentation.

**How to verify in Node.js (Express and NestJS).**

- Identify every credential-accepting endpoint: login, token issuance, refresh, MFA
  verification, password confirmation and password reset.
- Confirm each is rate limited: `express-rate-limit` or `rate-limiter-flexible` in
  Express, `@nestjs/throttler` (`ThrottlerGuard`, `@Throttle()`) in NestJS.
- Key limits on both account identifier and client IP, and use a shared store (Redis)
  when the service runs as several instances; the default in-memory stores are
  per-process.
- Confirm the client IP is correct behind proxies (see the trusted proxy item).

**Evidence.** Limiter configuration; repeated failed logins showing HTTP 429.

### NODE-AUTHN-008 No default or seeded accounts exist in production

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V6.3.2 (L1), V6 Authentication / V6.3 General Authentication Security |

**Requirement summary.** Default accounts such as "admin" or "root" are not present or are disabled.

**How to verify in Node.js (Express and NestJS).**

- Review seed scripts (Prisma `prisma/seed.ts`, TypeORM or Sequelize seeders, Knex
  seeds) and migrations for user inserts with fixed credentials.
- Confirm seeding is not part of the production deployment, or is environment-guarded.
- Query the production user table for well-known names and addresses.

**Evidence.** Seed script review; deployment pipeline step list; production query result (counts only).

## Session management

Applies to cookie-based sessions with express-session (directly or through Passport). Bearer-token authentication is covered in the Tokens section.

### NODE-SESS-001 Session identifier is regenerated on authentication

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.2.4 (L1), V7 Session Management / V7.2 Fundamental Session Management Security |
| API Top 10 | API2:2023 Broken Authentication |
| ZAP alerts | [40013 Session Fixation](https://www.zaproxy.org/docs/alerts/40013/) |

**Requirement summary.** A new session token is generated on authentication and re-authentication, and the previous token is terminated.

**How to verify in Node.js (Express and NestJS).**

- express-session does not regenerate the session on login by itself. Confirm the
  login handler calls `req.session.regenerate()` before storing the user.
- Passport 0.6.0 and later regenerate the session inside `req.login()`. Confirm the
  installed version and that no custom code writes the user into `req.session`
  without going through `req.login()`.
- Test: record the session cookie before login, authenticate, confirm it changed and
  the old value is rejected.

**Evidence.** Login handler code; `passport` version from the lockfile; cookie values before and after login.

### NODE-SESS-002 Logout invalidates the session on the server

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.4.1 (L1), V7 Session Management / V7.4 Session Termination |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** When a session is terminated by logout or expiry, it cannot be used again.

**How to verify in Node.js (Express and NestJS).**

- Confirm logout calls `req.logout()` (asynchronous with a callback since Passport
  0.6) and `req.session.destroy()`, and clears the cookie.
- For JWT-based sessions, confirm logout revokes the refresh token server-side and
  that access tokens are short-lived or checked against a revocation list.
- Test: copy the session cookie or token, log out, replay it and confirm rejection.

**Evidence.** Logout handler; replay request and response.

### NODE-SESS-003 Session cookie has the Secure attribute and a secure prefix

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V3.3.1 (L1), V3 Web Frontend Security / V3.3 Cookie Setup |
| Related ASVS | V3.3.3 |
| ZAP alerts | [10011 Cookie Without Secure Flag](https://www.zaproxy.org/docs/alerts/10011/) |

**Requirement summary.** Cookies have the Secure attribute; if the `__Host-` prefix is not used, the `__Secure-` prefix is used.

**How to verify in Node.js (Express and NestJS).**

- express-session: confirm `cookie.secure: true` in production. Behind a TLS
  terminating proxy this also requires `app.set('trust proxy', ...)`, otherwise the
  cookie is not sent.
- Set `name` to a value starting with `__Host-` (requires `path: '/'` and no
  `domain`); the default name `connect.sid` also discloses the stack.
- Apply the same attributes to cookies set with `res.cookie()`.

**Evidence.** Session middleware configuration; `Set-Cookie` headers from staging or production.

### NODE-SESS-006 Session identifiers have sufficient entropy

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.2.3 (L1), V7 Session Management / V7.2 Fundamental Session Management Security |
| Related ASVS | V7.2.2 |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Reference session tokens are unique, generated with a CSPRNG and have at least 128 bits of entropy.

**How to verify in Node.js (Express and NestJS).**

- express-session generates IDs with `uid-safe` (24 random bytes). If a custom
  `genid` is configured, confirm it uses `crypto.randomBytes()` or
  `crypto.randomUUID()`, not `Math.random()`, timestamps or counters.
- Confirm `secret` is a high-entropy value loaded from configuration, not a literal
  in source code, and supports rotation (an array of secrets).
- Confirm the production store is not the default `MemoryStore`, which leaks memory
  and does not share sessions across instances.

**Evidence.** Session middleware configuration; secret source; store type.

### NODE-SESS-011 Disabling an account terminates its sessions and tokens

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V7.4.2 (L1), V7 Session Management / V7.4 Session Termination |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** All active sessions are terminated when a user account is disabled or deleted.

**How to verify in Node.js (Express and NestJS).**

- Confirm the disable or delete action destroys the user's sessions in the store and
  revokes refresh tokens.
- If Passport `deserializeUser` loads the user on each request, confirm it rejects
  disabled accounts; if it only trusts the serialized object, disabled users keep
  access until the session expires.

**Evidence.** Disable/delete action code; `deserializeUser` implementation; test result.

## Access control

In Express, authorization is middleware that must be attached to each router; in NestJS, guards must be bound globally or per controller. Missing bindings fail open.

### NODE-AUTHZ-001 Function-level access requires explicit permission

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V8.2.1 (L1), V8 Authorization / V8.2 General Authorization Design |
| API Top 10 | API5:2023 Broken Function Level Authorization |

**Requirement summary.** Access to functions is restricted to consumers with explicit permissions.

**How to verify in Node.js (Express and NestJS).**

- NestJS: prefer a global authentication guard (`APP_GUARD`) with an explicit
  `@Public()` metadata opt-out, plus a roles or permissions guard that reads metadata
  through `Reflector`. Confirm handlers without role metadata are denied, not allowed.
- Express: confirm authorization middleware is mounted on each router before route
  handlers, and that routes registered before the middleware are intentionally public.
- Test administrative endpoints with a low-privilege token and expect 403.

**Evidence.** Guard or middleware registration; list of public routes; 403 responses.

### NODE-AUTHZ-002 Object-level access is checked for every record

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V8.2.2 (L1), V8 Authorization / V8.2 General Authorization Design |
| API Top 10 | API1:2023 Broken Object Level Authorization |

**Requirement summary.** Data-specific access is restricted to consumers with explicit permissions to each data item, preventing IDOR and broken object level authorization.

**How to verify in Node.js (Express and NestJS).**

- Review handlers that load records by `req.params.id` or a body identifier. Confirm
  the query includes the owner or tenant condition (for example
  `where: { id, ownerId: user.id }`) or an explicit policy check follows.
- Using UUIDs instead of sequential IDs does not replace the check.
- Test with two accounts: request the other account's identifiers and expect 403 or
  404.

**Evidence.** Query code for key resources; cross-account test results.

### NODE-AUTHZ-005 Responses return only the fields the consumer needs

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V15.3.1 (L1), V15 Secure Coding and Architecture / V15.3 Defensive Coding |
| API Top 10 | API3:2023 Broken Object Property Level Authorization |

**Requirement summary.** The application returns only the required subset of fields from a data object rather than the entire object.

**How to verify in Node.js (Express and NestJS).**

- Search for handlers returning ORM entities directly. Prefer explicit selection
  (Prisma `select`, TypeORM `select`) or response DTOs.
- NestJS: if `ClassSerializerInterceptor` is used, confirm sensitive properties carry
  `@Exclude()` or that entities use `@Expose()` allowlisting with
  `excludeExtraneousValues`.
- Inspect responses for password hashes, MFA secrets, reset tokens, internal flags and
  other users' data.

**Evidence.** Serialization configuration; sample responses from key endpoints.

### NODE-AUTHZ-006 Authorization is enforced on the server, not the client

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V8.3.1 (L1), V8 Authorization / V8.3 Operation Level Authorization |
| API Top 10 | API5:2023 Broken Function Level Authorization |

**Requirement summary.** Authorization rules are enforced at a trusted service layer and do not rely on controls the client can manipulate.

**How to verify in Node.js (Express and NestJS).**

- Confirm features hidden in the frontend are protected by server-side checks.
- Confirm roles and identifiers used in decisions come from the verified session or
  token, never from `req.body`, `req.query`, custom headers or unsigned cookies.
- Confirm claims in an unverified JWT (`jwt.decode()`) are never used for decisions.

**Evidence.** Mapping of UI-gated actions to server-side checks; direct request results.

## Self-contained tokens (JWT)

Applies to services that issue or accept JWTs, whether through `jsonwebtoken`, `jose`, `passport-jwt` or `@nestjs/jwt`.

### NODE-TOKEN-001 Tokens are verified before their claims are used

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V9.1.1 (L1), V9 Self-contained Tokens / V9.1 Token source and integrity |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Self-contained tokens are validated using their digital signature or MAC before their contents are accepted.

**How to verify in Node.js (Express and NestJS).**

- Search for `jwt.decode(`, `decodeJwt(` and manual `Buffer.from(token.split('.')[1],
  'base64')`. These do not verify signatures; claims must come from `jwt.verify()`,
  `jwtVerify()` or `JwtService.verify()`.
- Test: alter one payload character and expect 401.

**Evidence.** Search output; response to a tampered token.

### NODE-TOKEN-002 Token algorithms are restricted to an allowlist

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V9.1.2 (L1), V9 Self-contained Tokens / V9.1 Token source and integrity |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Only allowlisted algorithms can be used to create and verify self-contained tokens, and the `none` algorithm is never accepted.

**How to verify in Node.js (Express and NestJS).**

- Confirm every verification call passes an explicit list: `algorithms: ['RS256']` for
  `jsonwebtoken` and `passport-jwt`, `algorithms` in `jose` `jwtVerify()` options,
  `verifyOptions.algorithms` in `@nestjs/jwt`.
- Confirm symmetric and asymmetric algorithms are not mixed for the same key.
- Test: submit tokens with `alg: none` and with `HS256` signed using the public key;
  both must be rejected.

**Evidence.** Verification options; responses to the two test tokens.

### NODE-TOKEN-003 Verification keys come from trusted configuration

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V9.1.3 (L1), V9 Self-contained Tokens / V9.1 Token source and integrity |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** Key material used to validate tokens comes from trusted, pre-configured sources for the issuer; attacker-specified sources and keys are not accepted.

**How to verify in Node.js (Express and NestJS).**

- Confirm the JWKS URL is a fixed configuration value (for example
  `createRemoteJWKSet(new URL(config.jwksUri))` in `jose`) and that the `jku`, `x5u`
  and embedded `jwk` header parameters are ignored.
- When looking up keys by `kid`, confirm unknown `kid` values fail rather than falling
  back to a default key or a file path derived from `kid`.

**Evidence.** Key resolution code; response to a token with a forged `jku` header.

### NODE-TOKEN-004 Token validity period is enforced

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V9.2.1 (L1), V9 Self-contained Tokens / V9.2 Token content |
| API Top 10 | API2:2023 Broken Authentication |

**Requirement summary.** If a token carries a validity period, it is accepted only while the verification time falls within it.

**How to verify in Node.js (Express and NestJS).**

- `jsonwebtoken` and `passport-jwt` reject expired tokens unless `ignoreExpiration` is
  set; search for it. Neither requires `exp` to be present, so confirm issued tokens
  always include it, or use `jose` with `requiredClaims: ['exp']`.
- Confirm `clockTolerance` is small (seconds, not minutes) and that `nbf` is honoured.

**Evidence.** Issuance and verification options; response to an expired token.

## Input validation and output encoding

Validation enforces expected structure; encoding and parameterization prevent injection. Neither replaces the other.

### NODE-INPUT-001 Request input is validated against positive rules

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V2.2.1 (L1), V2 Validation and Business Logic / V2.2 Input Validation |
| Related ASVS | V2.1.1 |

**Requirement summary.** Input is validated against business expectations using allowlists of values, patterns and ranges, or against expected structure and logical limits.

**How to verify in Node.js (Express and NestJS).**

- NestJS: confirm a global `ValidationPipe` and DTOs with class-validator decorators
  for every body, query and parameter object; parameters need pipes such as
  `ParseIntPipe` or `ParseUUIDPipe`.
- Express: confirm a schema (zod, joi, ajv) validates `req.body`, `req.query` and
  `req.params` for each route, including type, length, format and enumerations.
- Confirm nested objects and arrays are validated (`@ValidateNested()` with
  `@Type()`, nested zod schemas) and have maximum sizes.

**Evidence.** Validation setup; examples of rejected invalid payloads.

### NODE-INPUT-002 Only validated input reaches business logic

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V2.2.2 (L1), V2 Validation and Business Logic / V2.2 Input Validation |

**Requirement summary.** Input validation is enforced at a trusted service layer; client-side validation is not relied upon.

**How to verify in Node.js (Express and NestJS).**

- Confirm handlers use the parsed result of validation (`schema.parse(req.body)`,
  DTO instances) rather than the raw `req.body`.
- Confirm validation shared with a frontend package is also executed on the server.

**Evidence.** Handler code samples for key endpoints.

### NODE-INPUT-003 Template output is encoded for its context

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.2.1 (L1), V1 Encoding and Sanitization / V1.2 Injection Prevention |
| ZAP alerts | [40012 Cross Site Scripting (Reflected)](https://www.zaproxy.org/docs/alerts/40012/), [40014 Cross Site Scripting (Persistent)](https://www.zaproxy.org/docs/alerts/40014/) |

**Requirement summary.** Output encoding for HTML elements, attributes, comments, CSS and HTTP headers matches the context in which the data is placed.

**How to verify in Node.js (Express and NestJS).**

- Search for raw output constructs: EJS `<%-`, Handlebars `{{{ }}}` and `SafeString`,
  Pug `!{}` and `!=`, Nunjucks `| safe`, React `dangerouslySetInnerHTML`.
- Confirm escaped output is not used in contexts where HTML escaping is insufficient:
  unquoted attributes, `href`/`src` without a scheme allowlist, inline event handlers,
  `<script>` and `<style>` blocks.

**Evidence.** Search output with a justification per raw output occurrence.

### NODE-INPUT-004 Database queries are parameterized

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.2.4 (L1), V1 Encoding and Sanitization / V1.2 Injection Prevention |
| ZAP alerts | [40018 SQL Injection](https://www.zaproxy.org/docs/alerts/40018/) |

**Requirement summary.** Database queries use parameterized queries or an ORM, and are protected from SQL and other database injection, including NoSQL.

**How to verify in Node.js (Express and NestJS).**

- SQL: review `pg`/`mysql2` calls for string concatenation instead of placeholders;
  Prisma `$queryRawUnsafe` / `$executeRawUnsafe` (the tagged-template `$queryRaw` is
  parameterized); TypeORM `query()` and QueryBuilder `where()` with interpolated
  strings; Sequelize `literal()` and `query()` without `replacements` or `bind`.
- Identifiers (sort columns, directions) cannot be parameterized and need allowlists.
- MongoDB: confirm request values are type-checked so objects such as `{"$ne": null}`
  cannot reach query filters; Mongoose `sanitizeFilter` can enforce this globally.
  Review `$where` and `$function` usage.

**Evidence.** Search output with review notes; validation of filter inputs.

### NODE-INPUT-005 Operating system commands are not built from input

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.2.5 (L1), V1 Encoding and Sanitization / V1.2 Injection Prevention |
| ZAP alerts | [90020 Remote OS Command Injection](https://www.zaproxy.org/docs/alerts/90020/) |

**Requirement summary.** The application protects against OS command injection by using parameterized OS calls or contextual command-line encoding.

**How to verify in Node.js (Express and NestJS).**

- Search for `child_process.exec`, `execSync` and `spawn`/`execFile` with
  `shell: true`. `exec` always runs a shell.
- Prefer `execFile` or `spawn` with an argument array and no shell, and prevent
  option injection by validating arguments and using `--` where supported.

**Evidence.** Search output with review notes per call site.

### NODE-INPUT-006 Rich-text HTML is sanitized with a maintained library

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.3.1 (L1), V1 Encoding and Sanitization / V1.3 Sanitization |
| ZAP alerts | [40014 Cross Site Scripting (Persistent)](https://www.zaproxy.org/docs/alerts/40014/) |

**Requirement summary.** Untrusted HTML from WYSIWYG editors or similar is sanitized with a well-known sanitization library or framework feature.

**How to verify in Node.js (Express and NestJS).**

- Confirm stored rich text is sanitized with an allowlist-based library such as
  DOMPurify (with `jsdom` on the server) or `sanitize-html`, with a restrictive
  configuration.
- Regex-based filtering and ad hoc tag stripping do not meet this requirement.

**Evidence.** Sanitizer configuration and call sites; neutralized test payloads.

### NODE-INPUT-007 Dynamic code execution is not used with input

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V1.3.2 (L1), V1 Encoding and Sanitization / V1.3 Sanitization |
| ZAP alerts | [90019 Server Side Code Injection](https://www.zaproxy.org/docs/alerts/90019/) |

**Requirement summary.** The application avoids `eval()` and other dynamic code execution; where unavoidable, input is sanitized first.

**How to verify in Node.js (Express and NestJS).**

- Search for `eval(`, `new Function(`, `setTimeout` / `setInterval` with string
  arguments, `vm.runInContext` / `vm.runInNewContext` and dynamic `require()` or
  `import()` with input-derived specifiers.
- The `vm` module is not a security boundary; it must not be used to run untrusted
  code.

**Evidence.** Search output with review notes.

## API and web service configuration

Configuration items that apply to JSON and GraphQL APIs and to the HTTP surface of the service.

### NODE-API-002 CORS allows only trusted origins

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V3.4.2 (L1), V3 Web Frontend Security / V3.4 Browser Security Mechanism Headers |
| API Top 10 | API8:2023 Security Misconfiguration |
| ZAP alerts | [40040 CORS Header](https://www.zaproxy.org/docs/alerts/40040/), [10098 Cross-Domain Misconfiguration](https://www.zaproxy.org/docs/alerts/10098/) |

**Requirement summary.** The `Access-Control-Allow-Origin` header is a fixed value, or the request Origin is validated against an allowlist of trusted origins.

**How to verify in Node.js (Express and NestJS).**

- `cors({ origin: true })` and `app.enableCors()` without options reflect or allow any
  origin. Confirm `origin` is an explicit array or a function that checks an allowlist.
- Confirm `credentials: true` is never combined with a reflecting or wildcard origin.
- Review origin regular expressions for missing anchors and unescaped dots.
- Test with `Origin: https://attacker.invalid`.

**Evidence.** CORS configuration; response headers for allowed and disallowed origins.

### NODE-API-003 Responses declare an accurate Content-Type

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V4.1.1 (L1), V4 API and Web Service / V4.1 Generic Web Service Security |
| API Top 10 | API8:2023 Security Misconfiguration |

**Requirement summary.** Every response with a body has a Content-Type that matches the content, with a safe character encoding.

**How to verify in Node.js (Express and NestJS).**

- `res.json()` sets `application/json; charset=utf-8`. `res.send()` with a string
  defaults to `text/html; charset=utf-8`; confirm API handlers do not send strings
  that include input, or set the type explicitly with `res.type()`.
- Confirm file downloads set `Content-Type`, `Content-Disposition: attachment` and
  `X-Content-Type-Options: nosniff` (Helmet sets the latter by default).

**Evidence.** Response headers for JSON, text and download endpoints.

### NODE-API-007 Source control metadata and environment files are not served

- [ ] Verified

| Field | Value |
| --- | --- |
| ASVS 5.0.0 | V13.4.1 (L1), V13 Configuration / V13.4 Unintended Information Leakage |
| API Top 10 | API8:2023 Security Misconfiguration |
| ZAP alerts | [40035 Hidden File Found](https://www.zaproxy.org/docs/alerts/40035/), [40034 .env Information Leak](https://www.zaproxy.org/docs/alerts/40034/) |

**Requirement summary.** The application is deployed without source control metadata such as `.git`, or that metadata is inaccessible externally and to the application.

**How to verify in Node.js (Express and NestJS).**

- Confirm `express.static()` and `ServeStaticModule` serve a dedicated directory
  (`public/`, `dist/client/`), never the project root.
- Request `/.git/HEAD`, `/.env` and `/package.json` and expect 404.
- Prefer container images built from a `.dockerignore` that excludes `.git` and
  `.env` files.

**Evidence.** Static file configuration; `.dockerignore`; HTTP responses for the paths above.
