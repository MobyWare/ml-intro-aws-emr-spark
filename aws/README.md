# Goals

The goals are to:

1. Submit Spark job from arbitrary EC2 instance to EMR 
2. Interactively run Spark Jobs using Jupyter/JupyterHub from EMR
3. Submit Spark job from CLI to a ephemeral EMR cluster that ends after job
4. Learn about deploying JupyterHub with Spark-capability on Kurbernetes in AWS

# Submitting Spark Jobs
Before you can do these instructions there are some known attributes the AWS environment needs to have. Such as:
The EC2 instance most be in a VPC with network access to the IPs represented on the EMR cluster.
The steps in this article, [Configuring Zeppelin for EMR](https://aws.amazon.com/blogs/big-data/running-an-external-zeppelin-instance-using-s3-backed-notebooks-with-spark-on-amazon-emr/), should have been followed to store the EMR cluster in S3 or you can copy the directories indicated in the article after the cluster has been deployed using __*SCP*__ or some other utility.

# 1) Set up EC2 with Spark
__*Steps*__

Once the listed pre-requistes are complete, you need to complete the following to set up the instance to communicate with Spark on EMR.

1. Launch the instance in the VPC with visibility to the EMR cluster.
2. Install the following:
    a. Build essential (Debian distro) or Developer Tools (Fedora distro). Used to upgrade Java.
    b. Java (JDK) >= 1.8.0
    c. Python - I recommend Anaconda. See this [link](https://repo.continuum.io/archive/) for the install scripts for linux. We used version 4.4.0 (64-bit).
    d. Spark. We used version 2.2.1
3. Configure SPARK\_HOME in .bash_profile to point to directory with Spark
4. Copy the configuration files from the pre-requisite steps (from S3) to SPARK_HOME/conf. You may want to back up the old dir.
5. Set HADOOP\_CONFIG\_DIR to the $SPARK\_HOME/conf
6. Set JAVA\_HOME in `$HADOOP\_CONF\_DIR/hadoop-env.sh`.
7. Set HADOOP\_USER\_NAME to _hadoop_ (default user on EMR clusters). You can see [Runing Spark on YARN](https://spark.apache.org/docs/2.1.1/running-on-yarn.html) for more details.
8. Update jupyter configuration to not launch browser and to accept external requests by setting NotebookApp.ip to '*' and NotebookApp.open_browser = False.


## Set up native access to S3
1. Follow instrucitons in this [install guide for hadoop 2.6](http://www.rexamine.com/2015/02/installing-hadoop-2-6-0-on-centos-7/) to set up hadoop client on EC2
2. Update entries in bash\_profile so that HADOOP\_CONF\_DIR is set to SPARK\_HOME/conf
3. Update the classpath for hadoop [to include hadoop-aws-[version].jar](https://stackoverflow.com/questions/28029134/how-can-i-access-s3-s3n-from-a-local-hadoop-2-6-installation)


__*Validate Spark can hit EMR*__

Validate using hadoop command `hadoop fs -ls /`. *If you get a list of directories and no errors it worked*


# 2) Set up Jupyter
Given that the anaconda package you can launch jupyter notebooks connected to the cluster by following the steps below. This assumes that you are forwarding the default Jupyter server port (i.e. 8888) to your local machine:
1. Setting `PSYPARK_DIRVER_PYTHON` and `PSYPARK_DIRVER_PYTHON_OPTS` to _jupyter_ and _notebook_ respectively.
2. Launch notebook with command `$SPARK_HOME/bin/pyspark --master yarn --deploy-mode client`
3. Navigate  your browser to 


# 3) Submit jobs using CLI
You can submit a job from the Client EMR given that yarn is configure per step 1. Use this command:

> spark-submit --deploy-mode cluster --master yarn `path/to/script.py` `script args`

You can create an ephemeral cluster that runs and app and destroys it using a cli command in the form:

> aws emr create-cluster \
> --name `cluster name` \
> --applications Name=Hadoop Name=Ganglia Name=Spark \
> --ec2-attributes KeyName=`key name`,InstanceProfile=EMR_EC2_DefaultRole \
> --ami-version 5.7.0 --log-uri `s3/log/path` \
> --steps Name=`step name`,Type=CUSTOM_JAR,ActionOnFailure=TERMINATE_CLUSTER,Jar=command-runner.jar,Args=[spark-submit,--master,yarn,--deploy-mode,cluster,`/path/to/script.py`] \
> --instance-groups \
> InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m4.large \
> InstanceGroupType=CORE,InstanceCount=`initial count`,InstanceType=`instance type` \
> --service-role EMR_DefaultRole --auto-terminate --region `region` 


Here is an example command with a python script file with the key name, EC2 family and region set:

> aws emr create-cluster \
> --name "HAIL Cluster - Spark Step (No Debug)" \
> --applications Name=Hadoop Name=Hive Name=Pig Name=Ganglia Name=Spark \
> --ec2-attributes KeyName=hail-dickm-emr-key,InstanceProfile=EMR_EC2_DefaultRole \
> --ami-version 5.7.0 --log-uri s3://hail-dickm-emr/emr-logs/ \
> --steps Name="PySpark Word Count",Type=CUSTOM_JAR,ActionOnFailure=TERMINATE_CLUSTER,Jar=command-runner.jar,Args=[spark-submit,--master,yarn,--deploy-mode,cluster,s3://hail-dickm-emr/scripts/wordcount.py] \
> --instance-groups \
> InstanceGroupType=MASTER,InstanceCount=1,InstanceType=m4.large \
> InstanceGroupType=CORE,InstanceCount=1,InstanceType=m4.large \
>--service-role EMR_DefaultRole --auto-terminate --region us-east-1

# 4) Set up Jupyter Hub
__TDB__

# Known issues
__*Unknow option -9, JVM*__

If you get an error with verbiage about, you should check that the HADOOP_OPTS variable is valid in `HADOOP\_CONF\_DIR/hadoop-env.sh`. I just replaced the spark one with the options in the orignal tar ball.

__*Error creating jupyter directory*__

I am not sure of a resolution. According to this [article](https://stackoverflow.com/questions/38984211/spark-2-0-java-io-ioexception-cannot-run-program-jupyter-error-2-no-such) it has to do with setting `PSPARK_PYTHON` env on the cluster.
