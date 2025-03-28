import numpy as np
import cv2

I = cv2.imread('china-original.png', cv2.IMREAD_GRAYSCALE)
I = I.astype(np.float32) / 255.0

noise_sigma = 0.05
noise_inc = .01
kernel_size = 3
kernel_size_inc = 2
flag = 'none'
sigma_color = .1
sigma_color_inc = .1
sigma_space = 15

while True:
    J = np.clip(I + np.random.randn(*I.shape) * noise_sigma, 0, 1)
    if flag == 'none':
        pass
    elif flag == 'box':
        J = cv2.blur(J, (kernel_size, kernel_size))
    elif flag == 'gus':
        g1d = cv2.getGaussianKernel(kernel_size, 0)
        J = cv2.filter2D(J, -1, g1d * g1d.T)
    elif flag == 'med':
        J = np.float32(cv2.medianBlur(np.uint8(255 * J), kernel_size)) / 255
    elif flag == 'bil':
        J = cv2.bilateralFilter(np.float32(J), kernel_size, sigma_color, sigma_space)
    cv2.imshow('Denoising Demo', J)
    key = cv2.waitKey(33) & 0xFF
    if key != 255:
        print(f'''
        noise_sigma : {noise_sigma}
        noise_inc : {noise_inc}
        kernel_size : {kernel_size}
        kernel_size_inc : {kernel_size_inc}
        flag : {flag}
        sigma_color : {sigma_color}
        sigma_color_inc : {sigma_color_inc}
        sigma_space : {sigma_space}
        ---------''')
    if key == ord('u'):
        noise_sigma += noise_inc
    elif key == ord('d'):
        if (new_noise := noise_sigma - noise_inc) >= 0:
            noise_sigma = new_noise
    elif key == ord('n'):
        flag = 'none'
    elif key == ord('b'):
        flag = 'box'
    elif key == ord('g'):
        flag = 'gus'
    elif key == ord('m'):
        flag = 'med'
    elif key == ord('l'):
        flag = 'bil'
    elif key == ord('+'):
        kernel_size += 2
    elif key == ord('-'):
        if (new_kernel_size := kernel_size - kernel_size_inc) >= 0:
            kernel_size = new_kernel_size
    elif key == ord('.'):
        sigma_color += .1
    elif key == ord(','):
        if (new_sigma_color := sigma_color - sigma_color_inc) >= 0:
            sigma_color = new_sigma_color
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
