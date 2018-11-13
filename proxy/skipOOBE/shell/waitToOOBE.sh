#!/usr/bin/env bash
serial=$1

adb_command="adb -s $serial"

waitToOOBE() {

    echo "waitToOOBE(): >>";
    $adb_command shell input keyevent 26
    len=0
    array=$($adb_command shell dumpsys window | grep  mFocusedApp | grep com.android.provision | grep -v AppWindowToken);
    len=${#array}
    echo "$len";

  while [ $len -eq "0" ]
   do

    $adb_command shell input keyevent 26
    echo "waitToOOBE(): sleep 5";
    sleep 5;

	array=$($adb_command shell dumpsys window | grep  mFocusedApp | grep com.android.provision | grep -v AppWindowToken);
	len=${#array}

  done

    echo "waitToOOBE(): << ";
}

waitToOOBE
