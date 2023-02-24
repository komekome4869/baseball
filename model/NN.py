from torch import nn
import torch.nn.functional as F

class NN(nn.Module):
    def __init__(self, num_input, n_nodes, n_layers=1, num_output=3):
        super(NN, self).__init__()
        self.input_layer = nn.Linear(num_input,n_nodes)
        layer = [nn.Linear(n_nodes,n_nodes) for _ in range(n_layers)]
        self.layer = nn.ModuleList(layer)
        self.output_layer = nn.Linear(n_nodes, num_output)
        self.num_input = num_input

    def forward(self, x):
        x = self.input_layer(x)
        x = F.relu(x)
        for i in range(len(self.layer)):
            x = self.layer[i](x)
            x = F.relu(x)
        out = self.output_layer(x)
        return out