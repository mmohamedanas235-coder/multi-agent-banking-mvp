import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Dict, Any

from app.config import config
from app.core.models import (
    ChatRequest, ChatResponse, HumanApprovalActionRequest
)
from app.agents.supervisor import supervisor
from app.data.banking_db import db
from app.tools.banking_tools import tools
from app.core.gateway import ai_gateway
from app.llm.provider import llm_manager
from app.core.rag import rag_retriever

app = FastAPI(
    title="NEXUS Core Banking Multi-Agent System",
    description="Autonomous Multi-Agent Banking Simulation Platform",
    version=config.VERSION
)

# Enable CORS for local dev flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to static frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def get_root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "NEXUS Multi-Agent Banking API active. UI index.html not yet initialized."}

@app.post("/api/chat", response_model=ChatResponse)
def handle_chat(req: ChatRequest):
    try:
        trace = supervisor.process_request(
            user_message=req.message,
            customer_id=req.customer_id,
            session_id=req.session_id,
            llm_provider=req.llm_provider,
            api_key=req.api_key
        )
        # Snapshot of customer after mutations
        cust = db.get_customer(req.customer_id)
        cust_snapshot = cust.dict() if cust else None

        return ChatResponse(
            success=True,
            trace=trace,
            customer_snapshot=cust_snapshot
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/action/approve")
def handle_approval(action_req: HumanApprovalActionRequest):
    """
    Handles Human-in-the-Loop authorization gate execution.
    """
    if action_req.action == "REJECT":
        return {
            "success": True,
            "status": "REJECTED_BY_USER",
            "message": f"Action '{action_req.action_type}' was declined by the account holder. No funds debited."
        }

    # If action is approved
    if action_req.action_type == "INTERNATIONAL_WIRE_TRANSFER":
        params = action_req.parameters
        from_acc = params.get("from_account", "ACC-1001-CHK")
        to_acc = params.get("to_account", "DE89-3704-0044-0532-0130-00")
        recipient = params.get("recipient_name", "John Doe")
        amount = float(params.get("amount", 15000.0))
        memo = params.get("memo", "Invoice Settlement #9921")

        transfer_res = db.execute_transfer(from_acc, to_acc, recipient, amount, memo)
        if not transfer_res.get("success", False):
            return {"success": False, "error": transfer_res.get("error")}

        # Send notification
        db.record_notification(
            action_req.customer_id,
            "SMS & PUSH",
            "International Wire Dispatched",
            f"Wire of ${amount:,.2f} USD to {recipient} has been settled and released to SWIFT network."
        )

        return {
            "success": True,
            "status": "APPROVED_AND_EXECUTED",
            "transfer_details": transfer_res,
            "message": f"Wire transfer of ${amount:,.2f} USD successfully released after cryptographic customer authorization."
        }

    return {"success": True, "status": "APPROVED", "message": f"Action {action_req.action_type} executed."}

@app.get("/api/customer/{customer_id}")
def get_customer(customer_id: str):
    cust = db.get_customer(customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Gather transactions for all customer accounts
    txns_map = {}
    for acc in cust.accounts:
        txns_map[acc.id] = [t.dict() for t in db.get_transactions_for_account(acc.id, limit=10)]

    return {
        "customer": cust.dict(),
        "transactions": txns_map,
        "disputes": [d for d in db.disputes if d["customer_id"] == customer_id],
        "notifications": [n for n in db.notifications if n["customer_id"] == customer_id]
    }

@app.get("/api/system/status")
def get_system_status():
    return {
        "bank_name": config.BANK_NAME,
        "version": config.VERSION,
        "active_provider": llm_manager.active_provider,
        "tools_registered_count": len(tools._tools),
        "total_tokens_evaluated": ai_gateway.total_tokens_processed,
        "total_pii_redacted": ai_gateway.total_pii_entities_redacted,
        "blocked_requests_count": ai_gateway.blocked_requests_count,
        "audit_logs_count": len(tools.audit_log),
        "recent_audit_logs": tools.audit_log[-10:]
    }

@app.post("/api/system/reset")
def reset_system():
    db.reset()
    ai_gateway.total_tokens_processed = 0
    ai_gateway.total_pii_entities_redacted = 0
    ai_gateway.blocked_requests_count = 0
    tools.audit_log.clear()
    return {"success": True, "message": "Core Banking database and AI Gateway metrics reset to initial state."}

@app.get("/api/knowledge/search")
def search_knowledge(q: str):
    return {"query": q, "results": rag_retriever.search(q, top_k=3)}

@app.post("/api/config/llm")
def set_llm_config(payload: Dict[str, Any]):
    provider = payload.get("provider", "cognitive")
    api_key = payload.get("api_key", "")
    llm_manager.set_provider(provider, api_key)
    return {"success": True, "provider": llm_manager.active_provider}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=config.HOST, port=config.PORT, reload=True)
