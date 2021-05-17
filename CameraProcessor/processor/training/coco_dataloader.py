import requests
from pycocotools.coco import COCO
import numpy
from PIL import Image
from os import path
from processor.data_object.bounding_box import BoundingBox
from processor.data_object.bounding_boxes import BoundingBoxes
from processor.data_object.rectangle import Rectangle
from processor.training.idataloader import IDataloader


class COCODataloader(IDataloader):

    def __init__(self, categories, file_path, nr_frames, image_path=''):
        super().__init__(categories, file_path, nr_frames, image_path='')
        self.coco = COCO(file_path)

    def parse_file(self):
        annotations = self.__get_annotations()
        boxes = self.__parse_boxes(annotations)
        return BoundingBoxes(boxes)

    def download_coco_images(self, amount):
        """Download images from the COCO dataset containing the category person.

        Args:
            amount: Amount of images to download.

        Returns: COCO images in the image_upload_path folder.

        """
        # Specify a list of category names of interest
        cat_ids = self.coco.getCatIds(catNms=['person'])
        # Get the corresponding image ids and images using loadImgs
        img_ids = self.coco.getImgIds(catIds=cat_ids)
        img_ids = img_ids[:amount]
        images = self.coco.loadImgs(img_ids)

        for image in images:
            image_data = requests.get(image['coco_url']).content
            with open(self.image_path + '/' + image['file_name'], 'wb') as handler:
                handler.write(image_data)

    def __parse_boxes(self, annotations):
        counter = 0
        boxes = []
        previous_name = ''

        for ann in annotations:
            width, height = self.get_image_size(ann['id'])
            box = BoundingBox(classification=self.coco.loadCats(ann['category_id'])[0]['name'],
                              rectangle=Rectangle(x1=ann['bbox'][0] / width,
                                                  y1=ann['bbox'][1] / height,
                                                  x2=(ann['bbox'][0] + ann['bbox'][2]) / width,
                                                  y2=(ann['bbox'][1] + ann['bbox'][3]) / height),
                              identifier=counter,
                              certainty=1)
            current_name = ann['image_id']
            if current_name != previous_name:
                counter += 1
            previous_name = current_name
        return boxes

    def __get_annotations(self):
        annotations = self.__get_all_annotations()
        annotations = self.__filter_annotations(annotations)
        return annotations

    def __get_all_annotations(self):
        # Specify a list of category names of interest
        cat_ids = self.coco.getCatIds(catNms=self.categories)
        # Get the corresponding image ids and images using loadImgs
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

    def get_image_size(self, image_id):
        """Gets the size of an image based on its COCO name.

          Args:
              image_id: String with the name of the image.

          Returns: width, height (integers).

          """
        file_path = path.abspath(self.image_path + numpy.zeros(12 - len(image_id)) + image_id + '.jpg')
        image = Image.open(file_path)
        return image.size
