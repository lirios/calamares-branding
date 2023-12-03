cmake_minimum_required(VERSION 3.10.0)

project("CalamaresBranding"
    VERSION "0.9.0"
    DESCRIPTION "Modules and configuration for the Calamares installer"
    LANGUAGES CXX C
)

## Only build on the appropriate platforms.
if(NOT (LINUX OR NOT CMAKE_SYSTEM_NAME MATCHES "Android"))
    message(NOTICE "Skipping the build as the condition \"LINUX OR NOT Android\" is not met.")
    return()
endif()

## ECM:
find_package(ECM 5.245.0 REQUIRED NO_MODULE)
list(APPEND CMAKE_MODULE_PATH ${ECM_MODULE_PATH})

## Installation directories:
include(KDEInstallDirs)

## Compiler settings:
set(KDE_SKIP_NULLPTR_WARNINGS_SETTINGS TRUE)
include(KDECompilerSettings NO_POLICY_SCOPE)

## CMake settings:
include(KDECMakeSettings)

## Find Qt 5:
find_package(Qt6
    REQUIRED
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
