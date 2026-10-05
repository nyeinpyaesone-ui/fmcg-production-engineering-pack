lint:
	yamllint -c .yamllint.yaml config/agent-policy.yaml
	npx --yes markdownlint-cli2 "README.md" "docs/**/*.md" ".agents/**/*.md"
	python3 scripts/check_docs.py
	gitleaks detect --no-git --source . || true

verify: lint
