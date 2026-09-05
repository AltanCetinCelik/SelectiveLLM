#!/usr/bin/env python3
"""Execute the preregistered dense-capacity feasibility experiment."""

from selectivellm.dense_capacity.runner import DenseCapacityRunner

if __name__ == "__main__":
    path = DenseCapacityRunner().run()
    print(path)
