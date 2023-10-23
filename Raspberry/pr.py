from roboflow import Roboflow
rf = Roboflow(api_key="9TwZaDpIJ3gnWQ0inEaH")
project = rf.workspace().project("plant-size-zrqp4")
model = project.version(2).model

predict = model.predict("WIN_20231018_16_21_30_Pro.jpg",
                        confidence=40, overlap=30).json()
# infer on a local image
print(predict)

print(predict['predictions'][0]['height'])
print(predict['predictions'][0]['width'])
