# Glance serverstatus agent
A flask endpoint for Glance serverstatus widget for remote servers.

Clone the repository:
```bash
git clone https://github.com/kubakubakuba/glance-serverstatus-agent.git
```

Modify the `.env` file:
```
SECRET_TOKEN=your-secret-token
PORT=8080
```

Build the docker image:
```bash
docker compose build
```

Run the docker container:
```bash
docker compose up -d
```

You can now test that the endpoint is working:

```
curl -H "Authorization: Bearer your-secret-token" http://localhost:8080/api/sysinfo/all
```