POETRY_BIN ?= ~/.local/bin/poetry

# ------------------------------------------
# dependency management
# ------------------------------------------

lock-no-update:
	$(POETRY_BIN) lock --no-update

lock-update:
	$(POETRY_BIN) lock

poetry-check-lock:
	$(POETRY_BIN) lock --check

pip-compatible:
	$(POETRY_BIN) run poetry-setup


# ------------------------------------------
# git
# ------------------------------------------
setup-precommit:
	rm -rf .git/hooks
	$(POETRY_BIN) run pip install pre-commit
	$(POETRY_BIN) run pre-commit install

hooks: setup-precommit

# ------------------------------------------
# newsfragments
# ------------------------------------------

towncrier_draft:
	$(POETRY_BIN) run towncrier --draft

towncrier_build:
	$(POETRY_BIN) run towncrier
