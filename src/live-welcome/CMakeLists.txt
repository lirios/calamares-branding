# Translations
file(GLOB LiveWelcome_TRANSLATIONS "${CMAKE_CURRENT_SOURCE_DIR}/translations/*_*.ts")
qt6_add_translation(LiveWelcome_QM_FILES ${LiveWelcome_TRANSLATIONS})
install(FILES ${LiveWelcome_QM_FILES}
        DESTINATION "${KDE_INSTALL_DATADIR}/liri-live-welcome/translations")

set(SOURCES
    main.cpp
    runner.cpp runner.h
    io.liri.LiveWelcome.desktop
)

qt_add_resources(SOURCES live-welcome.qrc)
qt6_add_executable(LiveWelcome
    MANUAL_FINALIZATION
    ${SOURCES}
    ${LiveWelcome_QM_FILES}
)

set_target_properties(LiveWelcome PROPERTIES OUTPUT_NAME "liri-live-welcome")

target_compile_definitions(LiveWelcome PRIVATE VERSION="${PROJECT_VERSION}")

target_link_libraries(LiveWelcome PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Qml
    Qt6::Quick
    Qt6::QuickControls2
)

qt6_finalize_target(LiveWelcome)

install(TARGETS LiveWelcome DESTINATION ${KDE_INSTALL_BINDIR})
install(FILES io.liri.LiveWelcome.desktop DESTINATION ${KDE_INSTALL_SYSCONFDIR}/xdg/autostart)
