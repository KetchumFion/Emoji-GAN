import json
import os
from datetime import datetime

import keras.backend as K
import numpy as np
# uncomment to use on machines that don't support standard matplotlib backend
# import matplotlib
# matplotlib.use('Agg')
from matplotlib import pyplot as plt


def load_unlabelled_dataset(company, resolution, channels):
    unlabelled_dataset_filepath = '../../dataset/'
    dataset = np.load(unlabelled_dataset_filepath + company + '_' + str(resolution) + '.npy')
    return np.reshape(dataset, (dataset.shape[0] * dataset.shape[1], resolution, resolution, channels))


def load_labelled_dataset(company, resolution, channels):
    unlabelled_dataset_filepath = '../../dataset/'
    dataset = np.load(unlabelled_dataset_filepath + company + '_' + str(resolution) + '.npy')
    dataset = dataset[:, :, :, :channels]
    return dataset


def set_model_trainable(model, trainable):
    model.trainable = trainable
    for l in model.layers:
        l.trainable = trainable


def save_samples(generated_data, rows, columns, resolution, channels, filenames):
    plt.subplots(rows, columns, figsize=(7, 7))

    k = 1
    for i in range(rows):
        for j in range(columns):
            plt.subplot(rows, columns, k)
            if channels == 1:
                plt.imshow((generated_data[k - 1].reshape(resolution, resolution) + 1.0) / 2.0, cmap='gray')
            else:
                plt.imshow((generated_data[k - 1].reshape(resolution, resolution, channels) + 1.0) / 2.0)
            plt.xticks([])
            plt.yticks([])
            k += 1
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    for filename in filenames:
        plt.savefig(filename)
    plt.clf()
    plt.close()


def save_samples_classes(generated_data, labels, rows, columns, resolution, channels, filenames):
    plt.subplots(rows, columns, figsize=(7, 7))

    k = 1
    for i in range(rows):
        for j in range(columns):
            plt.subplot(rows, columns, k)
            plt.title(labels[k - 1])
            if channels == 1:
                plt.imshow((generated_data[k - 1].reshape(resolution, resolution) + 1.0) / 2.0, cmap='gray')
            else:
                plt.imshow((generated_data[k - 1].reshape(resolution, resolution, channels) + 1.0) / 2.0)
                plt.xticks([])
            plt.yticks([])
            k += 1
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0.5)
    for filename in filenames:
        plt.savefig(filename)
    plt.clf()
    plt.close()


def save_losses_wgan(losses, filename, legend_name='critic'):
    plt.figure(figsize=(15, 4.5))
    plt.plot(losses[0])
    plt.plot(losses[1])
    plt.legend(['generator', legend_name])
    plt.savefig(filename)
    plt.clf()
    plt.close()


def save_losses_other(losses, filename, text):
    plt.figure(figsize=(15, 4.5))
    plt.plot(losses)
    plt.legend([text])
    plt.savefig(filename)
    plt.clf()
    plt.close()


def save_losses_wgan_gp_ae(losses, filename, legend_name='generator AE'):
    plt.subplots(2, 1, figsize=(15, 9))
    plt.subplot(2, 1, 1)
    plt.plot(losses[0])
    plt.plot(losses[1])
    plt.legend(['generator', 'critic'])

    plt.subplot(2, 1, 2)
    plt.plot(losses[2])
    plt.legend([legend_name])

    plt.savefig(filename)
    plt.clf()
    plt.close()


def save_latent_space(generated_data, grid_size, resolution, channels, filenames):
    plt.subplots(grid_size, grid_size, figsize=(grid_size, grid_size))

    for i in range(grid_size):
        for j in range(grid_size):
            plt.subplot(grid_size, grid_size, i * grid_size + j + 1)
            if channels == 1:
                plt.imshow((generated_data[i * grid_size + j].reshape(resolution, resolution) + 1.0) / 2.0, cmap='gray')
            else:
                plt.imshow((generated_data[i * grid_size + j].reshape(resolution, resolution, channels) + 1.0) / 2.0)
            plt.xticks([])
            plt.yticks([])
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    for filename in filenames:
        plt.savefig(filename)
    plt.clf()
    plt.close()


def save_latent_space_classes(generated_data, chosen_class, grid_size, resolution, channels, filenames):
    plt.subplots(grid_size, grid_size, figsize=(grid_size, grid_size))
    plt.suptitle(chosen_class)

    for i in range(grid_size):
        for j in range(grid_size):
            plt.subplot(grid_size, grid_size, i * grid_size + j + 1)
            if channels == 1:
                plt.imshow((generated_data[i * grid_size + j].reshape(resolution, resolution) + 1.0) / 2.0, cmap='gray')
            else:
                plt.imshow((generated_data[i * grid_size + j].reshape(resolution, resolution, channels) + 1.0) / 2.0)
            plt.xticks([])
            plt.yticks([])
    for filename in filenames:
        plt.savefig(filename)
    plt.clf()
    plt.close()


def generate_run_dir(model_type):
    root_path = '../outputs/' + model_type
    if not os.path.exists(root_path):
        os.makedirs(root_path)

    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    run_dir = root_path + '/' + current_datetime
    img_dir = run_dir + '/img'
    model_dir = run_dir + '/models'
    generated_datasets_dir = run_dir + '/generated_datasets'

    os.mkdir(run_dir)
    os.mkdir(img_dir)
    os.mkdir(model_dir)
    os.mkdir(generated_datasets_dir)

    return run_dir, img_dir, model_dir, generated_datasets_dir


def get_global_config():
    batch_size = 64
    epochs = 1000000
    latent_dim = 100
    img_frequency = 2500
    loss_frequency = 1250
    latent_space_frequency = 10000
    model_save_frequency = 100000
    dataset_generation_frequency = 100000
    dataset_generation_size = 1000

    n_generator = 1
    n_critic = 5
    generator_lr = 0.001
    critic_lr = 0.001
    gradient_penalty_weight = 10
    gamma = 0.5

    lr_decay_factor = 0.5
    lr_decay_steps = epochs / 4

    epoch = 0

    config = {
        'batch_size': batch_size,
        'epoch': epoch,
        'epochs': epochs,
        'latent_dim': latent_dim,
        'img_frequency': img_frequency,
        'loss_frequency': loss_frequency,
        'latent_space_frequency': latent_space_frequency,
        'model_save_frequency': model_save_frequency,
        'dataset_generation_frequency': dataset_generation_frequency,
        'dataset_generation_size': dataset_generation_size,
        'lr_decay_factor': lr_decay_factor,
        'lr_decay_steps': lr_decay_steps,
        'n_generator': n_generator,
        'n_critic': n_critic,
        'gradient_penalty_weight': gradient_penalty_weight,
        'gamma': gamma,
        'generator_lr': generator_lr,
        'critic_lr': critic_lr
    }

    return config


def merge_config_and_save(config_2):
    config = get_global_config()
    config.update(config_2)

    with open(str(config['run_dir']) + '/config.json', 'w') as f:
        json.dump(config, f, indent=4, sort_keys=True)

    return config


def update_config_epoch(config_filepath, new_epoch):
    config = json.load(open(config_filepath, 'r'))

    config['epoch'] = new_epoch
    with open(config_filepath, 'w') as f:
        json.dump(config, f, indent=4, sort_keys=True)


def wasserstein_loss(y_true, y_pred):
    return K.mean(y_true * y_pred)


def apply_lr_decay(models, lr_decay_factor):
    for model in models:
        lr_tensor = model.optimizer.lr
        lr = K.get_value(lr_tensor)
        K.set_value(lr_tensor, lr * lr_decay_factor)
