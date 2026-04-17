import requests
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class APIClient:
    """Cliente HTTP reutilizable para pruebas de API."""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"→ GET {url} params={params}")
        r = self.session.get(url, params=params, timeout=self.timeout)
        logger.info(f"← {r.status_code} | {r.elapsed.total_seconds():.3f}s")
        return r

    def post(self, endpoint, json=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"→ POST {url}")
        r = self.session.post(url, json=json, timeout=self.timeout)
        logger.info(f"← {r.status_code} | {r.elapsed.total_seconds():.3f}s")
        return r

    def put(self, endpoint, json=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"→ PUT {url}")
        r = self.session.put(url, json=json, timeout=self.timeout)
        logger.info(f"← {r.status_code} | {r.elapsed.total_seconds():.3f}s")
        return r

    def patch(self, endpoint, json=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"→ PATCH {url}")
        r = self.session.patch(url, json=json, timeout=self.timeout)
        logger.info(f"← {r.status_code} | {r.elapsed.total_seconds():.3f}s")
        return r

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"→ DELETE {url}")
        r = self.session.delete(url, timeout=self.timeout)
        logger.info(f"← {r.status_code} | {r.elapsed.total_seconds():.3f}s")
        return r
