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

import json
import subprocess
import tempfile
import libcalamares
import os

def mkdir_p(path):
    """
    Creates all subdirectories leading to the path.

    :param path: Path
    """
    if not os.path.exists(path):
        os.makedirs(path)


def bind_mount(src, dest=None, bind_ro=False, recurse=True):
    """
    Bind mount source to destination.

    :param src: Source path
    :param dest: Destination path
    :param bind_ro: Mount read-only
    :param recurse: Use --rbind to recurse, otherwise plain --bind
    """

    if libcalamares.globalstorage.contains('ostreeMountPoints'):
        mountpoints = libcalamares.globalstorage.value('ostreeMountPoints')
    else:
        mountpoints = []

    # Same basename by default
    if dest is None:
        dest = src

    # Make sure the mount point is created
    mkdir_p(dest)

    # Determine bind argument
    if bind_ro:
        subprocess.check_call(['mount', '--bind', src, src])
        subprocess.check_call(['mount', '--bind', '-o', 'remount,ro', src, src])
        mountpoints.append(src)
        mountpoints.append(src)
    else:
        if recurse:
            bindopt = '--rbind'
        else:
            bindopt = '--bind'
        subprocess.check_call(['mount', bindopt, src, dest])
        mountpoints.append(dest)

    libcalamares.globalstorage.insert('ostreeMountPoints', mountpoints)


def copy_bootloader_data():
    """
    Copy bootloader data files from the deployment checkout to
    the target root.
    """

    fw_type = libcalamares.globalstorage.value('firmwareType')
    install_path = libcalamares.globalstorage.value('rootMountPoint')
    deployment_path = libcalamares.globalstorage.value('ostreeDeploymentPath')

    # Destination directory
    boot_path = install_path + '/boot'

    # Where to find the data files
    source_path = deployment_path + '/usr/lib/ostree-boot'
    if not os.path.isdir(source_path):
        source_path = deployment_path + '/boot'

    # Copy data files
    for fname in os.listdir(source_path):
        src_path = os.path.join(source_path, fname)
        dest_path = os.path.join(boot_path, fname)

        # We want to copy only directories
        if not os.path.isdir(src_path):
            continue

        # Special case for EFI subdirectory
        if fname == 'efi':
            if fw_type == 'efi':
                for subname in os.listdir(src_path):
                    sub_srcpath = os.path.join(src_path, subname)
                    sub_destpath = os.path.join(dest_path, subname)
                    subprocess.check_call(['cp', '-r', '-p', sub_srcpath, sub_destpath])
        else:
            subprocess.check_call(['cp', '-r', '-p', src_path, dest_path])

    # /boot/grub2/grubenv is a symlink to a file inside /boot/efi,
    # remove it on BIOS systems since the target path doesn't exist
    efi_grubenv_link = boot_path + '/grub2/grubenv'
    if fw_type != 'efi' and os.path.islink(efi_grubenv_link):
        os.unlink(efi_grubenv_link)

    # rpm-ostree creates /boot/loader/grub.cfg when using grub, so
    # we must link the traditional /boot/grub2/grub.cfg to it
    grubcfg_orig = boot_path + '/grub2/grub.cfg'
    if os.path.exists(grubcfg_orig):
        os.unlink(grubcfg_orig)
    os.symlink('../loader/grub.cfg', grubcfg_orig)

    libcalamares.utils.debug(f'All boot loader data files copied to {boot_path}')


def create_tmpfiles():
    """
    Create temporary files and directories.
    """

    new_install_path = libcalamares.globalstorage.value('rootMountPoint')
    subprocess.run(['systemd-tmpfiles', '--create', '--boot',
                    '--root=' + new_install_path], check=False)


def build_new_root():
    """
    Create a new root from the deployment.
    """

    partitions = libcalamares.globalstorage.value('partitions')
    install_path = libcalamares.globalstorage.value('rootMountPoint')
    deployment_path = libcalamares.globalstorage.value('ostreeDeploymentPath')

    # We create a new root with part from the deployment and part from the physical root
    new_install_path = tempfile.mkdtemp(prefix='ostree-root-')
    libcalamares.globalstorage.insert('oldRootMountPoint', install_path)
    libcalamares.globalstorage.insert('rootMountPoint', new_install_path)
    mkdir_p(new_install_path)

    # Bind mount deployment to the new root mount point
    bind_mount(deployment_path, dest=new_install_path)

    # Bind mount all partitions
    for partition in partitions:
        if partition['mountPoint'] in ('/', '/boot', '/var'):
            continue
        bind_mount(install_path + partition['mountPoint'], dest=new_install_path + partition['mountPoint'])

    # Always bind mount /boot and /var into the new root, regardless of being separate partitions
    bind_mount(install_path + '/boot', dest=new_install_path + '/boot')
    if os.path.exists(install_path + '/var'):
        bind_mount(install_path + '/var', dest=new_install_path + '/var')
    else:
        var_path = install_path + '/ostree/deploy/lirios/var'
        bind_mount(var_path, dest=new_install_path + '/var')

    # Bind mount the old root as /sysroot
    bind_mount(install_path, dest=new_install_path + '/sysroot')

    # Now bind mount /dev, /sys and /proc
    for mount_point in ('/dev', '/sys', '/proc'):
        bind_mount(mount_point, dest=new_install_path + mount_point, recurse=False)

    libcalamares.utils.debug(f'New root at {new_install_path} ready')


def run():
    """
    Install the OS tree on the root file system.
    """

    # Installation path
    install_path = libcalamares.globalstorage.value('rootMountPoint')
    if not install_path:
        return ("No mount point for root partition in globalstorage",
                "globalstorage does not contain a \"rootMountPoint\" key, "
                "doing nothing")
    if not os.path.exists(install_path):
        return (f"Bad mount point for root partition in globalstorage",
                 "globalstorage[\"rootMountPoint\"] is \"{install_path}\", which does not "
                 "exist, doing nothing")

    progname = '/usr/bin/calamares-ostree-install'

    # The Calamares Python interpreter freezes when loading gobject-introspection, so we moved the
    # code to an external process

    if os.path.isdir('/ostree/repo'):
        url = 'file:///ostree/repo'
    else:
        url = libcalamares.job.configuration['url']
    ref = libcalamares.job.configuration['ref']

    deployment_path = None

    with subprocess.Popen([progname, url, ref, install_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        while True:
            line = p.stdout.readline().rstrip().decode('utf-8')
            if not line:
                break

            if line.startswith('PROGRESS:'):
                percent = float(line[9:])
                libcalamares.job.setprogress(percent)
            elif line.startswith('RESULT:'):
                deployment_path = line[7:]
                libcalamares.globalstorage.insert('ostreeDeploymentPath', deployment_path)
            elif line.startswith('OUTPUT:'):
                libcalamares.utils.debug(line[7:])
            elif line.startswith('ERROR:'):
                json.loads(line[6:])
                break
            elif line.startswith('QUIT'):
                break

    if deployment_path is None:
        return ('No deployment path', 'Unable to find OS tree deployment.')

    # Copy boot loader files
    copy_bootloader_data()

    # Build a new root with the deployment
    build_new_root()

    # Create temporary files and directories
    create_tmpfiles()

    # Reverse mountpoints list so that it's ready for next stages
    mountpoints = libcalamares.globalstorage.value('ostreeMountPoints')
    mountpoints.reverse()
    libcalamares.globalstorage.insert('ostreeMountPoints', mountpoints)

    return None
