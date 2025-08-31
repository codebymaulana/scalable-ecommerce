import requests

def call_service(url: str, method: str = "GET", data: dict = None, headers: dict = None):
    """
    Utility function to call an external service.
    """
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")

        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Service call failed: {str(e)}")