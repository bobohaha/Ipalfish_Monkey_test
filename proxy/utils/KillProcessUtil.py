import os


class KillProcessUtil:

    @staticmethod
    def kill_device_process(serial, process_name):

        print "kill_device_process(): >> serial is " + serial + ", process_name is " + process_name

        command = "adb -s " + serial + " shell ps -A | grep -i " + process_name + " | cut -d ' ' -f 2-11"
        output = os.popen(command)
        process_id_rst = output.read().strip()
        if ( len(process_id_rst) > 1 ):
            process_id_str = process_id_rst.replace(" ", "")
            process_id_str = process_id_str.replace("\n", ",")
            process_id_ary = process_id_str.split(",")

            for process_id in process_id_ary:
                print "kill_device_process(): id is " + process_id
                command = "adb -s " + serial + " shell kill -9 " + process_id
                os.system(command)

            print "kill_device_process(): << "
        else:
            pass

    @staticmethod
    def kill_process(process_name):

        print "kill_process(): >> process_name is " + process_name

        command = "ps -aux | grep " + process_name + " | grep -r color | cut -d ' ' -f 5-6"

        output = os.popen(command)
        process_id_rst = output.read().strip()
        if ( len(process_id_rst) > 1 ):
            process_id_str = process_id_rst.replace(" ", "")
            process_id_str = process_id_str.replace("\n", ",")
            process_id_ary = process_id_str.split(",")

            for process_id in process_id_ary:
                print "kill_process(): id is " + process_id
                command = "kill -9 " + process_id
                os.system(command)

            print "kill_process(): << "
        else:
            pass

# KillProcessUtil.kill_device_process("117cf09", "com.android.commands.monkey")
#KillProcessUtil.kill_process("press")




