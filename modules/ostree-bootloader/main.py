#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014, Aurélien Gâteau <agateau@kde.org>
#   Copyright 2014, Anke Boersma <demm@kaosx.us>
#   Copyright 2014, Daniel Hillenbrand <codeworkx@bbqlinux.org>
#   Copyright 2014, Benjamin Vaudour <benjamin.vaudour@yahoo.fr>
#   Copyright 2014, Kevin Kofler <kevin.kofler@chello.at>
#   Copyright 2015-2017, Philip Mueller <philm@manjaro.org>
#   Copyright 2016-2017, Teo Mrnjavac <teo@kde.org>
#   Copyright 2017, Alf Gaida <agaida@siduction.org>
#   Copyright 2017, Adriaan de Groot <groot@kde.org>
#   Copyright 2017, Gabriel Craciunescu <crazy@frugalware.org>
#   Copyright 2019, Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import subprocess

import libcalamares

from libcalamares.utils import check_target_env_call


def get_uuid():
    """
    Checks and passes 'uuid' to other routine.

    :return:
    """
    root_mount_point = libcalamares.globalstorage.value('rootMountPoint')
    print('Root mount point: "{!s}"'.format(root_mount_point))
    partitions = libcalamares.globalstorage.value('partitions')
    print('Partitions: "{!s}"'.format(partitions))

    for partition in partitions:
        if partition['mountPoint'] == '/':
            print('Root partition uuid: "{!s}"'.format(partition['uuid']))
            return partition['uuid']

    return ''


def install_systemd_boot(efi_directory):
    """
    Installs systemd-boot as bootloader for EFI setups.

    :param efi_directory:
    """
    print('Bootloader: systemd-boot')
    install_path = libcalamares.globalstorage.value('rootMountPoint')
    install_efi_directory = install_path + efi_directory
    subprocess.call(['bootctl',
                     '--path={!s}'.format(install_efi_directory),
                     'install'])


def install_grub(efi_directory, fw_type):
    """
    Installs grub as bootloader, either in pc or efi mode.

    :param efi_directory:
    :param fw_type:
    """
    if fw_type == 'efi':
        print('Bootloader: grub (efi)')
        install_path = libcalamares.globalstorage.value('rootMountPoint')
        install_efi_directory = install_path + efi_directory

        if not os.path.isdir(install_efi_directory):
            os.makedirs(install_efi_directory)

        if 'efiBootloaderId' in libcalamares.job.configuration:
            efi_bootloader_id = libcalamares.job.configuration[
                                    'efiBootloaderId']
        else:
            branding = libcalamares.globalstorage.value('branding')
            distribution = branding['bootloaderEntryName']
            file_name_sanitizer = str.maketrans(' /', '_-')
            efi_bootloader_id = distribution.translate(file_name_sanitizer)
        # get bitness of the underlying UEFI
        try:
            sysfile = open('/sys/firmware/efi/fw_platform_size', 'r')
            efi_bitness = sysfile.read(2)
        except Exception:
            # if the kernel is older than 4.0, the UEFI bitness likely isn't
            # exposed to the userspace so we assume a 64 bit UEFI here
            efi_bitness = '64'
        bitness_translate = {'32': '--target=i386-efi',
                             '64': '--target=x86_64-efi'}
        check_target_env_call([libcalamares.job.configuration['grubInstall'],
                               bitness_translate[efi_bitness],
                               '--efi-directory=' + efi_directory,
                               '--bootloader-id=' + efi_bootloader_id,
                               '--force'])

        # VFAT is weird, see issue CAL-385
        install_efi_directory_firmware = (vfat_correct_case(
                                              install_efi_directory,
                                              'EFI'))
        if not os.path.exists(install_efi_directory_firmware):
            os.makedirs(install_efi_directory_firmware)

        # there might be several values for the boot directory
        # most usual they are boot, Boot, BOOT

        install_efi_boot_directory = (vfat_correct_case(
                                          install_efi_directory_firmware,
                                          'boot'))
        if not os.path.exists(install_efi_boot_directory):
            os.makedirs(install_efi_boot_directory)

        # Workaround for some UEFI firmwares
        efi_file_source = {'32': os.path.join(install_efi_directory_firmware,
                                              efi_bootloader_id,
                                              'grubia32.efi'),
                           '64': os.path.join(install_efi_directory_firmware,
                                              efi_bootloader_id,
                                              'grubx64.efi')}

        efi_file_target = {'32': os.path.join(install_efi_boot_directory,
                                              'bootia32.efi'),
                           '64': os.path.join(install_efi_boot_directory,
                                              'bootx64.efi')}

        shutil.copy2(efi_file_source[efi_bitness], efi_file_target[efi_bitness])
    else:
        print('Bootloader: grub (bios)')
        if libcalamares.globalstorage.value('bootLoader') is None:
            return

        boot_loader = libcalamares.globalstorage.value('bootLoader')
        if boot_loader['installPath'] is None:
            return

        check_target_env_call([libcalamares.job.configuration['grubInstall'],
                               '--target=i386-pc',
                               '--recheck',
                               '--force',
                               boot_loader['installPath']])

    # The file specified in grubCfg should already be filled out
    # by the grubcfg job module.
    check_target_env_call([libcalamares.job.configuration['grubMkconfig'],
                           '-o', libcalamares.job.configuration['grubCfg']])


def vfat_correct_case(parent, name):
    for candidate in os.listdir(parent):
        if name.lower() == candidate.lower():
            return os.path.join(parent, candidate)
    return os.path.join(parent, name)


def prepare_bootloader(fw_type):
    """
    Prepares bootloader.
    Based on value 'efi_boot_loader', it either calls systemd-boot
    or grub to be installed.

    :param fw_type:
    :return:
    """
    efi_boot_loader = libcalamares.job.configuration['efiBootLoader']
    efi_directory = libcalamares.globalstorage.value('efiSystemPartition')

    if efi_boot_loader == 'systemd-boot' and fw_type == 'efi':
        install_systemd_boot(efi_directory)
    else:
        install_grub(efi_directory, fw_type)


def set_kernel_args():
    """
    Set kernel arguments using rpm-ostree.

    :return:
    """
    install_path = libcalamares.globalstorage.value('rootMountPoint')
    kernel_args = libcalamares.job.configuration.get('kernelArguments', '')

    kernel_params = []

    partitions = libcalamares.globalstorage.value('partitions')

    uuid = get_uuid()
    swap_uuid = ''

    cryptdevice_params = []

    cryptdevice_params = []

    # Take over swap settings:
    #  - unencrypted swap partition sets swap_uuid
    #  - encrypted root sets cryptdevice_params
    for partition in partitions:
        has_luks = 'luksMapperName' in partition
        if partition['fs'] == 'linuxswap' and not has_luks:
            swap_uuid = partition['uuid']

        if partition['mountPoint'] == '/' and has_luks:
            cryptdevice_params = ['cryptdevice=UUID='
                                  + partition['luksUuid']
                                  + ':'
                                  + partition['luksMapperName'],
                                  'root=/dev/mapper/'
                                  + partition['luksMapperName'],
                                  'resume=/dev/mapper/'
                                  + partition['luksMapperName']]

    if cryptdevice_params:
        kernel_params.extend(cryptdevice_params)
    else:
        kernel_params.append('root=UUID={!s}'.format(uuid))

    if swap_uuid:
        kernel_params.append('resume=UUID={!s}'.format(swap_uuid))

    # Append kernel arguments
    conf_path = install_path + '/boot/loader/entries/ostree-1-lirios.conf'
    conf_lines = []
    with open(conf_path, 'r') as conf_file:
        for line in conf_file.readlines():
            line = line.rstrip()
            if line.startswith('options '):
                line += ' ' + ' '.join(kernel_params)
                if kernel_args:
                    line += ' ' + kernel_args
            conf_lines.append(line)
    with open(conf_path, 'w') as conf_file:
        for line in conf_lines:
            conf_file.write(line + '\n')


def run():
    """
    Starts procedure and passes 'fw_type' to other routine.

    :return:
    """

    fw_type = libcalamares.globalstorage.value('firmwareType')

    if (libcalamares.globalstorage.value('bootLoader') is None
            and fw_type != 'efi'):
        return None

    partitions = libcalamares.globalstorage.value('partitions')

    if fw_type == 'efi':
        esp_found = False

        for partition in partitions:
            if (partition['mountPoint'] ==
                    libcalamares.globalstorage.value('efiSystemPartition')):
                esp_found = True

        if not esp_found:
            return None

    set_kernel_args()
    prepare_bootloader(fw_type)

    return None
