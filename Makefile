restart_doc:
	docker compose down
	docker rmi kworkbot-bot:latest
	docker compose up


