from euler import EulerEstimation


if __name__== "__main__":
    with open("lambda.txt") as f:
        ll = f.readlines()
        lambda_list = list()
        
        for l in ll:
            l_list = [int(x) for x in l.split()]
            lambda_list.append(l_list)
        
        
        forward_euler_values = list()
        backward_euler_values = list()

        euler_map = dict()

        for l in lambda_list:
            key_str = ""
            for lstr in l:
                key_str += str(lstr)
            euler_map[key_str] = dict()
            for count in range(0,5):
                step_size = abs((2*1.0/l[0]))/pow(2, count)
                #print "STEPPPPP SIZEEEEEE %lf"%step_size
                euler_map[key_str][str(step_size)] = dict() 
                #print step_size, l[0]
                e = EulerEstimation(step_size, 25, 200, l[0])
                euler_map[key_str][str(step_size)]["for_euler"] = list()
                euler_map[key_str][str(step_size)]["back_euler"] = list() 
                euler_map[key_str][str(step_size)]["for_euler"].append(e.estimate_using_forward_euler())
                euler_map[key_str][str(step_size)]["back_euler"].append(e.estimate_using_backward_euler())


        print euler_map

