from pathlib import Path

from matplotlib.pyplot import figure

import numpy as np


# %matplotlib inline


def coeffs(N):
    return np.random.rand(N) - 0.5


# +
def flattop(t, t_start, t_stop, t_rise, t_fall=None):
    if t_fall is None:
        t_fall = t_rise
    return _flattop_blackman(t, t_start, t_stop, t_rise, t_fall)


@np.vectorize
def _flattop_blackman(t, t_start, t_stop, t_rise, t_fall):
    if t_start <= t <= t_stop:
        f = 1.0
        if t <= t_start + t_rise:
            f = blackman(t, t_start, t_start + 2 * t_rise)
        elif t >= t_stop - t_fall:
            f = blackman(t, t_stop - 2 * t_fall, t_stop)
        return f
    else:
        return 0.0


def box(t, t_start, t_stop):
    """Box-shape (Theta-function)

    The shape is 0 before `t_start` and after `t_stop` and 1 elsewhere.

    Args:
        t (float): Time point or time grid
        t_start (float): First value of `t` for which the box has value 1
        t_stop (float): Last value of `t` for which the box has value 1

    Note:
        You may use :class:`numpy.vectorize`, :func:`functools.partial`, or
        :func:`qutip_callback`, cf.  :func:`flattop`.
    """
    if t < t_start:
        return 0.0
    if t > t_stop:
        return 0.0
    return 1.0


def blackman(t, t_start, t_stop, a=0.16):
    T = t_stop - t_start
    box_vec = np.vectorize(box)
    return (
        0.5
        * box_vec(t, t_start, t_stop)
        * (
            1.0
            - a
            - np.cos(2.0 * np.pi * (t - t_start) / T)
            + a * np.cos(4.0 * np.pi * (t - t_start) / T)
        )
    )


# -


def random_curve(x, coeffs):
    y = np.zeros(len(x))
    X = x[-1]
    for (n, a_n) in enumerate(coeffs):
        y += (np.sin(a_n * x)) ** 2
    return y * flattop(x, 0, X, 0.1 * X)


def control_onto_interval(y):
    res = np.zeros(len(y) - 1)
    for i in range(len(y) - 1):
        res[i] = 0.5 * (y[i] + y[i + 1])
    return res


def plot(
    outfile,
    show_curve=True,
    show_simple=False,
    show_points=False,
    show_bars=False,
):

    fig_width = 6.0  # Total width of figure canvas [cm]
    fig_height = 3.25  # Total height of figure canvas [cm]
    left_margin = 0.5  # Left canvas edge -> plots [cm]
    bottom_margin = 0.5  # Bottom canvas edge -> plots [cm]
    right_margin = 0.0  # Right canvas edge -> plots [cm]
    top_margin = 0.0  # Top canvas edge -> plots
    dpi = 300
    cm2inch = 0.39370079  # conversion factor cm to inch
    w = fig_width - (left_margin + right_margin)  # width of plot (cm)
    h = fig_height - (bottom_margin + top_margin)  # height of plot (cm)

    a_n = coeffs(5)
    a_n = np.array(
        [0.4976899, -0.37860223, -0.18034831, 0.17856751, -0.25214567]
    )

    x = np.linspace(0, 40, 100)
    y = random_curve(x, a_n)

    # fmt: off
    y_simple = (
        2.4 * blackman(x, 0, 18, a=0.16)
        + 3.6 * blackman(x, 23, 40, a=0.16)
    )
    # fmt: on

    x_points = np.linspace(0, 40, 20)
    y_points = random_curve(x_points, a_n)
    intervals = control_onto_interval(random_curve(x_points, a_n))

    fig = figure(figsize=(fig_width * cm2inch, fig_height * cm2inch), dpi=dpi)
    pos = [
        left_margin / fig_width,
        bottom_margin / fig_height,
        w / fig_width,
        h / fig_height,
    ]
    ax = fig.add_axes(pos)

    if show_simple:
        ax.plot(x, y_simple, color='black')
    if show_curve:
        ax.plot(x, y, color='black')
    if show_points:
        ax.plot(x_points, y_points, 'o')
    if show_bars:
        ax.bar(
            x_points[:-1],
            intervals,
            align='edge',
            width=x_points[1],
            alpha=0.5,
            linewidth=1,
            edgecolor='black',
        )
    ax.axis('off')

    padax = 2  # pt
    padlbl = 6  # pt

    x0 = np.min(x)
    x1 = np.max(x)
    Δx = x1 - x0
    padx = 0.03 * Δx
    y0 = np.min(y)
    y1 = np.max(y)
    Δy = y1 - y0
    pady = 0.03 * Δy * (w / h)
    ax.set_xlim(x0 - padx, x1 + padx)
    ax.set_ylim(y0 - pady, y1 + pady)

    ax.annotate(
        '',
        xy=(0, -padax),
        xycoords=('axes fraction', 'axes points'),
        xytext=(1, -padax),
        textcoords=('axes fraction', 'axes points'),
        arrowprops=dict(arrowstyle="<-", color='black'),
    )
    ax.annotate(
        'time',
        xy=(0.5, 0),
        xycoords='axes fraction',
        xytext=(0, -(padax + padlbl)),
        textcoords='offset points',
    )

    ax.annotate(
        '',
        xy=(-padax, 0),
        xycoords=('axes points', 'axes fraction'),
        xytext=(-padax, 1),
        textcoords=('axes points', 'axes fraction'),
        arrowprops=dict(arrowstyle="<-", color='black'),
    )
    ax.annotate(
        'control amplitude',
        xy=(0, 0.5),
        xycoords='axes fraction',
        xytext=(-(padax + padlbl), 0),
        textcoords='offset points',
        rotation=90,
        va='center',
    )

    ext = Path(outfile).suffix[1:]
    fig.savefig(outfile, format=ext, dpi=dpi)


def main():
    fileroot = str(Path(__file__).with_suffix(''))
    plot(
        show_curve=True,
        show_points=False,
        show_bars=False,
        outfile=(fileroot + '_continuous.pdf'),
    )
    plot(
        show_curve=True,
        show_points=True,
        show_bars=False,
        outfile=(fileroot + '_discrete.pdf'),
    )
    plot(
        show_curve=True,
        show_points=False,
        show_bars=True,
        outfile=(fileroot + '_pwc.pdf'),
    )
    plot(
        show_simple=True,
        show_curve=False,
        show_points=False,
        show_bars=False,
        outfile=(fileroot + '_simple.pdf'),
    )


if __name__ == "__main__":
    main()
