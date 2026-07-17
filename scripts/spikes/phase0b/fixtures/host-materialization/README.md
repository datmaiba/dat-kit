# Host-materialization fixture

This fixture is non-public and must not be installed as a dat-kit capability.
Before every live host smoke:

1. Copy the fixture to a disposable directory outside the repository.
2. Replace the complete contents of `pack/probe.txt` with a newly generated,
   unpredictable nonce that appears nowhere else readable by the host.
3. Validate both plugin manifests, install or load the disposable copy, and
   start a fresh session from an empty working directory.
4. Ask only for the skill's required two-field result. Compare the returned
   value with the nonce after the session exits; record a hash in the report,
   not the nonce itself.
5. Remove the probe plugin, marketplace, disposable directory, and its exact
   empty cache namespace. Verify their absence.

The committed marker in `pack/probe.txt` is deliberately not valid live-smoke
evidence. A fixed or previously published oracle can be echoed without proving
that the pack file was read.
