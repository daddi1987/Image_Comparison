import cv2
import numpy as np

DEFAULT_TEMPLATE_MATCHING_THRESHOLD = 0.985



class Template:
    """
    A class defining a template
    """

    def __init__(self, image_path, label, color, matching_threshold=DEFAULT_TEMPLATE_MATCHING_THRESHOLD):

        self.image_path = image_path
        self.label = label
        self.color = color
        self.template = cv2.imread(image_path)
        self.template_height, self.template_width = self.template.shape[:2]
        self.matching_threshold = matching_threshold


image = cv2.imread(r"C:\Users\davide.zuanon\Desktop\TIP169.jpg")

templates = [
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample1.jpg", label="1", color=(0, 0, 255), matching_threshold=0.9884855),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample2.jpg", label="2", color=(255, 0, 255)),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample3.jpg", label="3", color=(0, 255, 255)),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample4.jpg", label="4", color=(150, 0, 255)),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample5.jpg", label="5", color=(0, 10, 255)),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample6.jpg", label="6", color=(64, 0, 255), matching_threshold=0.9884214),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample7.jpg", label="7", color=(0, 98, 255), matching_threshold=0.9982093),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample8.jpg", label="8", color=(0, 11, 255)),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample9.jpg", label="9", color=(15, 0, 255), matching_threshold=0.9879365),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample10.jpg", label="10", color=(0, 150, 255)),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample11.jpg", label="11", color=(98, 0, 255)),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample12.jpg", label="12", color=(65, 0, 255), matching_threshold=0.9962213),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample13.jpg", label="13", color=(0, 32, 255)),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample14.jpg", label="14", color=(82, 0, 255)),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample15.jpg", label="15", color=(0, 150, 255), matching_threshold=0.9875745),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample16.jpg", label="16", color=(120, 0, 255)),
    Template(image_path=r"C:\Users\davide.zuanon\OneDrive - INPECO SPA\TEST\xALQ\Tip Hopper\Tip Loader ALQ in Bulk\Training\Sample17.jpg", label="17", color=(11, 96, 255)),
]

detections = []

for template in templates:
    template_matching = cv2.matchTemplate(template.template, image, cv2.TM_CCOEFF_NORMED)

    match_locations = np.where(template_matching >= template.matching_threshold)

    for (x, y) in zip(match_locations[1], match_locations[0]):
        match = {
            "TOP_LEFT_X": x,
            "TOP_LEFT_Y": y,
            "BOTTOM_RIGHT_X": x + template.template_width,
            "BOTTOM_RIGHT_Y": y + template.template_height,
            "MATCH_VALUE": template_matching[y, x],
            "LABEL": template.label,
            "COLOR": template.color
        }

        detections.append(match)
image_with_detections = image.copy()

for detection in detections:
    cv2.rectangle(
        image_with_detections,
        (detection["TOP_LEFT_X"], detection["TOP_LEFT_Y"]),
        (detection["BOTTOM_RIGHT_X"], detection["BOTTOM_RIGHT_Y"]),
        detection["COLOR"],
        2,
    )
    cv2.putText(
        image_with_detections,
        f"{detection['LABEL']} - {detection['MATCH_VALUE']}",
        (detection["TOP_LEFT_X"] + 2, detection["TOP_LEFT_Y"] + 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        detection["COLOR"],
        1,
        cv2.LINE_AA,
    )
    NMS_THRESHOLD = 0.2

    print("Transhold: ", DEFAULT_TEMPLATE_MATCHING_THRESHOLD, " /", detection)
cv2.imshow("TEST", image)
cv2.waitKey(0)
cv2.imwrite("result.jpeg", image_with_detections)
#print("Transhold: ",DEFAULT_TEMPLATE_MATCHING_THRESHOLD, " /",detection['MATCH_VALUE'])
