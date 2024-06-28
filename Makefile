all: build
format:
	black . -l 79
	linecheck . --fix
documentation:
	jb build docs
install:
	pip install -e .[dev]
test:
	pytest reweight/tests/ --maxfail=0
changelog:
	build-changelog changelog.yaml --output changelog.yaml --update-last-date --start-from 0.0.1 --append-file changelog_entry.yaml
	build-changelog changelog.yaml --org PolicyEngine --repo reweight --output CHANGELOG.md --template .github/changelog_template.md
	bump-version changelog.yaml setup.py
	rm changelog_entry.yaml || true
	touch changelog_entry.yaml
build:
	python setup.py sdist bdist_wheel