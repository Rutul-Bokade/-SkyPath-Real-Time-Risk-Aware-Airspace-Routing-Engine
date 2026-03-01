from models.optimizer import RouteOptimizer
from models.risk_engine import RiskEngine

if __name__ == '__main__':
    # Simulate rerouting alert
    optimizer = RouteOptimizer()
    optimizer.build_graph()
    risk_engine = RiskEngine()
    risks = risk_engine.get_all_risks('2026-03-02')
    optimizer.assign_risk(risks)
    new_path = optimizer.compute_optimal_route('LAX', 'BOM', lambda_risk=2.0)
    print('Rerouting alert! New recommended route:', new_path)
