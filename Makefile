MAKEFLAGS += --always-make

VERSION := $(shell python3 -c "from tomllib import load; print(load(open('.xproject_python', 'rb'))['version'])")
SUBPKGS := xpip-mirror xpip-upload xpip-build

all: build reinstall test

release: all
	if [ -n "${VERSION}" ]; then \
		git tag -a v${VERSION} -m "release v${VERSION}"; \
		git push origin --tags; \
	fi

version:
	@echo ${VERSION}

OPS := build clean test install uninstall reinstall

define make_target_rule
.PHONY: $(1)-$(2)
$(1)-$(2):
	@echo "Running '$(1)' in '$(2)'..."
	@make -C $(2) $(1)
endef

$(foreach op,$(OPS),$(foreach pkg,$(SUBPKGS),$(eval $(call make_target_rule,$(op),$(pkg)))))

test: $(foreach pkg,$(SUBPKGS),test-$(pkg))
build: $(foreach pkg,$(SUBPKGS),build-$(pkg))
clean: $(foreach pkg,$(SUBPKGS),clean-$(pkg))
install: $(foreach pkg,$(SUBPKGS),install-$(pkg))
uninstall: $(foreach pkg,$(SUBPKGS),uninstall-$(pkg))
reinstall: $(foreach pkg,$(SUBPKGS),reinstall-$(pkg))