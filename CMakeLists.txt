cmake_minimum_required(VERSION 3.10.0)

project("CalamaresBranding"
    VERSION "0.9.0"
    DESCRIPTION "Modules and configuration for the Calamares installer"
    LANGUAGES CXX C
)

## Shared macros and functions:
if(NOT LIRI_LOCAL_ECM)
    find_package(LiriCMakeShared "2.0.0" REQUIRED NO_MODULE)
    list(APPEND CMAKE_MODULE_PATH "${LCS_MODULE_PATH}")
endif()

## Set minimum versions required:
set(QT_MIN_VERSION "5.15.0")

## Add some paths to check for CMake modules:
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

## Liri specific setup common for all modules:
include(LiriSetup)

## Find Qt 5:
find_package(Qt5 "${QT_MIN_VERSION}"
    CONFIG REQUIRED
    COMPONENTS
        Core
        Gui
        Qml
        Quick
        QuickControls2
        LinguistTools
)

## Add subdirectories:
add_subdirectory(branding)
add_subdirectory(data)
add_subdirectory(modules)
add_subdirectory(settings)
add_subdirectory(src/ostree-install)
add_subdirectory(src/live-welcome)
