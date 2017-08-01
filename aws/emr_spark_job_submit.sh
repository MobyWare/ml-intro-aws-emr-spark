aws emr create-cluster \
--name "HAIL Cluster - Spark Step (No Debug)" \
--applications Name=Hadoop Name=Hive Name=Pig Name=Ganglia Name=Spark \
--ec2-attributes KeyName=hail-dickm-emr-key,InstanceProfile=EMR_EC2_DefaultRole \
--ami-version 5.7.0 --log-uri s3://hail-dickm-emr/emr-logs/ \
--steps Name="PySpark Word Count",Type=CUSTOM_JAR,ActionOnFailure=TERMINATE_CLUSTER,Jar=command-runner.jar,Args=[spark-submit,--master,yarn,--deploy-mode,cluster,s3://hail-dickm-emr/scripts/wordcount.py] \
--instance-groups \
InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m4.large \
InstanceGroupType=CORE,InstanceCount=1,InstanceType=m4.large \
--service-role EMR_DefaultRole --auto-terminate --region us-east-1 --no-verify-ssl