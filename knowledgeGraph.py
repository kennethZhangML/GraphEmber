import networkx as nx
import matplotlib.pyplot as plt

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_entity(self, entity_name):
        self.graph.add_node(entity_name, type = 'entity')

    def add_relationship(self, subject, predicate, object):
        self.graph.add_edge(subject, object, relationship = predicate)

    def visualize_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels = True, node_color = 'lightblue',
            node_size = 1500, font_size=12)
        labels = nx.get_edge_attributes(self.graph, 'relationship')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels = labels, font_size = 10)
        plt.show()

class ScratchKnowledgeGraph:
    def __init__(self):
        self.graph = {}

    def add_entity(self, entity_name):
        if entity_name not in self.graph:
            self.graph[entity_name] = {'type': 'entity', 'neighbors': {}}

    def add_relationship(self, subject, predicate, object):
        self.add_entity(subject)
        self.add_entity(object)
        self.graph[subject]['neighbors'][object] = predicate
        self.graph[object]['neighbors'][subject] = predicate

    def num_neighbours(self, entity):
        return len(self.graph[entity])

    def visualize_graph(self):
        for node, data in self.graph.items():
            print(f"Entity: {node} (Type: {data['type']})")
            print("Number of neighbours: ", len(self.graph[node]))
            for neighbor, predicate in data['neighbors'].items():
                print(f"  -> {predicate} -> {neighbor}")

# Expanded example usage with more entities and relationships:
if __name__ == "__main__":
    entities = [
        "John", "CompanyXYZ", "New York City", "Sarah", "Los Angeles",
        "Manager", "Employee", "Los Angeles Department", "Chicago",
        "Engineer", "Finance Department", "San Francisco", "IT Department",
        "Washington D.C.", "Customer", "Client", "Supplier", "Vendor"
    ]

    relationships = [
        ("John", "works_at", "CompanyXYZ"),
        ("CompanyXYZ", "is_located_in", "New York City"),
        ("Sarah", "works_at", "CompanyXYZ"),
        ("CompanyXYZ", "employs", "Sarah"),
        ("CompanyXYZ", "has_position", "Manager"),
        ("John", "has_position", "Employee"),
        ("Los Angeles Department", "is_located_in", "Los Angeles"),
        ("Employee", "works_in", "Los Angeles Department"),
        ("Los Angeles", "is_located_in", "California"),
        ("Engineer", "works_at", "CompanyXYZ"),
        ("Finance Department", "is_part_of", "CompanyXYZ"),
        ("San Francisco", "is_located_in", "California"),
        ("IT Department", "is_part_of", "CompanyXYZ"),
        ("Washington D.C.", "is_located_in", "Washington D.C."),
        ("Customer", "has_relationship_with", "CompanyXYZ"),
        ("Client", "has_relationship_with", "CompanyXYZ"),
        ("Supplier", "has_relationship_with", "CompanyXYZ"),
        ("Vendor", "has_relationship_with", "CompanyXYZ"),
        ("CompanyXYZ", "supplies_to", "Supplier"),
        ("CompanyXYZ", "buys_from", "Vendor"),
    ]

    knowledge_graph = KnowledgeGraph()

    for entity in entities:
        knowledge_graph.add_entity(entity)

    for relationship in relationships:
        knowledge_graph.add_relationship(*relationship)

    knowledge_graph.visualize_graph()

    kg = ScratchKnowledgeGraph()

    for entity in entities:
        kg.add_entity(entity)

    for relation in relationships:
        kg.add_relationship(subject = relation[0], predicate = relation[1], object = relation[2])
    kg.visualize_graph()
