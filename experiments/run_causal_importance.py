#!/usr/bin/env python3
"""Execute the preregistered causal-importance discovery experiment."""

from selectivellm.causal_importance.runner import CausalImportanceRunner

if __name__ == "__main__":
    print(CausalImportanceRunner().run())
