#!/usr/bin/env python3
"""
Sage CLI launcher.

This wrapper should behave like the installed `sage` command, including
subcommands such as `gateway`, `cron`, and `doctor`.
"""

if __name__ == "__main__":
    from sage_cli.main import main
    main()
