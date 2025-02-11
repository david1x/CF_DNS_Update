from dotenv import load_dotenv
from db import DBPOSTGRESQL
from telegram import send_telegram_message
import requests
import logging
import time
import json
import os

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

load_dotenv()

API_TOKEN=os.getenv("API_TOKEN")
ZONE_ID=os.getenv("ZONE_ID")
DOMAIN=os.getenv("DOMAIN")
RECORDS=os.getenv("RECORDS")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")
BOT_TOKEN = os.getenv("BOT_TOKEN")
TLG_ID = os.getenv("TLG_ID")
 

# Cloudflare API token and zone_id
api_token = API_TOKEN
zone_id = ZONE_ID

cloud_api_url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"

db = DBPOSTGRESQL(
    dbname=DB_NAME,
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    port=DB_PORT
)


domain = DOMAIN
''' 
--- use split if there are multiple records ---
exp. in .env: 
    'RECORD=contact about'  
split output 'dns_records = ['contact', 'about']'
'''
dns_records = os.getenv("RECORDS").split(" ") 

print(f'DNS_RECORDS: {dns_records}')

def get_public_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    if response.status_code == 200:
        return response.json()["ip"]
    raise Exception(f"Request to get public ip has failed. status code {response.status_code}")


def get_record_id(record_name: str) -> list:
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    params = {
        "name": f"{record_name}.{domain}",
        "type": "A",
    }

    response = requests.get(cloud_api_url, headers=headers, params=params)

    if response.status_code == 200:
        result = response.json()["result"]
        # logging.info(result)
        if result:
            return result[0]["id"]
        else:
            raise Exception(f"No matching DNS record found for {record_name}.{domain}")
    else:
        raise Exception(f"Error fetching DNS records. Status code: {response.status_code}")


def update_dns_record(record_id, ip, record_name):
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    data = {
        "type": "A",
        "name": f"{record_name}.{domain}",
        "content": ip,
        "ttl": 1,
        "proxied": True, 
    }

    response = requests.put(f"{cloud_api_url}/{record_id}", headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        logging.info(f"DNS record [{record_name}] with ID {record_id} updated successfully.")
    else:
        logging.error(f"Error updating DNS record. Status code: {response.status_code}")
        exit(1)


def main():
    try:
        t1_start = time.perf_counter()
        public_ip = get_public_ip()
        previous_ip = db.get_previous_ip()
        
        logging.info(f"public_ip: {public_ip}")
        logging.info(f"previous_ip: {previous_ip}")
        
        if not (previous_ip == public_ip):
            logging.info("Public IP has changed - Updating Cloudflare\n")
            for record in dns_records:
                try:
                    record_id = get_record_id(record)
                    logging.info(f"Found record with the name: {record}")
                    update_dns_record(record_id, public_ip, record)
                except Exception as e:
                    logging.error(e)
                    logging.debug("Skipping to the next record")
                finally:
                    continue
            t1_stop = time.perf_counter()
            
            logging.info("\nUpdating Database with the Current Public IP")
            db.update_public_ip(public_ip=public_ip)
            # Telegram
            message = f'IP Changed to {public_ip} |  Cloudflare Updated Successfully'
            send_telegram_message(bot_token=BOT_TOKEN, chat_id=[TLG_ID], message=message)
            
            logging.info("Elapsed time during the whole program in seconds:",
                                                    t1_stop-t1_start)
        else:
            logging.info(f'Public ip ({public_ip}) has not changed, No update required.\n')
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        # Telegram
        message = f'Failed to Run Cloudflare Script. Error: {e}'
        send_telegram_message(bot_token=BOT_TOKEN, chat_id=[TLG_ID], message=message)
        exit(1)            
            


if __name__ == "__main__":
    main()
    
