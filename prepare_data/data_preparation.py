from ultralytics.data.converter import convert_coco
from sklearn.model_selection import train_test_split
from pathlib import Path
import shutil

target_dir = "datasets"
origin_dir = "data_filtered"
subdir = ["test", "train", "val"]

def create_targets(origin, target):

    convert_coco(
        labels_dir = origin,
        save_dir= target,
        use_segments = False,
        use_keypoints = False,
        cls91to80 = True,
        lvis = False,
    )

    for x in subdir:
        Path(target_dir+"/"+x+"/images").mkdir(parents=True)
        Path(target_dir+"/"+x+"/labels").mkdir(parents=True)

def test_split(origin, target):

    imgs = list(Path('.').glob(origin+'/*.jpg'))
    txts = list(Path('.').glob(target+'/**/*.txt'))

    img_train, img_test, txt_train, txt_test = train_test_split(imgs, txts, test_size=0.3, random_state=42)
    img_val, img_test, txt_val, txt_test = train_test_split(img_test, txt_test, test_size=0.3, random_state=42)
    
    for x in img_train:
        shutil.copy(x, target_dir+"/train/images")
    for x in img_test:
        shutil.copy(x, target_dir+"/test/images")
    for x in txt_train:
        shutil.copy(x, target_dir+"/train/labels")
    for x in txt_test:
        shutil.copy(x, target_dir+"/test/labels")
    for x in img_val:
        shutil.copy(x, target_dir+"/val/images")
    for x in txt_val:
        shutil.copy(x, target_dir+"/val/labels")
    
    shutil.rmtree(target_dir + "/images")
    shutil.rmtree(target_dir + "/labels")