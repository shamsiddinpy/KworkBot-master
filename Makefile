restart_doc:
	docker compose down
	docker rmi kworkbot-master-bot :latest
	docker compose up


