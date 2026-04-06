import torch
import torch.nn as nn
from torchvision import models
import timm

class TripleAttentionFusion(nn.Module):
    def __init__(self, densenet, swin, vit, num_classes=4):
        super(TripleAttentionFusion, self).__init__()
        self.densenet_feat = nn.Sequential(*list(densenet.children())[:-1], nn.AdaptiveAvgPool2d(1))
        self.swin_feat = swin
        self.vit_feat = vit
        self.proj_cnn = nn.Linear(1024, 512)
        self.proj_swin = nn.Linear(768, 512)
        self.proj_vit = nn.Linear(768, 512)
        self.multihead_attn = nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)
        self.classifier = nn.Sequential(
            nn.Linear(512 * 3, 256),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        feat_cnn = self.densenet_feat(x).flatten(1)
        feat_swin = self.swin_feat.forward_features(x)
        if len(feat_swin.shape) == 4: feat_swin = feat_swin.mean(dim=(1, 2))
        elif len(feat_swin.shape) == 3: feat_swin = feat_swin.mean(dim=1)
        feat_vit = self.vit_feat.forward_features(x)
        if len(feat_vit.shape) == 3: feat_vit = feat_vit[:, 0]

        p_cnn = self.proj_cnn(feat_cnn).unsqueeze(1)
        p_swin = self.proj_swin(feat_swin).unsqueeze(1)
        p_vit = self.proj_vit(feat_vit).unsqueeze(1)

        query = torch.cat([p_swin, p_vit], dim=1)
        attn_out, _ = self.multihead_attn(query, p_cnn, p_cnn)
        combined = torch.cat([p_cnn.squeeze(1), attn_out.reshape(x.size(0), -1)], dim=1)
        return self.classifier(combined)

def get_model(num_classes=4):
    d_backbone = models.densenet121(weights=None)
    d_backbone.classifier = nn.Sequential(nn.Linear(1024, 512), nn.ReLU(), nn.Dropout(0.3), nn.Linear(512, num_classes))
    s_backbone = timm.create_model('swin_tiny_patch4_window7_224', pretrained=False, num_classes=num_classes)
    s_backbone.head = nn.Sequential(nn.Linear(768, 512), nn.ReLU(), nn.Dropout(0.3), nn.Linear(512, num_classes))
    v_backbone = timm.create_model('vit_base_patch16_224', pretrained=False, num_classes=num_classes)
    return TripleAttentionFusion(d_backbone, s_backbone, v_backbone, num_classes=num_classes)
