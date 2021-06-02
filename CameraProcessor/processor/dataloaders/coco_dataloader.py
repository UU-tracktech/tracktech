"""Datalaoder for COCO dataset.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from os import path

import requests
from pycocotools.coco import COCO

from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.rectangle import Rectangle
from processor.dataloaders.idataloader import IDataloader


class COCODataloader(IDataloader):
    """COCO Dataloader, formats COCO Data."""

    def __init__(self, configs, path_location):
        """Initialize coco dataloader.

        Args:
            configs (dict): A dictionary of the configs.
            path_location (str): String to select gt or det from the accuracy config.
        """
        super().__init__(configs, path_location)
        self.coco = COCO(self.file_path)

    def parse_file(self):
        """Parses an annotations file.

        Returns:
            bounding_boxes_list (list): List of bounding boxes.
        """
        annotations = self.__get_annotations()
        bounding_boxes_list = self.__parse_boxes(annotations)
        return bounding_boxes_list

    def download_coco_image(self, image_id):
        image = self.coco.loadImgs([image_id])[0]

        image_data = requests.get(image['coco_url']).content
        with open(self.image_path + '/' + image['file_name'], 'wb') as handler:
            handler.write(image_data)

    def download_coco_images(self, amount):
        """Download images from the COCO dataset containing the category person.

        Args:
            amount (integer): Amount of images to be downloaded.
        """
        # Specify a list of category names of interest.
        cat_ids = self.coco.getCatIds(catNms=['person'])
        # Get the corresponding image ids and images using loadImgs.
        img_ids = self.coco.getImgIds(catIds=cat_ids)
        img_ids = img_ids[:amount]
        images = self.coco.loadImgs(img_ids)

        for image in images:
            image_data = requests.get(image['coco_url']).content
            with open(self.image_path + '/' + image['file_name'], 'wb') as handler:
                handler.write(image_data)

    def get_image_dimensions(self, image_id, this_image_path):
        """Gets the size of an image based on its name.

        Args:
            image_id (integer): String with the name of the image.
            this_image_path (string): Path to image file.

        Returns:
            image.size (shape): width and height dimensions of the image.
        """
        image = self.coco.loadImgs([image_id])[0]
        width = int(image['width'])
        height = int(image['height'])

        return width, height

    def __parse_boxes(self, annotations):
        counter = 0
        bounding_boxes_list = []
        current_boxes = []
        current_image_id = annotations[0]['image_id']

        for annotation in annotations:
            image_id = annotation['image_id']
            width, height = self.get_image_dimensions(image_id, "")
            if not current_image_id == image_id:
                bounding_boxes_list.append(BoundingBoxes(current_boxes, int(self.__get_image_name(current_image_id))))
                current_boxes = []
                current_image_id = image_id
            current_boxes.append(BoundingBox(classification=self.coco.loadCats(annotation['category_id'])[0]['name'],
                                             rectangle=Rectangle(x1=annotation['bbox'][0] / width,
                                                                 y1=annotation['bbox'][1] / height,
                                                                 x2=(annotation['bbox'][0] + annotation['bbox'][
                                                                     2]) / width,
                                                                 y2=(annotation['bbox'][1] + annotation['bbox'][
                                                                     3]) / height),
                                             identifier=counter,
                                             certainty=1))
        return bounding_boxes_list

    def __get_annotations(self):
        annotations = self.__get_all_annotations()
        annotations = self.__filter_annotations(annotations)
        return annotations

    def __get_all_annotations(self):
        # Specify a list of category names of interest.
        cat_ids = self.coco.getCatIds(catNms=self.categories)
        # Get the corresponding image ids and images using loadImgs.
        img_ids = self.coco.getImgIds(catIds=cat_ids)
        img_ids = img_ids[:self.nr_frames]

        ann_ids = self.coco.getAnnIds(imgIds=img_ids)
        anns = self.coco.loadAnns(ann_ids)
        return anns

    def __filter_annotations(self, annotations):
        filtered_annotations = []

        with open(self.filter_config['targets_path']) as filter_names:
            filters = filter_names.read().splitlines()

        for ann in annotations:
            if self.coco.loadCats(ann['category_id'])[0]['name'] in filters:
                filtered_annotations.append(ann)
        return filtered_annotations

    def __get_image_name(self, image_id):
        zeros = ''
        for _ in range(12 - len(str(image_id))):
            zeros += '0'
        image_name = zeros + str(image_id)
        return image_name

    def __get_image_path(self, image_id):
        image_name = self.__get_image_name(image_id)
        this_image_path = path.abspath(f'{self.image_path}/{image_name}.jpg')
        return this_image_path
