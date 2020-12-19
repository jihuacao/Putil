usage()
{
cat << EOF
    usage: [environ data] $0 options

    environ data:
        remote_debug: 使用remote_debug=True或者remote_debug=true设定环境变量，代表即将进行remote_debug模式
        log_level: 使用log_level=Info等设定log等级
        del_train_time: 使用del_train_time=tim-1.time-2.time-3, 删除训练总目录中的分段训练目录
        train_name: 使用train_name=*name*，设置训练代表性目的以及影响训练子目录的名称
    OPTIONS:
        -g      （指定gpus，使用逗号分隔）ip0:gpu0.gpu1,ip1:gpu0.gpu1 example: 127.0.0.1:0.1.2,127.0.0.2:0,127.0.0.3:0.1
        -w       specify the number of worker for every dataset,（指定数据进程数）
        -b       specify the batch size
        --help   Usage
EOF
}

function print_dict(){
    adict=$1
    for key in $(echo ${!adict[*]}); do 
        echo $key=${adict[$key]}; 
    done
    return 0
}

batch_size=2
n_worker=1
gpus=()
ips=()
base_lr=0.001
while getopts "g:b:w:l:" OPT; do
    case $OPT in
        g) 
            echo 'set gpus: $OPTARG'
            ip_gpu_array=(${OPTARG//,/ })
            for (( i=0;i<${#ip_gpu_array[@]};i++)); do
                echo $i
                #echo ${ip_gpu_array[i]}
                ip_gpu=(${ip_gpu_array[i]//:/ })
                # 获取一个ip加一组gpu，如果没有指定ip，那么默认为127.0.0.1， 如果127.0.0.1已经存在了，那么一场结束
                if [ ${#ip_gpu[@]} -eq 1 ]; then 
                    echo 'only specify the gpu'
                    ip=127.0.0.1
                    gpu=${ip_gpu[0]}
                else
                    ip=${ip_gpu[0]}
                    gpu=${ip_gpu[1]}
                fi
                amount=(${gpu//./ })
                amount=${#amount[@]}
                gpus[$i]=$gpu
                ips[$i]=$ip
                #if [ $i -ne 0] then
                #    if [[ "$list_name" =~ "$var" ]]
                #    then
                #        ${var}
                #    fi
                #fi
                echo 'get ip:gpu:amount' ${ips[$i]}':' ${gpus[$i]}':' $amount
            done
            ;;
        b)
            echo "set batch size: $OPTARG"
            batch_size=$OPTARG
            ;;
        w)
            echo "set n_worker: $OPTARG"
            n_worker=$OPTARG
            ;;
        l)
            echo "set base_lr: $OPTAVG"
            base_lr=$OPTARG
            ;;
        ?)
            usage
            exit
            ;;
    esac
done

# 获取horovod中的H,np与main中的gpus参数
gpus_arg=
horovod_np_arg=0
horovod_H_arg=
if [ ${#gpus[@]} -eq 0 ] && [ ${#ips[@]} -eq 0 ]; then
    gpus[0]=0
    ips[0]=127.0.0.1
fi
for (( i=0;i<${#gpus[@]};i++ )); do
    gpus_arg=$(echo $gpus_arg ${gpus[$i]})
    echo 'gpu data:' ${gpus[$i]}
    amount=(${gpus[$i]//./ })
    amount=${#amount[@]}
    echo amount: $amount
    if [ -z'$horovod_np_arg' ]; then 
        echo 'empty'
        horovod_H_arg=$horovod_H_arg
    else 
        horovod_H_arg=$horovod_H_arg,
    fi
    horovod_H_arg=$(echo $horovod_H_arg${ips[$i]}:$amount)
    horovod_np_arg=$[$horovod_np_arg+$amount]
done
echo gpus_arg: $gpus_arg horovod_np_arg: $horovod_np_arg horovod_H_arg: $horovod_H_arg

# remote_debug 相关解析
if [ $remote_debug ] && ([ $remote_debug == 'true' ] || [ $remote_debug == 'True' ]); then
    echo "set remote_debug mode"
    remote_debug_arg=--remote_debug
else
    remote_debug_arg=
fi

# log_level 相关解析
if [ $log_level ]; then
    log_level_arg=--log_level=$log_level
    echo 'set log_level:' $(echo $log_level) $log_level_arg
else
    # Default: log_level
    log_level_arg=--log_level=Info
fi

# del_train_time 相关解析
if [ $del_train_time ]; then
    clean_train_arg=--clean_train' '${del_train_time//./ }
    echo 'set del train time:' ${del_train_time//./ } $clean_train_arg
else
    # Default: clean_train
    clean_train_arg=
fi

# train_name 相关解析
if [ $train_name ]; then
    train_name_arg=--train_name=$(echo $train_name)
    echo 'set train name:' $(echo $train_name) $train_name_arg
else
    # Default: train_name
    train_name_arg=
fi

declare -A sources
sources=(
[auto_save_source]=standard [auto_save_name]=DefaultAutoSave
[auto_stop_source]=standard [auto_stop_name]=DefaultAutoStop
[lr_reduce_source]=standard [lr_reduce_name]=DefaultLrReduce
[dataset_source]=standard [dataset_name]=DefaultDataset
[data_loader_source]=standard [data_loader_name]=DefaultDataLoader
[data_sampler_source]=standard [data_sampler_name]=DefaultDataSampler
[encode_source]=standard [encode_name]=DefaultEncode
[backbone_source]=standard [backbone_name]=DefaultBackbone 
[backend_source]=standard [backend_name]=DefaultBackend 
[decode_source]=standard [decode_name]=DefaultDecode
[loss_source]=standard [loss_name]=DefaultLoss
[indicator_source]=standard [indicator_name]=DefaultIndicator
[statistic_indicator_source]=standard [statistic_indicator_name]=DefaultStatisticIndicator 
[optimization_source]=standard [optimization_name]=DefaultOptimization
[aug_sources]=standard [aug_names]=DefaultAug
[data_type_adapter_source]=standard [data_type_adapter_name]=DefaultDataTypeAdapter
[fit_data_to_input_source]=standard [fit_data_to_input_name]=DefaultFitDataToInput
[fit_decode_to_result_source]=standard [fit_decode_to_result_name]=DefaultFitDecodeToResult
[recorder_source]=standard [recorder_name]=DefaultRecorder
[accumulated_opt_source]=standard [accumulated_opt_name]=DefaultAccumulatedOpt
)
## 从脚本外获取手动设置的环境变量
for key in $(echo ${!sources[*]}); do
    if [ $(eval echo '$'$key) ]; then
        echo 'manual set' $key 'from' ${sources[$key]}'(default)-->' $(eval echo '$'$key)
        sources[$key]=$(eval echo '$'$key)
    else
        sources[$key]=${sources[$key]}
    fi
done

# 生成环境变量语句
env_set_command=
for key in $(echo ${!sources[*]}); do
    env_set_command=$(echo $env_set_command $key=${sources[$key]})
done
echo env_command: $env_set_command