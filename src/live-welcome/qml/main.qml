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

import QtQuick 2.0
import QtQuick.Layouts 1.0
import QtQuick.Controls 2.0
import QtQuick.Controls.Material 2.0
import Fluid.Controls 1.0 as FluidControls

ApplicationWindow {
    title: qsTr("Welcome to Liri OS")
    width: 600
    height: 400
    minimumWidth: 600
    minimumHeight: 400
    visible: true

    Material.accent: Material.Blue
    Material.primary: Material.BlueGrey

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        FluidControls.Placeholder {
            icon.source: FluidControls.Utils.iconUrl("hardware/computer")
            text: qsTr("Welcome to Liri OS")
            subText: qsTr("You are currently running Liri OS from live media.\nYou can install Liri OS now, or launch \"Install to Hard Drive\" later.")

            Layout.fillWidth: true
            Layout.preferredHeight: 300
            Layout.alignment: Qt.AlignCenter
        }

        Item {
            Layout.fillHeight: true
        }

        FluidControls.ListItem {
            icon.source: FluidControls.Utils.iconUrl("action/exit_to_app")
            text: qsTr("Try Liri OS")
            onClicked: Qt.quit()
        }

        FluidControls.ListItem {
            icon.source: FluidControls.Utils.iconUrl("file/file_download")
            text: qsTr("Install to Hard Drive")
            onClicked: {
                Runner.run();
                Qt.quit();
            }
        }
    }
}
