from imutils.perspective import four_point_transform
import pytesseract
import imutils
import cv2
import re
from PIL import Image
import io
import base64

def scan_image(image_path):
	imageArr = []
	orig = cv2.imread(image_path)
	image = orig.copy()
	image = imutils.resize(image, width=500)
	ratio = orig.shape[1] / float(image.shape[1])

	# convert the image to grayscale, blur it slightly, and then apply
	# edge detection
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
	edged = cv2.Canny(blurred, 75, 200)

	# cv2.imshow("Input", image)
	# cv2.imshow("Edged", edged)
	imageArr.append(get_image(image))
	imageArr.append(get_image(edged))
	# cv2.waitKey(0)

	# find contours in the edge map and sort them by size in descending
	# order
	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

	# initialize a contour that corresponds to the receipt outline
	receiptCnt = None
	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if our approximated contour has four points, then we can
		# assume we have found the outline of the receipt
		if len(approx) == 4:
			receiptCnt = approx
			break
	# if the receipt contour is empty then our script could not find the
	# outline and we should be notified
	if receiptCnt is None:
		raise Exception(("Could not find receipt outline. "
			"Try debugging your edge detection and contour steps."))

	output = image.copy()
	cv2.drawContours(output, [receiptCnt], -1, (0, 255, 0), 2)
	# cv2.imshow("Receipt Outline", output)
	imageArr.append(get_image(output))
	# cv2.waitKey(0)
	# apply a four-point perspective transform to the *original* image to
	# obtain a top-down bird's-eye view of the receipt
	receipt = four_point_transform(orig, receiptCnt.reshape(4, 2) * ratio)
	# show transformed image
	# cv2.imshow("Receipt Transform", imutils.resize(receipt, width=500))
	# cv2.waitKey(0)
	# imageArr.append(get_image(imutils.resize(receipt, width=500)))
	imageArr.append(get_image(receipt))


	# apply OCR to the receipt image by assuming column data, ensuring
	# the text is *concatenated across the row* (additionally, for your
	# own images you may need to apply additional processing to cleanup
	# the image, including resizing, thresholding, etc.)
	options = "--psm 4"
	text = pytesseract.image_to_string(
		cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB),
		config=options)
	# show the raw output of the OCR process
	print("[INFO] raw output:")
	print("==================")
	print(text)
	print("\n")

	# define a regular expression that will match line items that include
	# a price component
	pricePattern = r'([0-9]+\.[0-9]+)'
	# show the output of filtering out *only* the line items in the
	# receipt
	print("[INFO] price line items:")
	print("========================")
	# loop over each of the line items in the OCR'd receipt
	for row in text.split("\n"):
		# check to see if the price regular expression matches the current
		# row
		if re.search(pricePattern, row) is not None:
			print(row)

	return text, imageArr

# Function to generate different images based on an identifier
def get_image(image):
	image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	# Convert the image to a PIL Image
	pil_img = Image.fromarray(image_rgb)

	# Save the image to a BytesIO object (in-memory)
	img_io = io.BytesIO()
	pil_img.save(img_io, 'PNG')
	img_io.seek(0)

	# Encode the image as base64
	img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

	return img_base64


