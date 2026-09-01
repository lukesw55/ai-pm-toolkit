# Code slop catalogue (A1–A10)

Load this reference when reviewing or producing code, comments, types, or identifiers. The 10 patterns below are the most common shapes of code that "looks like the model was trying to look thorough" without paying rent.

## A1. Boundary confusion

Slop:

```python
def total(items: list[Order]) -> float:
    if items is None:
        return 0.0
    if not isinstance(items, list):
        raise TypeError("items must be a list")
    return sum(o.amount for o in items if o is not None)
```

Fix:

```python
def total(items: list[Order]) -> float:
    return sum(o.amount for o in items)
```

Rule: validate user input, network payloads, file contents, env vars, and external APIs. Trust internal typed callers.

## A2. Try/except that cannot recover

Slop:

```python
try:
    payload = json.loads(raw)
except Exception as exc:
    logger.error("Failed to parse payload: %s", exc)
    payload = {}
```

Fix:

```python
payload = json.loads(raw)
```

Rule: catch only specific exceptions and only when the code can recover correctly.

## A3. Single-use abstraction

Slop:

```ts
const DEFAULT_TIMEOUT_MS = 30000;

function createClient() {
  return new Client({ timeout: DEFAULT_TIMEOUT_MS });
}

const client = createClient();
```

Fix:

```ts
const client = new Client({ timeout: 30_000 });
```

Rule: extract after real reuse, not imagined reuse.

## A4. Generic names

Slop names:

```text
data
result
temp
final
info
payloadData
processData
handleResult
DataManager
Helper
Utils
Service
```

Fix by naming the domain object:

```text
pendingInvoices
signedPayload
expiredSessions
normaliseOrders
issueRefund
```

Rule: name what it is or what domain action it performs.

## A5. Comments that restate code

Slop:

```ts
// Loop through users and send each one an email
for (const user of users) {
  sendWelcomeEmail(user);
}
```

Fix:

```ts
for (const user of users) {
  sendWelcomeEmail(user);
}
```

Keep comments only for non-obvious constraints:

```ts
// Stripe retries this webhook for 72 hours, so this must stay idempotent.
await recordWebhookOnce(event.id);
```

## A6. Narration logs

Slop:

```ts
logger.info("Starting user creation");
const user = await createUser(input);
logger.info("Sending welcome email");
await sendWelcomeEmail(user);
logger.info("Finished user creation");
```

Fix:

```ts
const user = await createUser(input);
await sendWelcomeEmail(user);
```

Rule: log production-relevant facts, not a transcript of the function.

## A7. Premature configurability

Slop:

```ts
function fetchUser(id: string, timeout = 30000, retries = 3, backoff = 2, jitter = true) {
  ...
}
```

Fix:

```ts
function fetchUser(id: string) {
  ...
}
```

Rule: add parameters when a real caller needs different behavior.

## A8. Dead compatibility

Slop:

```ts
export function normaliseOrders(orders: Order[]) {
  ...
}

// Deprecated alias, kept for compatibility.
export const processData = normaliseOrders;
```

Fix:

```ts
export function normaliseOrders(orders: Order[]) {
  ...
}
```

Rule: compatibility is for released public contracts, not local renames.

## A9. Type/interface inflation

Slop:

```ts
interface CreateUserRequest {
  email: string;
  name: string;
}

async function createUser(req: CreateUserRequest) {
  return api.post("/users", req);
}
```

Fix:

```ts
async function createUser(req: { email: string; name: string }) {
  return api.post("/users", req);
}
```

Rule: named types must be reused, exported, or domain-meaningful.

## A10. Banners and artificial regions

Slop:

```ts
// =====================
// Helpers
// =====================
```

Fix: delete it.

Rule: if a file needs banners to be readable, split the file or improve names. Note: banner lines (5+ `=` chars) on newly added lines are hard-blocked by `hooks/anti-slop-gate.sh` outside of vendored paths.
