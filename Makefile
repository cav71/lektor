

# self-documentation magic: http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## Display the list of available targets
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: check
check:  ## check code (ruff, mypy, and flake8)
	ruff check
	dmypy run -- --follow-import=skip
	flake8

all: build-js  ## build all

.PHONY: build-js
build-js: frontend/node_modules  ## build js frontend
	@echo "---> cleaning static files"
	@rm -rf lektor/admin/static
	@echo "---> building static files"
	@cd frontend; npm run build

frontend/node_modules: frontend/package-lock.json
	@echo "---> installing npm dependencies"
	@cd frontend; npm install
	@touch -m frontend/node_modules

# Run tests on Python files.
test-python:  ## run tx python tests
	@echo "---> running python tests"
	tox -e py

# Run tests on the Frontend code.
test-js: frontend/node_modules
	@echo "---> running javascript tests"
	@cd frontend; npx tsc
	@cd frontend; npm test

.PHONY: lint
# Lint code.
lint:
	pre-commit run -a
	tox -e lint

.PHONY: test
test: lint test-python test-js

.PHONY: test-all
# Run tests on all supported Python versions.
test-all: test-js
	pre-commit run -a
	tox
