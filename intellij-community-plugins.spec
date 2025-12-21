# setting some global constants
%global appname intellij
%global plugins_dir plugins

# disable debuginfo subpackage
%global debug_package %{nil}

# Disable build-id symlinks to avoid conflicts
%global _build_id_links none
# don't strip bundled binaries
%global __strip /bin/true
# dont repack jars
%global __jar_repack %{nil}
# disable rpath checks
%define __brp_check_rpaths %{nil}

# do not automatically detect and export provides and dependencies on bundled libraries and executables
%global __provides_exclude_from %{_javadir}/%{appname}-community/%{plugins_dir}/.*
%global __requires_exclude_from %{_javadir}/%{appname}-community/%{plugins_dir}/.*

# NOTE: You must update these versions to match the IntelliJ IDEA build version (e.g. 243.* for 2024.3)
# These are placeholders based on the original file.

# https://plugins.jetbrains.com/plugin/8183-gitlink/versions
%global repmapper_version 4.5.3
%global repmapper_id 839423
%global repmapper_name GitLink
%global repmapper_archive %{repmapper_name}-%{repmapper_version}

# https://plugins.jetbrains.com/plugin/12552-rpm-spec-file/versions
%global rpm_spec_file_version 2.3.0
%global rpm_spec_file_id 810018
%global rpm_spec_file_name intellij-rpmspec
%global rpm_spec_file_archive %{rpm_spec_file_name}-%{rpm_spec_file_version}

# https://plugins.jetbrains.com/plugin/7724-docker/versions
%global docker_integration_version 252.27397.129
%global docker_integration_id 884806
%global docker_integration_name clouds-docker-impl
%global docker_integration_archive %{docker_integration_name}-%{docker_integration_version}

# https://plugins.jetbrains.com/plugin/164-ideavim/versions
%global ideavim_version 2.27.2
%global ideavim_id 835262
%global ideavim_name IdeaVIM
%global ideavim_archive %{ideavim_name}-%{ideavim_version}

# https://plugins.jetbrains.com/plugin/6981-ini/versions
%global ini_version 252.27397.129
%global ini_id 884814
%global ini_name ini
%global ini_archive %{ini_name}-%{ini_version}

# https://plugins.jetbrains.com/plugin/7566-settings-repository/versions
%global settings_repository_version 252.23892.201
%global settings_repository_id 796427
%global settings_repository_name settingsRepository
%global settings_repository_archive %{settings_repository_name}-%{settings_repository_version}

# https://plugins.jetbrains.com/plugin/7495--ignore/versions
%global ignore_plugin_version 4.5.6
%global ignore_plugin_id 678216
%global ignore_plugin_name ignore
%global ignore_plugin_archive ignore-%{ignore_plugin_version}

# https://plugins.jetbrains.com/plugin/9525--env-files/versions
%global env_files_version 252.23892.201
%global env_files_id 796325
%global env_files_name dotenv
%global env_files_archive %{env_files_name}-%{env_files_version}

# https://plugins.jetbrains.com/plugin/22282-jetbrains-ai-assistant/versions
%global ai_assistant_version 252.27397.130
%global ai_assistant_id 884745
%global ai_assistant_name ml-llm
%global ai_assistant_archive %{ai_assistant_name}-%{ai_assistant_version}

Name:          %{appname}-community-plugins
Version:       2024.3.1
Release:       1%{?dist}

Summary:       Plugins for IntelliJ IDEA Community Edition
License:       Apache-2.0
URL:           https://www.jetbrains.com/idea/

Source0:       https://github.com/phracek/pycharm-community-edition/raw/master/copr-workaround.tar.xz
Source1:       https://plugins.jetbrains.com/files/8183/%{repmapper_id}/%{repmapper_archive}.zip#/%{repmapper_name}-%{repmapper_version}.zip
Source2:       https://plugins.jetbrains.com/files/12552/%{rpm_spec_file_id}/%{rpm_spec_file_archive}.zip#/%{rpm_spec_file_name}-%{rpm_spec_file_version}.zip
Source3:       https://plugins.jetbrains.com/files/7724/%{docker_integration_id}/%{docker_integration_archive}.zip#/%{docker_integration_name}-%{docker_integration_version}.zip
Source4:       https://plugins.jetbrains.com/files/164/%{ideavim_id}/%{ideavim_archive}.zip#/%{ideavim_name}-%{ideavim_version}.zip
Source5:       https://plugins.jetbrains.com/files/6981/%{ini_id}/%{ini_archive}.zip#/%{ini_name}-%{ini_version}.zip
Source6:       https://plugins.jetbrains.com/files/7566/%{settings_repository_id}/%{settings_repository_archive}.zip#/%{settings_repository_name}-%{settings_repository_version}.zip
Source7:       https://plugins.jetbrains.com/files/7495/%{ignore_plugin_id}/%{ignore_plugin_archive}.zip#/%{ignore_plugin_name}-%{ignore_plugin_version}.zip
Source8:       https://plugins.jetbrains.com/files/9525/%{env_files_id}/%{env_files_archive}.zip#/%{env_files_name}-%{env_files_version}.zip
Source9:       https://plugins.jetbrains.com/files/22282/%{ai_assistant_id}/%{ai_assistant_archive}.zip#/%{ai_assistant_name}-%{ai_assistant_version}.zip

BuildRequires: javapackages-filesystem

Requires:      %{appname}-community%{?_isa} = %{?epoch:%{epoch}:}%{version}

ExclusiveArch: x86_64 aarch64

%description
IntelliJ IDEA Community Edition contains several plugins. This package
contains extra plugins like IdeaVIM, Docker, RPM Spec, etc.

%prep
%setup -q -c -n %{appname}-community-%{version} -T
%setup -q -n %{appname}-community-%{version} -D -T -a 1
%setup -q -n %{appname}-community-%{version} -D -T -a 2
%setup -q -n %{appname}-community-%{version} -D -T -a 3
%setup -q -n %{appname}-community-%{version} -D -T -a 4
%setup -q -n %{appname}-community-%{version} -D -T -a 5
%setup -q -n %{appname}-community-%{version} -D -T -a 6
%setup -q -n %{appname}-community-%{version} -D -T -a 7
%setup -q -n %{appname}-community-%{version} -D -T -a 8
%setup -q -n %{appname}-community-%{version} -D -T -a 9

%install
mkdir -p %{buildroot}%{_javadir}/%{appname}-community/%{plugins_dir}

# Move all plugins to plugins directory
# Note: Ensure the variable names match the extracted folder names
cp -arf ./%{repmapper_name} %{buildroot}%{_javadir}/%{appname}-community/%{plugins_dir}/
cp -arf ./%{rpm_spec_file_name} %{buildroot}%{_javadir}/%{appname}-community/%{plugins_dir}/
cp -arf ./%{docker_integration_name} %{buildroot}%{_javadir}/%{appname}-community/%{plugins_dir}/
cp -arf ./%{ideavim_name} %{buildroot}%{_javadir}/%{appname}-community/%{plugins_dir}/
cp -arf ./%{ini_name} %{buildroot}%{_javadir}/%{appname}-community/%{plugins_dir}/
cp -arf ./%{settings_repository_name} %{buildroot}%{_javadir}/%{appname}-community/%{plugins_dir}/
cp -arf ./%{ignore_plugin_name} %{buildroot}%{_javadir}/%{appname}-community/%{plugins_dir}/
cp -arf ./%{env_files_name} %{buildroot}%{_javadir}/%{appname}-community/%{plugins_dir}/
cp -arf ./%{ai_assistant_name} %{buildroot}%{_javadir}/%{appname}-community/%{plugins_dir}/

%files
%{_javadir}/%{appname}-community/%{plugins_dir}/%{repmapper_name}
%{_javadir}/%{appname}-community/%{plugins_dir}/%{rpm_spec_file_name}
%{_javadir}/%{appname}-community/%{plugins_dir}/%{docker_integration_name}
%{_javadir}/%{appname}-community/%{plugins_dir}/%{ideavim_name}
%{_javadir}/%{appname}-community/%{plugins_dir}/%{ini_name}
%{_javadir}/%{appname}-community/%{plugins_dir}/%{settings_repository_name}
%{_javadir}/%{appname}-community/%{plugins_dir}/%{ignore_plugin_name}
%{_javadir}/%{appname}-community/%{plugins_dir}/%{env_files_name}
%{_javadir}/%{appname}-community/%{plugins_dir}/%{ai_assistant_name}

%changelog
* Sun Dec 21 2024 User <user@example.com> - 2024.3.1-1
- Initial IntelliJ IDEA Community Edition plugins package
