# SSSD Lab 4: Security Vulnerabilities

**Student:** Kurbanova Anelya  
**ID:** 22B030555  
**GitHub:** https://github.com/AnelyaKurbanova/SSSD_lab4.git

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

## Vulnerabilities

| Issue | Endpoint | Risk |
|-------|----------|------|
| Info leakage | `/crash` | Stack trace exposure |
| Hardcoded secrets | Code | Credential compromise |
| Config in repo | `config.yml` | Password exposure |
| Unsafe deserialization | `/deserialize` | RCE vulnerability |
| Missing auth | `/admin/users` | Unauthorized access |

## Fix

Create `security-fixes` branch and fix all vulnerabilities in `app.py`.