from client import AgentHumanInTheLoopApprovalGate
import json

def test():
    gate = AgentHumanInTheLoopApprovalGate()
    print("=== Testing Agent Human-in-the-Loop Approval Gate ===")
    res = gate.run_benchmark_approval_gate()
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    test()
