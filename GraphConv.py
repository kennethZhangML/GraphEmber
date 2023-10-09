import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

from knowledgeGraph import *

class GCN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(GCN, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        
        self.gc1 = nn.Linear(input_dim, hidden_dim)
        self.gc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, adjacency_matrix, features):
        x = torch.mm(adjacency_matrix, features)  
        x = torch.relu(self.gc1(x))  
        x = self.gc2(x)  
        return x

def create_adjacency_matrix(knowledge_graph):
    entities = list(knowledge_graph.graph.keys())
    num_entities = len(entities)
    adjacency_matrix = np.zeros((num_entities, num_entities))

    for i, entity in enumerate(entities):
        for neighbor in knowledge_graph.graph[entity]['neighbors']:
            j = entities.index(neighbor)
            adjacency_matrix[i][j] = 1

    return torch.tensor(adjacency_matrix, dtype = torch.float32)

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

    num_entities = len(entities)
    input_features = torch.randn(num_entities, len(entities), dtype = torch.float32)

    input_dim = len(entities)
    hidden_dim = 64
    output_dim = 32
    gcn = GCN(input_dim, hidden_dim, output_dim)
    adjacency_matrix = create_adjacency_matrix(knowledge_graph) 
    output = gcn(adjacency_matrix, input_features)
