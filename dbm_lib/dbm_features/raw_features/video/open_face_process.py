"""
file_name: process_features
project_name: DBM
created: 2020-20-07
"""

import os
import numpy as np
import pandas as pd
import glob
import logging

from dbm_lib.dbm_features.raw_features.util import util as ut

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger()

def batch_open_face(filepaths,video_url, input_dir, out_dir, of_path):
    """ Computes open_face features for the files in filepaths
    
    Args:
    -----
        filepaths: (itreable[str])
        video_tracking: To specify whether openface's video tracking module (FaceLandmarkVid)
                    is being used or the default (FeatureExtract)
        video_url: Raw video location on S3 bucket
        input_dir: Path to the input videos
        out_dir: Path to the processed output
        of_path: OpenFace source code path
                    
    Returns:
    --------
        (itreable[str]) list of .csv files
    """
    
    suffix = '_OF_features'
    csv_files = []
    
    for fp in filepaths:
        try:
            
            _, out_loc, fl_name = ut.filter_path(video_url, out_dir)
            full_f_name = fl_name + suffix
            output_directory = os.path.join(out_loc, full_f_name)

            csv_files.append(ut.compute_open_face_features(fp,output_directory,of_path))
            
        except Exception as e:
            logger.error('Failed to run OpenFace on {}\n{}'.format(fp, e))
            
    return csv_files
        
def process_open_face(video_uri, input_dir, out_dir, of_path, dbm_group):
    """
    Processing all patient's for fetching emotion expressivity
    -------------------
    -------------------
    Args:
        video_uri: video path; input_dir : input directory for video's; dbm_group: feature group
        out_dir: (str) Output directory for processed output; of_path: OpenFace source code path 
        
    """
    try:
        
        if dbm_group != None and len(dbm_group) == 1 and 'acoustic' in dbm_group:
            return

        filepaths = [video_uri]
        csv_filepaths = batch_open_face(filepaths, video_uri, input_dir, out_dir, of_path)
        
    except Exception as e:
        logger.error('Failed to process video file')