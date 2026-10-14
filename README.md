# Electronic Devices & Circuits Laboratory
PSG Institute of Technology and Applied Research · 25IC111
Prepared for Dr. Arivoli S.

## Deploy using GitHub and Streamlit
1. Extract this ZIP on your computer.
2. Create a GitHub repository named `electronic-devices-circuits-lab`.
3. Upload the CONTENTS of the `edc-lab` folder into the repository root. Keep `app.py`, `models.py`, `requirements.txt`, the entire `assets` folder and `.streamlit/config.toml`. Do not upload only the ZIP.
4. Visit https://share.streamlit.io/ and sign in with GitHub. Select Create app and choose your repository, branch `main`, and main file `app.py`.
5. In Advanced settings choose an available Python 3.13 runtime if offered. Python 3.12 also works. Click Deploy.
6. For student access use a public repository and verify that the deployed app sharing setting is public. Open the app URL in a private/incognito window before distributing it.
7. Share the resulting `streamlit.app` URL. No ChatGPT account is required by this app. Streamlit hosting access is controlled by the platform sharing setting.

Official deployment guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Run on your laptop (Python 3.13)
Open a terminal in this folder:
```
python -m venv .venv
```
Windows:
```
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
macOS/Linux activation: `source .venv/bin/activate`.

## Student workflow
Choose an experiment, read the aim and source manual, vary the simulator controls, download simulated CSV data, enter actual measurements in Observation & record, write an interpretation, and download the HTML record. Open the HTML in a browser and use Print → Save as PDF. Simulated and measured results are labelled separately. No student information is sent to a separate database by the application; Streamlit session data is temporary. Download before closing or refreshing.

## Included experiments
1. Maximum power transfer
2. Sinusoidal steady-state RLC (series and supplementary parallel option)
3. Series RLC resonance
4. RC transient response
5. PN and Zener diode characteristics
6. Half-wave and bridge rectifiers, optional capacitor filter
7. BJT input and output characteristics
8. Single-stage BJT amplifier
9. RC phase-shift oscillator using BJT
10. JFET as a switch

The supplied syllabus determines experiment numbering. Original manuals retain their original numbering. The parallel RLC manual is supplementary and does not replace the series RLC syllabus experiment.

## Model scope
This is an analytical teaching app, not SPICE. Ideal RLC elements, room-temperature diode approximation, fixed rectifier diode drops, simple BJT characteristics, approximate small-signal amplifier response, unloaded oscillator design formula and square-law JFET model are explicitly identified. The oscillator plot illustrates a sinusoid and does not solve startup or amplitude limiting. Amplifier cutoff frequencies are user inputs, not predictions from component capacitances. Bench procedures and circuits must be checked by faculty against real component datasheets. All original supplied manuals and extracted raster figures are included; equations embedded as images may not appear in extracted text. Confirm permission to publish supplied teaching material before using a public repository.

## Verification
Run `python test_models.py` for numerical checks. Run `python test_app.py` with Streamlit installed for all experiment screens and alternate device modes. Tests use Streamlit AppTest; no credentials are needed. Python 3.13 compatibility is intended; see VALIDATION.md for the environment actually tested.
