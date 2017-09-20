# Goal

The goals are to:
1. Submit Spark job from arbitrary EC2 instance to EMR 
2. Interactively run Spark Jobs using Jupyter/JupyterHub from EMR
3. Submit Spark job from CLI to a ephemeral EMR cluster that ends after job
4. Learn about deploying JupyterHub with Spark-capability on Kurbernetes in AWS

# Submitting Spark Jobs
Before you can do these instructions there are some known attributes the AWS environment needs to have. Such as:
The EC2 instance most be in a VPC with network access to the IPs represented on the EMR cluster.
The steps in this article, [Configuring Zeppelin for EMR](), should have been followed to store the EMR cluster in S3 or you can copy the directories indicated in the article after the cluster has been deployed using __*SCP*__ or some other utility.

## 1) Set up EC2 with Spark
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


### Set up native access to S3
1. Follow instrucitons in this [install guide for hadoop 2.6](http://www.rexamine.com/2015/02/installing-hadoop-2-6-0-on-centos-7/) to set up hadoop client on EC2
2. Update entries in bash\_profile so that HADOOP\_CONF\_DIR is set to SPARK\_HOME/conf
3. Update the classpath for hadoop [to include hadoop-aws-[version].jar](https://stackoverflow.com/questions/28029134/how-can-i-access-s3-s3n-from-a-local-hadoop-2-6-installation)



### Known issues
__*Unknow option -9, JVM*__
If you get an error with verbiage about, you should check that the HADOOP_OPTS variable is valid in `HADOOP\_CONF\_DIR/hadoop-env.sh`. I just replaced the spark one with the options in the orignal tar ball.

__*Validate Spark can hit EMR*__
Validate using hadoop command `hadoop fs -ls /`. *If you get a list of directories and no errors it worked*

_TO DO_

## 2) Set up Jupyter
_TO DO_

## 3) Set up Jupyter Hub
