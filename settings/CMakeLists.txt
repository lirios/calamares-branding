install(FILES "settings.conf" DESTINATION "${INSTALL_SYSCONFDIR}/calamares")
install(
    FILES
        "displaymanager.conf"
        "services-systemd.conf"
        "welcome.conf"
    DESTINATION
        "${INSTALL_SYSCONFDIR}/calamares/modules"
)
