.PHONY: fetch sim run

fetch:
	python scripts/fetch_data.py $(ARGS)

sim:
	@echo "Fortran simulation build not implemented yet"

run:
	@echo "Go client not implemented yet"
