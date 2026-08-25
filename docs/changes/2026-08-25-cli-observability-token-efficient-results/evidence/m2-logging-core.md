# M2 Logging Core Evidence

- Subject: privacy-safe event construction, strict configuration, safe local sink, bounded locking, and five-file rotation
- Requirements: R3-R17, R33-R34, AC1-AC4, AC8
- Tests: `node --test packages/rigorloop/test/cli-observability.test.js`
- Full package validation: `npm test --prefix packages/rigorloop` passed 171 tests after the package-isolation fixture included the new runtime modules.
- Security properties: event fields are allowlisted, control characters are normalized, events are capped at 16 KiB, unsafe paths and broad POSIX modes fail closed, and rotation owns five fixed names beneath the selected root.
- Result: passed
