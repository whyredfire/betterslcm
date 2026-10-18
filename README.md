# betterslcm

> **This project is archived** and no longer maintained. Development continues in the upstream project, [SLCM_APP](https://github.com/DK10WS/SLCM_APP/tree/web) (`web` branch).

An unofficial FastAPI wrapper around the MUJ SLCM student portal. It logs in with a student's portal credentials and returns attendance, CGPA, grades and internal marks as JSON.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/login` | Log in with `username` and `password` |
| `GET` | `/logout` | Log out |
| `GET` | `/attendance` | Attendance |
| `GET` | `/cgpa` | CGPA |
| `GET` | `/grades` | Grades |
| `GET` | `/internal_marks` | Internal marks |
| `GET` | `/status` | Health check |

FastAPI also serves interactive docs at `/docs`.

## Running

```bash
docker compose up
```

The API is then available at `http://localhost:8000`.

## License

Released under the [MIT License](LICENSE).
