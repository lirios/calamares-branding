Hawaii branding for Calamares
=============================

[![GitHub release](https://img.shields.io/github/release/hawaii-desktop/hawaii-calamares-branding.svg)](https://github.com/hawaii-desktop/hawaii-calamares-branding)
[![GitHub issues](https://img.shields.io/github/issues/hawaii-desktop/hawaii-calamares-branding.svg)](https://github.com/hawaii-desktop/hawaii-calamares-branding/issues)

This repository contains branding and customizations for Calamares,
used by the Hawaii operating system live images.

## Dependencies

In order to install branding and customizations you need:

* [CMake](http://www.cmake.org)
* [extra-cmake-modules](http://quickgit.kde.org/?p=extra-cmake-modules.git)

## Installation

Assuming you are in the source directory, just create a build directory
and run cmake:

```sh
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/opt/hawaii ..
```

If not passed, the `CMAKE_INSTALL_PREFIX` parameter defaults to /usr/local.
You have to specify a path that fits your needs, /opt/hawaii is just an example.

Package maintainers would pass `-DCMAKE_INSTALL_PREFIX=/usr`.

Now type:

```sh
make install
```

from the build directory.
