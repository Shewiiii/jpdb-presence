## Prerequisites
Make sure [Python](https://www.python.org/downloads/) 3.8 or above is installed on your PC.
## Installation 
1. Clone the repo.
2. Open the directory in Terminal.
3. Install the dependencies:
```cmd
pip install -r requirements.txt
```
3. Create a Discord application:    
   - Navigate to [Discord Developer Portal](https://discord.com/developers/), log in, and click `New Application`.
   - Name your application `jpdb` (This will be the name displayed in the rich presence).
   - Go to the Rich Presence section, and click `Add Image(s)` in the Assets section.
   - Select the `logo.png` file in the directory (it can be any image you want, as long as the file is named logo).
   - Go to the OAuth2 section, and locate your Client ID.

4. Get your jpdb SID/cookies (the cursed part):    
   - Navigate to [jpdb](https://jpdb.io/), log in.
   - Press `F12`, and click `Application` (Chrome) or `Storage` (Firefox).
   - Copy your sid value.
> [!WARNING]
> NEVER share your SID, anyone with a valid SID can instantly log in to your account. Your sid will not be valid anymore if you log out.

6. Create an `.env` file in jpdb-presence directory with the following lines:
```env
SID=<Your jpdb SID>
CLIENT_ID=<Your application's client ID>
```

7. Run the `main.py` file:
```cmd
python main.py
```
You can create a `jpdb-presence.bat` file on your desktop if you want to speed up the process, with the following in it:
```cmd
python absolute/path/to/main.py
```

If the logo does not appear yet, please wait a few minutes, Discord assets do not update instantly.
