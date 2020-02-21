import os
import glob
import torch
import torch.nn as nn
import shutil


def get_checkpoint_folder(chk_root, epoch):
  """
  Get the checkpoint's folder with the specified epoch.
  :param chk_root: the check point root directory, which may contain multiple checkpoints.
  :param epoch: the epoch of the checkpoint, set -1 to get the latest epoch.
  :return: the folder containing the checkpoint with the specified epoch.
  """
  assert os.path.isdir(chk_root), 'The folder does not exist: {}'.format(chk_root)

  if epoch < 0:
    latest_epoch = -1
    chk_folders = os.path.join(chk_root, 'chk_*')
    for folder in glob.glob(chk_folders):
      folder_name = os.path.basename(folder)
      tokens = folder_name.split('_')
      cur_epoch = int(tokens[-1])
      if cur_epoch > latest_epoch:
        latest_epoch = cur_epoch

    epoch = latest_epoch

  return os.path.join(chk_root, 'chk_{}'.format(epoch))


def load_checkpoint(epoch_idx, net, opt, save_dir, gpu_id=0):
    """ load network parameters from directory

    :param epoch_idx: the epoch idx of model to load
    :param net: the network object
    :param opt: the optimizer object
    :param save_dir: the save directory
    :return: loaded epoch index, loaded batch index
    """
    # load network parameters
    chk_file = os.path.join(save_dir, 'checkpoints', 'chk_{}'.format(epoch_idx), 'params.pth')
    assert os.path.isfile(chk_file), 'checkpoint file not found: {}'.format(chk_file)

    if gpu_id >= 0:
      os.environ['CUDA_VISIBLE_DEVICES'] = '{}'.format(int(gpu_id))

    map_location = 'cpu' if gpu_id >= 0 else None

    state = torch.load(chk_file, map_location=map_location)

    if gpu_id >= 0:
      net = nn.parallel.DataParallel(net)

    net.load_state_dict(state['state_dict'])

    # load optimizer state
    opt_file = os.path.join(save_dir, 'checkpoints', 'chk_{}'.format(epoch_idx), 'optimizer.pth')
    assert os.path.isfile(opt_file), 'optimizer file not found: {}'.format(chk_file)

    opt_state = torch.load(opt_file, map_location=map_location)
    opt.load_state_dict(opt_state)

    if gpu_id >= 0:
      del os.environ['CUDA_VISIBLE_DEVICES']

    return state['epoch'], state['batch']


def save_checkpoint(mask_net, voxel_net, voxel_net_params, opt, epoch_idx, batch_idx, cfg, config_file, max_stride, num_modality):
  """ save model and parameters into a checkpoint file (.pth)

  :param mask_net: the mask head network object
  :param voxel_net: the voxel head network object
  :param voxel_net_params: the basic parameters of voxel net
  :param opt: the optimizer object
  :param epoch_idx: the epoch index
  :param batch_idx: the batch index
  :param cfg: the configuration object
  :param config_file: the configuration file path
  :param max_stride: the maximum stride of network
  :param num_modality: the number of image modalities
  :return: None
  """
  chk_folder = os.path.join(cfg.general.save_dir, 'checkpoints', 'chk_{}'.format(epoch_idx))
  if not os.path.isdir(chk_folder):
    os.makedirs(chk_folder)

  state = {'epoch':             epoch_idx,
           'batch':             batch_idx,
           'net':               cfg.net.name,
           'dropout':           cfg.net.dropout_turn_on,
           'max_stride':        max_stride,
           'state_dict':        mask_net.state_dict(),
           'spacing':           cfg.dataset.spacing,
           'interpolation':     cfg.dataset.interpolation,
           'in_channels':       num_modality,
           'out_channels':      cfg.dataset.num_classes,
           'crop_normalizers':  [normalizer.to_dict() for normalizer in cfg.dataset.crop_normalizers]
           }

  state_voxel_net = {'epoch': epoch_idx,
                     'batch': batch_idx,
                     'net': voxel_net_params['name'],
                     'state_dict': voxel_net.state_dict(),
                     'in_channels': voxel_net_params['in_channels'],
                     'in_coarse_channels': voxel_net_params['in_coarse_channels'],
                     'in_fine_channels': voxel_net_params['in_fine_channels'],
                     'out_channels': voxel_net_params['out_channels'],
                     'num_fc': voxel_net_params['num_fc']
                    }

  # save python check point
  filename = os.path.join(chk_folder, 'params.pth')
  torch.save(state, filename)

  # save python check point
  voxel_head_filename = os.path.join(chk_folder, 'voxel_head_params.pth')
  torch.save(state_voxel_net, voxel_head_filename)

  # save python optimizer state
  opt_filename = os.path.join(chk_folder, 'optimizer.pth')
  torch.save(opt.state_dict(), opt_filename)

  # save training and inference configuration files
  config_folder = os.path.dirname(os.path.dirname(__file__))
  infer_config_file = os.path.join(os.path.join(config_folder, 'config', 'infer_config.py'))
  shutil.copy(infer_config_file, os.path.join(chk_folder, 'infer_config.py'))

  shutil.copy(config_file, os.path.join(chk_folder, 'train_config.py'))