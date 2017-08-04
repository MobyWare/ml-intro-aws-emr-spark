aws emr create-cluster --applications Name=Hadoop Name=Hive Name=Pig Name=Ganglia Name=Spark \
--tags 'RUN_TYPE=TRANSIENT' 'Project=HAIL' 'Environment=HAIL-DEV' \
--ec2-attributes '{"KeyName":"hail-dickm-emr-key","InstanceProfile":"EMR_EC2_DefaultRole","SubnetId":"subnet-3f61ed65","EmrManagedSlaveSecurityGroup":"sg-6a80c41b","EmrManagedMasterSecurityGroup":"sg-cf8cc8be"}' \
--release-label emr-5.7.0 --log-uri 's3n://hail-dickm-emr/emr-logs/' \
--steps '[{"Args":["spark-submit","--deploy-mode","cluster","s3://hail-dickm-emr/scripts/wordcount.py"],"Type":"CUSTOM_JAR","ActionOnFailure":"TERMINATE_CLUSTER","Jar":"command-runner.jar","Properties":"","Name":"PySpark Word Count"}]' \
--instance-groups '[{"InstanceCount":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":1}]},"InstanceGroupType":"CORE","InstanceType":"m4.2xlarge","Name":"Core - 2"},{"InstanceCount":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":1}]},"InstanceGroupType":"MASTER","InstanceType":"m4.2xlarge","Name":"Master - 1"}]' \
--auto-terminate --auto-scaling-role EMR_AutoScaling_DefaultRole --service-role EMR_DefaultRole \
--enable-debugging --name 'HAIL Initial Cluster (Spark Step)' \
--scale-down-behavior TERMINATE_AT_INSTANCE_HOUR --region us-east-1