import requests
import json
import os
from datetime import datetime


def load_locale(language):
    # Load the locale file for the selected language.
    locale_path = os.path.join(os.path.dirname(__file__), "locales", f"{language}.json")
    try:
        with open(locale_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to English if selected language file is missing
        with open(
            os.path.join(os.path.dirname(__file__), "locales", "en.json"),
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)


def t(key, locale_dict):
    # Translate a key using the loaded locale dictionary.
    return locale_dict.get(key, key)


def load_config():
    # Load configuration from config.json.
    with open("config.json", "r") as config_file:
        return json.load(config_file)


# Load config and locale at startup
config = load_config()
locale_dict = load_locale(config.get("language", "en"))


def get_headers(access_token):
    # Generate headers for HTTP requests.
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


def get_statuses(base_url, headers):
    # Get all user statuses.
    statuses = []
    url = f"{base_url}/api/v1/accounts/verify_credentials"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        account_id = response.json()["id"]
        next_url = f"{base_url}/api/v1/accounts/{account_id}/statuses"
        while next_url:
            resp = requests.get(next_url, headers=headers)
            if resp.status_code != 200:
                raise Exception(
                    f"{t('error_file_not_found', locale_dict)}: {resp.status_code}"
                )
            data = resp.json()
            statuses.extend(data)
            # Search for the "next" link in pagination
            next_url = None
            if "Link" in resp.headers:
                links = resp.headers["Link"].split(", ")
                for link in links:
                    if 'rel="next"' in link:
                        next_url = link.split("; ")[0].strip("<>")
                        break
    else:
        raise Exception(
            f"{t('error_file_not_found', locale_dict)}: {response.status_code}"
        )
    return statuses


def delete_status(base_url, headers, status_id):
    # Delete a status given its ID.
    url = f"{base_url}/api/v1/statuses/{status_id}"
    response = requests.delete(url, headers=headers)
    # Construct the public status URL
    # Try to get the account from the global context if possible
    # (This function is now always called with status_id only, so we can't get acct directly)
    # We'll print the URL in the same way as in dryrun, but without the account name if not available
    # The main loop will pass the full status object for dryrun, but only status_id for actual deletion
    status_url = f"{base_url}/statuses/{status_id}"
    if response.status_code != 200:
        print(
            t("error_deleting_status", locale_dict).format(
                status_id=status_id, code=response.status_code
            )
        )


def is_old_and_not_pinned_or_bookmarked(status, days_old):
    # Determine if a status is old, not pinned, and not bookmarked.
    created_at = datetime.strptime(status["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    if (datetime.utcnow() - created_at).days > days_old:
        if not status.get("pinned", False) and not status.get("bookmarked", False):
            return True
    return False


def main():
    # Main function.
    # Load configuration
    config = load_config()
    base_url = config["server_url"]
    access_token = config["access_token"]
    days_old = config["delete_older_than_days"]
    dryrun = config.get("dryrun", True)

    # Generate headers
    headers = get_headers(access_token)

    # Get and process statuses
    print(t("getting_statuses", locale_dict))
    statuses = get_statuses(base_url, headers)
    print(t("found_statuses", locale_dict).format(count=len(statuses)))
    to_delete = []
    for status in statuses:
        if is_old_and_not_pinned_or_bookmarked(status, days_old):
            to_delete.append(status)

    if not to_delete:
        print(t("nothing_to_delete", locale_dict))
    else:
        for status in to_delete:
            acct = status.get("account", {}).get("acct", None)
            status_id = status["id"]
            if acct:
                status_url = f"{base_url}/@{acct}/statuses/{status_id}"
            else:
                status_url = f"{base_url}/statuses/{status_id}"
            if dryrun:
                print(t("dryrun_would_delete_url", locale_dict).format(url=status_url))
            else:
                # Pass only status_id to delete_status, which will print the URL without account name
                delete_status(base_url, headers, status_id)
                print(t("deleted_url", locale_dict).format(url=status_url))
        if dryrun:
            print(t("dryrun_count", locale_dict).format(count=len(to_delete)))
        else:
            print(t("deleted_count", locale_dict).format(count=len(to_delete)))


if __name__ == "__main__":
    main()
