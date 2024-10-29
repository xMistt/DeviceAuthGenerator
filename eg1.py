import os
import sys
import json
import asyncio
import requests
import webbrowser

# Constants for authentication
SWITCH_TOKEN = "OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
ANDROID_TOKEN = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="


class EpicUser:
    def __init__(self, data: dict = {}):
        self.raw = data
        self.access_token = data.get("access_token", "")
        self.display_name = data.get("displayName", "")
        self.account_id = data.get("account_id", "")
        self.client_session = requests.Session()

    def get_email(self) -> str:
        response = self.client_session.get(
            f"https://account-public-service-prod03.ol.epicgames.com/account/api/public/account/displayName/{self.display_name}",
            headers={"Authorization": f"bearer {self.access_token}"}
        )
        return response.json().get("email")


class EpicGenerator:
    def __init__(self):
        self.http = requests.Session()
        self.access_token = ""

    async def start(self) -> None:
        print("Starting...")
        self.access_token = self.get_access_token()
        while True:
            device_code = self.create_device_code()
            webbrowser.open(device_code[0], new=1)

            user = await self.wait_for_device_code_completion(device_code[1])
            device_auths = self.create_device_auth_data(user)

            print(f"Generated {user.display_name}")
            self.save_device_auth(device_auths=device_auths, user=user)
            print(self.generate_eg1_token(user=user))
            choice = input("Generate another device auth? (Y/N): ")
            if choice.lower().strip() != "y":
                break

        self.http.close()
        sys.exit()

    def get_access_token(self) -> str:
        response = self.http.post(
            url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"basic {SWITCH_TOKEN}",
            },
            data={"grant_type": "client_credentials"}
        )
        return response.json().get("access_token")

    def create_device_code(self) -> tuple:
        response = self.http.post(
            url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/deviceAuthorization",
            headers={
                "Authorization": f"bearer {self.access_token}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
        data = response.json()
        return data["verification_uri_complete"], data["device_code"]

    async def wait_for_device_code_completion(self, code: str) -> EpicUser:
        while True:
            response = self.http.post(
                url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                headers={
                    "Authorization": f"basic {SWITCH_TOKEN}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={"grant_type": "device_code", "device_code": code}
            )
            if response.status_code == 200:
                return EpicUser(data=response.json())
            await asyncio.sleep(5)

    def create_device_auth_data(self, user: EpicUser) -> dict:
        response = self.http.post(
            url=f"https://account-public-service-prod.ol.epicgames.com/account/api/public/account/{user.account_id}/deviceAuth",
            headers={
                "Authorization": f"bearer {user.access_token}",
                "Content-Type": "application/json",
            }
        )
        data = response.json()
        print(data)
        print(user.access_token)
        return {
            "device_id": data["deviceId"],
            "account_id": data["accountId"],
            "secret": data["secret"],
            "created": data["created"]
        }
    
    def generate_eg1_token(self, user: EpicUser) -> str:
        if os.path.isfile("device_auths.json"):
            with open("device_auths.json", "r") as device_auth_file:
                current = json.load(device_auth_file)
            email_user = current.get(user.get_email(), {})
            
            # Ensure we have valid device auth data for the user
            if email_user:
                url = "https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token"
                headers = {
                    "Authorization": f"basic {SWITCH_TOKEN}",
                    "Content-Type": "application/x-www-form-urlencoded"
                }
                data = {
                    "grant_type": "device_auth",
                    "device_id": email_user["device_id"],
                    "account_id": email_user["account_id"],
                    "secret": email_user["secret"],
                    "token_type": "eg1"
                }
                
                # Send the request to generate the eg1 token
                response = requests.post(url=url, headers=headers, data=data)
                response_data = response.json()
                
                # Get the eg1 token if generation was successful
                eg1_token = response_data.get("access_token", "")
                if eg1_token:
                    print(f"EG1 token generated: {eg1_token}")
                    return eg1_token
                else:
                    print("Failed to generate EG1 token.")
                    return ""
            else:
                print("User device auth data not found in device_auths.json.")
                return ""

    def save_device_auth(self, device_auths: dict, user: EpicUser) -> None:
        if os.path.isfile("device_auths.json"):
            with open("device_auths.json", "r") as fp:
                current = json.load(fp)
        else:
            current = {}

        # Get the EG1 token and include it in the device auth data
        eg1_token = self.generate_eg1_token(user=user)
        device_auths["eg1_token"] = eg1_token

        current[user.get_email()] = device_auths
        
        with open("device_auths.json", "w") as fp:
            json.dump(current, fp, indent=4)

    

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())


gen = EpicGenerator()
gen.run()
