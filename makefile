BREW_TAP_REPO=git@github.com:benwainwright/homebrew-tools.git
NAME=call
PYTHON=python3
VENV=venv
BIN=venv/bin
PYTHON=$(BIN)/python3
PIP=$(BIN)/pip3


$(VENV):
	virtualenv -p python3 $(VENV)

install: $(VENV) requirements.txt
	$(PIP) install -r requirements.txt

build:
	$(PYTHON) setup.py sdist bdist_wheel

release: | release-tag update-tap

release-tag:
	git tag -m "$(NAME) $(RELEASE_VERSION)" $(RELEASE_VERSION)
	git push origin --tags

releases/%.tar.gz:
	if [ ! -d "releases" ]; then mkdir releases; fi
	curl --silent -L https://github.com/benwainwright/call/archive/$(*).tar.gz > releases/$(*).tar.gz

update-tap: releases/$(RELEASE_VERSION).tar.gz
	$(eval SHASUM := $(shell shasum -a 256 releases/$(RELEASE_VERSION).tar.gz | awk '{print $$1}'))
	git clone $(BREW_TAP_REPO) .tap-clone
	sed -E -i .bak 's/(https:\/\/github\.com\/benwainwright\/call\/archive\/)[0-9]+\.[0-9]+\.[0-9]+\.tar\.gz/\1$(RELEASE_VERSION)\.tar.gz/g' .tap-clone/Formula/call.rb
	sed -E -i .bak "s/(sha256 )'[0-9a-z]*'/\1'$(SHASUM)'/g" .tap-clone/Formula/call.rb
	cd .tap-clone && git add Formula/call.rb && git commit -m "Update $(NAME) to $(RELEASE_VERSION)" && git push origin master
	rm -rf .tap-clone
