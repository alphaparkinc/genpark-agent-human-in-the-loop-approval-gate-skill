import sys, json
from client import AgentHumanInTheLoopApprovalGate

def handle_mcp():
    gate = AgentHumanInTheLoopApprovalGate()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(gate.run_benchmark_approval_gate(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-agent-human-in-the-loop-approval-gate-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "evaluate_action_risk_tier", "description": "Classify action risk and determine approval requirements.", "inputSchema": {"type": "object", "properties": {"action_command": {"type": "string"}, "estimated_impact_usd": {"type": "number"}}}},
                    {"name": "create_reversible_checkpoint", "description": "Create rollback snapshot before mutating actions.", "inputSchema": {"type": "object", "properties": {"state_snapshot": {"type": "object"}}}},
                    {"name": "issue_approval_token", "description": "Generate cryptographically verifiable one-time execution token.", "inputSchema": {"type": "object", "properties": {"action_id": {"type": "string"}}}},
                    {"name": "run_benchmark_approval_gate", "description": "Run human-in-the-loop safety gate benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "evaluate_action_risk_tier":
                    res = gate.evaluate_action_risk_tier(args.get("action_command", ""), args.get("estimated_impact_usd", 0.0))
                elif tname == "create_reversible_checkpoint":
                    res = gate.create_reversible_checkpoint(args.get("state_snapshot", {}))
                elif tname == "issue_approval_token":
                    res = gate.issue_approval_token(args.get("action_id", ""), args.get("user_approved", True))
                else:
                    res = gate.run_benchmark_approval_gate()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
