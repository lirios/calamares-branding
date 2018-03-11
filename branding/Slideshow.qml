/****************************************************************************
 * This file is part of Liri.
 *
 * Copyright (C) 2018 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
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
import calamares.slideshow 1.0

Presentation {
    id: presentation

    width: 800
    height: 600

    Timer {
        interval: 5000
        running: false
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }
    
    SlideImage {
        Image {
            source: "logo.png"
            width: sourceSize.width / 2
            height: sourceSize.height / 2
            fillMode: Image.PreserveAspectFit
        }

        FocusText {
            anchors.centerIn: parent
            anchors.verticalCenterOffset: 0
            anchors.horizontalCenterOffset: 150
            width: 450
            text: qsTr("<h1>Welcome to Liri OS!</h1><br/>" +
                       "<p>Liri OS is driven by a hard working and dedicated community of volunteers.</p>" +
                       "<p>During the installation, this slideshow will provide you a quick introduction.</p><br/>" +
                       "<p>Press the <b>left mouse button</b> to go to the next slide or the <b>right mouse button</b> " +
                       "for the previous one.</p>")
        }
    }

    SlideImage {
        FocusText {
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 24
            width: 450
            text: qsTr("<p>Our desktop and apps follow the Material Design language from Google.</p>" +
                       "<p>This means the operating system will look consistent, be easy to use and undestand," +
                       "and have a high degree of polish and animations.</p>")
        }
    }

    SlideImage {
        FocusText {
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 24
            width: 450
            text: qsTr("<p>Our apps are installed by default and these include: file manager, terminal emulator," +
                       "text editor, web browser, calculator, app installer and settings.</p>" +
                       "<p>More apps can be installed from Flathub.</p>")
        }
    }
}
