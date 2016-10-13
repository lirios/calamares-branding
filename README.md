Calamares Branding
==================

[![ZenHub.io](https://img.shields.io/badge/supercharged%20by-zenhub.io-blue.svg)](https://zenhub.io)

[![License](https://img.shields.io/badge/license-GPLv3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
[![GitHub release](https://img.shields.io/github/release/lirios/calamares-branding.svg)](https://github.com/lirios/calamares-branding)
[![Build Status](https://travis-ci.org/lirios/calamares-branding.svg?branch=develop)](https://travis-ci.org/lirios/calamares-branding)
[![GitHub issues](https://img.shields.io/github/issues/lirios/calamares-branding.svg)](https://github.com/lirios/calamares-branding/issues)
[![Maintained](https://img.shields.io/maintenance/yes/2016.svg)](https://github.com/lirios/calamares-branding/commits/develop)

Liri OS branding and customizations for Calamares.

## Dependencies

In order to install branding and customizations you need:

 * [CMake](http://www.cmake.org)
 * [ECM >= 1.7.0](http://quickgit.kde.org/?p=extra-cmake-modules.git)

## Installation

From the root of the repository, run:

```sh
mkdir build; cd build
cmake .. -DKDE_INSTALL_USE_QT_SYS_PATHS=ON
make
make install # use sudo if necessary
```

On the `cmake` line, you can specify additional configuration parameters:

 * `-DCMAKE_INSTALL_PREFIX=/path/to/install` (for example, `/opt/liri` or `/usr`)
 * `-DCMAKE_BUILD_TYPE=<build_type>`, where `<build_type>` is one of:
   * **Debug:** debug build
   * **Release:** release build
   * **RelWithDebInfo:** release build with debugging information

## Licensing

Licensed under the terms of the GNU General Public License version 3 or,
at your option, any later version.
