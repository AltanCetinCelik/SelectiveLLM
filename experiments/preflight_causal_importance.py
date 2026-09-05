#!/usr/bin/env python3
"""Run the invariant-only objective-gradient preflight."""

from selectivellm.causal_importance.runner import CausalImportanceRunner

if __name__ == "__main__":
    print(CausalImportanceRunner().preflight())
