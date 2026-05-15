import json
import os

class KnowledgeGraphBridge:
    def __init__(self, crystal_path="elysia_eye/outputs/full_model_crystal.json"):
        with open(crystal_path, "r", encoding="utf-8") as f:
            self.crystal = json.load(f)

    def transmute_to_graph(self):
        """
        Converts the 27 Spherical Rotors into a Knowledge Graph format (Nodes & Edges).
        """
        print("[Graph Bridge] Transmuting Phase Rotors to Knowledge Graph...")

        nodes = []
        edges = []

        # Center Node (Love X)
        nodes.append({
            "id": "LoveX",
            "type": "Origin",
            "pos": [0, 0, 0],
            "description": "Equilibrium Point"
        })

        rotors = self.crystal['rotors']
        for r in rotors:
            # Rotor Node
            node_id = f"Rotor_{r['id']}"
            nodes.append({
                "id": node_id,
                "type": "PhaseRotor",
                "pos": r['pos'],
                "params": r['params']
            })

            # Edge to Origin
            edges.append({
                "source": node_id,
                "target": "LoveX",
                "relation": "resonance_axis",
                "strength": r['params']['amp']
            })

            # Edges to neighbors (simplified: connect to next rotor)
            next_id = f"Rotor_{(r['id'] + 1) % len(rotors)}"
            edges.append({
                "source": node_id,
                "target": next_id,
                "relation": "phase_interference",
                "strength": abs(r['params']['phi'] - rotors[(r['id'] + 1) % len(rotors)]['params']['phi'])
            })

        graph = {
            "metadata": self.crystal['metadata'],
            "nodes": nodes,
            "edges": edges
        }

        output_path = "elysia_eye/outputs/intelligence_graph.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=4)

        print(f"Graph transmutation complete: {output_path}")
        return graph

if __name__ == "__main__":
    bridge = KnowledgeGraphBridge()
    bridge.transmute_to_graph()
