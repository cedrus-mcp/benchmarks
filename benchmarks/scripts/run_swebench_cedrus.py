from __future__ import annotations

import sys
from pathlib import Path

from benchmarks.swebench.run_infer import main as swebench_main


DEFAULT_MCP_CONFIG = (
    Path(__file__).resolve().parents[1] / "swebench" / "mcp_config_swebench_cedrus.json"
)


def main() -> None:
    """Run swebench-infer with cedrus MCP config enabled.

    This is a thin wrapper around benchmarks.swebench.run_infer.main that
    ensures --mcp-config-path points at the default cedrus MCP config unless
    the user has already provided this flag.
    """

    # If the user already passed --mcp-config-path, just delegate; they are
    # taking full control of MCP configuration.
    if "--mcp-config-path" in sys.argv:
        swebench_main()
        return

    argv = sys.argv[1:]

    if not DEFAULT_MCP_CONFIG.is_file():
        raise SystemExit(
            f"Default cedrus MCP config not found: {DEFAULT_MCP_CONFIG}. "
            "Create it or pass --mcp-config-path explicitly."
        )

    argv = ["--mcp-config-path", str(DEFAULT_MCP_CONFIG), *argv]
    sys.argv = [sys.argv[0], *argv]
    swebench_main()


if __name__ == "__main__":  # pragma: no cover
    main()
