from typing import Dict, List, Optional
import copy
from datetime import datetime, timedelta

from app.core.models import (
    CustomerProfile, Account, Card, Transaction, Loan
)

class BankingDatabase:
    def __init__(self):
        self._initial_state = self._seed_data()
        self.customers: Dict[str, CustomerProfile] = copy.deepcopy(self._initial_state["customers"])
        self.transactions: Dict[str, List[Transaction]] = copy.deepcopy(self._initial_state["transactions"])
        self.disputes: List[Dict] = []
        self.notifications: List[Dict] = []
        self.transfer_log: List[Dict] = []

    def _seed_data(self) -> Dict:
        now = datetime.utcnow()
        t_now = now.strftime("%Y-%m-%d %H:%M:%S")
        t_1d = (now - timedelta(days=1)).strftime("%Y-%m-%d 14:22:10")
        t_2d = (now - timedelta(days=2)).strftime("%Y-%m-%d 09:15:00")
        t_3d = (now - timedelta(days=3)).strftime("%Y-%m-%d 19:40:22")
        t_5d = (now - timedelta(days=5)).strftime("%Y-%m-%d 11:05:44")

        # Persona 1: Elena Rostova (CUST-1001)
        elena = CustomerProfile(
            id="CUST-1001",
            name="Elena Rostova",
            email="elena.rostova@nexusbank.corp",
            phone="+1 (612) 555-0182",
            ssn_masked="***-**-8492",
            tier="WEALTH",
            kyc_status="VERIFIED",
            credit_score=785,
            annual_income=185000.0,
            accounts=[
                Account(
                    id="ACC-1001-CHK",
                    type="CHECKING",
                    account_number_masked="**** 6412",
                    routing_number="091000019",
                    balance=24850.40,
                    currency="USD",
                    status="ACTIVE"
                ),
                Account(
                    id="ACC-1001-SAV",
                    type="SAVINGS",
                    account_number_masked="**** 9981",
                    routing_number="091000019",
                    balance=85200.00,
                    currency="USD",
                    status="ACTIVE"
                )
            ],
            cards=[
                Card(
                    id="CARD-4912",
                    card_number_masked="4111-XXXX-XXXX-4912",
                    type="CREDIT",
                    network="VISA_INFINITE",
                    expiry="08/29",
                    status="ACTIVE",
                    spending_limit=30000.0,
                    current_cycle_spend=3420.50
                ),
                Card(
                    id="CARD-1129",
                    card_number_masked="4000-XXXX-XXXX-1129",
                    type="DEBIT",
                    network="VISA_PLATINUM",
                    expiry="11/28",
                    status="ACTIVE",
                    spending_limit=10000.0,
                    current_cycle_spend=1280.00
                )
            ],
            loans=[
                Loan(
                    id="LOAN-701",
                    type="AUTO",
                    original_principal=38000.0,
                    remaining_balance=12400.0,
                    interest_rate_apr=3.89,
                    term_months=48,
                    monthly_payment=610.20,
                    status="ACTIVE"
                )
            ]
        )

        elena_transactions = [
            Transaction(
                id="TXN-9081",
                account_id="ACC-1001-CHK",
                date=t_1d,
                description="Mayfair Watch Boutique - London UK",
                amount=1280.00,
                type="DEBIT",
                category="Luxury Goods",
                merchant="Mayfair Luxury Timepieces",
                location="London, United Kingdom",
                device="Unknown iPhone 14 / Safari (IP: 185.220.101.4)",
                status="FLAGGED",
                fraud_risk_score=92,
                risk_flags=["GEO_VELOCITY_ANOMALY", "UNRECOGNIZED_DEVICE", "FOREIGN_TRANSACTION_NO_TRAVEL_NOTICE"]
            ),
            Transaction(
                id="TXN-9080",
                account_id="ACC-1001-CHK",
                date=t_2d,
                description="Whole Foods Market",
                amount=142.15,
                type="DEBIT",
                category="Groceries",
                merchant="Whole Foods #1029",
                location="Minneapolis, MN, USA",
                device="Authorized iPhone 16 Pro (FaceID)",
                status="COMPLETED",
                fraud_risk_score=4,
                risk_flags=[]
            ),
            Transaction(
                id="TXN-9079",
                account_id="ACC-1001-CHK",
                date=t_3d,
                description="Target Store #002",
                amount=84.20,
                type="DEBIT",
                category="Retail",
                merchant="Target Corporation",
                location="Minneapolis, MN, USA",
                device="Apple Pay / NFC",
                status="COMPLETED",
                fraud_risk_score=2,
                risk_flags=[]
            ),
            Transaction(
                id="TXN-9078",
                account_id="ACC-1001-CHK",
                date=t_5d,
                description="Apex Global Tech - Payroll Direct Deposit",
                amount=7250.00,
                type="CREDIT",
                category="Income",
                merchant="Apex Global Tech Payroll",
                location="Minneapolis, MN, USA",
                device="ACH Automated Clearing",
                status="COMPLETED",
                fraud_risk_score=0,
                risk_flags=[]
            ),
            Transaction(
                id="TXN-9077",
                account_id="ACC-1001-CHK",
                date=t_5d,
                description="Xcel Energy Electric Utility",
                amount=115.40,
                type="DEBIT",
                category="Utilities",
                merchant="Xcel Energy",
                location="Minneapolis, MN, USA",
                device="Direct Debit Autopay",
                status="COMPLETED",
                fraud_risk_score=1,
                risk_flags=[]
            )
        ]

        # Persona 2: Marcus Vance (CUST-1002) - Business
        marcus = CustomerProfile(
            id="CUST-1002",
            name="Marcus Vance",
            email="m.vance@vancetech.io",
            phone="+1 (415) 555-0199",
            ssn_masked="***-**-3319",
            tier="BUSINESS",
            kyc_status="VERIFIED",
            credit_score=742,
            annual_income=260000.0,
            accounts=[
                Account(
                    id="ACC-1002-BUS",
                    type="BUSINESS",
                    account_number_masked="**** 7819",
                    routing_number="091000019",
                    balance=54200.00,
                    currency="USD",
                    status="ACTIVE"
                ),
                Account(
                    id="ACC-1002-PAY",
                    type="SAVINGS",
                    account_number_masked="**** 3320",
                    routing_number="091000019",
                    balance=32000.00,
                    currency="USD",
                    status="ACTIVE"
                )
            ],
            cards=[
                Card(
                    id="CARD-8841",
                    card_number_masked="5424-XXXX-XXXX-8841",
                    type="CREDIT",
                    network="MASTERCARD_COMMERCIAL",
                    expiry="03/28",
                    status="ACTIVE",
                    spending_limit=50000.0,
                    current_cycle_spend=12850.0
                )
            ],
            loans=[]
        )

        marcus_transactions = [
            Transaction(
                id="TXN-8012",
                account_id="ACC-1002-BUS",
                date=t_1d,
                description="AWS Cloud Services Infrastructure",
                amount=3420.00,
                type="DEBIT",
                category="Software & Infrastructure",
                merchant="Amazon Web Services",
                location="Seattle, WA, USA",
                device="Corporate Card on File",
                status="COMPLETED",
                fraud_risk_score=5,
                risk_flags=[]
            ),
            Transaction(
                id="TXN-8011",
                account_id="ACC-1002-BUS",
                date=t_2d,
                description="Client Retainer Deposit - Nordic Partners",
                amount=18500.00,
                type="CREDIT",
                category="B2B Revenue",
                merchant="Nordic Partners Ltd",
                location="San Francisco, CA, USA",
                device="Fedwire Transfer",
                status="COMPLETED",
                fraud_risk_score=2,
                risk_flags=[]
            )
        ]

        # Persona 3: Priya Sharma (CUST-1003) - Retail
        priya = CustomerProfile(
            id="CUST-1003",
            name="Priya Sharma",
            email="priya.sharma@nexusbank.corp",
            phone="+1 (312) 555-0144",
            ssn_masked="***-**-6102",
            tier="RETAIL",
            kyc_status="VERIFIED",
            credit_score=710,
            annual_income=92000.0,
            accounts=[
                Account(
                    id="ACC-1003-CHK",
                    type="CHECKING",
                    account_number_masked="**** 4103",
                    routing_number="091000019",
                    balance=3820.50,
                    currency="USD",
                    status="ACTIVE"
                ),
                Account(
                    id="ACC-1003-SAV",
                    type="SAVINGS",
                    account_number_masked="**** 9122",
                    routing_number="091000019",
                    balance=14200.00,
                    currency="USD",
                    status="ACTIVE"
                )
            ],
            cards=[
                Card(
                    id="CARD-3019",
                    card_number_masked="4200-XXXX-XXXX-3019",
                    type="CREDIT",
                    network="VISA_SIGNATURE",
                    expiry="06/27",
                    status="ACTIVE",
                    spending_limit=8000.0,
                    current_cycle_spend=940.0
                )
            ],
            loans=[]
        )

        priya_transactions = [
            Transaction(
                id="TXN-7010",
                account_id="ACC-1003-CHK",
                date=t_1d,
                description="Trader Joe's Grocery",
                amount=96.40,
                type="DEBIT",
                category="Groceries",
                merchant="Trader Joe's",
                location="Chicago, IL, USA",
                device="Apple Pay",
                status="COMPLETED",
                fraud_risk_score=2,
                risk_flags=[]
            )
        ]

        return {
            "customers": {
                "CUST-1001": elena,
                "CUST-1002": marcus,
                "CUST-1003": priya
            },
            "transactions": {
                "ACC-1001-CHK": elena_transactions,
                "ACC-1002-BUS": marcus_transactions,
                "ACC-1003-CHK": priya_transactions
            }
        }

    def reset(self):
        fresh = self._seed_data()
        self.customers = fresh["customers"]
        self.transactions = fresh["transactions"]
        self.disputes.clear()
        self.notifications.clear()
        self.transfer_log.clear()

    def get_customer(self, customer_id: str) -> Optional[CustomerProfile]:
        return self.customers.get(customer_id)

    def get_accounts_for_customer(self, customer_id: str) -> List[Account]:
        cust = self.get_customer(customer_id)
        return cust.accounts if cust else []

    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        for cust in self.customers.values():
            for acc in cust.accounts:
                if acc.id == account_id:
                    return acc
        return None

    def get_card_by_id(self, card_id: str) -> Optional[Card]:
        for cust in self.customers.values():
            for card in cust.cards:
                if card.id == card_id:
                    return card
        return None

    def get_transactions_for_account(self, account_id: str, limit: int = 10) -> List[Transaction]:
        txns = self.transactions.get(account_id, [])
        return txns[:limit]

    def set_card_status(self, card_id: str, new_status: str, reason: str = "") -> Optional[Card]:
        card = self.get_card_by_id(card_id)
        if card:
            card.status = new_status
            return card
        return None

    def dispute_transaction(self, transaction_id: str, customer_id: str, reason: str) -> Dict:
        for acc_id, txn_list in self.transactions.items():
            for txn in txn_list:
                if txn.id == transaction_id:
                    txn.status = "DISPUTED"
                    dispute_record = {
                        "dispute_id": f"DSP-{datetime.utcnow().strftime('%y%m%d')}-{transaction_id}",
                        "transaction_id": transaction_id,
                        "customer_id": customer_id,
                        "amount": txn.amount,
                        "merchant": txn.merchant,
                        "reason": reason,
                        "status": "PROVISIONAL_CREDIT_ISSUED",
                        "created_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    self.disputes.append(dispute_record)
                    return dispute_record
        return {"error": f"Transaction {transaction_id} not found"}

    def add_loan(self, customer_id: str, loan_type: str, amount: float, apr: float, term_months: int) -> Loan:
        cust = self.get_customer(customer_id)
        if not cust:
            raise ValueError(f"Customer {customer_id} not found")
        # monthly payment calculation: M = P * [ i(1 + i)^n ] / [ (1 + i)^n – 1]
        monthly_rate = (apr / 100.0) / 12.0
        if monthly_rate > 0:
            factor = (1.0 + monthly_rate) ** term_months
            monthly_payment = round(amount * (monthly_rate * factor) / (factor - 1.0), 2)
        else:
            monthly_payment = round(amount / term_months, 2)

        loan = Loan(
            id=f"LOAN-{len(cust.loans) + 801}",
            type=loan_type.upper(),
            original_principal=amount,
            remaining_balance=amount,
            interest_rate_apr=apr,
            term_months=term_months,
            monthly_payment=monthly_payment,
            status="APPROVED_DISBURSED"
        )
        cust.loans.append(loan)
        return loan

    def execute_transfer(self, from_account_id: str, to_account_id: str, recipient_name: str, amount: float, memo: str) -> Dict:
        from_acc = self.get_account_by_id(from_account_id)
        if not from_acc:
            return {"success": False, "error": f"Source account {from_account_id} not found"}
        if from_acc.balance < amount:
            return {"success": False, "error": f"Insufficient funds: Balance is ${from_acc.balance:,.2f}, required ${amount:,.2f}"}

        from_acc.balance = round(from_acc.balance - amount, 2)
        
        # Credit recipient if internal, otherwise simulated external clearing
        to_acc = self.get_account_by_id(to_account_id)
        if to_acc:
            to_acc.balance = round(to_acc.balance + amount, 2)

        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        txn_record = Transaction(
            id=f"TXN-OUT-{datetime.utcnow().strftime('%H%M%S')}",
            account_id=from_account_id,
            date=now_str,
            description=f"Transfer to {recipient_name} - {memo}",
            amount=amount,
            type="DEBIT",
            category="Wire Transfer",
            merchant=recipient_name,
            location="Online Banking Core",
            device="Authenticated Web Banking Session",
            status="COMPLETED",
            fraud_risk_score=15,
            risk_flags=["HIGH_VALUE_TRANSFER"] if amount >= 10000 else []
        )
        if from_account_id not in self.transactions:
            self.transactions[from_account_id] = []
        self.transactions[from_account_id].insert(0, txn_record)

        log_entry = {
            "transfer_id": f"WIR-{datetime.utcnow().strftime('%y%m%d%H%M%S')}",
            "from_account": from_account_id,
            "to_account": to_account_id,
            "recipient_name": recipient_name,
            "amount": amount,
            "memo": memo,
            "timestamp": now_str,
            "status": "SETTLED"
        }
        self.transfer_log.append(log_entry)
        return {"success": True, "transaction": txn_record.dict(), "wire_log": log_entry}

    def record_notification(self, customer_id: str, channel: str, subject: str, message: str, priority: str = "NORMAL"):
        entry = {
            "id": f"NTF-{len(self.notifications) + 1:04d}",
            "customer_id": customer_id,
            "channel": channel,
            "subject": subject,
            "message": message,
            "priority": priority,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "delivery_status": "DELIVERED"
        }
        self.notifications.append(entry)
        return entry

# Global singleton
db = BankingDatabase()
