# STAT 159 – HW3 Makefile
# Author: Riley Yu
# Description: Automates environment setup, site build, and cleanup tasks.

# === Environment Setup ===
# Creates or updates the conda environment using the provided environment.yml file.
env:
	@echo "Setting up or updating the conda environment using environment.yml..."
	conda env update -f environment.yml --prune

# === Build MyST HTML Site ===
# Builds the HTML version of the MyST website so it can be viewed locally.
html:
	@echo "Building the local HTML version of the MyST website..."
	myst build --html

# === Cleanup ===
# Remove generated output folders to keep the workspace clean.
clean:
	@echo "Cleaning up generated output folders: figures, audio, and _build..."
	rm -rf figures/* audio/* _build/*
