# NICE-EEG Cleaner
# Copyright (C) 2019 - Authors of NICE-EEG-Cleaner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# You can be released from the requirements of the license by purchasing a
# commercial license. Buying such a license is mandatory as soon as you
# develop commercial activities as mentioned in the GNU Affero General Public
# License version 3 without disclosing the source code of your own
# applications.
#

import json
import mne
from mne.utils import logger
import os.path as op

from argparse import ArgumentParser

from cleaner import reject, update_log
from cleaner.utils import configure_logging, remove_file_logging

# Read a raw file, plot and select bad channels.

from pipeline import raw_data_path
default_path = raw_data_path

default_scaling = 30e-6
default_lpass = 40
default_hpass = 1


parser = ArgumentParser(description='Clean a RAW (continous) file.')
parser.add_argument('--path', metavar='path', nargs=1, type=str,
                    default=default_path,
                    help='Path with the file or the subjects folder (if using '
                          'NICE Extensions package).')
    
parser.add_argument('--scaling', metavar='scaling', type=float, nargs='?',
                    default=default_scaling,
                    help=('Scaling to use when plotting EEG signals '
                          '(Default {})'.format(default_scaling)))

parser.add_argument('--hpass', metavar='hpass', type=float, nargs='?',
                    default=default_hpass,
                    help=('Frequency of the High Pass filter. Used only for'
                          'plotting. (Default {})'.format(default_hpass)))

parser.add_argument('--lpass', metavar='lpass', type=float, nargs='?',
                    default=default_lpass,
                    help=('Frequency of the Low Pass filter. Used only for'
                          'plotting. (Default {})'.format(default_lpass)))

parser.add_argument('--config', metavar='config', type=str, nargs='?',
                    default=None,
                    help=('NICE Extensions config to use for reading. '
                          'Defaults to None (do not use NICE Extensions)'))

args = parser.parse_args()
path = args.path
scaling = args.scaling
hpass = args.hpass
lpass = args.lpass
config = args.config

if isinstance(path, list):
    path = path[0]

if isinstance(scaling, list):
    scaling = scaling[0]

if isinstance(hpass, list):
    hpass = hpass[0]

if isinstance(lpass, list):
    lpass = lpass[0]

if isinstance(config, list):
    config = config[0]

configure_logging(path)
logger.info('Started RAW cleaner')

if config is None:
    raws = mne.io.read_raw_fif(path, preload=True)
    fname = path
else:
    raws = mne.io.read_raw_fif(path)

if not path.endswith('/') and op.isdir(path):
    path = '{}/'.format(path)

if not isinstance(raws, list):
    raws = [raws]

for t_raw in raws:
    fname = op.basename(t_raw.filenames[0])
    logger.info('Cleaning {}'.format(fname))

    # Mark previous bad channels
    reject(path, t_raw)

    logger.info('Filtering {} - {}'.format(hpass, lpass))
    t_raw.filter(hpass, lpass)
    
    # Plot
    t_raw.plot(block=True, scalings={'eeg': scaling})

    # Save new channels
    update_log(path, t_raw)

logger.info('Finished RAW cleaner')
remove_file_logging()