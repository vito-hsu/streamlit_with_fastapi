import backend_config
import cv2


def inference(model, image, user_height):
    user_height     = int(user_height)                              # int('640')
    model_name      = f"{backend_config.MODEL_PATH}{model}.t7"      # check downloaded model path
    model           = cv2.dnn.readNetFromTorch(model_name)          # load our downloaded models (.t7)
    height, width   = int(image.shape[0]), int(image.shape[1])
    new_width       = int((user_height / height) * width)
    resized_image   = cv2.resize(image, (new_width, user_height), interpolation=cv2.INTER_AREA)

    # Create our blob from the image
    # Then perform a forward pass run of the network
    # The Mean values for the ImageNet training set are R=103.93, G=116.77, B=123.68

    inp_blob = cv2.dnn.blobFromImage(
        resized_image,
        1.0,
        (new_width, user_height),
        (103.93, 116.77, 123.68),
        swapRB=False,
        crop=False,
    )

    model.setInput(inp_blob)
    output = model.forward()

    # Reshape the output Tensor,
    # add back the mean substruction,
    # re-order the channels
    output = output.reshape(3, output.shape[2], output.shape[3])
    output[0] += 103.93
    output[1] += 116.77
    output[2] += 123.68

    output = output.transpose(1, 2, 0)
    return output, resized_image