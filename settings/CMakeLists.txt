install(FILES "settings.conf" DESTINATION "${KDE_INSTALL_SYSCONFDIR}/calamares")
install(
    FILES
        "displaymanager.conf"
        "services-systemd.conf"
        "welcome.conf"
    DESTINATION
        "${KDE_INSTALL_SYSCONFDIR}/calamares/modules"
)
