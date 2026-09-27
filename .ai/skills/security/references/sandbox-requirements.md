# Sandbox Requirements & Execution Isolation Governance

## Metadata
- **document_id**: `sandbox_requirements`
- **version**: `1.0.0`
- **ecosystem**: CHAD / LapisLLM / Vibe Coding Instructions
- **domain**: Security & Tool Governance

## Purpose
Define the governance standards, isolation levels, resource quotas, network egress controls, and secret boundary requirements for tool execution and code evaluation within the CHAD agent runtime and LapisLLM ecosystem.

---

## 1. Sandbox Isolation Taxonomy

To align with permission levels defined in `.ai/contracts/tool.contract.md`, tool execution environments must be isolated according to four security tiers:

| Isolation Tier | Description | Allowed Permission Levels | Core Isolation Controls |
|---|---|---|---|
| **Level 0: Host Process** | Native process execution on host machine without additional containerization. | `READ_ONLY` | Unprivileged UID/GID, restricted read paths, read-only filesystem mounts. |
| **Level 1: Process-Bound** | Restricted subprocess with cgroups, namespace unsharing, and seccomp syscall filters. | `WORKSPACE_WRITE` | Restricted to workspace root (`/workspace`), no host network namespace (`CLONE_NEWNET`), blocked `ptrace` and `chroot`. |
| **Level 2: Container/microVM** | Isolated container (Docker/Podman/gVisor) or microVM (Firecracker/Kata) per session. | `ISOLATED_EXECUTE`, `NETWORK_ACCESS` | Ephemeral rootfs, non-root user, cgroup v2 limits, drop all Linux capabilities (`CAP_DROP=ALL`), default-deny network egress. |
| **Level 3: Air-Gapped Ephemeral** | Transient microVM destroyed immediately after tool completion. | `PRIVILEGED_MUTATION` | Strict single-use lifecycle, zero host disk persistence, isolated ephemeral virtual network, mandatory human checkpoint before dispatch. |

---

## 2. Resource Quotas & Runtime Limits

Every sandboxed execution environment must enforce strict cgroup and system quotas to prevent Denial of Service (DoS) attacks, infinite loops, fork bombs, and resource exhaustion:

```yaml
resource_limits:
  cpu_quota: 2.0                # Maximum 2.0 vCPU cores
  memory_limit: "2048MB"        # Hard limit on memory consumption
  memory_swap: "0MB"            # Swap memory disabled
  pids_limit: 100               # Hard process/thread count limit (fork bomb defense)
  disk_quota: "1024MB"          # Ephemeral tmpfs/workspace disk quota
  execution_timeout_seconds: 60 # Hard process execution timeout
  output_buffer_bytes: 1048576  # 1MB output buffer limit for stdout/stderr logs
```

---

## 3. Network Egress Controls

Sandboxed execution (`NETWORK_ACCESS`, `ISOLATED_EXECUTE`) must strictly restrict external network connectivity to defend against data exfiltration and unauthorized command-and-control (C2) communication:

1. **Default-Deny Policy**: All outbound TCP/UDP traffic is blocked by default at the firewall/network namespace boundary.
2. **Domain/IP Allowlisting**: Egress is restricted exclusively to approved domain names or CIDR blocks required by the tool contract (e.g., package registries, target APIs).
3. **Egress Proxying & TLS Inspection**:
   - Outbound requests pass through a transparent egress proxy.
   - Headers are sanitized; Authorization tokens and credentials are masked.
4. **Local Loopback Isolation**: Sandboxes are isolated from local host services (`127.0.0.1`, `localhost`, `169.254.169.254` cloud metadata endpoints).

---

## 4. Environment & Secret Boundary Isolation

Secrets (API keys, passwords, private tokens) must never bleed into sandboxed execution environments or untrusted tool invocations:

1. **Ephemeral File System**: Tools run on ephemeral `tmpfs` mounts that are completely wiped upon tool completion.
2. **Environment Variable Scrubbing**:
   - Host environment variables (`AWS_SECRET_ACCESS_KEY`, `GITHUB_TOKEN`, etc.) are stripped prior to sandbox initialization.
   - Only explicitly whitelisted, non-sensitive runtime variables (`PATH`, `LANG`, `TERM`) are exposed.
3. **Secret Masking & Redaction**:
   - Standard output (`stdout`) and standard error (`stderr`) streams are scanned by a regex redaction filter before being returned to the agent context.
   - Identified secrets are replaced with `[REDACTED_SECRET]`.

---

## 5. Audit Logging & Syscall Filtering

1. **Syscall Filtering (Seccomp)**:
   - Sandboxes must run under a restrictive seccomp profile blocking dangerous system calls (`unshare`, `kexec_load`, `reboot`, `init_module`, `bpf`).
2. **Telemetry & Execution Trace**:
   - Every tool call produces a structured execution trace containing:
     - `session_id` and `agent_id`
     - `tool_id` and declared `permission_level`
     - Exit code, execution duration, and peak memory usage
     - Cryptographic hash (SHA-256) of input arguments and output payload
3. **Trust Labeling**:
   - All stdout/stderr and output files generated inside the sandbox are tagged with `ISOLATED_SANDBOXED` trust level in accordance with `.ai/contracts/tool.contract.md`.

---

## 6. Ecosystem Compatibility

- **CHAD Runtime**: CHAD manages container/microVM lifecycle, enforces cgroup quotas, provisions ephemeral mounts, and inspects network egress proxies.
- **LapisLLM Model Gateway**: LapisLLM receives sandbox telemetry and handles `ISOLATED_SANDBOXED` trust labels during model context composition, preventing prompt injection from untrusted stdout/stderr contents.
