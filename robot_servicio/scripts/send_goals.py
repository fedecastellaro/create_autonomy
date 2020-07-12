#!/usr/bin/env python

import rospy
import scanf
from std_msgs.msg import String


class send_goals():
    def __init__(self):
        self.sec_1_table_1 = "('1',)"
        self.goals = rospy.Publisher('/create1/move_base_goals', String, queue_size=10)

        rospy.sleep(5)  # wait to be ready for publish
        r = rospy.Rate(1) # 1 Hz

        print_menu()

        while not rospy.is_shutdown():
            string_read = scanf.scanf("%s")

            int_read =  int(string_read[0])

            if (int_read == 1):
                self.goals.publish("sec_1_table_1")
            elif (int_read == 2):
                self.goals.publish("sec_1_table_2")
            elif (int_read == 3):
                self.goals.publish("sec_1_table_3")
            elif (int_read == 4):
                self.goals.publish("sec_2_table_left")
            elif (int_read == 5):
                self.goals.publish("sec_2_table_right")
            elif (int_read == 6):
                self.goals.publish("sec_3_table_small_1")
            elif (int_read == 7):
                self.goals.publish("sec_3_table_small_2")
            elif (int_read == 8):
                self.goals.publish("sec_3_table_big")
            else:
                rospy.logwarn("\n Invalid argument \n")
                print_menu()
                
            r.sleep()


def print_menu():
    rospy.logwarn("\n \n \n \
        1. sec_1_table_1 \t \t 2. sec_1_table_2 \t \t 3. sec_1_table_3 \n \
        4. sec_2_table_left \t \t 5. sec_2_table_right \n \
        6. sec_3_table_small_1 \t 7. sec_3_table_small_2 \t 8. sec_3_table_big \n \
        \n Opcion: ")



if __name__ == '__main__':
    rospy.init_node('send_goals')
    send_goals()