import matplotlib.pyplot as plt
import cv2


if __name__ == "__main__":
    img = cv2.cvtColor(
        cv2.imread("seam_carving/samples/sky_planes.jpeg"), cv2.COLOR_BGR2RGB
    )
    plt.figure(figsize=(7, 7))
    plt.imshow(img)
    plt.show()
