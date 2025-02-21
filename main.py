import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from tools.other_utils import read_file
from tools.session import get_proxied_session
from user_data.config import mobile_proxy

url = "https://beta.orchestrator.nexus.xyz/nodes"


def process_payloads_concurrently(payloads: list[str], interval: int = 1):
    pending_payloads = set(payloads)

    while pending_payloads:
        try:
            with get_proxied_session(proxy=mobile_proxy) as session:
                with ThreadPoolExecutor(max_workers=len(pending_payloads)) as executor:
                    future_to_payload = {
                        executor.submit(session.post, url, data=payload): payload
                        for payload in pending_payloads
                    }
                    for future in as_completed(future_to_payload):
                        payload = future_to_payload[future]
                        try:
                            response = future.result()
                            print(f"{payload}: {response.text}.")
                            pending_payloads.remove(payload)
                        except requests.exceptions.Timeout:
                            print(f"{payload}: timeout.")
                        except Exception as e:
                            print(f"{payload}: {e}.")
        except Exception as e:
            print(e)

        if pending_payloads:
            time.sleep(interval)


if __name__ == '__main__':
    payloads = read_file('user_data/payload.txt')
    process_payloads_concurrently(payloads)
