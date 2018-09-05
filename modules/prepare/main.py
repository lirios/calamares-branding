#
# This file is part of Liri.
#
# Copyright (C) 2016 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
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

import os
import shutil
import libcalamares

def run():
    """ Perform tasks to prepare the system.

    - Remove sudo configuration for the live media and installer.
    - Remove SDDM configuration for the live media.

    This job must be executed before packages and grubcfg.
    """

    install_path = libcalamares.globalstorage.value("rootMountPoint")

    for sudoers_filename in ("00-livemedia", "10-installer"):
        sudoers_path = os.path.join(install_path, "etc", "sudoers.d", sudoers_filename)
        if os.path.exists(sudoers_path):
            os.unlink(sudoers_path)

    sddm_conf_path = os.path.join(install_path, "usr", "lib", "sddm", "sddm.conf.d", "01-livemedia.conf")
    if os.path.exists(sddm_conf_path):
        os.unlink(sddm_conf_path)

    return None
