from easydict import EasyDict as edict

__C = edict()
cfg = __C

##################################
# general parameters
##################################
__C.general = {}

# Pick the largest connected component (cc) in segmentation
# Options:
# 1) True: pick the largest connected component
# 2) False: do not pick the largest connected component
__C.general.pick_largest_cc = True

# Remove small connected component (cc) in segmentation
# Options:
# 1) 0: Disable
# 2) a numerical number larger than 0: the threshold size of connected component
__C.general.remove_small_cc = 0

# partition type in the inference stage
# Options:
# 1) SIZE:    partition to blocks with specified size (unit: mm), set partition_size = [size_x, size_y, size_z]
# 2) DISABLE: no partition
__C.general.partition_type = 'SIZE'

# if partition type = 'SIZE', set the partition size (unit: mm).
# it is recommended to set this value as the same with the physical cropping size in the training phase
__C.general.partition_size = [51.2, 51.2, 51.2]

# the moving stride of the partition window. If set it as the same with the partition size, there will be no overlap
# between the partition windows. Otherwise, the value of the overlapped area will be averaged.
# it is recommended to set this value as 1/4 of the partition size in order to avoid the apparent in-consistence between
# different partition window.
__C.general.partition_stride = [51.2, 51.2, 51.2]

# enable voxel net
__C.general.turn_on_voxel_net = True

# number of voxels for voxel net
__C.general.num_voxels_for_voxel_net = 10240

# number of iteration in bayesian segmentation, set it as 1 for non-bayesian segmentation model
__C.general.bayesian_iteration = 1
