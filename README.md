# SelfCBR: Self-supervised Contrastive Learning for Bundle Recommendation


## Requirements
1. OS: Ubuntu 18.04 or higher version
2. python3.7
3. supported(tested) CUDA versions: 10.2
4. python modules: refer to [requirements.txt](https://github.com/mysbupt/SelfCBR/blob/main/requirements.txt)


## Code Structure
1. The entry script for training and evaluation is: [train.py](https://github.com/mysbupt/SelfCBR/blob/main/train.py)
2. The config file is: [config.yaml](https://github.com/mysbupt/SelfCBR/blob/main/config.yaml)
3. The script for data preprocess and dataloader: [utility.py](https://github.com/mysbupt/SelfCBR/blob/main/utility.py)
4. The model folder: ./models.
5. The experimental logs in tensorboard-format are saved in ./runs.
6. The experimental logs in txt-format are saved in ./log.
7. The best model and associate config file for each experimental setting is saved in ./checkpoints.
10. The script [get_all_the_res.py](https://github.com/mysbupt/SelfCBR/blob/main/get_all_the_res.py) is used to print the performance of all the trained and tested models on the screen.


## How to Run
1. Decompress the [dataset](https://github.com/mysbupt/SelfCBR/blob/main/dataset.tgz) in the top directory with the following command. Note that the downloaded files include all the three datasets ulilized in the paper: Youshu, NetEase, and iFashion.
    ```
    tar zxvf dataset.tgz. 
    ```

2. You can tune the hyper-parameters by revising the [config.yaml](https://github.com/mysbupt/SelfCBR/blob/main/config.yaml). Note that the settings in the config.yaml are the best settings we used in the submission. More details of each setting are elaborated in the file and paper. You can specify which gpu device (-g) and dataset (-d) to use for each training by the command line arguments. 

3. Run the training and evaluation with the specified hyper-parameters in config.yaml, using iFashion dataset and gpu 0, by the command: 
    ```
    python train.py -d iFashion -g 0. 
    ```

4. During the training, you can monitor the training loss and the evaluation performance by Tensorboard. You can get into ./runs to track the curves of your training and evaluation with the following command:
    ```
    cd ./runs && tensorboard --host="your host ip" --logdir=./
    ```

5. The performance of the model is saved in ./log. You can go into the folder and check the detailed training process of any finished experiments (Compared with the tensorboard log save in ./runs, ./log is just the txt-format human-readable training log). To quickly check the results for all implemented experiments, you can also print the results of all experiments in a table format on the terminal screen by running: 
    ```
    python get_all_the_res.py
    ```

6. The best model and associate configs are saved in ./checkpoints. You can load the dumped model and config to do inference on the testing set (The code is not released, considering conciseness, and you can implement by yourself).
