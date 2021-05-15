import requests
from pycocotools.coco import COCO


class COCODataloader:
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
            box = BoundingBox(classification =coco.loadCats(ann['category_id'])[0]['name'], xtl=ann['bbox'][0] / self.image_width,
                              ytl=ann['bbox'][1] / self.image_height,
                              xbr=(ann['bbox'][0] + ann['bbox'][2]) / self.image_width,
                              ybr=(ann['bbox'][1] + ann['bbox'][3]) / self.image_height, identifier=str(counter),
                              score=1)
            if box.label in filters:
                boxes.append(box)
            current_name = ann['image_id']
            if current_name != previous_name:
                counter += 1
            previous_name = current_name
        return boxes
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