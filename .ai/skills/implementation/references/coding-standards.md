# Coding Standards

## General

Prefer readable code with explicit control flow, small functions, stable interfaces, and minimal side effects.

## Consistency

Follow the existing project's naming, formatting, file structure, error handling, and testing conventions. Do not impose a new style because it seems cleaner in isolation.

## Inputs

Validate external input at trust boundaries. Keep validation close to the boundary unless the repository already centralizes it.

## Errors

Do not swallow errors silently. Preserve useful context and avoid exposing sensitive information.

## Tests

Add focused regression coverage for behavior that could regress. Test the contract, not private implementation details, unless the repository convention requires otherwise.

## Security

Use least privilege. Do not hard-code secrets. Avoid unsafe shell construction, string-based SQL, dynamic code execution, and unbounded resource usage.

## Dependencies

Prefer existing dependencies. When a new dependency is necessary, record the reason, version strategy, and verification impact in the plan.

## Configuration

Keep configuration explicit. Document new environment variables and define safe defaults where appropriate.

## Performance

Do not optimize speculative bottlenecks. Measure or identify concrete risk before complicating a design for performance.

## Compatibility

Preserve public API contracts unless a breaking change is explicitly requested. When changing a contract, update tests and documentation together.

## Generated files

Do not hand-edit generated files when a repository generator exists. Run the generator and verify the result.
