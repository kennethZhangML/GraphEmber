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

# Example usage:
if __name__ == "__main__":
    entities = ["John", "CompanyXYZ", "New York City", "Sarah", "Los Angeles"]
    relationships = [("John", "works_at", "CompanyXYZ"), ("CompanyXYZ", "is_located_in", "New York City")]

    knowledge_graph = KnowledgeGraph()

    for entity in entities:
        knowledge_graph.add_entity(entity)

    for relationship in relationships:
        knowledge_graph.add_relationship(*relationship)

    knowledge_graph.visualize_graph()
