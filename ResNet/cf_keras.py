import keras
from keras.models import Model
from keras import layers
import keras.backend as K
import numpy as np
from keras.layers.core import Lambda
import tensorflow as tf


weights_dict = dict()
def load_weights_from_file(weight_file):
    try:
        weights_dict = np.load(weight_file).item()
    except:
        weights_dict = np.load(weight_file, encoding='bytes').item()

    return weights_dict


def set_layer_weights(model, weights_dict):
    for layer in model.layers:
        if layer.name in weights_dict:
            cur_dict = weights_dict[layer.name]
            current_layer_parameters = list()
            if layer.__class__.__name__ == "BatchNormalization":
                if 'scale' in cur_dict:
                    current_layer_parameters.append(cur_dict['scale'])
                if 'bias' in cur_dict:
                    current_layer_parameters.append(cur_dict['bias'])
                current_layer_parameters.extend([cur_dict['mean'], cur_dict['var']])
            elif layer.__class__.__name__ == "Scale":
                if 'scale' in cur_dict:
                    current_layer_parameters.append(cur_dict['scale'])
                if 'bias' in cur_dict:
                    current_layer_parameters.append(cur_dict['bias'])
            elif layer.__class__.__name__ == "SeparableConv2D":
                current_layer_parameters = [cur_dict['depthwise_filter'], cur_dict['pointwise_filter']]
                if 'bias' in cur_dict:
                    current_layer_parameters.append(cur_dict['bias'])
            elif layer.__class__.__name__ == "Embedding":
                current_layer_parameters.append(cur_dict['weights'])
            else:
                # rot weights
                current_layer_parameters = [cur_dict['weights']]
                if 'bias' in cur_dict:
                    current_layer_parameters.append(cur_dict['bias'])
            model.get_layer(layer.name).set_weights(current_layer_parameters)

    return model


def KitModel(weight_file = None):
    global weights_dict
    weights_dict = load_weights_from_file(weight_file) if not weight_file == None else None
        
    data            = layers.Input(name = 'data', shape = (224, 224, 3,) )
    conv1_7x7_s2_input = layers.ZeroPadding2D(padding = ((3, 3), (3, 3)))(data)
    conv1_7x7_s2    = convolution(weights_dict, name='conv1/7x7_s2', input=conv1_7x7_s2_input, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(7, 7), strides=(2, 2), dilation_rate=(1, 1), padding='valid', use_bias=True)
    conv1_relu_7x7  = layers.Activation(name='conv1/relu_7x7', activation='relu')(conv1_7x7_s2)
    pool1_3x3_s2_input = layers.ZeroPadding2D(padding = ((0, 1), (0, 1)))(conv1_relu_7x7)
    pool1_3x3_s2    = layers.MaxPooling2D(name = 'pool1/3x3_s2', pool_size = (3, 3), strides = (2, 2), padding = 'valid')(pool1_3x3_s2_input)
    pool1_norm1     = LRN(size = 3, alpha = 9.999999747378752e-05, beta = 0.75, k = 1.0, name = 'pool1/norm1')(pool1_3x3_s2)
    conv2_3x3_reduce = convolution(weights_dict, name='conv2/3x3_reduce', input=pool1_norm1, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    conv2_relu_3x3_reduce = layers.Activation(name='conv2/relu_3x3_reduce', activation='relu')(conv2_3x3_reduce)
    conv2_3x3_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(conv2_relu_3x3_reduce)
    conv2_3x3       = convolution(weights_dict, name='conv2/3x3', input=conv2_3x3_input, group=1, conv_type='layers.Conv2D', filters=192, kernel_size=(3, 3), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    conv2_relu_3x3  = layers.Activation(name='conv2/relu_3x3', activation='relu')(conv2_3x3)
    conv2_norm2     = LRN(size = 3, alpha = 9.999999747378752e-05, beta = 0.75, k = 1.0, name = 'conv2/norm2')(conv2_relu_3x3)
    pool2_3x3_s2_input = layers.ZeroPadding2D(padding = ((0, 1), (0, 1)))(conv2_norm2)
    pool2_3x3_s2    = layers.MaxPooling2D(name = 'pool2/3x3_s2', pool_size = (3, 3), strides = (2, 2), padding = 'valid')(pool2_3x3_s2_input)
    inception_3a_3x3_reduce = convolution(weights_dict, name='inception_3a/3x3_reduce', input=pool2_3x3_s2, group=1, conv_type='layers.Conv2D', filters=96, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3a_pool_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(pool2_3x3_s2)
    inception_3a_pool = layers.MaxPooling2D(name = 'inception_3a/pool', pool_size = (3, 3), strides = (1, 1), padding = 'valid')(inception_3a_pool_input)
    inception_3a_1x1 = convolution(weights_dict, name='inception_3a/1x1', input=pool2_3x3_s2, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3a_5x5_reduce = convolution(weights_dict, name='inception_3a/5x5_reduce', input=pool2_3x3_s2, group=1, conv_type='layers.Conv2D', filters=16, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3a_relu_3x3_reduce = layers.Activation(name='inception_3a/relu_3x3_reduce', activation='relu')(inception_3a_3x3_reduce)
    inception_3a_pool_proj = convolution(weights_dict, name='inception_3a/pool_proj', input=inception_3a_pool, group=1, conv_type='layers.Conv2D', filters=32, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3a_relu_1x1 = layers.Activation(name='inception_3a/relu_1x1', activation='relu')(inception_3a_1x1)
    inception_3a_relu_5x5_reduce = layers.Activation(name='inception_3a/relu_5x5_reduce', activation='relu')(inception_3a_5x5_reduce)
    inception_3a_3x3_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_3a_relu_3x3_reduce)
    inception_3a_3x3 = convolution(weights_dict, name='inception_3a/3x3', input=inception_3a_3x3_input, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(3, 3), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3a_relu_pool_proj = layers.Activation(name='inception_3a/relu_pool_proj', activation='relu')(inception_3a_pool_proj)
    inception_3a_5x5_input = layers.ZeroPadding2D(padding = ((2, 2), (2, 2)))(inception_3a_relu_5x5_reduce)
    inception_3a_5x5 = convolution(weights_dict, name='inception_3a/5x5', input=inception_3a_5x5_input, group=1, conv_type='layers.Conv2D', filters=32, kernel_size=(5, 5), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3a_relu_3x3 = layers.Activation(name='inception_3a/relu_3x3', activation='relu')(inception_3a_3x3)
    inception_3a_relu_5x5 = layers.Activation(name='inception_3a/relu_5x5', activation='relu')(inception_3a_5x5)
    inception_3a_output = layers.concatenate(name = 'inception_3a/output', inputs = [inception_3a_relu_1x1, inception_3a_relu_3x3, inception_3a_relu_5x5, inception_3a_relu_pool_proj])
    inception_3b_3x3_reduce = convolution(weights_dict, name='inception_3b/3x3_reduce', input=inception_3a_output, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3b_pool_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_3a_output)
    inception_3b_pool = layers.MaxPooling2D(name = 'inception_3b/pool', pool_size = (3, 3), strides = (1, 1), padding = 'valid')(inception_3b_pool_input)
    inception_3b_1x1 = convolution(weights_dict, name='inception_3b/1x1', input=inception_3a_output, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3b_5x5_reduce = convolution(weights_dict, name='inception_3b/5x5_reduce', input=inception_3a_output, group=1, conv_type='layers.Conv2D', filters=32, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3b_relu_3x3_reduce = layers.Activation(name='inception_3b/relu_3x3_reduce', activation='relu')(inception_3b_3x3_reduce)
    inception_3b_pool_proj = convolution(weights_dict, name='inception_3b/pool_proj', input=inception_3b_pool, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3b_relu_1x1 = layers.Activation(name='inception_3b/relu_1x1', activation='relu')(inception_3b_1x1)
    inception_3b_relu_5x5_reduce = layers.Activation(name='inception_3b/relu_5x5_reduce', activation='relu')(inception_3b_5x5_reduce)
    inception_3b_3x3_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_3b_relu_3x3_reduce)
    inception_3b_3x3 = convolution(weights_dict, name='inception_3b/3x3', input=inception_3b_3x3_input, group=1, conv_type='layers.Conv2D', filters=192, kernel_size=(3, 3), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3b_relu_pool_proj = layers.Activation(name='inception_3b/relu_pool_proj', activation='relu')(inception_3b_pool_proj)
    inception_3b_5x5_input = layers.ZeroPadding2D(padding = ((2, 2), (2, 2)))(inception_3b_relu_5x5_reduce)
    inception_3b_5x5 = convolution(weights_dict, name='inception_3b/5x5', input=inception_3b_5x5_input, group=1, conv_type='layers.Conv2D', filters=96, kernel_size=(5, 5), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_3b_relu_3x3 = layers.Activation(name='inception_3b/relu_3x3', activation='relu')(inception_3b_3x3)
    inception_3b_relu_5x5 = layers.Activation(name='inception_3b/relu_5x5', activation='relu')(inception_3b_5x5)
    inception_3b_output = layers.concatenate(name = 'inception_3b/output', inputs = [inception_3b_relu_1x1, inception_3b_relu_3x3, inception_3b_relu_5x5, inception_3b_relu_pool_proj])
    pool3_3x3_s2_input = layers.ZeroPadding2D(padding = ((0, 1), (0, 1)))(inception_3b_output)
    pool3_3x3_s2    = layers.MaxPooling2D(name = 'pool3/3x3_s2', pool_size = (3, 3), strides = (2, 2), padding = 'valid')(pool3_3x3_s2_input)
    inception_4a_pool_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(pool3_3x3_s2)
    inception_4a_pool = layers.MaxPooling2D(name = 'inception_4a/pool', pool_size = (3, 3), strides = (1, 1), padding = 'valid')(inception_4a_pool_input)
    inception_4a_3x3_reduce = convolution(weights_dict, name='inception_4a/3x3_reduce', input=pool3_3x3_s2, group=1, conv_type='layers.Conv2D', filters=96, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4a_1x1 = convolution(weights_dict, name='inception_4a/1x1', input=pool3_3x3_s2, group=1, conv_type='layers.Conv2D', filters=192, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4a_5x5_reduce = convolution(weights_dict, name='inception_4a/5x5_reduce', input=pool3_3x3_s2, group=1, conv_type='layers.Conv2D', filters=16, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4a_pool_proj = convolution(weights_dict, name='inception_4a/pool_proj', input=inception_4a_pool, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4a_relu_3x3_reduce = layers.Activation(name='inception_4a/relu_3x3_reduce', activation='relu')(inception_4a_3x3_reduce)
    inception_4a_relu_1x1 = layers.Activation(name='inception_4a/relu_1x1', activation='relu')(inception_4a_1x1)
    inception_4a_relu_5x5_reduce = layers.Activation(name='inception_4a/relu_5x5_reduce', activation='relu')(inception_4a_5x5_reduce)
    inception_4a_relu_pool_proj = layers.Activation(name='inception_4a/relu_pool_proj', activation='relu')(inception_4a_pool_proj)
    inception_4a_3x3_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_4a_relu_3x3_reduce)
    inception_4a_3x3 = convolution(weights_dict, name='inception_4a/3x3', input=inception_4a_3x3_input, group=1, conv_type='layers.Conv2D', filters=208, kernel_size=(3, 3), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4a_5x5_input = layers.ZeroPadding2D(padding = ((2, 2), (2, 2)))(inception_4a_relu_5x5_reduce)
    inception_4a_5x5 = convolution(weights_dict, name='inception_4a/5x5', input=inception_4a_5x5_input, group=1, conv_type='layers.Conv2D', filters=48, kernel_size=(5, 5), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4a_relu_3x3 = layers.Activation(name='inception_4a/relu_3x3', activation='relu')(inception_4a_3x3)
    inception_4a_relu_5x5 = layers.Activation(name='inception_4a/relu_5x5', activation='relu')(inception_4a_5x5)
    inception_4a_output = layers.concatenate(name = 'inception_4a/output', inputs = [inception_4a_relu_1x1, inception_4a_relu_3x3, inception_4a_relu_5x5, inception_4a_relu_pool_proj])
    inception_4b_5x5_reduce = convolution(weights_dict, name='inception_4b/5x5_reduce', input=inception_4a_output, group=1, conv_type='layers.Conv2D', filters=24, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4b_pool_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_4a_output)
    inception_4b_pool = layers.MaxPooling2D(name = 'inception_4b/pool', pool_size = (3, 3), strides = (1, 1), padding = 'valid')(inception_4b_pool_input)
    inception_4b_3x3_reduce = convolution(weights_dict, name='inception_4b/3x3_reduce', input=inception_4a_output, group=1, conv_type='layers.Conv2D', filters=112, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4b_1x1 = convolution(weights_dict, name='inception_4b/1x1', input=inception_4a_output, group=1, conv_type='layers.Conv2D', filters=160, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4b_relu_5x5_reduce = layers.Activation(name='inception_4b/relu_5x5_reduce', activation='relu')(inception_4b_5x5_reduce)
    inception_4b_pool_proj = convolution(weights_dict, name='inception_4b/pool_proj', input=inception_4b_pool, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4b_relu_3x3_reduce = layers.Activation(name='inception_4b/relu_3x3_reduce', activation='relu')(inception_4b_3x3_reduce)
    inception_4b_relu_1x1 = layers.Activation(name='inception_4b/relu_1x1', activation='relu')(inception_4b_1x1)
    inception_4b_5x5_input = layers.ZeroPadding2D(padding = ((2, 2), (2, 2)))(inception_4b_relu_5x5_reduce)
    inception_4b_5x5 = convolution(weights_dict, name='inception_4b/5x5', input=inception_4b_5x5_input, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(5, 5), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4b_relu_pool_proj = layers.Activation(name='inception_4b/relu_pool_proj', activation='relu')(inception_4b_pool_proj)
    inception_4b_3x3_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_4b_relu_3x3_reduce)
    inception_4b_3x3 = convolution(weights_dict, name='inception_4b/3x3', input=inception_4b_3x3_input, group=1, conv_type='layers.Conv2D', filters=224, kernel_size=(3, 3), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4b_relu_5x5 = layers.Activation(name='inception_4b/relu_5x5', activation='relu')(inception_4b_5x5)
    inception_4b_relu_3x3 = layers.Activation(name='inception_4b/relu_3x3', activation='relu')(inception_4b_3x3)
    inception_4b_output = layers.concatenate(name = 'inception_4b/output', inputs = [inception_4b_relu_1x1, inception_4b_relu_3x3, inception_4b_relu_5x5, inception_4b_relu_pool_proj])
    inception_4c_3x3_reduce = convolution(weights_dict, name='inception_4c/3x3_reduce', input=inception_4b_output, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4c_1x1 = convolution(weights_dict, name='inception_4c/1x1', input=inception_4b_output, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4c_5x5_reduce = convolution(weights_dict, name='inception_4c/5x5_reduce', input=inception_4b_output, group=1, conv_type='layers.Conv2D', filters=24, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4c_pool_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_4b_output)
    inception_4c_pool = layers.MaxPooling2D(name = 'inception_4c/pool', pool_size = (3, 3), strides = (1, 1), padding = 'valid')(inception_4c_pool_input)
    inception_4c_relu_3x3_reduce = layers.Activation(name='inception_4c/relu_3x3_reduce', activation='relu')(inception_4c_3x3_reduce)
    inception_4c_relu_1x1 = layers.Activation(name='inception_4c/relu_1x1', activation='relu')(inception_4c_1x1)
    inception_4c_relu_5x5_reduce = layers.Activation(name='inception_4c/relu_5x5_reduce', activation='relu')(inception_4c_5x5_reduce)
    inception_4c_pool_proj = convolution(weights_dict, name='inception_4c/pool_proj', input=inception_4c_pool, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4c_3x3_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_4c_relu_3x3_reduce)
    inception_4c_3x3 = convolution(weights_dict, name='inception_4c/3x3', input=inception_4c_3x3_input, group=1, conv_type='layers.Conv2D', filters=256, kernel_size=(3, 3), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4c_5x5_input = layers.ZeroPadding2D(padding = ((2, 2), (2, 2)))(inception_4c_relu_5x5_reduce)
    inception_4c_5x5 = convolution(weights_dict, name='inception_4c/5x5', input=inception_4c_5x5_input, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(5, 5), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4c_relu_pool_proj = layers.Activation(name='inception_4c/relu_pool_proj', activation='relu')(inception_4c_pool_proj)
    inception_4c_relu_3x3 = layers.Activation(name='inception_4c/relu_3x3', activation='relu')(inception_4c_3x3)
    inception_4c_relu_5x5 = layers.Activation(name='inception_4c/relu_5x5', activation='relu')(inception_4c_5x5)
    inception_4c_output = layers.concatenate(name = 'inception_4c/output', inputs = [inception_4c_relu_1x1, inception_4c_relu_3x3, inception_4c_relu_5x5, inception_4c_relu_pool_proj])
    inception_4d_5x5_reduce = convolution(weights_dict, name='inception_4d/5x5_reduce', input=inception_4c_output, group=1, conv_type='layers.Conv2D', filters=32, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4d_pool_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_4c_output)
    inception_4d_pool = layers.MaxPooling2D(name = 'inception_4d/pool', pool_size = (3, 3), strides = (1, 1), padding = 'valid')(inception_4d_pool_input)
    inception_4d_1x1 = convolution(weights_dict, name='inception_4d/1x1', input=inception_4c_output, group=1, conv_type='layers.Conv2D', filters=112, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4d_3x3_reduce = convolution(weights_dict, name='inception_4d/3x3_reduce', input=inception_4c_output, group=1, conv_type='layers.Conv2D', filters=144, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4d_relu_5x5_reduce = layers.Activation(name='inception_4d/relu_5x5_reduce', activation='relu')(inception_4d_5x5_reduce)
    inception_4d_pool_proj = convolution(weights_dict, name='inception_4d/pool_proj', input=inception_4d_pool, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4d_relu_1x1 = layers.Activation(name='inception_4d/relu_1x1', activation='relu')(inception_4d_1x1)
    inception_4d_relu_3x3_reduce = layers.Activation(name='inception_4d/relu_3x3_reduce', activation='relu')(inception_4d_3x3_reduce)
    inception_4d_5x5_input = layers.ZeroPadding2D(padding = ((2, 2), (2, 2)))(inception_4d_relu_5x5_reduce)
    inception_4d_5x5 = convolution(weights_dict, name='inception_4d/5x5', input=inception_4d_5x5_input, group=1, conv_type='layers.Conv2D', filters=64, kernel_size=(5, 5), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4d_relu_pool_proj = layers.Activation(name='inception_4d/relu_pool_proj', activation='relu')(inception_4d_pool_proj)
    inception_4d_3x3_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_4d_relu_3x3_reduce)
    inception_4d_3x3 = convolution(weights_dict, name='inception_4d/3x3', input=inception_4d_3x3_input, group=1, conv_type='layers.Conv2D', filters=288, kernel_size=(3, 3), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4d_relu_5x5 = layers.Activation(name='inception_4d/relu_5x5', activation='relu')(inception_4d_5x5)
    inception_4d_relu_3x3 = layers.Activation(name='inception_4d/relu_3x3', activation='relu')(inception_4d_3x3)
    inception_4d_output = layers.concatenate(name = 'inception_4d/output', inputs = [inception_4d_relu_1x1, inception_4d_relu_3x3, inception_4d_relu_5x5, inception_4d_relu_pool_proj])
    inception_4e_5x5_reduce = convolution(weights_dict, name='inception_4e/5x5_reduce', input=inception_4d_output, group=1, conv_type='layers.Conv2D', filters=32, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4e_1x1 = convolution(weights_dict, name='inception_4e/1x1', input=inception_4d_output, group=1, conv_type='layers.Conv2D', filters=256, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4e_3x3_reduce = convolution(weights_dict, name='inception_4e/3x3_reduce', input=inception_4d_output, group=1, conv_type='layers.Conv2D', filters=160, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4e_pool_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_4d_output)
    inception_4e_pool = layers.MaxPooling2D(name = 'inception_4e/pool', pool_size = (3, 3), strides = (1, 1), padding = 'valid')(inception_4e_pool_input)
    inception_4e_relu_5x5_reduce = layers.Activation(name='inception_4e/relu_5x5_reduce', activation='relu')(inception_4e_5x5_reduce)
    inception_4e_relu_1x1 = layers.Activation(name='inception_4e/relu_1x1', activation='relu')(inception_4e_1x1)
    inception_4e_relu_3x3_reduce = layers.Activation(name='inception_4e/relu_3x3_reduce', activation='relu')(inception_4e_3x3_reduce)
    inception_4e_pool_proj = convolution(weights_dict, name='inception_4e/pool_proj', input=inception_4e_pool, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4e_5x5_input = layers.ZeroPadding2D(padding = ((2, 2), (2, 2)))(inception_4e_relu_5x5_reduce)
    inception_4e_5x5 = convolution(weights_dict, name='inception_4e/5x5', input=inception_4e_5x5_input, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(5, 5), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4e_3x3_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_4e_relu_3x3_reduce)
    inception_4e_3x3 = convolution(weights_dict, name='inception_4e/3x3', input=inception_4e_3x3_input, group=1, conv_type='layers.Conv2D', filters=320, kernel_size=(3, 3), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_4e_relu_pool_proj = layers.Activation(name='inception_4e/relu_pool_proj', activation='relu')(inception_4e_pool_proj)
    inception_4e_relu_5x5 = layers.Activation(name='inception_4e/relu_5x5', activation='relu')(inception_4e_5x5)
    inception_4e_relu_3x3 = layers.Activation(name='inception_4e/relu_3x3', activation='relu')(inception_4e_3x3)
    inception_4e_output = layers.concatenate(name = 'inception_4e/output', inputs = [inception_4e_relu_1x1, inception_4e_relu_3x3, inception_4e_relu_5x5, inception_4e_relu_pool_proj])
    pool4_3x3_s2_input = layers.ZeroPadding2D(padding = ((0, 1), (0, 1)))(inception_4e_output)
    pool4_3x3_s2    = layers.MaxPooling2D(name = 'pool4/3x3_s2', pool_size = (3, 3), strides = (2, 2), padding = 'valid')(pool4_3x3_s2_input)
    inception_5a_1x1 = convolution(weights_dict, name='inception_5a/1x1', input=pool4_3x3_s2, group=1, conv_type='layers.Conv2D', filters=256, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5a_3x3_reduce = convolution(weights_dict, name='inception_5a/3x3_reduce', input=pool4_3x3_s2, group=1, conv_type='layers.Conv2D', filters=160, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5a_5x5_reduce = convolution(weights_dict, name='inception_5a/5x5_reduce', input=pool4_3x3_s2, group=1, conv_type='layers.Conv2D', filters=32, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5a_pool_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(pool4_3x3_s2)
    inception_5a_pool = layers.MaxPooling2D(name = 'inception_5a/pool', pool_size = (3, 3), strides = (1, 1), padding = 'valid')(inception_5a_pool_input)
    inception_5a_relu_1x1 = layers.Activation(name='inception_5a/relu_1x1', activation='relu')(inception_5a_1x1)
    inception_5a_relu_3x3_reduce = layers.Activation(name='inception_5a/relu_3x3_reduce', activation='relu')(inception_5a_3x3_reduce)
    inception_5a_relu_5x5_reduce = layers.Activation(name='inception_5a/relu_5x5_reduce', activation='relu')(inception_5a_5x5_reduce)
    inception_5a_pool_proj = convolution(weights_dict, name='inception_5a/pool_proj', input=inception_5a_pool, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5a_3x3_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_5a_relu_3x3_reduce)
    inception_5a_3x3 = convolution(weights_dict, name='inception_5a/3x3', input=inception_5a_3x3_input, group=1, conv_type='layers.Conv2D', filters=320, kernel_size=(3, 3), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5a_5x5_input = layers.ZeroPadding2D(padding = ((2, 2), (2, 2)))(inception_5a_relu_5x5_reduce)
    inception_5a_5x5 = convolution(weights_dict, name='inception_5a/5x5', input=inception_5a_5x5_input, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(5, 5), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5a_relu_pool_proj = layers.Activation(name='inception_5a/relu_pool_proj', activation='relu')(inception_5a_pool_proj)
    inception_5a_relu_3x3 = layers.Activation(name='inception_5a/relu_3x3', activation='relu')(inception_5a_3x3)
    inception_5a_relu_5x5 = layers.Activation(name='inception_5a/relu_5x5', activation='relu')(inception_5a_5x5)
    inception_5a_output = layers.concatenate(name = 'inception_5a/output', inputs = [inception_5a_relu_1x1, inception_5a_relu_3x3, inception_5a_relu_5x5, inception_5a_relu_pool_proj])
    inception_5b_1x1 = convolution(weights_dict, name='inception_5b/1x1', input=inception_5a_output, group=1, conv_type='layers.Conv2D', filters=384, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5b_pool_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_5a_output)
    inception_5b_pool = layers.MaxPooling2D(name = 'inception_5b/pool', pool_size = (3, 3), strides = (1, 1), padding = 'valid')(inception_5b_pool_input)
    inception_5b_3x3_reduce = convolution(weights_dict, name='inception_5b/3x3_reduce', input=inception_5a_output, group=1, conv_type='layers.Conv2D', filters=192, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5b_5x5_reduce = convolution(weights_dict, name='inception_5b/5x5_reduce', input=inception_5a_output, group=1, conv_type='layers.Conv2D', filters=48, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5b_relu_1x1 = layers.Activation(name='inception_5b/relu_1x1', activation='relu')(inception_5b_1x1)
    inception_5b_pool_proj = convolution(weights_dict, name='inception_5b/pool_proj', input=inception_5b_pool, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(1, 1), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5b_relu_3x3_reduce = layers.Activation(name='inception_5b/relu_3x3_reduce', activation='relu')(inception_5b_3x3_reduce)
    inception_5b_relu_5x5_reduce = layers.Activation(name='inception_5b/relu_5x5_reduce', activation='relu')(inception_5b_5x5_reduce)
    inception_5b_relu_pool_proj = layers.Activation(name='inception_5b/relu_pool_proj', activation='relu')(inception_5b_pool_proj)
    inception_5b_3x3_input = layers.ZeroPadding2D(padding = ((1, 1), (1, 1)))(inception_5b_relu_3x3_reduce)
    inception_5b_3x3 = convolution(weights_dict, name='inception_5b/3x3', input=inception_5b_3x3_input, group=1, conv_type='layers.Conv2D', filters=384, kernel_size=(3, 3), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5b_5x5_input = layers.ZeroPadding2D(padding = ((2, 2), (2, 2)))(inception_5b_relu_5x5_reduce)
    inception_5b_5x5 = convolution(weights_dict, name='inception_5b/5x5', input=inception_5b_5x5_input, group=1, conv_type='layers.Conv2D', filters=128, kernel_size=(5, 5), strides=(1, 1), dilation_rate=(1, 1), padding='valid', use_bias=True)
    inception_5b_relu_3x3 = layers.Activation(name='inception_5b/relu_3x3', activation='relu')(inception_5b_3x3)
    inception_5b_relu_5x5 = layers.Activation(name='inception_5b/relu_5x5', activation='relu')(inception_5b_5x5)
    inception_5b_output = layers.concatenate(name = 'inception_5b/output', inputs = [inception_5b_relu_1x1, inception_5b_relu_3x3, inception_5b_relu_5x5, inception_5b_relu_pool_proj])
    pool5_7x7_s1    = layers.AveragePooling2D(name = 'pool5/7x7_s1', pool_size = (7, 7), strides = (1, 1), padding = 'valid')(inception_5b_output)
    pool5_drop_7x7_s1 = layers.Dropout(name = 'pool5/drop_7x7_s1', rate = 0.4000000059604645, seed = None)(pool5_7x7_s1)
    fc8_20_0        = __flatten(name = 'fc8-20_0', input = pool5_drop_7x7_s1)
    fc8_20_1        = layers.Dense(name = 'fc8-20_1', units = 23, use_bias = True)(fc8_20_0)
    prob            = layers.Activation(name='prob', activation='softmax')(fc8_20_1)
    model           = Model(inputs = [data], outputs = [prob])
    set_layer_weights(model, weights_dict)
    return model

import tensorflow as tf
class LRN(tf.keras.layers.Layer):
    def __init__(self, size=5, alpha=0.0005, beta=0.75, k=2, **kwargs):
        self.n = size
        self.alpha = alpha
        self.beta = beta
        self.k = k
        super(LRN, self).__init__(**kwargs)

    def build(self, input_shape):
        self.shape = input_shape
        super(LRN, self).build(input_shape)

    def call(self, x, mask=None):
        half_n = self.n - 1
        squared = K.square(x)
        scale = self.k
        norm_alpha = self.alpha / (2 * half_n + 1)
        if K.image_dim_ordering() == "th":
            b, f, r, c = self.shape
            squared = K.expand_dims(squared, 0)
            squared = K.spatial_3d_padding(squared, padding=((half_n, half_n), (0, 0), (0,0)))
            squared = K.squeeze(squared, 0)
            for i in range(half_n*2+1):
                scale += norm_alpha * squared[:, i:i+f, :, :]
        else:
            b, r, c, f = self.shape
            squared = K.expand_dims(squared, -1)
            squared = K.spatial_3d_padding(squared, padding=((0, 0), (0,0), (half_n, half_n)))
            squared = K.squeeze(squared, -1)
            for i in range(half_n*2+1):
                scale += norm_alpha * squared[:, :, :, i:i+f]

        scale = K.pow(scale, self.beta)
        return x / scale

    def compute_output_shape(self, input_shape):
        return input_shape

def convolution(weights_dict, name, input, group, conv_type, filters=None, **kwargs):
    if not conv_type.startswith('layer'):
        layer = keras.applications.mobilenet.DepthwiseConv2D(name=name, **kwargs)(input)
        return layer
    elif conv_type == 'layers.DepthwiseConv2D':
        layer = layers.DepthwiseConv2D(name=name, **kwargs)(input)
        return layer
    
    inp_filters = K.int_shape(input)[-1]
    inp_grouped_channels = int(inp_filters / group)
    out_grouped_channels = int(filters / group)
    group_list = []
    if group == 1:
        func = getattr(layers, conv_type.split('.')[-1])
        layer = func(name = name, filters = filters, **kwargs)(input)
        return layer
    weight_groups = list()
    if not weights_dict == None:
        w = np.array(weights_dict[name]['weights'])
        weight_groups = np.split(w, indices_or_sections=group, axis=-1)
    for c in range(group):
        x = layers.Lambda(lambda z: z[..., c * inp_grouped_channels:(c + 1) * inp_grouped_channels])(input)
        x = layers.Conv2D(name=name + "_" + str(c), filters=out_grouped_channels, **kwargs)(x)
        weights_dict[name + "_" + str(c)] = dict()
        weights_dict[name + "_" + str(c)]['weights'] = weight_groups[c]
        group_list.append(x)
    layer = layers.concatenate(group_list, axis = -1)
    if 'bias' in weights_dict[name]:
        b = K.variable(weights_dict[name]['bias'], name = name + "_bias")
        layer = layer + b
    return layer

def __flatten(name, input):
    if input.shape.ndims > 2: return layers.Flatten(name = name)(input)
    else: return input


