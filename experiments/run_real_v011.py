"""Execute the pinned v0.1.1 real-model validation."""

from selectivellm.real_validation.runner import RealBenchmarkRunner

if __name__ == "__main__":
    run = RealBenchmarkRunner().run(warm_repetitions=3)
    print(run)
