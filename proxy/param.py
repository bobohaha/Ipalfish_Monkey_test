from params import CaseName
from params import Language
from params import PackageName
from params import Region

# Param from manifest
PACKAGE_NAME = "PACKAGE_NAME"
TEST_APK_BUILD_VERSION = "TEST_APK_BUILD_VERSION"

# Need connect wifi in OOBE
NEED_CONNECT_WIFI_DEVICE = []
IS_NEED_CONNECT_WIFI_KEY = "isNeedConnectWifi"
IS_NEED_CONNECT_WIFI_VALUE = "true"

# Need choosing region and language
TEST_REGION_KEY = "Locale"
TEST_LANGUAGE_KEY = "Language"

# REGION configuration
TEST_REGION_DEFAULT = Region.INDIA

# Device list on different region
TEST_REGION_DEVICE = {}

# Package list on different region
TEST_REGION_PACKAGE = {Region.RUSSIA: [PackageName.GAME_CENTER]}

TEST_LANGUAGE_DEFAULT = Language.ENGLISH_US

# Region and language dictionary
TEST_REGION_LANGUAGE = {Region.TAIWAN: Language.TRADITIONAL_CHINESE}

# Package list on different language
TEST_LANGUAGE_PACKAGE = {}

PRESETTING_DEFAULT_CASE_NAME = CaseName.COMMON_PRESETTING
# Case list on different package
PRESETTING_CASE_PACKAGE = {PackageName.GAME_CENTER: CaseName.GAME_CENTER_PRESETTING,
                           PackageName.MUSIC: CaseName.MUSIC_PRESETTING,
                           PackageName.GlobalMIUIHome: CaseName.POCO_LAUNCHER_PRESETTING,
                           PackageName.FunnyPuriVideo: CaseName.PANI_PURI_PRESETTING,
                           PackageName.GlobalFileExplorer: CaseName.GLOBAL_FILE_EXPLORER_PRESETTING,
                           PackageName.MiDrop: CaseName.MI_DROP_PRESETTING,
                           PackageName.Browser: CaseName.BROWSER_PRESETTING,
                           PackageName.MintBrowser: CaseName.MINT_BROWSER_PRESETTING,
                           PackageName.Download: CaseName.DOWNLOAD_PRESETTING,
                           PackageName.MintLauncher: CaseName.POCO_LAUNCHER_PRESETTING,
                           PackageName.PersonalAssistant: CaseName.GLOBAL_PERSONAL_ASSISTANT_PRESETTING}

# Package need local resource
PACKAGE_NEED_LOCAL_RESOURCE = [PackageName.MUSIC,
                               PackageName.MiDrop,
                               PackageName.GlobalFileExplorer,
                               PackageName.FunnyPuriVideo]

# Package need 100+ local image
PACKAGE_NEED_LOCAL_IMAGE = [PackageName.MiDrop,
                            PackageName.GlobalFileExplorer]
