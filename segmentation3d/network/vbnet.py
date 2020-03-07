import torch
import torch.nn as nn

from segmentation3d.network.module.weight_init import kaiming_weight_init, gaussian_weight_init
from segmentation3d.network.module.vnet_inblock import InputBlock
from segmentation3d.network.module.vnet_outblock import OutputBlock
from segmentation3d.network.module.vnet_upblock import UpBlock
from segmentation3d.network.module.vnet_downblock import DownBlock


def parameters_kaiming_init(net):
    """ model parameters initialization """
    net.apply(kaiming_weight_init)


def parameters_gaussian_init(net):
    """ model parameters initialization """
    net.apply(gaussian_weight_init)


class SegmentationNet(nn.Module):
    """ volumetric segmentation network """

    def __init__(self, in_channels, out_channels, dropout_turn_on=False):
        super(SegmentationNet, self).__init__()
        self.in_block = InputBlock(in_channels, 16)
        self.down_32 = DownBlock(16, 1, compression=False)
        self.down_64 = DownBlock(32, 2, compression=True)
        self.down_128 = DownBlock(64, 3, compression=True)
        self.down_256 = DownBlock(128, 3, compression=True)
        self.up_256 = UpBlock(256, 256, 3, compression=True)
        self.up_128 = UpBlock(256, 128, 3, compression=True)
        self.up_64 = UpBlock(128, 64, 2, compression=False)
        self.up_32 = UpBlock(64, 32, 1, compression=False)
        self.out_block = OutputBlock(32, out_channels)
        self.dropout_turn_on = dropout_turn_on
        if self.dropout_turn_on:
            self.dropout = nn.Dropout3d(p=0.5, inplace=False)


    def forward(self, input):
        assert isinstance(input, torch.Tensor)

        if self.dropout_turn_on:
            self.dropout.train()

        out16 = self.in_block(input)
        out32 = self.down_32(out16)

        out64 = self.down_64(out32)
        if self.dropout_turn_on:
            out64 = self.dropout(out64)

        out128 = self.down_128(out64)
        if self.dropout_turn_on:
            out128 = self.dropout(out128)

        out256 = self.down_256(out128)
        if self.dropout_turn_on:
            out256 = self.dropout(out256)

        out = self.up_256(out256, out128)
        if self.dropout_turn_on:
            out = self.dropout(out)

        out = self.up_128(out, out64)
        if self.dropout_turn_on:
            out = self.dropout(out)

        out = self.up_64(out, out32)
        if self.dropout_turn_on:
            out = self.dropout(out)

        out = self.up_32(out, out16)
        out = self.out_block(out)
        return out

    def max_stride(self):
        return 16
