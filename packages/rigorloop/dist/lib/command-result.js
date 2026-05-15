export const EXIT = Object.freeze({
  success: 0,
  blocked: 2,
  validationFailed: 3,
  invalidUsage: 4,
  mutationConflict: 5,
  internal: 1,
});

const EXIT_CLASS_TO_CODE = Object.freeze({
  success: EXIT.success,
  blocked: EXIT.blocked,
  validation_failed: EXIT.validationFailed,
  invalid_usage: EXIT.invalidUsage,
  mutation_conflict: EXIT.mutationConflict,
  internal: EXIT.internal,
});

export function exitCodeForResult(result) {
  const exitClass = result.exit_class ?? result.exitClass;
  if (Object.hasOwn(EXIT_CLASS_TO_CODE, exitClass)) {
    return EXIT_CLASS_TO_CODE[exitClass];
  }

  if (result.status === "success" || result.status === "warning") {
    return EXIT.success;
  }
  if (result.status === "blocked") {
    return EXIT.blocked;
  }

  return EXIT.internal;
}
