## **This project is crucial-crawler**

### Docker images build

use the following to change the user to **desired user**

```shell
sudo su <desired user>
```

Build Image using following command

```shell
sudo docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) --build-arg UNAME=$(whoami) -t crucial_crawler:v1.0.0 -f Docker/Dockerfile .
```

**Note: Docker image for crawler is available as `crucial_crawler:v1.0.0`**

### Deploy

DB Configuration must set in `.env`
The working directory is set in _docker-compose.yml_.

```shell
sudo docker-compose --project-name crucial_crawler up -d
```

### Check Logs

```shell
sudo docker logs <container_id> -f 
```

or in `logs/` folder.

### Stop

```shell
sudo docker-compose --project-name crucial_crawler down
```

## Todo

- [X] Category in json_fixer must fix
- [ ] 'from size' for elasticsearch must add

## Celery

```shell
celery -A app worker -l INFO -c1 -P solo -Q crucial,memorycow
```

# Get number of workers

```shell
celery -A app status
```
