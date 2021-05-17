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

    def parse_file(self):
        coco = COCO(self.file_path)

        # Specify a list of category names of interest
        cat_ids = coco.getCatIds(catNms=['person'])
        # Get the corresponding image ids and images using loadImgs
        img_ids = coco.getImgIds(catIds=cat_ids)
        img_ids = img_ids[:self.nr_frames]

        ann_ids = coco.getAnnIds(imgIds=img_ids)
        anns = coco.loadAnns(ann_ids)
        with open(self.filter_config['targets_path']) as filter_names:
            filters = filter_names.read().splitlines()

        counter = 0
        boxes = []
        previous_name = ''

        for ann in anns:
            width, height = self.get_image_size(ann['id'])
            box = BoundingBox(classification=coco.loadCats(ann['category_id'])[0]['name'],
                              rectangle=Rectangle(x1=ann['bbox'][0] / width,
                                                  y1=ann['bbox'][1] / height,
                                                  x2=(ann['bbox'][0] + ann['bbox'][2]) / width,
                                                  y2=(ann['bbox'][1] + ann['bbox'][3]) / height),
                              identifier=str(counter),
                              score=1)
            if box.label in filters:
                boxes.append(box)
            current_name = ann['image_id']
            if current_name != previous_name:
                counter += 1
            previous_name = current_name
        return BoundingBoxes(boxes)

    def download_coco_images(self, amount):
        """Download images from the COCO dataset containing the category person.

        Args:
            amount: Amount of images to download.

        Returns: COCO images in the image_upload_path folder.

        """
        coco = COCO(self.accuracy_config['gt_path'])

        # Specify a list of category names of interest
        cat_ids = coco.getCatIds(catNms=['person'])
        # Get the corresponding image ids and images using loadImgs
        img_ids = coco.getImgIds(catIds=cat_ids)
        img_ids = img_ids[:amount]
        images = coco.loadImgs(img_ids)

        for image in images:
            image_data = requests.get(image['coco_url']).content
            with open(self.accuracy_config['image_upload_path'] + '/' + image['file_name'], 'wb') as handler:
                handler.write(image_data)

    def get_image_size(self, image_id):
        """Gets the size of an image based on its COCO name.

          Args:
              image_id: String with the name of the image.

          Returns: width, height (integers).

          """
        file_path = path.abspath(self.image_path + numpy.zeros(12 - len(image_id)) + image_id + '.jpg')
        image = Image.open(file_path)
        return image.size