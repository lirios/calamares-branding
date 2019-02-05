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

import subprocess
import libcalamares

def run():
    """
    Install the OS tree on the root file system.
    """

    install_path = libcalamares.globalstorage.value('rootMountPoint')

    progname = '/usr/bin/calamares-ostree-install'

    # The Calamares Python interpreter freezes when loading gobject-introspection, so we moved the
    # code to an external process

    deployment_path = None

    with subprocess.Popen([progname, install_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        (stdout, stderr) = p.communicate()

        if p.returncode == 0:
            output = stdout.decode('utf-8')
            for line in output.split('\n'):
                if line.startswith('PROGRESS'):
                    percent = float(line[9:])
                    libcalamares.job.setprogress(percent)
                elif line.startswith('RESULT'):
                    deployment_path = line[7:]
                    libcalamares.globalstorage.insert('ostreeDeploymentPath', deployment_path)
                else:
                    libcalamares.utils.debug(line)
        else:
            return stderr.decode('utf-8').split('\n')

    if deployment_path is None:
        return ('No deployment path', 'Unable to find OS tree deployment.')

    return None
