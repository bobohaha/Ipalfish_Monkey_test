serial=$1
adb_command="adb -s $serial"

lockPressHome() {

    echo "lockPressHome(): >> "

	#open power
	$adb_command shell input keyevent 224

	#unlock
    $adb_command shell input swipe 300 1000 300 500


  while [ True ]
   do


	#echo "Sending press home "

	$adb_command shell input keyevent 4
	$adb_command shell input keyevent 3

	echo "lockPressHome(): shell input keyevent 4, 3 and sleep 2s"

	sleep 2

  done




	echo "lockPressHome(): << "

}

lockPressHome
