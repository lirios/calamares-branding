import qbs 1.0

Project {
    name: "CalamaresBranding"

    readonly property string version: "0.9.0"

    minimumQbsVersion: "1.9.0"

    references: [
        "branding/branding.qbs",
        "data/data.qbs",
        "modules/modules.qbs",
        "settings/settings.qbs",
    ]

    InstallPackage {
        name: "calamares-branding-artifacts"
        targetName: name
        builtByDefault: false

        archiver.type: "tar"
        archiver.outputDirectory: project.buildDirectory

        Depends { name: "calamares-desktop" }
        Depends { name: "calamares-liri-branding" }
        Depends { name: "calamares-modules" }
        Depends { name: "calamares-settings" }
    }
}
