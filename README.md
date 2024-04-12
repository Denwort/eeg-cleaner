# EEG Cleaner

This project provides a pipeline for preprocessing raw EEG data and offers visualization tools for future analysis.

## Credits

This code was adapted from the work of [fraimondo](https://github.com/fraimondo). You can find the original code on this repo: [NICE-EED Cleaner](https://github.com/fraimondo/eeg_cleaner)

## Installation

NICE-EEG cleaner must be installed in development mode, go in the source
code directory and do:

    python setup.py develop

## Dependencies

The required dependencies to build the software are: 
- python >= 3.4
- mne-python \>= 0.13: <http://mne-tools.github.io/stable/index.html>

## How to use

NICE-EEG Cleaner is a collection of scripts that allows to tag and clean
EEG recordings, both continous and epoched data.

In the `scripts` folder you can find 3 scripts:

-   1_clean_raw.py: The intention of this script is to mark bad EEG channels on continous recordings and filter wrong frequencies.

-   2_clean_epochs.py: Rejects bad epochs.

-   3_clean_ica.py: Rejects bad components in the ICA.

The inteded way of use is to follow this pipeline:

1.  Run the script `1_0_clean_raw.py` to annotate the bad channels.
2.  Preprocess the continous data and create an epochs file. Recommended steps:
    -   Filter
    -   Cut data into epochs
    
    To do that, you can run `1_5_create_epochs.py`
    
3.  Run the script `2_0_clean_epochs.py` to annotate the bad epochs.
4.  Run ICA on the preprocessed epochs. 
    To do that, you can run `2_5_create_ica.py`
    Note: Once this step is done, the parameters in step 2 can't be changed.
5.  Run the script `3_0_clean_ica.py` to annotate the bad components.
6.  Finish the preprocessing:
    -   Apply ICA
    -   Interpolate bad channels
    -   Re-Reference

Steps 1, 3 and 5 updates a file named `eeg_cleaner.json`
with all the information needed to preprocess the raw files and recreate
the clean data. Some parameters can be changed at different steps.
Notice that the EEG cleaner relies on file names, so if any file is renamed, the
`eeg_cleaner.json` file should be updated.

## Pipeline

To excecute all the steps mencioned above in a simple way, you can follow these steps:

1. Add your raw data file to `/samples`
2. In pipeline.py, update the filepath to point to your new file.
2. Run `python pipeline.py`
3. The new files will be created inside `/samples`, including the final report.