env:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	echo "TWILIO_ACCOUNT_SID=<ENTER_HERE>" > .env
	echo "TWILIO_AUTH_TOKEN=<ENTER_HERE>" >> .env
	echo "TWILIO_NUMBER=<ENTER_HERE>" >> .env
	pre-commit install

clean:
	rm -rf venv
