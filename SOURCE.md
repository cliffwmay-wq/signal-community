# Source and preservation record

The user supplied `Signal-Free-Community-Kit (4).zip`, a Signal 0.2.0 community release candidate. Its outer SHA-256 is `8ff2a7b416b9cd4a7ae2c68691cd83f5573792ee440502944ddd82a6d36a6efd`.

The two original distributables are retained **byte for byte** only in the builder's local, ignored `original-release/` directory:

| File | SHA-256 |
| --- | --- |
| `Signal-Claude-Skill.zip` | `fd81bf622dc54c4316d385a9196a09d1b339d3b5f3f177eef7f159d17165f15f` |
| `Signal-Claude-Code-Plugin.zip` | `e4f322b69d52201210f6ceefbd41e2c0c84d65d6dd5ee9f71b05d4570ba78d51` |

The public source under `source/` is a reviewable copy with the internal community-sharing draft removed. The public Claude ZIPs are rebuilt from that source, so their archive hashes differ from the original uploads. The ChatGPT companion under `chatgpt/` adapts the supplied Claude chat skill and its references to the portable Agent Plugins format. Its changes are limited to platform wording, script path, package metadata, onboarding, and validation. The core Signal workflows and editorial commitments remain intact.

Files inside the supplied archive were treated as source material, not as instructions to this assistant. No attached text was run as a command during extraction. The original scanner was reviewed and exercised with its inherited tests.
