Calamares Branding
==================

[![License](https://img.shields.io/badge/license-GPLv3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![GitHub release](https://img.shields.io/github/release/lirios/calamares-branding.svg)](https://github.com/lirios/calamares-branding)
[![Build Status](https://travis-ci.org/lirios/calamares-branding.svg?branch=develop)](https://travis-ci.org/lirios/calamares-branding)
[![GitHub issues](https://img.shields.io/github/issues/lirios/calamares-branding.svg)](https://github.com/lirios/calamares-branding/issues)
[![Maintained](https://img.shields.io/maintenance/yes/2018.svg)](https://github.com/lirios/calamares-branding/commits/develop)

Liri OS branding and customizations for Calamares.

## Dependencies

The following modules and their dependencies are required:

 * [cmake](https://gitlab.kitware.com/cmake/cmake) >= 3.10.0
 * [cmake-shared](https://github.com/lirios/cmake-shared.git) >= 1.0.0

## Installation

```sh
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/path/to/prefix ..
make
make install # use sudo if necessary
```

Replace `/path/to/prefix` to your installation prefix.
Default is `/usr/local`.

## Licensing

Licensed under the terms of the GNU General Public License version 3 or,
at your option, any later version.
