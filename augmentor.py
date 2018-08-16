from imgaug import augmenters as iaa

### augmentors by https://github.com/aleju/imgaug
sometimes = lambda aug: iaa.Sometimes(0.5, aug)

# Define our sequence of augmentation steps that will be applied to every image
# All augmenters with per_channel=0.5 will sample one value _per image_
# in 50% of all cases. In all other cases they will sample new values
# _per channel_.
aug_pipe = iaa.Sequential(
    [
        # apply the following augmenters to most images
        # iaa.Fliplr(0.5), # horizontally flip 50% of all images
        # iaa.Flipud(0.2), # vertically flip 20% of all images
        # sometimes(iaa.Crop(percent=(0, 0.1))), # crop images by 0-10% of their height/width
        sometimes(iaa.Affine(
            # scale={"x": (0.8, 1.2), "y": (0.8, 1.2)}, # scale images to 80-120% of their size, individually per axis
            # translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)}, # translate by -20 to +20 percent (per axis)
            # rotate=(-5, 5), # rotate by -45 to +45 degrees
            # shear=(-5, 5), # shear by -16 to +16 degrees
            # order=[0, 1], # use nearest neighbour or bilinear interpolation (fast)
            # cval=(0, 255), # if mode is constant, use a cval between 0 and 255
            # mode=ia.ALL # use any of scikit-image's warping modes (see 2nd image from the top for examples)
        )),
        # execute 0 to 5 of the following (less important) augmenters per image
        # don't execute all of them, as that would often be way too strong
        iaa.SomeOf((0, 5),
                   [
                       # sometimes(iaa.Superpixels(p_replace=(0, 1.0), n_segments=(20, 200))), # convert images into their superpixel representation
                       iaa.OneOf([
                           iaa.GaussianBlur((0, 0.5)),  # blur images with a sigma between 0 and 3.0
                           iaa.AverageBlur(k=(2, 3)),  # blur image using local means with kernel sizes between 2 and 3
                           iaa.MedianBlur(k=(3, 5)),
                           # blur image using local medians with kernel sizes between 2 and 7
                       ]),
                       iaa.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)),  # sharpen images
                       # iaa.Emboss(alpha=(0, 1.0), strength=(0, 2.0)), # emboss images
                       # search either for all edges or for directed edges
                       # sometimes(iaa.OneOf([
                       #    iaa.EdgeDetect(alpha=(0, 0.7)),
                       #    iaa.DirectedEdgeDetect(alpha=(0, 0.7), direction=(0.0, 1.0)),
                       # ])),
                       iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
                       # add gaussian noise to images
                       iaa.OneOf([
                           iaa.Dropout((0.01, 0.1), per_channel=0.5),  # randomly remove up to 10% of the pixels
                           # iaa.CoarseDropout((0.03, 0.15), size_percent=(0.02, 0.05), per_channel=0.2),
                       ]),
                       # iaa.Invert(0.05, per_channel=True), # invert color channels
                       iaa.Add((-10, 10), per_channel=0.5),
                       # change brightness of images (by -10 to 10 of original value)
                       iaa.Multiply((0.5, 1.5), per_channel=0.5),
                       # change brightness of images (50-150% of original value)
                       iaa.ContrastNormalization((0.5, 2.0), per_channel=0.5),  # improve or worsen the contrast
                       # iaa.Grayscale(alpha=(0.0, 1.0)),
                       # sometimes(iaa.ElasticTransformation(alpha=(0.5, 3.5), sigma=0.25)), # move pixels locally around (with random strengths)
                       # sometimes(iaa.PiecewiseAffine(scale=(0.01, 0.05))) # sometimes move parts of the image around
                   ],
                   random_order=True
                   )
    ],
    random_order=True
)

if __name__ == '__main__':
    import random
    import os
    from config import image_h, image_w, test_image_folder, test_filelist_file
    import cv2 as cv

    test_path = test_image_folder
    with open(test_filelist_file, 'r') as file:
        lines = file.readlines()

    test_images = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            test_images.append(line)
    print('loaded {} test images'.format(len(test_images)))
    samples = random.sample(test_images, 10)

    for i, sample in enumerate(samples):
        image_name = sample
        filename = os.path.join(test_image_folder, image_name)
        image_bgr = cv.imread(filename)
        image_bgr = cv.resize(image_bgr, (image_h, image_w), cv.INTER_CUBIC)
        cv.imwrite('images/imgaug_before_{}.png'.format(i), image_bgr)
        image_bgr = aug_pipe.augment_image(image_bgr)
        cv.imwrite('images/imgaug_after_{}.png'.format(i), image_bgr)
