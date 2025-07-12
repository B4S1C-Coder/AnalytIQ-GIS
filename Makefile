.PHONY: whisper-test

whisper-test:
	cd whisper_test && poetry run uvicorn app:app --host 0.0.0.0 --port 8000