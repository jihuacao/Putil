# frame debug
--frame_debug \
--epochs=2 \
--naug \
--log_interval=1 \
--summary_interval=1 \
--evaluate_interval=1 \
--compute_efficiency \
--data_rate_in_compute_efficiency=@the data rate to compute the efficiency \
--batch_size=@the batch size \
--train_data_using_rate=@the data rate which provide two batch size \
--evaluate_data_using_rate=@the dataa rate which provide two batch size \
--test_batch_size=@the test batch size \
--test_data_using_rate=@the data rate which provide two test batch size \
# overfit model
--evaluate_off \
--test_off \
--evaluate_data_using_rate=-1 \
--test_data_using_rate=-1 \
--epoch=-1 \
--naug \
--evaluate_interval=-1
--batch_size=@the batch size \
--train_data_using_rate=@the suitable data rate for train data
