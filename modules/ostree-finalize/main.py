#
# This file is part of Liri.
#
# Copyright (C) 2019 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#
# $BEGIN_LICENSE:GPL3+$
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# $END_LICENSE$
#

import libcalamares

def run():
    # Swap the root mount point so that a second invokation of the `umount` job
    # will unmount the original root
    new_install_path = libcalamares.globalstorage.value('rootMountPoint')
    install_path = libcalamares.globalstorage.value('oldRootMountPoint')
    libcalamares.globalstorage.insert('rootMountPoint', install_path)
    libcalamares.globalstorage.remove('oldRootMountPoint')

    return None
