# Param from manifest
PACKAGE_NAME = "cn.xckj.talk_junior"
MONKEY_COMMAND = "monkey -v --throttle 300 --pct-touch 30 --pct-motion 20 --pct-nav 20 --pct-majornav 15 " \
                 "--pct-appswitch 5 --pct-anyevent 5 --pct-trackball 0 --pct-appswitch 0 --pct-syskeys 0 " \
                 "--ignore-crashes --ignore-timeouts --bugreport -p "
CI_TEST_RECORD_ID = "CI_TEST_RECORD_ID"
MONKEY_ROUND = "MONKEY_ROUND"
MONKEY_ROUND_MAXIMUM_TIME = "MONKEY_ROUND_MAXIMUM_TIME"
MONKEY_SEED = "MONKEY_SEED"
MONKEY_PARAM = "MONKEY_PARAM"
TARGET_LANGUAGE = "TARGET_LANGUAGE"
TARGET_REGION = "TARGET_REGION"
TESTER = "TESTER"
ISSUE_WATCHERS = "ISSUE_WATCHERS"
MONKEY_CHECK_INTERVAL_SECOND = 60

AI_CLASS_ROOM_ACTIVITY = "cn.xckj.talk_junior/cn.xckj.talk.module.classroom.classroom.ClassRoomPicBookActivity"


