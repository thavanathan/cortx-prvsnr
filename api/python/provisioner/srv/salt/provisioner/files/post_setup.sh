#!/bin/bash
#
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.
#


set -eu

verbosity="${1:-0}"

if [[ "$verbosity" -ge 2 ]]; then
    set -x
fi

# TODO EOS-11551 remove env routine later
# Does same as above, but recommended way of setting Global Envisonment Variables
cat > /etc/profile.d/set_path_env << EOM
#!/bin/sh
echo $PATH | grep -q "/usr/local/bin" || export PATH=$PATH:/usr/local/bin
EOM
. /etc/profile.d/set_path_env



# Create SEAGATE_USER_HOME_DIR requried for create users
mkdir -p "/opt/seagate/users"
chmod 644 "/opt/seagate/users"

# set api
prvsnr_group=prvsnrusers
echo "Creating group '$prvsnr_group'..."
groupadd -f "$prvsnr_group"

shared_dir=/var/lib/seagate/cortx/provisioner/shared
factory_profile_dir="${shared_dir}/factory_profile"
user_srv_dir="${shared_dir}/srv"
user_srv_fileroot_dir="${user_srv_dir}/salt"
user_srv_pillar_dir="${user_srv_dir}/pillar"

seagate_log_dir=/var/log/seagate
prvsnr_log_dir="${seagate_log_dir}/provisioner"

user_srv_fileroot_dir_old=/opt/seagate/cortx/provisioner/srv_user   # FIXME deprecate that
user_srv_pillar_dir_old=/opt/seagate/cortx/provisioner/pillar/user  # FIXME deprecate that

echo "Creating group '$prvsnr_group'..."
groupadd -f "$prvsnr_group"

echo "Configuring access for provisioner data ..."
# TODO IMPROVE EOS-9581 consider to remove _old dirs someday
for path in "$factory_profile_dir" \
            "$user_srv_fileroot_dir" \
            "$user_srv_pillar_dir" \
            "$prvsnr_log_dir" \
            "$user_srv_fileroot_dir_old" \
            "$user_srv_pillar_dir_old"; do
    mkdir -p "$path"
done

for path in "$user_srv_dir" \
            "$factory_profile_dir" \
            "$seagate_log_dir" \
            "$prvsnr_log_dir" \
            "$user_srv_fileroot_dir_old" \
            "$user_srv_pillar_dir_old"; do
    if [[ "$path" == "$seagate_log_dir" ]]; then
        chmod o+rx "$path"
    else
        find "$path" -exec chown :"$prvsnr_group" {} \;
        if [[ "$path" == "$factory_profile_dir" ]]; then
            # profile is expected to be copied to user space before appliance
            find "$path" -exec chmod g+r {} \; -exec chmod g-w {} \;
        else
            find "$path" -exec chmod g+rw {} \;
            find "$path" -type d -exec chmod g+s {} \;  # TODO ??? might be not necessary since setfacl is used
            find "$path" -type d -exec setfacl -dm g:"$prvsnr_group":rwx {} \;
        fi
    fi
done


# Provisioning cli directory
test -e ${PWD}/api/python/setup.py && \
  install_dir=${PWD} || \
  install_dir=/opt/seagate/cortx/provisioner

chown -R :"$prvsnr_group" "${install_dir}/cli"
chmod -R 750 "${install_dir}/cli"