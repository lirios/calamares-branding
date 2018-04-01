import qbs 1.0

Product {
    name: "calamares-scripts"

    Depends { name: "lirideployment" }

    Group {
        name: "Script"
        files: ["run-calamares"]
        qbs.install: true
        qbs.installDir: lirideployment.binDir
    }
}
