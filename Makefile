build:
	@echo "Building image"
	docker build --rm -t 3liz/changelog-release:0.4.0 .
