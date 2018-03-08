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

    - Initialize and populate pacman keyring so we can install
      packages later.
    - Install the kernel which is not included in the image.
    - Remove sudo configuration for the installer.
    - Rewrite os-release.

    This job must be executed before packages and grubcfg.
    """

    install_path = libcalamares.globalstorage.value("rootMountPoint")

    libcalamares.utils.target_env_call(["pacman-key", "--init"])
    libcalamares.utils.target_env_call(["pacman-key", "--populate"])

    boot_path = os.path.join(install_path, "boot", "vmlinuz-linux")
    shutil.copyfile("/run/archiso/bootmnt/liri/boot/x86_64/vmlinuz", boot_path)

    for sudoers_filename in ("00-livemedia", "10-installer"):
        sudoers_path = os.path.join(install_path, "etc", "sudoers.d", sudoers_filename)
        if os.path.exists(sudoers_path):
            os.unlink(sudoers_path)

    sddm_conf_path = os.path.join(install_path, "usr", "lib", "sddm", "sddm.conf.d", "01-livemedia.conf")
    if os.path.exists(sddm_conf_path):
        os.unlink(sddm_conf_path)

    mkinitcpio_path = os.path.join(install_path, "etc", "mkinitcpio-archiso.conf")
    if os.path.exists(mkinitcpio_path):
        os.unlink(mkinitcpio_path)

    os_release = os.path.join(install_path, "etc", "os-release")
    if os.path.exists(os_release):
        os.unlink(os_release)
    try:
        with open(os_release, "w") as fd:
            fd.write('NAME="Liri OS"\n')
            fd.write('ID=lirios\n')
            fd.write('PRETTY_NAME="Liri OS"\n')
            fd.write('ANSI_COLOR="0;36"\n')
            fd.write('HOME_URL="https://liri.io"\n')
            fd.write('BUG_REPORT_URL="https://github.com/lirios/lirios/issues"\n')
    except OSError as e:
        return ("Failed to write os-release", e.message)

    return None
