# coding=utf-8
from proxy.params.PackageName import *

# Jira API
JIRA_HOST = 'http://jira.n.xiaomi.com'
JIRA_PORT = 80
JIRA_ISSUE_LINK = JIRA_HOST + "/browse/{issueIdOrKey}"
JIRA_CREATE_ISSUE_API = '/rest/api/2/issue/'
JIRA_EDIT_ISSUE_API = '/rest/api/2/issue/{issueIdOrKey}'
JIRA_ADD_ATTACHMENT_API = '/rest/api/2/issue/{issueIdOrKey}/attachments'
JIRA_ADD_COMMENT_API = '/rest/api/2/issue/{issueIdOrKey}/comment'
JIRA_ADD_WATCHER_API = '/rest/api/2/issue/{issueIdOrKey}/watchers'
JIRA_TRANSITION_API = '/rest/api/2/issue/{issueIdOrKey}/transitions'

JIRA_FIELDS = "fields"
JIRA_UPDATE = "update"

# JIRA field name
PROJECT_FIELD = "project"  # {'name': 'project_name'} [set]
ISSUE_TYPE_FIELD = "issuetype"  # {'name': 'issue_type_name'} []
SUMMARY_FIELD = "summary"  # string [set]
COMPONENTS_FIELD = "components"  # [{'name': 'component'}] [add, set, remove]
PRIORITY_FIELD = "priority"  # {'name': 'priority'} [set]
BUG_TYPE_FIELD = "customfield_15660"  # {'value': 'bug_type'} [set]
REPRODUCTIVITY_FIELD = "customfield_12700"  # {'value': 'reproduce'} [set]
ASSIGNEE_FIELD = "assignee"  # user [set]
AFFECTS_VERSIONS_FIELD = "versions"  # [{'name', 'version'}] [add, set, remove]
ANDROID_VERSION_FIELD = "customfield_12600"  # [{'value': 'android_version'}] [add, set, remove]
MODEL_TAG_FIELD = "customfield_11905"  # [{'value': 'model_tag'}] [add, set, remove]
APK_VERSIONS_FIELD = "customfield_12926"  # [string, ...] [add, set, remove]
TEST_STAGE_FIELD = "customfield_14202"  # {'value': 'test_stage'} [set]
DESCRIPTION_FIELD = "description"  # string [set]
LABELS_FIELD = "labels"  # [string, ...] [add, set, remove]
DEVICE_NAME = "device_name"

# JIRA field values
# 项目(project name) {'name': 'component_name'}
# @deprecated
# PROJECT_MIUI_GLOBAL = "MIUIGLOBAL"
PROJECT_MIUI = "MIUI"

# 问题类型(issue type values) {'name': 'issue_type_name'}
ISSUE_TYPE_TASK = "Task"
ISSUE_TYPE_BUG = "bug"

# 模块(component values)
COMPONENT_GLOBAL_TABLECHECK = "Global-桌面布局"
COMPONENT_ANDROID_ONE_LAUNCHER = "Global-Android one Launcher"
COMPONENT_POCO_LAUNCHER = "Global-POCO Launcher"
COMPONENT_GLOBAL_DOWNLOAD_MANAGER = "Global-下载管理Download Manager"
COMPONENT_GLOBAL_FILE_EXPLORE = "Global-文件管理器File Explore"
COMPONENT_GLOBAL_PERSONAL_ASSISTANT = "Global-智能助理Personal Assistant"
COMPONENT_GLOBAL_BROWSER = "Global-浏览器Browser"
COMPONENT_GLOBAL_GAME_CENTER = "Global-游戏中心Games"
COMPONENT_GLOBAL_MUSIC = "Global-音乐Music"
COMPONENT_GLOBAL_THEME = "Global-国际主题 Theme"
COMPONENT_GLOBAL_TREND_NEWS = "TrendNews"
COMPONENT_GLOBAL_MI_DROP = "Global-快传Mi Drop"

# 优先级(priority values)
PRIORITY_BLOCKER = "Blocker"
PRIORITY_CRITICAL = "Critical"
PRIORITY_MAJOR = "Major"
PRIORITY_MINOR = "Minor"
PRIORITY_TRIVIAL = "Trivial"

# Bug type(bug type values) {'value': 'bug_type_value'}
BUG_TYPE_BASIC_FUNCTIONALITY = "基本功能 Basic Functionality"
BUG_TYPE_POWER_CONSUMPTION = "功耗 Power Consumption"
BUG_TYPE_PERFORMANCE = "性能 Performance"
BUG_TYPE_STABILITY = "稳定性 Stability"
BUG_TYPE_MEMORY = "内存 Memory"
BUG_TYPE_USER_EXPERIENCE = "用户体验 User Experience"
BUG_TYPE_AUTHENTICATION_PRIVACY = "认证&隐私 Authentication&Privacy"

# Reproductivity(reproductivity values )
REPRODUCTIVITY_EVERY_TIME = "必现 every time"
REPRODUCTIVITY_SOMETIMES = "偶现 sometimes"
REPRODUCTIVITY_ONCE = "一次 once"

# Android version(android version values)
ANDROID_VERSION_ALL = "All"
ANDROID_VERSION_P = "9.0"
ANDROID_VERSION_O_1 = "8.1"
ANDROID_VERSION_O = "8.0"
ANDROID_VERSION_N_1 = "7.1"
ANDROID_VERSION_N = "7.0"
ANDROID_VERSION_M = "6.0"
ANDROID_VERSION_L = "5.0"
ANDROID_VERSION_KK = "4.4"

# Test stage(test stage values)
TEST_STAGE_DEVELOPMENT = "研发测试 Development Test"
TEST_STAGE_DEVELOPMENT_ID = "16750"
TEST_STAGE_ACCEPTATION = "验收测试 Acceptation Test"
TEST_STAGE_ACCEPTATION_ID = "16751"
TEST_STAGE_FEEDBACK = "用户反馈 Feedback"
TEST_STAGE_FEEDBACK_ID = "16752"

# Model Tag(miui model values)
MODEL_TAG = {
    "beryllium_global": "E10_global",
    "sirius_global": "E2",
    "sagit_global": "C1",
    "rolex_global": "C3A //请移至闻泰项目",
    "natrium_global": "B7",
    "prada_global": "C5",
    "helium_global": "B3-652",
    "omega_global": "H3C //请移至龙旗项目",
    "markw_global": "B5W //请移至闻泰项目",
    "kate_global": "H3B //请移至龙旗项目",
    "hydrogen_global": "B3",
    "capricorn_global": "A7",
    "scorpio_global": "A4",
    "kenzo_global": "H3A //请移至龙旗项目",
    "ido_xhdpi_global": "A9 //请移至闻泰项目",
    "hennessy_global": "H3Z //请移至龙旗项目",
    "gucci_global": "H3X //请移至龙旗项目",
    "hermes_global": "H3Y //请移至龙旗项目",
    "wt88047_global": "H2X(QC) //请移至闻泰项目",
    "wt88047_pro_global": "H2X(QC) //请移至闻泰项目",
    "gemini_global": "A1",
    "latte_global": "A3",
    "comet_global": "E20",
    "ursa_global": "E8",
    "libra_global": "X11",
    "leo_global": "X7",
    "ferrari_global": "X9",
    "virgo_global": "X5",
    "mocha_global": "X6",
    "cancro_global": "X3W/X4W",
    "perseus_global": "E5_global",
    "nitrogen_global": "E4_global",
    "dipper_global": "E1_global",
    "polaris_global": "D5X_global",
    "oxygen_global": "D4",
    "chiron_global": "D5",
    "jason_global": "C8",
    "platina_global": "D2T_global",
    "lithium_global": "A8",
    "santoni_global": "A13// 请移至闻泰项目",
    "equuleus_global": "E1S_global",
    "cactus_global": "C3C_global//请移至闻泰项目",
    "cereus_global": "C3D_global//请移至闻泰项目",
    "sakura_india_global": "D1S_global//Please move to HQ",
    "ysl_global": "E6_global//请移至龙旗项目",
    "whyred_global": "E7S_global//Please move platform issues to HTH",
    "tulip_global": "E7T_global//请移至龙旗项目",
    "rosy_global": "D1_global//Please move platform issues to HONGMI",
    "vince_global": "E7 //请移至华勤项目",
    "mido_global": "C6//请移至华勤项目",
    "riva_global": "C3B_global//Please move platform issues to HONGMI",
    "tissot_sprout": "D2A_global_AndroidOne//Please move to HQ",
    "ugg_global": "D6S //请移至龙旗项目",
    "ugglite_global": "D6 //请移至龙旗项目",
    "nikel_global": "B6L //请移至龙旗项目",
    "jasmine_sprout": "D2S_global_AndroidOne//Please move to HTH",
    "daisy_sprout": "D1S_global_AndroidOne// Please move to HQ",
    "land_global": "A12 //请移至闻泰项目",
    "lavender_global": "F7A_global//Please move platform issues to HTH",
    "cepheus_global": "F1_global",
    "onc_global": "F6_global//Please move platform issues to HTH",
    # "": "F4_global",
    # "": "C3H_global//Please move to HQ",
    # "": "C3F_global/Please move platform issues to HONGMI",
    "grus_global": "F2_global",
    "andromeda_global": "E5G_global",
    "tiare_global": "C3G_global_AndroidGo//Please move platform issues to HONGMI",
    # "": "C3E_global//Please move platform issues to HONGMI",
    "onclite_global": "F6lite_global//Please move platform issues to HTH",
    "violet_global": "F7B_global//Please move platform issues to HTH",
    # "": "F10_global",
    # "": "F11_global",
    "lotus_global": "F9_global",
    "clover_global": "D9P//请移至华勤项目"
}

MODEL_TAG_ALL_DEVICES = "ALL DEVICES"

LABEL_GLOBAL_DEFAULT = "global"
LABEL_GLOBAL_DEV_CI = "global_dev_ci"


def get_miui_model(mod_device_name):
    if "global" not in mod_device_name and "_sprout" not in mod_device_name:
        mod_device_name += "_global"
    return MODEL_TAG[mod_device_name]


def get_component_assignee(package_name):
    package_name = package_name.rstrip()
    if package_name == GlobalFileExplorer:
        return COMPONENT_GLOBAL_FILE_EXPLORE, "zhouhongyu"
    if package_name == MUSIC:
        return COMPONENT_GLOBAL_MUSIC, "chenpeng7"
    if package_name == GlobalThemeManager:
        return COMPONENT_GLOBAL_THEME, "chenpeng7"
    if package_name == (GlobalMIUIHome, MintLauncher):
        return COMPONENT_POCO_LAUNCHER, "lvjian1"
    if package_name == FunnyPuriVideo:
        return COMPONENT_GLOBAL_TREND_NEWS, "hanmengmeng"
    if package_name == MintBrowser:
        return COMPONENT_GLOBAL_BROWSER, "chenchao12"
    if package_name == Browser:
        return COMPONENT_GLOBAL_BROWSER, "huangxueqing"
    if package_name == MiDrop:
        return COMPONENT_GLOBAL_MI_DROP, "cuixiang"
    if package_name == (PersonalAssistant, MIUIHome):
        return COMPONENT_GLOBAL_PERSONAL_ASSISTANT, "liwenquan"
    if package_name == (DownloadUi, Download):
        return COMPONENT_GLOBAL_DOWNLOAD_MANAGER, "dingtianmeng"

    return None, None
