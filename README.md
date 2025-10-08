# SSSD Lab 4: Security Vulnerabilities

## Setup

```bash
pip install -r requirements.txt
python app.py
```

App runs on: http://localhost:8001

## Test Vulnerabilities

```bash
# 1. Information leakage
curl http://localhost:8001/crash

# 2. Config exposure  
curl http://localhost:8001/show-config

# 3. Unsafe deserialization
curl "http://localhost:8001/deserialize?data=Y2NvcHlfcmVnCl9yZWNvbnN0cnVjdG9yCnAwCihjb21tYW5kcy5nZXRvcwpwMQp0cDIKUnAzCi4%3D"

# 4. No authentication
curl http://localhost:8001/admin/users
```
