# CHAD / LapisLLM / Vibe Coding Instructions ecosystem

The three repositories form one engineering ecosystem with deliberately separate responsibilities.

```text
vibe-coding-instructions
        |
        | policies / skills / role contracts
        v
      CHAD
        |
        | model gateway / inference contract
        v
    LapisLLM
```

## Responsibility matrix

| Repository | Owns | Must not own |
|---|---|---|
| vibe-coding-instructions | agent governance, skills, role contracts, evidence rules, token economics, self-improvement policy | runtime execution, user accounts, model training |
| CHAD | product UI/API, orchestration runtime, agents, tools, memory, files, provider routing, permissions | Transformer internals, model training |
| LapisLLM | tokenizer, Transformer, training, checkpoints, inference runtime, model evaluation, model-serving primitives | consumer UX, accounts, agent orchestration, product memory |

## Relationship

Vibe Coding Instructions is a **policy/control-plane repository for engineering agents**. It is not required to be deployed as CHAD's runtime.

CHAD may consume the role contracts and selected skills from this repository. It should not blindly copy every host-specific instruction file into the product runtime.

LapisLLM exposes model capabilities through a stable runtime boundary. CHAD consumes that boundary through its provider/model gateway.

## Runtime trust model

```text
trusted application policy
        >
agent role policy
        >
user request
        >
model output
        >
tool output / web pages / files
```

The exact execution implementation belongs to CHAD. This repository defines the policy expectations.

## Agent roles

The initial role vocabulary shared across the ecosystem is:

- **orchestrator** — decomposes bounded tasks and coordinates execution;
- **researcher** — retrieves and synthesizes evidence;
- **coder** — performs repository/code work through constrained tools;
- **analyst** — analyzes files, data and multimodal inputs.

A role contract defines responsibilities, required inputs, allowed tools, stop conditions, evidence requirements and handoff format. It does not define a particular model provider.

## Change propagation

A contract change that crosses repository boundaries must be updated in the affected repositories and verified with integration tests where feasible.

Example:

```text
Lapis adds capability metadata
        ↓
Lapis runtime contract updated
        ↓
CHAD provider adapter updated
        ↓
CHAD routing tests updated
        ↓
ecosystem docs updated
```

Do not silently change one repository and assume the other two remain compatible.

## Non-goal

The ecosystem is not a monorepo. Separate repositories are intentional because the model engine, product runtime and coding-agent governance have different release cycles and security boundaries.
