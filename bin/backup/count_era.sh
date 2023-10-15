#!/bin/bash

num=`./count_era.py`
num_j_Astar=`echo $num | awk '{ print $1 }'`
num_j_A=`echo $num | awk '{ print $2 }'`
num_Conf_A=`echo $num | awk '{ print $3 }'`

cat ../fullpaper.jemdoc | sed s/_ERA_ASTAR_/$num_j_Astar/g  \
                        | sed s/_ERA_A_/$num_j_A/g  \
                        | sed s/_ERA_ACONF_/$num_Conf_A/g     > ../_tmp

mv  -f ../_tmp ../fullpaper.jemdoc

cat ../fullpaper2.jemdoc | sed s/_ERA_ASTAR_/$num_j_Astar/g \
                        | sed s/_ERA_A_/$num_j_A/g  \
                        | sed s/_ERA_ACONF_/$num_Conf_A/g     > ../_tmp

mv  -f ../_tmp ../fullpaper2.jemdoc


