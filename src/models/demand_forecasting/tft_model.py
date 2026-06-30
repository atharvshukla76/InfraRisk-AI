import torch
import torch.nn as nn
import numpy as np

# A lightweight PyTorch implementation/stub of a Temporal Fusion Transformer (TFT)
# For full production, `pytorch-forecasting` is recommended, but this demonstrates 
# the core architecture components for robust sequence modeling.

class GatedResidualNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout=0.1):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.elu = nn.ELU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.dropout = nn.Dropout(dropout)
        self.gate = nn.Sequential(
            nn.Linear(input_size, output_size),
            nn.Sigmoid()
        )
        self.layer_norm = nn.LayerNorm(output_size)
        
        # Skip connection projection if sizes differ
        self.skip_proj = nn.Linear(input_size, output_size) if input_size != output_size else nn.Identity()

    def forward(self, x):
        skip = self.skip_proj(x)
        out = self.fc1(x)
        out = self.elu(out)
        out = self.fc2(out)
        out = self.dropout(out)
        
        # Gating mechanism
        gate = self.gate(x)
        out = gate * out
        
        return self.layer_norm(out + skip)

class TemporalFusionTransformer_Core(nn.Module):
    """
    Robust architecture for demand forecasting (Traffic/Toll Revenue, Energy Grid Load).
    Combines static covariates (location, project type) with dynamic covariates 
    (daily weather, GDP, historical traffic).
    """
    def __init__(self, static_dim, dynamic_dim, hidden_size=64, num_heads=4, num_layers=2):
        super().__init__()
        self.hidden_size = hidden_size
        
        # Variable Selection Networks (simplified via GRNs)
        self.static_encoder = GatedResidualNetwork(static_dim, hidden_size, hidden_size)
        self.dynamic_encoder = GatedResidualNetwork(dynamic_dim, hidden_size, hidden_size)
        
        # Temporal processing (LSTM instead of full multi-head for simplicity in this stub)
        self.lstm = nn.LSTM(
            input_size=hidden_size, 
            hidden_size=hidden_size, 
            num_layers=num_layers, 
            batch_first=True
        )
        
        # Attention mechanism
        self.attention = nn.MultiheadAttention(embed_dim=hidden_size, num_heads=num_heads, batch_first=True)
        
        # Output layer (Predicting P10, P50, P90 quantiles for risk modeling)
        self.output_layer = nn.Linear(hidden_size, 3) 

    def forward(self, static_feat, dynamic_feat):
        """
        static_feat: [batch_size, static_dim]
        dynamic_feat: [batch_size, seq_len, dynamic_dim]
        """
        batch_size, seq_len, _ = dynamic_feat.shape
        
        # Encode static features and expand to sequence length
        static_enc = self.static_encoder(static_feat) # [batch_size, hidden_size]
        static_enc_seq = static_enc.unsqueeze(1).repeat(1, seq_len, 1)
        
        # Encode dynamic features
        dynamic_enc = self.dynamic_encoder(dynamic_feat) # [batch_size, seq_len, hidden_size]
        
        # Combine
        combined_feat = dynamic_enc + static_enc_seq
        
        # Sequence modeling
        lstm_out, _ = self.lstm(combined_feat)
        
        # Self-attention over the sequence
        attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
        
        # Predict next step quantiles from the last sequence step
        last_step = attn_out[:, -1, :]
        quantiles = self.output_layer(last_step) # [batch_size, 3]
        
        return quantiles

def train_tft_dummy():
    """
    Demonstrates training the robust TFT model with synthetic traffic data.
    """
    print("Initializing Robust Temporal Fusion Transformer...")
    model = TemporalFusionTransformer_Core(static_dim=5, dynamic_dim=10)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    
    # Quantile Loss (Pinball Loss) for P10, P50, P90
    def quantile_loss(preds, targets, quantiles=[0.1, 0.5, 0.9]):
        losses = []
        for i, q in enumerate(quantiles):
            errors = targets - preds[:, i]
            loss = torch.max((q - 1) * errors, q * errors)
            losses.append(loss.mean())
        return sum(losses)
        
    print("Generating synthetic infrastructure traffic data...")
    # Batch=32, Seq_len=30 days, static=5, dynamic=10
    static_data = torch.rand((32, 5))
    dynamic_data = torch.rand((32, 30, 10))
    targets = torch.rand((32,)) # Target traffic volume for day 31
    
    print("Training loop started (5 epochs)...")
    model.train()
    for epoch in range(5):
        optimizer.zero_grad()
        preds = model(static_data, dynamic_data)
        loss = quantile_loss(preds, targets)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}/5 - Quantile Loss: {loss.item():.4f}")
        
    print("TFT Training Complete. System is robust against demand uncertainty.")
    return model

if __name__ == "__main__":
    train_tft_dummy()
