import qbs 1.0

Product {
    name: "calamares-modules"

    Depends { name: "lirideployment" }

    Group {
        name: "prepare module"
        prefix: "prepare/"
        files: [
            "main.py",
            "module.desc"
        ]
        qbs.install: true
        qbs.installDir: lirideployment.libDir + "/calamares/modules/prepare"
    }
}
