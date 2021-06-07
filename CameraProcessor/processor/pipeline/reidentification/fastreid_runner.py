import argparse
import cv2
from scipy.spatial.distance import cosine
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "fastreid"))

from processor.pipeline.reidentification.fastreid.fastreid.config import get_cfg
from processor.pipeline.reidentification.fastreid.demo.predictor import FeatureExtractionDemo

def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.freeze()
    return cfg

if __name__ == '__main__':

    args = argparse.ArgumentParser(description="Feature extraction with reid models")
    args.config_file = 'fastreid/config.yml'
    args.parallel = False

    cfg = setup_cfg(args)

    demo = FeatureExtractionDemo(cfg, parallel=args.parallel)

    image1 = cv2.imread('fastreid/images/image001.jpg')
    image2 = cv2.imread('fastreid/images/image004.jpg')


    image_feauture_1 = demo.run_on_image(image1)
    image_feauture_2 = demo.run_on_image(image2)

    distmat = 1 - cosine(image_feauture_1.cpu().numpy(), image_feauture_2.cpu().numpy())
    print(distmat)
