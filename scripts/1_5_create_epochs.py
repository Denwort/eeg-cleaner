from copy import deepcopy
import numpy as np
import mne
from mne.utils import logger
import os.path as op

# 1. Run 1_clean_raw.py

#  %run 1_clean_raw.py --path='/Users/fraimondo/data/lg_controls/subjects/jaco/test-raw.fif'

# 2. Filter and cut

import cleaner

from pipeline import raw_data_path

raw_fname = raw_data_path
raw = mne.io.read_raw_fif(raw_fname, preload=True)
cleaner.reject(raw_fname, raw, required=True)

duration = 1

#events = mne.make_fixed_length_events(raw)
epochs = mne.make_fixed_length_epochs(raw, duration=duration, preload=True)

from sklearn.decomposition import PCA
n_pca = 14


picks = mne.pick_types(epochs.info, meg=False, eeg=True, eog=False,
                        stim=False, exclude='bads')

pca = mne.decoding.UnsupervisedSpatialFilter(PCA(n_pca), average=False)
logger.info('Fitting PCA (n_pca = {})'.format(n_pca))
pca_data = pca.fit_transform(epochs.get_data()[:, picks, :])
blank = np.zeros((pca_data.shape[0], len(raw.info.ch_names), pca_data.shape[2]))
pca_data = np.concatenate([blank, pca_data], axis=1)
ch_names = raw.info.ch_names
ch_names += ['PCA{}'.format(x) for x in range(n_pca)]
ch_types = ['misc'] * len(ch_names)
info = mne.create_info(ch_names, epochs.info['sfreq'], ch_types)

info['description'] = epochs.info['description']
info.set_meas_date(epochs.info['meas_date'])

pca_epochs = mne.EpochsArray(pca_data, info)

new_ch_names = pca_epochs.ch_names
epochs.rename_channels({ch_name: new_ch_names[i] for i, ch_name in enumerate(epochs.ch_names)})

epochs.filter(l_freq=1, h_freq=40)

epochs_fname = raw_fname[:-4] + '-pca-epo.fif'
epochs.save(epochs_fname, overwrite=True)