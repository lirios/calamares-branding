install(DIRECTORY "prepare/" DESTINATION "${KDE_INSTALL_LIBDIR}/calamares/modules/prepare")
install(DIRECTORY "ostree/" DESTINATION "${KDE_INSTALL_LIBDIR}/calamares/modules/ostree")
install(DIRECTORY "ostree-bootloader/" DESTINATION "${KDE_INSTALL_LIBDIR}/calamares/modules/ostree-bootloader")
install(DIRECTORY "ostree-finalize/" DESTINATION "${KDE_INSTALL_LIBDIR}/calamares/modules/ostree-finalize")
install(FILES "ostree/ostree.conf" DESTINATION "${KDE_INSTALL_DATADIR}/calamares/modules")
install(FILES "ostree-bootloader/ostree-bootloader.conf" DESTINATION "${KDE_INSTALL_DATADIR}/calamares/modules")
