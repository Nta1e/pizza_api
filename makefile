DOCKER_COMPOSE_FILE=./docker/docker-compose.yml

# Build the required images
build:
	${INFO} "Building the required docker images"
	@ docker-compose -f $(DOCKER_COMPOSE_FILE) build
	${SUCCESS} "Build Completed successfully"
	@ echo " "

# Start all the containers
start:
	${INFO} "Starting all containers"
	@ echo " "
	@ docker-compose -f $(DOCKER_COMPOSE_FILE) up

# stop all the containers
stop:
	${INFO} "Stopping docker containers"
	@ echo " "
	@ docker-compose -f $(DOCKER_COMPOSE_FILE) down -v
	${SUCCESS} "All containers stopped successfully"

#colors
GREEN 	:= $(shell tput -Txterm setaf 2)
YELLOW 	:= $(shell tput -Txterm setaf 3)
NC 	:= "\e[0m"

# shell functions
INFO 	:= @bash -c 'printf $(YELLOW); echo "===> $$1"; printf $(NC)' SOME_VALUE
SUCCESS := @bash -c 'printf $(GREEN); echo "===> $$1"; printf $(NC)' SOME_VALUE
