# Test slop catalogue (E1–E8)

Load this reference when writing or reviewing test files — unit tests, integration tests, E2E tests, fixtures, test utilities. Test files attract a specific shape of slop because AI models pattern-match against testing-tutorial conventions that no production codebase actually uses.

The patterns below are the most common shapes of "tests that look thorough because they exist, but pay no rent". A test costs as much as the production code it shadows. Slop tests cost twice — they pass forever while the thing they should be guarding has rotted.

## E1. Verbose test names that read like documentation

Slop:

```ts
it('should return the correct sum when given an array of valid numbers as input', () => {
  expect(sum([1, 2, 3])).toBe(6);
});

it('should throw an error when the input is null or undefined', () => {
  expect(() => sum(null)).toThrow();
});
```

Fix:

```ts
it('sums valid numbers', () => {
  expect(sum([1, 2, 3])).toBe(6);
});

it('throws on null input', () => {
  expect(() => sum(null)).toThrow();
});
```

Rule: a test name describes what is being tested in the smallest words that locate it in the spec file. "Should return the correct value when given a valid input" is `it('works')` in slow motion.

## E2. Setup ceremony for stateless tests

Slop:

```ts
let calculator: Calculator;

beforeEach(() => {
  calculator = new Calculator();
});

afterEach(() => {
  calculator = null;
});

it('adds two numbers', () => {
  expect(calculator.add(2, 3)).toBe(5);
});
```

Fix:

```ts
it('adds two numbers', () => {
  expect(new Calculator().add(2, 3)).toBe(5);
});
```

Rule: `beforeEach` / `afterEach` exist for shared mutable state. If the test has no state to share, the ceremony is decoration.

## E3. One-assertion-per-test inflation

Slop:

```ts
it('returns id', () => {
  expect(user.id).toBe('u-1');
});

it('returns email', () => {
  expect(user.email).toBe('a@b.com');
});

it('returns name', () => {
  expect(user.name).toBe('Mira');
});

it('returns created date', () => {
  expect(user.createdAt).toEqual(new Date('2026-05-08'));
});
```

Fix:

```ts
it('returns the user payload', () => {
  expect(user).toEqual({
    id: 'u-1',
    email: 'a@b.com',
    name: 'Mira',
    createdAt: new Date('2026-05-08'),
  });
});
```

Rule: a test name is a contract. Bundling assertions that share a contract is correct; splitting them inflates the suite and obscures intent.

## E4. Mocking what doesn't need mocking

Slop:

```ts
import { isValidEmail } from './email';

vi.mock('./email');

it('rejects invalid email on signup', () => {
  (isValidEmail as Mock).mockReturnValue(false);
  expect(() => signup({ email: 'x' })).toThrow();
});
```

Fix:

```ts
import { signup } from './signup';

it('rejects invalid email on signup', () => {
  expect(() => signup({ email: 'not-an-email' })).toThrow();
});
```

Rule: mock only what crosses a real boundary — network, filesystem, time, randomness, external process. A pure function with no I/O should be called, not mocked. Mocking pure functions makes the test pass even when the function is wrong.

## E5. Snapshot tests for trivial outputs

Slop:

```ts
it('formats the user header', () => {
  expect(formatHeader({ name: 'Mira' })).toMatchSnapshot();
});

// __snapshots__/header.test.ts.snap
exports[`formats the user header`] = `"Welcome, Mira"`;
```

Fix:

```ts
it('formats the user header', () => {
  expect(formatHeader({ name: 'Mira' })).toBe('Welcome, Mira');
});
```

Rule: snapshots are for outputs too large to inline (rendered HTML, serialised AST, multi-line JSON). For short strings and small objects, inline equality reads faster and breaks more usefully.

## E6. "Helper" / "util" prefix epidemic

Slop:

```ts
// __tests__/helpers/dataHelper.ts
export const createTestData = () => ({ ... });

// __tests__/helpers/validateHelper.ts
export const validateResult = (r) => { ... };

// __tests__/helpers/setupHelper.ts
export const setupTest = () => { ... };
```

Fix:

```ts
// __tests__/fixtures/orders.ts
export const validOrder = () => ({ ... });

// __tests__/assertions/refundShape.ts
export const expectRefundedOrder = (order) => { ... };
```

Rule: in tests, the helper / util / data trap is even worse than in app code, because every test imports it. Name fixtures and assertions by what they actually represent in the domain.

## E7. Re-exporting the test framework

Slop:

```ts
// test/test-utils.ts
export { describe, it, expect, beforeEach, afterEach } from 'vitest';
export const setupTestDb = () => { ... };

// tests/foo.test.ts
import { describe, it, expect, setupTestDb } from '../test/test-utils';
```

Fix:

```ts
// tests/foo.test.ts
import { describe, it, expect } from 'vitest';
import { setupTestDb } from '../test/setup-test-db';
```

Rule: re-wrapping a stable framework API breaks IDE jump-to-source, breaks framework upgrades, and adds a layer of indirection that pays no rent. If your test framework provides globals (Jest, Vitest with globals), use them. Otherwise import directly.

## E8. Excessive Arrange/Act/Assert comments

Slop:

```ts
it('sums valid numbers', () => {
  // Arrange
  const input = [1, 2, 3];

  // Act
  const result = sum(input);

  // Assert
  expect(result).toBe(6);
});
```

Fix:

```ts
it('sums valid numbers', () => {
  expect(sum([1, 2, 3])).toBe(6);
});
```

Rule: AAA is implicit in any short test — the eye finds the assertion in two seconds. Comments restate the structure. Keep AAA explicit only for long integration tests where the three phases are genuinely separated by setup time and side effects.
