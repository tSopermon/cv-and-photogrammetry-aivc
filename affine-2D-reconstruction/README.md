# Affine 2D Reconstruction

This project demonstrates affine rectification of a perspectively distorted image using vanishing points and lines. The main steps are:

1. **Select Points:** Double-click four points on the image to define two pairs of parallel lines.
2. **Compute Vanishing Points:** The code calculates vanishing points and the vanishing line from these lines.
3. **Affine Transformation:** An affine transformation matrix is constructed to rectify the image so that the vanishing line becomes [0, 0, 1].
4. **Image Reconstruction:** The image is transformed to remove perspective distortion, and results are visualized using matplotlib.

See `reconstr.py` for the implementation and `Brueghel.jpg` for the sample image. For more details, refer to the accompanying report `report.pdf`.
