"""COCO datalaoder class.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from os import path

import requests
from pycocotools.coco import COCO

from processor.dataloaders.i_dataloader import IDataloader


class CocoDataloader(IDataloader):
    """COCO Dataloader, formats COCO Data."""

    def __init__(self, configs):
        """Initialize coco dataloader.

        Args:
            configs (dict): A dictionary of the configs.
            path_location (str): String to select gt or det from the accuracy config.
        """
        super().__init__(configs)
        dataloader_config = configs['COCO']
        self.file_path = dataloader_config['annotations_path']
        self.image_path = dataloader_config['image_path']
        self.coco = COCO(self.file_path)

    def download_coco_image(self, image_id):
        """Downloads a single coco image given the identifier.

        Args:
            image_id (int): Identifier of the image
        """
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

    def get_image_dimensions(self, image_id):
        """Gets the size of an image based on its name.

        Args:
            image_id (integer): String with the name of the image.

        Returns:
            image.size (shape): width and height dimensions of the image.
        """
        image = self.coco.loadImgs([image_id])[0]
        width = int(image['width'])
        height = int(image['height'])

        return width, height

    def parse_line(self, line):
        """Parses a line.

        Args:
            line (JSON): JSON object with file line contents.

        Returns:
            line ([(int, int, float, float, float, float, float, string, None)]): parsed line.
        """
        image_id = line['image_id']
        width, height = self.get_image_dimensions(image_id)
        identifier = line['id']
        classification = self.coco.loadCats(line['category_id'])[0]['name']
        x1 = line['bbox'][0] / width
        y1 = line['bbox'][1] / height
        x2 = (line['bbox'][0] + line['bbox'][2]) / width
        y2 = (line['bbox'][1] + line['bbox'][3]) / height
        certainty = 1
        return [(image_id, identifier, x1, y1, x2, y2, certainty, classification, None)]

    def get_annotations(self):
        """Gets annotations.

        Returns:
            annotations (list): List of string annotations.
        """
        annotations = self.__get_all_annotations()
        annotations = self.__filter_annotations(annotations)
        return annotations

    def __get_all_annotations(self):
        """Retrieves all the annotations from the self.categories.

        Returns:
            [(str)]: List of all the annotations from a category.
        """
        # Specify a list of category names of interest.
        cat_ids = self.coco.getCatIds(catNms=self.categories)
        # Get the corresponding image ids and images using loadImgs.
        img_ids = self.coco.getImgIds(catIds=cat_ids)
        img_ids = img_ids[:self.nr_frames]

        ann_ids = self.coco.getAnnIds(imgIds=img_ids)
        anns = self.coco.loadAnns(ann_ids)
        return anns

    def __filter_annotations(self, annotations):
        """Filters the annotations.

        Args:
            annotations ([(str)]): Annotations tuples in a list.

        Returns:
            [(str)]: List of filtered annotations
        """
        filtered_annotations = []

        with open(self.filter_config['targets_path']) as filter_names:
            filters = filter_names.read().splitlines()

        for ann in annotations:
            if self.coco.loadCats(ann['category_id'])[0]['name'] in filters:
                filtered_annotations.append(ann)
        return filtered_annotations

    def __get_image_name(self, image_id):
        """Gets the image name given an identifier.

        Args:
            image_id (int): Identifier of the image

        Returns:
            str: Name of the image.
        """
        zeros = ''
        for _ in range(12 - len(str(image_id))):
            zeros += '0'
        image_name = zeros + str(image_id)
        return image_name

    def __get_image_path(self, image_id):
        """Gets the image path given an identifier.

        Args:
            image_id (int): Identifier of the image

        Returns:
            str: Path of the image.
        """
        image_name = self.__get_image_name(image_id)
        this_image_path = path.abspath(f'{self.image_path}/{image_name}.jpg')
        return this_image_path
