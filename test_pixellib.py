import pixellib
from pixellib.torchbackend.instance import instanceSegmentation

ins = instanceSegmentation()
# ins.load_model("pointrend_resnet50.pkl")
ins.load_model("pointrend_resnet50.pkl", confidence = 0.3)
# 감지 잘안될경우 confidence 줄이기
target_classes = ins.select_target_classes(person = True, car = True)
results, output = ins.segmentImage("1.jpg", segment_target_classes = target_classes, show_bboxes=True, output_image_name="result.jpg")

print(results["boxes"])
print(results["class_ids"])
print(results["class_names"])
