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

import gi
import os
import shutil
import subprocess
import libcalamares

gi.require_version('GLib', '2.0')
gi.require_version('OSTree', '1.0')
gi.require_version('RpmOstree', '1.0')

from gi.repository import GLib, Gio, OSTree, RpmOstree


def run():
    """
    Install the OS tree on the root file system.
    """

    cancellable = None
    osname = 'lirios'
    nogpg = True
    noverifyssl = True
    remote_options = {
        'gpg-verify': GLib.Variant('b', not nogpg),
        'tls-permissive': GLib.Variant('b', noverifyssl),
    }
    ref = RpmOstree.varsubst_baserarch('lirios/unstable/${basearch}/desktop')
    remote_name = 'lirios'
    remote_url = 'https://repo.liri.io/ostree/repo/'
    install_path = libcalamares.globalstorage.value('rootMountPoint')

    # Initialize sysroot
    subprocess.run(['ostree', 'admin', '--sysroot=' + install_path,
                    'init-fs', install_path], check=True)

    # Load sysroot
    sysroot_file = Gio.File.new_for_path(install_path)
    sysroot = OSTree.Sysroot.new(sysroot_file)
    sysroot.load(cancellable)

    # We don't support resuming from interrupted installs
    repo = sysroot.get_repo(None)[1]
    repo.set_disable_fsync(True)

    repo.remote_change(None, OSTree.RepoRemoteChange.ADD_IF_NOT_EXISTS,
                       remote_name, remote_url,
                       GLib.Variant('a{sv}', remote_options), cancellable)

    progress = OSTree.AsyncProgress.new()
    progress.connect('changed', progress_cb)

    # Pull
    pull_options = {'refs': GLib.Variant('as', [ref])}
    try:
        repo.pull_with_options(remote_name,
                GLib.Variant('a{sv}', pull_options),
                progress, cancellable)
    except GLib.GError as e:
        libcalamares.utils.error('Failed to pull from repository')
        return ('Failed to pull from repository', e.message)

    # Deploy
    subprocess.check_call(['ostree', 'admin', '--sysroot=' + install_path,
        'os-init', osname])
    subprocess.check_call(['ostree', 'admin', '--sysroot=' + install_path,
        'deploy', '--os=' + osname, '%s:%s' % (remote_name, ref)])

    # Determine the path of the new deployment
    sysroot.load(None)
    deployments = sysroot.get_deployments()
    if len(deployments) > 0:
        libcalamares.utils.error('No deployments available')
        return ('No deployments found', 'OSTree failed to deploy operating system.')
    deployment = deployments[0]
    deployment_path = sysroot.get_deployment_directory(deployment).get_path()
    libcalamares.utils.debug('Deployment path: %s\n' % deployment_path)

    return None


def progress_cb(async_progress):
    accumulator = '** OSTree'
    status = async_progress.get_status()
    outstanding_fetches = async_progress.get_uint('outstanding-fetches')
    if status:
        accumulator += '\nStatus: ' + status
    elif outstanding_fetches > 0:
        fetched = async_progress.get_uint('fetched')
        requested = async_progress.get_uint('requested')
        if requested == 0:
            percent = 0.0
        else:
            percent = (fetched * (1.0 / requested)) * 100
        libcalamares.job.setprogress(percent)
    libcalamares.utils.debug(accumulator)
