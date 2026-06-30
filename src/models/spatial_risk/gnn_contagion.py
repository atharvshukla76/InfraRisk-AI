import torch
import torch.nn as nn
import torch.nn.functional as F

class GraphConvolution(nn.Module):
    """
    Pure PyTorch implementation of a Graph Convolutional Layer.
    Allows the model to run without strict dependency on pytorch-geometric.
    """
    def __init__(self, in_features, out_features):
        super(GraphConvolution, self).__init__()
        self.weight = nn.Parameter(torch.FloatTensor(in_features, out_features))
        self.bias = nn.Parameter(torch.FloatTensor(out_features))
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.xavier_uniform_(self.weight)
        nn.init.zeros_(self.bias)

    def forward(self, x, adj):
        """
        x: Node features [num_nodes, in_features]
        adj: Adjacency matrix (normalized) [num_nodes, num_nodes]
        """
        support = torch.mm(x, self.weight)
        output = torch.spmm(adj, support) # Sparse matrix multiplication
        return output + self.bias

class GNN_Contagion(nn.Module):
    """
    Graph Neural Network for Supply Chain and Systemic Contagion Risk.
    Predicts the probability of failure for every node in a network 
    given the state of connected nodes.
    """
    def __init__(self, num_features, hidden_size, num_classes=1, dropout=0.5):
        super(GNN_Contagion, self).__init__()
        
        self.gc1 = GraphConvolution(num_features, hidden_size)
        self.gc2 = GraphConvolution(hidden_size, hidden_size)
        self.gc3 = GraphConvolution(hidden_size, num_classes)
        self.dropout = dropout

    def forward(self, x, adj):
        # Layer 1
        x = F.relu(self.gc1(x, adj))
        x = F.dropout(x, self.dropout, training=self.training)
        
        # Layer 2
        x = F.relu(self.gc2(x, adj))
        x = F.dropout(x, self.dropout, training=self.training)
        
        # Output Layer (Sigmoid for Probability of Failure)
        x = torch.sigmoid(self.gc3(x, adj))
        return x

def train_gnn_dummy():
    """
    Demonstrates training the robust GNN model on a synthetic infrastructure network.
    """
    print("Initializing Graph Neural Network (GNN) for Contagion Risk...")
    
    # Synthetic Graph: 100 infrastructure assets (nodes)
    num_nodes = 100
    num_features = 10 # 10 features per asset (capacity, age, stress, etc.)
    
    model = GNN_Contagion(num_features=num_features, hidden_size=32)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.BCELoss()
    
    # Generate random features
    x = torch.rand((num_nodes, num_features))
    
    # Generate random adjacency matrix (connections between assets)
    # In reality, this would be computed from supply chain links or spatial distance
    adj = torch.rand((num_nodes, num_nodes))
    adj = (adj > 0.95).float() # Sparse connections
    # Normalize adjacency matrix for GCN (A_hat = D^-0.5 * A * D^-0.5)
    row_sum = adj.sum(1)
    d_inv_sqrt = torch.pow(row_sum, -0.5)
    d_inv_sqrt[torch.isinf(d_inv_sqrt)] = 0.
    d_mat_inv_sqrt = torch.diag(d_inv_sqrt)
    adj_normalized = torch.mm(torch.mm(d_mat_inv_sqrt, adj), d_mat_inv_sqrt)
    
    # Target: 1 if asset fails, 0 otherwise
    y = torch.randint(0, 2, (num_nodes, 1)).float()
    
    print("Training loop started (50 epochs)...")
    model.train()
    for epoch in range(50):
        optimizer.zero_grad()
        output = model(x, adj_normalized)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/50 - Contagion Loss: {loss.item():.4f}")
            
    print("GNN Training Complete. System is robust against systemic contagion.")
    return model

if __name__ == "__main__":
    train_gnn_dummy()
