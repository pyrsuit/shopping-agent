Start docker compose

```sh
docker compose up -d
```

Pull the model into the running container (one-time)

```sh
docker exec -it ollama ollama pull llama3.2:3b
```
