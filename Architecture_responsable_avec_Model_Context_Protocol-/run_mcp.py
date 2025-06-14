import json
import logging
import sqlite3
import datetime
import os

# Configure logging
logging.basicConfig(
    filename='mcp_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ModelContextProtocol:
    def __init__(self, permissions_file='mcp_permissions.json'):
        # Load permissions
        with open(permissions_file, 'r') as f:
            self.permissions = json.load(f)
        
        # Initialize database
        self.init_db()
        
        logging.info("MCP server initialized")
    
    def init_db(self):
        """Initialize the audit database"""
        conn = sqlite3.connect('mcp_audit.db')
        cursor = conn.cursor()
        
        # Create audit table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            request_type TEXT,
            data_accessed TEXT,
            decision TEXT,
            explanation TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_interaction(self, request_type, data_accessed, decision, explanation):
        """Log an interaction to both file and database"""
        timestamp = datetime.datetime.now().isoformat()
        
        # Log to file
        logging.info(f"Request: {request_type}, Data: {data_accessed}, Decision: {decision}, Explanation: {explanation}")
        
        # Log to database
        if self.permissions['audit']['store_decisions']:
            conn = sqlite3.connect('mcp_audit.db')
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO audit_log (timestamp, request_type, data_accessed, decision, explanation) VALUES (?, ?, ?, ?, ?)",
                (timestamp, request_type, data_accessed, decision, explanation)
            )
            
            conn.commit()
            conn.close()
    
    def check_permission(self, data_type, capability):
        """Check if the requested data access and capability are permitted"""
        data_permitted = self.permissions['data_access'].get(data_type, False)
        capability_permitted = self.permissions['capabilities'].get(capability, False)
        
        return data_permitted and capability_permitted
    
    def process_request(self, request_type, data_type, capability, context=None):
        """Process an incoming request"""
        # Check permissions
        if not self.check_permission(data_type, capability):
            decision = "denied"
            explanation = f"Permission denied for {data_type} with {capability}"
            self.log_interaction(request_type, data_type, decision, explanation)
            return {"status": "error", "message": explanation}
        
        # Process the request (simplified for example)
        decision = "approved"
        explanation = f"Request for {capability} on {data_type} was processed successfully"
        
        # Log the interaction
        self.log_interaction(request_type, data_type, decision, explanation)
        
        return {
            "status": "success",
            "message": explanation,
            "context": context
        }

if __name__ == "__main__":
    # Create MCP server
    mcp = ModelContextProtocol()
    
    # Example usage
    print("MCP Server running. Press Ctrl+C to exit.")
    
    try:
        # Simple demo
        result = mcp.process_request(
            "product_analysis",
            "product_data",
            "recommendation",
            {"products": ["Product A", "Product B", "Product C"]}
        )
        print(f"Demo request result: {result}")
        
        # Keep the server running
        while True:
            pass
    except KeyboardInterrupt:
        print("MCP Server stopped.")