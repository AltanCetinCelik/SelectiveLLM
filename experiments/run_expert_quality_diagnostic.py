"""Execute the preregistered v0.1.2 expert-quality diagnostic."""

from selectivellm.real_validation.expert_quality_runner import ExpertQualityDiagnosticRunner

if __name__ == "__main__":
    run = ExpertQualityDiagnosticRunner().run()
    print(run)
