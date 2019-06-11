/****************************************************************************
 * This file is part of Liri.
 *
 * Copyright (C) 2019 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
 *
 * $BEGIN_LICENSE:GPL3+$
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * $END_LICENSE$
 ***************************************************************************/

#include <QGuiApplication>
#include <QLibraryInfo>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQuickStyle>
#include <QStandardPaths>
#include <QTranslator>

#include "runner.h"

static void loadQtTranslations()
{
#ifndef QT_NO_TRANSLATION
    QString locale = QLocale::system().name();

    // Load Qt translations
    QTranslator *qtTranslator = new QTranslator(qApp);
    if (qtTranslator->load(QStringLiteral("qt_%1").arg(locale), QLibraryInfo::location(QLibraryInfo::TranslationsPath))) {
        qApp->installTranslator(qtTranslator);
    } else {
        delete qtTranslator;
    }
#endif
}

static void loadTranslations()
{
#ifndef QT_NO_TRANSLATION
    QString locale = QLocale::system().name();

    // Find the translations directory
    const QString path = QStringLiteral("liri-live-welcome/translations");
    const QString translationsDir =
            QStandardPaths::locate(QStandardPaths::GenericDataLocation,
                                   path,
                                   QStandardPaths::LocateDirectory);

    // Load shell translations
    QTranslator *appTranslator = new QTranslator(qGuiApp);
    if (appTranslator->load(QStringLiteral("%1/liri-live-welcome_%2").arg(translationsDir, locale))) {
        QCoreApplication::installTranslator(appTranslator);
    } else if (locale == QStringLiteral("C") ||
               locale.startsWith(QStringLiteral("en"))) {
        // English is the default, it's translated anyway
        delete appTranslator;
    }
#endif
}

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    // Setup application
    QGuiApplication app(argc, argv);
    app.setApplicationName(QStringLiteral("Live Welcome"));
    app.setApplicationVersion(QStringLiteral(VERSION));
    app.setOrganizationDomain(QStringLiteral("liri.io"));
    app.setOrganizationName(QStringLiteral("Liri"));
    app.setDesktopFileName(QStringLiteral("io.liri.LiveWelcome.desktop"));

    QQuickStyle::setStyle(QStringLiteral("Material"));

    // Load translations
    loadQtTranslations();
    loadTranslations();

    // Load UI
    QQmlApplicationEngine engine(QUrl(QStringLiteral("qrc:/qml/main.qml")));
    engine.rootContext()->setContextProperty(QStringLiteral("Runner"), new Runner(&engine));

    return app.exec();
}
