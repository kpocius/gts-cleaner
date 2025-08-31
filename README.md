# GoToSocial Cleaner  

A script to delete old posts on your GoToSocial server, helping keep your Fediverse clean and efficient.  

## Features  

- **Automated cleanup:** Removes old posts based on a date range or customizable conditions.  
- **Flexible configuration:** Define which posts to keep and which to delete.  
- **Compatibility:** Specifically designed for GoToSocial servers.  

## Requirements  

- Python 3.7 or higher.  
- API access to your GoToSocial server with appropriate permissions.  

## Installation  

1. Clone the repository:  

   ```bash
   git clone https://github.com/xurxia/gts-cleaner.git
   cd gts-cleaner
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Configure your access credentials and parameters in the config.json file:

   ```json
   {
   "server_url": "https://your-server.social",
   "access_token": "your-access-token",
   "delete_older_than_days": 30
   }
   ```

2. Run the script

   ```bash
   python main.py
   ```

## Warning

- This script permanently deletes posts. Make sure to review the settings before running it.
- Back up any important data if necessary.

## Contributions

Contributions are welcome! If you have ideas to improve this project, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit).
