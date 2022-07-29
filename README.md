<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />

<h3 align="center">Home Comfort Dataset</h3>

  <p align="center">
    Processing of the dataset gathered in the scope of the Smart Green Homes project.
  </p>


</div>



<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
        <a href="#usage">Usage</a>
        <ul>
            <li><a href="#example">Example</a></li>
        </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project

Processing of the dataset gathered during the execution of the Smart Green Homes project. This dataset comprises of envioronmental collected from volunteers' homes, which can be used for researching and developing techonogy solutions for households, with the goal of raising standards of comfort, safety and user satisfaction.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [![Python][Python-logo]][Python-url]
* [![Pandas][Pandas-logo]][Pandas-url]
* [![Matplotlib][Matplotlib-logo]][Matplotlib-url]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

To execute the script to generate the charts follow these simple steps.

### Prerequisites

To run the script you need to have at least Python 3.8 installed on your machine. You can find out how [in the official page](https://www.python.org/downloads/).

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/immarianaas/home-comfort-dataset.git
   ```

2. Install Python packages
   ```sh
   cd home-comfort-dataset
   python3 -m pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

## Usage

To run the program you only need to run `plot.py`. Some arguments to keep in mind:

| Positional arguments | Descriptions |
|---|---|
| `DATASET PATH`     | path to directory where the dataset files are placed |
| `SAVE IMAGES PATH` | existing directory where the images are to be saved if `ADDITIONAL DIRECTORY` is not set |

| Optional arguments | Descriptions |
|---|---|
| `-h`, `--help`     | shows a help message and exits |
| `-d ADDITIONAL DIRECTORY` | directory that might not exist (it will be created in that case); <br />if set, they are to be saved on `<SAVE IMAGES PATH>/<ADDITIONAL DIRECTORY>` |
| `--titles` | charts are to be saved with titles **(set by default)** |
| `--no-titles` | charts are to be saved without titles |

### Example

``` bash
# considering that '~/Documents/dataset' was the dataset files
# images should be saved on '~/Documents/plot_images'
python3 plot.py ~/Documents/dataset ~/Documents -d plot_images
```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/immarianaas/home-comfort-dataset.svg?style=for-the-badge
[contributors-url]: https://github.com/immarianaas/home-comfort-dataset/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/immarianaas/home-comfort-dataset.svg?style=for-the-badge
[forks-url]: https://github.com/immarianaas/home-comfort-dataset/network/members
[stars-shield]: https://img.shields.io/github/stars/immarianaas/home-comfort-dataset.svg?style=for-the-badge
[stars-url]: https://github.com/immarianaas/home-comfort-dataset/stargazers
[issues-shield]: https://img.shields.io/github/issues/immarianaas/home-comfort-dataset.svg?style=for-the-badge
[issues-url]: https://github.com/immarianaas/home-comfort-dataset/issues
[license-shield]: https://img.shields.io/github/license/immarianaas/home-comfort-dataset.svg?style=for-the-badge
[license-url]: https://github.com/immarianaas/home-comfort-dataset/blob/master/LICENSE.txt



[Python-logo]: https://img.shields.io/badge/Python-306998?style=for-the-badge&amp;logo=python&amp;logoColor=white

[Python-url]: https://python.org
[Matplotlib-url]: https://matplotlib.org
[Matplotlib-logo]: https://img.shields.io/badge/matplotlib-F9A46A?style=for-the-badge
[Pandas-logo]: https://img.shields.io/badge/pandas-b4b5bf?style=for-the-badge&logo=pandas&logoColor=black
[Pandas-url]: https://pandas.pydata.org/
