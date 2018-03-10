import qbs 1.0

Product {
    name: "calamares-desktop"

    Depends { name: "lirideployment" }

    Group {
        name: "Desktop file"
        files: ["calamares.desktop"]
        qbs.install: true
        qbs.installDir: lirideployment.dataDir + "/liri-calamares-branding"
    }
}
