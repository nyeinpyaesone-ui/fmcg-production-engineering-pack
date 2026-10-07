lint:
	yamllint -c .yamllint.yaml config/agent-policy.yaml
	yamllint -c .yamllint.yaml .github/workflows/quality.yml .github/workflows/release.yml
	npx --yes markdownlint-cli2 "README.md" "docs/**/*.md" ".agents/**/*.md"
	python3 scripts/check_docs.py
	gitleaks detect --no-git --source . || true

verify: lint
