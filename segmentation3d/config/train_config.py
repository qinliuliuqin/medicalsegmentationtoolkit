from easydict import EasyDict as edict
from segmentation3d.utils.normalizer import FixedNormalizer, AdaptiveNormalizer


__C = edict()
cfg = __C


##################################
# general parameters
##################################

__C.general = {}

# image-segmentation pair list
__C.general.imseg_list = '/shenlab/lab_stor6/qinliu/CT_Dental/datasets/train.txt'

# the output of training models and logs

__C.general.save_dir = '/shenlab/lab_stor6/qinliu/CT_Dental/models/model_0224_2020/model2'

# continue training from certain epoch, -1 to train from scratch
__C.general.resume_epoch = 900

# the number of GPUs used in training. Set to 0 if using cpu only.

__C.general.num_gpus = 1

# random seed used in training (debugging purpose)
__C.general.seed = 0


##################################
# data set parameters
##################################

__C.dataset = {}

# the number of classes
__C.dataset.num_classes = 3

# the resolution on which segmentation is performed
__C.dataset.spacing = [0.4, 0.4, 0.4]

# the sampling crop size, e.g., determine the context information
__C.dataset.crop_size = [128, 128, 128]

# sampling method:
# 1) GLOBAL: sampling crops randomly in the entire image domain
# 2) MASK: sampling crops randomly within segmentation mask
# 3) HYBRID: Sampling crops randomly with both GLOBAL and MASK methods
# 4) CENTER: sampling crops in the image center
__C.dataset.sampling_method = 'HYBRID'

# translation augmentation (unit: mm)
__C.dataset.random_translation = [64, 64, 5]

# linear interpolation method:
# 1) NN: nearest neighbor interpolation
# 2) LINEAR: linear interpolation
__C.dataset.interpolation = 'LINEAR'

# crop intensity normalizers (to [-1,1])
# one normalizer corresponds to one input modality
# 1) FixedNormalizer: use fixed mean and standard deviation to normalize intensity
# 2) AdaptiveNormalizer: use minimum and maximum intensity of crop to normalize intensity
__C.dataset.crop_normalizers = [AdaptiveNormalizer()]

##################################
# training loss
##################################

__C.loss = {}

# the name of loss function to use
# Focal: Focal loss, supports binary-class and multi-class segmentation
# Dice: Dice Similarity Loss which supports binary and multi-class segmentation
__C.loss.name = 'Focal'

# the weight for each class including background class
# weights will be normalized
__C.loss.obj_weight = [1/3, 1/3, 1/3]

# the gamma parameter in focal loss
__C.loss.focal_gamma = 2

##################################
# voxel head parameters
##################################

__C.voxel_head = {}

# the number voxels for voxel head network
__C.voxel_head.num_voxels = 32768 

# oversample ratio
__C.voxel_head.oversample_ratio = 3

# importance sample ratio
__C.voxel_head.importance_sample_ratio = 0.75

# number of fully-connected layers
__C.voxel_head.num_fc = 3

# voxel head loss name
__C.voxel_head.loss_name = 'Focal'

# the gamma parameter in focal loss
# only valid for Focal loss
__C.voxel_head.loss_focal_gamma = 2

# the weight for each class including background class weights will be normalized
__C.voxel_head.loss_obj_weight = [1/3, 1/3, 1/3]

# loss weight
__C.voxel_head.loss_weight = 0.5

##################################
# net
##################################

__C.net = {}

# the network name
__C.net.name = 'vbnet_rend'
>>>>>>> qinliu

# enable uncertainty by trun on drop out layers in the segmentation net
__C.net.dropout_turn_on = False

##################################
# training parameters
##################################

__C.train = {}

# the number of training epochs
__C.train.epochs = 2001

# the number of samples in a batch
__C.train.batchsize = 4

# the number of threads for IO
__C.train.num_threads = 4

# the learning rate
__C.train.lr = 1e-4

# the beta in Adam optimizer
__C.train.betas = (0.9, 0.999)

# the number of batches to save model
__C.train.save_epochs = 100


###################################
# debug parameters
###################################

__C.debug = {}

# whether to save input crops
__C.debug.save_inputs = False
