import requests
import json
from datetime import datetime

def load_config():
    """Carga la configuración desde el archivo config.json."""
    with open("config.json", "r") as config_file:
        return json.load(config_file)

def get_headers(access_token):
    """Genera los encabezados para las solicitudes HTTP."""
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

def get_statuses(base_url, headers):
    """Obtiene todos los estados del usuario."""
    statuses = []
    url = f"{base_url}/api/v1/accounts/verify_credentials"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        account_id = response.json()["id"]
        next_url = f"{base_url}/api/v1/accounts/{account_id}/statuses"
        while next_url:
            resp = requests.get(next_url, headers=headers)
            if resp.status_code != 200:
                raise Exception(f"Error al obtener los estados: {resp.status_code}")
            data = resp.json()
            statuses.extend(data)
            # Busca el enlace "next" en la paginación
            next_url = None
            if "Link" in resp.headers:
                links = resp.headers["Link"].split(", ")
                for link in links:
                    if 'rel="next"' in link:
                        next_url = link.split("; ")[0].strip("<>")
                        break
    else:
        raise Exception(f"Error al verificar las credenciales: {response.status_code}")
    return statuses

def delete_status(base_url, headers, status_id):
    """Elimina un estado dado su ID."""
    url = f"{base_url}/api/v1/statuses/{status_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Estado {status_id} eliminado correctamente.")
    else:
        print(f"Error al eliminar el estado {status_id}: {response.status_code}")

def is_old_and_not_pinned_or_bookmarked(status, days_old):
    """Determina si un estado es antiguo, no está fijado y no está en marcadores."""
    created_at = datetime.strptime(status["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    if (datetime.utcnow() - created_at).days > days_old:
        if not status.get("pinned", False) and not status.get("bookmarked", False):
            return True
    return False

def main():
    """Función principal."""
    # Cargar la configuración
    config = load_config()
    base_url = config["server_url"]
    access_token = config["access_token"]
    days_old = config["delete_older_than_days"]

    # Generar encabezados
    headers = get_headers(access_token)

    # Obtener y procesar estados
    print("Obteniendo estados...")
    statuses = get_statuses(base_url, headers)
    print(f"Se han encontrado {len(statuses)} estados.")
    for status in statuses:
        if is_old_and_not_pinned_or_bookmarked(status, days_old):
            delete_status(base_url, headers, status["id"])

if __name__ == "__main__":
    main()