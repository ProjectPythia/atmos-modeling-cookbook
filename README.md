<img src="thumbnail.png" alt="thumbnail" width="300"/>

# Fundamentals of Atmsopheric Modeling Cookbook

[![nightly-build](https://github.com/ProjectPythia/cookbook-template/actions/workflows/nightly-build.yaml/badge.svg)](https://github.com/ProjectPythia/cookbook-template/actions/workflows/nightly-build.yaml)
[![Binder](https://binder.projectpythia.org/badge_logo.svg)](https://binder.projectpythia.org/v2/gh/ProjectPythia/cookbook-template/main?labpath=notebooks)
[![DOI](https://zenodo.org/badge/475509405.svg)](https://zenodo.org/badge/latestdoi/475509405)

This Project Pythia Cookbook covers the fundamentals of atmospheric modeling, including topics such as:

- basic conservation equations
- approaches to finite differencing
- numerical scheme assessments
- numerical corrections and filtering
- coordinate systems
- initial/boundary conditions
- limitations and tradeoffs in modeling

## Motivation

Numerical models are widely used, but gaining expertise in how they work has often been unnecessarily challenging. This cookbook hopes to address that! This is intended for a somewhat broad audience: those with at least some atmospheric dynamics knowledge, but nearly any level of programming experience (assuming a baseline level as covered in the [Pythia Foundations](https://foundations.projectpythia.org/landing-page.html)).

## Authors

[JT Thielen](@jthielen), [Second Author](@second-author), etc. _Acknowledge primary content authors here_

### Contributors

<a href="https://github.com/ProjectPythia/cookbook-template/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ProjectPythia/cookbook-template" />
</a>

## Resources

This cookbook would not be possible without the vast collection of academic texts and prior work in atmospheric modeling. The key resources used in building this notebook include:

- Textbooks
    - [An Introduction to Numerical Modeling of the Atmosphere, by David Randall](https://hogback.atmos.colostate.edu/group/dave/at604pdf/An_Introduction_to_Numerical_Modeling_of_the_Atmosphere.pdf)
    - [Mesoscale Meteorological Modeling, 2nd Edition, by Roger Piekle](https://www.sciencedirect.com/bookseries/international-geophysics/vol/78/suppl/C)
- Journal Articles
    - ...
- Other Resources
    - [Pet Tornado, by Brian Fiedler](https://nbviewer.org/urls/www.dropbox.com/scl/fi/74w6w8kghbjjb7rbpwimx/N130_pettornado3d.ipynb/%3Frlkey%3Dhtke7col7cvohk3jno0s2p5vb%26dl%3D1)


## Structure

(State one or more sections that will comprise the notebook. E.g., _This cookbook is broken up into two main sections - "Foundations" and "Example Workflows."_ Then, describe each section below.)

### Section 1 ( Replace with the title of this section, e.g. "Foundations" )

(Add content for this section, e.g., "The foundational content includes ... ")

### Section 2 ( Replace with the title of this section, e.g. "Example workflows" )

(Add content for this section, e.g., "Example workflows include ... ")

## Running the Notebooks

You can either run the notebook using [Binder](https://binder.projectpythia.org/) or on your local machine.

### Running on Binder

The simplest way to interact with a Jupyter Notebook is through
[Binder](https://binder.projectpythia.org/), which enables the execution of a
[Jupyter Book](https://jupyterbook.org) in the cloud. The details of how this works are not
important for now. All you need to know is how to launch a Pythia
Cookbooks chapter via Binder. Simply navigate your mouse to
the top right corner of the book chapter you are viewing and click
on the rocket ship icon, (see figure below), and be sure to select
“launch Binder”. After a moment you should be presented with a
notebook that you can interact with. I.e. you’ll be able to execute
and even change the example programs. You’ll see that the code cells
have no output at first, until you execute them by pressing
{kbd}`Shift`\+{kbd}`Enter`. Complete details on how to interact with
a live Jupyter notebook are described in [Getting Started with
Jupyter](https://foundations.projectpythia.org/foundations/getting-started-jupyter.html).

### Running on Your Own Machine

If you are interested in running this material locally on your computer, you will need to follow this workflow:

(Replace "cookbook-example" with the title of your cookbooks)

1. Clone the `https://github.com/ProjectPythia/cookbook-example` repository:

   ```bash
    git clone https://github.com/ProjectPythia/cookbook-example.git
   ```

1. Move into the `cookbook-example` directory
   ```bash
   cd cookbook-example
   ```
1. Create and activate your conda environment from the `environment.yml` file
   ```bash
   conda env create -f environment.yml
   conda activate cookbook-example
   ```
1. Move into the `notebooks` directory and start up Jupyterlab
   ```bash
   cd notebooks/
   jupyter lab
   ```
