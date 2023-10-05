import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

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

if __name__ == "__main__":
    entities = ["John", "CompanyXYZ", "New York City", "Sarah", "Los Angeles"]
    relationships = [("John", "works_at", "CompanyXYZ"), ("CompanyXYZ", "is_located_in", "New York City")]

    myAdj = ERAdjacencyMatrix(entities, relationships)
    my_adj_matrix = myAdj.create_adj_matrix()
    print("Adjacency Matrix: ", my_adj_matrix)
