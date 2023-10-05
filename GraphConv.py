import torch
import torch.nn as nn

import torch_geometric
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree

class GraphConvGraph(MessagePassing):
    def __init__(self, in_channels, out_channels):
        super().__init__(aggr = 'add')
        self.lin = nn.Linear(in_channels, out_channels, bias = False)
        self.bias = nn.Parameter(torch.empty(out_channels))

        self.reset_parameters()
