<h1 align="center">DeviceAuthGenerator</h1>

<p align="center">
    <a href="https://www.python.org/downloads/" align="center">
        <img alt="Python" src="https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue">
    </a>
    <a href="https://www.python.org/dev/peps/pep-0008/" align="center">
        <img alt="PEP8" src="https://img.shields.io/badge/PEP8-compliant-brightgreen.svg">
    </a>
</p>

<p align="center">Program to easily create device auths for use in Epic Games API authentication.</p>

---

## Discord Support:
<a href="https://discord.gg/8heARRB"><img src="https://discordapp.com/api/guilds/624635034225213440/widget.png?style=banner2"></a>

---
## Example Usage:
<img src="https://i.imgur.com/weIdKDD.gif" />

## Usage:
DeviceAuthGenerator is pretty simple to use. You can either use run the Python script directly or use the pre-compiled
executable in the <a href="#">releases</a>.
1. Install the requirements _(only applies to the Python script, you don't need to install requirements for the executable)_.

    ```
    pip install -U -r requirements.txt
    ```

2. Run DeviceAuthGenerator, either being `generator.py` or `DeviceAuthGenerator.exe`.

3. Login the the Epic Games account you wish to generate device auths for when prompted.

3. Wait 5 or less seconds for device auths to be generated. They will then be pasted into the console, copied to
clipboard & saved in `device_auths.json` which is compatible out of the box with
   <a href="https://github.com/Terbau/fortnitepy">fortnitepy</a>.
   
## Example responses:
### Console
```json
Generated device auths for: xMistt.
{
    "device_id": "c403e1ea918b4414b01f6292ee7bbad2",
    "account_id": "ab0f2bb71b1d4e73ac467bd1b1072061'",
    "secret": "61E9F2025EA14493A63CD94AD1B9C569",
    "user_agent": "DeviceAuthGenerator/1.0.0 Windows/10",
    "created": {
        "location": "London, England",
        "ip_address": "215.42.168.146",
        "datetime": "2021-05-15T16:57:46.372Z"
    }
}

```
___
### File
```json
{
    "xmistt@partybot.com": {
        "device_id": "c403e1ea918b4414b01f6292ee7bbad2",
        "account_id": "ab0f2bb71b1d4e73ac467bd1b1072061",
        "secret": "61E9F2025EA14493A63CD94AD1B9C569",
        "user_agent": "DeviceAuthGenerator/1.0.0 Windows/10",
        "created": {
            "location": "London, England",
            "ip_address": "215.42.168.146",
            "datetime": "2021-05-15T16:57:46.372Z"
        }
    }
}
```
## Compiling:
You can compile DeviceAuthGenerator yourself by installing the requirements and pyinstaller, then you can compiile it by the command: 
```
pyinstaller --onefile -i icon.ico -n DeviceAuthGenerator generator.py
```
The executable will be found in `/dist`.


## License:
By downloading this, you agree to the Commons Clause license and that you're not allowed to sell this repository or any code from this repository. For more info see https://commonsclause.com/.
