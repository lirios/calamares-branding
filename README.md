Calamares Branding
==================

[![License](https://img.shields.io/badge/license-GPLv3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![GitHub release](https://img.shields.io/github/release/lirios/calamares-branding.svg)](https://github.com/lirios/calamares-branding)
[![CI](https://github.com/lirios/calamares-branding/workflows/CI/badge.svg?branch=develop)](https://github.com/lirios/calamares-branding/actions?query=workflow%3ACI)
[![GitHub issues](https://img.shields.io/github/issues/lirios/calamares-branding.svg)](https://github.com/lirios/calamares-branding/issues)

Liri OS branding and customizations for Calamares.

## Dependencies

The following modules and their dependencies are required:

 * [cmake](https://gitlab.kitware.com/cmake/cmake) >= 3.19.0
 * [extra-cmake-modules](https://invent.kde.org/frameworks/extra-cmake-modules) >= 5.245.0

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
