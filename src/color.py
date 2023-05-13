import scipy.optimize as opt
import numpy as np
import skimage.color as skc


def _circular_diff(a: float, b: float, interval: float = 1):
    return min(abs(a - b), abs(a - b - interval), abs(a - b + interval))


def _cmyk2rgb(cmyk: np.ndarray[float]):
    return (1 - cmyk[:3]) * (1 - cmyk[3])


def cmyk2rgb(cmyk: tuple[float]) -> tuple[int, int, int]:
    return tuple(int(x * 255) for x in _cmyk2rgb(np.array(cmyk)))


def cmyk2lab(cmyk: np.ndarray[float]):
    return skc.rgb2lab(_cmyk2rgb(cmyk))


def total_ink(cmyk: np.ndarray[float]):
    return np.sum(cmyk)


def cmyk_to_hsv(cmyk: np.ndarray[float]):
    return skc.rgb2hsv(_cmyk2rgb(cmyk))


def minimize_ink(my_cmyk: np.ndarray[float], max_lab_dist: float, max_hue_diff: float = 0.1):
    """
    minimize total ink while keeping the color difference between `my_cmyk` and result smaller than `max_lab_dist`
    """
    my_cmyk = np.array(my_cmyk)
    my_hue = cmyk_to_hsv(my_cmyk)[0]
    my_lab = cmyk2lab(my_cmyk)

    def lab_diff(cmyk: np.ndarray[float]):
        return np.linalg.norm(my_lab - cmyk2lab(cmyk))

    def hue_diff(cmyk: np.ndarray[float]):
        return _circular_diff(my_hue, cmyk_to_hsv(cmyk)[0])

    # max_lab_dist >= lab_diff(cmyk)
    lab_constraint = {
        'type': 'ineq',
        'fun': lambda cmyk: max_lab_dist - lab_diff(cmyk)
    }
    hue_constraint = {
        'type': 'ineq',
        'fun': lambda cmyk: max_hue_diff - hue_diff(cmyk)
    }

    res = opt.minimize(
        fun=total_ink,
        x0=my_cmyk.copy(),
        constraints=[lab_constraint, hue_constraint],
        bounds=[(0, 1)] * 4,
    )
    return res.x


if __name__ == "__main__":
    cmyk = np.array([0.1, 0.2, 0.3, 0.4])
    ink_before_minimize = total_ink(cmyk)
    out = minimize_ink(cmyk, 10)
    ink_after_minimize = total_ink(out)

    print(f'ink: {ink_before_minimize} -> {ink_after_minimize}')
    print(
        cmyk, '->', [float(x) for x in out],
    )
