
from django.conf import settings

def startModelBuilding():
    import os
    traing_path =  os.path.join(os.getcwd(), 'media', 'dataset','train')
    test_path =  os.path.join(os.getcwd(), 'media', 'dataset', 'test')
    import tensorflow as tf
    from keras.models import Sequential
    from keras.layers import Convolution2D
    from keras.layers import MaxPooling2D
    from keras.layers import Flatten
    from keras.layers import Dense, Dropout
    import matplotlib.pyplot as plt
    import os

    os.environ['CUDA_VISIBLE_DEVICES'] = "0"
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.experimental.set_virtual_device_configuration(gpus[0], [
                tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)])
        except RuntimeError as e:
            print(e)

    sz = 256
    # Step 1 - Building the CNN

    # Initializing the CNN
    classifier = Sequential()

    classifier.add(Convolution2D(32, (3, 3), input_shape=(sz, sz, 1), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Convolution2D(32, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size=(2, 2)))
    classifier.add(Flatten())

    # Adding a fully connected layer
    classifier.add(Dense(units=128, activation='relu'))
    classifier.add(Dropout(0.20))
    classifier.add(Dense(units=112, activation='relu'))
    classifier.add(Dropout(0.10))
    classifier.add(Dense(units=96, activation='relu'))
    classifier.add(Dropout(0.10))
    classifier.add(Dense(units=80, activation='relu'))
    classifier.add(Dropout(0.10))
    classifier.add(Dense(units=64, activation='relu'))
    classifier.add(Dense(units=5, activation='softmax'))  # softmax for more than 2

    # Compiling the CNN
    classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    classifier.summary()
    from keras.preprocessing.image import ImageDataGenerator

    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    training_set = train_datagen.flow_from_directory(traing_path,
                                                     target_size=(sz, sz),
                                                     batch_size=10,
                                                     color_mode='grayscale',
                                                     class_mode='categorical')

    test_set = test_datagen.flow_from_directory(test_path,
                                                target_size=(sz, sz),
                                                batch_size=10,
                                                color_mode='grayscale',
                                                class_mode='categorical')
    history = classifier.fit_generator(
        training_set,
        steps_per_epoch=training_set.n // training_set.batch_size,  # No of images in training set/batch size
        epochs=100,
        validation_data=test_set,
        validation_steps=test_set.n // test_set.batch_size)  # No of images in test set/batc
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    return history