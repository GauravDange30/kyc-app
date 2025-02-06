from fastapi.routing import APIRouter
import src.app.models as models
from fastapi import Request, Header
from src.app.controller import VerifyController
from fastapi.responses import JSONResponse
from src.utils.logger.jsonlogger import logger
from src.app.models import VerifyPanRequestBody, VerifyBankRequestBody
import random
from fastapi import Request
from fastapi.responses import JSONResponse
from src.services.db_connector import kyc_collection
from datetime import datetime, timezone

webhook_router = APIRouter()

@webhook_router.post("/api/verify/pan")
async def verify_pan(request: Request):
    try:
        headers = dict(request.headers)
        request_body = await request.json()

        try:
            request_body_check = VerifyPanRequestBody.model_validate(request_body)
        except Exception as e:
            logger.error(f"Data Validation Error: {e}")
            kyc_collection.insert_one({
                "kyc_type": "pan",
                "status": "failed_pan",
                "timestamp": datetime.now(timezone.utc)
            })
            logger.debug({"kyc_type": "pan","status": "failed_pan","timestamp": datetime.now(timezone.utc)})
            return JSONResponse(status_code=400, content={"error": "Invalid request body"})

        verify_pan_controller = VerifyController(request_body=request_body, headers=headers)
        api_response_to_send = verify_pan_controller.process_pan()

        status = "failed_pan"
        if api_response_to_send.status_code == 200:
            api_response_to_send_ = api_response_to_send.json()
            if api_response_to_send_['verification']=="SUCCESS":
                status = "successful"

        inserted = kyc_collection.insert_one({
            "kyc_type": "pan",
            "status": status,
            "timestamp": datetime.utcnow()
        })

        logger.debug(f"Inserted Record ID: {inserted.inserted_id}")
        return JSONResponse(status_code=api_response_to_send.status_code, content=api_response_to_send.json())


    except Exception as e:
        logger.error(f"Some Error: {e}")
        kyc_collection.insert_one({
            "kyc_type": "pan",
            "status": "failed_pan",
            "timestamp": datetime.now(timezone.utc)
        })
        logger.debug({"kyc_type": "pan","status": "failed_pan","timestamp": datetime.now(timezone.utc)})
        
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    
@webhook_router.post("/api/verify/ban/reverse")
async def verify_bank(request: Request):
    try:
        headers = dict(request.headers)
        request_body = await request.json()

        pan_status = "successful"
        additional_data = request_body.get("additionalData")
        if additional_data:
            pan_status = additional_data.get("pan_status")

        bank_status_f = "failed_bank"
        if pan_status=='failed_pan':
            bank_status_f = "failed_both"
        try:
            request_body_check = VerifyBankRequestBody.model_validate(request_body)
        except Exception as e:
            logger.error(f"Data Validation Error: {e}")
            kyc_collection.insert_one({
                "kyc_type": "bank",
                "status": bank_status_f,
                "timestamp": datetime.now(timezone.utc)
            })
            logger.debug({"kyc_type": "bank","status": "failed_bank","timestamp": datetime.now(timezone.utc)})
            return JSONResponse(status_code=400, content={"error": "Invalid request body"})

        verify_bank_controller = VerifyController(request_body=request_body, headers=headers)
        api_response_to_send = verify_bank_controller.process_bank()

        status = "successful" if api_response_to_send.status_code == 200 else "failed_bank"

        if status== "failed_bank" and pan_status=='failed_pan':
            status = 'failed_both'
        kyc_collection.insert_one({
            "kyc_type": "bank",
            "status": status,
            "timestamp": datetime.now(timezone.utc)
        })
        logger.debug({"kyc_type": "bank","status": status,"timestamp": datetime.now(timezone.utc)})
        return JSONResponse(status_code=api_response_to_send.status_code, content=api_response_to_send.json())

    except Exception as e:
        logger.error(f"Internal server error: {e}")
        kyc_collection.insert_one({
            "kyc_type": "bank",
            "status": bank_status_f,
            "timestamp": datetime.now(timezone.utc)
        })
        logger.debug({"kyc_type": "bank","status": "failed_bank","timestamp": datetime.now(timezone.utc)})
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

    

@webhook_router.get("/api/analytics")
async def get_analytics():
    total_attempts = kyc_collection.count_documents({})
    total_success = kyc_collection.count_documents({"status": "successful"})
    total_failed = kyc_collection.count_documents({"status": {"$ne": "successful"}})
    failed_due_pan = kyc_collection.count_documents({"status": "failed_pan"})
    failed_due_bank = kyc_collection.count_documents({"status": "failed_bank"})
    failed_due_both = kyc_collection.count_documents({"status": "failed_both"})

    return {
        "labels": [
            "Total KYC Attempted",
            "Total KYC Successful",
            "Total KYC Failed",
            "Total KYC Failed due PAN",
            "Total KYC Failed due Bank",
            "Total KYC Failed due PAN & Bank"
        ],
        "values": [
            total_attempts,
            total_success,
            total_failed,
            failed_due_pan,
            failed_due_bank,
            failed_due_both
        ]
    }

