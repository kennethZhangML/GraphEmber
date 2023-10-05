import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

from relationshipExtraction import *

def add_self_loops(adjacency_matrix):
    identity_matrix = np.identity(adjacency_matrix.shape[0])
    return adjacency_matrix + identity_matrix

def linear_transform(node_features, weight_matrix):
    return np.dot(node_features, weight_matrix)

def compute_normalization_coefficients(adjacency_matrix):
    degrees = np.sum(adjacency_matrix, axis = 1)
    sqrt_degrees = np.sqrt(degrees)
    return 1.0 / (sqrt_degrees[:, np.newaxis] * sqrt_degrees[np.newaxis, :])

def normalize_node_features(node_features, normalization_coefficients):
    return node_features * normalization_coefficients

def aggregate_neighboring_features(normalized_features, adjacency_matrix):
    return np.dot(adjacency_matrix, normalized_features)

def apply_bias(aggregated_features, bias_vector):
    return aggregated_features + bias_vector

class ERAdjacencyMatrix:
    def __init__ (self, entities, relationships):
        self.entities = entities
        self.relationships = relationships

        if (len(self.entities) != len(self.relationships)):
            print("Entity entries not of equal size to relationships!")

        self.entity_ids = {entity: idx for idx, entity in enumerate(entities)}
        self.num_entities = len(entities)
        self.adjacency_matrix = [[0] * self.num_entities for _ in range(self.num_entities)]

    def create_adj_matrix(self):
        for rel in self.relationships:
            entity1, _, entity2 = rel
            idx1, idx2 = self.entity_ids[entity1], self.entity_ids[entity2]
            self.adjacency_matrix[idx1][idx2] = 1
            self.adjacency_matrix[idx2][idx1] = 1

        adjacency_matrix = np.array(self.adjacency_matrix)
        return adjacency_matrix

class GCNLayer:
    def __init__(self, adjacency_matrix, input_dim, output_dim):
        self.adjacency_matrix = add_self_loops(adjacency_matrix)
        self.weight_matrix = np.random.randn(input_dim, output_dim)
        self.bias_vector = np.random.randn(output_dim)

    def forward(self, node_features):
        transformed_features = linear_transform(node_features, self.weight_matrix)
        normalization_coefficients = compute_normalization_coefficients(self.adjacency_matrix)
        normalized_features = normalize_node_features(transformed_features, normalization_coefficients)
        aggregated_features = aggregate_neighboring_features(normalized_features, self.adjacency_matrix)
        output = apply_bias(aggregated_features, self.bias_vector)
        return output

if __name__ == "__main__":
    entities = ["John", "CompanyXYZ", "New York City", "Sarah", "Los Angeles"]
    relationships = [("John", "works_at", "CompanyXYZ"), ("CompanyXYZ", "is_located_in", "New York City")]

    myAdj = ERAdjacencyMatrix(entities, relationships)
    my_adj_matrix = myAdj.create_adj_matrix()
    print("Adjacency Matrix:\n", my_adj_matrix)
