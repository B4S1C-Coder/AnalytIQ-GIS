.PHONY: whisper-test

whisper-test:
	poetry run uvicorn whisper_test.app:app --host 0.0.0.0 --port 8000