"""Finance Agent - Handles financial operations."""

from typing import Any, Dict, Optional

from ..core.slave_agent import SlaveAgent


class FinanceAgent(SlaveAgent):
    """
    Finance Agent - Specialized agent for financial operations.
    
    Capabilities:
    - Invoice processing
    - Expense approvals
    - Budget management
    - Payment processing
    - Financial reporting
    """
    
    def __init__(self, agent_id: Optional[str] = None):
        super().__init__(
            agent_id=agent_id,
            agent_type="finance",
            department="finance",
            capabilities=[
                "invoice_processing",
                "expense_approval",
                "budget_management",
                "payment_processing",
                "financial_reporting",
                "audit_support"
            ]
        )
    
    async def _process_department_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process finance-specific requests."""
        request_type = request.get("request_type")
        
        if request_type == "expense_query":
            return await self._handle_expense_query(request)
        
        elif request_type == "budget_query":
            return await self._handle_budget_query(request)
        
        elif request_type == "payment_status":
            return await self._handle_payment_status(request)
        
        else:
            return await super()._process_department_request(request)
    
    async def _execute_department_task(
        self,
        task_type: str,
        task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute finance-specific tasks."""
        
        if task_type == "process_invoice":
            return await self._process_invoice(task_data)
        
        elif task_type == "approve_expense":
            return await self._approve_expense(task_data)
        
        elif task_type == "process_payment":
            return await self._process_payment(task_data)
        
        elif task_type == "generate_report":
            return await self._generate_report(task_data)
        
        else:
            return await super()._execute_department_task(task_type, task_data)
    
    async def _handle_expense_query(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle expense queries."""
        expense_id = request.get("expense_id")
        
        return {
            "status": "success",
            "expense_id": expense_id,
            "result": f"Expense information retrieved for {expense_id}"
        }
    
    async def _handle_budget_query(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle budget queries."""
        department = request.get("department")
        period = request.get("period")
        
        return {
            "status": "success",
            "department": department,
            "period": period,
            "budget_info": f"Budget information for {department} - {period}"
        }
    
    async def _handle_payment_status(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle payment status queries."""
        payment_id = request.get("payment_id")
        
        return {
            "status": "success",
            "payment_id": payment_id,
            "payment_status": "processed",
            "message": "Payment completed successfully"
        }
    
    async def _process_invoice(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process an invoice."""
        invoice_id = task_data.get("invoice_id")
        amount = task_data.get("amount")
        vendor = task_data.get("vendor")
        
        return {
            "status": "completed",
            "invoice_id": invoice_id,
            "amount": amount,
            "vendor": vendor,
            "message": f"Invoice {invoice_id} processed for {vendor}"
        }
    
    async def _approve_expense(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Approve an expense."""
        expense_id = task_data.get("expense_id")
        amount = task_data.get("amount")
        category = task_data.get("category")
        
        return {
            "status": "completed",
            "expense_id": expense_id,
            "amount": amount,
            "category": category,
            "approved": True,
            "message": f"Expense {expense_id} approved"
        }
    
    async def _process_payment(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a payment."""
        payment_id = task_data.get("payment_id")
        amount = task_data.get("amount")
        recipient = task_data.get("recipient")
        
        return {
            "status": "completed",
            "payment_id": payment_id,
            "amount": amount,
            "recipient": recipient,
            "message": f"Payment of {amount} to {recipient} processed"
        }
    
    async def _generate_report(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a financial report."""
        report_type = task_data.get("report_type")
        period = task_data.get("period")
        
        return {
            "status": "completed",
            "report_type": report_type,
            "period": period,
            "message": f"{report_type} report generated for {period}"
        }
