.PHONY: whisper-test integrations-test run

whisper-test:
	poetry run bash -c "source secrets.env && uvicorn whisper_test.app:app --host 0.0.0.0 --port 8000"

integrations-test:
	bash -c "source secrets.env && poetry run python3 -m integrations.test"

run:
	@bash -c "source secrets.env && $(TARGET)"