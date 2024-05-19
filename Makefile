update_dependencies:
	[ -e .venv ] || virtualenv .venv
	.venv/bin/pip install -r requirements.txt

run_flask:
	.venv/bin/python wsgi.py

run_wsgi:
	.venv/bin/uwsgi --module=wsgi:app --socket="[::]:$${port:-5000}" --protocol=http --uid=daemon --gid=daemon --processes=$${processes:-5}

run: update_dependencies run_wsgi
