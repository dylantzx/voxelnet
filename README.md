# Introduction

This is an unofficial inplementation of [VoxelNet: End-to-End Learning for Point Cloud Based 3D Object Detection](https://arxiv.org/abs/1711.06396) in TensorFlow. A large part of this project is based on the work [here](https://github.com/jeasinema/VoxelNet-tensorflow). Thanks to [@jeasinema](https://github.com/jeasinema). This work is a modified version with bugs fixed and better experimental settings to chase the results reported in the paper (still ongoing).

# Dependencies
- `python3.6+`
- `TensorFlow 2.0` 
- `opencv`
- `shapely`
- `numba`
- `easydict`

# Installation
1. Clone this repository.

2. Install the dependencies
```
pip3 install -r requirements.txt
```

3. Compile the Cython module
```
python3 setup.py build_ext --inplace
```

4. Compile the evaluation code
```
cd kitti_eval
g++ -std=c++14 -o evaluate_object_3d_offline evaluate_object_3d_offline.cpp
```

5. Grant the execution permission to evaluation script
```
cd kitti_eval
chmod +x launch_test.sh
```

# Data Preparation
1. Download the 3D KITTI detection dataset from [here](http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d). Data to download include:
    * Velodyne point clouds (29 GB): input data to VoxelNet
    * Training labels of object data set (5 MB): input label to VoxelNet
    * Camera calibration matrices of object data set (16 MB): for visualization of predictions
    * Left color images of object data set (12 GB): for visualization of predictions

2. After downloading the 4 folders mentioned above, we will use `data.crop.py` to get the cropped point cloud data for training and validation. Point clouds outside the image coordinates will be removed. To do so, update the directories on `lines 82 - 85` in `data/crop.py` and run `data/crop.py` to generate the cropped data. Note that cropped point cloud data will overwrite raw point cloud data.

```
cd data
python crop.py
```

3. Split the training set into training and validation set according to the protocol [here](https://xiaozhichen.github.io/files/mv3d/imagesets.tar.gz). And rearrange the folders to have the following structure:
```plain
└── cropped_dataset
       ├── training   <-- training data
       |   ├── image_2
       |   ├── label_2
       |   └── velodyne
       └── validation  <--- evaluation data
       |   ├── image_2
       |   ├── label_2
       |   └── velodyne
```
        
4. Update the dataset directory in `config.py` and `kitti_eval/launch_test.sh`

# Train
1. Specify the GPUs to use in `config.py`
2. run `train.py` with desired hyper-parameters to start training:
```bash
$ python3 train.py --alpha 1 --beta 10
```
Note that the hyper-parameter settings introduced in the paper are not able to produce high quality results. So, a different setting is specified here.

Training on two Nvidia 1080 Ti GPUs takes around 3 days (160 epochs as reported in the paper). During training, training statistics are recorded in `log/default`, which can be monitored by tensorboard. And models are saved in `save_model/default`. Intermediate validation results will be dumped into the folder `predictions/XXX/data` with `XXX` as the epoch number. And metrics will be calculated and saved in  `predictions/XXX/log`. If the `--vis` flag is set to be `True`, visualizations of intermediate results will be dumped in the folder `predictions/XXX/vis`.

3. When the training is done, executing `parse_log.py` will generate the learning curve.
```bash
$ python3 parse_log.py predictions
```

4. There is a pre-trained model for car in `save_model/pre_trained_car`.


# Evaluate
1. run `test.py -n default` to produce final predictions on the validation set after training is done. Change `-n` flag to `pre_trained_car` will start testing for the pre-trained model (only car model provided for now).
```bash
$ python3 test.py -n pre_trained_car -b 1
```
results will be dumped into `predictions/data`. Set the `--vis` flag to True if dumping visualizations and they will be saved into `predictions/vis`.

2. run the following command to measure quantitative performances of predictions:
```
./kitti_eval/evaluate_object_3d_offline [DATA_DIR]/validation/label_2 ./predictions
```

# Performances

The current implementation and training scheme are able to produce results in the tables below.

##### Bird's eye view detection performance: AP on KITTI validation set

| Car | Easy | Moderate | Hard |
|:-:|:-:|:-:|:-:|
| Reported | 89.60 | 84.81 | 78.57 |
| Reproduced | 85.41  | 83.16  | 77.10 |

##### 3D detection performance: AP on KITTI validation set

| Car | Easy | Moderate | Hard |
|:-:|:-:|:-:|:-:|
| Reported | 81.97 | 65.46 | 62.85 |
| Reproduced | 53.43  | 48.78 | 48.06 |

# TODO
- [X] improve the performances
- [ ] reproduce results for `Pedestrian` and `Cyclist`
- [X] fix the deadlock problem in multi-thread processing in training
- [X] fix the infinite loop problem in `test.py`
- [X] replace averaged calibration matrices with correct ones


