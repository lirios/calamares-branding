import qbs 1.0

Product {
    name: "calamares-settings"

    Depends { name: "lirideployment" }

    Group {
        name: "Main settings"
        files: ["settings.conf"]
        qbs.install: true
        qbs.installDir: lirideployment.etcDir + "/calamares"
    }

    Group {
        name: "Modules settings"
        files: [
            "bootloader.conf",
            "displaymanager.conf",
            "grubcfg.conf",
            "initcpio.conf",
            "packages.conf",
            "removeuser.conf",
            "unpackfs.conf",
        ]
        qbs.install: true
        qbs.installDir: lirideployment.etcDir + "/calamares"
    }
}
