import cv2


class SlideSolver:
    def __init__(self, bg, slide):
        self.bg = cv2.imdecode(bg, 0)
        self.slide = cv2.imdecode(slide, 0)

    def get_position(self):
        bg = self.__sobel_operator(self.bg)
        slide = self.__sobel_operator(self.slide)
        
        matched = cv2.matchTemplate(bg, slide, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(matched)
        
        return max_loc

    def __sobel_operator(self, img):
        scale = 1
        delta = 0
        ddepth = cv2.CV_16S

        img = cv2.GaussianBlur(img, (3, 3), 0)
        grad_x = cv2.Sobel(img, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(img, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
        
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return grad
