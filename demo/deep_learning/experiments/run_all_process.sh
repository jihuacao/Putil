# 需要进行运行的点：
# first command: train->save,checkpoint,deploy->lr_reduce->not stop->evaluate->test->
# train->no lr_reduce->not stop->evaluate->save,checkpoint,deploy->lr_reduce->stop->
# load checkpoint->first command content->load saved->run evaluate->load save->test
# 获取shell参数
# sources与name的默认环境值
source ./experiments/common.sh
$env_command \
horovodrun -np $horovod_np_arg -H $horovod_H_arg --start-timeout=100 python main.py --help \
#--debug \
#--batch_size=$batch_size \
#--n_worker_per_dataset=$n_worker \
#--gpus $gpus_arg \
#$remote_debug_arg \