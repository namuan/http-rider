export PROJECTNAME=$(shell basename "$(PWD)")

.SILENT: ;               # no need for @

release: ## Step to prepare a new release
	echo "Instructions to prepare release"
	echo "Repo: http-rider: Increment version in httprider/__init__.py"
	echo "Repo: http-rider: Increment version in .travis.yml"
	echo "Commit - Preparing Release x.x.x"
	echo "Check Differences between Releases using Fork"
	echo "Repo: http-rider-osx: Increment version in .travis.yml"
	echo "Commit - Release x.x.x - MacOS"
	echo "Repo: http-rider-win: Increment version in .appveyor.yml"
	echo "Commit - Release x.x.x - Windows"
	echo "Repo: http-rider: Update Download Links in README.md"
	echo "Repo: http-rider-docs: Update content/en/docs/getting-started/installation.md"

black: ## Runs black for code formatting
	./venv/bin/black httprider

lint: black ## Runs Flake8 for linting
	./venv/bin/flake8 httprider

deps: ## Reinstalls dependencies
	./venv/bin/python3 -m pip install --upgrade pip
	./venv/bin/python3 -m pip install -U -r requirements/dev.txt

clean: ## Clean package
	rm -rf build dist

setup: ## Re-initiates virtualenv
	rm -rf venv
	python3.9 -m venv venv
	./venv/bin/python3 -m pip install -r requirements/dev.txt
	echo "Once everything is installed, 'make run' to run the application"

package: clean ## Rebuilds venv and packages app
	./venv/bin/python3 -m pip install -r requirements/build.txt
	export PYTHONPATH=`pwd`:$PYTHONPATH && ./venv/bin/python3 setup.py bdist_app

uic: ## Converts ui files to python
	for i in `ls resources/ui/*.ui`; do FNAME=`basename $${i} ".ui"`; ./venv/bin/pyuic6 $${i} > "httprider/generated/$${FNAME}.py"; done

run: ## Runs the application
	export PYTHONPATH=`pwd`:$PYTHONPATH && ./venv/bin/python3 httprider/application.py

test: ## Run all unit tests
	export PYTHONPATH=`pwd`:$PYTHONPATH && ./venv/bin/pytest httprider/tests

uitest: ## Run all unit tests
	rm -vf $$HOME/Library/Preferences/Python/httprider.db
	export PYTHONPATH=`pwd`:$PYTHONPATH && ./venv/bin/pytest uitests

runapp: ## Runs the packaged application
	./dist/HttpRider.app/Contents/MacOS/app

install-macosx: package ## Installs application in users Application folder
	./scripts/install-macosx.sh httprider.app

icns: ## Generates icon files from svg
	echo "Run ./mk-icns.sh resources/icons/httprider.svg httprider"

.PHONY: help
.DEFAULT_GOAL := help

help: Makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo