### models/risk_engine.py

```python
import pandas as pd

class RiskEngine:
    def __init__(self, notam_file='data/sample_NOTAMs.csv'):
        self.notam_df = pd.read_csv(notam_file)

    def get_airport_risk(self, iata_code, date):
        """Return risk score (0-1) for a given airport on a given date"""
        df = self.notam_df[(self.notam_df['Airport_IATA']==iata_code) &
                           (self.notam_df['Start_Date'] <= date) &
                           (self.notam_df['End_Date'] >= date)]
        if df.empty:
            return 0.0
        return df['Risk_Level'].max()

    def get_all_risks(self, date):
        """Return a dict of airport codes to risk scores"""
        risks = {}
        for iata in self.notam_df['Airport_IATA'].unique():
            risks[iata] = self.get_airport_risk(iata, date)
        return risks
```

---

### models/optimizer.py

```python
import networkx as nx
from risk_engine import RiskEngine

class RouteOptimizer:
    def __init__(self, airports_file='data/airports.csv'):
        self.airports_file = airports_file
        self.G = nx.DiGraph()

    def build_graph(self):
        import pandas as pd
        df = pd.read_csv(self.airports_file)
        for i, row in df.iterrows():
            self.G.add_node(row['IATA'], lat=row['Latitude'], lon=row['Longitude'])

        # Fully connected example (for demo)
        for src in self.G.nodes:
            for dest in self.G.nodes:
                if src != dest:
                    self.G.add_edge(src, dest, travel_time=1.0, risk=0.0)

    def assign_risk(self, risk_dict):
        for u, v in self.G.edges:
            self.G[u][v]['risk'] = risk_dict.get(v, 0.0)

    def compute_optimal_route(self, origin, destination, lambda_risk=1.0):
        # Edge weight = travel_time + lambda*risk
        def weight(u, v, d):
            return d['travel_time'] + lambda_risk * d['risk']
        path = nx.shortest_path(self.G, origin, destination, weight=weight)
        return path
```

---

### scripts/update_graph.py

```python
from models.optimizer import RouteOptimizer
from models.risk_engine import RiskEngine

if __name__ == '__main__':
    optimizer = RouteOptimizer()
    optimizer.build_graph()
    risk_engine = RiskEngine()
    risks = risk_engine.get_all_risks('2026-03-02')
    optimizer.assign_risk(risks)
    path = optimizer.compute_optimal_route('LAX', 'BOM', lambda_risk=1.5)
    print('Optimal route:', path)
```

---

### scripts/reroute_alert.py

```python
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
```
