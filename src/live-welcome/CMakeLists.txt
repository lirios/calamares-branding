# Translations
file(GLOB LiveWelcome_TRANSLATIONS "${CMAKE_CURRENT_SOURCE_DIR}/translations/*_*.ts")
qt5_add_translation(LiveWelcome_QM_FILES ${LiveWelcome_TRANSLATIONS})
install(FILES ${LiveWelcome_QM_FILES}
        DESTINATION "${INSTALL_DATADIR}/liri-live-welcome/translations")

liri_add_executable(LiveWelcome
    OUTPUT_NAME
        "liri-live-welcome"
    SOURCES
        main.cpp
        runner.cpp
        runner.h
        ${LiveWelcome_QM_FILES}
    DEFINES
        QT_NO_CAST_FROM_ASCII
        QT_NO_FOREACH
        VERSION="${PROJECT_VERSION}"
    DESKTOP
        "${CMAKE_CURRENT_SOURCE_DIR}/io.liri.LiveWelcome.desktop"
    DESKTOP_INSTALL_DIRECTORY
        "${INSTALL_SYSCONFDIR}/xdg/autostart"
    RESOURCES
        "live-welcome.qrc"
    LIBRARIES
        Qt5::Core
        Qt5::Gui
        Qt5::Qml
        Qt5::Quick
        Qt5::QuickControls2
    QTQUICK_COMPILER
)
