import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', 'best.pt')
model.conf = 0.45   
model.agnostic = True    
model.iou = 0.2                                               
# Images
img = 'ssr.jpg'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)


# Results
# results.show()  # or .show(), .save(), .crop(), .pandas(), etc.
results.show(labels=False)
print(results.pandas().xyxy[0])
pandasbox=len(results.pandas().xyxy[0]) 
print("number: "+str(pandasbox))