.PHONY: help run test audit adversarial dist clean

help:
	@echo "RESETA™ Enterprise - Institutional Developer Operations"
	@echo "--------------------------------------------------------"
	@echo "make run          : Start local FastAPI backend and static server"
	@echo "make test         : Run automated pytest suite (54+ test vectors)"
	@echo "make audit        : Run platform link, route, and code quality audit"
	@echo "make adversarial  : Run 15-vector autonomous Red-Team safety benchmark"
	@echo "make dist         : Package clean enterprise distribution into dist/"
	@echo "make clean        : Remove temporary cache, coverage, and build artifacts"

run:
	./.venv/bin/uvicorn backend.main:app --reload --port 8000

test:
	./.venv/bin/python -m pytest tests/ -v

audit:
	./.venv/bin/python scripts/audit_platform.py

adversarial:
	./.venv/bin/python scripts/run_adversarial_suite.py

dist:
	./.venv/bin/python scripts/package_dist.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name ".DS_Store" -delete
	rm -rf dist/ build/ *.egg-info/ .coverage htmlcov/
