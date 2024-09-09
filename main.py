from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from algosdk.v2client import algod, indexer

app = FastAPI()

# Create Algod and Indexer clients
def create_algod_client():
    algod_address = "https://testnet-api.algonode.cloud"
    algod_token = ""  # No API key required for Algonode
    return algod.AlgodClient(algod_token, algod_address)

def create_indexer_client():
    indexer_address = "https://testnet-idx.algonode.cloud"
    indexer_token = ""  # No API key required for Algonode
    return indexer.IndexerClient(indexer_token, indexer_address)

algod_client = create_algod_client()
indexer_client = create_indexer_client()

# static files and templates
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/deploy_contract")
async def deploy_contract():
    try:
        app = Application(
            approval_program=contract_source,
            clear_program=contract_clear,
            on_completion=ApplicationState.get_complete()
        )
        tx_id = app.deploy(algod_client)
        return {"transaction_id": tx_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vote")
async def vote(vote: BaseModel):
    try:
        voter_address = vote.voter_address
        candidate_id = vote.candidate_id

        if not (0 <= candidate_id < 5):
            raise HTTPException(status_code=400, detail="Invalid candidate ID")

        account_info = algod_client.account_info(voter_address)
        if account_info.get('amount') == 0:
            raise HTTPException(status_code=400, detail="Voter has already voted")

        txn = {
            "type": "payment",
            "amount": 1000,
            "receiver": contract_address
        }
        signed_txn = txn.sign(voter_private_key)
        tx_id = algod_client.send_transaction(signed_txn)
        return {"transaction_id": tx_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/results", response_class=HTMLResponse)
async def get_results(request: Request):
    try:
        results = indexer_client.search_assets(limit=5)
        return templates.TemplateResponse("results.html", {"request": request, "results": results})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/account", response_class=HTMLResponse)
async def get_account_details(request: Request, address: str = None):
    try:
        account_info = {}
        if address:
            account_info = algod_client.account_info(address)
        return templates.TemplateResponse("account.html", {"request": request, "account_info": account_info})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class Vote(BaseModel):
    voter_address: str
    candidate_id: int



