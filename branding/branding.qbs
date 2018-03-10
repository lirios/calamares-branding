import qbs 1.0

Product {
    name: "calamares-liri-branding"

    Depends { name: "lirideployment" }

    Group {
        name: "Branding"
        files: [
            "branding.desc",
            "*.png",
            "*.qml"
        ]
        qbs.install: true
        qbs.installDir: lirideployment.dataDir + "/calamares/branding/liri"
    }
}
