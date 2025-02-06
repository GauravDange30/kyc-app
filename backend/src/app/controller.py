import requests
import src.config as env_vars
from src.utils.logger.jsonlogger import logger
from requests_toolbelt.utils import dump

class VerifyController:
    def __init__(self, request_body: dict, headers: dict):
        self._request_body = request_body
        self._headers = headers

    def process_pan(self):
        try:

            required_headers = {
                'x-client-id': self._headers.get('x-client-id'),
                'x-client-secret': self._headers.get('x-client-secret'),
                'x-product-instance-id': self._headers.get('x-product-instance-id'),
                'Content-Type': "application/json"
            }
            logger.debug(f"URL {env_vars.PAN_VERIFY_URL}")
            logger.debug(f"BODY {self._request_body}")
            logger.debug(f"HEADERS {required_headers}")
            
            response = requests.post(
                url = env_vars.PAN_VERIFY_URL,
                json=self._request_body,
                headers=required_headers
            )
            logger.debug(f"Resposne {response.json()}")
            return response
        except requests.RequestException as e:
            response = requests.Response()
            response.status_code = 500
            response._content = {"error": "Internal Server Error", "details": str(e)}

            return response
        
    def process_bank(self):
        try:
            #Setting Default response_mock_payment

            response_mock_payment = requests.Response()
            response_mock_payment.status_code = 400  
            response_mock_payment._content = b'{"error": "Payment verification failed or payment ID missing"}'

            required_headers = {
                'x-client-id': self._headers.get('x-client-id'),
                'x-client-secret': self._headers.get('x-client-secret'),
                'x-product-instance-id': self._headers.get('x-product-instance-id'),
                'Content-Type': "application/json"
            }

            response = requests.post(
                url = env_vars.BANK_VERIFY_URL,
                json=self._request_body,
                headers=required_headers
            )
            logger.debug(f"URL {env_vars.BANK_VERIFY_URL}")
            logger.debug(f"BODY {self._request_body}")
            logger.debug(f"HEADERS {required_headers}")
            logger.debug(f"Resposne {response.json()}")
            if response.status_code in [200,201]:
                logger.debug(f"Reverse Penny Drop Resposne {response.json()}")
                response_json = response.json()
                status = response_json.get('status')
                payment_id = response_json.get('id')
                if payment_id and status=='BAV_REVERSE_PENNY_DROP_CREATED':
                    response_mock_payment = requests.post(
                            url = env_vars.BANK_VERIFY_MOCK_URL.format(payment_id),
                            json={"paymentStatus": "failed"},
                            headers=required_headers
                        )
                    return response_mock_payment
            else:
                response_mock_payment = requests.Response()
                response_mock_payment.status_code = 400
                response_mock_payment._content = b'{"error": "Reverse Penny Drop Creation Failed"}'

            return response_mock_payment
        except requests.RequestException as e:
            response_mock_payment = requests.Response()
            response_mock_payment.status_code = 500
            response_mock_payment._content = {"error": "Internal Server Error", "details": str(e)}

            return response_mock_payment