from jnius import autoclass, cast
import json

# --- Import du wrapper Java ---
MiniHttpClient = autoclass("org.zoecorp.MiniHttpClient")


# --- Classe réponse compatible requests.Response ---
class AndroidResponse:
    def __init__(self, java_response_str):
        # Le Java renvoie un JSON {"status_code":.., "text":..}
        try:
            resp = json.loads(java_response_str)
            self.status_code = resp.get("status_code", 0)
            self.text = resp.get("text", "")
        except Exception:
            self.status_code = 0
            self.text = java_response_str

    def json(self):
        try:
            return json.loads(self.text)
        except Exception:
            return None


# --- Session Android utilisant MiniHttpClient ---
class AndroidHttpSession:
    def __init__(self):
        self.client = MiniHttpClient

    def request(self, method, url, **kwargs):
        data = kwargs.get("data")
        json_data = kwargs.get("json")
        payload = json.dumps(json_data or data) if (json_data or data) else None

        method_upper = method.upper()
        if method_upper == "GET":
            java_resp = self.client.get(url)
        elif method_upper == "POST":
            java_resp = self.client.post(url, payload)
        elif method_upper == "PUT":
            java_resp = self.client.put(url, payload)
        elif method_upper == "DELETE":
            java_resp = self.client.delete(url, payload)
        else:
            raise ValueError(f"Méthode HTTP non supportée: {method}")

        return AndroidResponse(java_resp)

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)
