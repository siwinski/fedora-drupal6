%define drupaldir %{_datadir}/drupal6
Name: drupal6
Version:  6.22
Release:  3%{?dist}
Summary: An open-source content-management platform

Group: Applications/Publishing
License: GPL+
URL: http://www.drupal.org
Source0: http://ftp.osuosl.org/pub/drupal/files/projects/drupal-%{version}.tar.gz
Source1: %{name}.conf
Source2: drupal-README.fedora
Source3: %{name}-cron
Source4: drupal-files-migrator.sh
Patch0: drupal-6.0-scripts-noshebang.patch

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: php, php-gd, php-mbstring, wget

%description
Equipped with a powerful blend of features, Drupal is a Content Management 
System written in PHP that can support a variety of websites ranging from
personal weblogs to large community-driven websites.  Drupal is highly
configurable, skinnable, and secure.

%prep

%setup -q -n drupal-%{version}

%patch0 -p1
chmod -x scripts/drupal.sh

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{drupaldir}
cp -pr * %{buildroot}%{drupaldir}
cp -pr .htaccess %{buildroot}%{drupaldir}
mkdir -p %{buildroot}%{_sysconfdir}/httpd
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
cp -pr %SOURCE1 %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mv %{buildroot}%{drupaldir}/sites/* %{buildroot}%{_sysconfdir}/%{name}
rmdir %{buildroot}%{drupaldir}/sites
ln -s ../../..%{_sysconfdir}/%{name} %{buildroot}%{drupaldir}/sites
mkdir -p %{buildroot}%{_docdir}
cp -pr %SOURCE2 .
install -D -p -m 0644 %SOURCE3 %{buildroot}%{_sysconfdir}/cron.hourly/%{name}
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/files/default
ln -s ../../..%{_localstatedir}/lib/%{name}/files/default %{buildroot}%{_sysconfdir}/%{name}/default/files
cp -pr %SOURCE4 .
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mv %{buildroot}%{drupaldir}/.htaccess %{buildroot}%{_sysconfdir}/httpd/conf.d/drupal6-site.htaccess
ln -s ../../../%{_sysconfdir}/httpd/conf.d/drupal6-site.htaccess %{buildroot}%{drupaldir}/.htaccess

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt INSTALL* LICENSE* MAINTAINERS.txt UPGRADE.txt drupal-README.fedora sites/all/README.txt drupal-files-migrator.sh
%{drupaldir}
%exclude %{drupaldir}/CHANGELOG.txt
%exclude %{drupaldir}/INSTALL* 
%exclude %{drupaldir}/LICENSE* 
%exclude %{drupaldir}/MAINTAINERS.txt 
%exclude %{drupaldir}/UPGRADE.txt
%dir %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/%{name}/all
%exclude %{_sysconfdir}/%{name}/all/README.txt
%config(noreplace) %{_sysconfdir}/%{name}/default
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}*.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}*.htaccess
%attr(755,root,apache) %config(noreplace) %{_sysconfdir}/cron.hourly/%{name}
%dir %attr(775,root,apache) %{_localstatedir}/lib/%{name}/
%dir %attr(775,root,apache) %{_localstatedir}/lib/%{name}/files/
%dir %attr(775,root,apache) %{_localstatedir}/lib/%{name}/files/default/

%changelog
* Thu Jun 30 2011 Jon Ciesla <limb@jcomserv.net> - 6.22-3
- Drop unneeded dirs in /etc/drupal6, BZ 706735.

* Fri Jun 17 2011 Jon Ciesla <limb@jcomserv.net> - 6.22-2
- Bump and rebuild for BZ 712251.

* Thu May 26 2011 Jon Ciesla <limb@jcomserv.net> - 6.22-1
- Update to 6.22, SA-CORE-2011-001.

* Thu Feb 24 2011 Jon Ciesla <limb@jcomserv.net> - 6.20-1
- Update to 6.20.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 12 2010 Jon Ciesla <limb@jcomserv.net> - 6.19-1
- Update to 6.19, SA-CORE-2010-002.
- Moved .htaccess to /etc/httpd/conf.d/drupal6-site.htaccess and symlinked, per review.

* Tue Jul 13 2010 Jon Ciesla <limb@jcomserv.net> - 6.17-2
- Fixed license tag.

* Mon Jun 28 2010 Jon Ciesla <limb@jcomserv.net> - 6.17-1
- Update to 6.17, review fixes.

* Mon Mar 08 2010 Jon Ciesla <limb@jcomserv.net> - 6.16-1
- Update to 6.16, SA-CORE-2010-001.

* Thu Dec 17 2009 Jon Ciesla <limb@jcomserv.net> - 6.15-1
- Update to 6.15, SA-CORE-2009-009.

* Wed Sep 16 2009 Jon Ciesla <limb@jcomserv.net> - 6.14-1
- Update to 6.14, SA-CORE-2009-008.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Jon Ciesla <limb@jcomserv.net> - 6.13-1
- Update to 6.11, SA-CORE-2009-007.
- Added clarifying text on module installation to readme, BZ 500707.

* Thu May 14 2009 Jon Ciesla <limb@jcomserv.net> - 6.12-1
- Update to 6.11, SA-CORE-2009-006.

* Thu Apr 30 2009 Jon Ciesla <limb@jcomserv.net> - 6.11-1
- Update to 6.11, SA-CORE-2009-005.

* Mon Apr 27 2009 Jon Ciesla <limb@jcomserv.net> - 6.10-2
- Added SELinux/sendmail note to README, BZ 497642.

* Thu Feb 26 2009 Jon Ciesla <limb@jcomserv.net> - 6.10-1
- Update to 6.10, SA-CORE-2009-003.

* Tue Feb 17 2009 Jon Ciesla <limb@jcomserv.net> - 6.9-2
- Drop pre script for files move, 472642.
- Updated drupal-README.fedora.
- Mark cron job noreplace, BZ 485567.

* Thu Jan 15 2009 Jon Ciesla <limb@jcomserv.net> - 6.9-1
- Upgrade to 6.9, SA-CORE-2009-001.

* Fri Jan 02 2009 Jon Ciesla <limb@jcomserv.net> - 6.8-1
- Upgrade to 6.8.
- Move files directories from sites to /var/lib/drupal/files/N for selinux reasons, 472642.
- Included script to move files outside of default, use at your own risk, patches welcome.

* Thu Dec 11 2008 Jon Ciesla <limb@jcomserv.net> - 6.7-1
- Upgrade to 6.7, SA-2008-073.

* Wed Oct 22 2008 Jon Ciesla <limb@jcomserv.net> - 6.6-1
- Upgrade to 6.6, SA-2008-067.

* Thu Oct 09 2008 Jon Ciesla <limb@jcomserv.net> - 6.5-1
- Upgrade to 6.5, SA-2008-060.
- Added notes to README and drupal.conf re CVE-2008-3661.

* Thu Aug 14 2008 Jon Ciesla <limb@jcomserv.net> - 6.4-1
- Upgrade to 6.4, SA-2008-047.

* Thu Jul 10 2008 Jon Ciesla <limb@jcomserv.net> - 6.3-1
- Upgrade to 6.3, upstream security fixes, SA-2008-044.

* Thu Apr 10 2008 Jon Ciesla <limb@jcomserv.net> - 6.2-1
- Upgrade to 6.2, upstream security fixes, SA-2008-026.

* Thu Feb 28 2008 Jon Ciesla <limb@jcomserv.net> - 6.1-1
- Upgrade to 6.1, upstream security fixes, SA-2008-018.

* Fri Feb 22 2008 Jon Ciesla <limb@jcomserv.net> - 6.0-1
- Upgrade to 6.0.
- Updated noshebang patch.

* Mon Feb 04 2008 Jon Ciesla <limb@jcomserv.net> - 5.7-1
- Upgrade to 5.7, several non-security bugs fixed.

* Fri Jan 11 2008 Jon Ciesla <limb@jcomserv.net> - 5.6-1
- Upgrade to 5.6, upstream security fixes.

* Mon Jan 07 2008 Jon Ciesla <limb@jcomserv.net> - 5.5-2
- Include .htaccess file, BZ 427720.

* Mon Dec 10 2007 Jon Ciesla <limb@jcomserv.net> - 5.5-1
- Upgrade to 5.5, critical fixes.

* Thu Dec 06 2007 Jon Ciesla <limb@jcomserv.net> - 5.4-2
- Fix /files -> /var/lib/drupal dir perms, BZ 414761.

* Wed Dec 05 2007 Jon Ciesla <limb@jcomserv.net> - 5.4-1
- Upgrade to 5.4, advisory ID DRUPAL-SA-2007-031.
- Augmented README regarding symlinks, BZ 254228.

* Thu Oct 18 2007 Jon Ciesla <limb@jcomserv.net> - 5.3-1
- Upgrade to 5.3, fixes:
- HTTP response splitting.
- Arbitrary code execution.
- Cross-site scripting.
- Cross-site request forgery.
- Access bypass.

* Mon Sep 24 2007 Jon Ciesla <limb@jcomserv.net> - 5.2-3
- Minor doc correction, BZ 301541.

* Thu Aug 16 2007 Jon Ciesla <limb@jcomserv.net> - 5.2-2
- License tag correction.

* Thu Jul 26 2007 Jon Ciesla <limb@jcomserv.net> - 5.2-1
- Upgrade to 5.2, Cross-site request forgery fix.

* Fri Jul 20 2007 Jon Ciesla <limb@jcomserv.net> - 5.1-5
- Corrected buildroot.
- Moved /etc/drupal/all/README.txt to correct place.

* Wed Jul 04 2007 Jon Ciesla <limb@jcomserv.net> - 5.1-4
- Made settings.php not readonly by default, with note in drupal-README.fedora
- Locked down initial security configuration, documented steps required.
- Description cleanup.
- Added wget requires.

* Wed Jun 06 2007 Jon Ciesla <limb@jcomserv.net> - 5.1-3
- Fixed initial setting.php perms.
- Added files dir.

* Wed May 30 2007 Jon Ciesla <limb@jcomserv.net> - 5.1-2
- Fixed category, duped docs, apache restart, cron job.

* Wed May 30 2007 Jon Ciesla <limb@jcomserv.net> - 5.1-1
- Initial packaging.
