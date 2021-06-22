import numpy as np
import cv2
import imutils


class ImageRestore:
    def __init__(self):
        self.template = cv2.imread('images/template.jpg')
        self.template = cv2.resize(self.template, dsize=(1300, 1300), interpolation=cv2.INTER_AREA)
        self.crop_template = self.crop_images(self.template)

    def restore_image(self, imageName):
        self.image = cv2.imread(imageName)
        self.image = cv2.resize(self.image, dsize=(1300, 1300), interpolation=cv2.INTER_AREA)
        self.crop_image = self.crop_images(self.image)
        self.aligned = self.align_images(self.crop_image, self.crop_template, debug=True)

        #cv2.imshow('asd',self.aligned)
        #cv2.waitKey(0)
        return self.aligned
        # crop_image = rotate_images(crop_image)



    def align_images(self, image, template, maxFeatures=500, keepPercent=0.2, debug=False):
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # cv2.imshow('grey', imageGray)
        # cv2.waitKey(0)
        #
        # cv2.imshow('grey', templateGray)
        # cv2.waitKey(0)

        orb = cv2.ORB_create(maxFeatures)
        (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
        (kpsB, descsB) = orb.detectAndCompute(templateGray, None)

        method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
        matcher = cv2.DescriptorMatcher_create(method)
        matches = matcher.match(descsA, descsB, None)

        matches = sorted(matches, key=lambda x: x.distance)

        keep = int(len(matches) * keepPercent)
        matches = matches[:keep]

        if debug:
            matchedVis = cv2.drawMatches(image, kpsA, template, kpsB,
                                         matches, None)
            matchedVis = imutils.resize(matchedVis, width=700)
            #cv2.imshow("Matched Keypoints", matchedVis)
            #cv2.waitKey(0)

            ptsA = np.zeros((len(matches), 2), dtype="float")
            ptsB = np.zeros((len(matches), 2), dtype="float")

            for (i, m) in enumerate(matches):
                ptsA[i] = kpsA[m.queryIdx].pt
                ptsB[i] = kpsB[m.trainIdx].pt

            (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
            (h, w) = template.shape[:2]
            aligned = cv2.warpPerspective(image, H, (w, h))

            return aligned

    def crop_images(self, image):
        original = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (25, 25), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # Perform morph operations, first open to remove noise, then close to combine
        noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, noise_kernel, iterations=2)
        close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=3)
        # Find enclosing boundingbox and crop ROI
        coords = cv2.findNonZero(close)
        x, y, w, h = cv2.boundingRect(coords)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        crop = original[y:y + h, x:x + w]
        # cv2.imshow('thresh', thresh)
        # cv2.imshow('close', close)
        # cv2.imshow('image', image)
        #cv2.imshow('crop', crop)
        #cv2.waitKey()
        return crop

    def rotate_images(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)

        thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        coords = np.column_stack(np.where(thresh > 0))
        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = - angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        # show the output image
        print("[INFO] angle: {:.3f}".format(angle))
        cv2.imshow("Rotated", rotated)
        cv2.waitKey(0)
        return rotated


# def align_images(image, template, maxFeatures=500, keepPercent=0.2, debug=False):
#     imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
#
#     # cv2.imshow('grey', imageGray)
#     # cv2.waitKey(0)
#     #
#     # cv2.imshow('grey', templateGray)
#     # cv2.waitKey(0)
#
#     orb = cv2.ORB_create(maxFeatures)
#     (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
#     (kpsB, descsB) = orb.detectAndCompute(templateGray, None)
#
#     method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
#     matcher = cv2.DescriptorMatcher_create(method)
#     matches = matcher.match(descsA, descsB, None)
#
#     matches = sorted(matches, key=lambda x: x.distance)
#
#     keep = int(len(matches) * keepPercent)
#     matches = matches[:keep]
#
#     if debug:
#         matchedVis = cv2.drawMatches(image, kpsA, template, kpsB,
#                                      matches, None)
#         matchedVis = imutils.resize(matchedVis, width=1000)
#         cv2.imshow("Matched Keypoints", matchedVis)
#         cv2.waitKey(0)
#
#         ptsA = np.zeros((len(matches), 2), dtype="float")
#         ptsB = np.zeros((len(matches), 2), dtype="float")
#
#         for (i, m) in enumerate(matches):
#             ptsA[i] = kpsA[m.queryIdx].pt
#             ptsB[i] = kpsB[m.trainIdx].pt
#
#         (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
#         (h, w) = template.shape[:2]
#         aligned = cv2.warpPerspective(image, H, (w, h))
#
#         return aligned
#
#
# def crop_images(image):
#     original = image.copy()
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (25, 25), 0)
#     thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#     # Perform morph operations, first open to remove noise, then close to combine
#     noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
#     opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, noise_kernel, iterations=2)
#     close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
#     close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=3)
#     # Find enclosing boundingbox and crop ROI
#     coords = cv2.findNonZero(close)
#     x, y, w, h = cv2.boundingRect(coords)
#     cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
#     crop = original[y:y + h, x:x + w]
#     # cv2.imshow('thresh', thresh)
#     # cv2.imshow('close', close)
#     # cv2.imshow('image', image)
#     cv2.imshow('crop', crop)
#     cv2.waitKey()
#     return crop
#
#
# def rotate_images(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.bitwise_not(gray)
#
#     thresh = cv2.threshold(gray, 0, 255,
#                            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#     coords = np.column_stack(np.where(thresh > 0))
#     angle = cv2.minAreaRect(coords)[-1]
#
#     if angle < -45:
#         angle = -(90 + angle)
#     else:
#         angle = - angle
#     (h, w) = image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(image, M, (w, h),
#                              flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
#     cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
#                 (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#     # show the output image
#     print("[INFO] angle: {:.3f}".format(angle))
#     cv2.imshow("Rotated", rotated)
#     cv2.waitKey(0)
#     return rotated


# if __name__ == '__main__':
#     print('Start')
#     image = cv2.imread('image/7.jpg')
#     template = cv2.imread('image/template.jpg')
#     print(image.shape, template.shape)
#     image = cv2.resize(image, dsize=(1300, 1300), interpolation=cv2.INTER_AREA)
#     template = cv2.resize(template, dsize=(1300, 1300), interpolation=cv2.INTER_AREA)
#
#     print(image.shape)
#     crop_image = crop_images(image)
#     # crop_image = rotate_images(crop_image)
#
#     crop_template = crop_images(template)
#
#     aligned = align_images(crop_image, crop_template, debug=True)
#
#     aligned = imutils.resize(aligned, width=700)
#     crop_template = imutils.resize(crop_template, width=700)
#
#     stacked = np.hstack([aligned, crop_template])
#
#     overlay = crop_template.copy()
#     output = aligned.copy()
#     cv2.addWeighted(overlay, 0.5, output, 0.5, 0, output)
#
#     cv2.imshow("Image Alignment Stacked", stacked)
#     cv2.imshow("Image Alignment Overlay", output)
#     cv2.waitKey(0)

#
