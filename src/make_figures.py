"""
Generate remade figures for the English report.

Replace the example CSVs in `data/` with your measured data and re-run this script.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "figures" / "remade"
OUT.mkdir(parents=True, exist_ok=True)

def save(fig, stem: str):
    fig.tight_layout()
    fig.savefig(OUT / f"{stem}.png", dpi=200)
    fig.savefig(OUT / f"{stem}.svg")
    plt.close(fig)

def fig1_measurement_bench_schematic():
    fig = plt.figure(figsize=(9, 2.2))
    ax = fig.add_subplot(111)
    ax.axis("off")

    def box(x, y, w, h, text):
        rect = Rectangle((x, y), w, h, fill=False, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=10)

    box(0.02, 0.35, 0.18, 0.3, "Light source")
    box(0.26, 0.35, 0.18, 0.3, "Monochromator")
    box(0.50, 0.35, 0.18, 0.3, "Integrating\nsphere")
    box(0.74, 0.35, 0.22, 0.3, "Sensor under test\n(camera)")

    for (x1, y1, x2, y2) in [(0.20, 0.50, 0.26, 0.50),
                            (0.44, 0.50, 0.50, 0.50),
                            (0.68, 0.50, 0.74, 0.50)]:
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle="->", mutation_scale=12,
                                     linewidth=1.5))

    box(0.52, 0.05, 0.18, 0.22, "Calibrated\ndetector")
    ax.add_patch(FancyArrowPatch((0.59, 0.35), (0.59, 0.27),
                                 arrowstyle="->", mutation_scale=12,
                                 linewidth=1.2))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    save(fig, "fig1_measurement_bench_schematic")

def fig2_second_order_interference_concept():
    fig = plt.figure(figsize=(7, 3.6))
    ax = fig.add_subplot(111)
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Relative intensity (arb.)")
    ax.set_title("Second-order diffraction/interference (conceptual)")

    peaks1 = [(450, 1.0, "Blue (1st)"),
              (550, 1.0, "Green (1st)"),
              (650, 1.0, "Red (1st)")]
    for mu, amp, label in peaks1:
        x = np.linspace(mu - 40, mu + 40, 200)
        y = amp * np.exp(-0.5 * ((x - mu) / 12) ** 2)
        ax.plot(x, y, label=label)

    # Conceptual second-order peaks (dashed), shifted to longer wavelengths
    peaks2 = [(900, 0.35, "Blue (2nd)"),
              (1100, 0.35, "Green (2nd)"),
              (1300, 0.35, "Red (2nd)")]
    for mu, amp, label in peaks2:
        x = np.linspace(mu - 60, mu + 60, 200)
        y = amp * np.exp(-0.5 * ((x - mu) / 18) ** 2)
        ax.plot(x, y, linestyle="--", label=label)

    ax.set_xlim(380, 1400)
    ax.legend(fontsize=7, ncol=3, frameon=False)
    save(fig, "fig2_second_order_interference_concept")

def fig3_histogram_example(seed: int = 0):
    rng = np.random.default_rng(seed)
    pixels = np.clip(rng.normal(loc=128, scale=30, size=20000), 0, 255)

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.hist(pixels, bins=50)
    ax.set_xlabel("Pixel value (8-bit)")
    ax.set_ylabel("Count")
    ax.set_title("Typical image histogram (example)")
    save(fig, "fig3_histogram")

def fig4_power_vs_wavelength():
    df = pd.read_csv(DATA / "spectral_power_detector_example.csv")

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.plot(df["wavelength_nm"], df["power_W"], marker="o")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Power (W)")
    ax.set_title("Spectral power at integrating sphere output")
    save(fig, "fig4_power_vs_wavelength")

def fig5_camera_response():
    df = pd.read_csv(DATA / "spectral_camera_response_example.csv")

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.plot(df["wavelength_nm"], df["camera_response_arb"], marker="o")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Spectral response (arb. units)")
    ax.set_title("Camera spectral response")
    save(fig, "fig5_camera_response")

def fig6_temporal_noise_example(seed: int = 0):
    rng = np.random.default_rng(seed)
    t = np.arange(0, 100)
    pixel = 250 + rng.normal(0, 4, size=len(t)) + 2*np.sin(2*np.pi*t/30)

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)
    ax.plot(t, pixel)
    ax.set_xlabel("Frame index (time)")
    ax.set_ylabel("Pixel value (DN)")
    ax.set_title("Temporal noise: one pixel over time (example)")
    save(fig, "fig6_temporal_noise")

def fig7_spatial_noise_example(seed: int = 0):
    rng = np.random.default_rng(seed)
    H, W = 120, 220
    yy, xx = np.mgrid[0:H, 0:W]

    avg_img = 210 + 40*np.exp(-((xx - W*0.45)**2 + (yy - H*0.40)**2) / (2*(0.35*min(H, W))**2))
    fpn = rng.normal(0, 1.2, size=(H, W)) + (rng.random((H, W)) - 0.5)*0.6
    ref_img = avg_img + fpn + rng.normal(0, 0.8, size=(H, W))
    fpn_est = ref_img - avg_img

    fig = plt.figure(figsize=(8, 3))
    ax1 = fig.add_subplot(1, 2, 1)
    im1 = ax1.imshow(avg_img, cmap="gray")
    ax1.set_title("Average image (example)")
    ax1.axis("off")
    fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.02)

    ax2 = fig.add_subplot(1, 2, 2)
    im2 = ax2.imshow(fpn_est, cmap="gray")
    ax2.set_title("Fixed-pattern noise (example)")
    ax2.axis("off")
    fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.02)

    fig.tight_layout()
    fig.savefig(OUT / "fig7_spatial_noise.png", dpi=200)
    plt.close(fig)

def fig8_average_3d_example(seed: int = 0):
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    rng = np.random.default_rng(seed)
    H, W = 120, 220
    yy, xx = np.mgrid[0:H, 0:W]
    avg_img = 210 + 40*np.exp(-((xx - W*0.45)**2 + (yy - H*0.40)**2) / (2*(0.35*min(H, W))**2))

    X, Y = np.meshgrid(np.linspace(0, 1, W), np.linspace(0, 1, H))
    Z = avg_img

    fig = plt.figure(figsize=(6, 4.5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, rstride=2, cstride=2, linewidth=0, antialiased=True)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("Intensity (DN)")
    ax.set_title("3D view of the average image (example)")
    fig.tight_layout()
    fig.savefig(OUT / "fig8_average_3d.png", dpi=200)
    plt.close(fig)

def main():
    fig1_measurement_bench_schematic()
    fig2_second_order_interference_concept()
    fig3_histogram_example()
    fig4_power_vs_wavelength()
    fig5_camera_response()
    fig6_temporal_noise_example()
    fig7_spatial_noise_example()
    fig8_average_3d_example()

if __name__ == "__main__":
    main()
