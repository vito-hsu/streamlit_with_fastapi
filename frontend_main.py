# Today, I'll introduce how to build a streamlit with fastapi.
# In this project, I devided it into four parts.
# In frontend_main.py file, you'll see that built mainly by streamlit.
# In backend_main.py file, it is mainly built by fastapi.
# In backend_inference.py file, it is the main algorithm of this project.
# In this project, I'll give you a try, which makes your photo transfer its style and save these photos locally.
# Ok, let's go!!

# In this part, I'll give 5 key points about this project.
# The first thing, I'll introduce how the streamlit app work with fastapi. 
# The second thing is about the api parameters.
# The third thing is about how the algorithm(model) work in this project.
# The fourth thing is about the asynchronous design.
# The fifth key point is about the model files.
# Ok, it's all. Thx for your watching!!

# In the final (third) part, I'll check the performance difference between ASYNC DESIGN and SYNC DESIGN with fastapi.
# Let's check it out!

import requests
import streamlit as st
from PIL import Image
import time

st.set_page_config(layout = "wide")     # in streamlit app, the layout default setting is 'centered'


#########################################################################################################################################
# Because our project use a large amount of style-transfer models, which we won't design by ourselves.
# The fifth key is you must download these models first before you run the project.
STYLES = {                              # You should download the painting model from the following links one by one into models folder~~
    "candy": "candy",                   # https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/candy.t7
    "composition 6": "composition_vii", # https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/composition_vii.t7
    "feathers": "feathers",             # https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/feathers.t7
    "la_muse": "la_muse",               # https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/la_muse.t7
    "mosaic": "mosaic",                 # https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/mosaic.t7
    "starry night": "starry_night",     # https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/starry_night.t7
    "the scream": "the_scream",         # https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/the_scream.t7
    "the wave": "the_wave",             # https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/the_wave.t7
    "udnie": "udnie"                    # https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/instance_norm/udnie.t7
}
#########################################################################################################################################

st.title("Style transfer web app")
image       = st.file_uploader("Choose an image")                               
style       = st.selectbox("Choose the style", [i for i in STYLES.keys()])      # the 'first' parameter for the restapi url~~
user_width  = st.number_input('Input the width you want: ', value=640)          # the 'third' parameter for the restapi url~~


if st.button("Style Transfer"):
    start_time = time.time()
    if image is not None and style is not None:
        files               = {"file": image.getvalue()}                        # the 'second' parameter for the restapi url~~
        res                 = requests.post(                                    # request our restapi! this is the first key!
            f"http://127.0.0.1:8080/{style}/{user_width}",                      # and you must build this line with backend_main.py
            files = files                                                       # so let's see the backen_main.py
        )      
        img_path            = res.json()                                        # the third thing you should know is....           
        image               = Image.open(img_path.get("name"))                  # the main(core) idea of this project is to save processed
        st.image(image)                                                         # photos to local PC first and then open these photos
                                                                                # and show in our streamlit UI...
        displayed_styles    = [style]
        displayed           = 1
        total               = len(STYLES)

        st.write("Generating other models...")

        while displayed < total:
            for style in STYLES:
                if style not in displayed_styles:
                    try:
                        # st.write(f'Style Name : {style}')                           #  NOTICE. This line will cause bug in program....
                        path = f"{img_path.get('name').split('.')[0]}_{STYLES[style]}.jpg"
                        image = Image.open(path)
                        st.image(image)                                         # YOU CAN ADD WIDTH st.image(image, width=500)
                        time.sleep(1)                                           # add this line, and compare ASYNC and SYNC
                        displayed += 1
                        displayed_styles.append(style)
                    except:
                        pass
    
    end_time = time.time()
    st.text(f'Total Run Time :{end_time-start_time}s')


# And the second thing is to run streamlit server !!
# Ok!! Let's try it~~
# This part is for basic tutorial of this app~~
# The next video, I'll introduce the key codes of the project~~
# THX for your watching!!