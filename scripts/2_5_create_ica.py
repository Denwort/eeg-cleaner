from copy import deepcopy
import numpy as np
import mne
from mne.utils import logger
import os.path as op

import cleaner

from pipeline import raw_data_path

epochs_fname = raw_data_path[:-4] + '-pca-epo.fif'

epochs = mne.read_epochs(epochs_fname)
cleaner.reject(epochs_fname, epochs, required=True)
epochs.pick_types(eeg=True, exclude=[])
montage = mne.channels.make_standard_montage('standard_1020')
epochs.set_montage(montage)
epochs_fname = epochs_fname.replace('-pca-epo.fif', '-ica-epo.fif')
epochs.save(epochs_fname, overwrite=True)

picks = mne.pick_types(epochs.info, meg=False, eeg=True, eog=False,
                        stim=False, exclude='bads')
ica = mne.preprocessing.ICA(
    n_components=0.99, max_iter=512,
    method='infomax', verbose=True)


ica.fit(epochs, picks=picks, verbose=True)
ica_fname = epochs_fname.replace('-ica-epo.fif', '-epo-ica.fif')
ica.save(ica_fname, overwrite=True)

