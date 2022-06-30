import uuid, uvicorn
from fastapi import File, FastAPI, UploadFile
import numpy as np
from PIL import Image
import backend_config
import backend_inference
import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import time
import cv2


# But in this video, I hope you know the design first.
# You can see, process_image function is in the generate_remaining_models function
# And you can guess if we just run process_image function, it should run normally too
# So, it is the fourth key point I think you should know in the project~~

#######################         asynchronous design          #########################
async def generate_remaining_models(models, image, name: str, user_height):
    await asyncio.get_event_loop().run_in_executor(
        ProcessPoolExecutor(), partial(process_image, models, image, name, user_height)
    )
######################################################################################



def process_image(models, image, name: str, user_height):
    for model in models:
        output, resized = backend_inference.inference(models[model], image, user_height)
        name            = name.split(".")[0]
        name            = f"{name.split('_')[0]}_{models[model]}.jpg"        
        cv2.imwrite(name, output)




app = FastAPI()                                             # In the backend_main.py, it's just a normal fastapi py file
                                                            # so, if you don't know how to use fastapi package
                                                            # I suggest you checking this first~

                                                            # the second key point about this project is that
                                                            # you must know how many parameters in this api~
                                                            # in this project, we have three parameters
@app.post("/{style}/{user_height}")                         # If you want to request this restapi, you should give the following parameters: 
async def get_image(style: str, user_height, file: UploadFile = File(...)):             # 'style', 'file', 'user_height'
    image           = np.array(Image.open(file.file))                           
    model           = backend_config.STYLES[style]
    start           = time.time()
    output, resized = backend_inference.inference(model, image, user_height)            # main(core) algorithm in this project~
    name            = f"storage/{str(uuid.uuid4())}.jpg"                                # saving location(path)
    cv2.imwrite(name, output)                                                           # imwrite for saving our output photos
    models          = backend_config.STYLES.copy()                                      # for remaining models
    del models[style]                                                                   # you can compare the following two designs
    # First, I try with Asynchronous Design. about 17 seconds
    # Secondly, try Synchronous Design. about 13 seconds
    # Let's try again
    # Ok~ Next, we do something~ Synchronous Design about 21 seconds, Asynchronous Design still about 17 seconds..
    # That's all. THX for watching this video~~
    # process_image(models, image, name, user_height)                                     # Synchronous Design,  you can manually adjust here
    asyncio.create_task(generate_remaining_models(models, image, name, user_height))    # Asynchronous Design, you can manually adjust here
    return {"name": name, "time": time.time() - start}                                     



@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}



if __name__ == "__main__":
    uvicorn.run("backend_main:app", host="127.0.0.1", port=8080)


# To show this project, the first thing you should do is run fastapi server
# Rerun this py first!!
# OK!!!