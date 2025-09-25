# GoToSocial Cleaner  

A script to delete old posts on your GoToSocial server, helping keep your Fediverse clean and efficient.  

## Acknowledgement & WARNING

The script is forked from [xurxia/gts-cleaner](https://github.com/xurxia/gts-cleaner) and heavily vibe-coded. Use at your own risk!

## Features  

- **Automated cleanup:** Removes old posts based on a date range or customizable conditions.  
- **Flexible configuration:** Define which posts to keep and which to delete.  
- **Compatibility:** Specifically designed for GoToSocial servers.  

## Requirements  

- Python 3.7 or higher.  
- [API access to your GoToSocial server](https://docs.gotosocial.org/en/latest/api/authentication) with appropriate permissions.  

## Installation  

1. Clone the repository:  

   ```bash
   git clone https://github.com/kpocius/gts-cleaner.git
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
   "language": "en",
   "server_url": "https://your-server.social",
   "access_token": "your-access-token",
   "delete_older_than_days": 30,
   "dryrun": true
   }
   ```

2. Run the script

   ```bash
   python main.py
   ```

3. If you are happy with Dry Run results, set `"dryrun": false` and run it again.

## Warning

- This script permanently deletes posts! Make sure to run it with `"dryrun": true` first.
- Back up any important data if necessary.

## Contributions

Contributions are welcome! If you have ideas to improve this project, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit).
