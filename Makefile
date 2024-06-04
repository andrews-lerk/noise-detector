py := pdm run
package_dir := src
tests_dir := tests

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: detector
detector: ## Run noise detection process
	$(py) python -m $(package_dir).noise_detector.cli.detector --listen_secs=$(listen_secs) --delay=$(delay)

.PHONY: volume
volume: ## Run volume level present
	$(py) python -m $(package_dir).noise_detector.cli.volume

.PHONY: install
install: ## Install all depends
	pdm install -G:all

.PHONY: init
init: ## Init config and results dir
	cp -r config.dist config
	mkdir results