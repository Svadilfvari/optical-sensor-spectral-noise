# Optical Sensor Characterization: Spectral Response & Noise

**Recommended GitHub repository name:** `optical-sensor-spectral-noise`

This repository is a self-contained, article-style guide (in **English**) to measuring an image sensor’s **spectral response** and **noise** (temporal + spatial / fixed-pattern). It also includes reproducible scripts and figures so you can adapt the workflow to many CMOS/CCD-style detectors.

- Full write-up: **[`report/REPORT_EN.md`](report/REPORT_EN.md)**
- Original reference (French PDF): **[`report/original_report_fr.pdf`](report/original_report_fr.pdf)**
- Figures:
  - extracted from the PDF: `figures/original/`
  - redrawn, clean versions: `figures/remade/`

---

## Table of contents

1. [Why spectral response and noise matter](#why-spectral-response-and-noise-matter)  
2. [Background: how image sensors form a signal](#background-how-image-sensors-form-a-signal)  
3. [Experimental setup](#experimental-setup)  
4. [From calibrated photodiode to optical power](#from-calibrated-photodiode-to-optical-power)  
5. [Estimating the camera spectral response](#estimating-the-camera-spectral-response)  
6. [Noise: temporal vs spatial](#noise-temporal-vs-spatial)  
7. [Reproducibility](#reproducibility)  
8. [Suggested citation](#suggested-citation)

---

## Why spectral response and noise matter

Two cameras can look “similar” yet behave very differently in practice:

- **Spectral response** determines *which wavelengths* are converted efficiently into electrons (and therefore into pixel values).  
  This affects color rendering, sensitivity under LEDs vs sunlight, and near‑IR leakage.
- **Noise** determines how reliably small signals are measured (low light, high frame rate, scientific imaging).  
  Noise also limits resolution after processing (denoising, HDR merging, calibration, etc.).

In this lab, we probe both with a controlled light source and repeated image captures.

---

## Background: how image sensors form a signal

### Photons → electrons → digital numbers

At a high level:

1. Light at wavelength **λ** delivers photons to a pixel.
2. The silicon photodiode in the pixel converts a fraction into photoelectrons.  
   That fraction is often summarized by the **quantum efficiency** `QE(λ)`.
3. Electrons are integrated over the exposure time, then converted to a voltage, amplified, and digitized
   to a pixel value (often called **DN** for “digital number”).

A very simplified relation is:

\[
\text{DN} \;\propto\; G \cdot QE(\lambda) \cdot N_{\gamma}(\lambda) \; + \; \text{offset} \; + \; \text{noise}
\]

where `G` is the camera gain chain, and `Nγ` is the number of incident photons during the exposure.

### CMOS vs CCD (conceptual)

- **CCD:** charges are shifted across the chip to a readout node → historically very uniform, but requires specialized readout.
- **CMOS:** each pixel has its own readout circuitry (amplifier/switching) → flexible, low power, widely used; can have stronger fixed-pattern components if uncorrected.

### Color sensors (Bayer) vs monochrome sensors

A **color** sensor typically has a *Bayer filter array* (R/G/B filters) and often an **IR-cut** filter.  
A **monochrome** sensor has no CFA, so each pixel measures intensity over the full spectral band.

This repository treats the camera response as a *single response curve* (typical when measuring a monochrome channel
or a grayscale-converted signal).

---

## Experimental setup

We use a monochromator-based bench to sweep wavelength and illuminate the sensor under test (SUT).

![Measurement bench overview](figures/remade/fig1_measurement_bench_schematic.png)

*Figure 1 — Typical measurement chain: broadband source → monochromator → integrating sphere → sensor under test.  
A calibrated detector measures the sphere output so we can convert camera readings into a wavelength‑dependent response.*

### Why an integrating sphere?

An integrating sphere helps make illumination **uniform** and **stable** across the sensor field by multiple diffuse reflections.
That’s crucial when we later interpret **spatial** patterns as *sensor behavior* rather than illumination artifacts.

### A practical pitfall: second-order diffraction / stray light

Monochromators can leak light from other diffraction orders.  
A classic example: light at \( \lambda/2 \) (2nd order) can contaminate the measurement at \( \lambda \),
especially at longer wavelengths where the source is strong and the monochromator/grating efficiency changes.

![Second-order concept](figures/remade/fig2_second_order_interference_concept.png)

*Figure 2 — Conceptual illustration: a “red” setting can receive contamination from a second-order “blue/green” component.
In real benches, order-sorting filters and careful calibration reduce this effect.*

---

## From calibrated photodiode to optical power

To interpret the camera response, we want to know how much light the sphere delivers at each wavelength.

A **calibrated photodiode** provides a traceable conversion from incident optical power to photocurrent via its
**spectral responsivity** \( S(\lambda) \) (A/W):

\[
I(\lambda) = S(\lambda) \cdot P(\lambda)
\quad\Rightarrow\quad
P(\lambda) = \frac{I(\lambda)}{S(\lambda)}
\]

In practice, the lab provides `S(λ)` (from calibration data) and we measure current `I(λ)`.

This repo includes an *example* power-vs-wavelength curve:

![Spectral power example](figures/remade/fig4_power_vs_wavelength.png)

*Figure 3 — Example of the optical power measured at the integrating sphere output versus wavelength.*

---

## Estimating the camera spectral response

### What we compute

A common approach is to compute a **relative spectral response**:

\[
R_{\text{cam}}(\lambda) \;\propto\; \frac{\text{DN}(\lambda) - \text{DN}_{\text{dark}}}{P(\lambda)}
\]

- `DN(λ)` is the mean pixel value measured under monochromatic illumination.
- `DN_dark` is the mean value with the light blocked (offset + dark signal).
- `P(λ)` is the optical power measured by the calibrated detector at that wavelength.

Because many camera internal parameters are unknown (gain, aperture transmission, exact irradiance at the sensor, etc.),
this is typically presented as a **normalized** response curve (shape vs wavelength).

![Camera response example](figures/remade/fig5_camera_response.png)

*Figure 4 — Example camera spectral response curve (illustrative).  
Peak location and shape depend on sensor type, optics, and filtering (IR-cut, CFA, microlenses, etc.).*

### What influences the curve?

Even if the silicon QE is smooth, the overall camera response is shaped by:

- lens / window transmission
- microlenses and pixel geometry
- color filters (if present)
- IR-cut filters
- anti-reflection coatings
- sensor electronics (gain and digitization)

---

## Noise: temporal vs spatial

Noise is easiest to understand if we separate two ideas:

1. **Temporal noise:** the value of a *single pixel* fluctuates from frame to frame (time).  
2. **Spatial noise / fixed-pattern noise:** some pixels are consistently higher/lower than others (space).

Both matter: temporal noise limits repeatability, while fixed-pattern noise appears as “texture” that doesn’t average away.

### Temporal noise (frame-to-frame)

If we record many frames under constant illumination and track one pixel, we observe fluctuations:

![Temporal noise example](figures/remade/fig6_temporal_noise.png)

*Figure 5 — Pixel value over time for repeated captures (example). The spread is a measure of temporal noise.*

A standard estimate for temporal noise for one pixel is the standard deviation over time:

\[
\sigma_t = \mathrm{std}(x_1, x_2, \ldots, x_N)
\]

A very robust trick (when illumination might drift slowly) is to use the difference of consecutive frames:

\[
\sigma_t \approx \frac{\mathrm{std}(I_1 - I_2)}{\sqrt{2}}
\]

because subtracting cancels constant offsets and halves shared low-frequency trends.

#### Physical sources of temporal noise (conceptual)

- **Shot noise:** photon arrivals are Poisson → variance ≈ mean signal (in electrons).  
- **Dark current noise:** thermally generated electrons (increases with temperature and exposure time).  
- **Read noise:** noise added by amplifiers/ADC during readout (often dominant at very low light).  
- **Quantization noise:** from finite ADC resolution (usually small when signal spans many codes).

### Spatial noise / fixed-pattern noise (pixel-to-pixel)

If we average many frames, temporal noise reduces roughly as \(1/\sqrt{N}\), but **fixed-pattern** components remain.

The average image can show illumination structure (from the sphere / optics), and the residual after subtracting a smooth
average can reveal fixed-pattern texture:

![Spatial noise example](figures/remade/fig7_spatial_noise.png)

*Figure 6 — Left: average image over many frames (example illumination profile).  
Right: fixed-pattern noise illustration (residual after removing the smooth average trend).*

A 3D surface view can make gradients and vignetting patterns more obvious:

![3D average image view](figures/remade/fig8_average_3d.png)

*Figure 7 — 3D view of the average image (example).*

#### Practical takeaway

- Averaging many frames improves SNR **against temporal noise**.
- Averaging does **not** remove fixed-pattern noise; it often reveals it more clearly.
- A common mitigation is **flat-field correction** (divide by a calibrated illumination map) and/or **dark-frame subtraction**.

### Histograms as a quick diagnostic

Histograms summarize the distribution of pixel values and help spot saturation, clipping, or multimodal behavior:

![Histogram example](figures/remade/fig3_histogram.png)

*Figure 8 — Example pixel histogram. Mean and spread relate to signal level and noise; shape can reveal artifacts.*

---

## Reproducibility

### Generate the remade figures

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/make_figures.py
```

### Using your real measurement data

The plots in `figures/remade/` are **reproducible illustrations** driven by CSVs in `data/`.  
To regenerate with measured data, replace the example CSVs while keeping the same columns:

- `data/spectral_power_detector_example.csv`  
  - `wavelength_nm`, `power_W`
- `data/spectral_camera_response_example.csv`  
  - `wavelength_nm`, `camera_response_arb`

Then re-run `python src/make_figures.py`.

---

## Suggested citation

If you reuse or adapt this material, cite the original course/lab context (Sorbonne Université — Bio-Inspired Vision, 2024–2025),
and keep `report/original_report_fr.pdf` as the reference artifact.