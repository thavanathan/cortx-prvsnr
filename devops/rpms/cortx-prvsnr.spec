Name:       cortx-prvsnr
Version:    %{_cortx_prvsnr_version}
Release:    %{_build_number}_%{_cortx_prvsnr_git_ver}_%{?dist:el7}
Summary:    CORTX Provisioning.

Group:      Tools
License:    Seagate
URL:        http://gitlab.mero.colo.seagate.com/eos/provisioner/ees-prvsnr
Source:     %{name}-%{version}-%{_cortx_prvsnr_git_ver}.tar.gz

BuildRequires: python36-devel

Requires: python36
Requires: python36-PyYAML
Requires: python36-pip
Requires: rsync
#Requires: salt-master = 2019.2.0
#Requires: salt-minion = 2019.2.0
#Requires: salt-ssh
#Requires: salt-syndic


%description
CORTX Provisioning to deploy CORTX Object storage software.


%prep
%setup -n %{name}-%{version}-%{_cortx_prvsnr_git_ver}
rm -rf %{buildroot}


%build
# Turn off the brp-python-bytecompile automagic
%global _python_bytecompile_extra 0
%global __python %{__python3}



%install
# Create directories
#mkdir -p %{buildroot}/opt/seagate/cortx/provisioner
mkdir -p %{buildroot}/opt/seagate/cortx/provisioner/{files,conf}

# Copy files
cp -R cli %{buildroot}/opt/seagate/cortx/provisioner
cp -R pillar %{buildroot}/opt/seagate/cortx/provisioner
cp -R srv %{buildroot}/opt/seagate/cortx/provisioner
# TODO EOS-11551 remove later
cp -R api %{buildroot}/opt/seagate/cortx/provisioner
cp -R files/conf %{buildroot}/opt/seagate/cortx/provisioner/


%clean
rm -rf %{buildroot}


%files
# %config(noreplace) /opt/seagate/cortx/provisioner/%{name}.yaml
/opt/seagate/cortx/provisioner/cli
/opt/seagate/cortx/provisioner/files
/opt/seagate/cortx/provisioner/pillar
/opt/seagate/cortx/provisioner/srv
# TODO EOS-11551 remove later
/opt/seagate/cortx/provisioner/api
/opt/seagate/cortx/provisioner/conf

# TODO EOS-11551 remove later
%post
api_dir="/opt/seagate/cortx/provisioner/api/python"
echo "Configuring access for provisioner data ..."
bash "${api_dir}/provisioner/srv/salt/provisioner/files/post_setup.sh"

#   install api globally using pip
pip3 install "${api_dir}"


%preun
# uninstall api globally using pip (only for pkg uninstall)
if [ $1 -eq 0 ] ; then
    pip3 uninstall -y cortx-prvsnr
fi