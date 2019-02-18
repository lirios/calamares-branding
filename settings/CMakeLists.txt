install(FILES "settings.conf" DESTINATION "${INSTALL_SYSCONFDIR}/calamares")
install(
    FILES
        "bootloader.conf"
        "displaymanager.conf"
        "grubcfg.conf"
        "services.conf"
        "welcome.conf"
    DESTINATION
        "${INSTALL_SYSCONFDIR}/calamares/modules"
)
